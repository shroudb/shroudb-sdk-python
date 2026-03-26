"""
ShroudbTransit error types.

Auto-generated from shroudb-transit protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbTransitError(Exception):
    """Base exception for all ShroudbTransit operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbTransitError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbTransitError)
        return subclass(code, message)


class BadargError(ShroudbTransitError):
    """Missing or invalid argument"""


class DeniedError(ShroudbTransitError):
    """Authentication required or insufficient permissions"""


class DisabledError(ShroudbTransitError):
    """Keyring is disabled"""


class InternalError(ShroudbTransitError):
    """Unexpected server error"""


class NotfoundError(ShroudbTransitError):
    """Keyring or key version not found"""


class NotreadyError(ShroudbTransitError):
    """Server is starting up or shutting down"""


class WrongtypeError(ShroudbTransitError):
    """Operation not supported for this keyring type"""


_ERROR_MAP: dict[str, type[ShroudbTransitError]] = {
    "BADARG": BadargError,
    "DENIED": DeniedError,
    "DISABLED": DisabledError,
    "INTERNAL": InternalError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "WRONGTYPE": WrongtypeError,
}
