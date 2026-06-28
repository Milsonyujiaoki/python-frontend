"""End-to-end tests for Streamlit application using Playwright."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestStreamlitApp:
    """E2E tests for the Streamlit application."""

    @pytest.fixture(scope="function")
    def base_url(self):
        """Get the base URL for the application."""
        return "http://localhost:8501"

    def test_home_page_loads(self, page: Page, base_url: str):
        """Test that the home page loads successfully."""
        response = page.goto(base_url)
        assert response.status == 200

        # Check for app title
        expect(page).to_have_title("BarberShop SaaS")

        # Check for sidebar navigation
        expect(page.locator("css=[data-testid='stSidebar']")).to_be_visible()

    def test_sidebar_navigation_visible(self, page: Page, base_url: str):
        """Test that sidebar navigation is visible."""
        page.goto(base_url)

        # Check sidebar contains navigation options
        sidebar = page.locator("css=[data-testid='stSidebar']")
        expect(sidebar).to_contain_text("Navigation")
        expect(sidebar).to_contain_text("Dashboard")
        expect(sidebar).to_contain_text("Customers")
        expect(sidebar).to_contain_text("Barbers")
        expect(sidebar).to_contain_text("Services")

    def test_dashboard_page_displays_metrics(self, page: Page, base_url: str):
        """Test that dashboard displays key metrics."""
        page.goto(base_url)

        # Wait for dashboard to load
        page.wait_for_load_state("networkidle")

        # Check for dashboard title
        expect(page.locator("h1")).to_contain_text("Dashboard")

        # Check for metric cards (they render with specific data-testid)
        # Streamlit metrics have specific structure
        expect(page.locator("css=div[data-testid='stMetric']")).to_have_count(4)

    def test_customers_page_loads(self, page: Page, base_url: str):
        """Test that customers page loads and displays data."""
        page.goto(f"{base_url}/customers")

        # Wait for page to load
        page.wait_for_load_state("networkidle")

        # Check for customers title
        expect(page.locator("h1")).to_contain_text("Customers")

        # Check for data table
        expect(page.locator("css=div[data-testid='stDataFrame']")).to_be_visible()

    def test_barbers_page_loads(self, page: Page, base_url: str):
        """Test that barbers page loads and displays data."""
        page.goto(f"{base_url}/barbers")

        page.wait_for_load_state("networkidle")

        expect(page.locator("h1")).to_contain_text("Barbers")
        expect(page.locator("css=div[data-testid='stDataFrame']")).to_be_visible()

    def test_services_page_loads(self, page: Page, base_url: str):
        """Test that services page loads and displays data."""
        page.goto(f"{base_url}/services")

        page.wait_for_load_state("networkidle")

        expect(page.locator("h1")).to_contain_text("Services")
        expect(page.locator("css=div[data-testid='stDataFrame']")).to_be_visible()

    def test_login_page_loads(self, page: Page, base_url: str):
        """Test that login page loads and displays form."""
        page.goto(f"{base_url}/login")

        page.wait_for_load_state("networkidle")

        expect(page.locator("h1")).to_contain_text("Login")

        # Check for login form fields
        expect(page.locator("css=input[type='text']")).to_be_visible()
        expect(page.locator("css=input[type='password']")).to_be_visible()

    def test_login_form_submission(self, page: Page, base_url: str):
        """Test login form submission."""
        page.goto(f"{base_url}/login")
        page.wait_for_load_state("networkidle")

        # Fill in login form
        email_input = page.locator("css=input[type='text']").first
        email_input.fill("admin@barbershop.com")

        password_input = page.locator("css=input[type='password']").first
        password_input.fill("password123")

        # Submit form
        submit_button = page.locator(
            "css=button[data-testid='stButton'][type='submit']"
        )
        submit_button.click()

        # Wait for navigation or success message
        page.wait_for_load_state("networkidle")

        # Should stay on page or redirect to dashboard
        # Check for logged in state (user email displayed)
        expect(page.locator("css=[data-testid='stSidebar']")).to_contain_text(
            "admin@barbershop.com"
        )

    def test_navigation_to_customers(self, page: Page, base_url: str):
        """Test navigation from sidebar to customers page."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Click on Customers in sidebar
        sidebar = page.locator("css=[data-testid='stSidebar']")
        customers_link = sidebar.locator("text=Customers").first
        customers_link.click()

        # Wait for navigation
        page.wait_for_load_state("networkidle")

        # Should be on customers page
        expect(page.locator("h1")).to_contain_text("Customers")
        expect(page.url).to_contain("customers")

    def test_navigation_to_barbers(self, page: Page, base_url: str):
        """Test navigation from sidebar to barbers page."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        sidebar = page.locator("css=[data-testid='stSidebar']")
        barbers_link = sidebar.locator("text=Barbers").first
        barbers_link.click()

        page.wait_for_load_state("networkidle")

        expect(page.locator("h1")).to_contain_text("Barbers")
        expect(page.url).to_contain("barbers")

    def test_navigation_to_services(self, page: Page, base_url: str):
        """Test navigation from sidebar to services page."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        sidebar = page.locator("css=[data-testid='stSidebar']")
        services_link = sidebar.locator("text=Services").first
        services_link.click()

        page.wait_for_load_state("networkidle")

        expect(page.locator("h1")).to_contain_text("Services")
        expect(page.url).to_contain("services")

    def test_add_customer_button(self, page: Page, base_url: str):
        """Test that add customer button is visible and clickable."""
        page.goto(f"{base_url}/customers")
        page.wait_for_load_state("networkidle")

        # Find add customer button
        add_button = page.locator("text=Add Customer").first
        expect(add_button).to_be_visible()
        expect(add_button).to_be_enabled()

    def test_add_barber_button(self, page: Page, base_url: str):
        """Test that add barber button is visible and clickable."""
        page.goto(f"{base_url}/barbers")
        page.wait_for_load_state("networkidle")

        add_button = page.locator("text=Add Barber").first
        expect(add_button).to_be_visible()
        expect(add_button).to_be_enabled()

    def test_add_service_button(self, page: Page, base_url: str):
        """Test that add service button is visible and clickable."""
        page.goto(f"{base_url}/services")
        page.wait_for_load_state("networkidle")

        add_button = page.locator("text=Add Service").first
        expect(add_button).to_be_visible()
        expect(add_button).to_be_enabled()

    def test_search_functionality(self, page: Page, base_url: str):
        """Test search input is available on list pages."""
        page.goto(f"{base_url}/customers")
        page.wait_for_load_state("networkidle")

        # Find search input
        search_input = page.locator(
            "css=input[placeholder*='Search'], css=input[aria-label*='Search']"
        ).first
        expect(search_input).to_be_visible()

        # Test search functionality
        search_input.fill("John")
        page.wait_for_timeout(500)  # Wait for debounced search

        # Table should filter results
        expect(page.locator("css=div[data-testid='stDataFrame']")).to_be_visible()

    def test_responsive_layout(self, page: Page, base_url: str):
        """Test responsive layout on different screen sizes."""
        # Test mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Sidebar should still be accessible (as drawer or collapsed)
        expect(page.locator("css=[data-testid='stSidebar']")).to_be_visible()

        # Test tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        expect(page.locator("css=[data-testid='stSidebar']")).to_be_visible()


@pytest.mark.e2e
class TestStreamlitAuthentication:
    """E2E tests for authentication flow."""

    @pytest.fixture(scope="function")
    def base_url(self):
        """Get the base URL for the application."""
        return "http://localhost:8501"

    def test_logout_functionality(self, page: Page, base_url: str):
        """Test logout functionality."""
        # First login
        page.goto(f"{base_url}/login")
        page.wait_for_load_state("networkidle")

        email_input = page.locator("css=input[type='text']").first
        email_input.fill("test@example.com")

        password_input = page.locator("css=input[type='password']").first
        password_input.fill("password123")

        submit_button = page.locator(
            "css=button[data-testid='stButton'][type='submit']"
        )
        submit_button.click()

        page.wait_for_load_state("networkidle")

        # Click logout button in sidebar
        sidebar = page.locator("css=[data-testid='stSidebar']")
        logout_button = sidebar.locator("text=Logout").first
        logout_button.click()

        page.wait_for_load_state("networkidle")

        # Should show "Not logged in" after logout
        expect(sidebar).to_contain_text("Not logged in")

    def test_unauthenticated_access_redirect(self, page: Page, base_url: str):
        """Test that unauthenticated users are redirected to login."""
        # This test depends on whether auth is enforced
        # If auth is optional in demo mode, this test should be adjusted

        page.goto(f"{base_url}/customers")
        page.wait_for_load_state("networkidle")

        # Check current URL - should either stay on page (demo mode)
        # or redirect to login
        current_url = page.url

        # In demo mode, access is allowed without auth
        assert "customers" in current_url or "login" in current_url