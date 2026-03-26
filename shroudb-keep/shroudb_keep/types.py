"""
ShroudbKeep response types.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

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
class DeleteResponse:
    """Response from DELETE command."""

    path: str = ""
    deleted_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "DeleteResponse":
        return cls(
            path = data["path"],
            deleted_at = data["deleted_at"],
        )


@dataclass
class GetResponse:
    """Response from GET command."""

    path: str = ""
    value: str = ""
    version: int = 0
    meta: Optional[str] = None
    created_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "GetResponse":
        return cls(
            path = data["path"],
            value = data["value"],
            version = int(data["version"]),
            meta = data.get("meta"),
            created_at = data["created_at"],
        )


@dataclass
class ListResponse:
    """Response from LIST command."""

    paths: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ListResponse":
        return cls(
            paths = data["paths"],
        )


@dataclass
class PutResponse:
    """Response from PUT command."""

    path: str = ""
    version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "PutResponse":
        return cls(
            path = data["path"],
            version = int(data["version"]),
        )


@dataclass
class RotateResponse:
    """Response from ROTATE command."""

    path: str = ""
    version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RotateResponse":
        return cls(
            path = data["path"],
            version = int(data["version"]),
        )


@dataclass
class VersionsResponse:
    """Response from VERSIONS command."""

    path: str = ""
    versions: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "VersionsResponse":
        return cls(
            path = data["path"],
            versions = data["versions"],
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
