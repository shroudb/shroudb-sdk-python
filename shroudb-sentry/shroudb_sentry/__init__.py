"""
ShroudbSentry — Python client for the ShroudbSentry Policy-based authorization engine.

Auto-generated from shroudb-sentry protocol spec. Do not edit.

Usage::

    from shroudb_sentry import ShroudbSentryClient

    async with await ShroudbSentryClient.connect("shroudb-sentry://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbSentryClient, Subscription
from .errors import ShroudbSentryError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import AuthResponse, EvaluateResponse, KeyInfoResponse, KeyRotateResponse, PolicyInfoResponse, PolicyListResponse, PolicyReloadResponse
from .errors import BadargError, DeniedError, InternalError, NokeyError, NotfoundError, NotreadyError

__version__ = "0.1.0"

__all__ = [
    "ShroudbSentryClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbSentryError",
    "AuthResponse",
    "EvaluateResponse",
    "KeyInfoResponse",
    "KeyRotateResponse",
    "PolicyInfoResponse",
    "PolicyListResponse",
    "PolicyReloadResponse",
    "BadargError",
    "DeniedError",
    "InternalError",
    "NokeyError",
    "NotfoundError",
    "NotreadyError",
]
