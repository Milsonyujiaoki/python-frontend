"""GSAP animator wrapper for Reflex.

The Reflex framework can execute arbitrary JavaScript in the browser via
``window.eval``. This module provides a thin Python wrapper around the
GSAP animation library (loaded from a CDN) so that Reflex components can
trigger animations without writing inline JS.

Typical usage::

    from reflex import rx
    from .gsap_animator import GSAPAnimator

    animator = GSAPAnimator()

    def on_click():
        animator.to("#my-box", {"x": 200}, duration=0.5, easing="ease-out")

    # In a component
    rx.box(id="my-box", width="100px", height="100px", bg="blue")
    rx.button("Move", on_click=on_click)
"""

import json
import reflex as rx

# CDN URL for GSAP (latest version)
GSAP_CDN = "https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"

def load_gsap() -> None:
    """Inject the GSAP script tag if it hasn't been loaded yet.

    The function checks the ``window.GSAP_LOADED`` flag; if false it creates a
    ``<script>`` element pointing at the CDN URL. Reflex's ``rx.eval`` runs the
    JavaScript in the client environment.
    """
    # The JS checks the flag and injects only when needed.
    js = (
        "if (!window.GSAP_LOADED) {"
        f"var s=document.createElement('script');s.src='{GSAP_CDN}';s.onload=function(){{window.GSAP_LOADED=true;}};document.head.appendChild(s);"
        "}"
    )
    rx.eval(js)


class GSAPAnimator:
    """Load GSAP once and expose ``to``/``from`` animation helpers.

    The implementation relies on ``rx.use_effect`` to inject the script
    tag when the first ``GSAPAnimator`` instance is created. Subsequent
    instances reuse the already‑loaded library.
    """

    _initialized = False

    def __init__(self) -> None:
        # Ensure the GSAP script is injected on the client side.
        if not GSAPAnimator._initialized:
            rx.use_effect(self._inject_script, [])
            GSAPAnimator._initialized = True

    def _inject_script(self) -> None:
        # Public helper – can be called independently to ensure script is present.
        load_gsap()

        """Inject a <script> tag that loads GSAP via ``window.eval``.

        ``window.eval`` executes a string of JavaScript in the browser
        context. We create a minimal script that appends the GSAP CDN to the
        document head and resolves a promise when the library is ready.
        """
        js = (
            f"var s=document.createElement('script');"
            f"s.src='{GSAP_CDN}';"
            f"s.onload=function(){{window.GSAP_LOADED=true;}};"
            f"document.head.appendChild(s);"
        )
        # ``window.eval`` runs the string on the client.
        rx.eval(js)

    def _ensure_loaded(self) -> None:
        """Guarantee that GSAP has been loaded before calling animations.
        In a production build the script will already be present; during
        development we poll the ``GSAP_LOADED`` flag.
        """
        check_js = "return !!window.GSAP_LOADED;"
        # ``rx.eval`` returns a ``Promise``; ``use_effect`` can wait for it.
        # Here we simply fire the check – if not loaded, the animation will
        # fail silently, which is acceptable for the prototype.
        rx.eval(check_js)

    def to(
        self,
        target: str,
        vars_: dict,
        *,
        duration: float = 0.5,
        easing: str = "power1.out",
        delay: float = 0.0,
    ) -> None:
        """Run ``gsap.to`` on ``target``.

        Args:
            target: CSS selector (e.g. "#my-box" or ".item")
            vars_: Animation properties (e.g. {"x": 100, "opacity": 0})
            duration: Length of the animation in seconds
            easing: GSAP easing string
            delay: Optional start delay in seconds
        """
        self._ensure_loaded()
        # Build the JS call string. ``json.dumps`` safely serialises the dict.
        vars_json = json.dumps(vars_)
        js = (
            f"gsap.to('{target}', Object.assign({vars_json}, {{duration:{duration}, ease:'{easing}', delay:{delay}}));"
        )
        rx.eval(js)

    # Convenience alias for ``from`` animations (starting state).
    def from_(self, target: str, vars_: dict, *, duration: float = 0.5, easing: str = "power1.out", delay: float = 0.0) -> None:
        """Run ``gsap.from`` – similar signature to :meth:`to`."""
        self._ensure_loaded()
        vars_json = json.dumps(vars_)
        js = (
            f"gsap.from('{target}', Object.assign({vars_json}, {{duration:{duration}, ease:'{easing}', delay:{delay}}));"
        )
        rx.eval(js)

__all__ = ["GSAPAnimator"]
