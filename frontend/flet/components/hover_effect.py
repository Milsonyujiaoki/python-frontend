"""Hover effect component for Flet.

Provides a wrapper that applies a scale and elevation on mouse hover.
"""

import flet as ft

def HoverEffect(content: ft.Control, *, scale: float = 1.05, elevation: int = 4) -> ft.Control:
    """Wrap a Flet control with hover styling.

    Args:
        content: The child control.
        scale: Scale factor on hover.
        elevation: Elevation (shadow) on hover.
    """
    # Use MouseRegion to detect hover.
    return ft.MouseRegion(
        content=content,
        on_enter=lambda e: setattr(content, "scale", scale) or setattr(content, "elevation", elevation),
        on_exit=lambda e: setattr(content, "scale", 1.0) or setattr(content, "elevation", 0),
    )

__all__ = ["HoverEffect"]
