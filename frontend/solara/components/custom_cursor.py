"""Custom cursor component for Solara.

This component provides an interactive cursor that grows on hover elements.
It only activates on desktop devices and respects reduced-motion preferences.

Usage::

    from frontend.solara.components.custom_cursor import CustomCursor

    def HomePage():
        solara.Div("Page content")
        CustomCursor()  # Add once at app root
"""

import solara
import uuid


@solara.component
def CustomCursor(
    *,
    base_size: int = 16,
    hover_size: int = 32,
    color: str = "rgba(124, 58, 237, 0.5)",  # Violet with opacity
    halo_color: str = "rgba(124, 58, 237, 0.2)",
    transition_duration: float = 0.2,
    enabled: bool = True,
):
    """Custom interactive cursor component.

    Args:
        base_size: Base cursor size in pixels.
        hover_size: Cursor size on hover in pixels.
        color: Cursor fill color.
        halo_color: Cursor halo/glow color.
        transition_duration: Animation duration in seconds.
        enabled: If False, cursor is disabled.
    """

    cursor_id = f"custom-cursor-{uuid.uuid4().hex[:8]}"

    # CSS for custom cursor
    cursor_css = f"""
/* Custom cursor setup */
#root, body {{
    cursor: none !important;
}}

#root *, body * {{
    cursor: none !important;
}}

#{{cursor_id}}::after, #{{cursor_id}}::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: {base_size}px;
    height: {base_size}px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: width {transition_duration}s ease, height {transition_duration}s ease,
                background-color {transition_duration}s ease, transform {transition_duration}s ease;
    transform: translate(-50%, -50%);
}}

/* Inner dot */
#{{cursor_id}}::before {{
    background-color: {color};
    width: {base_size // 2}px;
    height: {base_size // 2}px;
}}

/* Outer halo */
#{{cursor_id}}::after {{
    background-color: {halo_color};
}}

/* Hover state */
#{{cursor_id}}.hover::before {{
    width: {hover_size}px;
    height: {hover_size}px;
    background-color: {color};
}}

#{{cursor_id}}.hover::after {{
    width: {hover_size * 2}px;
    height: {hover_size * 2}px;
    background-color: {halo_color};
}}

/* Click state */
#{{cursor_id}}.active::before {{
    transform: translate(-50%, -50%) scale(0.8);
}}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {{
    #{{cursor_id}}::before, #{{cursor_id}}::after {{
        transition: none !important;
    }}
}}

/* Mobile devices - show default cursor */
@media (pointer: coarse) {{
    #root, body, #root *, body * {{
        cursor: auto !important;
    }}
    #{{cursor_id}} {{
        display: none !important;
    }}
}}
"""

    # JavaScript for cursor tracking
    cursor_js = f"""
(function() {{
    if (window.SOLARA_CUSTOM_CURSOR || !document.getElementById('{cursor_id}')) return;
    window.SOLARA_CUSTOM_CURSOR = true;

    const cursor = document.getElementById('{cursor_id}');
    let cursorEl = null;

    function createCursor() {{
        cursorEl = document.createElement('div');
        cursorEl.id = '{cursor_id}';
        cursorEl.className = 'custom-cursor';
        document.body.appendChild(cursorEl);
    }}

    createCursor();

    // Track mouse movement
    document.addEventListener('mousemove', (e) => {{
        if (cursorEl) {{
            cursorEl.style.left = e.clientX + 'px';
            cursorEl.style.top = e.clientY + 'px';
        }}
    }});

    // Hover effects - detect interactive elements
    const interactiveSelector = 'a, button, input, select, textarea, [role="button"], .clickable';
    const elements = document.querySelectorAll(interactiveSelector);

    elements.forEach(el => {{
        el.addEventListener('mouseenter', () => {{
            if (cursorEl) cursorEl.classList.add('hover');
        }});
        el.addEventListener('mouseleave', () => {{
            if (cursorEl) cursorEl.classList.remove('hover');
        }});
        el.addEventListener('mousedown', () => {{
            if (cursorEl) cursorEl.classList.add('active');
        }});
        el.addEventListener('mouseup', () => {{
            if (cursorEl) cursorEl.classList.remove('active');
        }});
    }});

    // Handle dynamic content - use MutationObserver
    const observer = new MutationObserver((mutations) => {{
        mutations.forEach(mutation => {{
            mutation.addedNodes.forEach(node => {{
                if (node.nodeType === 1) {{
                    const interactive = node.querySelectorAll(interactiveSelector);
                    interactive.forEach(el => {{
                        el.addEventListener('mouseenter', () => {{
                            if (cursorEl) cursorEl.classList.add('hover');
                        }});
                        el.addEventListener('mouseleave', () => {{
                            if (cursorEl) cursorEl.classList.remove('hover');
                        }});
                        el.addEventListener('mousedown', () => {{
                            if (cursorEl) cursorEl.classList.add('active');
                        }});
                        el.addEventListener('mouseup', () => {{
                            if (cursorEl) cursorEl.classList.remove('active');
                        }});
                    }});
                }}
            }});
        }});
    }});

    observer.observe(document.body, {{ childList: true, subtree: true }});
}})();
"""

    # Inject CSS
    css_style_tag = f"""
<style id="custom-cursor-styles">
{cursor_css.format(cursor_id=cursor_id)}
</style>
"""

    # Use effect to inject JS on mount
    solara.use_effect(
        lambda: solara.run_script(cursor_js),
        []
    )

    # Return hidden container with CSS
    return solara.html.Tag(
        "div",
        children=[css_style_tag],
        id=cursor_id,
        class_name="custom-cursor-root",
        style="display: none;",
    )


__all__ = ["CustomCursor"]