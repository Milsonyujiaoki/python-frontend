"""Skeleton shimmer loading component for Streamlit.

Provides a simple rectangular placeholder with CSS animation indicating loading.
"""

import streamlit as st

def skeleton(*, width: str = "100%", height: str = "20px"):
    """Render a skeleton block.

    Args:
        width: CSS width.
        height: CSS height.
    """
    html = f"""
    <div style='width:{width}; height:{height}; background:#eee; border-radius:4px;\n        animation: shimmer 1.5s infinite;'></div>
    <style>
    @keyframes shimmer {{
        0% {{ background-position: -200px 0; }}
        100% {{ background-position: calc(200% + 200px) 0; }}
    }}
    div {{
        background: linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%);
        background-size: 200% 100%;
    }}
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

__all__ = ["skeleton"]
