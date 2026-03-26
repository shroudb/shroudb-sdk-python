"""
ShroudbAuth HTTP client.

Auto-generated from shroudb-auth API spec. Do not edit.
"""
from __future__ import annotations

from typing import Any, Optional

import httpx

from .errors import ShroudbAuthError
from .types import ChangePasswordResponse, ForgotPasswordResponse, HealthResponse, JwksResponse, LoginResponse, LogoutResponse, LogoutAllResponse, RefreshResponse, ResetPasswordResponse, SessionResponse, SessionsResponse, SignupResponse


class ShroudbAuthClient:
    """Async HTTP client for the ShroudbAuth Authentication service.

    Usage::

        async with ShroudbAuthClient("http://localhost:4001") as client:
            result = await client.signup("alice", "s3cret")
            print(result.access_token)
    """

    def __init__(
        self,
        base_url: str,
        *,
        keyspace: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        """Create a new ShroudbAuth client.

        Args:
            base_url: Base URL of the ShroudbAuth server (e.g. ``"http://localhost:4001"``).
            keyspace: Default keyspace for all requests. Can be overridden per call.
            timeout: Request timeout in seconds (default: 30).
        """
        self._base_url = base_url.rstrip("/")
        self._keyspace = keyspace
        self._http = httpx.AsyncClient(timeout=timeout)
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None

    @property
    def access_token(self) -> Optional[str]:
        """Current access token, if any."""
        return self._access_token

    @access_token.setter
    def access_token(self, value: Optional[str]) -> None:
        self._access_token = value

    @property
    def refresh_token(self) -> Optional[str]:
        """Current refresh token, if any."""
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value: Optional[str]) -> None:
        self._refresh_token = value

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> "ShroudbAuthClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def _resolve_keyspace(self, keyspace: Optional[str]) -> str:
        """Return the keyspace to use, raising if none provided."""
        ks = keyspace or self._keyspace
        if ks is None:
            raise ValueError(
                "No keyspace provided. Pass keyspace= to the method or set it in the constructor."
            )
        return ks

    def _auth_headers(self) -> dict[str, str]:
        """Headers for endpoints that require access_token auth."""
        if self._access_token is None:
            raise ShroudbAuthError("UNAUTHORIZED", "No access token set. Log in or sign up first.")
        return {"Authorization": f"Bearer {self._access_token}"}

    def _refresh_headers(self) -> dict[str, str]:
        """Headers for endpoints that require refresh_token auth."""
        if self._refresh_token is None:
            raise ShroudbAuthError("UNAUTHORIZED", "No refresh token set. Log in or sign up first.")
        return {"Authorization": f"Bearer {self._refresh_token}"}

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        expected_status: int = 200,
    ) -> dict[str, Any]:
        """Send an HTTP request and return the parsed JSON response.

        Raises:
            ShroudbAuthError: On non-success status codes with error body.
        """
        url = f"{self._base_url}{path}"
        hdrs: dict[str, str] = dict(headers or {})
        resp = await self._http.request(method, url, json=json, headers=hdrs)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                raise ShroudbAuthError._from_response(resp.status_code, data)
            except (ShroudbAuthError, ):
                raise
            except (ValueError, KeyError):
                body_text = resp.text[:500]
                raise ShroudbAuthError("HTTP_ERROR", body_text)
        if resp.status_code != expected_status:
            body_text = resp.text[:500]
            raise ShroudbAuthError(
                "UNEXPECTED_STATUS",
                f"expected {expected_status}, got {resp.status_code}: {body_text}",
            )
        if resp.status_code == 204 or not resp.content:
            return {}
        return resp.json()

    async def change_password(self, new_password: str, old_password: str, *, keyspace: Optional[str] = None) -> ChangePasswordResponse:
        """Change password for the currently authenticated user"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/change-password"
        body: dict[str, Any] = {"new_password": new_password, "old_password": old_password}
        data = await self._request("POST", path, json=body, headers=self._auth_headers(), expected_status=200)
        return ChangePasswordResponse._from_dict(data)


    async def forgot_password(self, user_id: str, *, keyspace: Optional[str] = None) -> ForgotPasswordResponse:
        """Request a password reset token (always returns 200 to prevent enumeration)"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/forgot-password"
        body: dict[str, Any] = {"user_id": user_id}
        data = await self._request("POST", path, json=body, expected_status=200)
        return ForgotPasswordResponse._from_dict(data)


    async def health(self) -> HealthResponse:
        """Health check endpoint"""
        path = "/auth/health"
        data = await self._request("GET", path, expected_status=200)
        return HealthResponse._from_dict(data)


    async def jwks(self, *, keyspace: Optional[str] = None) -> JwksResponse:
        """Public JSON Web Key Set for verifying access tokens"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/.well-known/jwks.json"
        data = await self._request("GET", path, expected_status=200)
        return JwksResponse._from_dict(data)


    async def login(self, password: str, user_id: str, *, keyspace: Optional[str] = None) -> LoginResponse:
        """Authenticate a user and receive access + refresh tokens"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/login"
        body: dict[str, Any] = {"password": password, "user_id": user_id}
        data = await self._request("POST", path, json=body, expected_status=200)
        result = LoginResponse._from_dict(data)
        self._access_token = result.access_token
        self._refresh_token = result.refresh_token
        return result


    async def logout(self, *, keyspace: Optional[str] = None) -> LogoutResponse:
        """Revoke the current refresh token family and clear cookies"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/logout"
        data = await self._request("POST", path, headers=self._refresh_headers(), expected_status=200)
        return LogoutResponse._from_dict(data)


    async def logout_all(self, user_id: str, *, keyspace: Optional[str] = None) -> LogoutAllResponse:
        """Revoke all refresh token families for a user"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/logout-all"
        body: dict[str, Any] = {"user_id": user_id}
        data = await self._request("POST", path, json=body, headers=self._auth_headers(), expected_status=200)
        return LogoutAllResponse._from_dict(data)


    async def refresh(self, *, keyspace: Optional[str] = None) -> RefreshResponse:
        """Exchange a refresh token for new access + refresh tokens"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/refresh"
        data = await self._request("POST", path, headers=self._refresh_headers(), expected_status=200)
        result = RefreshResponse._from_dict(data)
        self._access_token = result.access_token
        self._refresh_token = result.refresh_token
        return result


    async def reset_password(self, new_password: str, token: str, *, keyspace: Optional[str] = None) -> ResetPasswordResponse:
        """Reset password using a single-use reset token (revoked after use)"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/reset-password"
        body: dict[str, Any] = {"new_password": new_password, "token": token}
        data = await self._request("POST", path, json=body, expected_status=200)
        return ResetPasswordResponse._from_dict(data)


    async def session(self, *, keyspace: Optional[str] = None) -> SessionResponse:
        """Validate current session and return user info"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/session"
        data = await self._request("GET", path, headers=self._auth_headers(), expected_status=200)
        return SessionResponse._from_dict(data)


    async def sessions(self, *, keyspace: Optional[str] = None) -> SessionsResponse:
        """List active sessions (refresh token families) for the authenticated user"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/sessions"
        data = await self._request("GET", path, headers=self._auth_headers(), expected_status=200)
        return SessionsResponse._from_dict(data)


    async def signup(self, password: str, user_id: str, *, metadata: Optional[dict[str, Any]] = None, keyspace: Optional[str] = None) -> SignupResponse:
        """Register a new user and receive access + refresh tokens"""
        ks = self._resolve_keyspace(keyspace)
        path = f"/auth/{ks}/signup"
        body: dict[str, Any] = {"password": password, "user_id": user_id}
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._request("POST", path, json=body, expected_status=201)
        result = SignupResponse._from_dict(data)
        self._access_token = result.access_token
        self._refresh_token = result.refresh_token
        return result

