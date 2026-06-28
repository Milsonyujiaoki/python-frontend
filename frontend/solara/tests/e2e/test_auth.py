"""
End-to-end tests for authentication flows in Solara frontend.
"""
import pytest
import re
from playwright.async_api import expect

@pytest.mark.e2e
async def test_user_login_page_loads(page):
    """Test that the login page loads correctly."""
    # Navigate to the login page
    await page.goto("http://localhost:8000/login")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Login")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='Email']")).to_be_visible()
    await expect(page.locator("input[placeholder='Password']")).to_be_visible()
    await expect(page.locator("button:has-text('Sign In')")).to_be_visible()

@pytest.mark.e2e
async def test_user_registration_page_loads(page):
    """Test that the registration page loads correctly."""
    # Navigate to the registration page
    await page.goto("http://localhost:8000/register")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Register")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='First Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Last Name']")).to_be_visible()
    await expect(page.locator("input[placeholder='Email']")).to_be_visible()
    await expect(page.locator("input[placeholder='Password']")).to_be_visible()
    await expect(page.locator("input[placeholder='Confirm Password']")).to_be_visible()
    await expect(page.locator("button:has-text('Create Account')")).to_be_visible()

@pytest.mark.e2e
async def test_password_reset_page_loads(page):
    """Test that the password reset page loads correctly."""
    # Navigate to the password reset page
    await page.goto("http://localhost:8000/forgot-password")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Forgot Password")).to_be_visible()

    # Check that the form elements are present
    await expect(page.locator("input[placeholder='Email']")).to_be_visible()
    await expect(page.locator("button:has-text('Reset Password')")).to_be_visible()