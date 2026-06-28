# FastUI Development Patterns

This document provides guidance on developing with FastUI for the Barbershop SaaS application. FastUI is a Python framework for building frontends using JSON schemas defined on the backend.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Schema-Driven Development](#schema-driven-development)
4. [Component Patterns](#component-patterns)
5. [Form Handling](#form-handling)
6. [Data Tables](#data-tables)
7. [API Integration](#api-integration)
8. [Testing](#testing)
9. [Best Practices](#best-practices)

## Overview

FastUI follows a **backend-first** development approach where:
- UI components are defined by backend API schemas
- The frontend automatically adapts to schema changes
- Validation is handled both client-side and server-side
- No JavaScript/React knowledge required - pure Python

### Key Benefits

- **Rapid Development**: Define UI through Python schemas
- **Type Safety**: Automatic validation from Pydantic models
- **Consistent UX**: Standardized components across the application
- **Hot Reload**: Changes reflect immediately during development

## Project Structure

```
frontend/fastui/
├── main.py                 # FastAPI application with FastUI routes
├── requirements.txt        # Dependencies
├── pytest.ini             # Test configuration
├── components/            # Reusable UI component definitions
│   ├── __init__.py
│   ├── navigation.py      # Navigation bar, headers, footers
│   ├── tables.py          # Data tables with sorting/filtering
│   └── forms.py           # Form schemas and builders
├── services/              # API client services
│   ├── __init__.py
│   └── api_client.py      # HTTP client for API calls
├── utils/                 # Utility functions
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── unit/              # Unit tests for components
    │   ├── __init__.py
    │   └── test_components.py
    └── e2e/               # End-to-end tests
        ├── __init__.py
        ├── conftest.py
        └── test_pages.py
```

## Schema-Driven Development

### Basic API Endpoint Pattern

```python
from fastapi import FastAPI
from fastui import components as c

app = FastAPI()

@app.get("/api/my-page", response_model=list[c.AnyComponent])
def my_page():
    return [
        c.Heading(text="My Page", level=2),
        c.Paragraph(text="Content goes here"),
    ]
```

### Response Model

All FastUI endpoints should return `list[c.AnyComponent]` which allows the framework to render multiple components in sequence.

### Component Types

FastUI provides these core components:

| Component | Purpose |
|-----------|---------|
| `Heading` | Page/section titles |
| `Paragraph` | Text content |
| `Markdown` | Formatted text |
| `Table` | Data tables |
| `TablePaginated` | Tables with pagination |
| `ModelForm` | Forms from JSON schema |
| `Button` | Clickable buttons |
| `Link` | Navigation links |
| `Navbar` | Top navigation bar |
| `PageHeader` | Page header |
| `Footer` | Page footer |
| `Div` | Container with styling |
| `Image` | Image display |
| `Video` | Video playback |

## Component Patterns

### Navigation Component

```python
from fastui import components as c

def get_nav_links():
    return [
        c.Link(label="Dashboard", on_click="/", active="/"),
        c.Link(label="Customers", on_click="/customers", active="/customers"),
        c.Link(label="Barbers", on on_click="/barbers", active="/barbers"),
    ]

@app.get("/api/layout")
def layout():
    return [
        c.PageHeader(title="My App"),
        c.Navbar(links=get_nav_links()),
        # Page content here
    ]
```

### Page Layout Pattern

```python
from fastui import components as c
from typing import List

def create_page_layout(
    title: str,
    body: List[c.AnyComponent],
    include_nav: bool = True
) -> List[c.AnyComponent]:
    """Create consistent page layout."""
    components = [
        c.PageHeader(title=title),
    ]

    if include_nav:
        components.append(c.Navbar(links=get_nav_links()))

    components.append(c.Page(body=body))
    return components
```

### Loading States

```python
@app.get("/api/data-page")
def data_page():
    return [
        c.Heading(text="Data"),
        c.Paragraph(text="Loading..."),
        # In production, data would be fetched via data_url
        c.Table(
            columns=[...],
            data_url="/api/data/fetch",
        ),
    ]
```

## Form Handling

### Simple Form

```python
from fastui import components as c

@app.get("/api/login")
def login_page():
    return [
        c.Heading(text="Login"),
        c.ModelForm(
            model={
                "title": "LoginForm",
                "type": "object",
                "properties": {
                    "email": {"title": "Email", "type": "string", "format": "email"},
                    "password": {"title": "Password", "type": "string", "format": "password"},
                },
                "required": ["email", "password"],
            },
            submit_url="/api/login/submit",
            submit_method="POST",
        ),
    ]

@app.post("/api/login/submit")
def login_submit(form_data: dict):
    # Process form data
    return {"success": True}
```

### Form with Pydantic

```python
from pydantic import BaseModel, EmailStr

class CustomerForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    notes: str = ""

@app.get("/api/customers/create")
def create_customer_form():
    return [
        c.Heading(text="New Customer"),
        c.ModelForm(
            model=CustomerForm.model_json_schema(),
            submit_url="/api/customers",
            submit_method="POST",
        ),
    ]
```

### Form Validation Errors

```python
from fastui import components as c
from fastapi import Form

@app.post("/api/customers")
def create_customer(
    name: str = Form(...),
    email: str = Form(...),
):
    # Validate
    if not is_valid_email(email):
        return [
            c.Heading(text="New Customer"),
            c.ModelForm(
                model=...,
                submit_url="/api/customers",
                initial={"name": name, "email": email},
                # FastUI will show errors from response
            ),
        ], 422

    # Success - redirect
    return c.PageEvent(
        name="redirect",
        context={"url": "/customers"},
    )
```

## Data Tables

### Simple Table

```python
from fastui.components import display

@app.get("/api/customers")
def customers_page():
    return [
        c.Heading(text="Customers"),
        c.Button(text="Add Customer", on_click="/api/customers/create"),
        c.Table(
            columns=[
                display.DisplayLookup(field="id", header="ID"),
                display.DisplayLookup(field="name", header="Name"),
                display.DisplayLookup(field="email", header="Email"),
                display.DisplayLookup(field="phone", header="Phone"),
            ],
            data=[
                {"id": 1, "name": "John", "email": "john@example.com"},
                {"id": 2, "name": "Jane", "email": "jane@example.com"},
            ],
        ),
    ]
```

### Server-Side Data

```python
@app.get("/api/customers")
def customers_page():
    return [
        c.Heading(text="Customers"),
        c.Table(
            columns=CUSTOMER_COLUMNS,
            data_url="/api/customers/data",
            # FastUI automatically fetches data and handles pagination
        ),
    ]

@app.get("/api/customers/data")
def customers_data():
    return db.get_all_customers()
```

### Table with Actions

```python
from fastui.components import display

CUSTOMER_COLUMNS = [
    display.DisplayLookup(field="id", header="ID"),
    display.DisplayLookup(field="name", header="Name"),
    display.DisplayLookup(
        field="name",
        header="Actions",
        mode="link",
        on_click="/api/customers/{id}/edit",
    ),
]
```

## API Integration

### API Client Pattern

```python
import httpx

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url

    async def get(self, endpoint: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()

api_client = APIClient()
```

### CRUD Operations

```python
async def fetch_customers():
    return await api_client.get("/customers")

async def create_customer(data: dict):
    return await api_client.post("/customers", data)

async def update_customer(customer_id: int, data: dict):
    return await api_client.put(f"/customers/{customer_id}", data)

async def delete_customer(customer_id: int):
    return await api_client.delete(f"/customers/{customer_id}")
```

## Testing

### Unit Testing Components

```python
import pytest
from fastui import components as c

def test_navigation_component():
    nav = c.Navbar(
        links=[c.Link(label="Home", on_click="/")],
        brand_text="My App",
    )
    assert nav.brand_text == "My App"
    assert len(nav.links) == 1
```

### E2E Testing with Playwright

```python
import pytest
from playwright.async_api import expect

@pytest.mark.e2e
async def test_dashboard_loads(page):
    await page.goto("http://localhost:8000/")
    await expect(page.locator("h2:has-text('Dashboard')")).to_be_visible()

@pytest.mark.e2e
async def test_create_customer(page):
    await page.goto("http://localhost:8000/customers")
    await page.click("button:has-text('Add Customer')")

    await page.fill('input[name="name"]', "Test User")
    await page.fill('input[name="email"]', "test@example.com")
    await page.click('button[type="submit"]')

    await expect(page.locator("text=Test User")).to_be_visible()
```

### Test Fixtures

```python
# conftest.py
import pytest
from playwright.async_api import async_playwright

@pytest.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()
```

## Best Practices

### Schema Organization

1. **Keep schemas in separate files**: Define form schemas in `components/forms.py`
2. **Reuse schemas**: Create shared column definitions for tables
3. **Type hints**: Use Pydantic models for type safety

### Performance

1. **Use data_url for large tables**: Let FastUI handle pagination
2. **Debounce search inputs**: Use `debounce` prop on Input components
3. **Lazy load data**: Fetch data on demand, not upfront

### Error Handling

1. **Return proper status codes**: 422 for validation errors
2. **Include error messages**: FastUI displays them automatically
3. **Graceful degradation**: Show user-friendly messages

### Accessibility

1. **Use semantic components**: Heading levels, proper labels
2. **Add aria attributes**: When needed for custom components
3. **Keyboard navigation**: Test with keyboard only

## Running the Application

### Development

```bash
# Install dependencies
pip install -r frontend/fastui/requirements.txt

# Run with uvicorn
uvicorn frontend.fastui.main:app --reload --port 8000
```

### Testing

```bash
# Run unit tests
pytest frontend/fastui/tests/unit -v

# Run E2E tests (requires running app)
pytest frontend/fastui/tests/e2e -v -m e2e
```

## Troubleshooting

### Common Issues

**Schema validation errors:**
- Ensure response_model is `list[c.AnyComponent]`
- Use `response_model_exclude_none=True` if needed

**Form not submitting:**
- Check `submit_url` is correct
- Ensure `submit_method` matches backend route

**Table not showing data:**
- Verify `data_url` endpoint returns array
- Check column `field` names match data keys

## Resources

- [FastUI Documentation](https://fastui.tiangolo.com/)
- [FastUI GitHub](https://github.com/pydantic/FastUI)
- [Pydantic Documentation](https://docs.pydantic.dev/)