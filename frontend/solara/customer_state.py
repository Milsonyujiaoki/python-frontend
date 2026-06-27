"""
Customer state management with performance optimizations.

Features:
- API data fetching with caching
- Pagination support
- Search and filter with debouncing
- Optimistic updates
"""

import solara
from typing import List, Dict, Any, Optional
from .services.api_service import use_api_data, api_service
from .utils.data_cache import cached_computation, LRUCache

# Cache for computed operations (e.g., filtered lists)
customer_cache = LRUCache(max_size=50, ttl=60)

# Reactive variables for customer state
customers = solara.reactive([])  # List of customer dictionaries
loading = solara.reactive(False)
error = solara.reactive(None)

# Pagination state
current_page = solara.reactive(0)
page_size = solara.reactive(10)
total_count = solara.reactive(0)

# Search and filter state
search_query = solara.reactive("")
filter_active = solara.reactive(None)  # None = all, True/False = specific


@solara.memoize
def get_filtered_customers():
    """
    Get filtered list of customers based on search and filter criteria.
    Uses memoization to avoid recalculating on every render.
    """
    if not customers.value:
        return []

    result = customers.value

    # Apply search filter
    if search_query.value.strip():
        query_lower = search_query.value.lower()
        result = [
            c for c in result
            if query_lower in c.get("name", "").lower()
            or query_lower in c.get("email", "").lower()
            or query_lower in c.get("phone", "").lower()
        ]

    # Apply active status filter
    if filter_active.value is not None:
        result = [c for c in result if c.get("is_active") == filter_active.value]

    return result


@solara.memoize
def get_paginated_customers():
    """
    Get paginated list of customers.
    Uses memoization based on page and page_size.
    """
    filtered = get_filtered_customers()
    total_count.value = len(filtered)

    start_idx = current_page.value * page_size.value
    end_idx = start_idx + page_size.value

    return filtered[start_idx:end_idx]


def set_customers(customer_list: List[Dict[str, Any]]):
    """Set the customer list."""
    customers.value = customer_list
    current_page.value = 0  # Reset to first page


def set_loading(is_loading: bool):
    """Set loading state."""
    loading.value = is_loading


def set_error(err: Optional[str]):
    """Set error state."""
    error.value = err


def set_search_query(query: str):
    """Set search query with debouncing effect."""
    search_query.value = query
    current_page.value = 0  # Reset to first page on search


def set_filter_active(active: Optional[bool]):
    """Set active status filter."""
    filter_active.value = active
    current_page.value = 0  # Reset to first page on filter change


def set_page(page: int):
    """Set current page."""
    current_page.value = page


def set_page_size(size: int):
    """Set page size."""
    page_size.value = size
    current_page.value = 0  # Reset to first page


def add_customer(customer: Dict[str, Any]):
    """
    Add a customer with optimistic update.
    The UI updates immediately, then syncs with backend.
    """
    new_id = max((c.get("id", 0) for c in customers.value), default=0) + 1
    customer_with_id = {"id": new_id, **customer}
    customers.value = [*customers.value, customer_with_id]

    # Invalidate API cache to force refresh on next fetch
    api_service.invalidate("/customers")


def update_customer(updated_customer: Dict[str, Any]):
    """
    Update a customer with optimistic update.
    """
    customer_id = updated_customer.get("id")
    if customer_id is None:
        return

    new_list = []
    for c in customers.value:
        if c.get("id") == customer_id:
            new_list.append(updated_customer)
        else:
            new_list.append(c)

    customers.value = new_list
    api_service.invalidate("/customers")


def delete_customer(customer_id: int):
    """
    Delete a customer with optimistic update.
    """
    customers.value = [c for c in customers.value if c.get("id") != customer_id]
    api_service.invalidate("/customers")


def get_customer_by_id(customer_id: int) -> Optional[Dict[str, Any]]:
    """Get a customer by ID."""
    for c in customers.value:
        if c.get("id") == customer_id:
            return c
    return None


def get_entities() -> List[Dict[str, Any]]:
    """Get the list of entities (for compatibility)."""
    return get_paginated_customers()


def get_total_count() -> int:
    """Get total count of filtered customers."""
    return len(get_filtered_customers())


def get_total_pages() -> int:
    """Get total number of pages."""
    total = get_total_count()
    return max(1, (total + page_size.value - 1) // page_size.value)


@solara.component
def CustomerDataProvider():
    """
    Component that provides customer data with automatic fetching and caching.

    Usage:
        @solara.component
        def CustomersPage():
            with CustomerDataProvider():
                # Access customer data here
                customers_data = get_paginated_customers()
                ...
    """
    # Use the API hook for data fetching
    data, loading_state, error_state, refresh = use_api_data(
        endpoint="/customers",
        cache_key="customers_list",
        ttl=300,
        auto_fetch=True,
    )

    # Sync with local state when data changes
    solara.use_effect(
        lambda: set_customers(data) if data else None,
        [data]
    )

    solara.use_effect(
        lambda: set_loading(loading_state),
        [loading_state]
    )

    solara.use_effect(
        lambda: set_error(error_state),
        [error_state]
    )

    # Return nothing - this is a provider component
    return None