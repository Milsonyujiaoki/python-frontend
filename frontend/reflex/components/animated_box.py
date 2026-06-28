"""AnimatedBox: a Reflex component with GPU‑accelerated CSS animation.

The component renders a ``div`` with a configurable animation defined via CSS
custom properties generated from ``frontend.shared.design.motion``. Users can
choose duration and easing tokens defined there.
"""

import reflex as rx
from ..shared.design.motion import generate_css_variables, DURATION_TOKENS, EASING_TOKENS

# Ensure the CSS variables are injected once per page.
def _inject_motion_css() -> None:
    css = generate_css_variables()
    # Reflex injects a style tag via ``rx.style`` helper.
    rx.style(css)

_rx.use_effect(_inject_motion_css, [])

def animated_box(*, width: str = "100px", height: str = "100px", bg: str = "#4a90e2", duration: str = "normal", easing: str = "ease-in-out") -> rx.Component:
    """Return a ``div`` that animates opacity on mount.

    Args:
        width: CSS width.
        height: CSS height.
        bg: Background colour.
        duration: Token name from ``DURATION_TOKENS``.
        easing: Token name from ``EASING_TOKENS``.
    """
    dur_ms = DURATION_TOKENS.get(duration, 300)
    ease_val = EASING_TOKENS.get(easing, "cubic-bezier(0.42, 0, 0.58, 1)")
    animation_css = (
        f"animation: fadeIn {dur_ms}ms {ease_val} forwards;"
    )
    return rx.box(
        id="animated-box",
        width=width,
        height=height,
        bg=bg,
        style=animation_css,
    )

# Global CSS for the fade‑in animation – injected once.
rx.style(
    """
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    """
)

__all__ = ["animated_box"]
