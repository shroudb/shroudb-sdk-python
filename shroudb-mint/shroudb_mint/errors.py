"""
ShroudbMint error types.

Auto-generated from shroudb-mint protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbMintError(Exception):
    """Base exception for all ShroudbMint operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbMintError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbMintError)
        return subclass(code, message)


class BadargError(ShroudbMintError):
    """Missing or invalid argument"""


class DeniedError(ShroudbMintError):
    """Authentication required or insufficient permissions"""


class DisabledError(ShroudbMintError):
    """CA is disabled"""


class ExistsError(ShroudbMintError):
    """CA already exists"""


class InternalError(ShroudbMintError):
    """Unexpected server error"""


class NokeyError(ShroudbMintError):
    """Signing key not available"""


class NotfoundError(ShroudbMintError):
    """CA or certificate not found"""


class NotreadyError(ShroudbMintError):
    """Server is starting up or shutting down"""


class StorageError(ShroudbMintError):
    """Backend storage error"""


_ERROR_MAP: dict[str, type[ShroudbMintError]] = {
    "BADARG": BadargError,
    "DENIED": DeniedError,
    "DISABLED": DisabledError,
    "EXISTS": ExistsError,
    "INTERNAL": InternalError,
    "NOKEY": NokeyError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "STORAGE": StorageError,
}
