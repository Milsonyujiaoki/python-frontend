import reflex as rx
from state import ReflexAuthState
from components.nav import layout


def forgot_password() -> rx.Component:
    """Forgot password page component."""
    return layout(
        rx.container(
            rx.vstack(
                rx.heading("Forgot Password", size="lg"),
                rx.text(
                    "Enter your email address to receive a password reset link.",
                    text_align="center",
                    color="gray",
                    mb=6,
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Email",
                            type="email",
                            value=ReflexAuthState.reset_email,
                            on_change=ReflexAuthState.set_reset_email,
                            required=True,
                            width="100%",
                        ),
                        rx.button(
                            rx.cond(
                                ReflexAuthState.is_loading,
                                rx.spinner(size="sm"),
                                "Send Reset Link"
                            ),
                            type="submit",
                            width="100%",
                            color_scheme="orange",
                            mt=4,
                            disabled=~ReflexAuthState.forgot_password_form_valid,
                        ),
                        rx.button(
                            "Back to Login",
                            href="/login",
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
                    on_submit=ReflexAuthState.forgot_password,
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
forgot_password = forgot_password