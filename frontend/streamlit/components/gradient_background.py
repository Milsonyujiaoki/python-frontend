"""Streamlit component that renders a mesh gradient background.

The component injects a full‑width <div> with a CSS mesh‑gradient background.
It can be used at the top of a page layout.
"""

import streamlit as st

def gradient_background(*, colors=None, angle: int = 45):
    """Render a gradient background.

    Args:
        colors: List of color strings. If ``None`` a default palette is used.
        angle: Gradient angle in degrees.
    """
    if colors is None:
        colors = ["#ff7e5f", "#feb47b", "#86a8e7", "#91eae4"]
    # Build CSS mesh gradient (simplified linear gradient for demo).
    gradient = f"linear-gradient({angle}deg, {', '.join(colors)})"
    html = f"""
    <div style='position:fixed; top:0; left:0; width:100%; height:100%;
                pointer-events:none; background:{gradient}; z-index:-1;'></div>
    """
    st.markdown(html, unsafe_allow_html=True)

__all__ = ["gradient_background"]
