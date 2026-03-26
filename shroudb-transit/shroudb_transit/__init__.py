"""
ShroudbTransit — Python client for the ShroudbTransit Encryption-as-a-service.

Auto-generated from shroudb-transit protocol spec. Do not edit.

Usage::

    from shroudb_transit import ShroudbTransitClient

    async with await ShroudbTransitClient.connect("shroudb-transit://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbTransitClient, Subscription
from .errors import ShroudbTransitError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import DecryptResponse, EncryptResponse, GenerateDataKeyResponse, KeyInfoResponse, RewrapResponse, RotateResponse, SignResponse, VerifySignatureResponse
from .errors import BadargError, DeniedError, DisabledError, InternalError, NotfoundError, NotreadyError, WrongtypeError

__version__ = "0.1.0"

__all__ = [
    "ShroudbTransitClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbTransitError",
    "DecryptResponse",
    "EncryptResponse",
    "GenerateDataKeyResponse",
    "KeyInfoResponse",
    "RewrapResponse",
    "RotateResponse",
    "SignResponse",
    "VerifySignatureResponse",
    "BadargError",
    "DeniedError",
    "DisabledError",
    "InternalError",
    "NotfoundError",
    "NotreadyError",
    "WrongtypeError",
]
