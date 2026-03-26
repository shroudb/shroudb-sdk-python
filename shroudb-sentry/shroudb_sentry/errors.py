"""
ShroudbSentry error types.

Auto-generated from shroudb-sentry protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbSentryError(Exception):
    """Base exception for all ShroudbSentry operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbSentryError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbSentryError)
        return subclass(code, message)


class BadargError(ShroudbSentryError):
    """Missing or invalid argument"""


class DeniedError(ShroudbSentryError):
    """Authentication required or insufficient permissions"""


class InternalError(ShroudbSentryError):
    """Unexpected server error"""


class NokeyError(ShroudbSentryError):
    """Signing key not available"""


class NotfoundError(ShroudbSentryError):
    """Policy not found"""


class NotreadyError(ShroudbSentryError):
    """Server is starting up or shutting down"""


_ERROR_MAP: dict[str, type[ShroudbSentryError]] = {
    "BADARG": BadargError,
    "DENIED": DeniedError,
    "INTERNAL": InternalError,
    "NOKEY": NokeyError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
}
