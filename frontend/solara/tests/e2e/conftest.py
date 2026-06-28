"""
Configuration and fixtures for End-to-End tests.
"""
import pytest
from playwright.async_api import async_playwright, BrowserContext, Page

# Base URL for the application
BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
async def browser():
    """Create a browser instance for the test session."""
    async with async_playwright() as p:
        # Launch browser in headless mode for CI, headed for local debugging
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture
async def context(browser):
    """Create a browser context for each test."""
    context = await browser.new_context()
    yield context
    await context.close()

@pytest.fixture
async def page(context):
    """Create a page for each test."""
    page = await context.new_page()
    yield page
    await page.close()

@pytest.fixture
async def authenticated_user(page):
    """
    Fixture that provides an authenticated user session.
    This assumes there are test users available or creates one.
    """
    # Navigate to login page
    await page.goto(f"{BASE_URL}/login")

    # For testing purposes, we'll use a known test user
    # In a real scenario, you might need to register a user first
    # or use API calls to set up authentication state

    # Fill in login form
    await page.fill('input[placeholder="Email"]', "test@example.com")
    await page.fill('input[placeholder="Password"]', "password123")

    # Submit the form
    await page.click('button:has-text("Sign In")')

    # Wait for navigation to dashboard or home page
    await page.wait_for_url(f"{BASE_URL}/dashboard", timeout=5000)

    # Return the page object with authenticated session
    yield page

@pytest.fixture
async def test_customer(page, authenticated_user):
    """Create a test customer and return its details."""
    # This would typically involve creating a customer via UI or API
    # For now, we'll return a mock object
    # In a real implementation, you would:
    # 1. Navigate to create customer page
    # 2. Fill out the form
    # 3. Submit and capture the created customer's ID

    # Mock return value - replace with actual implementation
    class MockCustomer:
        def __init__(self):
            self.id = 1
            self.name = "Test Customer"
            self.email = "test@example.com"

    return MockCustomer()

@pytest.fixture
async def test_barber(page, authenticated_user):
    """Create a test barber and return its details."""
    # Similar to test_customer, this would create a barber via UI
    class MockBarber:
        def __init__(self):
            self.id = 1
            self.first_name = "Test"
            self.last_name = "Barber"
            self.email = "barber@example.com"

    return MockBarber()

@pytest.fixture
async def test_service(page, authenticated_user):
    """Create a test service and return its details."""
    # Similar to test_customer, this would create a service via UI
    class MockService:
        def __init__(self):
            self.id = 1
            self.name = "Haircut"
            self.price = 25.0
            self.duration = 30

    return MockService()