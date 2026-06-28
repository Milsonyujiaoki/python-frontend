"""Glassmorphism component for Streamlit.

Applies a blurred, translucent backdrop to a container.
"""

import streamlit as st

def glass_container(*, content, blur: int = 8, bg_color: str = "rgba(255,255,255,0.2)"):
    """Render content inside a glassmorphic box.

    Args:
        content: Callable that writes Streamlit elements.
        blur: Blur radius in px.
        bg_color: Background color with alpha.
    """
    html = f"""
    <div style='backdrop-filter: blur({blur}px); background:{bg_color};
                border-radius: 12px; padding: 16px; box-shadow: 0 4px 30px rgba(0,0,0,0.1);'>
    </div>
    """
    # Use a placeholder to inject the container, then call content.
    placeholder = st.empty()
    placeholder.markdown(html, unsafe_allow_html=True)
    # Render inner content after the container – Streamlit renders sequentially.
    content()

__all__ = ["glass_container"]
