"""Scrollytelling component for Reflex.

The component registers a ``scroll`` event listener on the window and updates a
Reflex ``state`` variable that can be used to drive animations based on the
scroll position. It demonstrates how to combine ``rx.use_effect`` and ``rx.state``.
"""

import reflex as rx

def scrollytelling(*, step_height: int = 500) -> rx.Component:
    """Create a scrollytelling container.

    Args:
        step_height: Number of pixels per storytelling step.
    Returns:
        A ``div`` whose background colour changes as the user scrolls.
    """
    # Reactive state to hold current step index.
    step_state = rx.state(step=0)

    def on_scroll(event: dict) -> None:
        # ``event`` contains ``scrollY`` in the browser.
        scroll_y = event.get("scrollY", 0)
        new_step = scroll_y // step_height
        if new_step != step_state.step:
            step_state.set(step=new_step)

    # Register the listener once.
    rx.use_effect(lambda: rx.eval("window.addEventListener('scroll', e => rx.emit({scrollY: window.scrollY});") ), [])
    # Reflex automatically routes the emitted dict to ``on_scroll``.
    rx.on(event="scroll", handler=on_scroll)

    # Style varies with step.
    bg_color = rx.cond(
        step_state.step == 0, "#ffdddd",
        step_state.step == 1, "#ddffdd",
        step_state.step == 2, "#ddddff",
        "#ffffff",
    )
    return rx.box(
        "Scroll to see the story change",
        width="100%",
        height="400px",
        bg=bg_color,
        display="flex",
        align_items="center",
        justify_content="center",
    )

__all__ = ["scrollytelling"]
