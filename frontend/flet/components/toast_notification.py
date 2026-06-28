"""Toast notification components for Flet.

Provides slide in/out toast notifications with various types.
Simplified implementation using core Flet APIs.
"""

from typing import Callable, Optional
import flet as ft


def toast_notification(
    *,
    message: str,
    toast_type: str = "info",
    on_close: Optional[Callable] = None,
) -> ft.Container:
    """Create a toast notification container.

    Args:
        message: Toast message text.
        toast_type: One of "info", "success", "error", "warning".
        on_close: Callback when toast is closed.

    Returns:
        A Container with the toast UI.
    """
    colors = {
        "info": {"bg": "#3b82f6", "icon": ft.Icons.INFO_OUTLINED},
        "success": {"bg": "#10b981", "icon": ft.Icons.CHECK_CIRCLE_OUTLINED},
        "error": {"bg": "#ef4444", "icon": ft.Icons.ERROR_OUTLINED},
        "warning": {"bg": "#f59e0b", "icon": ft.Icons.WARNING_AMBER_OUTLINED},
    }
    palette = colors.get(toast_type, colors["info"])

    toast = ft.Container(
        content=ft.Row(
            [
                ft.Icon(palette["icon"], color="#fff", size=20),
                ft.Text(message, color="#ffffff", size=14, weight="500"),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_color="#fff",
                    icon_size=18,
                    on_click=on_close,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=palette["bg"],
        border_radius=8,
        padding=12,
        width=320,
    )

    return toast


class ToastNotificationManager:
    """Manager for toast notifications with queue and animations."""

    def __init__(self, page: ft.Page, position: str = "top-right"):
        self.page = page
        self.position = position
        self.toast_stack = ft.Column(spacing=8, tight=True)
        self.container = ft.Container(
            content=self.toast_stack,
            width=340,
        )

    def show(
        self,
        *,
        message: str,
        toast_type: str = "info",
        duration: int = 3000,
        on_close: Optional[Callable] = None,
    ) -> None:
        """Show a toast notification.

        Args:
            message: Toast message text.
            toast_type: One of "info", "success", "error", "warning".
            duration: Display duration in milliseconds.
            on_close: Callback when toast is closed.
        """
        toast = toast_notification(
            message=message,
            toast_type=toast_type,
            on_close=lambda: self.dismiss(toast)
        )

        self.toast_stack.controls.append(toast)
        self.page.update()

        # Auto-dismiss after duration
        import asyncio
        async def auto_dismiss():
            await asyncio.sleep(duration / 1000)
            self.dismiss(toast, on_close)

        asyncio.create_task(auto_dismiss())

    def dismiss(self, toast: ft.Container, on_close: Optional[Callable] = None) -> None:
        """Dismiss a toast.

        Args:
            toast: The toast container to dismiss.
            on_close: Optional callback after dismissal.
        """
        if toast in self.toast_stack.controls:
            self.toast_stack.controls.remove(toast)
            self.page.update()
            if on_close:
                on_close()


__all__ = ["toast_notification", "ToastNotificationManager"]