"""
ShroudbMint response types.

Auto-generated from shroudb-mint protocol spec. Do not edit.
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
class CaCreateResponse:
    """Response from CA_CREATE command."""

    ca: str = ""
    serial: str = ""
    certificate: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CaCreateResponse":
        return cls(
            ca = data["ca"],
            serial = data["serial"],
            certificate = data["certificate"],
        )


@dataclass
class CaExportResponse:
    """Response from CA_EXPORT command."""

    certificate: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CaExportResponse":
        return cls(
            certificate = data["certificate"],
        )


@dataclass
class CaInfoResponse:
    """Response from CA_INFO command."""

    ca: str = ""
    algorithm: str = ""
    subject: str = ""
    serial: str = ""
    not_before: Any = None
    not_after: Any = None
    issued_count: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CaInfoResponse":
        return cls(
            ca = data["ca"],
            algorithm = data["algorithm"],
            subject = data["subject"],
            serial = data["serial"],
            not_before = data["not_before"],
            not_after = data["not_after"],
            issued_count = data["issued_count"],
        )


@dataclass
class CaListResponse:
    """Response from CA_LIST command."""

    cas: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CaListResponse":
        return cls(
            cas = data["cas"],
        )


@dataclass
class CaRotateResponse:
    """Response from CA_ROTATE command."""

    serial: str = ""
    previous_serial: Optional[str] = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CaRotateResponse":
        return cls(
            serial = data["serial"],
            previous_serial = data.get("previous_serial"),
        )


@dataclass
class CrlInfoResponse:
    """Response from CRL_INFO command."""

    ca: str = ""
    crl_number: Any = None
    last_update: Any = None
    next_update: Any = None
    revoked_count: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "CrlInfoResponse":
        return cls(
            ca = data["ca"],
            crl_number = data["crl_number"],
            last_update = data["last_update"],
            next_update = data["next_update"],
            revoked_count = data["revoked_count"],
        )


@dataclass
class InspectResponse:
    """Response from INSPECT command."""

    serial: str = ""
    subject: str = ""
    not_before: Any = None
    not_after: Any = None
    state: str = ""
    certificate: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "InspectResponse":
        return cls(
            serial = data["serial"],
            subject = data["subject"],
            not_before = data["not_before"],
            not_after = data["not_after"],
            state = data["state"],
            certificate = data["certificate"],
        )


@dataclass
class IssueResponse:
    """Response from ISSUE command."""

    serial: str = ""
    certificate: str = ""
    private_key: str = ""
    chain: str = ""
    not_after: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "IssueResponse":
        return cls(
            serial = data["serial"],
            certificate = data["certificate"],
            private_key = data["private_key"],
            chain = data["chain"],
            not_after = data["not_after"],
        )


@dataclass
class IssueFromCsrResponse:
    """Response from ISSUE_FROM_CSR command."""

    serial: str = ""
    certificate: str = ""
    chain: str = ""
    not_after: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "IssueFromCsrResponse":
        return cls(
            serial = data["serial"],
            certificate = data["certificate"],
            chain = data["chain"],
            not_after = data["not_after"],
        )


@dataclass
class ListCertsResponse:
    """Response from LIST_CERTS command."""

    certificates: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ListCertsResponse":
        return cls(
            certificates = data["certificates"],
        )


@dataclass
class RenewResponse:
    """Response from RENEW command."""

    serial: str = ""
    certificate: str = ""
    private_key: str = ""
    not_after: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RenewResponse":
        return cls(
            serial = data["serial"],
            certificate = data["certificate"],
            private_key = data["private_key"],
            not_after = data["not_after"],
        )


@dataclass
class RevokeResponse:
    """Response from REVOKE command."""

    serial: str = ""
    revoked_at: Any = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RevokeResponse":
        return cls(
            serial = data["serial"],
            revoked_at = data["revoked_at"],
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
