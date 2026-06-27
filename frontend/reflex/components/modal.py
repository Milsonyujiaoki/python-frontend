import reflex as rx

def modal_overlay(
    is_open: bool,
    content: rx.Component,
    on_close,
    title: str = "",
    width: str = "400px",
    padding: str = "4",
):
    """
    A reusable modal overlay component with backdrop.

    Args:
        is_open: bool, whether the modal is open
        content: rx.Component, the content to display in the modal body
        on_close: callable, the function to call when closing the modal
        title: str, the modal title (default: "")
        width: str, the width of the modal (default: "400px")
        padding: str, the padding inside the modal (default: "4")

    Returns:
        rx.Component: A modal overlay component.
    """
    return rx.cond(
        is_open,
        rx.box(
            # Backdrop
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background_color="rgba(0, 0, 0, 0.5)",
                z_index="1000",
                on_click=on_close,
            ),
            # Modal content
            rx.box(
                rx.box(
                    rx.box(
                        rx.button(
                            "×",
                            on_click=on_close,
                            variant="ghost",
                            size="1",
                            position="absolute",
                            top="0",
                            right="0",
                        ),
                        rx.cond(
                            title != "",
                            rx.heading(title, size="lg", margin_bottom="4"),
                            rx.fragment(),
                        ),
                        content,
                        width=width,
                        padding=padding,
                        background_color="white",
                        border_radius="lg",
                        box_shadow="lg",
                    ),
                    position="fixed",
                    top="50%",
                    left="50%",
                    transform="translate(-50%, -50%)",
                    z_index="1001",
                ),
                width="100%",
                height="100vh",
                display="flex",
                justify_content="center",
                align_items="center",
            ),
            position="relative",
            width="100%",
            height="100vh",
        ),
        rx.fragment(),
    )


def simple_modal(
    is_open: bool,
    title: str,
    content: rx.Component,
    on_close,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
    confirm_on_click=None,
    cancel_on_click=None,
    confirm_loading: bool = False,
    confirm_color_scheme: str = "blue",
    width: str = "400px",
    padding: str = "4",
):
    """
    A simple modal with confirmation and cancellation buttons.

    Args:
        is_open: bool, whether the modal is open
        title: str, the modal title
        content: rx.Component, the content to display in the modal body
        on_close: callable, the function to call when closing the modal (via backdrop or X button)
        confirm_label: str, the confirm button label (default: "Confirm")
        cancel_label: str, the cancel button label (default: "Cancel")
        confirm_on_click: callable, the confirm button on_click handler
        cancel_on_click: callable, the cancel button on_click handler (defaults to on_close if not provided)
        confirm_loading: bool, whether the confirm button is loading (default: False)
        confirm_color_scheme: str, the confirm button color scheme (default: "blue")
        width: str, the width of the modal (default: "400px")
        padding: str, the padding inside the modal (default: "4")

    Returns:
        rx.Component: A simple modal component.
    """
    # Use on_close for cancel if not provided
    actual_cancel_on_click = cancel_on_click if cancel_on_click is not None else on_close

    return modal_overlay(
        is_open=is_open,
        title=title,
        width=width,
        padding=padding,
        content=rx.vstack(
            content,
            rx.divider(),
            rx.hstack(
                rx.button(
                    cancel_label,
                    on_click=actual_cancel_on_click,
                    variant="outline",
                    size=["md", "lg", "lg"],
                ),
                rx.button(
                    rx.cond(
                        confirm_loading,
                        rx.spinner(size="sm"),
                        confirm_label,
                    ),
                    on_click=confirm_on_click,
                    loading=confirm_loading,
                    color_scheme=confirm_color_scheme,
                    size=["md", "lg", "lg"],
                ),
                spacing="4",
                justify="end",
                width="100%",
            ),
            width="100%",
            spacing="4",
        ),
        on_close=on_close,
    )