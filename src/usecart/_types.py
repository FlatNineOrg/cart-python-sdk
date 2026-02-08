"""Type definitions for the Cart API SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, TypedDict


# ─── Core Resource Types ─────────────────────────────────────────────────────


class Store(TypedDict, total=False):
    domain: str
    platform: str
    currency: str
    products_count: int
    vendors_count: int
    monthly_visitors: int
    monthly_visitors_trend: float
    bounce_rate: float
    avg_visit_length: float
    pages_per_visit: float
    language: str
    meta_title: str
    meta_description: str
    is_live: bool
    is_dropshipping: bool
    is_pod: bool
    facebook: str | None
    twitter: str | None
    instagram: str | None
    created_at: str


class Product(TypedDict, total=False):
    id: str
    store_domain: str
    title: str
    handle: str
    image: str
    price: float
    initial_price: float
    currency: str
    vendor: str
    added_at: str


class TrafficGeo(TypedDict):
    country: str
    percentage: float


class TrafficSource(TypedDict):
    direct: float
    search: float
    social: float
    mail: float
    display: float
    referrals: float


class StoreTraffic(TypedDict, total=False):
    monthly_visitors: int
    trend: float
    bounce_rate: float
    avg_visit_length: float
    pages_per_visit: float
    traffic_by_geo: List[TrafficGeo]
    traffic_by_source: TrafficSource


class StoreTechItem(TypedDict):
    name: str
    category: str


# StoreTech is a list of StoreTechItem
StoreTech = List[StoreTechItem]


class Ad(TypedDict, total=False):
    id: str
    store_domain: str
    platform: str
    image: str
    landing_url: str
    first_seen: str
    last_seen: str


class Supplier(TypedDict, total=False):
    id: str
    name: str
    location: str
    type: str
    product_types: List[str]


class NicheOverview(TypedDict, total=False):
    keyword: str
    total_stores: int
    total_products: int
    avg_price: float
    top_stores: List[Store]
    trending_products: List[Product]


class Account(TypedDict):
    email: str
    plan: str
    requests_today: int
    requests_limit: int


class TrendingData(TypedDict):
    stores: List[Store]
    products: List[Product]


# ─── API Response Types ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class ApiResponseMeta:
    """Metadata about the API response."""

    request_id: str
    timestamp: str
    page: int
    total_pages: int
    total_results: int


@dataclass(frozen=True)
class ApiResponseUsage:
    """API usage information."""

    requests_today: int
    limit: int


@dataclass(frozen=True)
class ApiResponse:
    """Wrapper for all API responses.

    Attributes:
        data: The response payload (list of dicts or single dict).
        meta: Response metadata (request_id, pagination, etc.).
        usage: API usage stats (requests_today, limit).
    """

    data: object
    meta: ApiResponseMeta
    usage: ApiResponseUsage


# ─── Rate Limit Info ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class RateLimitInfo:
    """Rate limit information from response headers."""

    remaining: int
    limit: int
