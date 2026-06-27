"""Customer table component with pagination and search."""

import solara
from .customer_state import (
    get_paginated_customers,
    get_total_pages,
    get_total_count,
    set_page,
    set_search_query,
    delete_customer,
    customers,
    loading,
    error,
)

# Define the columns for the customer table
CUSTOMER_COLUMNS = [
    {"label": "ID", "field": "id"},
    {"label": "Name", "field": "name"},
    {"label": "Email", "field": "email"},
    {"label": "Phone", "field": "phone"},
]

# Define the row actions for the customer table
CUSTOMER_ROW_ACTIONS = [
    {
        "label": "Edit",
        "on_click": lambda item: None,  # Navigate to edit page
        "color": "primary",
        "text": True,
        "outline": True,
    },
    {
        "label": "Delete",
        "on_click": lambda item: delete_customer(item.get("id")),
        "color": "error",
        "text": True,
        "outline": True,
    },
]


@solara.component
def CustomerTable():
    """
    Customer table with pagination, search, and performance optimizations.

    Features:
    - Server-side pagination for large datasets
    - Debounced search across name, email, and phone
    - Optimistic updates for delete operations
    - Loading and error states
    """
    # Get paginated data (memoized)
    page_items = get_paginated_customers()
    total_pages = get_total_pages()
    total_count = get_total_count()

    # Page change handler
    def handle_page_change(page: int):
        set_page(page)

    # Import base table dynamically to avoid circular imports
    from .components.base_table import BaseTable

    return BaseTable(
        title="Customers",
        columns=CUSTOMER_COLUMNS,
        items=page_items,
        row_actions=CUSTOMER_ROW_ACTIONS,
        pagination=True,
        page_size=10,
        searchable=True,
        search_field=None,  # Search all fields
        loading=loading.value,
        error=error.value,
        on_page_change=handle_page_change,
    )