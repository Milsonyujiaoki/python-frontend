"""Metric card component with entry animation for Streamlit.

Shows a metric value with an animated fade/slide-in effect using CSS.
"""

import streamlit as st

def metric_card(*, title: str, value: str, icon: str = "🔢", duration: int = 300):
    """Render a metric card.

    Args:
        title: Card title.
        value: Metric value.
        icon: Emoji or icon string.
        duration: Animation duration in ms.
    """
    html = f"""
    <div style='opacity:0; transform: translateY(20px); animation: fadeIn {duration}ms forwards;'>
        <h4>{icon} {title}</h4>
        <p style='font-size: 24px; margin:0;'>{value}</p>
    </div>
    <style>
    @keyframes fadeIn {{
        to {{ opacity:1; transform: translateY(0); }}
    }}
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

__all__ = ["metric_card"]
