"""Caching utilities for Streamlit application."""

import streamlit as st
import hashlib
from typing import Any, Callable, Optional
from datetime import datetime, timedelta
import json


@st.cache_data(ttl=300)
def cached_api_call(endpoint: str, params: Optional[dict] = None) -> Any:
    """
    Cache API calls with TTL.

    Args:
        endpoint: API endpoint path
        params: Optional query parameters

    Returns:
        API response data
    """
    # This is a placeholder - actual implementation would call the API
    # from services.api_client import get_api_client
    # client = get_api_client()
    # return client.get(endpoint, params)
    pass


@st.cache_data
def hash_data(data: Any) -> str:
    """
    Create hash of data for cache keys.

    Args:
        data: Data to hash

    Returns:
        MD5 hash string
    """
    json_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.md5(json_str.encode()).hexdigest()


@st.cache_resource
def get_cache_stats() -> dict:
    """
    Get cache statistics.

    Returns:
        Dictionary with cache statistics
    """
    return {
        "data_cache_items": len(st.cache_data.get_stats()),
        "resource_cache_items": len(st.cache_resource.get_stats()),
        "last_cleared": st.session_state.get("last_cache_clear", "Never"),
    }


def clear_data_cache():
    """Clear all data cache."""
    st.cache_data.clear()
    st.session_state.last_cache_clear = datetime.now().isoformat()
    st.success("Data cache cleared")


def clear_resource_cache():
    """Clear all resource cache."""
    st.cache_resource.clear()
    st.success("Resource cache cleared")


def cached_computation(func: Callable) -> Callable:
    """
    Decorator for caching expensive computations.

    Usage:
        @cached_computation
        def expensive_calculation(data):
            # ... computation ...
            return result
    """
    return st.cache_data(func)


@st.cache_data
def process_large_dataset(data_json: str, operation: str) -> Any:
    """
    Cache for processing large datasets.

    Args:
        data_json: JSON string of data
        operation: Operation to perform

    Returns:
        Processed result
    """
    import json
    data = json.loads(data_json)

    if operation == "aggregate":
        # Example aggregation
        return {"count": len(data), "processed_at": datetime.now().isoformat()}
    elif operation == "validate":
        # Example validation
        return {"valid": True, "errors": []}
    else:
        return {"result": "unknown operation"}


@st.cache_data
def filter_and_sort_data(
    data_json: str,
    filters: dict,
    sort_by: str,
    ascending: bool = True,
) -> str:
    """
    Cache for filtering and sorting operations.

    Args:
        data_json: JSON string of data
        filters: Filter criteria
        sort_by: Column to sort by
        ascending: Sort direction

    Returns:
        JSON string of filtered/sorted data
    """
    import pandas as pd
    import json

    data = json.loads(data_json)
    df = pd.DataFrame(data)

    # Apply filters
    for key, value in filters.items():
        if value and value != "All":
            df = df[df[key].astype(str) == str(value)]

    # Sort
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=ascending)

    return df.to_json(orient="records")


@st.cache_data
def compute_metrics(data_json: str, metric_types: list) -> dict:
    """
    Cache for computing metrics from data.

    Args:
        data_json: JSON string of data
        metric_types: List of metric types to compute

    Returns:
        Dictionary of computed metrics
    """
    import pandas as pd
    import json

    data = json.loads(data_json)
    df = pd.DataFrame(data)

    metrics = {}

    if "count" in metric_types:
        metrics["count"] = len(df)

    if "sum" in metric_types:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        metrics["sum"] = {col: df[col].sum() for col in numeric_cols}

    if "avg" in metric_types:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        metrics["avg"] = {col: df[col].mean() for col in numeric_cols}

    if "min_max" in metric_types:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        metrics["min_max"] = {
            col: {"min": df[col].min(), "max": df[col].max()}
            for col in numeric_cols
        }

    return metrics


@st.cache_data
def generate_chart_data(
    data_json: str,
    chart_type: str,
    x_column: str,
    y_column: str,
) -> dict:
    """
    Cache for preparing chart data.

    Args:
        data_json: JSON string of data
        chart_type: Type of chart (line, bar, pie, etc.)
        x_column: Column for x-axis
        y_column: Column for y-axis

    Returns:
        Dictionary with chart configuration and data
    """
    import json

    data = json.loads(data_json)

    return {
        "chart_type": chart_type,
        "x_column": x_column,
        "y_column": y_column,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }


def memoize_cache_info() -> dict:
    """
    Get information about memoized caches.

    Returns:
        Dictionary with cache information
    """
    return {
        "data_cache": {
            "type": "st.cache_data",
            "description": "Caches data and pure functions",
            "ttl_support": True,
        },
        "resource_cache": {
            "type": "st.cache_resource",
            "description": "Caches resources like DB connections",
            "ttl_support": False,
        },
    }