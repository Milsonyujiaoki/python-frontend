"""Service table component with pagination and search."""

import solara
from .service_state import (
    get_paginated_services,
    get_total_pages,
    get_total_count,
    set_page,
    set_search_query,
    delete_service,
    loading,
    error,
)


def format_price(value):
    """Format price as currency with two decimal places."""
    try:
        return f"${float(value):.2f}"
    except (ValueError, TypeError):
        return "$0.00"


# Define the columns for the service table
SERVICE_COLUMNS = [
    {"label": "ID", "field": "id"},
    {"label": "Name", "field": "name"},
    {"label": "Description", "field": "description"},
    {"label": "Duration", "field": "duration"},
    {"label": "Price", "field": "price", "format": format_price},
]

# Define the row actions for the service table
SERVICE_ROW_ACTIONS = [
    {
        "label": "Edit",
        "on_click": lambda item: None,  # Navigate to edit page
        "color": "primary",
        "text": True,
        "outline": True,
    },
    {
        "label": "Delete",
        "on_click": lambda item: delete_service(item.get("id")),
        "color": "error",
        "text": True,
        "outline": True,
    },
]


@solara.component
def ServiceTable():
    """
    Service table with pagination, search, and performance optimizations.

    Features:
    - Server-side pagination for large datasets
    - Debounced search across name and description
    - Price formatting
    - Optimistic updates for delete operations
    - Loading and error states
    """
    # Get paginated data (memoized)
    page_items = get_paginated_services()
    total_pages = get_total_pages()
    total_count = get_total_count()

    # Page change handler
    def handle_page_change(page: int):
        set_page(page)

    # Import base table dynamically to avoid circular imports
    from .components.base_table import BaseTable

    return BaseTable(
        title="Services",
        columns=SERVICE_COLUMNS,
        items=page_items,
        row_actions=SERVICE_ROW_ACTIONS,
        pagination=True,
        page_size=10,
        searchable=True,
        search_field=None,  # Search all fields
        loading=loading.value,
        error=error.value,
        on_page_change=handle_page_change,
    )