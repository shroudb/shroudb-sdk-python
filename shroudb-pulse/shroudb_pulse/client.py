"""
ShroudbPulse client.

Auto-generated from shroudb-pulse protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbPulseError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import ActorsResponse, AuthResponse, CountResponse, ErrorsResponse, HotspotsResponse, IngestResponse, IngestBatchResponse, QueryResponse, SourceListResponse, SourceStatusResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbPulse connection URI.

    Supported formats::

        shroudb-pulse://localhost
        shroudb-pulse://localhost:7099
        shroudb-pulse+tls://prod.example.com
        shroudb-pulse://mytoken@localhost:7099
        shroudb-pulse://mytoken@localhost/sessions
        shroudb-pulse+tls://tok@host:7099/keys
    """
    tls = False
    if uri.startswith("shroudb-pulse+tls://"):
        tls = True
        rest = uri[len("shroudb-pulse+tls://"):]
    elif uri.startswith("shroudb-pulse://"):
        rest = uri[len("shroudb-pulse://"):]
    else:
        raise ValueError(f"Invalid ShroudbPulse URI: {uri}  (expected shroudb-pulse:// or shroudb-pulse+tls://)")

    auth_token = None
    if "@" in rest:
        auth_token, rest = rest.split("@", 1)

    keyspace = None
    if "/" in rest:
        rest, keyspace = rest.split("/", 1)
        if not keyspace:
            keyspace = None

    host = rest
    port = DEFAULT_PORT
    if ":" in host:
        host, port_str = host.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            port = DEFAULT_PORT

    return {
        "host": host,
        "port": port,
        "tls": tls,
        "auth_token": auth_token,
        "keyspace": keyspace,
    }


class Subscription:
    """Async iterator for subscription events. Use as async context manager."""

    def __init__(self, conn: _Connection) -> None:
        self._conn = conn

    async def __aenter__(self) -> "Subscription":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    def __aiter__(self) -> "Subscription":
        return self

    async def __anext__(self) -> SubscriptionEvent:
        try:
            frame = await self._conn._read_frame()
            if isinstance(frame, list) and len(frame) >= 5 and frame[0] == "event":
                return SubscriptionEvent._from_frame(frame)
            return await self.__anext__()
        except (ConnectionError, asyncio.IncompleteReadError):
            raise StopAsyncIteration

    async def close(self) -> None:
        """Close the underlying connection, ending the subscription."""
        await self._conn.close()


class ShroudbPulseClient:
    """Async client for the ShroudbPulse Observability plane for unified audit event streaming.

    Connect using a ShroudbPulse URI::

        async with await ShroudbPulseClient.connect("shroudb-pulse://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbPulseClient.connect("shroudb-pulse+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbPulseClient.connect("shroudb-pulse://localhost", max_idle=8)
    """

    def __init__(
        self,
        pool: _Pool,
        *,
        host: str,
        port: int,
        tls: bool,
        auth: str | None,
    ) -> None:
        self._pool = pool
        self._host = host
        self._port = port
        self._tls = tls
        self._auth = auth

    @classmethod
    async def connect(
        cls,
        uri: str = "shroudb-pulse://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbPulseClient":
        """Connect to a ShroudbPulse server.

        Args:
            uri: ShroudbPulse connection URI.
                 Format: ``shroudb-pulse://[token@]host[:port][/keyspace]``
                 or ``shroudb-pulse+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbPulseClient instance.

        Examples::

            client = await ShroudbPulseClient.connect("shroudb-pulse://localhost")
            client = await ShroudbPulseClient.connect("shroudb-pulse+tls://token@host:7099/keys")
        """
        cfg = parse_uri(uri)
        pool = _Pool(
            cfg["host"],
            cfg["port"],
            tls=cfg["tls"],
            auth=cfg["auth_token"],
            max_idle=max_idle,
            max_open=max_open,
        )
        return cls(
            pool,
            host=cfg["host"],
            port=cfg["port"],
            tls=cfg["tls"],
            auth=cfg["auth_token"],
        )

    async def close(self) -> None:
        """Close the client and all pooled connections."""
        await self._pool.close()

    async def __aenter__(self) -> "ShroudbPulseClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _execute(self, *args: str) -> Any:
        """Acquire a pooled connection, execute, and return it."""
        conn = await self._pool.get()
        try:
            result = await conn.execute(*args)
            await self._pool.put(conn)
            return result
        except Exception:
            await conn.close()
            raise

    def pipeline(self) -> "Pipeline":
        """Create a pipeline for batching commands.

        Usage::

            async with client.pipeline() as pipe:
                pipe.issue("keyspace", ttl_secs=3600)
                pipe.verify("keyspace", token)
                results = await pipe.execute()
        """
        from ._pipeline import Pipeline
        return Pipeline(self._pool)

    async def actors(self, window: Optional[str] = None) -> ActorsResponse:
        """Most active actors"""
        args: list[str] = []
        args.append("ACTORS")
        if window is not None:
            args.extend(["WINDOW", str(window)])
        result = await self._execute(*args)
        return ActorsResponse._from_dict(result)


    async def auth(self, token: Any) -> AuthResponse:
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        result = await self._execute(*args)
        return AuthResponse._from_dict(result)


    async def count(self) -> CountResponse:
        """Count events matching filter arguments"""
        args: list[str] = []
        args.append("COUNT")
        result = await self._execute(*args)
        return CountResponse._from_dict(result)


    async def errors(self, engine: Optional[str] = None, window: Optional[str] = None) -> ErrorsResponse:
        """Per-operation error rates"""
        args: list[str] = []
        args.append("ERRORS")
        if engine is not None:
            args.extend(["ENGINE", str(engine)])
        if window is not None:
            args.extend(["WINDOW", str(window)])
        result = await self._execute(*args)
        return ErrorsResponse._from_dict(result)


    async def health(self) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        result = await self._execute(*args)


    async def hotspots(self, engine: Optional[str] = None, window: Optional[str] = None) -> HotspotsResponse:
        """Find hotspot resources with highest activity"""
        args: list[str] = []
        args.append("HOTSPOTS")
        if engine is not None:
            args.extend(["ENGINE", str(engine)])
        if window is not None:
            args.extend(["WINDOW", str(window)])
        result = await self._execute(*args)
        return HotspotsResponse._from_dict(result)


    async def ingest(self, json: str) -> IngestResponse:
        """Ingest a single audit event"""
        args: list[str] = []
        args.append("INGEST")
        args.append(str(json))
        result = await self._execute(*args)
        return IngestResponse._from_dict(result)


    async def ingest_batch(self, json: str) -> IngestBatchResponse:
        """Ingest a batch of audit events"""
        args: list[str] = []
        args.append("INGEST_BATCH")
        args.append(str(json))
        result = await self._execute(*args)
        return IngestBatchResponse._from_dict(result)


    async def query(self) -> QueryResponse:
        """Query events with filter arguments"""
        args: list[str] = []
        args.append("QUERY")
        result = await self._execute(*args)
        return QueryResponse._from_dict(result)


    async def source_list(self) -> SourceListResponse:
        """List configured event sources"""
        args: list[str] = []
        args.append("SOURCE_LIST")
        result = await self._execute(*args)
        return SourceListResponse._from_dict(result)


    async def source_status(self) -> SourceStatusResponse:
        """Show per-source ingestion statistics"""
        args: list[str] = []
        args.append("SOURCE_STATUS")
        result = await self._execute(*args)
        return SourceStatusResponse._from_dict(result)

