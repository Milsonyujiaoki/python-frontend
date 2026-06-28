"""Microinteractions library for Python frontends.

This module provides reusable microinteraction components that can be used
across Solara, Reflex, Streamlit, and Flet frontends. All interactions use
the design system motion tokens for consistency.

Usage::

    from frontend.shared.microinteractions import (
        Hoverable, Clickable, Tooltip, CheckmarkIcon,
        LoadingOverlay, ShakeOnError
    )

    Hoverable(
        children=MyButton(),
        scale=1.05,
        shadow=True,
    )
"""

import solara
from typing import Optional, Literal, Union
import uuid
from frontend.shared.design.motion import DURATION_TOKENS, EASING_TOKENS


# =============================================================================
# HOVER EFFECTS
# =============================================================================

@solara.component
def Hoverable(
    children: solara.Element = None,
    *,
    scale: float = 1.05,
    shadow: bool = True,
    shadow_color: str = "rgba(0,0,0,0.15)",
    rotate: Optional[float] = None,
    brightness: Optional[float] = None,
    duration: Literal["fast", "normal", "slow"] = "fast",
    class_name: Optional[str] = None,
):
    """Wraps content with hover-driven scale + shadow effects.

    Args:
        children: Content to wrap.
        scale: Scale factor on hover (1.05 = 5% larger).
        shadow: Enable box-shadow on hover.
        shadow_color: Shadow color.
        rotate: Rotation degrees on hover.
        brightness: Brightness filter on hover (0-200).
        duration: Animation duration.
        class_name: Additional CSS classes.
    """
    duration_ms = DURATION_TOKENS.get(duration, 150)
    unique_id = f"hoverable-{uuid.uuid4().hex[:8]}"

    # Build hover CSS
    hover_transforms = [f"scale({scale})"]
    if rotate:
        hover_transforms.append(f"rotate({rotate}deg)")
    hover_transform = " ".join(hover_transforms)

    shadow_css = ""
    if shadow:
        shadow_css = f"box-shadow: 0 8px 25px {shadow_color};"

    brightness_css = ""
    if brightness:
        brightness_css = f"filter: brightness({brightness}%);"

    hover_css = f"""
#{unique_id}:hover {{
    transform: {hover_transform};
    {shadow_css}
    {brightness_css}
}}
"""

    css_style = f"""
<style>
#{unique_id} {{
    display: inline-block;
    transition: transform {duration_ms}ms ease, box-shadow {duration_ms}ms ease, filter {duration_ms}ms ease;
    transform-origin: center;
    will-change: transform, box-shadow;
}}
{hover_css}
</style>
"""

    merged_class = f"hoverable {class_name}" if class_name else "hoverable"

    return solara.html.Tag(
        "div",
        children=[css_style, children],
        id=unique_id,
        class_name=merged_class,
    )


# =============================================================================
# CLICKABLE / ACTIVE STATES
# =============================================================================

@solara.component
def Clickable(
    children: solara.Element = None,
    *,
    on_click: Optional[callable] = None,
    scale_down: float = 0.95,
    feedback: bool = True,
    duration: Literal["fast", "normal"] = "fast",
):
    """Wraps content with active-state feedback (scale down on click).

    Args:
        children: Content to wrap.
        on_click: Callback function.
        scale_down: Scale factor on mousedown (0.95 = 5% smaller).
        feedback: Enable visual feedback.
        duration: Animation duration.
    """
    duration_ms = DURATION_TOKENS.get(duration, 150)
    unique_id = f"clickable-{uuid.uuid4().hex[:8]}"

    # Active state tracking
    active, set_active = solara.use_state(False)

    # Build CSS
    css_style = f"""
<style>
#{unique_id} {{
    display: inline-block;
    transition: transform {duration_ms}ms ease;
    transform-origin: center;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}}
#{unique_id}.active {{
    transform: scale({scale_down});
}}
</style>
"""

    def handle_pointer_down():
        if feedback:
            set_active(True)

    def handle_pointer_up():
        if feedback:
            set_active(False)
        if on_click:
            on_click()

    merged_children = [css_style]
    if callable(children):
        merged_children.append(children())
    else:
        merged_children.append(children)

    return solara.html.Tag(
        "div",
        children=merged_children,
        id=unique_id,
        class_name="clickable",
        on_mouse_down=lambda: handle_pointer_down(),
        on_mouse_up=lambda: handle_pointer_up(),
        on_touch_start=lambda: handle_pointer_down(),
        on_touch_end=lambda: handle_pointer_up(),
    )


# =============================================================================
# TOOLTIP
# =============================================================================

@solara.component
def Tooltip(
    children: solara.Element = None,
    tooltip: str = "",
    position: Literal["top", "bottom", "left", "right"] = "top",
    delay: float = 0.3,
    duration: Literal["fast", "normal"] = "normal",
):
    """Animated tooltip that appears on hover.

    Args:
        children: Element to attach tooltip to.
        tooltip: Tooltip text content.
        position: Tooltip position relative to element.
        delay: Delay before showing tooltip (seconds).
        duration: Animation duration.
    """
    unique_id = f"tooltip-{uuid.uuid4().hex[:8]}"
    duration_ms = DURATION_TOKENS.get(duration, 300)

    # Position-based CSS
    position_css = {
        "top": {"bottom": "100%", "left": "50%", "transform": "translateX(-50%) translateY(-8px)"},
        "bottom": {"top": "100%", "left": "50%", "transform": "translateX(-50%) translateY(8px)"},
        "left": {"right": "100%", "top": "50%", "transform": "translateX(-8px) translateY(-50%)"},
        "right": {"left": "100%", "top": "50%", "transform": "translateX(8px) translateY(-50%)"},
    }

    pos = position_css.get(position, position_css["top"])
    transform_base = pos.get("transform", "")

    css_style = f"""
<style>
#{unique_id} {{
    position: relative;
    display: inline-block;
}}
#{unique_id} .tooltip-text {{
    visibility: hidden;
    opacity: 0;
    position: absolute;
    {transform_base};
    background: #1e293b;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 1000;
    transition: opacity {duration_ms}ms ease, visibility {duration_ms}ms ease, transform {duration_ms}ms ease;
    pointer-events: none;
}}
#{unique_id}:hover .tooltip-text {{
    visibility: visible;
    opacity: 1;
    animation: tooltip-fade-in {duration_ms}ms ease forwards;
    animation-delay: {delay}s;
}}
@keyframes tooltip-fade-in {{
    from {{ opacity: 0; transform: {transform_base}; }}
    to {{ opacity: 1; transform: {pos.get('transform').replace('translateX(-50%)', 'translateX(-50%)').replace('translateX(-8px)', 'translateX(-8px)').replace('translateY(8px)', 'translateY(0)').replace('translateY(-8px)', 'translateY(0)').replace('translateY(-50%)', 'translateY(-50%)').replace('translateY(50%)', 'translateY(-50%)' if 'translateY' in str(pos.get('transform', '')) else 'translateY(-50%)'); }}
}}
</style>
"""

    return solara.html.Tag(
        "span",
        children=[
            css_style,
            children,
            solara.span(class_="tooltip-text", children=[tooltip]),
        ],
        id=unique_id,
        class_name="tooltip-container",
    )


# =============================================================================
# CHECKMARK ANIMATION
# =============================================================================

@solara.component
def CheckmarkIcon(
    *,
    size: int = 24,
    color: str = "#10b981",  # Emerald
    duration: Literal["fast", "normal", "slow"] = "normal",
    on_complete: Optional[callable] = None,
):
    """Animated SVG checkmark with stroke draw effect.

    Args:
        size: Icon size in pixels.
        color: Checkmark color.
        duration: Animation duration.
        on_complete: Callback when animation completes.
    """
    unique_id = f"checkmark-{uuid.uuid4().hex[:8]}"
    duration_ms = DURATION_TOKENS.get(duration, 300)

    # SVG path length is approximately 32
    path_length = 32

    css_style = f"""
<style>
#{unique_id} chevron {{
    stroke-dasharray: {path_length};
    stroke-dashoffset: {path_length};
    animation: draw-check {duration_ms}ms ease forwards;
}}
@keyframes draw-check {{
    to {{ stroke-dashoffset: 0; }}
}}
</style>
"""

    def handle_animation_end():
        if on_complete:
            on_complete()

    return solara.html.Tag(
        "svg",
        children=[
            css_style,
            solara.html.Tag(
                "path",
                attributes={
                    "d": "M20 6L9 17L4 12",
                    "fill": "none",
                    "stroke": color,
                    "stroke-width": "3",
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "class": f"#{unique_id} chevron",
                },
            ),
        ],
        id=unique_id,
        width=size,
        height=size,
        viewBox="0 0 24 24",
        on_animation_end=lambda: handle_animation_end(),
    )


# =============================================================================
# LOADING OVERLAY
# =============================================================================

@solara.component
def LoadingOverlay(
    *,
    show: bool = False,
    backdrop: bool = True,
    spinner_color: str = "#7c3aed",
    spinner_size: int = 40,
    message: str = "Loading...",
    full_screen: bool = True,
):
    """Loading overlay with animated spinner.

    Args:
        show: Whether to show the overlay.
        backdrop: Show semi-transparent backdrop.
        spinner_color: Spinner color.
        spinner_size: Spinner size in pixels.
        message: Loading message text.
        full_screen: Cover entire screen vs parent container.
    """
    unique_id = f"loading-overlay-{uuid.uuid4().hex[:8]}"

    css_style = f"""
<style>
#{unique_id} {{
    position: {'fixed' if full_screen else 'absolute'};
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: {('flex' if show else 'none')};
    align-items: center;
    justify-content: center;
    flex-direction: column;
    z-index: 9999;
}}
#{unique_id} .backdrop {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
}}
#{unique_id} .spinner {{
    width: {spinner_size}px;
    height: {spinner_size}px;
    border: 3px solid rgba(124, 58, 237, 0.2);
    border-top-color: {spinner_color};
    border-radius: 50%;
    animation: spin 1s linear infinite;
    position: relative;
    z-index: 1;
}}
#{unique_id} .message {{
    color: white;
    font-size: 14px;
    margin-top: 16px;
    position: relative;
    z-index: 1;
}}
@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
</style>
"""

    return solara.html.Tag(
        "div",
        children=[
            css_style,
            solara.html.Tag(
                "div",
                class_name="backdrop" if backdrop else "",
            ) if show else None,
            solara.html.Tag(
                "div",
                class_name="spinner",
            ) if show else None,
            solara.html.Tag(
                "span",
                children=[message],
                class_name="message",
            ) if show else None,
        ],
        id=unique_id,
        style="display: none;" if not show else "",
    )


# =============================================================================
# SHAKE ERROR ANIMATION
# =============================================================================

@solara.component
def ShakeOnError(
    children: solara.Element = None,
    *,
    error: Optional[str] = None,
    shakes: int = 3,
    amplitude: float = 10,
    duration: Literal["fast", "normal"] = "normal",
    class_name: Optional[str] = None,
):
    """Shake animation triggered by error state.

    Args:
        children: Content to wrap.
        error: Error message. If set, shake animation triggers.
        shakes: Number of shake oscillations.
        amplitude: Shake amplitude in pixels.
        duration: Base animation duration.
        class_name: Additional CSS classes.
    """
    unique_id = f"shake-{uuid.uuid4().hex[:8]}"
    duration_ms = DURATION_TOKENS.get(duration, 300)
    total_duration = duration_ms * shakes * 2  # Round trip

    # Build shake keyframes
    half_shake = amplitude
    keyframes = []
    for i in range(shakes * 2 + 1):
        percent = (i / (shakes * 2)) * 100
        offset = half_shake if i % 2 == 0 else -half_shake
        keyframes.append(f"    {percent}% {{ transform: translateX({offset}px); }}")
    shake_css = "\n".join(keyframes)

    css_style = f"""
<style>
@keyframes shake-{unique_id} {{
{shake_css}
}}
#{unique_id} {{
    display: inline-block;
    animation: {('shake-animation' if error else 'none')};
}}
@keyframes shake-animation {{
{shake_css}
}}
</style>
"""

    animation_style = {"animation": f"shake-{unique_id} {total_duration}ms ease-in-out"} if error else {}

    return solara.html.Tag(
        "div",
        children=[css_style, children],
        id=unique_id,
        class_name=f"shake-container {class_name}" if class_name else "shake-container",
        style=animation_style,
    )


# =============================================================================
# GLOBAL CSS (inject once at app level)
# =============================================================================

MICROINTERACTIONS_CSS = """
/* Microinteractions base styles */
.hoverable, .clickable {{
    cursor: pointer;
    transform: translateZ(0);
    will-change: transform, box-shadow;
}}

/* Reduced motion fallback */
@media (prefers-reduced-motion: reduce) {{
    .hoverable, .clickable, .tooltip-container, .shake-container {{
        transition: none !important;
        animation: none !important;
        transform: none !important;
    }}
}}
"""

__all__ = [
    "Hoverable",
    "Clickable",
    "Tooltip",
    "CheckmarkIcon",
    "LoadingOverlay",
    "ShakeOnError",
    "MICROINTERACTIONS_CSS",
]