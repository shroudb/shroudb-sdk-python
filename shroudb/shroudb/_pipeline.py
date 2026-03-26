"""
Shroudb pipeline for batching commands.

Auto-generated from shroudb protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import ConfigGetResponse, HealthResponse, InspectResponse, IssueResponse, JwksResponse, KeysResponse, KeystateResponse, PasswordChangeResponse, PasswordImportResponse, PasswordSetResponse, PasswordVerifyResponse, RefreshResponse, RevokeResponse, RevokeBulkResponse, RevokeFamilyResponse, RotateResponse, SchemaResponse, VerifyResponse


class Pipeline:
    """Batch multiple Shroudb commands and execute them in a single round-trip.

    Usage::

        async with client.pipeline() as pipe:
            pipe.issue("keyspace", ttl_secs=3600)
            pipe.verify("keyspace", token)
            results = await pipe.execute()
            # results[0] is IssueResponse, results[1] is VerifyResponse
    """

    def __init__(self, pool: _Pool) -> None:
        self._pool = pool
        self._conn: _Connection | None = None
        self._commands: list[tuple[list[str], Callable[[Any], Any] | None]] = []

    async def __aenter__(self) -> "Pipeline":
        self._conn = await self._pool.get()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._conn is not None:
            await self._pool.put(self._conn)
            self._conn = None

    def auth(self, token: str) -> "Pipeline":
        """Authenticate the current connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        self._commands.append((args, None))
        return self


    def config_get(self, key: str) -> "Pipeline":
        """Retrieve a runtime configuration value"""
        args: list[str] = []
        args.extend(["CONFIG", "GET"])
        args.append(str(key))
        self._commands.append((args, ConfigGetResponse._from_dict))
        return self


    def config_set(self, key: str, value: str) -> "Pipeline":
        """Set a runtime configuration value"""
        args: list[str] = []
        args.extend(["CONFIG", "SET"])
        args.append(str(key))
        args.append(str(value))
        self._commands.append((args, None))
        return self


    def health(self, keyspace: Optional[str] = None) -> "Pipeline":
        """Check server or keyspace health"""
        args: list[str] = []
        args.append("HEALTH")
        if keyspace is not None:
            args.append(str(keyspace))
        self._commands.append((args, HealthResponse._from_dict))
        return self


    def inspect(self, keyspace: str, credential_id: str) -> "Pipeline":
        """Retrieve full details about a credential"""
        args: list[str] = []
        args.append("INSPECT")
        args.append(str(keyspace))
        args.append(str(credential_id))
        self._commands.append((args, InspectResponse._from_dict))
        return self


    def issue(self, keyspace: str, claims: Optional[dict[str, Any]] = None, metadata: Optional[dict[str, Any]] = None, ttl_secs: Optional[int] = None, idempotency_key: Optional[str] = None) -> "Pipeline":
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
        self._commands.append((args, IssueResponse._from_dict))
        return self


    def jwks(self, keyspace: str) -> "Pipeline":
        """Return the JSON Web Key Set for a JWT keyspace"""
        args: list[str] = []
        args.append("JWKS")
        args.append(str(keyspace))
        self._commands.append((args, JwksResponse._from_dict))
        return self


    def keys(self, keyspace: str, cursor: Optional[str] = None, pattern: Optional[str] = None, state_filter: Optional[str] = None, count: Optional[int] = None) -> "Pipeline":
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
        self._commands.append((args, KeysResponse._from_dict))
        return self


    def keystate(self, keyspace: str) -> "Pipeline":
        """Show the current key ring state for a keyspace"""
        args: list[str] = []
        args.append("KEYSTATE")
        args.append(str(keyspace))
        self._commands.append((args, KeystateResponse._from_dict))
        return self


    def password_change(self, keyspace: str, user_id: str, old_password: str, new_password: str) -> "Pipeline":
        """Change a user's password (requires old password)"""
        args: list[str] = []
        args.extend(["PASSWORD", "CHANGE"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(old_password))
        args.append(str(new_password))
        self._commands.append((args, PasswordChangeResponse._from_dict))
        return self


    def password_import(self, keyspace: str, user_id: str, hash: str, metadata: Optional[dict[str, Any]] = None) -> "Pipeline":
        """Import a pre-hashed password for migration from another system (argon2, bcrypt, scrypt)"""
        args: list[str] = []
        args.extend(["PASSWORD", "IMPORT"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(hash))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        self._commands.append((args, PasswordImportResponse._from_dict))
        return self


    def password_set(self, keyspace: str, user_id: str, password: str, metadata: Optional[dict[str, Any]] = None) -> "Pipeline":
        """Set a password for a user in a password keyspace"""
        args: list[str] = []
        args.extend(["PASSWORD", "SET"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(password))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        self._commands.append((args, PasswordSetResponse._from_dict))
        return self


    def password_verify(self, keyspace: str, user_id: str, password: str) -> "Pipeline":
        """Verify a user's password"""
        args: list[str] = []
        args.extend(["PASSWORD", "VERIFY"])
        args.append(str(keyspace))
        args.append(str(user_id))
        args.append(str(password))
        self._commands.append((args, PasswordVerifyResponse._from_dict))
        return self


    def refresh(self, keyspace: str, token: str) -> "Pipeline":
        """Exchange a refresh token for a new one"""
        args: list[str] = []
        args.append("REFRESH")
        args.append(str(keyspace))
        args.append(str(token))
        self._commands.append((args, RefreshResponse._from_dict))
        return self


    def revoke(self, keyspace: str, credential_id: str) -> "Pipeline":
        """Revoke a credential by ID"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        args.append(str(credential_id))
        self._commands.append((args, RevokeResponse._from_dict))
        return self


    def revoke_bulk(self, keyspace: str, ids: Optional[list[str]] = None) -> "Pipeline":
        """Bulk-revoke multiple credentials"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        if ids is not None:
            args.append("BULK")
            args.extend(str(x) for x in ids)
        self._commands.append((args, RevokeBulkResponse._from_dict))
        return self


    def revoke_family(self, keyspace: str, family_id: str) -> "Pipeline":
        """Revoke all credentials in a refresh token family"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(keyspace))
        if family_id is not None:
            args.extend(["FAMILY", str(family_id)])
        self._commands.append((args, RevokeFamilyResponse._from_dict))
        return self


    def rotate(self, keyspace: str, force: bool = False, nowait: bool = False, dryrun: bool = False) -> "Pipeline":
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
        self._commands.append((args, RotateResponse._from_dict))
        return self


    def schema(self, keyspace: str) -> "Pipeline":
        """Display the metadata schema for a keyspace"""
        args: list[str] = []
        args.append("SCHEMA")
        args.append(str(keyspace))
        self._commands.append((args, SchemaResponse._from_dict))
        return self


    def suspend(self, keyspace: str, credential_id: str) -> "Pipeline":
        """Temporarily suspend a credential"""
        args: list[str] = []
        args.append("SUSPEND")
        args.append(str(keyspace))
        args.append(str(credential_id))
        self._commands.append((args, None))
        return self


    def unsuspend(self, keyspace: str, credential_id: str) -> "Pipeline":
        """Reactivate a previously suspended credential"""
        args: list[str] = []
        args.append("UNSUSPEND")
        args.append(str(keyspace))
        args.append(str(credential_id))
        self._commands.append((args, None))
        return self


    def update(self, keyspace: str, credential_id: str, metadata: Optional[dict[str, Any]] = None) -> "Pipeline":
        """Update metadata on an existing credential"""
        args: list[str] = []
        args.append("UPDATE")
        args.append(str(keyspace))
        args.append(str(credential_id))
        if metadata is not None:
            args.extend(["META", json.dumps(metadata)])
        self._commands.append((args, None))
        return self


    def verify(self, keyspace: str, token: str, payload: Optional[str] = None, check_revoked: bool = False) -> "Pipeline":
        """Verify a credential (JWT, API key, or HMAC signature)"""
        args: list[str] = []
        args.append("VERIFY")
        args.append(str(keyspace))
        args.append(str(token))
        if payload is not None:
            args.extend(["PAYLOAD", str(payload)])
        if check_revoked:
            args.append("CHECKREV")
        self._commands.append((args, VerifyResponse._from_dict))
        return self


    async def execute(self) -> list[Any]:
        """Send all queued commands and return their responses.

        Returns a list of typed response objects in the same order
        commands were added.
        """
        if self._conn is None:
            raise RuntimeError("Pipeline must be used as an async context manager")
        for cmd_args, _ in self._commands:
            await self._conn.send_command(*cmd_args)
        await self._conn.flush()

        results: list[Any] = []
        for _, parser in self._commands:
            raw = await self._conn.read_response()
            if parser is not None:
                results.append(parser(raw))
            else:
                results.append(raw)
        self._commands.clear()
        return results

    def __len__(self) -> int:
        return len(self._commands)

    def clear(self) -> None:
        """Discard all queued commands."""
        self._commands.clear()
