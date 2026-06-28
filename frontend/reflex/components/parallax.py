"""Parallax scrolling component for Reflex.

The component renders a container with a background image that moves at a
different speed than the foreground content based on scroll position.
This is a lightweight implementation using ``window.scrollY``.
"""

import reflex as rx

def parallax(*, image_url: str, speed: float = 0.5, height: str = "400px") -> rx.Component:
    """Render a parallax section.

    Args:
        image_url: URL of the background image.
        speed: Multiplier for scroll offset (0 = static, 1 = same speed).
        height: Height of the component.
    """
    # Reactive state for background offset.
    offset_state = rx.state(y_offset=0)

    # JS listener: update offset_state on scroll.
    js = (
        "window.addEventListener('scroll', function(){"
        f"  rx.setState('y_offset', window.scrollY * {speed});"
        "});"
    )
    rx.eval(js)

    # Compute background position.
    bg_position = rx.cond(
        True,  # always true – we use the state.
        f"center calc(50% + {{offset_state.y_offset}}px)",
        "center 50%",
    )
    return rx.box(
        width="100%",
        height=height,
        style=(
            f"background-image: url('{image_url}'); "
            f"background-attachment: fixed; "
            f"background-position: {bg_position}; "
            "background-size: cover;"
        ),
        overflow="hidden",
    )

__all__ = ["parallax"]
