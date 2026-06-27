import reflex as rx
from state import ReflexAuthState
from components.nav import layout


def login() -> rx.Component:
    """Login page component."""
    return layout(
        rx.container(
            rx.vstack(
                rx.heading("Login to BarberShop", size="3"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=ReflexAuthState.login_email,
                            on_change=ReflexAuthState.set_login_email,
                            required=True,
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            value=ReflexAuthState.login_password,
                            on_change=ReflexAuthState.set_login_password,
                            required=True,
                            width="100%",
                        ),
                        rx.button(
                            rx.cond(
                                ReflexAuthState.is_loading,
                                rx.spinner(size="sm"),
                                "Sign In"
                            ),
                            type="submit",
                            width="100%",
                            color_scheme="blue",
                            mt=4,
                            disabled=~ReflexAuthState.login_form_valid,
                        ),
                        rx.button(
                            "Forgot Password?",
                            href="/forgot-password",
                            variant="link",
                            size="sm",
                            mt=2,
                        ),
                        rx.button(
                            "Don't have an account? Sign Up",
                            href="/register",
                            variant="outline",
                            mt=2,
                        ),
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(ReflexAuthState.error_message),
                            status="error",
                            is_visible=ReflexAuthState.error_message != "",
                            mt=3,
                        ),
                        width="100%",
                        max_width="400px",
                    ),
                    on_submit=ReflexAuthState.login,
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
login = login