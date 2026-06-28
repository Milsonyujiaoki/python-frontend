"""Components package for Streamlit frontend."""

from .sidebar import render_sidebar
from .dashboard import render_dashboard
from .base_table import render_table, render_searchable_table, render_paginated_table
from .base_form import render_form, render_customer_form, render_barber_form, render_service_form
from .visualization import (
    render_metric_cards,
    render_line_chart,
    render_bar_chart,
    render_pie_chart,
    render_scatter_plot,
    render_histogram,
    render_area_chart,
    render_gauge_chart,
    render_revenue_dashboard,
    render_service_analytics,
)

__all__ = [
    "render_sidebar",
    "render_dashboard",
    "render_table",
    "render_searchable_table",
    "render_paginated_table",
    "render_form",
    "render_customer_form",
    "render_barber_form",
    "render_service_form",
    "render_metric_cards",
    "render_line_chart",
    "render_bar_chart",
    "render_pie_chart",
    "render_scatter_plot",
    "render_histogram",
    "render_area_chart",
    "render_gauge_chart",
    "render_revenue_dashboard",
    "render_service_analytics",
]