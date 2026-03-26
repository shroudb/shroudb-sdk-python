"""
ShroudbCourier error types.

Auto-generated from shroudb-courier protocol spec. Do not edit.
"""
from __future__ import annotations


class ShroudbCourierError(Exception):
    """Base exception for all ShroudbCourier operations."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

    @classmethod
    def _from_server(cls, code: str, message: str) -> "ShroudbCourierError":
        """Internal: construct the appropriate error subclass from a server error."""
        subclass = _ERROR_MAP.get(code, ShroudbCourierError)
        return subclass(code, message)


class BadargError(ShroudbCourierError):
    """Missing or invalid argument"""


class DeliveryFailedError(ShroudbCourierError):
    """Notification delivery failed"""


class DeniedError(ShroudbCourierError):
    """Authentication required or insufficient permissions"""


class InternalError(ShroudbCourierError):
    """Unexpected server error"""


class NotfoundError(ShroudbCourierError):
    """Template not found"""


class NotreadyError(ShroudbCourierError):
    """Server is starting up or shutting down"""


class TemplateErrorError(ShroudbCourierError):
    """Template rendering error"""


_ERROR_MAP: dict[str, type[ShroudbCourierError]] = {
    "BADARG": BadargError,
    "DELIVERY_FAILED": DeliveryFailedError,
    "DENIED": DeniedError,
    "INTERNAL": InternalError,
    "NOTFOUND": NotfoundError,
    "NOTREADY": NotreadyError,
    "TEMPLATE_ERROR": TemplateErrorError,
}
