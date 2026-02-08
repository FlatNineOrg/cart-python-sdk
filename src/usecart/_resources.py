"""Resource classes for the Cart API SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._types import ApiResponse

if TYPE_CHECKING:
    from ._http import HttpClient

try:
    from urllib.parse import quote as _quote
except ImportError:  # pragma: no cover
    from urllib import quote as _quote  # type: ignore[attr-defined,no-redef]


def _encode(segment: str) -> str:
    """URL-encode a path segment."""
    return _quote(segment, safe="")


class StoresResource:
    """Namespace for store-related endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        *,
        keyword: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort: str | None = None,
        platform: str | None = None,
        language: str | None = None,
        currency: str | None = None,
        biz_model: str | None = None,
        has_ads: bool | None = None,
        status: str | None = None,
        min_traffic: int | None = None,
    ) -> ApiResponse:
        """Search for stores. ``GET /v1/stores``"""
        params: dict[str, Any] = {
            "keyword": keyword,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            "platform": platform,
            "language": language,
            "currency": currency,
            "biz_model": biz_model,
            "has_ads": has_ads,
            "status": status,
            "min_traffic": min_traffic,
        }
        return self._http.get("/stores", params)

    def get(self, domain: str) -> ApiResponse:
        """Get a single store by domain. ``GET /v1/stores/:domain``"""
        return self._http.get(f"/stores/{_encode(domain)}")

    def get_products(
        self,
        domain: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
        sort: str | None = None,
    ) -> ApiResponse:
        """Get products for a store. ``GET /v1/stores/:domain/products``"""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "sort": sort,
        }
        return self._http.get(f"/stores/{_encode(domain)}/products", params)

    def get_ads(self, domain: str) -> ApiResponse:
        """Get ads for a store. ``GET /v1/stores/:domain/ads``"""
        return self._http.get(f"/stores/{_encode(domain)}/ads")

    def get_traffic(self, domain: str) -> ApiResponse:
        """Get traffic data for a store. ``GET /v1/stores/:domain/traffic``"""
        return self._http.get(f"/stores/{_encode(domain)}/traffic")

    def get_tech(self, domain: str) -> ApiResponse:
        """Get technology stack for a store. ``GET /v1/stores/:domain/tech``"""
        return self._http.get(f"/stores/{_encode(domain)}/tech")

    def compare(self, domains: list[str]) -> ApiResponse:
        """Compare multiple stores. ``GET /v1/stores/compare?domains=a.com,b.com``"""
        return self._http.get("/stores/compare", {"domains": domains})


class ProductsResource:
    """Namespace for product-related endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        *,
        keyword: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        currency: str | None = None,
    ) -> ApiResponse:
        """Search for products. ``GET /v1/products``"""
        params: dict[str, Any] = {
            "keyword": keyword,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            "min_price": min_price,
            "max_price": max_price,
            "currency": currency,
        }
        return self._http.get("/products", params)

    def get(self, id: str) -> ApiResponse:
        """Get a single product by ID. ``GET /v1/products/:id``"""
        return self._http.get(f"/products/{_encode(id)}")

    def trending(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        category: str | None = None,
    ) -> ApiResponse:
        """Get trending products. ``GET /v1/products/trending``"""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "category": category,
        }
        return self._http.get("/products/trending", params)


class AdsResource:
    """Namespace for ad-related endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        *,
        keyword: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort: str | None = None,
        platform: str | None = None,
        store_domain: str | None = None,
    ) -> ApiResponse:
        """Search for ads. ``GET /v1/ads``"""
        params: dict[str, Any] = {
            "keyword": keyword,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            "platform": platform,
            "store_domain": store_domain,
        }
        return self._http.get("/ads", params)

    def get(self, id: str) -> ApiResponse:
        """Get a single ad by ID. ``GET /v1/ads/:id``"""
        return self._http.get(f"/ads/{_encode(id)}")


class SuppliersResource:
    """Namespace for supplier-related endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search(
        self,
        *,
        keyword: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort: str | None = None,
        location: str | None = None,
        type: str | None = None,
    ) -> ApiResponse:
        """Search for suppliers. ``GET /v1/suppliers``"""
        params: dict[str, Any] = {
            "keyword": keyword,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            "location": location,
            "type": type,
        }
        return self._http.get("/suppliers", params)


class NichesResource:
    """Namespace for niche-related endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, keyword: str) -> ApiResponse:
        """Get a niche overview by keyword. ``GET /v1/niches/:keyword``"""
        return self._http.get(f"/niches/{_encode(keyword)}")
