"""
ShroudbAuth — Python client for the ShroudbAuth Authentication service.

Auto-generated from shroudb-auth API spec. Do not edit.

Usage::

    from shroudb_auth import ShroudbAuthClient

    async with ShroudbAuthClient("http://localhost:4001") as client:
        result = await client.signup("alice", "s3cret")
        print(result.access_token)
"""
from .client import ShroudbAuthClient
from .errors import ShroudbAuthError
from .types import ChangePasswordResponse, ForgotPasswordResponse, HealthResponse, JwksResponse, LoginResponse, LogoutResponse, LogoutAllResponse, RefreshResponse, ResetPasswordResponse, SessionResponse, SessionsResponse, SignupResponse
from .errors import BadRequestError, ConflictError, ForbiddenError, InternalError, TooManyRequestsError, UnauthorizedError

__version__ = "0.1.0"

__all__ = [
    "ShroudbAuthClient",
    "ShroudbAuthError",
    "ChangePasswordResponse",
    "ForgotPasswordResponse",
    "HealthResponse",
    "JwksResponse",
    "LoginResponse",
    "LogoutResponse",
    "LogoutAllResponse",
    "RefreshResponse",
    "ResetPasswordResponse",
    "SessionResponse",
    "SessionsResponse",
    "SignupResponse",
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "InternalError",
    "TooManyRequestsError",
    "UnauthorizedError",
]
