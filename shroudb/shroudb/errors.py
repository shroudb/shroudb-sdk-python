"""
Shroudb error types.

Auto-generated from shroudb protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbError(Exception):
    """Base exception for all Shroudb operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbError)
        return subclass(code, message)


class BadargError(ShroudbError):
    """Missing or malformed command argument"""


class ChainLimitError(ShroudbError):
    """Refresh token chain limit exceeded"""


class CryptoError(ShroudbError):
    """Cryptographic operation failed"""


class DeniedError(ShroudbError):
    """Authentication required or insufficient permissions"""


class DisabledError(ShroudbError):
    """Keyspace is disabled"""


class ExpiredError(ShroudbError):
    """Credential has expired"""


class InternalError(ShroudbError):
    """Unexpected internal error"""


class LockedError(ShroudbError):
    """Account temporarily locked due to too many failed attempts"""


class NotfoundError(ShroudbError):
    """Credential, keyspace, or resource does not exist"""


class NotreadyError(ShroudbError):
    """Server is not ready (still starting up)"""


class ReuseDetectedError(ShroudbError):
    """Refresh token reuse detected — family revoked"""


class StateErrorError(ShroudbError):
    """Credential is in wrong state for this operation"""


class StorageError(ShroudbError):
    """Storage engine error"""


class ValidationErrorError(ShroudbError):
    """Metadata or claims failed schema validation"""


class WrongtypeError(ShroudbError):
    """Operation not supported for this keyspace type"""


_ERROR_MAP: dict[str, type[ShroudbError]] = {
    "BADARG": BadargError,
    "CHAIN_LIMIT": ChainLimitError,
    "CRYPTO": CryptoError,
    "DENIED": DeniedError,
    "DISABLED": DisabledError,
    "EXPIRED": ExpiredError,
    "INTERNAL": InternalError,
    "LOCKED": LockedError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "REUSE_DETECTED": ReuseDetectedError,
    "STATE_ERROR": StateErrorError,
    "STORAGE": StorageError,
    "VALIDATION_ERROR": ValidationErrorError,
    "WRONGTYPE": WrongtypeError,
}
