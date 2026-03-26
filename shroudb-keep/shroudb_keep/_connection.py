"""
Internal ShroudbKeep protocol codec.

This module is an implementation detail of the ShroudbKeep client library.
Do not import directly — use `shroudb_keep.ShroudbKeepClient` instead.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import ssl
from typing import Any

from .errors import ShroudbKeepError

DEFAULT_PORT = 6899


class _Connection:
    """Low-level async connection. Internal use only."""

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        self._reader = reader
        self._writer = writer

    @classmethod
    async def open(
        cls, host: str, port: int, *, tls: bool = False, auth: str | None = None,
    ) -> "_Connection":
        if tls:
            ctx = ssl.create_default_context()
            reader, writer = await asyncio.open_connection(host, port, ssl=ctx)
        else:
            reader, writer = await asyncio.open_connection(host, port)
        conn = cls(reader, writer)
        if auth:
            await conn.execute("AUTH", auth)
        return conn

    async def execute(self, *args: str) -> Any:
        """Send a command and read the response."""
        parts = [f"*{len(args)}\r\n"]
        for arg in args:
            encoded = arg.encode("utf-8")
            parts.append(f"${len(encoded)}\r\n")
            parts.append(arg)
            parts.append("\r\n")
        self._writer.write("".join(parts).encode("utf-8"))
        await self._writer.drain()
        return await self._read_frame()

    async def _read_frame(self) -> Any:
        prefix = await self._reader.readline()
        if not prefix:
            raise ConnectionError("Connection closed")
        tag = chr(prefix[0])
        payload = prefix[1:].rstrip(b"\r\n").decode("utf-8")

        if tag == "+":
            return payload
        elif tag == "-":
            code, _, message = payload.partition(" ")
            raise ShroudbKeepError._from_server(code, message)
        elif tag == ":":
            return int(payload)
        elif tag == "$":
            length = int(payload)
            if length < 0:
                return None
            data = await self._reader.readexactly(length + 2)
            return data[:-2].decode("utf-8")
        elif tag == "*":
            count = int(payload)
            return [await self._read_frame() for _ in range(count)]
        elif tag == "%":
            count = int(payload)
            result: dict[str, Any] = {}
            for _ in range(count):
                key = await self._read_frame()
                val = await self._read_frame()
                result[str(key)] = val
            return result
        elif tag == "_":
            return None
        else:
            raise ShroudbKeepError(f"INTERNAL", f"Unknown response type: {tag}")

    async def send_command(self, *args: str) -> None:
        """Encode and buffer a command without reading the response."""
        parts = [f"*{len(args)}\r\n"]
        for arg in args:
            encoded = arg.encode("utf-8")
            parts.append(f"${len(encoded)}\r\n")
            parts.append(arg)
            parts.append("\r\n")
        self._writer.write("".join(parts).encode("utf-8"))

    async def flush(self) -> None:
        """Flush the write buffer."""
        await self._writer.drain()

    async def read_response(self) -> Any:
        """Read a single response frame."""
        return await self._read_frame()

    async def close(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()
