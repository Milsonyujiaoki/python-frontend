"""
Configuration and fixtures for FastUI E2E tests.
"""

import pytest
from playwright.async_api import async_playwright, BrowserContext, Page

# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
async def browser():
    """Create a browser instance for the test session."""
    async with async_playwright() as p:
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