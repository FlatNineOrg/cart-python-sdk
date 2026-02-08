"""HTTP client for the Cart API using only stdlib."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

from ._errors import CartApiError, CartAuthError, CartRateLimitError
from ._types import ApiResponse, ApiResponseMeta, ApiResponseUsage, RateLimitInfo

_VERSION = "0.1.0"


class HttpClient:
    """Low-level HTTP client that handles auth, serialization, and errors."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self.rate_limit: RateLimitInfo | None = None

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse:
        """Execute an authenticated GET request against the Cart API."""
        url = self._build_url(path, params)

        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Accept": "application/json",
                "User-Agent": f"usecart-python/{_VERSION}",
            },
        )

        try:
            with urllib.request.urlopen(req) as resp:
                self._parse_rate_limit_headers(resp)
                body = json.loads(resp.read().decode("utf-8"))
                return self._parse_response(body)
        except urllib.error.HTTPError as exc:
            self._parse_rate_limit_headers(exc)
            self._handle_error_response(exc)

    def _build_url(self, path: str, params: dict[str, Any] | None) -> str:
        """Build the full URL with query string."""
        url = f"{self._base_url}{path}"

        if not params:
            return url

        parts: list[str] = []
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                parts.append(f"{urllib.parse.quote(key)}={str(value).lower()}")
            elif isinstance(value, list):
                joined = ",".join(
                    urllib.parse.quote(str(v), safe="") for v in value
                )
                parts.append(f"{urllib.parse.quote(key)}={joined}")
            else:
                parts.append(
                    f"{urllib.parse.quote(key)}={urllib.parse.quote(str(value), safe='')}"
                )

        if parts:
            url = f"{url}?{'&'.join(parts)}"

        return url

    def _parse_rate_limit_headers(self, resp: Any) -> None:
        """Extract rate limit information from response headers."""
        remaining = resp.headers.get("X-RateLimit-Remaining")
        limit = resp.headers.get("X-RateLimit-Limit")

        if remaining is not None and limit is not None:
            self.rate_limit = RateLimitInfo(
                remaining=int(remaining),
                limit=int(limit),
            )

    def _handle_error_response(self, exc: urllib.error.HTTPError) -> NoReturn:
        """Parse an error response and raise the appropriate typed error."""
        status = exc.code
        code = "unknown_error"
        message = f"Cart API error: {status}"
        request_id: str | None = None

        try:
            body = json.loads(exc.read().decode("utf-8"))
            error = body.get("error", {})
            if error:
                code = error.get("code", code)
                message = error.get("message", message)
                request_id = error.get("request_id")
        except (json.JSONDecodeError, AttributeError):
            pass

        if status == 401:
            raise CartAuthError(message, request_id)

        if status == 429:
            retry_after_header = exc.headers.get("Retry-After")
            retry_after = (
                int(retry_after_header) if retry_after_header else None
            )
            raise CartRateLimitError(
                message,
                request_id,
                retry_after,
                self.rate_limit.limit if self.rate_limit else None,
                self.rate_limit.remaining if self.rate_limit else None,
            )

        raise CartApiError(message, status, code, request_id)

    @staticmethod
    def _parse_response(body: dict[str, Any]) -> ApiResponse:
        """Parse a successful JSON response into an ApiResponse."""
        raw_meta = body.get("meta", {})
        meta = ApiResponseMeta(
            request_id=raw_meta.get("request_id", ""),
            timestamp=raw_meta.get("timestamp", ""),
            page=raw_meta.get("page", 0),
            total_pages=raw_meta.get("total_pages", 0),
            total_results=raw_meta.get("total_results", 0),
        )

        raw_usage = body.get("usage", {})
        usage = ApiResponseUsage(
            requests_today=raw_usage.get("requests_today", 0),
            limit=raw_usage.get("limit", 0),
        )

        return ApiResponse(
            data=body.get("data"),
            meta=meta,
            usage=usage,
        )
