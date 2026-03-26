"""
ShroudbKeep client.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbKeepError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import AuthResponse, DeleteResponse, GetResponse, ListResponse, PutResponse, RotateResponse, VersionsResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbKeep connection URI.

    Supported formats::

        shroudb-keep://localhost
        shroudb-keep://localhost:6899
        shroudb-keep+tls://prod.example.com
        shroudb-keep://mytoken@localhost:6899
        shroudb-keep://mytoken@localhost/sessions
        shroudb-keep+tls://tok@host:6899/keys
    """
    tls = False
    if uri.startswith("shroudb-keep+tls://"):
        tls = True
        rest = uri[len("shroudb-keep+tls://"):]
    elif uri.startswith("shroudb-keep://"):
        rest = uri[len("shroudb-keep://"):]
    else:
        raise ValueError(f"Invalid ShroudbKeep URI: {uri}  (expected shroudb-keep:// or shroudb-keep+tls://)")

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


class ShroudbKeepClient:
    """Async client for the ShroudbKeep Secrets manager.

    Connect using a ShroudbKeep URI::

        async with await ShroudbKeepClient.connect("shroudb-keep://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbKeepClient.connect("shroudb-keep+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbKeepClient.connect("shroudb-keep://localhost", max_idle=8)
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
        uri: str = "shroudb-keep://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbKeepClient":
        """Connect to a ShroudbKeep server.

        Args:
            uri: ShroudbKeep connection URI.
                 Format: ``shroudb-keep://[token@]host[:port][/keyspace]``
                 or ``shroudb-keep+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbKeepClient instance.

        Examples::

            client = await ShroudbKeepClient.connect("shroudb-keep://localhost")
            client = await ShroudbKeepClient.connect("shroudb-keep+tls://token@host:6899/keys")
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

    async def __aenter__(self) -> "ShroudbKeepClient":
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

    async def auth(self, token: Any) -> AuthResponse:
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        result = await self._execute(*args)
        return AuthResponse._from_dict(result)


    async def delete(self, path: str) -> DeleteResponse:
        """Soft-delete a secret"""
        args: list[str] = []
        args.append("DELETE")
        args.append(str(path))
        result = await self._execute(*args)
        return DeleteResponse._from_dict(result)


    async def get(self, path: str, version: Optional[int] = None) -> GetResponse:
        """Retrieve a secret (latest or specific version)"""
        args: list[str] = []
        args.append("GET")
        args.append(str(path))
        if version is not None:
            args.extend(["VERSION", str(version)])
        result = await self._execute(*args)
        return GetResponse._from_dict(result)


    async def health(self, path: Optional[str] = None) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if path is not None:
            args.append(str(path))
        result = await self._execute(*args)


    async def list(self, prefix: Optional[str] = None) -> ListResponse:
        """List secret paths matching a prefix"""
        args: list[str] = []
        args.append("LIST")
        if prefix is not None:
            args.append(str(prefix))
        result = await self._execute(*args)
        return ListResponse._from_dict(result)


    async def put(self, path: str, value: str, meta: Optional[str] = None) -> PutResponse:
        """Store a secret (creates a new version)"""
        args: list[str] = []
        args.append("PUT")
        args.append(str(path))
        args.append(str(value))
        if meta is not None:
            args.extend(["META", str(meta)])
        result = await self._execute(*args)
        return PutResponse._from_dict(result)


    async def rotate(self, path: str) -> RotateResponse:
        """Re-encrypt the latest version under the current key"""
        args: list[str] = []
        args.append("ROTATE")
        args.append(str(path))
        result = await self._execute(*args)
        return RotateResponse._from_dict(result)


    async def versions(self, path: str) -> VersionsResponse:
        """Show version history for a secret"""
        args: list[str] = []
        args.append("VERSIONS")
        args.append(str(path))
        result = await self._execute(*args)
        return VersionsResponse._from_dict(result)

