"""
ShroudbPulse response types.

Auto-generated from shroudb-pulse protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class ActorsResponse:
    """Response from ACTORS command."""

    actors: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ActorsResponse":
        return cls(
            actors = data["actors"],
        )


@dataclass
class AuthResponse:
    """Response from AUTH command."""

    status: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "AuthResponse":
        return cls(
            status = data["status"],
        )


@dataclass
class CountResponse:
    """Response from COUNT command."""

    count: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CountResponse":
        return cls(
            count = data["count"],
        )


@dataclass
class ErrorsResponse:
    """Response from ERRORS command."""

    error_rates: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ErrorsResponse":
        return cls(
            error_rates = data["error_rates"],
        )


@dataclass
class HotspotsResponse:
    """Response from HOTSPOTS command."""

    hotspots: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "HotspotsResponse":
        return cls(
            hotspots = data["hotspots"],
        )


@dataclass
class IngestResponse:
    """Response from INGEST command."""

    id: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "IngestResponse":
        return cls(
            id = data["id"],
        )


@dataclass
class IngestBatchResponse:
    """Response from INGEST_BATCH command."""

    count: Any = None
    ids: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "IngestBatchResponse":
        return cls(
            count = data["count"],
            ids = data["ids"],
        )


@dataclass
class QueryResponse:
    """Response from QUERY command."""

    events: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "QueryResponse":
        return cls(
            events = data["events"],
        )


@dataclass
class SourceListResponse:
    """Response from SOURCE_LIST command."""

    sources: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SourceListResponse":
        return cls(
            sources = data["sources"],
        )


@dataclass
class SourceStatusResponse:
    """Response from SOURCE_STATUS command."""

    sources: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SourceStatusResponse":
        return cls(
            sources = data["sources"],
        )



@dataclass
class SubscriptionEvent:
    """A real-time event from a SUBSCRIBE stream."""

    event_type: str = ""
    keyspace: str = ""
    detail: str = ""
    timestamp: int = 0

    @staticmethod
    def _from_frame(frame: list) -> "SubscriptionEvent":
        return SubscriptionEvent(
            event_type=frame[1],
            keyspace=frame[2],
            detail=frame[3],
            timestamp=int(frame[4]),
        )
