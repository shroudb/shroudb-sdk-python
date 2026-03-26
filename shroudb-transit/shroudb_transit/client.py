"""
ShroudbTransit client.

Auto-generated from shroudb-transit protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbTransitError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import DecryptResponse, EncryptResponse, GenerateDataKeyResponse, KeyInfoResponse, RewrapResponse, RotateResponse, SignResponse, VerifySignatureResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbTransit connection URI.

    Supported formats::

        shroudb-transit://localhost
        shroudb-transit://localhost:6499
        shroudb-transit+tls://prod.example.com
        shroudb-transit://mytoken@localhost:6499
        shroudb-transit://mytoken@localhost/sessions
        shroudb-transit+tls://tok@host:6499/keys
    """
    tls = False
    if uri.startswith("shroudb-transit+tls://"):
        tls = True
        rest = uri[len("shroudb-transit+tls://"):]
    elif uri.startswith("shroudb-transit://"):
        rest = uri[len("shroudb-transit://"):]
    else:
        raise ValueError(f"Invalid ShroudbTransit URI: {uri}  (expected shroudb-transit:// or shroudb-transit+tls://)")

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


class ShroudbTransitClient:
    """Async client for the ShroudbTransit Encryption-as-a-service.

    Connect using a ShroudbTransit URI::

        async with await ShroudbTransitClient.connect("shroudb-transit://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbTransitClient.connect("shroudb-transit+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbTransitClient.connect("shroudb-transit://localhost", max_idle=8)
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
        uri: str = "shroudb-transit://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbTransitClient":
        """Connect to a ShroudbTransit server.

        Args:
            uri: ShroudbTransit connection URI.
                 Format: ``shroudb-transit://[token@]host[:port][/keyspace]``
                 or ``shroudb-transit+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbTransitClient instance.

        Examples::

            client = await ShroudbTransitClient.connect("shroudb-transit://localhost")
            client = await ShroudbTransitClient.connect("shroudb-transit+tls://token@host:6499/keys")
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

    async def __aenter__(self) -> "ShroudbTransitClient":
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

    async def decrypt(self, keyring: str, ciphertext: str, context: Optional[Any] = None) -> DecryptResponse:
        """Decrypt ciphertext using the embedded key version"""
        args: list[str] = []
        args.append("DECRYPT")
        args.append(str(keyring))
        args.append(str(ciphertext))
        if context is not None:
            args.extend(["CONTEXT", str(context)])
        result = await self._execute(*args)
        return DecryptResponse._from_dict(result)


    async def encrypt(self, keyring: str, plaintext: str, context: Optional[Any] = None, key_version: Optional[int] = None, convergent: Optional[Any] = None) -> EncryptResponse:
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
        result = await self._execute(*args)
        return EncryptResponse._from_dict(result)


    async def generate_data_key(self, keyring: str, bits: Optional[int] = None) -> GenerateDataKeyResponse:
        """Generate a data encryption key (envelope encryption pattern)"""
        args: list[str] = []
        args.append("GENERATE_DATA_KEY")
        args.append(str(keyring))
        if bits is not None:
            args.extend(["BITS", str(bits)])
        result = await self._execute(*args)
        return GenerateDataKeyResponse._from_dict(result)


    async def health(self, keyring: Optional[str] = None) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if keyring is not None:
            args.append(str(keyring))
        result = await self._execute(*args)


    async def key_info(self, keyring: str) -> KeyInfoResponse:
        """Get keyring metadata and key version information"""
        args: list[str] = []
        args.append("KEY_INFO")
        args.append(str(keyring))
        result = await self._execute(*args)
        return KeyInfoResponse._from_dict(result)


    async def rewrap(self, keyring: str, ciphertext: str, context: Optional[Any] = None) -> RewrapResponse:
        """Re-encrypt ciphertext with the current active key version"""
        args: list[str] = []
        args.append("REWRAP")
        args.append(str(keyring))
        args.append(str(ciphertext))
        if context is not None:
            args.extend(["CONTEXT", str(context)])
        result = await self._execute(*args)
        return RewrapResponse._from_dict(result)


    async def rotate(self, keyring: str, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> RotateResponse:
        """Rotate the keyring to a new key version"""
        args: list[str] = []
        args.append("ROTATE")
        args.append(str(keyring))
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        result = await self._execute(*args)
        return RotateResponse._from_dict(result)


    async def sign(self, keyring: str, data: str, algorithm: Optional[Any] = None) -> SignResponse:
        """Create a detached signature"""
        args: list[str] = []
        args.append("SIGN")
        args.append(str(keyring))
        args.append(str(data))
        if algorithm is not None:
            args.extend(["ALGORITHM", str(algorithm)])
        result = await self._execute(*args)
        return SignResponse._from_dict(result)


    async def verify_signature(self, keyring: str, data: str, signature: str) -> VerifySignatureResponse:
        """Verify a detached signature"""
        args: list[str] = []
        args.append("VERIFY_SIGNATURE")
        args.append(str(keyring))
        args.append(str(data))
        args.append(str(signature))
        result = await self._execute(*args)
        return VerifySignatureResponse._from_dict(result)

