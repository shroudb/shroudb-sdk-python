"""
ShroudbAuth error types.

Auto-generated from shroudb-auth API spec. Do not edit.
"""
from __future__ import annotations

from typing import Any


class ShroudbAuthError(Exception):
    """Base exception for all ShroudbAuth operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_response(cls, status_code: int, data: dict[str, Any]) -> "ShroudbAuthError":
        """Construct the appropriate error subclass from an HTTP error response.

        Expected response body: ``{"error": "CODE", "message": "..."}``
        """
        code = data.get("error", "UNKNOWN")
        message = data.get("message", data.get("error", f"HTTP {status_code}"))
        subclass = _ERROR_MAP.get(code, ShroudbAuthError)
        return subclass(code, message)


class BadRequestError(ShroudbAuthError):
    """Invalid request body or parameters"""


class ConflictError(ShroudbAuthError):
    """Resource already exists (e.g. duplicate signup)"""


class ForbiddenError(ShroudbAuthError):
    """Insufficient permissions"""


class InternalError(ShroudbAuthError):
    """Internal server error"""


class TooManyRequestsError(ShroudbAuthError):
    """Account locked due to too many failed attempts"""


class UnauthorizedError(ShroudbAuthError):
    """Authentication required or invalid credentials"""


_ERROR_MAP: dict[str, type[ShroudbAuthError]] = {
    "BAD_REQUEST": BadRequestError,
    "CONFLICT": ConflictError,
    "FORBIDDEN": ForbiddenError,
    "INTERNAL": InternalError,
    "TOO_MANY_REQUESTS": TooManyRequestsError,
    "UNAUTHORIZED": UnauthorizedError,
}
