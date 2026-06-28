"""Parallax scrolling component for Solara.

This component renders a container with a background image that moves at a
different speed than the foreground content based on the page scroll position.
It uses a small JavaScript snippet injected via ``solara.html`` to update the
background position.
"""

import solara
from solara import html

def parallax_scrolling(*, image_url: str, speed: float = 0.5, height: str = "400px") -> solara.Component:
    """Render a parallax section.

    Args:
        image_url: URL of the background image.
        speed: Multiplier for scroll offset (0 = static, 1 = same speed).
        height: Height of the component.
    """
    container_id = "solara-parallax"

    # Inject JS that updates background position on scroll.
    js = f"""
        window.addEventListener('scroll', function() {{
            var el = document.getElementById('{container_id}');
            if (!el) return;
            var offset = window.scrollY * {speed};
            el.style.backgroundPosition = 'center ' + offset + 'px';
        }});
    """
    solara.use_effect(lambda: solara.run_script(js), [])

    style = f"background-image: url('{image_url}'); background-attachment: fixed; background-size: cover; height: {height};"
    return html.div(id=container_id, style=style)

__all__ = ["parallax_scrolling"]
