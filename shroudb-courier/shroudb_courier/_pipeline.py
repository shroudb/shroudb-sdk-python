"""
ShroudbCourier pipeline for batching commands.

Auto-generated from shroudb-courier protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import AuthResponse, ChannelInfoResponse, ChannelListResponse, ConnectionsResponse, DeliverResponse, TemplateInfoResponse, TemplateListResponse, TemplateReloadResponse


class Pipeline:
    """Batch multiple ShroudbCourier commands and execute them in a single round-trip.

    Usage::

        async with client.pipeline() as pipe:
            pipe.issue("keyspace", ttl_secs=3600)
            pipe.verify("keyspace", token)
            results = await pipe.execute()
            # results[0] is IssueResponse, results[1] is VerifyResponse
    """

    def __init__(self, pool: _Pool) -> None:
        self._pool = pool
        self._conn: _Connection | None = None
        self._commands: list[tuple[list[str], Callable[[Any], Any] | None]] = []

    async def __aenter__(self) -> "Pipeline":
        self._conn = await self._pool.get()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._conn is not None:
            await self._pool.put(self._conn)
            self._conn = None

    def auth(self, token: Any) -> "Pipeline":
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        self._commands.append((args, AuthResponse._from_dict))
        return self


    def channel_info(self, channel: Any) -> "Pipeline":
        """Get subscriber count for a WebSocket channel"""
        args: list[str] = []
        args.append("CHANNEL_INFO")
        args.append(str(channel))
        self._commands.append((args, ChannelInfoResponse._from_dict))
        return self


    def channel_list(self) -> "Pipeline":
        """List all active WebSocket channels"""
        args: list[str] = []
        args.append("CHANNEL_LIST")
        self._commands.append((args, ChannelListResponse._from_dict))
        return self


    def connections(self) -> "Pipeline":
        """Get total WebSocket connections"""
        args: list[str] = []
        args.append("CONNECTIONS")
        self._commands.append((args, ConnectionsResponse._from_dict))
        return self


    def deliver(self, json: str) -> "Pipeline":
        """Deliver a notification (decrypts recipient, renders template, sends via adapter)"""
        args: list[str] = []
        args.append("DELIVER")
        args.append(str(json))
        self._commands.append((args, DeliverResponse._from_dict))
        return self


    def health(self) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        self._commands.append((args, None))
        return self


    def template_info(self, name: str) -> "Pipeline":
        """Get information about a specific template"""
        args: list[str] = []
        args.append("TEMPLATE_INFO")
        args.append(str(name))
        self._commands.append((args, TemplateInfoResponse._from_dict))
        return self


    def template_list(self) -> "Pipeline":
        """List all loaded templates"""
        args: list[str] = []
        args.append("TEMPLATE_LIST")
        self._commands.append((args, TemplateListResponse._from_dict))
        return self


    def template_reload(self) -> "Pipeline":
        """Reload templates from disk"""
        args: list[str] = []
        args.append("TEMPLATE_RELOAD")
        self._commands.append((args, TemplateReloadResponse._from_dict))
        return self


    async def execute(self) -> list[Any]:
        """Send all queued commands and return their responses.

        Returns a list of typed response objects in the same order
        commands were added.
        """
        if self._conn is None:
            raise RuntimeError("Pipeline must be used as an async context manager")
        for cmd_args, _ in self._commands:
            await self._conn.send_command(*cmd_args)
        await self._conn.flush()

        results: list[Any] = []
        for _, parser in self._commands:
            raw = await self._conn.read_response()
            if parser is not None:
                results.append(parser(raw))
            else:
                results.append(raw)
        self._commands.clear()
        return results

    def __len__(self) -> int:
        return len(self._commands)

    def clear(self) -> None:
        """Discard all queued commands."""
        self._commands.clear()
