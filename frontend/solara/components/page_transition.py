"""Page transition components for Solara.

This module provides animated page transitions (fade, slide, zoom) that wrap
Solara page content. Transitions use the design system motion tokens for
consistent timing.

Usage::

    from frontend.solara.components.page_transition import FadeTransition, SlideTransition

    def dashboard():
        return FadeTransition(
            children=DashboardContent(),
            direction="in",
            duration="normal",
        )
"""

import solara
from typing import Optional, Literal
import uuid
from frontend.shared.design.motion import DURATION_TOKENS, EASING_TOKENS


@solara.component
def PageTransition(
    children: solara.Element = None,
    *,
    transition: Literal["fade", "slide-left", "slide-right", "slide-up", "slide-down", "zoom-in"] = "fade",
    direction: Literal["in", "out"] = "in",
    duration: Literal["fast", "normal", "slow"] = "normal",
    easing: str = "ease-out",
    delay: float = 0.0,
    key: Optional[str] = None,
):
    """Animated page transition wrapper.

    Args:
        children: Page content to wrap.
        transition: Type of transition animation.
        direction: "in" for page entering, "out" for page leaving.
        duration: Animation duration token.
        easing: Easing function from EASING_TOKENS.
        delay: Delay before animation starts (seconds).
        key: Optional key to force rerender.
    """
    unique_id = f"page-transition-{uuid.uuid4().hex[:8]}"
    duration_ms = DURATION_TOKENS.get(duration, 300)
    easing_css = EASING_TOKENS.get(easing, "ease-out")

    # Build animation based on type and direction
    from_state = {
        ("fade", "in"): {"opacity": "0"},
        ("fade", "out"): {"opacity": "1"},
        ("slide-left", "in"): {"opacity": "0", "transform": "translateX(30px)"},
        ("slide-left", "out"): {"opacity": "1", "transform": "translateX(-30px)"},
        ("slide-right", "in"): {"opacity": "0", "transform": "translateX(-30px)"},
        ("slide-right", "out"): {"opacity": "1", "transform": "translateX(30px)"},
        ("slide-up", "in"): {"opacity": "0", "transform": "translateY(20px)"},
        ("slide-up", "out"): {"opacity": "1", "transform": "translateY(-20px)"},
        ("slide-down", "in"): {"opacity": "0", "transform": "translateY(-20px)"},
        ("slide-down", "out"): {"opacity": "1", "transform": "translateY(20px)"},
        ("zoom-in", "in"): {"opacity": "0", "transform": "scale(0.95)"},
        ("zoom-in", "out"): {"opacity": "1", "transform": "scale(1.05)"},
    }

    to_state = {
        ("fade", "in"): {"opacity": "1"},
        ("fade", "out"): {"opacity": "0"},
        ("slide-left", "in"): {"opacity": "1", "transform": "translateX(0)"},
        ("slide-left", "out"): {"opacity": "0", "transform": "translateX(-100%)"},
        ("slide-right", "in"): {"opacity": "1", "transform": "translateX(0)"},
        ("slide-right", "out"): {"opacity": "0", "transform": "translateX(100%)"},
        ("slide-up", "in"): {"opacity": "1", "transform": "translateX(0)"},
        ("slide-up", "out"): {"opacity": "0", "transform": "translateY(-100%)"},
        ("slide-down", "in"): {"opacity": "1", "transform": "translateX(0)"},
        ("slide-down", "out"): {"opacity": "0", "transform": "translateY(100%)"},
        ("zoom-in", "in"): {"opacity": "1", "transform": "scale(1)"},
        ("zoom-in", "out"): {"opacity": "0", "transform": "scale(1.1)"},
    }

    anim_name = f"page-{transition}-{direction}-{unique_id}"
    key = key or unique_id

    from_props = from_state.get((transition, direction), {"opacity": "0"})
    to_props = to_state.get((transition, direction), {"opacity": "1"})

    # Generate keyframes CSS
    from_css = "; ".join(f"{k}: {v}" for k, v in from_props.items())
    to_css = "; ".join(f"{k}: {v}" for k, v in to_props.items())

    keyframes_css = f"""
@keyframes {anim_name} {{
    0% {{ {from_css} }}
    100% {{ {to_css} }}
}}
"""

    # Style for wrapper
    wrapper_style = {
        "animationName": f"({keyframes_css})",
        "animationDuration": f"{duration_ms}ms",
        "animationDelay": f"{delay}s",
        "animationTimingFunction": easing_css,
        "animationFillMode": "forwards",
        "position": "relative",
        "width": "100%",
        "height": "100%",
    }

    return solara.html.Tag(
        "div",
        children=[children],
        key=key,
        id=unique_id,
        style=wrapper_style,
    )


# Convenience components for common transitions
@solara.component
def FadeTransition(
    children: solara.Element = None,
    *,
    direction: Literal["in", "out"] = "in",
    duration: Literal["fast", "normal", "slow"] = "normal",
    delay: float = 0.0,
):
    """Simple fade transition wrapper."""
    return PageTransition(
        children=children,
        transition="fade",
        direction=direction,
        duration=duration,
        delay=delay,
    )


@solara.component
def SlideTransition(
    children: solara.Element = None,
    *,
    direction: Literal["left", "right", "up", "down"] = "left",
    in_out: Literal["in", "out"] = "in",
    duration: Literal["fast", "normal", "slow"] = "normal",
    delay: float = 0.0,
):
    """Slide transition wrapper with direction."""
    transition_map = {
        "left": "slide-left",
        "right": "slide-right",
        "up": "slide-up",
        "down": "slide-down",
    }
    return PageTransition(
        children=children,
        transition=transition_map.get(direction, "slide-left"),
        direction=in_out,
        duration=duration,
        delay=delay,
    )


@solara.component
def ZoomTransition(
    children: solara.Element = None,
    *,
    direction: Literal["in", "out"] = "in",
    duration: Literal["fast", "normal", "slow"] = "normal",
    delay: float = 0.0,
):
    """Zoom-in transition wrapper."""
    return PageTransition(
        children=children,
        transition="zoom-in",
        direction=direction,
        duration=duration,
        delay=delay,
    )


# Global CSS for page transitions
PAGE_TRANSITION_CSS = """
/* Page transition anchor point */
.page-transition {
    position: relative;
    width: 100%;
    height: 100%;
    transform: translateZ(0);
    will-change: transform, opacity;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .page-transition * {
        animation: none !important;
        transition: none !important;
        transform: none !important;
    }
}
"""

__all__ = ["PageTransition", "FadeTransition", "SlideTransition", "ZoomTransition", "PAGE_TRANSITION_CSS"]