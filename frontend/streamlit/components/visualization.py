"""Visualization components for Streamlit application."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional


def render_metric_cards(
    metrics: List[Dict[str, Any]], columns: int = 4
) -> None:
    """
    Render a row of metric cards.

    Args:
        metrics: List of metric dictionaries with keys:
            - label: str
            - value: str or number
            - delta: str (optional)
            - delta_color: str - "normal", "inverse", "off" (optional)
        columns: Number of columns to use
    """
    cols = st.columns(columns)

    for i, metric in enumerate(metrics):
        with cols[i % columns]:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", 0),
                delta=metric.get("delta"),
                delta_color=metric.get("delta_color", "normal"),
            )


def render_line_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None,
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render a line chart.

    Args:
        data: DataFrame with the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color: Optional column for color encoding
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.line(data, x=x, y=y, color=color, markers=True, title=title)
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None,
    orientation: str = "v",
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render a bar chart.

    Args:
        data: DataFrame with the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color: Optional column for color encoding
        orientation: "v" for vertical, "h" for horizontal
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.bar(
        data, x=x, y=y, color=color, orientation=orientation, title=title
    )
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_pie_chart(
    data: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    hole: float = 0.0,
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render a pie or donut chart.

    Args:
        data: DataFrame with the data
        names: Column name for category names
        values: Column name for values
        title: Chart title
        hole: 0.0 for pie, 0.3-0.5 for donut
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title,
        hole=hole,
    )
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_scatter_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None,
    size: Optional[str] = None,
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render a scatter plot.

    Args:
        data: DataFrame with the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color: Optional column for color encoding
        size: Optional column for size encoding
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title)
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_histogram(
    data: pd.DataFrame,
    x: str,
    title: str,
    color: Optional[str] = None,
    nbins: Optional[int] = None,
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render a histogram.

    Args:
        data: DataFrame with the data
        x: Column name for the histogram
        title: Chart title
        color: Optional column for color encoding
        nbins: Optional number of bins
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.histogram(data, x=x, color=color, nbins=nbins, title=title)
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_area_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    stack: bool = True,
    height: int = 400,
    use_container_width: bool = True,
) -> None:
    """
    Render an area chart.

    Args:
        data: DataFrame with the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        stack: Whether to stack multiple series
        height: Chart height in pixels
        use_container_width: Whether to use full container width
    """
    fig = px.area(data, x=x, y=y, title=title)
    fig.update_layout(template="plotly_white", height=height)
    st.plotly_chart(fig, use_container_width=use_container_width)


def render_gauge_chart(
    value: float,
    min_value: float = 0,
    max_value: float = 100,
    title: str = "Gauge",
    suffix: str = "",
) -> None:
    """
    Render a gauge chart.

    Args:
        value: Current value to display
        min_value: Minimum value on the gauge
        max_value: Maximum value on the gauge
        title: Gauge title
        suffix: Suffix to add to the value display
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"size": 24}},
            number={"suffix": suffix},
            gauge={
                "axis": {"range": [min_value, max_value]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [min_value, max_value * 0.33], "color": "#ffcccc"},
                    {
                        "range": [max_value * 0.33, max_value * 0.66],
                        "color": "#ffffcc",
                    },
                    {"range": [max_value * 0.66, max_value], "color": "#ccffcc"},
                ],
            },
        )
    )

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_revenue_dashboard() -> None:
    """Render a revenue analytics dashboard."""
    st.subheader("💰 Revenue Analytics")

    # Sample revenue data
    revenue_data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Revenue": [12000, 15000, 18000, 22000, 25000, 28000],
            "Expenses": [8000, 9000, 10000, 11000, 12000, 13000],
            "Profit": [4000, 6000, 8000, 11000, 13000, 15000],
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        render_line_chart(
            revenue_data,
            x="Month",
            y="Revenue",
            title="Monthly Revenue Trend",
            height=350,
        )

    with col2:
        render_bar_chart(
            revenue_data,
            x="Month",
            y="Profit",
            title="Monthly Profit",
            height=350,
        )

    # Profit margin gauge
    current_margin = (
        revenue_data["Profit"].iloc[-1] / revenue_data["Revenue"].iloc[-1] * 100
    )
    render_gauge_chart(
        current_margin,
        min_value=0,
        max_value=100,
        title="Profit Margin",
        suffix="%",
    )


def render_service_analytics() -> None:
    """Render service performance analytics."""
    st.subheader("💇 Service Analytics")

    # Sample service data
    service_data = pd.DataFrame(
        {
            "Service": [
                "Haircut",
                "Beard Trim",
                "Coloring",
                "Styling",
                "Treatment",
                "Fade",
            ],
            "Count": [45, 25, 15, 10, 5, 20],
            "Revenue": [1575, 500, 1200, 400, 250, 800],
            "Avg Rating": [4.8, 4.7, 4.9, 4.6, 4.8, 4.9],
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        render_pie_chart(
            service_data,
            names="Service",
            values="Count",
            title="Service Distribution",
            hole=0.4,
            height=350,
        )

    with col2:
        render_bar_chart(
            service_data,
            x="Service",
            y="Revenue",
            title="Revenue by Service",
            orientation="v",
            height=350,
        )

    # Performance table
    st.markdown("### Service Performance")
    st.dataframe(
        service_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Avg Rating": st.column_config.NumberColumn(
                "Avg Rating", format="%.1f⭐"
            ),
            "Revenue": st.column_config.NumberColumn("Revenue", format="$%.0f"),
        },
    )