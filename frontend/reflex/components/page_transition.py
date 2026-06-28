"""Page transition component for Reflex.

Provides a wrapper that fades children in/out when the ``show`` prop toggles.
This mimics a simple page navigation animation.
"""

import reflex as rx

def page_transition(*, show: bool = True, duration: str = "normal", easing: str = "ease-in-out", children: list[rx.Component] | None = None) -> rx.Component:
    """Wrap ``children`` with a fade transition.

    Args:
        show: Whether the content is visible.
        duration: Token name from ``frontend.shared.design.motion``.
        easing: Token name from ``frontend.shared.design.motion``.
        children: List of Reflex components to render.
    """
    from ..shared.design.motion import DURATION_TOKENS, EASING_TOKENS

    dur_ms = DURATION_TOKENS.get(duration, 300)
    ease_val = EASING_TOKENS.get(easing, "cubic-bezier(0.42, 0, 0.58, 1)")
    style = (
        f"transition: opacity {dur_ms}ms {ease_val};"
        f"opacity: {'1' if show else '0'};"
    )
    return rx.box(* (children or []), style=style)

__all__ = ["page_transition"]
