"""Ripple effect component for Flet buttons.

Injects a CSS ripple animation using a temporary overlay div.
"""

import flet as ft

def RippleEffect(content: ft.Control) -> ft.Control:
    """Wrap a Flet control with a ripple effect on click.

    Args:
        content: The child control (typically a Button).
    """
    # Use MouseRegion to capture clicks and overlay a ripple.
    ripple_overlay = ft.Container(
        width=0,
        height=0,
        bg_color="rgba(0,0,0,0.2)",
        border_radius=9999,
        opacity=0,
        animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT),
    )

    def on_click(e):
        # Position ripple at click location (simplified center).
        ripple_overlay.width = 100
        ripple_overlay.height = 100
        ripple_overlay.opacity = 0.5
        ripple_overlay.update()
        # Fade out after short delay.
        ripple_overlay.opacity = 0
        ripple_overlay.update()
        if hasattr(content, "on_click") and content.on_click:
            content.on_click(e)

    # Wrap with a Stack to overlay ripple on top of the content.
    return ft.Stack([
        content,
        ripple_overlay,
    ], on_click=on_click)

__all__ = ["RippleEffect"]
