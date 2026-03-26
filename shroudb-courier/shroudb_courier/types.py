"""
ShroudbCourier response types.

Auto-generated from shroudb-courier protocol spec. Do not edit.
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
class ChannelInfoResponse:
    """Response from CHANNEL_INFO command."""

    channel: Any = None
    subscribers: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ChannelInfoResponse":
        return cls(
            channel = data["channel"],
            subscribers = data["subscribers"],
        )


@dataclass
class ChannelListResponse:
    """Response from CHANNEL_LIST command."""

    channels: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ChannelListResponse":
        return cls(
            channels = data["channels"],
        )


@dataclass
class ConnectionsResponse:
    """Response from CONNECTIONS command."""

    connections: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ConnectionsResponse":
        return cls(
            connections = data["connections"],
        )


@dataclass
class DeliverResponse:
    """Response from DELIVER command."""

    delivery_id: str = ""
    channel: str = ""
    status: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "DeliverResponse":
        return cls(
            delivery_id = data["delivery_id"],
            channel = data["channel"],
            status = data["status"],
        )


@dataclass
class TemplateInfoResponse:
    """Response from TEMPLATE_INFO command."""

    name: str = ""
    channels: Any = None
    variables: Any = None
    loaded_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "TemplateInfoResponse":
        return cls(
            name = data["name"],
            channels = data["channels"],
            variables = data["variables"],
            loaded_at = data["loaded_at"],
        )


@dataclass
class TemplateListResponse:
    """Response from TEMPLATE_LIST command."""

    templates: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "TemplateListResponse":
        return cls(
            templates = data["templates"],
        )


@dataclass
class TemplateReloadResponse:
    """Response from TEMPLATE_RELOAD command."""

    count: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "TemplateReloadResponse":
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
