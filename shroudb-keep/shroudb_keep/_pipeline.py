"""
ShroudbKeep pipeline for batching commands.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import AuthResponse, DeleteResponse, GetResponse, ListResponse, PutResponse, RotateResponse, VersionsResponse


class Pipeline:
    """Batch multiple ShroudbKeep commands and execute them in a single round-trip.

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


    def delete(self, path: str) -> "Pipeline":
        """Soft-delete a secret"""
        args: list[str] = []
        args.append("DELETE")
        args.append(str(path))
        self._commands.append((args, DeleteResponse._from_dict))
        return self


    def get(self, path: str, version: Optional[int] = None) -> "Pipeline":
        """Retrieve a secret (latest or specific version)"""
        args: list[str] = []
        args.append("GET")
        args.append(str(path))
        if version is not None:
            args.extend(["VERSION", str(version)])
        self._commands.append((args, GetResponse._from_dict))
        return self


    def health(self, path: Optional[str] = None) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if path is not None:
            args.append(str(path))
        self._commands.append((args, None))
        return self


    def list(self, prefix: Optional[str] = None) -> "Pipeline":
        """List secret paths matching a prefix"""
        args: list[str] = []
        args.append("LIST")
        if prefix is not None:
            args.append(str(prefix))
        self._commands.append((args, ListResponse._from_dict))
        return self


    def put(self, path: str, value: str, meta: Optional[str] = None) -> "Pipeline":
        """Store a secret (creates a new version)"""
        args: list[str] = []
        args.append("PUT")
        args.append(str(path))
        args.append(str(value))
        if meta is not None:
            args.extend(["META", str(meta)])
        self._commands.append((args, PutResponse._from_dict))
        return self


    def rotate(self, path: str) -> "Pipeline":
        """Re-encrypt the latest version under the current key"""
        args: list[str] = []
        args.append("ROTATE")
        args.append(str(path))
        self._commands.append((args, RotateResponse._from_dict))
        return self


    def versions(self, path: str) -> "Pipeline":
        """Show version history for a secret"""
        args: list[str] = []
        args.append("VERSIONS")
        args.append(str(path))
        self._commands.append((args, VersionsResponse._from_dict))
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
