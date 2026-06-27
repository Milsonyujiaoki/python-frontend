import reflex as rx
from state import ReflexAuthState

def navbar() -> rx.Component:
    """Responsive navigation bar component."""
    return rx.box(
        rx.hstack(
            rx.link(
                rx.image(
                    src="/logo.png",
                    height=["2rem", "2.5rem", "3rem"],  # Responsive height
                    width="auto",
                    alt="BarberShop Logo",
                ),
                href="/",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    "Dashboard",
                    href="/",
                    _hover={"color": "#6366f1"},
                    padding_x=[ "0.5em", "0.75em", "1em" ],  # Responsive padding
                ),
                rx.link(
                    "Customers",
                    href="/customers",
                    _hover={"color": "#6366f1"},
                    padding_x=[ "0.5em", "0.75em", "1em" ],
                ),
                rx.link(
                    "Barbers",
                    href="/barbers",
                    _hover={"color": "#6366f1"},
                    padding_x=[ "0.5em", "0.75em", "1em" ],
                ),
                rx.link(
                    "Services",
                    href="/services",
                    _hover={"color": "#6366f1"},
                    padding_x=[ "0.5em", "0.75em", "1em" ],
                ),
                rx.button(
                    "Logout",
                    on_click=ReflexAuthState.logout,
                    color_scheme="red",
                    variant="soft",
                    size=["sm", "sm", "md"],  # Responsive button size
                ),
                rx.color_button(position="left"),
                spacing=["2", "3", "4"],  # Responsive spacing
                wrap="wrap",  # Allow wrapping on small screens
                justify="center",
                align="center",
            ),
            align="center",
            width="100%",
            padding=["1rem", "1.5rem", "2rem"],  # Responsive padding
            border_bottom="1px solid #e5e7eb",
        ),
        width="100%",
        # Ensure minimum touch target height
        min_height=["3.5rem", "4rem", "4.5rem"],
    )


def layout(child: rx.Component) -> rx.Component:
    """Layout wrapper for pages with responsive design."""
    return rx.vstack(
        navbar(),
        rx.box(
            child,
            padding=[ "1em", "1.5em", "2em" ],  # Responsive padding
            width="100%",
            max_width="1200px",
            margin_x="auto",  # Center horizontally
            flex="1",
        ),
        spacing="0",
        width="100%",
        min_height="100vh",
        # Ensure responsive spacing
        padding_y=[ "0.5em", "1em", "1.5em" ],
    )