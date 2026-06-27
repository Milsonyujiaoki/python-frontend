import reflex as rx
from state import ReflexAuthState
from components.nav import layout


def register() -> rx.Component:
    """Register page component."""
    return layout(
        rx.container(
            rx.vstack(
                rx.heading("Create Account", size="lg"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Full Name",
                            type="text",
                            value=ReflexAuthState.register_full_name,
                            on_change=ReflexAuthState.set_register_full_name,
                            required=True,
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=ReflexAuthState.register_email,
                            on_change=ReflexAuthState.set_register_email,
                            required=True,
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            value=ReflexAuthState.register_password,
                            on_change=ReflexAuthState.set_register_password,
                            required=True,
                            width="100%",
                        ),
                        rx.button(
                            rx.cond(
                                ReflexAuthState.is_loading,
                                rx.spinner(size="sm"),
                                "Create Account"
                            ),
                            type="submit",
                            width="100%",
                            color_scheme="green",
                            mt=4,
                            disabled=~ReflexAuthState.register_form_valid,
                        ),
                        rx.button(
                            "Already have an account? Sign In",
                            href="/login",
                            variant="link",
                            size="sm",
                            mt=2,
                        ),
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(ReflexAuthState.error_message),
                            status="error",
                            is_visible=ReflexAuthState.error_message != "",
                            mt=3,
                        ),
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(ReflexAuthState.success_message),
                            status="success",
                            is_visible=ReflexAuthState.success_message != "",
                            mt=3,
                        ),
                        width="100%",
                        max_width="400px",
                    ),
                    on_submit=ReflexAuthState.register,
                    reset_on_submit=False,
                    width="100%",
                    max_width="400px",
                ),
                spacing="4",
                justify="center",
                align="stretch",
                min_height="85vh",
            ),
        )
    )


# Export for import in __init__.py
register = register