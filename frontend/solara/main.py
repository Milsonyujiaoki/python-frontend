"""
✂️ BarberPro - Modern Solara Frontend

Design Reference: Linear + Vercel
- Clean, minimal interface
- Developer-focused UX
- Subtle animations
- Professional data presentation
"""
import solara
import solara.lab
import pandas as pd
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

API_BASE_URL = "http://localhost:8000/api/v1"

# Brand colors (Nubank/Linear inspired)
COLORS = {
    "primary": "#7c3aed",      # Violet
    "primary_dark": "#6d28d9",
    "secondary": "#10b981",    # Emerald
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "bg_dark": "#0f172a",
    "bg_light": "#f8fafc",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "border": "#e2e8f0",
}

# =============================================================================
# APPLICATION STATE
# =============================================================================

class AppState:
    """Global application state management."""
    authenticated = solara.reactive(False)
    user_email = solara.reactive(None)
    current_page = solara.reactive("dashboard")
    sidebar_open = solara.reactive(True)
    dark_mode = solara.reactive(False)

    # Cached data
    customers = solara.reactive([])
    barbers = solara.reactive([])
    services = solara.reactive([])

    # UI state
    loading = solara.reactive(False)
    error = solara.reactive(None)
    search_query = solara.reactive("")


state = AppState()


# =============================================================================
# API CLIENT
# =============================================================================

class APIClient:
    """REST API client for backend communication."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 10

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response with error handling."""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 204:
            return None
        else:
            try:
                error_data = response.json()
                raise Exception(error_data.get("error", {}).get("message", "API Error"))
            except:
                raise Exception(f"HTTP {response.status_code}: {response.text[:100]}")

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Make GET request."""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.Timeout:
            raise Exception("Request timeout - server may be busy")
        except requests.ConnectionError:
            raise Exception("Cannot connect to API - is the backend running?")

    def post(self, endpoint: str, data: dict) -> dict:
        """Make POST request."""
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            json=data,
            timeout=self.timeout
        )
        return self._handle_response(response)

    def put(self, endpoint: str, data: dict) -> dict:
        """Make PUT request."""
        response = self.session.put(
            f"{self.base_url}{endpoint}",
            json=data,
            timeout=self.timeout
        )
        return self._handle_response(response)

    def delete(self, endpoint: str) -> None:
        """Make DELETE request."""
        response = self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout
        )
        return self._handle_response(response)


api = APIClient()


# =============================================================================
# DATA FETCHING HOOKS
# =============================================================================

@solara.component
def use_customers():
    """Hook to fetch and cache customers."""
    customers, set_customers = solara.use_state([])
    loading, set_loading = solara.use_state(False)
    error, set_error = solara.use_state(None)

    async def fetch():
        set_loading(True)
        try:
            data = api.get("/customers/")
            set_customers(data)
            set_error(None)
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)

    solara.use_effect(fetch, [])

    return customers, loading, error, fetch


@solara.component
def use_barbers():
    """Hook to fetch and cache barbers."""
    barbers, set_barbers = solara.use_state([])
    loading, set_loading = solara.use_state(False)
    error, set_error = solara.use_state(None)

    async def fetch():
        set_loading(True)
        try:
            data = api.get("/barbers/")
            set_barbers(data)
            set_error(None)
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)

    solara.use_effect(fetch, [])

    return barbers, loading, error, fetch


@solara.component
def use_services():
    """Hook to fetch and cache services."""
    services, set_services = solara.use_state([])
    loading, set_loading = solara.use_state(False)
    error, set_error = solara.use_state(None)

    async def fetch():
        set_loading(True)
        try:
            data = api.get("/services/")
            set_services(data)
            set_error(None)
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)

    solara.use_effect(fetch, [])

    return services, loading, error, fetch


# =============================================================================
# UI COMPONENTS
# =============================================================================

@solara.component
def LoadingSpinner():
    """Beautiful loading spinner."""
    with solara.Div(style={"display": "flex", "display": "flex", "align_items": "center", "padding": "40px"}):
        solara.HTML(
            tag="div",
            style_="""
                border: 4px solid #f3f3f3;
                border-top: 4px solid #7c3aed;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            """,
            attributes={
                "style": """
                    animation: spin 1s linear infinite;
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                """
            }
        )
        solara.Text("Loading...", style={"margin_top": "16px", "color": "#64748b"})


@solara.component
def ErrorMessage(message: str):
    """Error message banner."""
    with solara.Div(style={
        "padding": "16px",
        "background": "#fef2f2",
        "border": "1px solid #fecaca",
        "border_radius": "12px",
        "margin": "16px 0"
    }):
        solara.Markdown(f"**⚠️ Error:** {message}", style={"color": "#dc2626", "margin": "0"})


@solara.component
def MetricCard(title: str, value: str, icon: str, trend: str = None, color: str = COLORS["primary"]):
    """Modern metric card with gradient background."""
    with solara.Card(
        elevation=0,
        style={
            "background": f"linear-gradient(135deg, {color} 0%, {color}dd 100%)",
            "color": "white",
            "padding": "24px",
            "border_radius": "16px",
            "min_width": "200px",
            "flex": "1",
            "box_shadow": "0 4px 6px -1px rgba(0,0,0,0.1)",
        }
    ):
        with solara.Div(style={"display": "flex", "display": "flex", "justify_content": "space-between", "align_items": "center"}):
            solara.Markdown(f"**{title}**", style={"color": "rgba(255,255,255,0.9)", "font_size": "14px", "margin": "0"})
            solara.Markdown(icon, style={"font_size": "24px", "margin": "0"})

        solara.Markdown(
            f"**{value}**",
            style={"color": "white", "font_size": "32px", "font_weight": "700", "margin": "16px 0 0 0"}
        )

        if trend:
            solara.Markdown(trend, style={"color": "rgba(255,255,255,0.8)", "font_size": "12px", "margin": "8px 0 0 0"})


@solara.component
def StatCard(title: str, value: str, subtitle: str = None):
    """Simple stat card."""
    with solara.Card(
        elevation=0,
        style={
            "background": "white",
            "padding": "20px",
            "border_radius": "16px",
            "border": f"1px solid {COLORS['border']}",
            "min_width": "180px",
            "flex": "1",
        }
    ):
        solara.Markdown(title, style={"color": COLORS["text_secondary"], "font_size": "13px", "margin": "0 0 8px 0"})
        solara.Markdown(value, style={"color": COLORS["text_primary"], "font_size": "28px", "font_weight": "700", "margin": "0"})
        if subtitle:
            solara.Markdown(subtitle, style={"color": COLORS["success"], "font_size": "12px", "margin": "8px 0 0 0"})


@solara.component
def NavigationRail():
    """Modern sidebar navigation."""
    with solara.Div(style={
        "width": "260px",
        "background": COLORS["bg_dark"],
        "padding": "20px 16px",
        "height": "100vh",
        "position": "fixed",
        "left": "0",
        "top": "0",
        "box_shadow": "4px 0 12px rgba(0,0,0,0.1)",
    }):
        # Logo
        with solara.Div(style={"display": "flex", "align_items": "center", "margin_bottom": "32px", "padding": "0 8px"}):
            solara.Markdown("✂️", style={"font_size": "32px", "margin": "0"})
            solara.Markdown(
                "**BarberPro**",
                style={"color": "white", "font_size": "20px", "font_weight": "700", "margin": "0 0 0 10px"}
            )

        solara.Markdown("---", style={"border_color": "rgba(255,255,255,0.1)", "margin": "0 0 24px 0"})

        # Navigation items
        nav_items = [
            ("dashboard", "🏠", "Dashboard"),
            ("customers", "👥", "Customers"),
            ("barbers", "💈", "Barbers"),
            ("services", "💇", "Services"),
            ("appointments", "📅", "Appointments"),
        ]

        for page, icon, label in nav_items:
            is_active = state.current_page.value == page
            with solara.Button(
                on_click=lambda p=page: setattr(state, 'current_page', p),
                style={
                    "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)" if is_active else "transparent",
                    "color": "white",
                    "border_radius": "12px",
                    "padding": "14px 16px",
                    "margin": "4px 0",
                    "border": "none",
                    "text_align": "left",
                    "transition": "all 0.2s ease",
                }
            ):
                with solara.Div(style={"display": "flex", "display": "flex", "align_items": "center", "gap": "12px"}):
                    solara.Markdown(icon, style={"font_size": "18px", "margin": "0"})
                    solara.Markdown(label, style={"font_size": "14px", "font_weight": "500" if is_active else "400", "margin": "0"})

        solara.Markdown("---", style={"border_color": "rgba(255,255,255,0.1)", "margin": "auto 0 24px 0"})

        # User section
        if state.authenticated.value:
            with solara.Div(style={"padding": "12px", "background": "rgba(255,255,255,0.1)", "border_radius": "12px"}):
                solara.Markdown(
                    f"👤 {state.user_email.value}",
                    style={"color": "white", "font_size": "13px", "margin": "0 0 8px 0"}
                )
                solara.Button(
                    "Logout",
                    on_click=lambda: (setattr(state, 'authenticated', False), setattr(state, 'user_email', None)),
                    style={"background": "rgba(239,68,68,0.2)", "color": "#fca5a5", "border": "none", "border_radius": "8px", "padding": "8px 12px"}
                )
        else:
            solara.Button(
                "🔐 Login",
                on_click=lambda: setattr(state, 'current_page', 'login'),
                style={"background": "rgba(255,255,255,0.1)", "color": "white", "border": "none", "border_radius": "8px", "padding": "10px"}
            )


@solara.component
def TopBar():
    """Top navigation bar."""
    with solara.Div(style={
        "background": "white",
        "padding": "16px 24px",
        "border_bottom": f"1px solid {COLORS['border']}",
        "justify_content": "space-between",
        "align_items": "center",
        "margin_left": "260px",
    }):
        # Breadcrumb
        page_name = state.current_page.value.capitalize()
        solara.Markdown(f"**{page_name}**", style={"color": COLORS["text_primary"], "font_size": "20px", "margin": "0"})

        # Right actions
        with solara.Div(style={"display": "flex", "display": "flex", "align_items": "center", "gap": "12px"}):
            solara.Button(
                icon_name="mdi-bell",
                text=True,
                style={"color": COLORS["text_secondary"], "min_width": "40px"}
            )
            with solara.Card(
                elevation=0,
                style={"display": "flex", "display": "flex", "width": "36px", "height": "36px", "border_radius": "50%", "background": COLORS["primary"], "display": "flex", "align_items": "center", "justify_content": "center"}
            ):
                solara.Markdown("👤", style={"margin": "0", "font_size": "16px"})


# =============================================================================
# PAGES
# =============================================================================

@solara.component
def DashboardPage():
    """Dashboard with metrics and overview."""
    solara.Title("Dashboard")

    with solara.Div(style={"padding": "24px"}):
        # Welcome header
        solara.Markdown(
            f"## Welcome back! 👋",
            style={"color": COLORS["text_primary"], "margin": "0 0 8px 0"}
        )
        solara.Markdown(
            f"Here's what's happening at your barbershop today.",
            style={"color": COLORS["text_secondary"], "margin": "0 0 24px 0"}
        )

        # Metrics row
        with solara.Div(style={"display": "flex", "gap": "16px", "flex_wrap": "wrap", "margin_bottom": "24px"}):
            StatCard("Total Customers", "127", "+12% vs last week")
            StatCard("Active Barbers", "8", "All on shift")
            StatCard("Services", "24", "5 categories")
            StatCard("Today's Revenue", "R$ 2.450", "+18% vs yesterday")

        # Content cards
        with solara.Div(style={"display": "flex", "gap": "16px", "flex_wrap": "wrap"}):
            # Recent appointments
            with solara.Card(
                elevation=0,
                style={
                    "background": "white",
                    "padding": "24px",
                    "border_radius": "16px",
                    "border": f"1px solid {COLORS['border']}",
                    "flex": "2",
                    "min_width": "400px",
                }
            ):
                solara.Markdown("**📅 Today's Appointments**", style={"margin": "0 0 16px 0"})

                appointments_data = pd.DataFrame([
                    {"Time": "09:00", "Customer": "Carlos Silva", "Barber": "Mike", "Service": "Fade", "Status": "✓ Done"},
                    {"Time": "10:00", "Customer": "André Costa", "Barber": "Sarah", "Service": "Coloring", "Status": "⏳ In Progress"},
                    {"Time": "11:30", "Customer": "Bruno Lima", "Barber": "Mike", "Service": "Beard Trim", "Status": "⏳ Pending"},
                    {"Time": "13:00", "Customer": "Pedro Rocha", "Barber": "Tom", "Service": "Full Cut", "Status": "⏳ Pending"},
                ])
                solara.DataFrame(appointments_data)

            # Quick stats
            with solara.Card(
                elevation=0,
                style={
                    "background": "white",
                    "padding": "24px",
                    "border_radius": "16px",
                    "border": f"1px solid {COLORS['border']}",
                    "flex": "1",
                    "min_width": "250px",
                }
            ):
                solara.Markdown("**⚡ Quick Stats**", style={"margin": "0 0 16px 0"})

                with solara.Div(style={"display": "flex", "gap": "12px"}):
                    solara.ProgressLinear(value=0.75, style={"margin": "0"})
                    solara.Markdown("75% capacity today", style={"font_size": "12px", "color": COLORS["text_secondary"], "margin": "0"})

                    solara.ProgressLinear(value=0.6, style={"margin": "0"})
                    solara.Markdown("6 barbers on duty", style={"font_size": "12px", "color": COLORS["text_secondary"], "margin": "0"})

                    solara.ProgressLinear(value=0.9, style={"margin": "0"})
                    solara.Markdown("90% customer satisfaction", style={"font_size": "12px", "color": COLORS["text_secondary"], "margin": "0"})


@solara.component
def CustomersPage():
    """Customers management page."""
    solara.Title("Customers")

    customers, loading, error, refresh = use_customers()
    search_query = solara.use_reactive("")
    show_form = solara.use_reactive(False)

    with solara.Div(style={"padding": "24px"}):
        # Header
        with solara.Div(style={"display": "flex", "display": "flex", "justify_content": "space-between", "align_items": "center", "margin_bottom": "24px"}):
            solara.Markdown("## 👥 Customers", style={"margin": "0"})
            solara.Button(
                "➕ Add Customer",
                on_click=lambda: setattr(show_form, 'value', True),
                style={
                    "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                    "color": "white",
                    "border": "none",
                    "border_radius": "10px",
                    "padding": "12px 24px",
                    "font_weight": "600",
                }
            )

        # Search
        solara.InputText(
            label="",
            value=search_query,
            placeholder="🔍 Search by name or email...",
            style={"margin_bottom": "16px"}
        )

        # Content
        if loading.value:
            LoadingSpinner()
        elif error.value:
            ErrorMessage(error.value)
        else:
            # Filter customers
            filtered = [
                c for c in customers
                if search_query.value.lower() in c.get("first_name", "").lower()
                or search_query.value.lower() in c.get("last_name", "").lower()
                or search_query.value.lower() in c.get("email", "").lower()
            ]

            # Format for display
            display_data = []
            for c in filtered:
                display_data.append({
                    "Name": f"{c.get('first_name', '')} {c.get('last_name', '')}",
                    "Email": c.get('email', ''),
                    "Phone": c.get('phone', '-'),
                    "Status": "Active" if c.get('is_active', True) else "Inactive",
                })

            solara.DataFrame(pd.DataFrame(display_data))


@solara.component
def BarbersPage():
    """Barbers management page with card layout."""
    solara.Title("Barbers")

    barbers, loading, error, refresh = use_barbers()
    search_query = solara.use_reactive("")

    with solara.Div(style={"padding": "24px"}):
        # Header
        solara.Markdown("## 💈 Barbers", style={"margin": "0 0 24px 0"})

        # Search
        solara.InputText(
            label="",
            value=search_query,
            placeholder="🔍 Search by name or specialty...",
            style={"margin_bottom": "16px"}
        )

        # Content
        if loading.value:
            LoadingSpinner()
        elif error.value:
            ErrorMessage(error.value)
        else:
            # Filter barbers
            filtered = [
                b for b in barbers
                if search_query.value.lower() in b.get("first_name", "").lower()
                or search_query.value.lower() in b.get("last_name", "").lower()
                or search_query.value.lower() in b.get("specialty", "").lower()
            ]

            # Cards layout
            with solara.Div(style={"display": "flex", "gap": "16px", "flex_wrap": "wrap"}):
                for barber in filtered:
                    with solara.Card(
                        elevation=0,
                        style={
                            "background": "white",
                            "padding": "20px",
                            "border_radius": "16px",
                            "border": f"1px solid {COLORS['border']}",
                            "min_width": "280px",
                            "flex": "1",
                        }
                    ):
                        with solara.Div(style={"display": "flex", "display": "flex", "align_items": "center", "gap": "12px", "margin_bottom": "12px"}):
                            avatar_style = {
                                "width": "48px", "height": "48px", "border_radius": "50%",
                                "background": COLORS["primary"], "color": "white",
                                "display": "flex", "align_items": "center", "justify_content": "center",
                                "font_size": "20px", "font_weight": "700"
                            }
                            initial = barber.get('first_name', '?')[0].upper()
                            solara.Markdown(initial, style=avatar_style)

                            with solara.Div():
                                solara.Markdown(
                                    f"**{barber.get('first_name', '')} {barber.get('last_name', '')}**",
                                    style={"margin": "0", "font_size": "16px"}
                                )
                                status = "Active" if barber.get('is_active', True) else "Off"
                                solara.Markdown(status, style={"margin": "0", "font_size": "12px", "color": COLORS["success"] if barber.get('is_active', True) else COLORS["text_secondary"]})

                        solara.Markdown(
                            f"💼 **Specialty**: {barber.get('specialty', 'General')}",
                            style={"margin": "8px 0", "font_size": "14px"}
                        )

                        if barber.get('bio'):
                            solara.Markdown(
                                f"📝 {barber.get('bio', '')[:50]}...",
                                style={"margin": "8px 0", "font_size": "12px", "color": COLORS["text_secondary"]}
                            )

                        # Rating
                        solara.Markdown("⭐⭐⭐⭐⭐", style={"margin": "12px 0 0 0", "font_size": "14px"})


@solara.component
def ServicesPage():
    """Services management page."""
    solara.Title("Services")

    services, loading, error, refresh = use_services()
    search_query = solara.use_reactive("")

    with solara.Div(style={"padding": "24px"}):
        # Header
        solara.Markdown("## 💇 Services", style={"margin": "0 0 24px 0"})

        # Search
        solara.InputText(
            label="",
            value=search_query,
            placeholder="🔍 Search services...",
            style={"margin_bottom": "16px"}
        )

        # Content
        if loading.value:
            LoadingSpinner()
        elif error.value:
            ErrorMessage(error.value)
        else:
            filtered = [
                s for s in services
                if search_query.value.lower() in s.get("name", "").lower()
            ]

            display_data = []
            for s in filtered:
                display_data.append({
                    "Service": s.get('name', ''),
                    "Description": s.get('description', '')[:50] + '...' if len(s.get('description', '')) > 50 else s.get('description', ''),
                    "Price": f"R$ {s.get('price', 0) / 100:.2f}",
                    "Duration": f"{s.get('duration_minutes', 0)} min",
                    "Status": "Active" if s.get('is_active', True) else "Inactive",
                })

            solara.DataFrame(pd.DataFrame(display_data))


@solara.component
def LoginPage():
    """Modern login page."""
    solara.Title("Login")

    email = solara.use_reactive("")
    password = solara.use_reactive("")

    with solara.Div(style={"display": "flex", "display": "flex", 
        "min_height": "100vh",
        "background": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        "padding": "40px",
        "align_items": "center",
        "justify_content": "center",
    }):
        with solara.Card(
            elevation=0,
            style={
                "background": "white",
                "padding": "40px",
                "border_radius": "24px",
                "min_width": "400px",
                "box_shadow": "0 20px 25px -5px rgba(0,0,0,0.1)",
            }
        ):
            # Logo
            solara.Markdown(
                "✂️ **BarberPro**",
                style={"text_align": "center", "font_size": "28px", "margin": "0 0 8px 0"}
            )
            solara.Markdown(
                "Professional Barbershop Management",
                style={"text_align": "center", "color": COLORS["text_secondary"], "font_size": "14px", "margin": "0 0 32px 0"}
            )

            # Form
            solara.InputText(
                label="Email",
                value=email,
                placeholder="Enter your email",
                style={"margin_bottom": "16px"}
            )
            solara.InputText(
                label="Password",
                value=password,
                placeholder="Enter your password",
                type="password",
                style={"margin_bottom": "24px"}
            )

            # Buttons
            solara.Button(
                "Login",
                on_click=lambda: (
                    setattr(state, 'authenticated', True),
                    setattr(state, 'user_email', email.value),
                    setattr(state, 'current_page', 'dashboard')
                ) if email.value and password.value else None,
                style={
                    "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                    "color": "white",
                    "border": "none",
                    "border_radius": "12px",
                    "padding": "14px 28px",
                    "font_weight": "600",
                    "width": "100%",
                    "margin_bottom": "12px",
                }
            )

            solara.Button(
                "Demo Login (no password)",
                on_click=lambda: (
                    setattr(state, 'authenticated', True),
                    setattr(state, 'user_email', 'demo@barberpro.com'),
                    setattr(state, 'current_page', 'dashboard')
                ),
                style={
                    "background": "#f1f5f9",
                    "color": COLORS["text_primary"],
                    "border": f"1px solid {COLORS['border']}",
                    "border_radius": "12px",
                    "padding": "14px 28px",
                    "font_weight": "500",
                    "width": "100%",
                }
            )


@solara.component
def Page():
    """Main application layout."""
    page = state.current_page.value

    # Render navigation
    if page != "login":
        NavigationRail()

        with solara.Div(style={"margin_left": "260px", "min_height": "100vh", "background": "#f8fafc"}):
            TopBar()

            # Page content
            if page == "dashboard":
                DashboardPage()
            elif page == "customers":
                CustomersPage()
            elif page == "barbers":
                BarbersPage()
            elif page == "services":
                ServicesPage()
            elif page == "appointments":
                solara.Markdown("## 📅 Appointments\n\nComing soon!", style={"padding": "24px"})
            else:
                solara.Markdown("## Page not found", style={"padding": "24px"})
    else:
        LoginPage()


# App metadata
solara.Meta(title="BarberPro - Professional Barbershop Management")