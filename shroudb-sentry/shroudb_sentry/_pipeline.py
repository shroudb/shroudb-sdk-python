"""
ShroudbSentry pipeline for batching commands.

Auto-generated from shroudb-sentry protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import AuthResponse, EvaluateResponse, KeyInfoResponse, KeyRotateResponse, PolicyInfoResponse, PolicyListResponse, PolicyReloadResponse


class Pipeline:
    """Batch multiple ShroudbSentry commands and execute them in a single round-trip.

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


    def evaluate(self, json: str) -> "Pipeline":
        """Evaluate an authorization request against loaded policies"""
        args: list[str] = []
        args.append("EVALUATE")
        args.append(str(json))
        self._commands.append((args, EvaluateResponse._from_dict))
        return self


    def health(self) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        self._commands.append((args, None))
        return self


    def key_info(self) -> "Pipeline":
        """Get signing key information"""
        args: list[str] = []
        args.append("KEY_INFO")
        self._commands.append((args, KeyInfoResponse._from_dict))
        return self


    def key_rotate(self, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> "Pipeline":
        """Rotate the signing key used for JWT decisions"""
        args: list[str] = []
        args.append("KEY_ROTATE")
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        self._commands.append((args, KeyRotateResponse._from_dict))
        return self


    def policy_info(self, name: str) -> "Pipeline":
        """Get information about a specific policy"""
        args: list[str] = []
        args.append("POLICY_INFO")
        args.append(str(name))
        self._commands.append((args, PolicyInfoResponse._from_dict))
        return self


    def policy_list(self) -> "Pipeline":
        """List all loaded policies"""
        args: list[str] = []
        args.append("POLICY_LIST")
        self._commands.append((args, PolicyListResponse._from_dict))
        return self


    def policy_reload(self) -> "Pipeline":
        """Reload policies from disk"""
        args: list[str] = []
        args.append("POLICY_RELOAD")
        self._commands.append((args, PolicyReloadResponse._from_dict))
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
