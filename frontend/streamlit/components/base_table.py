"""Base table component for Streamlit application."""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional, Callable


def render_table(
    data: List[Dict[str, Any]],
    columns: Optional[List[str]] = None,
    column_config: Optional[Dict] = None,
    hide_index: bool = True,
    use_container_width: bool = True,
    on_row_click: Optional[Callable] = None,
    key: Optional[str] = None,
) -> None:
    """
    Render a data table with customizable options.

    Args:
        data: List of dictionaries containing the data
        columns: Optional list of columns to display
        column_config: Optional column configuration
        hide_index: Whether to hide the index column
        use_container_width: Whether to use full container width
        on_row_click: Optional callback for row click events
        key: Optional streamlit key for the component
    """
    if not data:
        st.info("No data available")
        return

    df = pd.DataFrame(data)

    if columns:
        df = df[columns]

    st.dataframe(
        df,
        column_config=column_config,
        hide_index=hide_index,
        use_container_width=use_container_width,
        key=key,
        on_select=on_row_click if on_row_click else None,
    )


def render_searchable_table(
    data: List[Dict[str, Any]],
    search_placeholder: str = "Search...",
    search_columns: Optional[List[str]] = None,
    **kwargs,
) -> None:
    """
    Render a table with search functionality.

    Args:
        data: List of dictionaries containing the data
        search_placeholder: Placeholder text for search input
        search_columns: Columns to search in (None = all columns)
        **kwargs: Additional arguments passed to render_table
    """
    # Search input
    col_search, col_space = st.columns([3, 1])
    with col_search:
        search_query = st.text_input(
            "🔍 Search",
            placeholder=search_placeholder,
            label_visibility="collapsed",
            key=f"search_{kwargs.get('key', 'table')}",
        )

    # Filter data
    filtered_data = data

    if search_query:
        filtered_data = []
        for row in data:
            for col in search_columns or row.keys():
                if col in row and search_query.lower() in str(row.get(col, "")).lower():
                    filtered_data.append(row)
                    break

    if not filtered_data:
        st.warning("No results found")
        return

    render_table(filtered_data, **kwargs)


def render_paginated_table(
    data: List[Dict[str, Any]],
    page_size: int = 10,
    **kwargs,
) -> None:
    """
    Render a table with pagination.

    Args:
        data: List of dictionaries containing the data
        page_size: Number of rows per page
        **kwargs: Additional arguments passed to render_table
    """
    total_items = len(data)
    total_pages = (total_items + page_size - 1) // page_size

    if total_pages <= 1:
        render_table(data, **kwargs)
        return

    # Pagination controls
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        page = st.slider(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            key=f"page_{kwargs.get('key', 'table')}",
        )

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_data = data[start_idx:end_idx]

    render_table(page_data, **kwargs)

    # Pagination info
    with col_left:
        st.caption(f"Showing {start_idx + 1}-{min(end_idx, total_items)} of {total_items}")

    with col_right:
        st.caption(f"Page {page} of {total_pages}")