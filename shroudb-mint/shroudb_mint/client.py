"""
ShroudbMint client.

Auto-generated from shroudb-mint protocol spec. Do not edit.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from .errors import ShroudbMintError
from ._connection import _Connection, DEFAULT_PORT
from ._pool import _Pool
from .types import SubscriptionEvent
from .types import AuthResponse, CaCreateResponse, CaExportResponse, CaInfoResponse, CaListResponse, CaRotateResponse, CrlInfoResponse, InspectResponse, IssueResponse, IssueFromCsrResponse, ListCertsResponse, RenewResponse, RevokeResponse


def parse_uri(uri: str) -> dict[str, Any]:
    """Parse a ShroudbMint connection URI.

    Supported formats::

        shroudb-mint://localhost
        shroudb-mint://localhost:6699
        shroudb-mint+tls://prod.example.com
        shroudb-mint://mytoken@localhost:6699
        shroudb-mint://mytoken@localhost/sessions
        shroudb-mint+tls://tok@host:6699/keys
    """
    tls = False
    if uri.startswith("shroudb-mint+tls://"):
        tls = True
        rest = uri[len("shroudb-mint+tls://"):]
    elif uri.startswith("shroudb-mint://"):
        rest = uri[len("shroudb-mint://"):]
    else:
        raise ValueError(f"Invalid ShroudbMint URI: {uri}  (expected shroudb-mint:// or shroudb-mint+tls://)")

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


class ShroudbMintClient:
    """Async client for the ShroudbMint Lightweight internal Certificate Authority.

    Connect using a ShroudbMint URI::

        async with await ShroudbMintClient.connect("shroudb-mint://localhost") as client:
            result = await client.issue("my-keyspace")
            print(result.token)

        # With TLS and auth:
        client = await ShroudbMintClient.connect("shroudb-mint+tls://mytoken@prod.example.com/keys")

        # With pool tuning:
        client = await ShroudbMintClient.connect("shroudb-mint://localhost", max_idle=8)
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
        uri: str = "shroudb-mint://localhost",
        *,
        max_idle: int = 4,
        max_open: int = 0,
    ) -> "ShroudbMintClient":
        """Connect to a ShroudbMint server.

        Args:
            uri: ShroudbMint connection URI.
                 Format: ``shroudb-mint://[token@]host[:port][/keyspace]``
                 or ``shroudb-mint+tls://[token@]host[:port][/keyspace]``
            max_idle: Maximum idle connections in pool (default: 4).
            max_open: Maximum total connections, 0 = unlimited (default: 0).

        Returns:
            A connected ShroudbMintClient instance.

        Examples::

            client = await ShroudbMintClient.connect("shroudb-mint://localhost")
            client = await ShroudbMintClient.connect("shroudb-mint+tls://token@host:6699/keys")
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

    async def __aenter__(self) -> "ShroudbMintClient":
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

    async def auth(self, token: Any) -> AuthResponse:
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        result = await self._execute(*args)
        return AuthResponse._from_dict(result)


    async def ca_create(self, ca: str, algorithm: str, subject: str, ttl_days: int, parent: Optional[str] = None) -> CaCreateResponse:
        """Create a new Certificate Authority"""
        args: list[str] = []
        args.append("CA_CREATE")
        args.append(str(ca))
        args.append(str(algorithm))
        args.append(str(subject))
        args.append(str(ttl_days))
        if parent is not None:
            args.extend(["PARENT", str(parent)])
        result = await self._execute(*args)
        return CaCreateResponse._from_dict(result)


    async def ca_export(self, ca: str, format: Optional[str] = None) -> CaExportResponse:
        """Export the CA's public certificate"""
        args: list[str] = []
        args.append("CA_EXPORT")
        args.append(str(ca))
        if format is not None:
            args.extend(["FORMAT", str(format)])
        result = await self._execute(*args)
        return CaExportResponse._from_dict(result)


    async def ca_info(self, ca: str) -> CaInfoResponse:
        """Get information about a CA"""
        args: list[str] = []
        args.append("CA_INFO")
        args.append(str(ca))
        result = await self._execute(*args)
        return CaInfoResponse._from_dict(result)


    async def ca_list(self) -> CaListResponse:
        """List all CAs"""
        args: list[str] = []
        args.append("CA_LIST")
        result = await self._execute(*args)
        return CaListResponse._from_dict(result)


    async def ca_rotate(self, ca: str, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> CaRotateResponse:
        """Rotate the CA's signing key"""
        args: list[str] = []
        args.append("CA_ROTATE")
        args.append(str(ca))
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        result = await self._execute(*args)
        return CaRotateResponse._from_dict(result)


    async def crl_info(self, ca: str) -> CrlInfoResponse:
        """Get CRL information for a CA"""
        args: list[str] = []
        args.append("CRL_INFO")
        args.append(str(ca))
        result = await self._execute(*args)
        return CrlInfoResponse._from_dict(result)


    async def health(self, ca: Optional[str] = None) -> None:
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if ca is not None:
            args.append(str(ca))
        result = await self._execute(*args)


    async def inspect(self, ca: str, serial: str) -> InspectResponse:
        """Inspect a certificate"""
        args: list[str] = []
        args.append("INSPECT")
        args.append(str(ca))
        args.append(str(serial))
        result = await self._execute(*args)
        return InspectResponse._from_dict(result)


    async def issue(self, ca: str, subject: str, profile: str, ttl: Optional[str] = None, san_dns: Optional[Any] = None, san_ip: Optional[Any] = None) -> IssueResponse:
        """Issue a new certificate"""
        args: list[str] = []
        args.append("ISSUE")
        args.append(str(ca))
        args.append(str(subject))
        args.append(str(profile))
        if ttl is not None:
            args.extend(["TTL", str(ttl)])
        if san_dns is not None:
            args.extend(["SAN_DNS", str(san_dns)])
        if san_ip is not None:
            args.extend(["SAN_IP", str(san_ip)])
        result = await self._execute(*args)
        return IssueResponse._from_dict(result)


    async def issue_from_csr(self, ca: str, csr_pem: str, profile: str, ttl: Optional[str] = None) -> IssueFromCsrResponse:
        """Issue a certificate from a CSR"""
        args: list[str] = []
        args.append("ISSUE_FROM_CSR")
        args.append(str(ca))
        args.append(str(csr_pem))
        args.append(str(profile))
        if ttl is not None:
            args.extend(["TTL", str(ttl)])
        result = await self._execute(*args)
        return IssueFromCsrResponse._from_dict(result)


    async def list_certs(self, ca: str, state: Optional[str] = None, limit: Optional[Any] = None, offset: Optional[Any] = None) -> ListCertsResponse:
        """List certificates for a CA"""
        args: list[str] = []
        args.append("LIST_CERTS")
        args.append(str(ca))
        if state is not None:
            args.extend(["STATE", str(state)])
        if limit is not None:
            args.extend(["LIMIT", str(limit)])
        if offset is not None:
            args.extend(["OFFSET", str(offset)])
        result = await self._execute(*args)
        return ListCertsResponse._from_dict(result)


    async def renew(self, ca: str, serial: str, ttl: Optional[str] = None) -> RenewResponse:
        """Renew a certificate"""
        args: list[str] = []
        args.append("RENEW")
        args.append(str(ca))
        args.append(str(serial))
        if ttl is not None:
            args.extend(["TTL", str(ttl)])
        result = await self._execute(*args)
        return RenewResponse._from_dict(result)


    async def revoke(self, ca: str, serial: str, reason: Optional[str] = None) -> RevokeResponse:
        """Revoke a certificate"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(ca))
        args.append(str(serial))
        if reason is not None:
            args.extend(["REASON", str(reason)])
        result = await self._execute(*args)
        return RevokeResponse._from_dict(result)

