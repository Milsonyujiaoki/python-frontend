"""
Data table components for FastUI frontend.

Provides reusable table components with sorting, filtering, and pagination.
"""

from fastui import components as c
from fastui.components import display
from typing import List, Dict, Any, Optional, Callable


def create_table(
    title: str,
    columns: List[display.DisplayLookup],
    data: List[Dict[str, Any]],
    data_url: Optional[str] = None,
    actions: Optional[List[Dict[str, str]]] = None,
) -> c.Table:
    """
    Create a standard data table.

    Args:
        title: Table title
        columns: List of column definitions
        data: Table data (or use data_url for server-side)
        data_url: URL for server-side data fetching
        actions: Optional row actions (edit, delete, etc.)
    """
    return c.Table(
        columns=columns,
        data=data,
        data_url=data_url,
    )


def create_paginated_table(
    title: str,
    columns: List[display.DisplayLookup],
    data_url: str,
    page_size: int = 10,
) -> c.Table:
    """
    Create a table with server-side pagination.

    Args:
        title: Table title
        columns: Column definitions
        data_url: URL for paginated data
        page_size: Number of items per page
    """
    return c.Table(
        columns=columns,
        data_url=data_url,
        # FastUI handles pagination automatically when data_url is provided
    )


def create_searchable_table(
    title: str,
    columns: List[display.DisplayLookup],
    data_url: str,
    search_placeholder: str = "Search...",
) -> List[c.AnyComponent]:
    """
    Create a table with search functionality.

    Args:
        title: Table title
        columns: Column definitions
        data_url: URL for data with search support
        search_placeholder: Placeholder text for search input
    """
    return [
        c.Heading(text=title, level=2),
        c.Input(
            placeholder=search_placeholder,
            debounce=300,
            # Search would be handled by updating data_url with query params
        ),
        c.Table(columns=columns, data_url=data_url),
    ]


# Predefined column sets for common entities
CUSTOMER_COLUMNS = [
    display.DisplayLookup(field="id", header="ID", width=50),
    display.DisplayLookup(field="name", header="Name"),
    display.DisplayLookup(field="email", header="Email"),
    display.DisplayLookup(field="phone", header="Phone"),
    display.DisplayLookup(field="is_active", header="Active", width=80),
]

BARBER_COLUMNS = [
    display.DisplayLookup(field="id", header="ID", width=50),
    display.DisplayLookup(field="name", header="Name"),
    display.DisplayLookup(field="email", header="Email"),
    display.DisplayLookup(field="phone", header="Phone"),
    display.DisplayLookup(field="specialty", header="Specialty"),
]

SERVICE_COLUMNS = [
    display.DisplayLookup(field="id", header="ID", width=50),
    display.DisplayLookup(field="name", header="Name"),
    display.DisplayLookup(field="description", header="Description"),
    display.DisplayLookup(field="duration", header="Duration (min)", width=120),
    display.DisplayLookup(field="price", header="Price", width=100),
]