"""
API service for data fetching with caching and error handling.

Provides optimized data fetching with caching, retries, and error handling.
"""

import solara
from typing import Any, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import asyncio
import time

T = TypeVar('T')


class LoadState(Enum):
    """State of a data loading operation."""
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class LoadResult(Generic[T]):
    """Result of a data loading operation."""
    data: Optional[T]
    state: LoadState
    error: Optional[str] = None
    last_updated: Optional[float] = None


class ApiService:
    """
    Service for making API calls with caching and error handling.

    Features:
    - Response caching with configurable TTL
    - Automatic retries with exponential backoff
    - Request deduplication
    - Error handling and retry logic
    """

    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self._cache: Dict[str, LoadResult] = {}
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._default_ttl = 300  # 5 minutes

    async def _fetch_with_retry(
        self,
        url: str,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> Any:
        """
        Fetch data from URL with retry logic.

        Args:
            url: The URL to fetch
            max_retries: Maximum number of retry attempts
            backoff_factor: Multiplier for delay between retries

        Returns:
            The response data

        Raises:
            Exception: If all retries fail
        """
        import httpx

        last_error = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=10.0)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise  # Don't retry 404s
                last_error = str(e)
            except httpx.RequestError as e:
                last_error = str(e)
            except Exception as e:
                last_error = str(e)

            if attempt < max_retries - 1:
                await asyncio.sleep(backoff_factor * (2 ** attempt))

        raise Exception(f"Failed after {max_retries} retries: {last_error}")

    async def fetch(
        self,
        endpoint: str,
        cache_key: Optional[str] = None,
        ttl: Optional[int] = None,
        force_refresh: bool = False,
    ) -> LoadResult[List[Dict[str, Any]]]:
        """
        Fetch data from an API endpoint with caching.

        Args:
            endpoint: API endpoint path
            cache_key: Optional custom cache key
            ttl: Time-to-live in seconds (default: 300)
            force_refresh: Force refresh from server

        Returns:
            LoadResult with data or error
        """
        cache_key = cache_key or f"{endpoint}"
        ttl = ttl or self._default_ttl

        # Check cache first
        if not force_refresh and cache_key in self._cache:
            cached = self._cache[cache_key]
            if cached.state == LoadState.SUCCESS:
                if cached.last_updated and time.time() - cached.last_updated < ttl:
                    return cached

        # Check for pending request
        if cache_key in self._pending_requests:
            try:
                data = await self._pending_requests[cache_key]
                return LoadResult(data=data, state=LoadState.SUCCESS)
            except Exception as e:
                return LoadResult(data=None, state=LoadState.ERROR, error=str(e))

        # Set loading state
        self._cache[cache_key] = LoadResult(
            data=None,
            state=LoadState.LOADING,
        )

        # Create pending request
        future = asyncio.Future()
        self._pending_requests[cache_key] = future

        try:
            url = f"{self.base_url}{endpoint}"
            data = await self._fetch_with_retry(url)
            future.set_result(data)

            # Update cache
            self._cache[cache_key] = LoadResult(
                data=data,
                state=LoadState.SUCCESS,
                last_updated=time.time(),
            )
            return self._cache[cache_key]

        except Exception as e:
            future.set_exception(e)
            self._cache[cache_key] = LoadResult(
                data=None,
                state=LoadState.ERROR,
                error=str(e),
            )
            return self._cache[cache_key]

        finally:
            self._pending_requests.pop(cache_key, None)

    def invalidate(self, cache_key: str) -> None:
        """Invalidate a cached entry."""
        self._cache.pop(cache_key, None)

    def invalidate_all(self) -> None:
        """Clear all cached data."""
        self._cache.clear()


# Global API service instance
api_service = ApiService()


# Reactive state wrapper for API data
@solara.component
def use_api_data(
    endpoint: str,
    cache_key: Optional[str] = None,
    ttl: int = 300,
    auto_fetch: bool = True,
):
    """
    React hook for fetching API data with caching.

    Usage:
        data, loading, error, refresh = use_api_data("/customers")

    Args:
        endpoint: API endpoint path
        cache_key: Optional custom cache key
        ttl: Cache TTL in seconds
        auto_fetch: Automatically fetch on mount

    Returns:
        Tuple of (data, loading, error, refresh_fn)
    """
    result, set_result = solara.use_state(
        LoadResult(data=None, state=LoadState.IDLE)
    )
    cache_key = cache_key or endpoint

    async def fetch_data():
        set_result(LoadResult(data=None, state=LoadState.LOADING))
        result = await api_service.fetch(
            endpoint,
            cache_key=cache_key,
            ttl=ttl,
        )
        set_result(result)

    def refresh():
        asyncio.create_task(fetch_data())

    solara.use_effect(
        lambda: fetch_data() if auto_fetch else None,
        [endpoint, cache_key]
    )

    return (
        result.data,
        result.state == LoadState.LOADING,
        result.error,
        refresh,
    )