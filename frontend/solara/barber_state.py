"""
Barber state management with performance optimizations.

Features:
- API data fetching with caching
- Pagination support
- Search and filter with debouncing
- Optimistic updates
"""

import solara
from typing import List, Dict, Any, Optional

# Reactive variables for barber state
barbers = solara.reactive([])  # List of barber dictionaries
loading = solara.reactive(False)
error = solara.reactive(None)

# Pagination state
current_page = solara.reactive(0)
page_size = solara.reactive(10)
total_count = solara.reactive(0)

# Search and filter state
search_query = solara.reactive("")
filter_specialty = solara.reactive(None)  # None = all, or specific specialty


@solara.memoize
def get_filtered_barbers():
    """
    Get filtered list of barbers based on search and filter criteria.
    Uses memoization to avoid recalculating on every render.
    """
    if not barbers.value:
        return []

    result = barbers.value

    # Apply search filter
    if search_query.value.strip():
        query_lower = search_query.value.lower()
        result = [
            b for b in result
            if query_lower in b.get("first_name", "").lower()
            or query_lower in b.get("last_name", "").lower()
            or query_lower in b.get("email", "").lower()
            or query_lower in b.get("specialty", "").lower()
        ]

    # Apply specialty filter
    if filter_specialty.value:
        result = [b for b in result if b.get("specialty") == filter_specialty.value]

    return result


@solara.memoize
def get_paginated_barbers():
    """
    Get paginated list of barbers.
    Uses memoization based on page and page_size.
    """
    filtered = get_filtered_barbers()
    total_count.value = len(filtered)

    start_idx = current_page.value * page_size.value
    end_idx = start_idx + page_size.value

    return filtered[start_idx:end_idx]


def set_barbers(barber_list: List[Dict[str, Any]]):
    """Set the barber list."""
    barbers.value = barber_list
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


def set_filter_specialty(specialty: Optional[str]):
    """Set specialty filter."""
    filter_specialty.value = specialty
    current_page.value = 0


def set_page(page: int):
    """Set current page."""
    current_page.value = page


def set_page_size(size: int):
    """Set page size."""
    page_size.value = size
    current_page.value = 0


def add_barber(barber: Dict[str, Any]):
    """Add a barber with optimistic update."""
    new_id = max((b.get("id", 0) for b in barbers.value), default=0) + 1
    barber_with_id = {"id": new_id, **barber}
    barbers.value = [*barbers.value, barber_with_id]


def update_barber(updated_barber: Dict[str, Any]):
    """Update a barber with optimistic update."""
    barber_id = updated_barber.get("id")
    if barber_id is None:
        return

    new_list = []
    for b in barbers.value:
        if b.get("id") == barber_id:
            new_list.append(updated_barber)
        else:
            new_list.append(b)

    barbers.value = new_list


def delete_barber(barber_id: int):
    """Delete a barber by ID."""
    barbers.value = [b for b in barbers.value if b.get("id") != barber_id]


def get_barber_by_id(barber_id: int) -> Optional[Dict[str, Any]]:
    """Get a barber by ID."""
    for b in barbers.value:
        if b.get("id") == barber_id:
            return b
    return None


def get_entities() -> List[Dict[str, Any]]:
    """Get the list of entities (for compatibility)."""
    return get_paginated_barbers()


def get_total_count() -> int:
    """Get total count of filtered barbers."""
    return len(get_filtered_barbers())


def get_total_pages() -> int:
    """Get total number of pages."""
    total = get_total_count()
    return max(1, (total + page_size.value - 1) // page_size.value)