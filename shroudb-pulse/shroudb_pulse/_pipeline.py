"""
ShroudbPulse pipeline for batching commands.

Auto-generated from shroudb-pulse protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import ActorsResponse, AuthResponse, CountResponse, ErrorsResponse, HotspotsResponse, IngestResponse, IngestBatchResponse, QueryResponse, SourceListResponse, SourceStatusResponse


class Pipeline:
    """Batch multiple ShroudbPulse commands and execute them in a single round-trip.

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

    def actors(self, window: Optional[str] = None) -> "Pipeline":
        """Most active actors"""
        args: list[str] = []
        args.append("ACTORS")
        if window is not None:
            args.extend(["WINDOW", str(window)])
        self._commands.append((args, ActorsResponse._from_dict))
        return self


    def auth(self, token: Any) -> "Pipeline":
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        self._commands.append((args, AuthResponse._from_dict))
        return self


    def count(self) -> "Pipeline":
        """Count events matching filter arguments"""
        args: list[str] = []
        args.append("COUNT")
        self._commands.append((args, CountResponse._from_dict))
        return self


    def errors(self, engine: Optional[str] = None, window: Optional[str] = None) -> "Pipeline":
        """Per-operation error rates"""
        args: list[str] = []
        args.append("ERRORS")
        if engine is not None:
            args.extend(["ENGINE", str(engine)])
        if window is not None:
            args.extend(["WINDOW", str(window)])
        self._commands.append((args, ErrorsResponse._from_dict))
        return self


    def health(self) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        self._commands.append((args, None))
        return self


    def hotspots(self, engine: Optional[str] = None, window: Optional[str] = None) -> "Pipeline":
        """Find hotspot resources with highest activity"""
        args: list[str] = []
        args.append("HOTSPOTS")
        if engine is not None:
            args.extend(["ENGINE", str(engine)])
        if window is not None:
            args.extend(["WINDOW", str(window)])
        self._commands.append((args, HotspotsResponse._from_dict))
        return self


    def ingest(self, json: str) -> "Pipeline":
        """Ingest a single audit event"""
        args: list[str] = []
        args.append("INGEST")
        args.append(str(json))
        self._commands.append((args, IngestResponse._from_dict))
        return self


    def ingest_batch(self, json: str) -> "Pipeline":
        """Ingest a batch of audit events"""
        args: list[str] = []
        args.append("INGEST_BATCH")
        args.append(str(json))
        self._commands.append((args, IngestBatchResponse._from_dict))
        return self


    def query(self) -> "Pipeline":
        """Query events with filter arguments"""
        args: list[str] = []
        args.append("QUERY")
        self._commands.append((args, QueryResponse._from_dict))
        return self


    def source_list(self) -> "Pipeline":
        """List configured event sources"""
        args: list[str] = []
        args.append("SOURCE_LIST")
        self._commands.append((args, SourceListResponse._from_dict))
        return self


    def source_status(self) -> "Pipeline":
        """Show per-source ingestion statistics"""
        args: list[str] = []
        args.append("SOURCE_STATUS")
        self._commands.append((args, SourceStatusResponse._from_dict))
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
