# Streamlit Frontend Development Patterns

## Overview

This document provides comprehensive guidance for developing with the Streamlit frontend in the BarberShop SaaS application. Streamlit offers rapid prototyping capabilities with minimal boilerplate, making it ideal for data-centric applications and quick iterations.

## Architecture

```
frontend/streamlit/
├── main.py                 # Main application entry point
├── pages/                  # Multi-page application structure
│   ├── login.py           # Authentication page
│   ├── customers.py       # Customer management
│   ├── barbers.py         # Barber management
│   └── services.py        # Service management
├── components/             # Reusable UI components
│   ├── sidebar.py         # Navigation sidebar
│   ├── dashboard.py       # Dashboard widgets
│   ├── base_table.py      # Reusable table component
│   ├── base_form.py       # Reusable form component
│   └── visualization.py   # Charts and analytics
├── services/               # Business logic layer
│   └── api_client.py      # API communication
├── utils/                  # Utility functions
│   └── session_state.py   # Session state management
└── tests/                  # Test suite
    ├── unit/              # Unit tests
    └── e2e/               # End-to-end tests
```

## Session State Management

Streamlit reruns the entire script on every interaction. Session state persists data across reruns.

### Initialization Pattern

```python
# utils/session_state.py
import streamlit as st

def initialize_session_state():
    """Initialize all session state variables with defaults."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "customers" not in st.session_state:
        st.session_state.customers = []
    if "barbers" not in st.session_state:
        st.session_state.barbers = []
    if "services" not in st.session_state:
        st.session_state.services = []
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "search": "",
            "status": "All",
            "category": "All",
        }
```

### State Accessors Pattern

```python
# Getters
def get_customers():
    """Get customers from session state."""
    return st.session_state.get("customers", [])

def get_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)

# Setters
def set_customers(customers: list):
    """Set customers in session state."""
    st.session_state.customers = customers

def set_authenticated(value: bool):
    """Set authentication status."""
    st.session_state.authenticated = value
```

### Best Practices

1. **Always check before setting**: Use `if "key" not in st.session_state` to avoid overwriting
2. **Centralize initialization**: Call `initialize_session_state()` at app startup
3. **Use accessors**: Encapsulate state access in getter/setter functions
4. **Minimize state**: Only store what's needed across reruns
5. **Clear on logout**: Reset all state when user logs out

## Component Patterns

### Sidebar Navigation

```python
# components/sidebar.py
def render_sidebar():
    """Render navigation sidebar with pages and quick actions."""
    with st.sidebar:
        st.title("✂️ BarberShop")

        # Navigation
        page = st.radio(
            "Go to",
            ["🏠 Dashboard", "👥 Customers", "💈 Barbers", "💇 Services"],
            label_visibility="collapsed",
        )

        # Handle navigation with st.switch_page
        if page == "🏠 Dashboard":
            st.switch_page("main.py")
        elif page == "👥 Customers":
            st.switch_page("pages/customers.py")
```

### Data Tables

```python
# components/base_table.py
import pandas as pd
import streamlit as st

def render_table(
    data: list[dict],
    columns: list[str] = None,
    column_config: dict = None,
    hide_index: bool = True,
):
    """Render a data table with configuration."""
    if not data:
        st.info("No data available")
        return

    df = pd.DataFrame(data)
    st.dataframe(
        df,
        column_config=column_config,
        hide_index=hide_index,
        use_container_width=True,
    )
```

### Forms

```python
# components/base_form.py
def render_form(
    form_key: str,
    fields: list[dict],
    submit_label: str = "Save",
    on_submit: callable = None,
):
    """Render a configurable form."""
    with st.form(form_key):
        values = {}

        for field in fields:
            if field["type"] == "text":
                values[field["key"]] = st.text_input(
                    field["label"],
                    required=field.get("required", False),
                )
            elif field["type"] == "email":
                values[field["key"]] = st.text_input(
                    field["label"],
                    type="email",
                )

        submitted = st.form_submit_button(submit_label)

        if submitted and on_submit:
            on_submit(values)
```

### Visualizations

```python
# components/visualization.py
import plotly.express as px

def render_line_chart(data: pd.DataFrame, x: str, y: str, title: str):
    """Render a line chart."""
    fig = px.line(data, x=x, y=y, markers=True, title=title)
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

def render_metric_cards(metrics: list[dict]):
    """Render row of metric cards."""
    cols = st.columns(len(metrics))
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=metric["label"],
                value=metric["value"],
                delta=metric.get("delta"),
            )
```

## Data Fetching

### API Client Pattern

```python
# services/api_client.py
import httpx

class APIClient:
    """HTTP client for backend API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0

    async def _request(self, method: str, endpoint: str, data: dict = None):
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def get_customers(self) -> list[dict]:
        """Fetch all customers."""
        return await self._request("GET", "/api/customers")
```

### Caching Pattern

```python
# utils/cache.py
import streamlit as st
from functools import wraps

@st.cache_data(ttl=300)
def fetch_customers_cached(api_client: APIClient) -> list[dict]:
    """Fetch customers with caching."""
    return api_client.get_customers()

@st.cache_resource
def get_api_client() -> APIClient:
    """Get singleton API client."""
    return APIClient()
```

## Performance Optimization

### Caching Strategies

```python
# st.cache_data - For data that can be cached across sessions
@st.cache_data
def load_large_dataset():
    return pd.read_csv("large_file.csv")

# st.cache_resource - For connections and resources
@st.cache_resource
def get_database_connection():
    return create_connection()

# st.experimental_memo - Deprecated, use cache_data instead
```

### Lazy Loading

```python
# Load data only when needed
if st.session_state.get("show_customers", False):
    customers = load_customers()
    render_customer_table(customers)
```

### Rerun Optimization

```python
# Use st.rerun() strategically
if form_submitted:
    if valid:
        save_data()
        st.success("Saved!")
        st.rerun()  # Refresh to show changes
    else:
        st.error("Invalid data")  # No rerun needed
```

## Testing

### Unit Tests

```python
# tests/unit/test_components.py
import pytest
from unittest.mock import patch

def test_render_table_with_data():
    """Test table renders with data."""
    from components.base_table import render_table

    data = [{"name": "John", "age": 30}]

    with patch("streamlit.dataframe") as mock_df:
        render_table(data)
        mock_df.assert_called_once()

def test_session_state_getters():
    """Test session state getter functions."""
    from utils.session_state import get_customers

    mock_state = {"customers": [{"id": 1, "name": "Test"}]}

    with patch("streamlit.session_state", mock_state):
        result = get_customers()
        assert len(result) == 1
```

### E2E Tests

```python
# tests/e2e/test_streamlit_app.py
import pytest
from playwright.sync_api import Page, expect

def test_home_page_loads(page: Page, base_url: str):
    """Test that home page loads."""
    response = page.goto(base_url)
    assert response.status == 200
    expect(page).to_have_title("BarberShop SaaS")

def test_login_form_submission(page: Page, base_url: str):
    """Test login form submission."""
    page.goto(f"{base_url}/login")

    page.locator("input[type='text']").fill("admin@example.com")
    page.locator("input[type='password']").fill("password")
    page.locator("button[type='submit']").click()

    expect(page.locator("sidebar")).to_contain_text("admin@example.com")
```

### Pytest Configuration

```python
# conftest.py
import pytest

@pytest.fixture
def mock_session_state():
    """Mock session state for testing."""
    mock_state = {}
    with patch("streamlit.session_state", mock_state):
        yield mock_state

@pytest.fixture
def sample_customers():
    """Sample customer data."""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
    ]
```

## Multi-Page Application

### Page Structure

```python
# pages/customers.py
import streamlit as st
from components.sidebar import render_sidebar
from utils.session_state import get_customers

st.set_page_config(page_title="Customers", page_icon="👥")
render_sidebar()

def render_customers():
    st.title("👥 Customers")
    customers = get_customers()
    # Render content
```

### Page Navigation

```python
# Using st.switch_page (Streamlit 1.23+)
st.switch_page("pages/customers.py")
st.switch_page("pages/barbers.py")

# Conditional navigation
if not st.session_state.authenticated:
    st.switch_page("pages/login.py")
```

## File Upload/Download

### Upload Pattern

```python
# File upload component
uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    help="Upload customer data"
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(f"Uploaded {len(df)} rows")
    # Process data
```

### Download Pattern

```python
# File download component
@st.cache_data
def convert_to_csv(data: list[dict]) -> str:
    """Convert data to CSV format."""
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

csv_data = convert_to_csv(get_customers())

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="customers.csv",
    mime="text/csv",
)
```

## Common Patterns Cookbook

### Search with Debounce

```python
# Search input with automatic filtering
search_query = st.text_input(
    "🔍 Search",
    placeholder="Start typing...",
    key="search_input"
)

# Filter data based on search
filtered = [
    c for c in data
    if search_query.lower() in c.get("name", "").lower()
]
```

### Confirmation Dialog

```python
# Delete confirmation
if st.button("🗑️ Delete"):
    st.session_state.show_delete_confirm = True

if st.session_state.get("show_delete_confirm"):
    st.warning("Are you sure?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Delete"):
            delete_item()
            st.session_state.show_delete_confirm = False
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.show_delete_confirm = False
            st.rerun()
```

### Toast Notifications

```python
# Success message
st.toast("✅ Customer saved successfully!")

# Error message
st.toast("❌ Failed to save customer", icon="🚨")

# Info message
st.toast("ℹ️ Changes will be saved automatically", icon="💡")
```

### Expandable Sections

```python
# Collapsible content
with st.expander("📊 Advanced Filters", expanded=False):
    st.selectbox("Category", ["All", "Hair", "Beard"])
    st.slider("Price Range", 0, 200, (0, 100))
```

### Tabs

```python
# Tabbed interface
tab1, tab2, tab3 = st.tabs(["📋 List", "📊 Analytics", "⚙️ Settings"])

with tab1:
    render_list_view()
with tab2:
    render_analytics()
with tab3:
    render_settings()
```

## Deployment

### Production Configuration

```python
# .streamlit/config.toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#0E1117"
backgroundColor = "#FFFFFF"
```

### Running in Production

```bash
# Development
streamlit run main.py

# Production with specific config
streamlit run main.py \
    --server.headless=true \
    --server.port=8501 \
    --server.enableCORS=false
```

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.headless", "true"]
```

## Best Practices Summary

1. **Session State**: Initialize early, access through getters/setters, clear on logout
2. **Components**: Keep them focused and reusable, pass data as parameters
3. **Performance**: Use caching strategically, minimize reruns, lazy load heavy data
4. **Testing**: Unit test logic, E2E test flows, mock external dependencies
5. **Forms**: Use `st.form` for grouped submissions, validate before processing
6. **Navigation**: Use `st.switch_page` for multi-page apps, guard with auth checks
7. **Error Handling**: Show user-friendly messages, log errors for debugging
8. **Accessibility**: Use clear labels, provide keyboard navigation, add alt text

## Troubleshooting

### Common Issues

1. **State not persisting**: Ensure initialization happens before access
2. **Too many reruns**: Use `st.form` for grouped inputs, check for state changes
3. **Cache misses**: Ensure cached functions have hashable inputs
4. **File upload errors**: Check file type and size limits

### Debug Mode

```python
# Enable debug output
import streamlit as st
st.write(st.session_state)  # Inspect session state
```