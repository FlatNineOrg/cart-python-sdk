"""Cart API client."""

from __future__ import annotations

from typing import Any

from ._http import HttpClient
from ._resources import (
    AdsResource,
    NichesResource,
    ProductsResource,
    StoresResource,
    SuppliersResource,
)
from ._types import ApiResponse, RateLimitInfo

_DEFAULT_BASE_URL = "https://api.usecart.com/v1"


class Cart:
    """Cart API client for e-commerce intelligence.

    Example::

        from usecart import Cart

        cart = Cart("cart_sk_...")
        stores = cart.stores.search(keyword="fitness")
        print(stores.data)

    Args:
        api_key: Your Cart API key (starts with ``cart_sk_``).
        base_url: Override the default API base URL.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
    ) -> None:
        if not api_key:
            raise ValueError(
                "An API key is required. Pass it as the first argument: "
                "Cart('cart_sk_...')"
            )

        self._http = HttpClient(api_key, base_url)

        self.stores = StoresResource(self._http)
        self.products = ProductsResource(self._http)
        self.ads = AdsResource(self._http)
        self.suppliers = SuppliersResource(self._http)
        self.niches = NichesResource(self._http)

    @property
    def rate_limit(self) -> RateLimitInfo | None:
        """Most recent rate limit info from the last API response."""
        return self._http.rate_limit

    def trending(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        category: str | None = None,
    ) -> ApiResponse:
        """Get trending stores and products. ``GET /v1/trending``"""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "category": category,
        }
        return self._http.get("/trending", params)

    def account(self) -> ApiResponse:
        """Get the authenticated account details. ``GET /v1/account``"""
        return self._http.get("/account")


# Alias for those who prefer the longer name
CartClient = Cart
