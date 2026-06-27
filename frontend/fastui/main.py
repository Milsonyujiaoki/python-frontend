"""
FastUI Frontend Application for Barbershop SaaS.

This application uses FastUI to generate UI components from backend-defined JSON schemas.
The frontend automatically adapts to backend schema changes.
"""

from fastapi import FastAPI
from fastui import components as c
from fastui.components import display
from fastui.fastapi import fastui_app
from starlette.requests import Request
from starlette.responses import HTMLResponse

# Create FastAPI app
app = FastAPI(
    title="Barbershop SaaS - FastUI Frontend",
    description="API-driven UI for barbershop management",
    version="0.1.0",
)

# Mount FastUI app
app.mount("/api", fastui_app())


def get_nav_menu() -> list[c.Link]:
    """Get navigation menu items."""
    return [
        c.Link(
            label="Dashboard",
            on_click="/",
            active="/",
        ),
        c.Link(
            label="Customers",
            on_click="/customers",
            active="/customers",
        ),
        c.Link(
            label="Barbers",
            on_click="/barbers",
            active="/barbers",
        ),
        c.Link(
            label="Services",
            on_click="/services",
            active="/services",
        ),
        c.Link(
            label="Login",
            on_click="/login",
            active="/login",
        ),
    ]


def get_page_layout(body: list[c.AnyComponent]) -> list[c.AnyComponent]:
    """Get standard page layout with navigation."""
    return [
        c.PageHeader(
            title="BarberShop SaaS",
            title_event="/",
        ),
        c.Navbar(
            links=get_nav_menu(),
        ),
        c.Page(
            body=body,
        ),
    ]


@app.get("/api/", response_model=list[c.AnyComponent], response_model_exclude_none=True)
def api_dashboard():
    """Dashboard API endpoint."""
    return [
        c.Heading(text="Dashboard", level=2),
        c.Markdown(text="Welcome to the BarberShop SaaS management system."),
        c.Div(
            components=[
                c.Link(
                    label="Manage Customers",
                    on_click="/customers",
                    style={"fontSize": "1.2em"},
                ),
                c.Link(
                    label="Manage Barbers",
                    on_click="/barbers",
                    style={"fontSize": "1.2em"},
                ),
                c.Link(
                    label="Manage Services",
                    on_click="/services",
                    style={"fontSize": "1.2em"},
                ),
            ],
            style={"display": "flex", "gap": "20px", "marginTop": "20px"},
        ),
        c.Paragraph(text="Select an option above to get started."),
    ]


@app.get("/api/customers", response_model=list[c.AnyComponent], response_model_exclude_none=True)
def api_customers():
    """Customers list API endpoint."""
    return [
        c.Heading(text="Customers", level=2),
        c.Button(text="Add Customer", on_click="/customers/create"),
        c.Table(
            columns=[
                display.DisplayLookup(field="id", header="ID"),
                display.DisplayLookup(field="name", header="Name"),
                display.DisplayLookup(field="email", header="Email"),
                display.DisplayLookup(field="phone", header="Phone"),
            ],
            data=[
                {"id": 1, "name": "John Doe", "email": "john@example.com", "phone": "555-1234"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "555-5678"},
            ],
            data_url="/api/customers/data",
        ),
    ]


@app.get("/api/customers/data")
def api_customers_data():
    """Customers data endpoint for table."""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "phone": "555-1234"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "555-5678"},
    ]


@app.get("/api/barbers", response_model=list[c.AnyComponent], response_model_exclude_none=True)
def api_barbers():
    """Barbers list API endpoint."""
    return [
        c.Heading(text="Barbers", level=2),
        c.Button(text="Add Barber", on_click="/barbers/create"),
        c.Table(
            columns=[
                display.DisplayLookup(field="id", header="ID"),
                display.DisplayLookup(field="name", header="Name"),
                display.DisplayLookup(field="email", header="Email"),
                display.DisplayLookup(field="phone", header="Phone"),
                display.DisplayLookup(field="specialty", header="Specialty"),
            ],
            data=[
                {"id": 1, "name": "Mike Barber", "email": "mike@barbershop.com", "phone": "555-1111", "specialty": "Classic Cuts"},
                {"id": 2, "name": "Sarah Styles", "email": "sarah@barbershop.com", "phone": "555-2222", "specialty": "Modern Styles"},
            ],
            data_url="/api/barbers/data",
        ),
    ]


@app.get("/api/barbers/data")
def api_barbers_data():
    """Barbers data endpoint for table."""
    return [
        {"id": 1, "name": "Mike Barber", "email": "mike@barbershop.com", "phone": "555-1111", "specialty": "Classic Cuts"},
        {"id": 2, "name": "Sarah Styles", "email": "sarah@barbershop.com", "phone": "555-2222", "specialty": "Modern Styles"},
    ]


@app.get("/api/services", response_model=list[c.AnyComponent], response_model_exclude_none=True)
def api_services():
    """Services list API endpoint."""
    return [
        c.Heading(text="Services", level=2),
        c.Button(text="Add Service", on_click="/services/create"),
        c.Table(
            columns=[
                display.DisplayLookup(field="id", header="ID"),
                display.DisplayLookup(field="name", header="Name"),
                display.DisplayLookup(field="description", header="Description"),
                display.DisplayLookup(field="duration", header="Duration (min)"),
                display.DisplayLookup(field="price", header="Price"),
            ],
            data=[
                {"id": 1, "name": "Haircut", "description": "Standard haircut", "duration": 30, "price": 25.00},
                {"id": 2, "name": "Beard Trim", "description": "Beard shaping and trim", "duration": 20, "price": 15.00},
                {"id": 3, "name": "Full Service", "description": "Haircut + Beard Trim", "duration": 45, "price": 35.00},
            ],
            data_url="/api/services/data",
        ),
    ]


@app.get("/api/services/data")
def api_services_data():
    """Services data endpoint for table."""
    return [
        {"id": 1, "name": "Haircut", "description": "Standard haircut", "duration": 30, "price": 25.00},
        {"id": 2, "name": "Beard Trim", "description": "Beard shaping and trim", "duration": 20, "price": 15.00},
        {"id": 3, "name": "Full Service", "description": "Haircut + Beard Trim", "duration": 45, "price": 35.00},
    ]


@app.get("/api/login", response_model=list[c.AnyComponent], response_model_exclude_none=True)
def api_login():
    """Login page API endpoint."""
    return [
        c.Heading(text="Login", level=2),
        c.ModelForm(
            model={
                "title": "Login",
                "type": "object",
                "properties": {
                    "email": {"title": "Email", "type": "string", "format": "email"},
                    "password": {"title": "Password", "type": "string", "format": "password"},
                },
                "required": ["email", "password"],
            },
            submit_url="/api/login/submit",
            submit_method="POST",
            display_mode="inline",
        ),
    ]


@app.get("/{path:path}")
async def html_page() -> HTMLResponse:
    """Serve HTML page with FastUI prebuilt frontend."""
    from fastui import AnyComponent, prebuilt_html
    from starlette.responses import HTMLResponse

    return prebuilt_html(
        title="BarberShop SaaS - FastUI",
        api_url="/api",
    )