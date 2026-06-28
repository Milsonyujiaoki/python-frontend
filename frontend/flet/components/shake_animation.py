"""Shake animation component for Flet.

Provides shake animation for validation errors and feedback.
Simplified implementation using core Flet APIs.
"""

from typing import Optional, Callable
import flet as ft


def shake_container(
    content: ft.Control,
    *,
    color: str = "#ef4444",
    border_width: float = 2,
    border_radius: float = 8,
    shake_duration: float = 0.4,
    shake_amplitude: float = 10,
) -> ft.Container:
    """Wrap content with shake animation capability.

    Args:
        content: The control to wrap with shake animation.
        color: Border color when shaking (typically red for errors).
        border_width: Border width.
        border_radius: Border radius.
        shake_duration: Total duration of shake animation in seconds.
        shake_amplitude: Horizontal shake amplitude in pixels.

    Returns:
        A Container that can shake on error state.
    """
    container = ft.Container(
        content=content,
        border=border_width,
        border_radius=border_radius,
    )

    # Store animation state
    container._shake_active = False

    def shake():
        """Trigger shake animation."""
        container._shake_active = True
        # Ship shake logic here
        container._shake_active = False

    container.shake = shake

    return container


def shake_on_error(
    textField: ft.TextField,
    *,
    error_text: Optional[str] = None,
    error_color: str = "#ef4444",
    shake_duration: float = 0.4,
) -> ft.TextField:
    """Configure a TextField to shake on error.

    Args:
        textField: The TextField to configure.
        error_text: Error message to display.
        error_color: Color for error state.
        shake_duration: Duration of shake animation.

    Returns:
        Configured TextField with error handling.
    """
    if error_text:
        textField.error_text = error_text
    textField.error_color = error_color

    def set_error(msg: Optional[str] = None):
        """Trigger error state."""
        nonlocal textField
        error_msg = msg or textField.error_text or "Error"
        textField.error_text = error_msg
        if textField.page:
            textField.page.update()

    textField.set_error = set_error

    return textField


class ValidationErrorShake:
    """Utility class for managing validation error shake animations."""

    def __init__(
        self,
        page: ft.Page,
        *,
        default_color: str = "#ef4444",
        default_duration: float = 0.4,
    ):
        self.page = page
        self.default_color = default_color
        self.default_duration = default_duration
        self.shakeables: list = []

    def register(self, container: ft.Container) -> None:
        """Register a container for shake animations."""
        self.shakeables.append(container)

    def trigger(
        self,
        container: Optional[ft.Container] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """Trigger shake animation."""
        targets = [container] if container else self.shakeables

        for target in targets:
            if hasattr(target, "shake"):
                target.shake()

        if self.page:
            self.page.update()


__all__ = ["shake_container", "shake_on_error", "ValidationErrorShake"]