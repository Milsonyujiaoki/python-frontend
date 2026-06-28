"""
End-to-end tests for dashboard and navigation flows in Solara frontend.
"""
import pytest
import re
from playwright.async_api import expect

@pytest.mark.e2e
async def test_dashboard_page_loads_authenticated(page, authenticated_user):
    """Test that the dashboard page loads correctly for authenticated user."""
    await page.goto("http://localhost:8000/dashboard")

    # Check that the page title or heading is correct
    await expect(page.locator("text=Dashboard")).to_be_visible()

    # Check that key dashboard elements are present
    # These would vary based on the actual dashboard implementation
    await expect(page.locator("text=Total Customers")).to_be_visible()
    await expect(page.locator("text=Total Barbers")).to_be_visible()
    await expect(page.locator("text=Total Services")).to_be_visible()

@pytest.mark.e2e
async def test_navigation_sidebar_links(page, authenticated_user):
    """Test that navigation sidebar links work correctly."""
    await page.goto("http://localhost:8000/dashboard")

    # Check that navigation elements are present
    await expect(page.locator("text=Customers")).to_be_visible()
    await expect(page.locator("text=Barbers")).to_be_visible()
    await expect(page.locator("text=Services")).to_be_visible()
    await expect(page.locator("text=Dashboard")).to_be_visible()

    # Test clicking on navigation links
    await page.click("text=Customers")
    await expect(page).to_have_url(re.compile(r".*/customers"))

    await page.click("text=Barbers")
    await expect(page).to_have_url(re.compile(r".*/barbers"))

    await page.click("text=Services")
    await expect(page).to_have_url(re.compile(r".*/services"))

    await page.click("text=Dashboard")
    await expect(page).to_have_url(re.compile(r".*/dashboard"))

@pytest.mark.e2e
async def test_user_profile_navigation(page, authenticated_user):
    """Test that user profile navigation works correctly."""
    await page.goto("http://localhost:8000/dashboard")

    # Look for user profile or account menu
    # This would depend on the actual implementation
    await expect(page.locator("text=Profile")).to_be_visible()
    await expect(page.locator("text=Account")).to_be_visible()
    await expect(page.locator("text=Logout")).to_be_visible()

    # Test clicking on logout
    await page.click("text=Logout")
    # After logout, should redirect to login page
    await expect(page).to_have_url(re.compile(r".*/login"))