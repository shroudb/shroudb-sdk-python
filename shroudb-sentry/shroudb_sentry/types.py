"""
ShroudbSentry response types.

Auto-generated from shroudb-sentry protocol spec. Do not edit.
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
class EvaluateResponse:
    """Response from EVALUATE command."""

    decision: str = ""
    token: str = ""
    reasons: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "EvaluateResponse":
        return cls(
            decision = data["decision"],
            token = data["token"],
            reasons = data["reasons"],
        )


@dataclass
class KeyInfoResponse:
    """Response from KEY_INFO command."""

    key_id: Any = None
    algorithm: Any = None
    created_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "KeyInfoResponse":
        return cls(
            key_id = data["key_id"],
            algorithm = data["algorithm"],
            created_at = data["created_at"],
        )


@dataclass
class KeyRotateResponse:
    """Response from KEY_ROTATE command."""

    key_id: Any = None
    previous_key_id: Optional[Any] = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "KeyRotateResponse":
        return cls(
            key_id = data["key_id"],
            previous_key_id = data.get("previous_key_id"),
        )


@dataclass
class PolicyInfoResponse:
    """Response from POLICY_INFO command."""

    name: str = ""
    version: Any = None
    rules: Any = None
    loaded_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "PolicyInfoResponse":
        return cls(
            name = data["name"],
            version = data["version"],
            rules = data["rules"],
            loaded_at = data["loaded_at"],
        )


@dataclass
class PolicyListResponse:
    """Response from POLICY_LIST command."""

    policies: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "PolicyListResponse":
        return cls(
            policies = data["policies"],
        )


@dataclass
class PolicyReloadResponse:
    """Response from POLICY_RELOAD command."""

    count: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "PolicyReloadResponse":
        return cls(
            count = data["count"],
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
