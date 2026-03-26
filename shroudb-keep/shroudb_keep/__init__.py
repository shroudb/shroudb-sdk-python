"""
ShroudbKeep — Python client for the ShroudbKeep Secrets manager.

Auto-generated from shroudb-keep protocol spec. Do not edit.

Usage::

    from shroudb_keep import ShroudbKeepClient

    async with await ShroudbKeepClient.connect("shroudb-keep://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbKeepClient, Subscription
from .errors import ShroudbKeepError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import AuthResponse, DeleteResponse, GetResponse, ListResponse, PutResponse, RotateResponse, VersionsResponse
from .errors import BadargError, DeletedError, DeniedError, InternalError, NotfoundError, NotreadyError, StorageError

__version__ = "0.1.0"

__all__ = [
    "ShroudbKeepClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbKeepError",
    "AuthResponse",
    "DeleteResponse",
    "GetResponse",
    "ListResponse",
    "PutResponse",
    "RotateResponse",
    "VersionsResponse",
    "BadargError",
    "DeletedError",
    "DeniedError",
    "InternalError",
    "NotfoundError",
    "NotreadyError",
    "StorageError",
]
