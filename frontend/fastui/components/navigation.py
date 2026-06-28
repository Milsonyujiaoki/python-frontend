"""
Navigation components for FastUI frontend.

Provides consistent navigation structure across all pages.
"""

from fastui import components as c
from typing import List, Optional


def get_main_nav() -> List[c.Link]:
    """Get main navigation menu items."""
    return [
        c.Link(label="Dashboard", on_click="/", active="/"),
        c.Link(label="Customers", on_click="/customers", active="/customers"),
        c.Link(label="Barbers", on_click="/barbers", active="/barbers"),
        c.Link(label="Services", on_click="/services", active="/services"),
        c.Link(label="Appointments", on_click="/appointments", active="/appointments"),
    ]


def get_auth_nav() -> List[c.Link]:
    """Get navigation items for authentication pages."""
    return [
        c.Link(label="Login", on_click="/login", active="/login"),
        c.Link(label="Register", on_click="/register", active="/register"),
    ]


def create_page_header(title: str, subtitle: Optional[str] = None) -> c.PageHeader:
    """Create a standard page header."""
    return c.PageHeader(
        title=title,
        subtitle=subtitle,
    )


def create_navbar(links: Optional[List[c.Link]] = None) -> c.Navbar:
    """Create a standard navigation bar."""
    if links is None:
        links = get_main_nav()
    return c.Navbar(links=links, brand_text="BarberShop SaaS")


def create_footer() -> c.Footer:
    """Create a standard footer."""
    return c.Footer(
        links=[
            c.Link(label="Privacy", on_click="/privacy"),
            c.Link(label="Terms", on_click="/terms"),
            c.Link(label="Contact", on_click="/contact"),
        ],
        extra_text="© 2024 BarberShop SaaS. All rights reserved.",
    )