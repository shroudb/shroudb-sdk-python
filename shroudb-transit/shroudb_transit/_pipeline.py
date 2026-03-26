"""
ShroudbTransit pipeline for batching commands.

Auto-generated from shroudb-transit protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import DecryptResponse, EncryptResponse, GenerateDataKeyResponse, KeyInfoResponse, RewrapResponse, RotateResponse, SignResponse, VerifySignatureResponse


class Pipeline:
    """Batch multiple ShroudbTransit commands and execute them in a single round-trip.

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

    def decrypt(self, keyring: str, ciphertext: str, context: Optional[Any] = None) -> "Pipeline":
        """Decrypt ciphertext using the embedded key version"""
        args: list[str] = []
        args.append("DECRYPT")
        args.append(str(keyring))
        args.append(str(ciphertext))
        if context is not None:
            args.extend(["CONTEXT", str(context)])
        self._commands.append((args, DecryptResponse._from_dict))
        return self


    def encrypt(self, keyring: str, plaintext: str, context: Optional[Any] = None, key_version: Optional[int] = None, convergent: Optional[Any] = None) -> "Pipeline":
        """Encrypt plaintext with the active key version"""
        args: list[str] = []
        args.append("ENCRYPT")
        args.append(str(keyring))
        args.append(str(plaintext))
        if context is not None:
            args.extend(["CONTEXT", str(context)])
        if key_version is not None:
            args.extend(["KEY_VERSION", str(key_version)])
        if convergent is not None:
            args.extend(["CONVERGENT", str(convergent)])
        self._commands.append((args, EncryptResponse._from_dict))
        return self


    def generate_data_key(self, keyring: str, bits: Optional[int] = None) -> "Pipeline":
        """Generate a data encryption key (envelope encryption pattern)"""
        args: list[str] = []
        args.append("GENERATE_DATA_KEY")
        args.append(str(keyring))
        if bits is not None:
            args.extend(["BITS", str(bits)])
        self._commands.append((args, GenerateDataKeyResponse._from_dict))
        return self


    def health(self, keyring: Optional[str] = None) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if keyring is not None:
            args.append(str(keyring))
        self._commands.append((args, None))
        return self


    def key_info(self, keyring: str) -> "Pipeline":
        """Get keyring metadata and key version information"""
        args: list[str] = []
        args.append("KEY_INFO")
        args.append(str(keyring))
        self._commands.append((args, KeyInfoResponse._from_dict))
        return self


    def rewrap(self, keyring: str, ciphertext: str, context: Optional[Any] = None) -> "Pipeline":
        """Re-encrypt ciphertext with the current active key version"""
        args: list[str] = []
        args.append("REWRAP")
        args.append(str(keyring))
        args.append(str(ciphertext))
        if context is not None:
            args.extend(["CONTEXT", str(context)])
        self._commands.append((args, RewrapResponse._from_dict))
        return self


    def rotate(self, keyring: str, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> "Pipeline":
        """Rotate the keyring to a new key version"""
        args: list[str] = []
        args.append("ROTATE")
        args.append(str(keyring))
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        self._commands.append((args, RotateResponse._from_dict))
        return self


    def sign(self, keyring: str, data: str, algorithm: Optional[Any] = None) -> "Pipeline":
        """Create a detached signature"""
        args: list[str] = []
        args.append("SIGN")
        args.append(str(keyring))
        args.append(str(data))
        if algorithm is not None:
            args.extend(["ALGORITHM", str(algorithm)])
        self._commands.append((args, SignResponse._from_dict))
        return self


    def verify_signature(self, keyring: str, data: str, signature: str) -> "Pipeline":
        """Verify a detached signature"""
        args: list[str] = []
        args.append("VERIFY_SIGNATURE")
        args.append(str(keyring))
        args.append(str(data))
        args.append(str(signature))
        self._commands.append((args, VerifySignatureResponse._from_dict))
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
