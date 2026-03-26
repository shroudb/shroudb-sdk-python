"""
ShroudbMint pipeline for batching commands.

Auto-generated from shroudb-mint protocol spec. Do not edit.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Optional

from ._connection import _Connection
from ._pool import _Pool
from .types import AuthResponse, CaCreateResponse, CaExportResponse, CaInfoResponse, CaListResponse, CaRotateResponse, CrlInfoResponse, InspectResponse, IssueResponse, IssueFromCsrResponse, ListCertsResponse, RenewResponse, RevokeResponse


class Pipeline:
    """Batch multiple ShroudbMint commands and execute them in a single round-trip.

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

    def auth(self, token: Any) -> "Pipeline":
        """Authenticate the connection"""
        args: list[str] = []
        args.append("AUTH")
        args.append(str(token))
        self._commands.append((args, AuthResponse._from_dict))
        return self


    def ca_create(self, ca: str, algorithm: str, subject: str, ttl_days: int, parent: Optional[str] = None) -> "Pipeline":
        """Create a new Certificate Authority"""
        args: list[str] = []
        args.append("CA_CREATE")
        args.append(str(ca))
        args.append(str(algorithm))
        args.append(str(subject))
        args.append(str(ttl_days))
        if parent is not None:
            args.extend(["PARENT", str(parent)])
        self._commands.append((args, CaCreateResponse._from_dict))
        return self


    def ca_export(self, ca: str, format: Optional[str] = None) -> "Pipeline":
        """Export the CA's public certificate"""
        args: list[str] = []
        args.append("CA_EXPORT")
        args.append(str(ca))
        if format is not None:
            args.extend(["FORMAT", str(format)])
        self._commands.append((args, CaExportResponse._from_dict))
        return self


    def ca_info(self, ca: str) -> "Pipeline":
        """Get information about a CA"""
        args: list[str] = []
        args.append("CA_INFO")
        args.append(str(ca))
        self._commands.append((args, CaInfoResponse._from_dict))
        return self


    def ca_list(self) -> "Pipeline":
        """List all CAs"""
        args: list[str] = []
        args.append("CA_LIST")
        self._commands.append((args, CaListResponse._from_dict))
        return self


    def ca_rotate(self, ca: str, force: Optional[Any] = None, dryrun: Optional[Any] = None) -> "Pipeline":
        """Rotate the CA's signing key"""
        args: list[str] = []
        args.append("CA_ROTATE")
        args.append(str(ca))
        if force is not None:
            args.extend(["FORCE", str(force)])
        if dryrun is not None:
            args.extend(["DRYRUN", str(dryrun)])
        self._commands.append((args, CaRotateResponse._from_dict))
        return self


    def crl_info(self, ca: str) -> "Pipeline":
        """Get CRL information for a CA"""
        args: list[str] = []
        args.append("CRL_INFO")
        args.append(str(ca))
        self._commands.append((args, CrlInfoResponse._from_dict))
        return self


    def health(self, ca: Optional[str] = None) -> "Pipeline":
        """Check server health"""
        args: list[str] = []
        args.append("HEALTH")
        if ca is not None:
            args.append(str(ca))
        self._commands.append((args, None))
        return self


    def inspect(self, ca: str, serial: str) -> "Pipeline":
        """Inspect a certificate"""
        args: list[str] = []
        args.append("INSPECT")
        args.append(str(ca))
        args.append(str(serial))
        self._commands.append((args, InspectResponse._from_dict))
        return self


    def issue(self, ca: str, subject: str, profile: str, ttl: Optional[str] = None, san_dns: Optional[Any] = None, san_ip: Optional[Any] = None) -> "Pipeline":
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
        self._commands.append((args, IssueResponse._from_dict))
        return self


    def issue_from_csr(self, ca: str, csr_pem: str, profile: str, ttl: Optional[str] = None) -> "Pipeline":
        """Issue a certificate from a CSR"""
        args: list[str] = []
        args.append("ISSUE_FROM_CSR")
        args.append(str(ca))
        args.append(str(csr_pem))
        args.append(str(profile))
        if ttl is not None:
            args.extend(["TTL", str(ttl)])
        self._commands.append((args, IssueFromCsrResponse._from_dict))
        return self


    def list_certs(self, ca: str, state: Optional[str] = None, limit: Optional[Any] = None, offset: Optional[Any] = None) -> "Pipeline":
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
        self._commands.append((args, ListCertsResponse._from_dict))
        return self


    def renew(self, ca: str, serial: str, ttl: Optional[str] = None) -> "Pipeline":
        """Renew a certificate"""
        args: list[str] = []
        args.append("RENEW")
        args.append(str(ca))
        args.append(str(serial))
        if ttl is not None:
            args.extend(["TTL", str(ttl)])
        self._commands.append((args, RenewResponse._from_dict))
        return self


    def revoke(self, ca: str, serial: str, reason: Optional[str] = None) -> "Pipeline":
        """Revoke a certificate"""
        args: list[str] = []
        args.append("REVOKE")
        args.append(str(ca))
        args.append(str(serial))
        if reason is not None:
            args.extend(["REASON", str(reason)])
        self._commands.append((args, RevokeResponse._from_dict))
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
