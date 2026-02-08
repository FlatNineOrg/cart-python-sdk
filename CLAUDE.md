# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Python SDK for the Cart e-commerce intelligence API (`usecart` on PyPI). Zero runtime dependencies — uses only Python stdlib (`urllib`, `json`, `dataclasses`). Requires Python 3.9+.

## Build & Development Commands

```bash
pip install -e .            # Editable install for development
python -m build             # Build sdist + wheel into dist/
python -m build --wheel     # Build wheel only
mypy src/                   # Type checking (py.typed / PEP 561 compliant)
```

No test suite, linter config, or CI exists yet.

## Architecture

All source lives under `src/usecart/`. Internal modules are prefixed with `_`; the public API is defined in `__init__.py` via `__all__`.

**`_client.py`** — `Cart` (aliased as `CartClient`) is the entry point. Accepts an API key, constructs an `HttpClient`, and exposes resource namespaces (`cart.stores`, `cart.products`, `cart.ads`, `cart.suppliers`, `cart.niches`) plus top-level `cart.trending()` and `cart.account()`.

**`_resources.py`** — Five resource classes (`StoresResource`, `ProductsResource`, `AdsResource`, `SuppliersResource`, `NichesResource`). Each takes an `HttpClient` and exposes methods that map 1:1 to API endpoints. Path segments are URL-encoded via `_encode()`.

**`_http.py`** — `HttpClient` wraps `urllib.request`. Builds URLs with query params (None values filtered out), sets `Authorization: Bearer` + `User-Agent` headers, parses JSON responses into `ApiResponse` dataclasses, and maps HTTP errors to typed exceptions. Caches rate-limit info from `X-RateLimit-*` headers.

**`_types.py`** — `TypedDict` subclasses for API data models (Store, Product, Ad, etc.) and `@dataclass(frozen=True)` containers for responses (`ApiResponse`, `ApiResponseMeta`, `RateLimitInfo`).

**`_errors.py`** — Exception hierarchy: `CartApiError` (base) → `CartAuthError` (401), `CartRateLimitError` (429). Errors carry `status`, `code`, `message`, `request_id`; rate-limit errors add `retry_after`.

## Key Patterns

- Every API method returns `ApiResponse` with `.data`, `.meta`, and `.usage` attributes.
- Query params are built as a dict including None values; `HttpClient._build_url()` strips None entries.
- Response dataclasses are frozen (immutable).
- Uses `from __future__ import annotations` and `TYPE_CHECKING` guards throughout.
- Base URL: `https://api.usecart.com/v1`. API keys start with `cart_sk_`.
