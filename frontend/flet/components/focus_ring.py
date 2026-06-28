"""Focus ring component for Flet.

Adds a visible focus outline with brand colors when a control receives keyboard focus.
"""

import flet as ft

def FocusRing(content: ft.Control, *, color: str = "#ff7e5f", width: int = 2) -> ft.Control:
    """Wrap a control with a focus ring.

    Args:
        content: Child control.
        color: Ring colour.
        width: Ring thickness in pixels.
    """
    # Use a Container with a border that becomes visible on focus.
    wrapper = ft.Container(
        content=content,
        border=ft.Border.all(width=0, color="transparent"),
        on_focus=lambda e: wrapper.update(border=ft.Border.all(width=width, color=color)),
        on_blur=lambda e: wrapper.update(border=ft.Border.all(width=0, color="transparent")),
    )
    return wrapper

__all__ = ["FocusRing"]
