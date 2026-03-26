"""
ShroudbMint — Python client for the ShroudbMint Lightweight internal Certificate Authority.

Auto-generated from shroudb-mint protocol spec. Do not edit.

Usage::

    from shroudb_mint import ShroudbMintClient

    async with await ShroudbMintClient.connect("shroudb-mint://localhost") as client:
        result = await client.issue("my-keyspace", ttl_secs=3600)
        print(result.credential_id, result.token)
"""
from .client import ShroudbMintClient, Subscription
from .errors import ShroudbMintError
from ._pipeline import Pipeline
from .types import SubscriptionEvent
from .types import AuthResponse, CaCreateResponse, CaExportResponse, CaInfoResponse, CaListResponse, CaRotateResponse, CrlInfoResponse, InspectResponse, IssueResponse, IssueFromCsrResponse, ListCertsResponse, RenewResponse, RevokeResponse
from .errors import BadargError, DeniedError, DisabledError, ExistsError, InternalError, NokeyError, NotfoundError, NotreadyError, StorageError

__version__ = "0.1.0"

__all__ = [
    "ShroudbMintClient",
    "Pipeline",
    "Subscription",
    "SubscriptionEvent",
    "ShroudbMintError",
    "AuthResponse",
    "CaCreateResponse",
    "CaExportResponse",
    "CaInfoResponse",
    "CaListResponse",
    "CaRotateResponse",
    "CrlInfoResponse",
    "InspectResponse",
    "IssueResponse",
    "IssueFromCsrResponse",
    "ListCertsResponse",
    "RenewResponse",
    "RevokeResponse",
    "BadargError",
    "DeniedError",
    "DisabledError",
    "ExistsError",
    "InternalError",
    "NokeyError",
    "NotfoundError",
    "NotreadyError",
    "StorageError",
]
