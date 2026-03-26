"""
ShroudbCourier — Python client for the ShroudbCourier Secure notification delivery pipeline.

Auto-generated from shroudb-courier protocol spec. Do not edit.

Usage::

    from shroudb_courier import ShroudbCourierClient

    async with await ShroudbCourierClient.connect("shroudb-courier://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbCourierClient, Subscription
from .errors import ShroudbCourierError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import AuthResponse, ChannelInfoResponse, ChannelListResponse, ConnectionsResponse, DeliverResponse, TemplateInfoResponse, TemplateListResponse, TemplateReloadResponse
from .errors import BadargError, DeliveryFailedError, DeniedError, InternalError, NotfoundError, NotreadyError, TemplateErrorError

__version__ = "0.1.0"

__all__ = [
    "ShroudbCourierClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbCourierError",
    "AuthResponse",
    "ChannelInfoResponse",
    "ChannelListResponse",
    "ConnectionsResponse",
    "DeliverResponse",
    "TemplateInfoResponse",
    "TemplateListResponse",
    "TemplateReloadResponse",
    "BadargError",
    "DeliveryFailedError",
    "DeniedError",
    "InternalError",
    "NotfoundError",
    "NotreadyError",
    "TemplateErrorError",
]
