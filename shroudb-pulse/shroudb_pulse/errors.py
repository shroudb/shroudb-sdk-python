"""
ShroudbPulse error types.

Auto-generated from shroudb-pulse protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbPulseError(Exception):
    """Base exception for all ShroudbPulse operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbPulseError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbPulseError)
        return subclass(code, message)


class BadargError(ShroudbPulseError):
    """Missing or invalid argument"""


class DeniedError(ShroudbPulseError):
    """Authentication required or insufficient permissions"""


class InternalError(ShroudbPulseError):
    """Unexpected server error"""


class NotfoundError(ShroudbPulseError):
    """Resource not found"""


class NotreadyError(ShroudbPulseError):
    """Server is starting up or shutting down"""


class StorageError(ShroudbPulseError):
    """Backend storage or WAL error"""


_ERROR_MAP: dict[str, type[ShroudbPulseError]] = {
    "BADARG": BadargError,
    "DENIED": DeniedError,
    "INTERNAL": InternalError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "STORAGE": StorageError,
}
