"""
Shroudb client.

Auto-generated from shroudb protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import ConfigGetResponse, HealthResponse, InspectResponse, IssueResponse, JwksResponse, KeysResponse, KeystateResponse, PasswordChangeResponse, PasswordImportResponse, PasswordSetResponse, PasswordVerifyResponse, RefreshResponse, RevokeResponse, RevokeBulkResponse, RevokeFamilyResponse, RotateResponse, SchemaResponse, VerifyResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a Shroudb connection URI.

    Supported formats::

        shroudb://localhost
        shroudb://localhost:6399
        shroudb+tls://prod.example.com
        shroudb://mytoken@localhost:6399
        shroudb://mytoken@localhost/sessions
        shroudb+tls://tok@host:6399/keys
    """
    tls = False
    if uri.startswith("shroudb+tls://"):
        tls = True
        rest = uri[len("shroudb+tls://"):]
    elif uri.startswith("shroudb://"):
        rest = uri[len("shroudb://"):]
    else:
        raise ValueError(f"Invalid Shroudb URI: {uri}  (expected shroudb:// or shroudb+tls://)")

    auth_token = None
    if "@" in rest:
        auth_token, rest = rest.split("@", 1)

    keyspace = None
    if "/" in rest:
        rest, keyspace = rest.split("/", 1)
        if not keyspace:
            keyspace = None

    host = rest
    port = DEFAULT_PORT
    if ":" in host:
        host, port_str = host.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            port = DEFAULT_PORT

    return {
        "host": host,
        "port": port,
        "tls": tls,
        "auth_token": auth_token,
        "keyspace": keyspace,
    }


class Subscription:
    """Async iterator for subscription events. Use as async context manager."""

    def __init__(self, conn: _Connection) -> None:
        self._conn = conn

    async def __aenter__(self) -> "Subscription":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    def __aiter__(self) -> "Subscription":
        return self

    async def __anext__(self) -> SubscriptionEvent:
        try:
            frame = await self._conn._read_frame()
            if isinstance(frame, list) and len(frame) >= 5 and frame[0] == "event":
                return SubscriptionEvent._from_frame(frame)
            return await self.__anext__()
        except (ConnectionError, asyncio.IncompleteReadError):
            raise StopAsyncIteration

    async def close(self) -> None:
        """Close the underlying connection, ending the subscription."""
        await self._conn.close()


class ShroudbClient:
    """Async client for the Shroudb Credential management server.

    Connect using a Shroudb URI::

        async with await ShroudbClient.connect("shroudb://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbClient.connect("shroudb+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbClient.connect("shroudb://localhost", max_idle=8)
    """

    def __init__(
        self,
        pool: _Pool,
        *,
        host: str,
        port: int,
        tls: bool,
        auth: str | None,
    ) -> None:
        self._pool = pool
        self._host = host
        self._port = port
        self._tls = tls
        self._auth = auth

    @classmethod
    async def connect(
        cls,
        uri: str = "shroudb://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbClient":
        """Connect to a Shroudb server.

        Args:
            uri: Shroudb connection URI.
                 Format: ``shroudb://[token@]host[:port][/keyspace]``
                 or ``shroudb+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbClient instance.

        Examples::

            client = await ShroudbClient.connect("shroudb://localhost")
            client = await ShroudbClient.connect("shroudb+tls://token@host:6399/keys")
        """
        cfg = parse_uri(uri)
        pool = _Pool(
            cfg["host"],
            cfg["port"],
            tls=cfg["tls"],
            auth=cfg["auth_token"],
            max_idle=max_idle,
            max_open=max_open,
        )
        return cls(
            pool,
            host=cfg["host"],
            port=cfg["port"],
            tls=cfg["tls"],
            auth=cfg["auth_token"],
        )

    async def close(self) -> None:
        """Close the client and all pooled connections."""
        await self._pool.close()

    async def __aenter__(self) -> "ShroudbClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _execute(self, *args: str) -> Any:
        """Acquire a pooled connection, execute, and return it."""
        conn = await self._pool.get()
        try:
            result = await conn.execute(*args)
            await self._pool.put(conn)
            return result
        except Exception:
            await conn.close()
            raise

    def pipeline(self) -> "Pipeline":
        """Create a pipeline for batching commands.

        Usage::

            async with client.pipeline() as pipe:
                pipe.issue("keyspace", ttl_secs=3600)
                pipe.verify("keyspace", token)
                results = await pipe.execute()
        """
        from ._pipeline import Pipeline
        return Pipeline(self._pool)

    async def auth(self, token: str) -> None:
        """Authenticate the current connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        result = await self._execute(*args)


    async def config_get(self, key: str) -> ConfigGetResponse:
        """Retrieve a runtime configuration value"""
        args: list[str] = []
        args.extend(["CONFIG", "GET"])
        args.append(str(key))
        result = await self._execute(*args)
        return ConfigGetResponse._from_dict(result)


    async def config_set(self, key: str, value: str) -> None:
        """Set a runtime configuration value"""
        args: list[str] = []
        args.extend(["CONFIG", "SET"])
        args.append(str(key))
        args.append(str(value))
        result = await self._execute(*args)


    async def health(self, keyspace: Optional[str] = None) -> HealthResponse:
        """Check server or keyspace health"""
        args: list[str] = []
        args.append("HEALTH")
        if keyspace is not None:
            args.append(str(keyspace))
        result = await self._execute(*args)
        return HealthResponse._from_dict(result)


    async def inspect(self, keyspace: str, credential_id: str) -> InspectResponse:
        """Retrieve full details about a credential"""
        args: list[str] = []
        args.append("INSPECT")
        args.append(str(keyspace))
        args.append(str(credential_id))
        result = await self._execute(*args)
        return InspectResponse._from_dict(result)


    async def issue(self, keyspace: str, claims: Optional[dict[str, Any]] = None, metadata: Optional[dict[str, Any]] = None, ttl_secs: Optional[int] = None, idempotency_key: Optional[str] = None) -> IssueResponse:
        """Issue a new credential in the given keyspace"""
        args: list[str] = []
        args.append("ISSUE")
        args.append(str(keyspace))
        if claims is not None:
            args.extend(["CLAIMS", json.dumps(claims)])
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        if ttl_secs is not None:
            args.extend(["TTL", str(ttl_secs)])
        if idempotency_key is not None:
            args.extend(["IDEMPOTENCY_KEY", str(idempotency_key)])
        result = await self._execute(*args)
        return IssueResponse._from_dict(result)


    async def jwks(self, keyspace: str) -> JwksResponse:
        """Return the JSON Web Key Set for a JWT keyspace"""
        args: list[str] = []
        args.append("JWKS")
        args.append(str(keyspace))
        result = await self._execute(*args)
        return JwksResponse._from_dict(result)


    async def keys(self, keyspace: str, cursor: Optional[str] = None, pattern: Optional[str] = None, state_filter: Optional[str] = None, count: Optional[int] = None) -> KeysResponse:
        """List credential IDs with optional filtering and pagination"""
        args: list[str] = []
        args.append("KEYS")
        args.append(str(keyspace))
        if cursor is not None:
            args.extend(["CURSOR", str(cursor)])
        if pattern is not None:
            args.extend(["MATCH", str(pattern)])
        if state_filter is not None:
            args.extend(["STATE", str(state_filter)])
        if count is not None:
            args.extend(["COUNT", str(count)])
        result = await self._execute(*args)
        return KeysResponse._from_dict(result)


    async def keystate(self, keyspace: str) -> KeystateResponse:
        """Show the current key ring state for a keyspace"""
        args: list[str] = []
        args.append("KEYSTATE")
        args.append(str(keyspace))
        result = await self._execute(*args)
        return KeystateResponse._from_dict(result)


    async def password_change(self, keyspace: str, user_id: str, old_password: str, new_password: str) -> PasswordChangeResponse:
        """Change a user's password (requires old password)"""
        args: list[str] = []
        args.extend(["PASSWORD", "CHANGE"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(old_password))
        args.append(str(new_password))
        result = await self._execute(*args)
        return PasswordChangeResponse._from_dict(result)


    async def password_import(self, keyspace: str, user_id: str, hash: str, metadata: Optional[dict[str, Any]] = None) -> PasswordImportResponse:
        """Import a pre-hashed password for migration from another system (argon2, bcrypt, scrypt)"""
        args: list[str] = []
        args.extend(["PASSWORD", "IMPORT"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(hash))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        result = await self._execute(*args)
        return PasswordImportResponse._from_dict(result)


    async def password_set(self, keyspace: str, user_id: str, password: str, metadata: Optional[dict[str, Any]] = None) -> PasswordSetResponse:
        """Set a password for a user in a password keyspace"""
        args: list[str] = []
        args.extend(["PASSWORD", "SET"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(password))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        result = await self._execute(*args)
        return PasswordSetResponse._from_dict(result)


    async def password_verify(self, keyspace: str, user_id: str, password: str) -> PasswordVerifyResponse:
        """Verify a user's password"""
        args: list[str] = []
        args.extend(["PASSWORD", "VERIFY"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(password))
        result = await self._execute(*args)
        return PasswordVerifyResponse._from_dict(result)


    async def refresh(self, keyspace: str, token: str) -> RefreshResponse:
        """Exchange a refresh token for a new one"""
        args: list[str] = []
        args.append("REFRESH")
        args.append(str(keyspace))
        args.append(str(token))
        result = await self._execute(*args)
        return RefreshResponse._from_dict(result)


    async def revoke(self, keyspace: str, credential_id: str) -> RevokeResponse:
        """Revoke a credential by ID"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        args.append(str(credential_id))
        result = await self._execute(*args)
        return RevokeResponse._from_dict(result)


    async def revoke_bulk(self, keyspace: str, ids: Optional[list[str]] = None) -> RevokeBulkResponse:
        """Bulk-revoke multiple credentials"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        if ids is not None:
            args.append("BULK")
            args.extend(str(x) for x in ids)
        result = await self._execute(*args)
        return RevokeBulkResponse._from_dict(result)


    async def revoke_family(self, keyspace: str, family_id: str) -> RevokeFamilyResponse:
        """Revoke all credentials in a refresh token family"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        if family_id is not None:
            args.extend(["FAMILY", str(family_id)])
        result = await self._execute(*args)
        return RevokeFamilyResponse._from_dict(result)


    async def rotate(self, keyspace: str, force: bool = False, nowait: bool = False, dryrun: bool = False) -> RotateResponse:
        """Trigger signing key rotation for a keyspace"""
        args: list[str] = []
        args.append("ROTATE")
        args.append(str(keyspace))
        if force:
            args.append("FORCE")
        if nowait:
            args.append("NOWAIT")
        if dryrun:
            args.append("DRYRUN")
        result = await self._execute(*args)
        return RotateResponse._from_dict(result)


    async def schema(self, keyspace: str) -> SchemaResponse:
        """Display the metadata schema for a keyspace"""
        args: list[str] = []
        args.append("SCHEMA")
        args.append(str(keyspace))
        result = await self._execute(*args)
        return SchemaResponse._from_dict(result)


    async def subscribe(self, channel: str) -> Subscription:
        """Subscribe to real-time event notifications.

        Opens a dedicated connection for streaming events.
        Use as an async context manager:

            async with await client.subscribe("keyspace:tokens") as sub:
                async for event in sub:
                    print(event.event_type, event.keyspace, event.detail)

        Args:
            channel: Channel name (e.g. "keyspace:tokens") or "*" for all events.

        Returns:
            A Subscription async iterator.
        """
        conn = await _Connection.open(self._host, self._port, tls=self._tls, auth=self._auth)
        result = await conn.execute("SUBSCRIBE", channel)
        if isinstance(result, dict) and result.get("status") != "OK":
            await conn.close()
            raise ShroudbError("SUBSCRIBE_FAILED", str(result))
        return Subscription(conn)


    async def suspend(self, keyspace: str, credential_id: str) -> None:
        """Temporarily suspend a credential"""
        args: list[str] = []
        args.append("SUSPEND")
        args.append(str(keyspace))
        args.append(str(credential_id))
        result = await self._execute(*args)


    async def unsuspend(self, keyspace: str, credential_id: str) -> None:
        """Reactivate a previously suspended credential"""
        args: list[str] = []
        args.append("UNSUSPEND")
        args.append(str(keyspace))
        args.append(str(credential_id))
        result = await self._execute(*args)


    async def update(self, keyspace: str, credential_id: str, metadata: Optional[dict[str, Any]] = None) -> None:
        """Update metadata on an existing credential"""
        args: list[str] = []
        args.append("UPDATE")
        args.append(str(keyspace))
        args.append(str(credential_id))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        result = await self._execute(*args)


    async def verify(self, keyspace: str, token: str, payload: Optional[str] = None, check_revoked: bool = False) -> VerifyResponse:
        """Verify a credential (JWT, API key, or HMAC signature)"""
        args: list[str] = []
        args.append("VERIFY")
        args.append(str(keyspace))
        args.append(str(token))
        if payload is not None:
            args.extend(["PAYLOAD", str(payload)])
        if check_revoked:
            args.append("CHECKREV")
        result = await self._execute(*args)
        return VerifyResponse._from_dict(result)

