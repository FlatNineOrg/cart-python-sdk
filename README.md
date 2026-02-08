# usecart

Python SDK for the [Cart](https://usecart.com) e-commerce intelligence API.

Zero dependencies. Python 3.9+.

## Install

```bash
pip install usecart
```

## Quick Start

```python
from usecart import Cart

cart = Cart("cart_sk_...")

# Search stores
stores = cart.stores.search(keyword="fitness", platform="shopify", min_traffic=10000)
print(stores.data)
# [{"domain": "gymshark.com", "traffic": 4200000, ...}, ...]

# Get a single store
store = cart.stores.get("gymshark.com")

# Search products
products = cart.products.search(keyword="yoga mat", min_price=20)

# Get trending
trending = cart.trending()

# Check rate limits
print(cart.rate_limit)
# RateLimitInfo(remaining=99, limit=100)
```

## Response Shape

Every method returns an `ApiResponse` with three attributes:

```python
response = cart.stores.search(keyword="fitness")

response.data          # list of dicts or single dict
response.meta          # ApiResponseMeta(request_id, timestamp, page, total_pages, total_results)
response.usage         # ApiResponseUsage(requests_today, limit)
```

## Resources

| Resource | Methods |
|----------|---------|
| `cart.stores` | `search()`, `get()`, `get_products()`, `get_ads()`, `get_traffic()`, `get_tech()`, `compare()` |
| `cart.products` | `search()`, `get()`, `trending()` |
| `cart.ads` | `search()`, `get()` |
| `cart.suppliers` | `search()` |
| `cart.niches` | `get()` |
| top-level | `cart.trending()`, `cart.account()` |

## Error Handling

```python
from usecart import Cart, CartAuthError, CartRateLimitError, CartApiError

cart = Cart("cart_sk_...")

try:
    stores = cart.stores.search(keyword="fitness")
except CartAuthError as e:
    print(f"Auth failed: {e}")
except CartRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except CartApiError as e:
    print(f"API error {e.status}: {e.message}")
```

## Links

- [Documentation](https://docs.usecart.com)
- [API Reference](https://docs.usecart.com)
- [TypeScript SDK](https://www.npmjs.com/package/@usecart/sdk)
