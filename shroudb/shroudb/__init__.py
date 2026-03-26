"""
Shroudb — Python client for the Shroudb Credential management server.

Auto-generated from shroudb protocol spec. Do not edit.

Usage::

    from shroudb import ShroudbClient

    async with await ShroudbClient.connect("shroudb://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbClient, Subscription
from .errors import ShroudbError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import ConfigGetResponse, HealthResponse, InspectResponse, IssueResponse, JwksResponse, KeysResponse, KeystateResponse, PasswordChangeResponse, PasswordImportResponse, PasswordSetResponse, PasswordVerifyResponse, RefreshResponse, RevokeResponse, RevokeBulkResponse, RevokeFamilyResponse, RotateResponse, SchemaResponse, VerifyResponse
from .errors import BadargError, ChainLimitError, CryptoError, DeniedError, DisabledError, ExpiredError, InternalError, LockedError, NotfoundError, NotreadyError, ReuseDetectedError, StateErrorError, StorageError, ValidationErrorError, WrongtypeError

__version__ = "0.1.0"

__all__ = [
    "ShroudbClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbError",
    "ConfigGetResponse",
    "HealthResponse",
    "InspectResponse",
    "IssueResponse",
    "JwksResponse",
    "KeysResponse",
    "KeystateResponse",
    "PasswordChangeResponse",
    "PasswordImportResponse",
    "PasswordSetResponse",
    "PasswordVerifyResponse",
    "RefreshResponse",
    "RevokeResponse",
    "RevokeBulkResponse",
    "RevokeFamilyResponse",
    "RotateResponse",
    "SchemaResponse",
    "VerifyResponse",
    "BadargError",
    "ChainLimitError",
    "CryptoError",
    "DeniedError",
    "DisabledError",
    "ExpiredError",
    "InternalError",
    "LockedError",
    "NotfoundError",
    "NotreadyError",
    "ReuseDetectedError",
    "StateErrorError",
    "StorageError",
    "ValidationErrorError",
    "WrongtypeError",
]
