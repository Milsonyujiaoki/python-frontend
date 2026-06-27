import reflex as rx
from .state import ReflexAuthState
from .pages.auth import login_page, register_page, forgot_password_page
from .pages.dashboard import dashboard_page
from .pages.customers import customers_page
from .pages.barbers import barbers_page
from .pages.services import services_page

# Define the app
app = rx.App()

# Add pages
app.add_page(login_page, route="/login", title="Login - BarberShop")
app.add_page(register_page, route="/register", title="Register - BarberShop")
app.add_page(forgot_password_page, route="/forgot-password", title="Forgot Password - BarberShop")
app.add_page(dashboard_page, route="/", title="Dashboard - BarberShop")
app.add_page(customers_page, route="/customers", title="Customers - BarberShop")
app.add_page(barbers_page, route="/barbers", title="Barbers - BarberShop")
app.add_page(services_page, route="/services", title="Services - BarberShop")

if __name__ == "__main__":
    app.run()