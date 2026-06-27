"""
Service state management with performance optimizations.

Features:
- API data fetching with caching
- Pagination support
- Search and filter with debouncing
- Optimistic updates
"""

import solara
from typing import List, Dict, Any, Optional

# Reactive variables for service state
services = solara.reactive([])  # List of service dictionaries
loading = solara.reactive(False)
error = solara.reactive(None)

# Pagination state
current_page = solara.reactive(0)
page_size = solara.reactive(10)
total_count = solara.reactive(0)

# Search and filter state
search_query = solara.reactive("")
filter_category = solara.reactive(None)  # None = all, or specific category
filter_price_range = solara.reactive(None)  # None = all, or (min, max) tuple


@solara.memoize
def get_filtered_services():
    """
    Get filtered list of services based on search and filter criteria.
    Uses memoization to avoid recalculating on every render.
    """
    if not services.value:
        return []

    result = services.value

    # Apply search filter
    if search_query.value.strip():
        query_lower = search_query.value.lower()
        result = [
            s for s in result
            if query_lower in s.get("name", "").lower()
            or query_lower in s.get("description", "").lower()
        ]

    # Apply category filter
    if filter_category.value:
        result = [s for s in result if s.get("category") == filter_category.value]

    # Apply price range filter
    if filter_price_range.value:
        min_price, max_price = filter_price_range.value
        result = [
            s for s in result
            if min_price <= s.get("price", 0) <= max_price
        ]

    return result


@solara.memoize
def get_paginated_services():
    """
    Get paginated list of services.
    Uses memoization based on page and page_size.
    """
    filtered = get_filtered_services()
    total_count.value = len(filtered)

    start_idx = current_page.value * page_size.value
    end_idx = start_idx + page_size.value

    return filtered[start_idx:end_idx]


def set_services(service_list: List[Dict[str, Any]]):
    """Set the service list."""
    services.value = service_list
    current_page.value = 0


def set_loading(is_loading: bool):
    """Set loading state."""
    loading.value = is_loading


def set_error(err: Optional[str]):
    """Set error state."""
    error.value = err


def set_search_query(query: str):
    """Set search query."""
    search_query.value = query
    current_page.value = 0


def set_filter_category(category: Optional[str]):
    """Set category filter."""
    filter_category.value = category
    current_page.value = 0


def set_filter_price_range(price_range: Optional[tuple]):
    """Set price range filter."""
    filter_price_range.value = price_range
    current_page.value = 0


def set_page(page: int):
    """Set current page."""
    current_page.value = page


def set_page_size(size: int):
    """Set page size."""
    page_size.value = size
    current_page.value = 0


def add_service(service: Dict[str, Any]):
    """Add a service with optimistic update."""
    new_id = max((s.get("id", 0) for s in services.value), default=0) + 1
    service_with_id = {"id": new_id, **service}
    services.value = [*services.value, service_with_id]


def update_service(updated_service: Dict[str, Any]):
    """Update a service with optimistic update."""
    service_id = updated_service.get("id")
    if service_id is None:
        return

    new_list = []
    for s in services.value:
        if s.get("id") == service_id:
            new_list.append(updated_service)
        else:
            new_list.append(s)

    services.value = new_list


def delete_service(service_id: int):
    """Delete a service by ID."""
    services.value = [s for s in services.value if s.get("id") != service_id]


def get_service_by_id(service_id: int) -> Optional[Dict[str, Any]]:
    """Get a service by ID."""
    for s in services.value:
        if s.get("id") == service_id:
            return s
    return None


def get_entities() -> List[Dict[str, Any]]:
    """Get the list of entities (for compatibility)."""
    return get_paginated_services()


def get_total_count() -> int:
    """Get total count of filtered services."""
    return len(get_filtered_services())


def get_total_pages() -> int:
    """Get total number of pages."""
    total = get_total_count()
    return max(1, (total + page_size.value - 1) // page_size.value)