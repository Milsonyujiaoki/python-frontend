# Solara Development Patterns

This document provides guidance on developing with Solara for the Barbershop SaaS application. It covers common patterns, best practices, and performance optimizations specific to Solara.

## Table of Contents

1. [Project Structure](#project-structure)
2. [State Management](#state-management)
3. [Component Patterns](#component-patterns)
4. [Data Fetching](#data-fetching)
5. [Performance Optimization](#performance-optimization)
6. [Testing](#testing)
7. [Common Patterns](#common-patterns)

## Project Structure

```
frontend/solara/
├── main.py                 # Application entry point and routing
├── components/             # Reusable UI components
│   ├── base_table.py       # Generic paginated table
│   ├── base_form.py        # Generic form component
│   ├── customer_table.py   # Customer-specific table
│   ├── barber_table.py     # Barber-specific table
│   ├── service_table.py    # Service-specific table
│   └── visualization.py    # Charts and analytics
├── pages/                  # Page components (routes)
│   ├── login.py
│   ├── register.py
│   ├── customers.py
│   ├── barbers.py
│   └── services.py
├── state/                  # State management modules
│   ├── customer_state.py
│   ├── barber_state.py
│   └── service_state.py
├── services/               # API and external services
│   └── api_service.py      # HTTP client with caching
├── utils/                  # Utility functions
│   └── data_cache.py       # Caching and memoization
└── tests/                  # Test suites
    ├── unit/               # Unit tests
    └── e2e/                # End-to-end tests
```

## State Management

### Reactive Variables

Solara uses reactive variables for state management. Always use `solara.reactive()` for state that should trigger re-renders:

```python
import solara

# Good: Reactive state
customers = solara.reactive([])
loading = solara.reactive(False)

# Access value with .value
def get_customer_count():
    return len(customers.value)

# Update value with .value assignment
def add_customer(customer):
    customers.value = [*customers.value, customer]
```

### State with Memoization

For computed state that depends on other state, use `@solara.memoize`:

```python
@solara.memoize
def get_filtered_customers():
    """Filters are applied here, result is cached until dependencies change."""
    if not search_query.value:
        return customers.value
    
    query = search_query.value.lower()
    return [
        c for c in customers.value
        if query in c.get("name", "").lower()
    ]
```

### Pagination State

For large datasets, maintain pagination state separately:

```python
current_page = solara.reactive(0)
page_size = solara.reactive(10)

@solara.memoize
def get_paginated_items():
    filtered = get_filtered_customers()
    start = current_page.value * page_size.value
    end = start + page_size.value
    return filtered[start:end]
```

## Component Patterns

### Basic Component

```python
import solara

@solara.component
def CustomerCard(customer: dict):
    """Display a single customer card."""
    return solara.Card(
        title=customer.get("name", "Unknown"),
        children=[
            solara.Markdown(f"**Email:** {customer.get('email')}"),
            solara.Markdown(f"**Phone:** {customer.get('phone')}"),
        ]
    )
```

### Component with State

```python
import solara

@solara.component
def SearchableTable(items, columns):
    """Table with built-in search functionality."""
    search_query, set_search_query = solara.use_state("")
    
    @solara.memoize
    def filtered_items():
        if not search_query:
            return items
        query = search_query.lower()
        return [i for i in items if query in str(i.values()).lower()]
    
    return solara.Column([
        solara.InputText(
            label="Search",
            value=search_query,
            on_value=set_search_query,
        ),
        Table(data=filtered_items(), columns=columns),
    ])
```

### Component with Effects

```python
import solara

@solara.component
def DataFetcher(endpoint):
    """Component that fetches data on mount."""
    data, set_data = solara.use_state(None)
    loading, set_loading = solara.use_state(False)
    error, set_error = solara.use_state(None)
    
    async def fetch_data():
        set_loading(True)
        try:
            response = await api.get(endpoint)
            set_data(response.json())
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)
    
    # Fetch on mount and when endpoint changes
    solara.use_effect(
        lambda: fetch_data(),
        [endpoint]
    )
    
    if loading:
        return solara.ProgressCircular()
    if error:
        return solara.ErrorBanner(error)
    
    return DataTable(data=data)
```

## Data Fetching

### API Service Pattern

Use the centralized API service for all data fetching:

```python
from services.api_service import use_api_data

@solara.component
def CustomersPage():
    # use_api_data returns: (data, loading, error, refresh)
    customers, loading, error, refresh = use_api_data(
        endpoint="/customers",
        cache_key="customers_list",
        ttl=300,  # 5 minute cache
    )
    
    if loading:
        return solara.ProgressLinear()
    if error:
        return solara.ErrorBanner(error)
    
    return CustomerTable(items=customers)
```

### Optimistic Updates

For better UX, update state immediately and sync with backend:

```python
def delete_customer(customer_id):
    # Optimistic update - remove from UI immediately
    customers.value = [c for c in customers.value if c.get("id") != customer_id]
    
    # Invalidate cache to force refresh on next fetch
    api_service.invalidate("/customers")
    
    # Optionally: make actual API call
    # await api.delete(f"/customers/{customer_id}")
```

## Performance Optimization

### LRU Cache for Expensive Computations

```python
from utils.data_cache import LRUCache, cached_computation

# Global cache instance
computed_cache = LRUCache(max_size=100, ttl=60)

def get_expensive_report():
    return cached_computation(
        key="monthly_report",
        compute_fn=lambda: generate_report(),  # Expensive operation
    )
```

### Debounced Search

```python
import asyncio
import solara

@solara.component
def DebouncedSearch(on_search):
    """Search input with debouncing to avoid excessive filtering."""
    search_query, set_search_query = solara.use_state("")
    timer, set_timer = solara.use_state(None)
    
    def schedule_search():
        if timer:
            timer.cancel()
        
        async def do_search():
            await asyncio.sleep(0.3)  # 300ms debounce
            on_search(search_query)
        
        new_timer = asyncio.create_task(do_search())
        set_timer(new_timer)
    
    return solara.InputText(
        label="Search",
        value=search_query,
        on_value=lambda v: (set_search_query(v), schedule_search()),
    )
```

### Virtual Scrolling for Large Lists

For very large datasets (1000+ items), consider virtual scrolling:

```python
@solara.component
def VirtualList(items, item_height=50, visible_height=400):
    """Render only visible items for large lists."""
    scroll_position, set_scroll_position = solara.use_state(0)
    
    visible_start = scroll_position // item_height
    visible_count = visible_height // item_height + 1
    visible_items = items[visible_start:visible_start + visible_count]
    
    return solara.Column([
        solara.Div(style={"height": f"{len(items) * item_height}px"}),
        # Render only visible items with absolute positioning
        *[
            solara.Div(
                children=[ItemComponent(item)],
                style={
                    "position": "absolute",
                    "top": f"{i * item_height}px",
                    "height": f"{item_height}px",
                }
            )
            for i, item in enumerate(visible_items, start=visible_start)
        ],
    ])
```

## Testing

### Unit Testing Components

```python
import solara
import pytest
from solara.test import TestClient
from components.customer_table import CustomerTable

def test_customer_table_renders():
    """Test that customer table renders correctly."""
    
    @solara.component
    def TestApp():
        return CustomerTable()
    
    client = TestClient(TestApp)
    page = client.get("/")
    
    assert page.status_code == 200
    assert "Customers" in page.content.decode()
```

### Testing State Management

```python
def test_customer_state_add():
    """Test adding a customer to state."""
    from customer_state import customers, add_customer, get_customer_by_id
    
    # Initial state
    initial_count = len(customers.value)
    
    # Add customer
    add_customer({"name": "Test User", "email": "test@example.com"})
    
    # Verify
    assert len(customers.value) == initial_count + 1
    assert get_customer_by_id(customers.value[-1]["id"]) is not None
```

### End-to-End Testing

See `tests/e2e/` for Playwright-based E2E tests:

```python
# tests/e2e/test_customers.py
@pytest.mark.e2e
async def test_create_customer(page, authenticated_user):
    """Test creating a new customer through the UI."""
    await page.goto("/customers")
    await page.click("text=Add Customer")
    
    await page.fill('input[name="name"]', "John Doe")
    await page.fill('input[name="email"]', "john@example.com")
    await page.click("button:has-text('Save')")
    
    await expect(page.locator("text=John Doe")).to_be_visible()
```

## Common Patterns

### Form with Validation

```python
@solara.component
def CustomerForm(customer_id=None, on_save=None):
    """Form for creating/editing customers with validation."""
    name, set_name = solara.use_state("")
    email, set_email = solara.use_state("")
    phone, set_phone = solara.use_state("")
    errors, set_errors = solara.use_state({})
    
    def validate():
        errors = {}
        if not name.strip():
            errors["name"] = "Name is required"
        if not email or "@" not in email:
            errors["email"] = "Valid email is required"
        return errors
    
    def handle_save():
        validation_errors = validate()
        if validation_errors:
            set_errors(validation_errors)
            return
        
        customer_data = {"name": name, "email": email, "phone": phone}
        if on_save:
            on_save(customer_data)
    
    return solara.Column([
        solara.InputText(
            label="Name",
            value=name,
            on_value=set_name,
            error="name" in errors,
            helper_text=errors.get("name"),
        ),
        solara.InputText(
            label="Email",
            value=email,
            on_value=set_email,
            error="email" in errors,
            helper_text=errors.get("email"),
        ),
        solara.InputText(
            label="Phone",
            value=phone,
            on_value=set_phone,
        ),
        solara.Button(
            label="Save Customer",
            on_click=handle_save,
            color="primary",
        ),
    ])
```

### Modal Dialog

```python
@solara.component
def ConfirmDialog(title, message, on_confirm, on_cancel):
    """Reusable confirmation dialog."""
    return solara.Column([
        solara.Markdown(f"## {title}"),
        solara.Markdown(message),
        solara.Row([
            solara.Button(
                label="Cancel",
                on_click=on_cancel,
                text=True,
            ),
            solara.Button(
                label="Confirm",
                on_click=on_confirm,
                color="error",
            ),
        ], justify="end"),
    ])
```

### Loading States

```python
@solara.component
def LoadingWrapper(loading, error, children):
    """Wrapper component for consistent loading/error states."""
    if loading:
        return solara.Column([
            solara.ProgressCircular(),
            solara.Markdown("*Loading...*"),
        ], align="center")
    
    if error:
        return solara.ErrorBanner(
            error,
            on_close=lambda: None,
        )
    
    return children
```

Jupyter Notebook Integration

### Running Solara in Jupyter

```python
# In a Jupyter notebook cell:
import solara
import solara.lab

@solara.component
def NotebookDashboard():
    counter, set_counter = solara.use_state(0)
    return solara.Column([
        solara.Markdown(f"# Counter: {counter}"),
        solara.Button(
            label="Increment",
            on_click=lambda: set_counter(counter + 1),
        ),
    ])

# Display in notebook
NotebookDashboard()
```

### Exporting to Standalone App

```bash
# Convert notebook to standalone app
solara run my_notebook.ipynb

# Or build for production
solara build my_notebook.ipynb --output-dir=dist
```

## Deployment

### Development Server

```bash
# Start development server with hot reload
solara run frontend/solara/main.py --port 8080
```

### Production Build

```bash
# Build for production
solara build frontend/solara/main.py --output-dir=dist

# Serve production build
uvicorn dist.server:app --host 0.0.0.0 --port 8080
```

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/solara/ ./frontend/solara/

EXPOSE 8080

CMD ["solara", "run", "frontend/solara/main.py", "--port", "8080", "--host", "0.0.0.0"]
```

## Troubleshooting

### Common Issues

**State not updating UI:**
- Ensure you're using `solara.reactive()` for state
- Access state with `.value`
- Create new lists/objects when updating (don't mutate in place)

**Slow rendering with large datasets:**
- Use `@solara.memoize` for computed values
- Implement pagination
- Consider virtual scrolling for 1000+ items

**API calls on every render:**
- Wrap API calls in `solara.use_effect()`
- Use the `use_api_data` hook for automatic caching

**Circular imports:**
- Use dynamic imports inside components
- Move shared utilities to separate modules

## Resources

- [Solara Documentation](https://solara.dev/documentation)
- [Solara GitHub](https://github.com/widgetti/solara)
- [Reacton (Solara's underlying library)](https://reacton.readthedocs.io/)
- [ipywidgets (for custom components)](https://ipywidgets.readthedocs.io/)