"""
End-to-end tests for customer management flows in Solara frontend.
"""
import pytest
import re
from playwright.async_api import expect

@pytest.mark.e2e
async def test_customer_list_page_loads_authenticated(page, authenticated_user):
    """Test that the customer list loads correctly for authenticated user."""
    # Assuming we have a fixture that logs in the user
    await page.goto("http://localhost:8000/customers")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Customers")).to_be_visible()

    # Check that the table or list of customers is present
    await expect(page.locator("table")).to_be_visible()
    # or alternatively
    # await expect(page.locator('[data-testid="customer-list"]')).to_be_visible()

@pytest.mark.e2e
async def test_create_customer_form_loads(page, authenticated_user):
    """Test that the create customer form loads correctly."""
    await page.goto("http://localhost:8000/customers/create")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Create Customer")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='First Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Last Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Email']")).to_be_visible()
    await expect(page.locator("input[placeholder='Phone Number']")).to_be_visible()
    await expect(page.locator("button:has-text('Save Customer')")).to_be_visible()

@pytest.mark.e2e
async def test_customer_detail_page_loads(page, authenticated_user, test_customer):
    """Test that the customer detail page loads correctly."""
    # Navigate to the customer detail page
    await page.goto(f"http://localhost:8000/customers/{test_customer.id}")

    # Check that the customer details are displayed
    await expect(page.locator(f"text={test_customer.first_name}")).to_be_visible()
    await expect(page.locator(f"text={test_customer.last_name}")).to_be_visible()
    await expect(page.locator(f"text={test_customer.email}")).to_be_visible()

    # Check that action buttons are present
    await expect(page.locator("button:has-text('Edit Customer')")).to_be_visible()
    await expect(page.locator("button:has-text('Delete Customer')")).to_be_visible()