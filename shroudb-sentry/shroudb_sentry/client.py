"""
ShroudbSentry client.

Auto-generated from shroudb-sentry protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbSentryError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import AuthResponse, EvaluateResponse, KeyInfoResponse, KeyRotateResponse, PolicyInfoResponse, PolicyListResponse, PolicyReloadResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbSentry connection URI.

    Supported formats::

        shroudb-sentry://localhost
        shroudb-sentry://localhost:6799
        shroudb-sentry+tls://prod.example.com
        shroudb-sentry://mytoken@localhost:6799
        shroudb-sentry://mytoken@localhost/sessions
        shroudb-sentry+tls://tok@host:6799/keys
    """
    tls = False
    if uri.startswith("shroudb-sentry+tls://"):
        tls = True
        rest = uri[len("shroudb-sentry+tls://"):]
    elif uri.startswith("shroudb-sentry://"):
        rest = uri[len("shroudb-sentry://"):]
    else:
        raise ValueError(f"Invalid ShroudbSentry URI: {uri}  (expected shroudb-sentry:// or shroudb-sentry+tls://)")

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


class ShroudbSentryClient:
    """Async client for the ShroudbSentry Policy-based authorization engine.

    Connect using a ShroudbSentry URI::

        async with await ShroudbSentryClient.connect("shroudb-sentry://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbSentryClient.connect("shroudb-sentry+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbSentryClient.connect("shroudb-sentry://localhost", max_idle=8)
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
        uri: str = "shroudb-sentry://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbSentryClient":
        """Connect to a ShroudbSentry server.

        Args:
            uri: ShroudbSentry connection URI.
                 Format: ``shroudb-sentry://[token@]host[:port][/keyspace]``
                 or ``shroudb-sentry+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbSentryClient instance.

        Examples::

            client = await ShroudbSentryClient.connect("shroudb-sentry://localhost")
            client = await ShroudbSentryClient.connect("shroudb-sentry+tls://token@host:6799/keys")
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

    async def __aenter__(self) -> "ShroudbSentryClient":
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


    async def evaluate(self, json: str) -> EvaluateResponse:
        """Evaluate an authorization request against loaded policies"""
        args: list[str] = []
        args.append("EVALUATE")
        args.append(str(json))
        result = await self._execute(*args)
        return EvaluateResponse._from_dict(result)


    async def health(self) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        result = await self._execute(*args)


    async def key_info(self) -> KeyInfoResponse:
        """Get signing key information"""
        args: list[str] = []
        args.append("KEY_INFO")
        result = await self._execute(*args)
        return KeyInfoResponse._from_dict(result)


    async def key_rotate(self, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> KeyRotateResponse:
        """Rotate the signing key used for JWT decisions"""
        args: list[str] = []
        args.append("KEY_ROTATE")
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        result = await self._execute(*args)
        return KeyRotateResponse._from_dict(result)


    async def policy_info(self, name: str) -> PolicyInfoResponse:
        """Get information about a specific policy"""
        args: list[str] = []
        args.append("POLICY_INFO")
        args.append(str(name))
        result = await self._execute(*args)
        return PolicyInfoResponse._from_dict(result)


    async def policy_list(self) -> PolicyListResponse:
        """List all loaded policies"""
        args: list[str] = []
        args.append("POLICY_LIST")
        result = await self._execute(*args)
        return PolicyListResponse._from_dict(result)


    async def policy_reload(self) -> PolicyReloadResponse:
        """Reload policies from disk"""
        args: list[str] = []
        args.append("POLICY_RELOAD")
        result = await self._execute(*args)
        return PolicyReloadResponse._from_dict(result)

