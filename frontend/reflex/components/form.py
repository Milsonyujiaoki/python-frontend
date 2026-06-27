import reflex as rx


def form_input(
    placeholder: str,
    value: str,
    on_change,
    required: bool = False,
    width: str = "100%",
    size: list = ["md", "lg", "lg"],
    input_type: str = "text",
):
    """
    A reusable form input component.

    Args:
        placeholder: str, the placeholder text
        value: str, the current value
        on_change: callable, the on_change handler
        required: bool, whether the field is required (default: False)
        width: str, the width of the input (default: "100%")
        size: list, responsive size values (default: ["md", "lg", "lg"])
        input_type: str, the input type (default: "text")

    Returns:
        rx.Component: A form input component.
    """
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        required=required,
        width=width,
        size=size,
        type=input_type,
    )


def form_textarea(
    placeholder: str,
    value: str,
    on_change,
    required: bool = False,
    width: str = "100%",
    size: list = ["md", "lg", "lg"],
    rows: int = 3,
):
    """
    A reusable form textarea component.

    Args:
        placeholder: str, the placeholder text
        value: str, the current value
        on_change: callable, the on_change handler
        required: bool, whether the field is required (default: False)
        width: str, the width of the textarea (default: "100%")
        size: list, responsive size values (default: ["md", "lg", "lg"])
        rows: int, number of rows (default: 3)

    Returns:
        rx.Component: A form textarea component.
    """
    return rx.text_area(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        required=required,
        width=width,
        size=size,
        rows=rows,
    )


def form_select(
    placeholder: str,
    value: str,
    on_change,
    options: list,
    required: bool = False,
    width: str = "100%",
    size: list = ["md", "lg", "lg"],
):
    """
    A reusable form select component.

    Args:
        placeholder: str, the placeholder text
        value: str, the current value
        on_change: callable, the on_change handler
        options: list, list of options (each option should be a string)
        required: bool, whether the field is required (default: False)
        width: str, the width of the select (default: "100%")
        size: list, responsive size values (default: ["md", "lg", "lg"])

    Returns:
        rx.Component: A form select component.
    """
    return rx.select(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        required=required,
        width=width,
        size=size,
        items=options,
    )


def form_button(
    label: str,
    on_click,
    loading: bool = False,
    color_scheme: str = "green",
    variant: str = "solid",
    size: list = ["md", "lg", "lg"],
    disabled: bool = False,
):
    """
    A reusable form button component.

    Args:
        label: str, the button text
        on_click: callable, the on_click handler
        loading: bool, whether to show loading spinner (default: False)
        color_scheme: str, the color scheme (default: "green")
        variant: str, the variant (default: "solid")
        size: list, responsive size values (default: ["md", "lg", "lg"])
        disabled: bool, whether the button is disabled (default: False)

    Returns:
        rx.Component: A form button component.
    """
    if loading:
        button_content = rx.spinner(size="sm")
    else:
        button_content = label

    return rx.button(
        button_content,
        on_click=on_click,
        loading=loading,
        color_scheme=color_scheme,
        variant=variant,
        size=size,
        disabled=disabled,
    )


def form_field(
    label: str,
    component: rx.Component,
    required: bool = False,
    width: str = "100%",
):
    """
    A reusable form field wrapper that combines a label with a component.

    Args:
        label: str, the field label
        component: rx.Component, the input component (input, textarea, select, etc.)
        required: bool, whether the field is required (default: False)
        width: str, the width of the field (default: "100%")

    Returns:
        rx.Component: A form field with label and component.
    """
    return rx.vstack(
        rx.hstack(
            rx.text(
                label,
                weight="medium",
                width="100px",
            ),
            rx.spacer(),
            width="100%",
        ),
        component,
        width=width,
        spacing="1",
    )


def form_alert(
    message: str,
    status: str = "error",
    visible: bool = True,
    mt: int = 3,
):
    """
    A reusable form alert component.

    Args:
        message: str, the alert message
        status: str, the status ("error", "success", "warning", "info") (default: "error")
        visible: bool, whether the alert is visible (default: True)
        mt: int, margin top (default: 3)

    Returns:
        rx.Component: An alert component (toast notification).
    """
    # Return an event trigger that shows a toast when the condition is true
    # We use a conditional that returns the toast event when visible, otherwise nothing
    return rx.cond(
        visible,
        rx.cond(
            status == "success",
            rx.toast.success(message),
            rx.cond(
                status == "error",
                rx.toast.error(message),
                rx.cond(
                    status == "warning",
                    rx.toast.warning(message),
                    rx.toast.info(message)  # default to info for other statuses
                )
            )
        ),
        rx.fragment(),  # Return nothing when not visible
    )


def form_action_buttons(
    cancel_on_click,
    action_on_click,
    cancel_label: str = "Cancel",
    action_label: str = "Submit",
    action_loading: bool = False,
    action_color_scheme: str = "green",
    cancel_variant: str = "outline",
    size: list = ["md", "lg", "lg"],
    spacing: str = "3",
    width: str = "100%",
):
    """
    A reusable form action buttons component.

    Args:
        cancel_on_click: callable, the cancel on_click handler
        action_on_click: callable, the action on_click handler
        cancel_label: str, the cancel button label (default: "Cancel")
        action_label: str, the action button label (default: "Submit")
        action_loading: bool, whether the action button is loading (default: False)
        action_color_scheme: str, the action button color scheme (default: "green")
        cancel_variant: str, the cancel button variant (default: "outline")
        size: list, responsive size values (default: ["md", "lg", "lg"])
        spacing: str, spacing between buttons (default: "3")
        width: str, width of the container (default: "100%")

    Returns:
        rx.Component: A form action buttons component.
    """
    return rx.hstack(
        rx.button(
            cancel_label,
            on_click=cancel_on_click,
            variant=cancel_variant,
            size=size,
        ),
        rx.button(
            rx.cond(
                action_loading,
                rx.spinner(size="sm"),
                action_label,
            ),
            on_click=action_on_click,
            loading=action_loading,
            color_scheme=action_color_scheme,
            size=size,
        ),
        spacing=spacing,
        width=width,
        justify="end",
    )


__all__ = [
    "form_input",
    "form_textarea",
    "form_select",
    "form_button",
    "form_field",
    "form_alert",
    "form_action_buttons",
]