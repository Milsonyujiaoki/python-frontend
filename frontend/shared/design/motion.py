"""Design system motion tokens and helpers.

This module defines standard animation durations, easing curves, and a helper
to generate CSS variable declarations for the token values. The values are
chosen to be ergonomic for the UI library and can be referenced from
framework‑specific style generators (e.g. FastUI, Streamlit, Solara, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Dict

# ---------------------------------------------------------------------------
# Duration tokens (in milliseconds)
# ---------------------------------------------------------------------------
DURATION_TOKENS: Mapping[str, int] = {
    "fast": 150,
    "normal": 300,
    "slow": 500,
    "cinematic": 800,
}

# ---------------------------------------------------------------------------
# Easing tokens – CSS cubic‑bezier strings that map to common easing names.
# ---------------------------------------------------------------------------
EASING_TOKENS: Mapping[str, str] = {
    "ease-in": "cubic-bezier(0.42, 0, 1, 1)",
    "ease-out": "cubic-bezier(0, 0, 0.58, 1)",
    "ease-in-out": "cubic-bezier(0.42, 0, 0.58, 1)",
    "bounce": "cubic-bezier(0.68, -0.55, 0.27, 1.55)",
    "elastic": "cubic-bezier(0.5, 1.5, 0.5, -0.5)",
}

# ---------------------------------------------------------------------------
# Helper to produce CSS custom properties for the tokens.
# ---------------------------------------------------------------------------
def generate_css_variables() -> str:
    """Return a CSS ``:root`` block with custom properties for motion.

    The generated CSS looks like::

        :root {
            --motion-duration-fast: 150ms;
            --motion-duration-normal: 300ms;
            ...
            --motion-easing-ease-in: cubic-bezier(...);
            ...
        }
    """
    lines = [":root {"]
    for name, ms in DURATION_TOKENS.items():
        lines.append(f"    --motion-duration-{name}: {ms}ms;")
    for name, bez in EASING_TOKENS.items():
        lines.append(f"    --motion-easing-{name}: {bez};")
    lines.append("}")
    return "\n".join(lines)

# Export a small mapping for quick lookup in Python‑side code.
MOTION_TOKENS: Dict[str, int | str] = {
    **{f"duration-{k}": v for k, v in DURATION_TOKENS.items()},
    **{f"easing-{k}": v for k, v in EASING_TOKENS.items()},
}

__all__ = [
    "DURATION_TOKENS",
    "EASING_TOKENS",
    "generate_css_variables",
    "MOTION_TOKENS",
    "prefers_reduced_motion_css",
    "custom_cursor_css",
]

def prefers_reduced_motion_css() -> str:
    """CSS for reduced‑motion preference (already defined)."""
    return (
        "@media (prefers-reduced-motion: reduce) {\n"
        "    * {\n"
        "        animation-duration: 0ms !important;\n"
        "        transition-duration: 0ms !important;\n"
        "        animation-iteration-count: 1 !important;\n"
        "        animation-timing-function: linear !important;\n"
        "    }\n"
        "}\n"
    )

def fallback_animation_css() -> str:
    """Return CSS that disables animations entirely.

    Used when the JavaScript injection fails (e.g., network block). Frontend
    code can inject this string as a safety net.
    """
    return (
        "* {\n"
        "    animation: none !important;\n"
        "    transition: none !important;\n"
        "    transform: none !important;\n"
        "}\n"
    )
    """CSS that disables motion when ``prefers-reduced-motion`` is set.

    The function returns a ``@media`` block that forces animation
    durations to ``0ms`` and easings to ``linear``. Frontend code can
    inject the returned string into the page head.
    """
    return (
        "@media (prefers-reduced-motion: reduce) {\n"
        "    * {\n"
        "        animation-duration: 0ms !important;\n"
        "        transition-duration: 0ms !important;\n"
        "        animation-iteration-count: 1 !important;\n"
        "        animation-timing-function: linear !important;\n"
        "    }\n"
        "}\n"
    )

def custom_cursor_css() -> str:
    """CSS for a growing custom cursor on hover.

    The cursor expands to 32px with a soft halo effect. Frontends can inject
    this style globally or scoped to a container.
    """
    return (
        "* { cursor: none; }\n"
        "body::after {\n"
        "  content: '';\n"
        "  position: fixed;\n"
        "  top: 0; left: 0;\n"
        "  width: 16px; height: 16px;\n"
        "  border-radius: 50%;\n"
        "  background: rgba(0,0,0,0.2);\n"
        "  pointer-events: none;\n"
        "  transform: translate(-50%, -50%);\n"
        "  transition: width 0.2s ease, height 0.2s ease;\n"
        "}\n"
        "*:hover::after { width: 32px; height: 32px; background: rgba(0,0,0,0.4); }"
    )
