"""Pytest configuration and fixtures for Streamlit tests."""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the streamlit directory to the path for imports
streamlit_dir = Path(__file__).parent.parent
sys.path.insert(0, str(streamlit_dir))


@pytest.fixture
def mock_streamlit_session_state():
    """Mock Streamlit session state for testing."""
    mock_state = {}

    with patch("streamlit.session_state", mock_state):
        yield mock_state


@pytest.fixture
def sample_customers():
    """Sample customer data for testing."""
    return [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "status": "Active",
            "last_visit": "2026-06-25",
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "+1234567891",
            "status": "VIP",
            "last_visit": "2026-06-26",
        },
        {
            "id": 3,
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "phone": "+1234567892",
            "status": "Inactive",
            "last_visit": "2026-06-20",
        },
    ]


@pytest.fixture
def sample_barbers():
    """Sample barber data for testing."""
    return [
        {
            "id": 1,
            "name": "Mike Johnson",
            "email": "mike@barbershop.com",
            "phone": "+1234567890",
            "specialty": "Classic Cuts, Beard Trim",
            "status": "Active",
            "rating": 4.9,
        },
        {
            "id": 2,
            "name": "Sarah Williams",
            "email": "sarah@barbershop.com",
            "phone": "+1234567891",
            "specialty": "Coloring, Styling",
            "status": "Active",
            "rating": 4.8,
        },
    ]


@pytest.fixture
def sample_services():
    """Sample service data for testing."""
    return [
        {
            "id": 1,
            "name": "Classic Haircut",
            "description": "Traditional haircut with scissor over comb",
            "price": 35.00,
            "duration": 30,
            "category": "Hair",
            "active": True,
        },
        {
            "id": 2,
            "name": "Beard Trim & Shape",
            "description": "Professional beard trimming and shaping",
            "price": 20.00,
            "duration": 20,
            "category": "Beard",
            "active": True,
        },
        {
            "id": 3,
            "name": "Full Color",
            "description": "Complete hair coloring service",
            "price": 80.00,
            "duration": 90,
            "category": "Coloring",
            "active": True,
        },
    ]


@pytest.fixture
def mock_api_response():
    """Mock API response for testing."""
    return {
        "success": True,
        "data": [],
        "message": "Operation completed successfully",
    }


@pytest.fixture
def mock_httpx_client():
    """Mock httpx AsyncClient for testing API calls."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_auth_credentials():
    """Sample authentication credentials for testing."""
    return {"email": "admin@barbershop.com", "password": "password123"}


@pytest.fixture
def sample_jwt_token():
    """Sample JWT token for testing."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


# Marker configuration
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")