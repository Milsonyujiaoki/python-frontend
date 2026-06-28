"""
End-to-end tests for barber management flows in Solara frontend.
"""
import pytest
import re
from playwright.async_api import expect

@pytest.mark.e2e
async def test_barber_list_page_loads_authenticated(page, authenticated_user):
    """Test that the barber list loads correctly for authenticated user."""
    await page.goto("http://localhost:8000/barbers")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Barbers")).to_be_visible()

    # Check that the table or list of barbers is present
    await expect(page.locator("table")).to_be_visible()

@pytest.mark.e2e
async def test_create_barber_form_loads(page, authenticated_user):
    """Test that the create barber form loads correctly."""
    await page.goto("http://localhost:8000/barbers/create")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Create Barber")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='First Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Last Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Email']")).to_be_visible()
    await expect(page.locator("input[placeholder='Phone Number']")).to_be_visible()
    await expect(page.locator("input[placeholder='Specialty']")).to_be_visible()
    await expect(page.locator("button:has-text('Save Barber')")).to_be_visible()

@pytest.mark.e2e
async def test_barber_detail_page_loads(page, authenticated_user, test_barber):
    """Test that the barber detail page loads correctly."""
    # Navigate to the barber detail page
    await page.goto(f"http://localhost:8000/barbers/{test_barber.id}")

    # Check that the barber details are displayed
    await expect(page.locator(f"text={test_barber.first_name}")).to_be_visible()
    await expect(page.locator(f"text={test_barber.last_name}")).to_be_visible()
    await expect(page.locator(f"text={test_barber.email}")).to_be_visible()

    # Check that action buttons are present
    await expect(page.locator("button:has-text('Edit Barber')")).to_be_visible()
    await expect(page.locator("button:has-text('Delete Barber')")).to_be_visible()