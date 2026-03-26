"""
ShroudbKeep error types.

Auto-generated from shroudb-keep protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbKeepError(Exception):
    """Base exception for all ShroudbKeep operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbKeepError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbKeepError)
        return subclass(code, message)


class BadargError(ShroudbKeepError):
    """Missing or invalid argument"""


class DeletedError(ShroudbKeepError):
    """Secret has been soft-deleted"""


class DeniedError(ShroudbKeepError):
    """Authentication required or insufficient permissions"""


class InternalError(ShroudbKeepError):
    """Unexpected server error"""


class NotfoundError(ShroudbKeepError):
    """Secret path or version not found"""


class NotreadyError(ShroudbKeepError):
    """Server is starting up or shutting down"""


class StorageError(ShroudbKeepError):
    """Backend storage error"""


_ERROR_MAP: dict[str, type[ShroudbKeepError]] = {
    "BADARG": BadargError,
    "DELETED": DeletedError,
    "DENIED": DeniedError,
    "INTERNAL": InternalError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "STORAGE": StorageError,
}
