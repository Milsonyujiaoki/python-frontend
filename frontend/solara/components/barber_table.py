"""Barber table component with pagination and search."""

import solara
from .barber_state import (
    get_paginated_barbers,
    get_total_pages,
    get_total_count,
    set_page,
    set_search_query,
    delete_barber,
    loading,
    error,
)

# Define the columns for the barber table
BARBER_COLUMNS = [
    {"label": "ID", "field": "id"},
    {"label": "Name", "field": "name"},
    {"label": "Email", "field": "email"},
    {"label": "Phone", "field": "phone"},
    {"label": "Specialty", "field": "specialty"},
]

# Define the row actions for the barber table
BARBER_ROW_ACTIONS = [
    {
        "label": "Edit",
        "on_click": lambda item: None,  # Navigate to edit page
        "color": "primary",
        "text": True,
        "outline": True,
    },
    {
        "label": "Delete",
        "on_click": lambda item: delete_barber(item.get("id")),
        "color": "error",
        "text": True,
        "outline": True,
    },
]


@solara.component
def BarberTable():
    """
    Barber table with pagination, search, and performance optimizations.

    Features:
    - Server-side pagination for large datasets
    - Debounced search across name, email, phone, and specialty
    - Optimistic updates for delete operations
    - Loading and error states
    """
    # Get paginated data (memoized)
    page_items = get_paginated_barbers()
    total_pages = get_total_pages()
    total_count = get_total_count()

    # Page change handler
    def handle_page_change(page: int):
        set_page(page)

    # Import base table dynamically to avoid circular imports
    from .components.base_table import BaseTable

    return BaseTable(
        title="Barbers",
        columns=BARBER_COLUMNS,
        items=page_items,
        row_actions=BARBER_ROW_ACTIONS,
        pagination=True,
        page_size=10,
        searchable=True,
        search_field=None,  # Search all fields
        loading=loading.value,
        error=error.value,
        on_page_change=handle_page_change,
    )