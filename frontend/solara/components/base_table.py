"""Base table component with pagination and performance optimizations."""

import solara
from typing import List, Dict, Any, Optional, Callable


def BaseTable(
    title: str,
    columns: List[Dict[str, Any]],
    items: List[Dict[str, Any]],
    row_actions: List[Dict[str, Any]] = None,
    pagination: bool = True,
    page_size: int = 10,
    searchable: bool = True,
    search_field: Optional[str] = None,
    loading: bool = False,
    error: Optional[str] = None,
    on_page_change: Optional[Callable[[int], None]] = None,
):
    """
    A generic table with pagination, search, and performance optimizations.

    Args:
        title: The title to display above the table
        columns: List of column definitions
        items: List of dictionaries representing the rows
        row_actions: List of action definitions for each row
        pagination: Enable pagination (default: True)
        page_size: Number of items per page (default: 10)
        searchable: Enable search functionality (default: True)
        search_field: Field to search on, or None to search all fields
        loading: Show loading state
        error: Display error message if provided
        on_page_change: Callback when page changes
    """
    # State for pagination
    page, set_page = solara.use_state(0)
    # State for search
    search_query, set_search_query = solara.use_state("")

    # Reset page when items change
    solara.use_effect(
        lambda: set_page(0),
        [len(items)]
    )

    # Filter items based on search query with memoization
    @solara.memoize
    def get_filtered_items():
        if not search_query.strip():
            return items

        query_lower = search_query.lower()

        if search_field:
            # Search specific field
            return [
                item for item in items
                if query_lower in str(item.get(search_field, "")).lower()
            ]
        else:
            # Search all fields
            filtered = []
            for item in items:
                for value in item.values():
                    if query_lower in str(value).lower():
                        filtered.append(item)
                        break
            return filtered

    filtered_items = get_filtered_items()

    # Calculate pagination
    total_items = len(filtered_items)
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    # Ensure current page is valid
    if page >= total_pages:
        set_page(total_pages - 1)

    # Get items for current page
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_items)
    page_items = filtered_items[start_idx:end_idx]

    # Notify parent of page change
    solara.use_effect(
        lambda: on_page_change(page) if on_page_change else None,
        [page]
    )

    # Build the table header
    header_cells = [solara.Th(col["label"]) for col in columns]
    if row_actions:
        header_cells.append(solara.Th("Actions"))

    # Build the table rows with optimized rendering
    rows = []
    for item in page_items:
        row_cells = []
        for col in columns:
            field_value = item.get(col["field"], "")
            # Apply formatting if specified
            if "format" in col and callable(col["format"]):
                formatted_value = col["format"](field_value)
            else:
                formatted_value = field_value
            cell_content = solara.Td(str(formatted_value))
            row_cells.append(cell_content)

        # Add action buttons if specified
        if row_actions:
            action_cells = []
            for action in row_actions:
                def make_callback(act, itm):
                    return lambda _: act["on_click"](itm)

                action_button = solara.Button(
                    label=action["label"],
                    on_click=make_callback(action, item),
                    color=action.get("color", "primary"),
                    text=action.get("text", False),
                    outline=action.get("outline", False),
                )
                action_cells.append(solara.Td(action_button))

            row_cells.append(solara.Td(solara.Column(action_cells)))

        rows.append(row_cells)

    # Build pagination controls
    def pagination_controls():
        """Render pagination controls."""
        if not pagination or total_pages <= 1:
            return None

        # Generate page buttons with ellipsis for large page counts
        page_buttons = []

        # Always show first page
        page_buttons.append(
            solara.Button(
                label="1",
                on_click=lambda _: set_page(0),
                text=True,
                color="primary" if page == 0 else None,
            )
        )

        # Show ellipsis if there are many pages before current
        if page > 2:
            page_buttons.append(solara.Label("..."))

        # Show pages around current page
        for p in range(max(1, page - 1), min(total_pages - 1, page + 2)):
            page_buttons.append(
                solara.Button(
                    label=str(p + 1),
                    on_click=lambda _, p=p: set_page(p),
                    text=True,
                    color="primary" if p == page else None,
                )
            )

        # Show ellipsis if there are many pages after current
        if page < total_pages - 3:
            page_buttons.append(solara.Label("..."))

        # Always show last page if more than 1 page
        if total_pages > 1:
            page_buttons.append(
                solara.Button(
                    label=str(total_pages),
                    on_click=lambda _: set_page(total_pages - 1),
                    text=True,
                    color="primary" if page == total_pages - 1 else None,
                )
            )

        # Navigation buttons
        prev_button = solara.Button(
            label="Previous",
            on_click=lambda _: set_page(max(0, page - 1)),
            disabled=page == 0,
            text=True,
        )

        next_button = solara.Button(
            label="Next",
            on_click=lambda _: set_page(min(total_pages - 1, page + 1)),
            disabled=page >= total_pages - 1,
            text=True,
        )

        # Page info label
        page_info = solara.Label(
            f"Page {page + 1} of {total_pages} ({total_items} items)"
        )

        return solara.Row(
            justify="space-between",
            align="center",
            style={"margin": "10px 0"},
            children=[
                solara.Row(children=[prev_button, next_button]),
                page_info,
                solara.Row(children=page_buttons),
            ]
        )

    # Build search input
    def search_input():
        """Render search input."""
        if not searchable:
            return None

        return solara.Row(
            justify="space-between",
            align="center",
            style={"margin": "10px 0"},
            children=[
                solara.InputText(
                    label="Search",
                    value=search_query,
                    on_value=set_search_query,
                    placeholder="Type to search...",
                    style={"width": "300px"},
                ),
                solara.Label(f"Showing {len(page_items)} of {total_items} items"),
            ]
        )

    # Build the content
    content_children = []

    # Add title
    content_children.append(solara.Markdown(f"### {title}"))

    # Add loading state
    if loading:
        content_children.append(solara.ProgressLinear())

    # Add error state
    if error:
        content_children.append(
            solara.ErrorBanner(error, on_close=lambda: None)
        )

    # Add search input
    if searchable:
        content_children.append(search_input())

    # Add table
    if page_items:
        table_children = [header_cells, *rows]
        content_children.append(solara.Table(table_children))
    else:
        # No data message
        no_data_msg = "No data found" if not filtered_items else "No results on this page"
        content_children.append(solara.Markdown(f"*{no_data_msg}*"))

    # Add pagination controls
    if pagination:
        content_children.append(pagination_controls())

    return solara.Column(content_children)