"""Main application component for Solara frontend."""

import solara
from .pages.login import LoginPage
from .pages.register import RegisterPage
from .pages.forgot_password import ForgotPasswordPage
from .pages.customers import CustomersPage
from .pages.barbers import BarbersPage
from .pages.services import ServicesPage

# Placeholder for dashboard page
@solara.component
def DashboardPage():
    # Import state modules
    from .customer_state import customers
    from .barber_state import barbers
    from .service_state import services

    # Get counts
    customer_count = len(customers.value)
    barber_count = len(barbers.value)
    service_count = len(services.value)

    return solara.Column([
        solara.Markdown("# Dashboard"),
        solara.Markdown("Welcome to the BarberShop dashboard!"),
        solara.Row(
            style={"margin": "20px 0", "justify": "space-around"},
            children=[
                solara.Card(
                    title="Customers",
                    children=[
                        solara.Markdown(f"# {customer_count}"),
                        solara.Markdown("Total customers"),
                    ],
                    style={"padding": "20px", "width": "200px", "textAlign": "center"},
                    elevation=1,
                ),
                solara.Card(
                    title="Barbers",
                    children=[
                        solara.Markdown(f"# {barber_count}"),
                        solara.Markdown("Total barbers"),
                    ],
                    style={"padding": "20px", "width": "200px", "textAlign": "center"},
                    elevation=1,
                ),
                solara.Card(
                    title="Services",
                    children=[
                        solara.Markdown(f"# {service_count}"),
                        solara.Markdown("Total services"),
                    ],
                    style={"padding": "20px", "width": "200px", "textAlign": "center"},
                    elevation=1,
                ),
            ]
        ),
        solara.Markdown("## Recent Activity"),
        solara.Markdown("*(This section would show recent actions like new customers, appointments, etc.)*"),
    ])

# Define routes
routes = {
    "/": DashboardPage,
    "/login": LoginPage,
    "/register": RegisterPage,
    "/forgot-password": ForgotPasswordPage,
    "/customers": CustomersPage,
    "/barbers": BarbersPage,
    "/services": ServicesPage,
}

@solara.component
def NotFoundPage():
    return solara.Column([
        solara.Markdown("# 404: Page Not Found"),
        solara.Link(label="Go to home", href="/"),
    ])

@solara.component
def MainLayout():
    # Route state
    pathname, set_pathname = solara.use_state("/")

    # Navigation handler
    def navigate_to(path):
        set_pathname(path)

    # Get the component for the current path, or 404 if not found
    PageComponent = routes.get(pathname, NotFoundPage)

    return solara.Column([
        # Header
        solara.AppBar(
            title="BarberShop",
            elevation=True,
            background_color="#1976d2",
            text_color="#ffffff",
        ),
        # Navigation buttons
        solara.Row(
            justify="space-around",
            style={"margin": "10px 0"},
            children=[
                solara.Button(label="Dashboard", on_click=lambda: navigate_to("/"), text=True),
                solara.Button(label="Login", on_click=lambda: navigate_to("/login"), text=True),
                solara.Button(label="Register", on_click=lambda: navigate_to("/register"), text=True),
                solara.Button(label="Forgot Password", on_click=lambda: navigate_to("/forgot-password"), text=True),
                solara.Button(label="Customers", on_click=lambda: navigate_to("/customers"), text=True),
                solara.Button(label="Barbers", on_click=lambda: navigate_to("/barbers"), text=True),
                solara.Button(label="Services", on_click=lambda: navigate_to("/services"), text=True),
            ]
        ),
        # Main content
        solara.Column(
            style={"padding": "20px"},
            children=[
                # Here we render the current page component
                PageComponent()
            ]
        )
    ])

# Set the main component
def main():
    return MainLayout