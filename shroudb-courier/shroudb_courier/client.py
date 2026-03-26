"""
ShroudbCourier client.

Auto-generated from shroudb-courier protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbCourierError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import AuthResponse, ChannelInfoResponse, ChannelListResponse, ConnectionsResponse, DeliverResponse, TemplateInfoResponse, TemplateListResponse, TemplateReloadResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbCourier connection URI.

    Supported formats::

        shroudb-courier://localhost
        shroudb-courier://localhost:6999
        shroudb-courier+tls://prod.example.com
        shroudb-courier://mytoken@localhost:6999
        shroudb-courier://mytoken@localhost/sessions
        shroudb-courier+tls://tok@host:6999/keys
    """
    tls = False
    if uri.startswith("shroudb-courier+tls://"):
        tls = True
        rest = uri[len("shroudb-courier+tls://"):]
    elif uri.startswith("shroudb-courier://"):
        rest = uri[len("shroudb-courier://"):]
    else:
        raise ValueError(f"Invalid ShroudbCourier URI: {uri}  (expected shroudb-courier:// or shroudb-courier+tls://)")

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


class ShroudbCourierClient:
    """Async client for the ShroudbCourier Secure notification delivery pipeline.

    Connect using a ShroudbCourier URI::

        async with await ShroudbCourierClient.connect("shroudb-courier://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbCourierClient.connect("shroudb-courier+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbCourierClient.connect("shroudb-courier://localhost", max_idle=8)
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
        uri: str = "shroudb-courier://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbCourierClient":
        """Connect to a ShroudbCourier server.

        Args:
            uri: ShroudbCourier connection URI.
                 Format: ``shroudb-courier://[token@]host[:port][/keyspace]``
                 or ``shroudb-courier+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbCourierClient instance.

        Examples::

            client = await ShroudbCourierClient.connect("shroudb-courier://localhost")
            client = await ShroudbCourierClient.connect("shroudb-courier+tls://token@host:6999/keys")
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

    async def __aenter__(self) -> "ShroudbCourierClient":
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


    async def channel_info(self, channel: Any) -> ChannelInfoResponse:
        """Get subscriber count for a WebSocket channel"""
        args: list[str] = []
        args.append("CHANNEL_INFO")
        args.append(str(channel))
        result = await self._execute(*args)
        return ChannelInfoResponse._from_dict(result)


    async def channel_list(self) -> ChannelListResponse:
        """List all active WebSocket channels"""
        args: list[str] = []
        args.append("CHANNEL_LIST")
        result = await self._execute(*args)
        return ChannelListResponse._from_dict(result)


    async def connections(self) -> ConnectionsResponse:
        """Get total WebSocket connections"""
        args: list[str] = []
        args.append("CONNECTIONS")
        result = await self._execute(*args)
        return ConnectionsResponse._from_dict(result)


    async def deliver(self, json: str) -> DeliverResponse:
        """Deliver a notification (decrypts recipient, renders template, sends via adapter)"""
        args: list[str] = []
        args.append("DELIVER")
        args.append(str(json))
        result = await self._execute(*args)
        return DeliverResponse._from_dict(result)


    async def health(self) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        result = await self._execute(*args)


    async def template_info(self, name: str) -> TemplateInfoResponse:
        """Get information about a specific template"""
        args: list[str] = []
        args.append("TEMPLATE_INFO")
        args.append(str(name))
        result = await self._execute(*args)
        return TemplateInfoResponse._from_dict(result)


    async def template_list(self) -> TemplateListResponse:
        """List all loaded templates"""
        args: list[str] = []
        args.append("TEMPLATE_LIST")
        result = await self._execute(*args)
        return TemplateListResponse._from_dict(result)


    async def template_reload(self) -> TemplateReloadResponse:
        """Reload templates from disk"""
        args: list[str] = []
        args.append("TEMPLATE_RELOAD")
        result = await self._execute(*args)
        return TemplateReloadResponse._from_dict(result)

