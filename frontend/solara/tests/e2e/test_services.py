"""
End-to-end tests for service management flows in Solara frontend.
"""
import pytest
import re
from playwright.async_api import expect

@pytest.mark.e2e
async def test_service_list_page_loads_authenticated(page, authenticated_user):
    """Test that the service list loads correctly for authenticated user."""
    await page.goto("http://localhost:8000/services")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Services")).to_be_visible()

    # Check that the table or list of services is present
    await expect(page.locator("table")).to_be_visible()

@pytest.mark.e2e
async def test_create_service_form_loads(page, authenticated_user):
    """Test that the create service form loads correctly."""
    await page.goto("http://localhost:8000/services/create")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Create Service")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='Service Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Duration (minutes)']")).to_be_visible()
    await expect(page.locator("input[placeholder='Price']")).to_be_visible()
    await expect(page.locator("textarea[placeholder='Description']")).to_be_visible()
    await expect(page.locator("button:has-text('Save Service')")).to_be_visible()

@pytest.mark.e2e
async def test_service_detail_page_loads(page, authenticated_user, test_service):
    """Test that the service detail page loads correctly."""
    # Navigate to the service detail page
    await page.goto(f"http://localhost:8000/services/{test_service.id}")

    # Check that the service details are displayed
    await expect(page.locator(f"text={test_service.name}")).to_be_visible()
    await expect(page.locator(f"text={test_service.price}")).to_be_visible()
    await expect(page.locator(f"text={test_service.duration}")).to_be_visible()

    # Check that action buttons are present
    await expect(page.locator("button:has-text('Edit Service')")).to_be_visible()
    await expect(page.locator("button:has-text('Delete Service')")).to_be_visible()