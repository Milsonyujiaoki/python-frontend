"""BarberShop Reflex App - Main application file."""
import reflex as rx
import sys
import os

# Add the reflex directory to the path so we can import from it
REFLEX_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, REFLEX_DIR)

from state import ReflexAuthState
from pages.auth import login_page, register_page, forgot_password_page
from pages.dashboard import dashboard_page
from pages.customers import customers_page
from pages.barbers import barbers_page
from pages.services import services_page


class BarberShopState(ReflexAuthState):
    """The app state inheriting from custom auth state."""
    pass


def index() -> rx.Component:
    """Redirect root to dashboard."""
    return rx.redirect("/")


app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="blue",
    ),
)
app.add_page(login_page, route="/login", title="Login - BarberShop")
app.add_page(register_page, route="/register", title="Register - BarberShop")
app.add_page(forgot_password_page, route="/forgot-password", title="Forgot Password - BarberShop")
app.add_page(dashboard_page, route="/", title="Dashboard - BarberShop")
app.add_page(customers_page, route="/customers", title="Customers - BarberShop")
app.add_page(barbers_page, route="/barbers", title="Barbers - BarberShop")
app.add_page(services_page, route="/services", title="Services - BarberShop")