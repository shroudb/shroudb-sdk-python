"""
ShroudbTransit response types.

Auto-generated from shroudb-transit protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class DecryptResponse:
    """Response from DECRYPT command."""

    plaintext: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "DecryptResponse":
        return cls(
            plaintext = data["plaintext"],
        )


@dataclass
class EncryptResponse:
    """Response from ENCRYPT command."""

    ciphertext: str = ""
    key_version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "EncryptResponse":
        return cls(
            ciphertext = data["ciphertext"],
            key_version = int(data["key_version"]),
        )


@dataclass
class GenerateDataKeyResponse:
    """Response from GENERATE_DATA_KEY command."""

    plaintext_key: str = ""
    wrapped_key: str = ""
    key_version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "GenerateDataKeyResponse":
        return cls(
            plaintext_key = data["plaintext_key"],
            wrapped_key = data["wrapped_key"],
            key_version = int(data["key_version"]),
        )


@dataclass
class KeyInfoResponse:
    """Response from KEY_INFO command."""

    keyring: str = ""
    type: Any = None
    active_version: int = 0
    versions: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "KeyInfoResponse":
        return cls(
            keyring = data["keyring"],
            type = data["type"],
            active_version = int(data["active_version"]),
            versions = data["versions"],
        )


@dataclass
class RewrapResponse:
    """Response from REWRAP command."""

    ciphertext: str = ""
    key_version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RewrapResponse":
        return cls(
            ciphertext = data["ciphertext"],
            key_version = int(data["key_version"]),
        )


@dataclass
class RotateResponse:
    """Response from ROTATE command."""

    key_version: int = 0
    previous_version: Optional[int] = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RotateResponse":
        return cls(
            key_version = int(data["key_version"]),
            previous_version = int(data["previous_version"]) if data.get("previous_version") is not None else None,
        )


@dataclass
class SignResponse:
    """Response from SIGN command."""

    signature: str = ""
    key_version: int = 0

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SignResponse":
        return cls(
            signature = data["signature"],
            key_version = int(data["key_version"]),
        )


@dataclass
class VerifySignatureResponse:
    """Response from VERIFY_SIGNATURE command."""

    valid: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "VerifySignatureResponse":
        return cls(
            valid = data["valid"],
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
