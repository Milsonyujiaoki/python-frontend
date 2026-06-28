"""
End-to-end tests for FastUI frontend.
"""

import pytest
from playwright.async_api import expect


@pytest.mark.e2e
async def test_dashboard_page_loads(page):
    """Test that the dashboard page loads correctly."""
    await page.goto("http://localhost:8000/")

    # Check for dashboard heading
    await expect(page.locator("h2:has-text('Dashboard')")).to_be_visible()

    # Check for navigation links
    await expect(page.locator("text=Customers")).to_be_visible()
    await expect(page.locator("text=Barbers")).to_be_visible()
    await expect(page.locator("text=Services")).to_be_visible()


@pytest.mark.e2e
async def test_customers_page_loads(page):
    """Test that the customers page loads correctly."""
    await page.goto("http://localhost:8000/customers")

    # Check for customers heading
    await expect(page.locator("h2:has-text('Customers')")).to_be_visible()

    # Check for add customer button
    await expect(page.locator("button:has-text('Add Customer')")).to_be_visible()

    # Check for table
    await expect(page.locator("table")).to_be_visible()


@pytest.mark.e2e
async def test_barbers_page_loads(page):
    """Test that the barbers page loads correctly."""
    await page.goto("http://localhost:8000/barbers")

    # Check for barbers heading
    await expect(page.locator("h2:has-text('Barbers')")).to_be_visible()

    # Check for add barber button
    await expect(page.locator("button:has-text('Add Barber')")).to_be_visible()

    # Check for table with specialty column
    await expect(page.locator("th:has-text('Specialty')")).to_be_visible()


@pytest.mark.e2e
async def test_services_page_loads(page):
    """Test that the services page loads correctly."""
    await page.goto("http://localhost:8000/services")

    # Check for services heading
    await expect(page.locator("h2:has-text('Services')")).to_be_visible()

    # Check for add service button
    await expect(page.locator("button:has-text('Add Service')")).to_be_visible()

    # Check for table with price column
    await expect(page.locator("th:has-text('Price')")).to_be_visible()


@pytest.mark.e2e
async def test_login_page_loads(page):
    """Test that the login page loads correctly."""
    await page.goto("http://localhost:8000/login")

    # Check for login heading
    await expect(page.locator("h2:has-text('Login')")).to_be_visible()

    # Check for form fields
    await expect(page.locator('input[type="email"]')).to_be_visible()
    await expect(page.locator('input[type="password"]')).to_be_visible()

    # Check for submit button
    await expect(page.locator('button[type="submit"]')).to_be_visible()