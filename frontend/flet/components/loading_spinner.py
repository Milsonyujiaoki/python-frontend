"""Loading spinner components for Flet.

Provides animated loading indicators with various styles.
Simplified implementation using core Flet APIs.
"""

import flet as ft
from typing import Optional


def loading_spinner(
    *,
    color: str = "#6366f1",
    background_color: Optional[str] = None,
    size: int = 24,
    style: str = "circular",
    speed: float = 1.0,
) -> ft.Column:
    """Render an animated loading spinner.

    Args:
        color: Spinner color (hex or named color).
        background_color: Background color for the spinner track.
        size: Size in pixels.
        style: One of "circular", "dots", "bars".
        speed: Animation speed multiplier (1.0 = normal).

    Returns:
        A Column containing the spinner widget.
    """
    if style == "circular":
        spinner = ft.ProgressRing(
            color=color,
            bgcolor=background_color,
            width=size,
            height=size,
        )
    elif style == "dots":
        spinner = ft.Row(
            controls=[
                ft.Container(
                    width=size // 2,
                    height=size // 2,
                    bgcolor=color,
                    border_radius=size // 4,
                )
                for _ in range(3)
            ],
            spacing=size // 4,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    elif style == "bars":
        spinner = ft.Row(
            controls=[
                ft.Container(
                    width=size // 6,
                    height=size,
                    bgcolor=color,
                    border_radius=2,
                )
                for _ in range(4)
            ],
            spacing=size // 8,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    else:
        spinner = ft.ProgressRing(
            color=color,
            bgcolor=background_color,
            width=size,
            height=size,
        )

    return ft.Column([spinner], alignment=ft.MainAxisAlignment.CENTER, tight=True)


def spinner_overlay(
    *,
    message: str = "Carregando...",
    color: str = "#6366f1",
) -> ft.Container:
    """Render a full-screen loading overlay."""
    return ft.Container(
        content=ft.Column(
            [
                loading_spinner(color=color, size=40),
                ft.Text(message, size=14, color="#666"),
            ],
            spacing=16,
        ),
    )


__all__ = ["loading_spinner", "spinner_overlay"]