"""
Internal connection pool.

This module is an implementation detail of the ShroudbKeep client library.
Do not import directly — use `shroudb_keep.ShroudbKeepClient` instead.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
from collections import deque
from typing import Optional

from ._connection import _Connection


class _Pool:
    """Async connection pool for ShroudbKeep. Internal use only."""

    def __init__(
        self,
        host: str,
        port: int,
        *,
        tls: bool = False,
        auth: Optional[str] = None,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> None:
        self._host = host
        self._port = port
        self._tls = tls
        self._auth = auth
        self._max_idle = max_idle
        self._max_open = max_open
        self._idle: deque[_Connection] = deque()
        self._open = 0
        self._lock = asyncio.Lock()

    async def get(self) -> _Connection:
        async with self._lock:
            if self._idle:
                return self._idle.pop()
            self._open += 1

        try:
            conn = await _Connection.open(self._host, self._port, tls=self._tls, auth=self._auth)
            return conn
        except Exception:
            async with self._lock:
                self._open -= 1
            raise

    async def put(self, conn: _Connection) -> None:
        async with self._lock:
            if len(self._idle) < self._max_idle:
                self._idle.append(conn)
            else:
                await conn.close()
                self._open -= 1

    async def close(self) -> None:
        async with self._lock:
            while self._idle:
                await self._idle.pop().close()
            self._open = 0
