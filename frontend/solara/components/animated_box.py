"""AnimatedBox component for Solara.

This component provides GPU-accelerated CSS animations using the design system
motion tokens. It supports entrance animations, hover effects, and custom
transformations.

Usage::

    from frontend.shared.design.motion import DURATION_TOKENS
    from frontend.solara.components.animated_box import AnimatedBox

    AnimatedBox(
        children="Hello",
        animation="fade-in",
        duration="normal",
        delay=0.2,
    )
"""

import solara
from typing import Optional, Literal
import uuid

# Import motion tokens from shared design system
from frontend.shared.design.motion import DURATION_TOKENS, EASING_TOKENS


@solara.component
def AnimatedBox(
    children: solapa.Element = None,
    *,
    animation: Literal[
        "fade-in", "slide-up", "slide-down", "slide-left", "slide-right",
        "scale-in", "rotate-in", "bounce-in", "elastic-in"
    ] = "fade-in",
    duration: Literal["fast", "normal", "slow", "cinematic"] = "normal",
    delay: float = 0.0,
    easing: str = "ease-out",
    trigger: Optional[str] = None,
    once: bool = True,
    hover_scale: Optional[float] = None,
    hover_rotate: Optional[float] = None,
    class_name: Optional[str] = None,
    style: Optional[dict] = None,
    id: Optional[str] = None,
):
    """GPU-accelerated animated box component.

    Args:
        children: Content to animate.
        animation: Type of entrance animation.
        duration: Animation duration token (fast/normal/slow/cinematic).
        delay: Delay before animation starts (in seconds).
        easing: Easing function from EASING_TOKENS.
        trigger: Optional CSS class to trigger animation (for scroll-triggered).
        once: If True, animation only runs once.
        hover_scale: Scale factor on hover (e.g., 1.05 for 5% growth).
        hover_rotate: Rotation degrees on hover.
        class_name: Additional CSS classes.
        style: Additional inline styles.
        id: Element ID.
    """

    # Get duration in ms from token
    duration_ms = DURATION_TOKENS.get(duration, 300)
    easing_css = EASING_TOKENS.get(easing, "ease-out")

    # Generate unique ID for this instance
    instance_id = id or f"animated-box-{uuid.uuid4().hex[:8]}"

    # Base animation keyframes
    keyframes = {
        "fade-in": {"0%": {"opacity": "0"}, "100%": {"opacity": "1"}},
        "slide-up": {"0%": {"opacity": "0", "transform": "translateY(20px)"}, "100%": {"opacity": "1", "transform": "translateY(0)"}},
        "slide-down": {"0%": {"opacity": "0", "transform": "translateY(-20px)"}, "100%": {"opacity": "1", "transform": "translateY(0)"}},
        "slide-left": {"0%": {"opacity": "0", "transform": "translateX(20px)"}, "100%": {"opacity": "1", "transform": "translateX(0)"}},
        "slide-right": {"0%": {"opacity": "0", "transform": "translateX(-20px)"}, "100%": {"opacity": "1", "transform": "translateX(0)"}},
        "scale-in": {"0%": {"opacity": "0", "transform": "scale(0.8)"}, "100%": {"opacity": "1", "transform": "scale(1)"}},
        "rotate-in": {"0%": {"opacity": "0", "transform": "rotate(-10deg) scale(0.9)"}, "100%": {"opacity": "1", "transform": "rotate(0) scale(1)"}},
        "bounce-in": {"0%": {"opacity": "0", "transform": "scale(0.3)"}, "50%": {"transform": "scale(1.05)"}, "70%": {"transform": "scale(0.98)"}, "100%": {"opacity": "1", "transform": "scale(1)"}},
        "elastic-in": {"0%": {"opacity": "0", "transform": "translateX(-100%) scale(0.5)"}, "100%": {"opacity": "1", "transform": "translateX(0) scale(1)"}},
    }

    # Build dynamic @keyframes rule
    aura_name = f"anim-{animation}-{duration}-{easing}"
    kf = keyframes.get(animation, keyframes["fade-in"])

    keyframes_css = f"@keyframes {aura_name} {{\n"
    for stop, styles in kf.items():
        transforms = " ".join(f"{k}({v})" if k in ("translateX", "translateY", "scale", "rotate") else f"{k}:{v}" for k, v in styles.items())
        if any(k.startswith("translate") or k == "scale" for k in styles.keys()):
            transforms = " ".join(f"{k}({v})" for k, v in styles.items() if k in ("translateX", "translateY", "scale", "rotate"))
            non_transform = " ".join(f"{k}:{v}" for k, v in styles.items() if k not in ("translateX", "translateY", "scale", "rotate", "opacity"))
            transform_str = f"transform: {transforms};" if transforms else ""
            opacity_str = f"opacity: {styles.get('opacity', 1)};" if "opacity" in styles else ""
            keyframes_css += f"    {stop} {{ {transform_str} {opacity_str}{non_transform} }}\n"
        else:
            props = "; ".join(f"{k}: {v}" for k, v in styles.items())
            keyframes_css += f"    {stop} {{ {props} }}\n"
    keyframes_css += "}"

    # Hover effects
    hover_css = ""
    if hover_scale:
        hover_css += f"transform: scale({hover_scale})"
        if hover_rotate:
            hover_css += f" rotate({hover_rotate}deg)"
        hover_css += ";"

    # Build inline style
    base_style = {
        "animationName": f"({keyframes_css})",
        "animationDuration": f"{duration_ms}ms",
        "animationDelay": f"{delay}s",
        "animationTimingFunction": easing_css,
        "animationFillMode": "both",
        "transform": "translateZ(0)",  # GPU layer
        "willChange": "transform, opacity",
    }

    if hover_css:
        base_style["onMouseEnter"] = lambda e: setattr(e.target, "style", e.target.style + hover_css) if hasattr(e.target, "style") else None

    # Merge with user style
    merged_style = {**base_style, **(style or {})}

    merged_class = f"animated-box {class_name}" if class_name else "animated-box"

    return solara.Box(
        children=children,
        class_name=merged_class.strip(),
        style=merged_style,
        id=instance_id,
    )


# Global CSS to be injected once at app level
ANIMATED_BOX_GLOBAL_CSS = """
/* AnimatedBox GPU-accelerated styles */
.animated-box {
    transform: translateZ(0);
    will-change: transform, opacity;
    backface-visibility: hidden;
}

/* Reduced motion fallback */
@media (prefers-reduced-motion: reduce) {
    .animated-box {
        animation: none !important;
        transition: none !important;
        transform: none !important;
    }
}
"""

__all__ = ["AnimatedBox", "ANIMATED_BOX_GLOBAL_CSS"]