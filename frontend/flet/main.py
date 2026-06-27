"""
✂️ BarberPro - Flet Mobile-First Frontend

Design Reference: Instagram + Twitter Mobile
- Touch-friendly interface
- Bottom navigation bar
- Card-based feed layout
- Stories-style quick actions
- Modern gradient aesthetics

Style: Social media app meets professional SaaS
"""

import flet as ft
from datetime import datetime, timedelta
import requests

# =============================================================================
# CONFIGURATION
# =============================================================================

API_BASE_URL = "http://localhost:8000/api/v1"

# Instagram-inspired color palette
COLORS = {
    "primary_start": "#833AB4",  # Instagram purple
    "primary_mid": "#FD1D1D",    # Instagram red
    "primary_end": "#FCB045",    # Instagram orange
    "twitter_blue": "#1DA1F2",
    "background": "#FAFAFA",
    "surface": "#FFFFFF",
    "text_primary": "#262626",
    "text_secondary": "#8E8E8E",
    "border": "#DBDBDB",
    "success": "#00C853",
    "error": "#D32F2F",
}


# =============================================================================
# API CLIENT
# =============================================================================

class APIClient:
    """REST API client."""

    def __init__(self):
        self.session = requests.Session()
        self.timeout = 10

    def get(self, endpoint: str):
        try:
            response = self.session.get(f"{API_BASE_URL}{endpoint}", timeout=self.timeout)
            return response.json() if response.status_code == 200 else []
        except:
            return []


api = APIClient()


# =============================================================================
# COMPONENT: STORY CIRCLE
# =============================================================================

def StoryCircle(icon: str, label: str, on_click=None, gradient=False):
    """Instagram stories-style circular button."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [ft.Text(icon, size=24)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    width=56,
                    height=56,
                    border_radius=28,
                    gradient=ft.LinearGradient(
                        colors=[COLORS["primary_start"], COLORS["primary_end"]],
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                    ) if gradient else None,
                    bgcolor=ft.colors.WHITE if not gradient else None,
                    border=ft.border.all(2, COLORS["primary_start"]) if not gradient else None,
                    alignment=ft.alignment.center,
                ),
                ft.Text(label, size=11, color=COLORS["text_primary"], text_align=ft.TextAlign.CENTER),
            ],
            spacing=4,
            tight=True,
        ),
        on_click=on_click,
    )


# =============================================================================
# COMPONENT: POST CARD
# =============================================================================

def PostCard(title: str, subtitle: str, icon: str = "📌", actions=None):
    """Instagram post-style card."""
    return ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(icon, size=20),
                            width=40,
                            height=40,
                            border_radius=20,
                            bgcolor=f"{COLORS['primary_start']}20",
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            [
                                ft.Text(title, weight=ft.FontWeight.BOLD, size=14),
                                ft.Text(subtitle, size=12, color=COLORS["text_secondary"]),
                            ],
                            spacing=2,
                        ),
                        ftSpacer(),
                        ft.IconButton(ft.icons.MORE_VERT, icon_size=20),
                    ],
                    spacing=12,
                ),
                # Content
                ft.Container(
                    content=ft.Text("View details →", color=COLORS["twitter_blue"], weight=ft.FontWeight.BOLD),
                    padding=ft.padding.only(top=8),
                ),
            ],
            spacing=12,
        ),
        padding=16,
        bgcolor=COLORS["surface"],
        border_radius=12,
        border=ft.border.all(1, COLORS["border"]),
    )


def ftSpacer():
    """Expandable spacer."""
    return ft.Column([], expand=True)


# =============================================================================
# PAGE: DASHBOARD
# =============================================================================

class DashboardPage(ft.Column):
    """Main dashboard with social feed style."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 16

        # Stories bar (quick actions)
        self.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        StoryCircle("📊", "Stats", self.on_stats, gradient=True),
                        StoryCircle("👥", "Clients", self.on_customers),
                        StoryCircle("💈", "Barbers", self.on_barbers),
                        StoryCircle("💇", "Services", self.on_services),
                        StoryCircle("📅", "Agenda", self.on_agenda),
                        StoryCircle("💰", "Revenue", self.on_revenue),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
            )
        )

        # Metrics cards
        self.controls.append(self.metrics_section())

        # Activity feed
        self.controls.append(
            ft.Container(
                content=ft.Text("Recent Activity", weight=ft.FontWeight.BOLD, size=16),
                padding=ft.padding.symmetric(horizontal=16),
            )
        )

        self.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        PostCard("Carlos Silva", "Fade with Mike • 09:00", "✓"),
                        PostCard("André Costa", "Coloring with Sarah • 10:00", "⏳"),
                        PostCard("Bruno Lima", "Beard Trim • 11:30", "📅"),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=16),
            )
        )

    def metrics_section(self):
        """Horizontal scrolling metrics."""
        return ft.Container(
            content=ft.Row(
                [
                    self.metric_card("127", "Clientes", "👥", "#667eea"),
                    self.metric_card("8", "Barbers", "💈", "#0acf82"),
                    self.metric_card("24", "Serviços", "💇", "#f093fb"),
                    self.metric_card("R$ 2.450", "Hoje", "💰", "#ff9a9e"),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16),
        )

    def metric_card(self, value: str, label: str, icon: str, color: str):
        """Single metric card."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(icon, size=24),
                    ft.Text(value, weight=ft.FontWeight.BOLD, size=20, color=color),
                    ft.Text(label, size=11, color=COLORS["text_secondary"]),
                ],
                spacing=4,
                tight=True,
            ),
            width=100,
            padding=16,
            bgcolor=COLORS["surface"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"]),
        )

    def on_stats(self, e):
        self.page.go("/analytics")

    def on_customers(self, e):
        self.page.go("/customers")

    def on_barbers(self, e):
        self.page.go("/barbers")

    def on_services(self, e):
        self.page.go("/services")

    def on_agenda(self, e):
        self.page.go("/appointments")

    def on_revenue(self, e):
        self.page.go("/revenue")


# =============================================================================
# PAGE: CUSTOMERS
# =============================================================================

class CustomersPage(ft.Column):
    """Customers list with Instagram-style cards."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 8

        # Search bar
        self.controls.append(
            ft.Container(
                content=ft.TextField(
                    hint_text="🔍 Search customers...",
                    border_radius=24,
                    filled=True,
                    bgcolor=ft.colors.GREY_100,
                    prefix_icon=ft.icons.SEARCH,
                    content_padding=16,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
            )
        )

        # Customers list
        customers = api.get("/customers/")
        for customer in customers:
            name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}"
            email = customer.get('email', '')
            avatar = customer.get('first_name', '?')[0].upper()

            self.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(avatar, size=20, weight=ft.FontWeight.BOLD, color="white"),
                                width=50,
                                height=50,
                                border_radius=25,
                                gradient=ft.LinearGradient(
                                    colors=[COLORS["primary_start"], COLORS["primary_end"]],
                                ),
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=14),
                                    ft.Text(email, size=12, color=COLORS["text_secondary"]),
                                ],
                                spacing=2,
                            ),
                            ftSpacer(),
                            ft.IconButton(ft.icons.CHEVRON_RIGHT),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    bgcolor=COLORS["surface"],
                )
            )

        # FAB for add customer
        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Icon(ft.icons.ADD),
            bgcolor=COLORS["primary_start"],
            on_click=self.add_customer,
        )

    def add_customer(self, e):
        self.page.go("/customers/add")


# =============================================================================
# PAGE: BARBERS
# =============================================================================

class BarbersPage(ft.Column):
    """Barbers list with Twitter-style profile cards."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 8

        # Header
        self.controls.append(
            ft.Container(
                content=ft.Text("💈 Barbers", weight=ft.FontWeight.BOLD, size=20),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
            )
        )

        # Barbers list
        barbers = api.get("/barbers/")
        for barber in barbers:
            name = f"{barber.get('first_name', '')} {barber.get('last_name', '')}"
            specialty = barber.get('specialty', 'General')
            avatar = barber.get('first_name', '?')[0].upper()

            self.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(avatar, size=24, weight=ft.FontWeight.BOLD, color="white"),
                                        width=56,
                                        height=56,
                                        border_radius=28,
                                        gradient=ft.LinearGradient(
                                            colors=[COLORS["twitter_blue"], "#1484d8"],
                                        ),
                                        alignment=ft.alignment.center,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text(specialty, size=13, color=COLORS["text_secondary"]),
                                        ],
                                        spacing=4,
                                    ),
                                    ftSpacer(),
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [ft.Text("⭐", size=12), ft.Text("4.9", size=12)],
                                                spacing=4,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                spacing=12,
                            ),
                            ft.Divider(height=1),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    bgcolor=COLORS["surface"],
                )
            )

        # FAB
        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Icon(ft.icons.ADD),
            bgcolor=COLORS["twitter_blue"],
            on_click=self.add_barber,
        )

    def add_barber(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Add barber coming soon!"))
        self.page.snack_bar.open = True
        self.page.update()


# =============================================================================
# PAGE: SERVICES
# =============================================================================

class ServicesPage(ft.Column):
    """Services with pricing cards."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.spacing = 8

        # Header
        self.controls.append(
            ft.Container(
                content=ft.Text("💇 Services & Pricing", weight=ft.FontWeight.BOLD, size=20),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
            )
        )

        # Services list
        services = api.get("/services/")
        for service in services:
            name = service.get('name', 'Unknown')
            description = service.get('description', '')[:50]
            price = service.get('price', 0) / 100
            duration = service.get('duration_minutes', 0)

            self.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("✂️", size=24),
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor=f"{COLORS['primary_start']}15",
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=14),
                                    ft.Text(f"{duration} min • {description}...", size=12, color=COLORS["text_secondary"]),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(f"R$ {price:.2f}", weight=ft.FontWeight.BOLD, size=16, color=COLORS["primary_start"]),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    bgcolor=COLORS["surface"],
                    border_radius=12,
                    margin=ft.margin.symmetric(horizontal=16),
                )
            )


# =============================================================================
# PAGE: LOGIN
# =============================================================================

class LoginPage(ft.Column):
    """Instagram-style login screen."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.spacing = 16
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Logo with gradient
        self.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("✂️", size=64),
                        ft.Text(
                            "BarberPro",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            gradient=ft.LinearGradient(
                                colors=[COLORS["primary_start"], COLORS["primary_end"]],
                            ),
                        ),
                        ft.Text("Professional Barbershop Management", color=COLORS["text_secondary"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=40,
            )
        )

        # Login form
        self.email = ft.TextField(
            label="Email",
            hint_text="demo@barberpro.com",
            border_radius=8,
            content_padding=14,
        )
        self.password = ft.TextField(
            label="Password",
            password=True,
            border_radius=8,
            content_padding=14,
        )

        self.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        self.email,
                        self.password,
                        ft.Container(
                            content=ft.Text("Login", color="white", weight=ft.FontWeight.BOLD),
                            padding=14,
                            bgcolor=COLORS["primary_start"],
                            border_radius=8,
                            width=300,
                            alignment=ft.alignment.center,
                            on_click=self.handle_login,
                        ),
                        ft.Text("or", color=COLORS["text_secondary"]),
                        ft.Container(
                            content=ft.Text("Demo Login", color=COLORS["twitter_blue"], weight=ft.FontWeight.BOLD),
                            padding=14,
                            width=300,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, COLORS["border"]),
                            border_radius=8,
                            on_click=self.demo_login,
                        ),
                    ],
                    spacing=12,
                ),
                padding=20,
            )
        )

    def handle_login(self, e):
        if self.email.value and self.password.value:
            self.page.session_set("authenticated", True)
            self.page.session_set("user_email", self.email.value)
            self.page.go("/")
            self.page.update()

    def demo_login(self, e):
        self.page.session_set("authenticated", True)
        self.page.session_set("user_email", "demo@barberpro.com")
        self.page.go("/")
        self.page.update()


# =============================================================================
# NAVIGATION RAIL (Bottom for mobile)
# =============================================================================

def create_bottom_nav(page: ft.Page):
    """Instagram-style bottom navigation."""
    return ft.BottomNavigationBar(
        items=[
            ft.BottomNavigationBarItem(
                icon=ft.Icon(ft.icons.HOME),
                label="Home",
            ),
            ft.BottomNavigationBarItem(
                icon=ft.Icon(ft.icons.SEARCH),
                label="Search",
            ),
            ft.BottomNavigationBarItem(
                icon=ft.Icon(ft.icons.ADD_BOX, size=32),
                label="Add",
            ),
            ft.BottomNavigationBarItem(
                icon=ft.Icon(ft.icons.FAVORITE_BORDER),
                label="Saved",
            ),
            ft.BottomNavigationBarItem(
                icon=ft.Icon(ft.icons.PERSON),
                label="Profile",
            ),
        ],
        on_change=lambda e: handle_nav_change(page, e),
    )


def handle_nav_change(page: ft.Page, e):
    """Handle navigation change."""
    routes = ["/", "/search", "/add", "/saved", "/profile"]
    if e.control.selected_index < len(routes):
        page.go(routes[e.control.selected_index])


# =============================================================================
# MAIN APP
# =============================================================================

def main(page: ft.Page):
    """Main application entry point."""

    # Configure page
    page.title = "BarberPro"
    page.bgcolor = COLORS["background"]
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    # Responsive layout
    page.window.width = 412 if page.platform == "mobile" else 1200
    page.window.height = 915 if page.platform == "mobile" else 800

    def route_change(e):
        """Handle route changes."""
        page.views.clear()

        # Check authentication
        authenticated = page.session_get("authenticated", False)

        if page.route == "/login" or not authenticated:
            page.views.append(
                ft.View(
                    "/",
                    [LoginPage(page)],
                    padding=0,
                )
            )
        elif page.route == "/" or page.route == "":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Container(
                            content=DashboardPage(page),
                            expand=True,
                        ),
                    ],
                    bottom_bar=create_bottom_nav(page),
                    padding=0,
                )
            )
        elif page.route == "/customers":
            page.views.append(
                ft.View(
                    "/customers",
                    [
                        ft.AppBar(
                            title=ft.Text("👥 Customers"),
                            bgcolor=COLORS["surface"],
                            elevation=1,
                        ),
                        CustomersPage(page),
                    ],
                    bottom_bar=create_bottom_nav(page),
                )
            )
        elif page.route == "/barbers":
            page.views.append(
                ft.View(
                    "/barbers",
                    [
                        ft.AppBar(
                            title=ft.Text("💈 Barbers"),
                            bgcolor=COLORS["surface"],
                            elevation=1,
                        ),
                        BarbersPage(page),
                    ],
                    bottom_bar=create_bottom_nav(page),
                )
            )
        elif page.route == "/services":
            page.views.append(
                ft.View(
                    "/services",
                    [
                        ft.AppBar(
                            title=ft.Text("💇 Services"),
                            bgcolor=COLORS["surface"],
                            elevation=1,
                        ),
                        ServicesPage(page),
                    ],
                    bottom_bar=create_bottom_nav(page),
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/404",
                    [ft.Text("Page not found!", size=20)],
                    bottom_bar=create_bottom_nav(page),
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8083)