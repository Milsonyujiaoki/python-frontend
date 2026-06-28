"""Session state management for Streamlit application."""

import streamlit as st
from typing import Any, Dict, List, Optional


def initialize_session_state() -> None:
    """Initialize all session state variables."""

    # Authentication state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    # Data cache state
    if "customers_cache" not in st.session_state:
        st.session_state.customers_cache = []
    if "barbers_cache" not in st.session_state:
        st.session_state.barbers_cache = []
    if "services_cache" not in st.session_state:
        st.session_state.services_cache = []

    # Filter state
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "filter_active" not in st.session_state:
        st.session_state.filter_active = None

    # Pagination state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
    if "page_size" not in st.session_state:
        st.session_state.page_size = 10


def set_authenticated(value: bool) -> None:
    """Set authentication state."""
    st.session_state.authenticated = value


def set_user(user: Dict[str, Any]) -> None:
    """Set current user."""
    st.session_state.user = user


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.authenticated


def logout() -> None:
    """Clear user session."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_email = None


# Data cache management
def set_customers(customers: List[Dict]) -> None:
    """Cache customers data."""
    st.session_state.customers_cache = customers


def get_customers() -> List[Dict]:
    """Get cached customers data."""
    return st.session_state.customers_cache


def set_barbers(barbers: List[Dict]) -> None:
    """Cache barbers data."""
    st.session_state.barbers_cache = barbers


def get_barbers() -> List[Dict]:
    """Get cached barbers data."""
    return st.session_state.barbers_cache


def set_services(services: List[Dict]) -> None:
    """Cache services data."""
    st.session_state.services_cache = services


def get_services() -> List[Dict]:
    """Get cached services data."""
    return st.session_state.services_cache


def clear_cache() -> None:
    """Clear all cached data."""
    st.session_state.customers_cache = []
    st.session_state.barbers_cache = []
    st.session_state.services_cache = []