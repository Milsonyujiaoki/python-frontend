"""
Data caching utilities for Solara frontend.

Provides caching, memoization, and performance optimizations for large datasets.
"""

import solara
from typing import Any, Dict, List, Optional, Callable, TypeVar
from functools import lru_cache
import time
from collections import OrderedDict

T = TypeVar('T')


class LRUCache:
    """
    Least Recently Used cache for storing API responses and computed data.

    Args:
        max_size: Maximum number of items to cache
        ttl: Time-to-live in seconds for cache entries
    """

    def __init__(self, max_size: int = 100, ttl: int = 300):
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: Dict[str, float] = {}
        self.max_size = max_size
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """Get an item from the cache, or None if not found or expired."""
        if key not in self._cache:
            return None

        # Check if expired
        if time.time() - self._timestamps[key] > self.ttl:
            self._cache.pop(key)
            self._timestamps.pop(key)
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]

    def set(self, key: str, value: Any) -> None:
        """Set an item in the cache."""
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        self._timestamps[key] = time.time()

        # Evict oldest if over capacity
        if len(self._cache) > self.max_size:
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key)
            self._timestamps.pop(oldest_key)

    def invalidate(self, key: str) -> None:
        """Remove an item from the cache."""
        if key in self._cache:
            self._cache.pop(key)
            self._timestamps.pop(key)

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
        self._timestamps.clear()


# Global cache instance for API data
api_cache = LRUCache(max_size=50, ttl=300)  # 5 minute TTL


# Global cache instance for computed data
computed_cache = LRUCache(max_size=100, ttl=60)  # 1 minute TTL


@solara.memoize
def cached_computation(key: str, compute_fn: Callable[[], T], invalidate: bool = False) -> T:
    """
    Memoize an expensive computation using Solara's built-in memoization.

    Args:
        key: Cache key for the computation
        compute_fn: Function that performs the expensive computation
        invalidate: If True, invalidate the cached result

    Returns:
        The computed or cached value
    """
    if invalidate:
        api_cache.invalidate(key)
        return compute_fn()

    cached = api_cache.get(key)
    if cached is not None:
        return cached

    result = compute_fn()
    api_cache.set(key, result)
    return result


def debounce(delay_ms: int = 300):
    """
    Decorator factory for debouncing function calls.

    Useful for search inputs and filters to avoid excessive computations.

    Args:
        delay_ms: Delay in milliseconds before executing the function

    Returns:
        Decorator function
    """
    import asyncio
    from functools import wraps

    def decorator(func):
        last_call = None
        pending_task = None

        @wraps(func)
        @solara.component
        def wrapper(*args, **kwargs):
            nonlocal last_call, pending_task

            # Create a reactive variable for the debounced value
            debounced_value, set_debounced_value = solara.use_state(None)
            timer, set_timer = solara.use_state(None)

            def call_function():
                result = func(*args, **kwargs)
                set_debounced_value(result)

            def schedule_call():
                # Cancel previous timer if exists
                if timer is not None:
                    timer.cancel()

                # Schedule new call
                new_timer = asyncio.call_later(delay_ms / 1000.0, call_function)
                set_timer(new_timer)

            schedule_call()

            return debounced_value

        return wrapper

    return decorator