"""
ShroudbAuth response types.

Auto-generated from shroudb-auth API spec. Do not edit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class ChangePasswordResponse:
    """Response from Change password for the currently authenticated user."""

    status: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ChangePasswordResponse":
        return cls(
            status=data["status"],
        )


@dataclass
class ForgotPasswordResponse:
    """Response from Request a password reset token (always returns 200 to prevent enumeration)."""

    status: str = ""
    expires_in: Optional[int] = None
    reset_token: Optional[str] = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ForgotPasswordResponse":
        return cls(
            status=data["status"],
            expires_in=data.get("expires_in"),
            reset_token=data.get("reset_token"),
        )


@dataclass
class HealthResponse:
    """Response from Health check endpoint."""

    status: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "HealthResponse":
        return cls(
            status=data["status"],
        )


@dataclass
class JwksResponse:
    """Response from Public JSON Web Key Set for verifying access tokens."""

    keys: list[Any] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "JwksResponse":
        return cls(
            keys=data["keys"],
        )


@dataclass
class LoginResponse:
    """Response from Authenticate a user and receive access + refresh tokens."""

    access_token: str = ""
    expires_in: int = 0
    refresh_token: str = ""
    user_id: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            refresh_token=data["refresh_token"],
            user_id=data["user_id"],
        )


@dataclass
class LogoutResponse:
    """Response from Revoke the current refresh token family and clear cookies."""

    status: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "LogoutResponse":
        return cls(
            status=data["status"],
        )


@dataclass
class LogoutAllResponse:
    """Response from Revoke all refresh token families for a user."""

    revoked_families: int = 0
    status: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "LogoutAllResponse":
        return cls(
            revoked_families=data["revoked_families"],
            status=data["status"],
        )


@dataclass
class RefreshResponse:
    """Response from Exchange a refresh token for new access + refresh tokens."""

    access_token: str = ""
    expires_in: int = 0
    refresh_token: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "RefreshResponse":
        return cls(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            refresh_token=data["refresh_token"],
        )


@dataclass
class ResetPasswordResponse:
    """Response from Reset password using a single-use reset token (revoked after use)."""

    status: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "ResetPasswordResponse":
        return cls(
            status=data["status"],
        )


@dataclass
class SessionResponse:
    """Response from Validate current session and return user info."""

    claims: dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[int] = None
    user_id: Optional[str] = None

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SessionResponse":
        return cls(
            claims=data["claims"],
            expires_at=data.get("expires_at"),
            user_id=data.get("user_id"),
        )


@dataclass
class SessionsResponse:
    """Response from List active sessions (refresh token families) for the authenticated user."""

    active_sessions: list[Any] = field(default_factory=list)
    user_id: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SessionsResponse":
        return cls(
            active_sessions=data["active_sessions"],
            user_id=data["user_id"],
        )


@dataclass
class SignupResponse:
    """Response from Register a new user and receive access + refresh tokens."""

    access_token: str = ""
    expires_in: int = 0
    refresh_token: str = ""
    user_id: str = ""

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> "SignupResponse":
        return cls(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            refresh_token=data["refresh_token"],
            user_id=data["user_id"],
        )


