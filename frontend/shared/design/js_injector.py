"""Utility for injecting arbitrary JavaScript into Reflex pages.

The Reflex framework provides ``rx.eval`` which evaluates a string of JS in the
browser. This helper builds a safe wrapper that only injects the script once.
It is used by several animation components (GSAP, Three.js, custom cursor,
etc.)
"""

import reflex as rx
from typing import Callable

_injected_scripts: set[str] = set()

def inject_js(script_url: str, check_flag: str | None = None) -> None:
    """Inject a ``<script>`` tag loading ``script_url`` if not already present.

    Args:
        script_url: Fully qualified URL to the JavaScript resource.
        check_flag: Optional global JavaScript variable name that signals the
            script has already been loaded (e.g. ``window.GSAP_LOADED``). If
            supplied the function will only inject when the flag is falsy.
    """
    if script_url in _injected_scripts:
        return  # Already injected in this session.

    # Build the JS guard.
    if check_flag:
        js = (
            f"if (!{check_flag}) {{"
            f"var s=document.createElement('script');s.src='{script_url}';"
            f"s.onload=function(){{{check_flag}=true;}};document.head.appendChild(s);"
            "}}"
        )
    else:
        js = (
            f"var s=document.createElement('script');s.src='{script_url}';"
            "document.head.appendChild(s);"
        )
    rx.eval(js)
    _injected_scripts.add(script_url)

def inject_inline(js_body: str) -> None:
    """Execute a snippet of JS directly via ``rx.eval``.

    This is useful for small helpers that do not require a full external file.
    """
    rx.eval(js_body)

__all__ = ["inject_js", "inject_inline"]
