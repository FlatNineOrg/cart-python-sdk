"""Error classes for the Cart API SDK."""

from __future__ import annotations


class CartApiError(Exception):
    """Base error class for all Cart API errors.

    Attributes:
        message: Human-readable error description.
        status: HTTP status code returned by the API.
        code: Machine-readable error code (e.g. "invalid_request", "not_found").
        request_id: Unique identifier for the request, useful for support tickets.
    """

    def __init__(
        self,
        message: str,
        status: int,
        code: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"status={self.status}, code={self.code!r}, "
            f"request_id={self.request_id!r})"
        )


class CartAuthError(CartApiError):
    """Thrown when the API returns a 401 Unauthorized response.

    This usually means the API key is missing, invalid, or revoked.
    """

    def __init__(self, message: str, request_id: str | None = None) -> None:
        super().__init__(message, 401, "auth_error", request_id)


class CartRateLimitError(CartApiError):
    """Thrown when the API returns a 429 Too Many Requests response.

    Contains rate limit details so callers can implement backoff.

    Attributes:
        retry_after: Number of seconds until the rate limit resets.
        rate_limit: Maximum number of requests allowed per period.
        rate_limit_remaining: Number of requests remaining in the current period.
    """

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        retry_after: int | None = None,
        rate_limit: int | None = None,
        rate_limit_remaining: int | None = None,
    ) -> None:
        super().__init__(message, 429, "rate_limit_exceeded", request_id)
        self.retry_after = retry_after
        self.rate_limit = rate_limit
        self.rate_limit_remaining = rate_limit_remaining
