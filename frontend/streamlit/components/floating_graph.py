"""Floating graph component with shadow and depth for Streamlit.

Uses Altair to generate a simple chart and applies CSS to give a floating
appearance.
"""

import streamlit as st
import altair as alt
import pandas as pd

def floating_graph(*, data=None, chart_type: str = "line"):
    """Render a chart with a floating style.

    Args:
        data: Optional pandas DataFrame. If ``None`` a demo dataset is used.
        chart_type: ``line`` or ``bar``.
    """
    if data is None:
        data = pd.DataFrame({
            "x": range(10),
            "y": [i ** 0.5 for i in range(10)],
        })
    if chart_type == "bar":
        chart = alt.Chart(data).mark_bar().encode(x="x", y="y")
    else:
        chart = alt.Chart(data).mark_line(point=True).encode(x="x", y="y")
    # Apply CSS for floating effect.
    html = """
    <style>
    .floating-chart {\n        box-shadow: 0 8px 20px rgba(0,0,0,0.15);\n        border-radius: 8px;\n        padding: 8px;\n        background: white;\n    }\n    </style>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True, theme="streamlit")

__all__ = ["floating_graph"]
