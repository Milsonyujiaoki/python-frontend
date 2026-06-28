# Flet Frontend Development Patterns

## Overview

Flet enables building cross-platform applications (web, desktop, mobile) from a single Python codebase. This document provides patterns and best practices for the BarberShop SaaS Flet frontend.

## Architecture

```
frontend/flet/
├── main.py                 # Application entry point
├── pages/                  # Page components (optional, using views instead)
├── components/             # Reusable widgets
├── services/               # Business logic
│   └── api_client.py      # API communication
├── utils/                  # Utilities
│   └── state_manager.py   # State management
└── tests/                  # Tests
    ├── unit/
    └── e2e/
```

## Routing and Navigation

Flet uses a views-based navigation system:

```python
def main(page: ft.Page):
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(ft.View("/", [dashboard_view]))
        elif page.route == "/customers":
            page.views.append(ft.View("/customers", [customers_view]))
        
        page.update()
    
    def view_pop(e):
        page.views.pop()
        page.go(page.views[-1].route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
```

## State Management

Using the StateManager pattern:

```python
from utils.state_manager import StateManager

state = StateManager(page)

# Set values
state.set_authenticated("user@example.com")
state.set("customers", customer_list)

# Get values
if state.is_authenticated():
    email = state.get_user_email()

# Clear on logout
state.logout()
```

## Reusable Components

### Custom AppBar

```python
class CustomAppBar(ft.AppBar):
    def __init__(self, page, on_nav):
        super().__init__(
            leading=ft.IconButton(ft.icons.MENU, on_click=self.open_drawer),
            title=ft.Text("App Title"),
            actions=[ft.IconButton(ft.icons.NOTIFICATIONS)],
        )
```

### Metric Card

```python
def create_metric_card(title, value, delta, color):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=12, color=ft.colors.GREY_600),
            ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(delta, size=12, color=delta_color),
        ]),
        padding=16,
        border_radius=8,
        border=ft.border.all(1, ft.colors.OUTLINE),
    )
```

## Data Tables

```python
ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Name")),
        ft.DataColumn(ft.Text("Email")),
        ft.DataColumn(ft.Text("Actions")),
    ],
    rows=[
        ft.DataRow(cells=[
            ft.DataCell(ft.Text("John Doe")),
            ft.DataCell(ft.Text("john@example.com")),
            ft.DataCell(ft.Row([
                ft.IconButton(ft.icons.EDIT),
                ft.IconButton(ft.icons.DELETE),
            ])),
        ]),
    ],
)
```

## Forms

```python
def create_form():
    return ft.Column([
        ft.TextField(label="Name", expand=True),
        ft.TextField(label="Email", expand=True),
        ft.Dropdown(options=[
            ft.dropdown.Option("Active"),
            ft.dropdown.Option("Inactive"),
        ]),
        ft.ElevatedButton("Save"),
    ])
```

## Platform-Specific Features

### File Picker

```python
file_picker = ft.FilePicker(on_result=handle_file_pick)
page.overlay.append(file_picker)

def pick_file():
    file_picker.pick_files(allowed_extensions=["csv", "xlsx"])
```

### Camera (Mobile)

```python
# For mobile platforms
camera = ft.Camera(on_image_captured=handle_photo)
```

## Responsive Layout

```python
def responsive_view(page):
    # Get window width
    width = page.window.width
    
    if width < 600:
        # Mobile layout
        return ft.Column([mobile_components])
    elif width < 1000:
        # Tablet layout
        return ft.Row([tablet_components])
    else:
        # Desktop layout
        return ft.Row([desktop_components])
```

## Testing

### Unit Tests

```python
import flet as ft

def test_metric_card():
    card = create_metric_card("Test", "100", "+10", ft.colors.GREEN)
    assert isinstance(card, ft.Container)
    assert card.width == 150
```

### Integration Tests

```python
def test_navigation(page):
    page.go("/customers")
    assert page.route == "/customers"
```

## Best Practices

1. **Use views for pages** - Flet's view system handles navigation naturally
2. **Centralize state** - Use StateManager for consistent state handling
3. **Component composition** - Build complex UIs from small, reusable components
4. **Responsive first** - Design for multiple screen sizes from the start
5. **Async for API calls** - Use async/await for non-blocking operations

## Deployment

### Web

```bash
flet run main.py --web
```

### Desktop

```bash
flet run main.py
```

### Mobile (Packaging)

```bash
flet pack main.py --platform android
flet pack main.py --platform ios
```

## Common Patterns

### Dialog

```python
def show_dialog(page, title, content):
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[ft.TextButton("OK", on_click=close)],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()
```

### Snackbar

```python
def show_snackbar(page, message):
    page.snack_bar = ft.SnackBar(ft.Text(message))
    page.snack_bar.open = True
    page.update()
```

### Loading Indicator

```python
def set_loading(page, loading=True):
    page.overlay.clear()
    if loading:
        page.overlay.append(
            ft.Container(
                content=ft.CircularProgressIndicator(),
                bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                expand=True,
            )
        )
    page.update()
```
