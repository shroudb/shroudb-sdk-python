"""
ShroudbPulse — Python client for the ShroudbPulse Observability plane for unified audit event streaming.

Auto-generated from shroudb-pulse protocol spec. Do not edit.

Usage::

    from shroudb_pulse import ShroudbPulseClient

    async with await ShroudbPulseClient.connect("shroudb-pulse://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbPulseClient, Subscription
from .errors import ShroudbPulseError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import ActorsResponse, AuthResponse, CountResponse, ErrorsResponse, HotspotsResponse, IngestResponse, IngestBatchResponse, QueryResponse, SourceListResponse, SourceStatusResponse
from .errors import BadargError, DeniedError, InternalError, NotfoundError, NotreadyError, StorageError

__version__ = "0.1.0"

__all__ = [
    "ShroudbPulseClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbPulseError",
    "ActorsResponse",
    "AuthResponse",
    "CountResponse",
    "ErrorsResponse",
    "HotspotsResponse",
    "IngestResponse",
    "IngestBatchResponse",
    "QueryResponse",
    "SourceListResponse",
    "SourceStatusResponse",
    "BadargError",
    "DeniedError",
    "InternalError",
    "NotfoundError",
    "NotreadyError",
    "StorageError",
]
