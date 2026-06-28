"""Scrollytelling component for Solara.

This component creates scroll-triggered animations where content reveals
itself as the user scrolls. Each "step" can have its own animation that
triggers when the section enters the viewport.

Usage::

    from frontend.solara.components.scrollytelling import Scrollytelling, Step

    Scrollytelling(
        steps=[
            Step(title="First", animation="fade-in"),
            Step(title="Second", animation="slide-up"),
        ],
        container_height="600px",
    )
"""

import solara
from typing import List, Optional, Literal
import uuid


@solara.component
def Step(
    children: solara.Element = None,
    *,
    animation: Literal["fade-in", "slide-up", "slide-down", "scale-in"] = "fade-in",
    threshold: float = 0.2,
    once: bool = True,
    class_name: Optional[str] = None,
):
    """Individual step in a scrollytelling sequence.

    Args:
        children: Content for this step.
        animation: Animation to trigger when step becomes visible.
        threshold: Percentage of element visible to trigger (0.0-1.0).
        once: If True, animation only triggers once.
        class_name: Additional CSS classes.
    """
    step_id = f"scrolly-step-{uuid.uuid4().hex[:8]}"

    # Build CSS class based on animation
    anim_class = f"step-{animation.replace('-', '')}"
    merged_class = f"scrollytelling-step invisible {anim_class} {class_name}" if class_name else f"scrollytelling-step invisible {anim_class}"

    return solara.Div(
        children=children,
        id=step_id,
        class_name=merged_class,
        data_threshold=str(threshold),
        data_once=str(once).lower(),
        data_animation=animation,
    )


@solara.component
def Scrollytelling(
    steps: List[solara.Element] = None,
    *,
    container_height: str = "100vh",
    smooth_scroll: bool = True,
    class_name: Optional[str] = None,
):
    """Scrollytelling container with scroll-triggered animations.

    Args:
        steps: List of Step components.
        container_height: Height of the scrolling container.
        smooth_scroll: Enable smooth scrolling behavior.
        class_name: Additional CSS classes.
    """
    container_id = f"scrollytelling-{uuid.uuid4().hex[:8]}"

    # Intersection Observer JavaScript
    observer_js = f"""
(function() {{
    if (window.SOLARA_SCROLLY_OBSERVER) return;
    window.SOLARA_SCROLLY_OBSERVER = true;

    const steps = document.querySelectorAll('#{container_id} .scrollytelling-step');

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const step = entry.target;
                const once = step.dataset.once === 'true';

                step.classList.remove('invisible');
                step.classList.add('visible');
                step.style.animationPlayState = 'running';

                if (once) {{
                    observer.unobserve(step);
                }}
            }} else {{
                const once = step.dataset.once === 'true';
                if (!once) {{
                    step.classList.remove('visible');
                    step.classList.add('invisible');
                }}
            }}
        }});
    {{}}, {{
        threshold: parseFloat(document.getElementById('{container_id}').dataset.threshold || '0.2'),
        rootMargin: '0px'
    }});

    steps.forEach(step => {{
        step.style.animationPlayState = 'paused';
        observer.observe(step);
    }});
}})();
"""

    # Inject script on mount
    solara.use_effect(
        lambda: solara.run_script(observer_js),
        []
    )

    merged_class = f"scrollytelling-container {class_name}" if class_name else "scrollytelling-container"

    return solara.Div(
        children=steps,
        id=container_id,
        class_name=merged_class,
        style={
            "height": container_height,
            "overflow-y": "auto",
            "position": "relative",
        },
        data_threshold="0.2",
    )


# Global CSS for scrollytelling
SCROLLYTELLING_CSS = """
/* Scrollytelling base styles */
.scrollytelling-container {
    position: relative;
    scroll-behavior: smooth;
}

.scrollytelling-step {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
    min-height: 50vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Invisible state */
.invisible {
    opacity: 0;
}

/* Visible state */
.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Animation variations */
.step-slideup.visible {
    transform: translateY(0);
}

.step-slidedown.visible {
    transform: translateY(0);
}

.step-scalein.visible {
    transform: scale(1);
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .scrollytelling-step {
        transition: none;
        opacity: 1 !important;
        transform: none !important;
    }
}
"""

__all__ = ["Scrollytelling", "Step", "SCROLLYTELLING_CSS"]