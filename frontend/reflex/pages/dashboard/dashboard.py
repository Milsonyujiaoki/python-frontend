import reflex as rx
from state import ReflexAuthState
from components.nav import layout


def dashboard_page() -> rx.Component:
    """Dashboard page component."""
    return layout(
        rx.container(
            rx.cond(
                ReflexAuthState.is_authenticated,
                rx.vstack(
                    rx.heading("BarberShop Dashboard", size="xl"),
                    rx.grid(
                        rx.card(
                            rx.vstack(
                                rx.icon("users", size=48),
                                rx.heading("Customers", size="md"),
                                rx.text("Manage your customers", color="gray"),
                                rx.button(
                                    "View Customers",
                                    href="/customers",
                                    color_scheme="blue",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.icon("users", size=48),
                                rx.heading("Barbers", size="md"),
                                rx.text("Manage your barbers", color="gray"),
                                rx.button(
                                    "View Barbers",
                                    href="/barbers",
                                    color_scheme="green",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.icon("sparkles", size=48),
                                rx.heading("Services", size="md"),
                                rx.text("Manage your services", color="gray"),
                                rx.button(
                                    "View Services",
                                    href="/services",
                                    color_scheme="purple",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            width="100%",
                        ),
                        columns=[1, 2, 3],
                        spacing="4",
                        width="100%",
                    ),
                    rx.spacer(),
                    rx.center(
                        rx.badge(
                            f"Logged in as: {ReflexAuthState.current_user.get('email', 'User')}",
                            color_scheme="green"
                        )
                    ),
                    spacing="5",
                    justify="center",
                    min_height="85vh",
                ),
                rx.redirect("/login")
            ),
        )
    )


# Export for import in main.py
dashboard = dashboard_page