"""Example carousel component using GSAP for slide animation.

The component renders a horizontal list of items (simple colored boxes) and
animates an automatic sliding loop using the ``GSAPAnimator`` wrapper.
This serves as a demo for task 2.6 – a carousel with auto‑slide and
GSAP‑driven distortion effects.
"""

import reflex as rx
from .gsap_animator import GSAPAnimator

def example_carousel(*, width: str = "100%", height: str = "200px", slide_interval: float = 3.0) -> rx.Component:
    """Render a simple carousel.

    Args:
        width: CSS width of the carousel container.
        height: CSS height of the carousel container.
        slide_interval: Seconds between slide transitions.
    """
    container_id = "carousel-container"
    # Create a list of three placeholder slides.
    slides = [
        rx.box(bg="red", width="100%", height="100%", key=f"slide{i}")
        for i in range(3)
    ]
    # Container that will hold the slides side‑by‑side.
    carousel = rx.box(
        *slides,
        id=container_id,
        width=width,
        height=height,
        overflow="hidden",
        display="flex",
        position="relative",
    )

    # Initialise animation on mount.
    def start_animation():
        animator = GSAPAnimator()
        # Use GSAP to animate the container's X translation.
        # The animation moves -100% every interval, then loops.
        js = (
            f"gsap.to('#{container_id}', {{x: '-=100%', duration: 0.8, ease: 'power1.inOut', repeat: -1, repeatDelay: {slide_interval}}});"
        )
        rx.eval(js)

    rx.use_effect(lambda: start_animation(), [])
    return carousel

__all__ = ["example_carousel"]
