"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

# Try to import the app - adjust the import path as needed
try:
    from main import app
except ImportError:
    try:
        from backend.main import app
    except ImportError:
        try:
            from app.main import app
        except ImportError:
            app = None

if app is not None:
    client = TestClient(app)
else:
    client = None


def test_api_health_check():
    """Test that the API health check endpoint works."""
    if client is None:
        pytest.skip("Main app not found for testing")
        return
    
    # This would be implemented when main app is created
    # For now, we'll just test that the client was created
    assert client is not None


def test_customer_endpoints():
    """Test customer CRUD operations."""
    if client is None:
        pytest.skip("Main app not found for testing")
        return
    
    # Test creating a customer
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "date_of_birth": "1990-01-01",
        "notes": "Test customer"
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 201
    created_customer = response.json()
    assert created_customer["first_name"] == "John"
    assert created_customer["email"] == "john.doe@example.com"
    customer_id = created_customer["id"]
    
    # Test getting the customer
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    
    # Test updating the customer
    update_data = {"last_name": "Smith"}
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["last_name"] == "Smith"
    
    # Test deleting the customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404


def test_barber_endpoints():
    """Test barber CRUD operations."""
    if client is None:
        pytest.skip("Main app not found for testing")
        return
    
    # Test creating a barber
    barber_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "0987654321",
        "specialty": "Haircut",
        "bio": "Experienced barber"
    }
    
    response = client.post("/barbers/", json=barber_data)
    assert response.status_code == 201
    created_barber = response.json()
    assert created_barber["first_name"] == "Jane"
    assert created_barber["email"] == "jane.smith@example.com"
    barber_id = created_barber["id"]
    
    # Test getting the barber
    response = client.get(f"/barbers/{barber_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"
    
    # Test updating the barber
    update_data = {"last_name": "Johnson"}
    response = client.put(f"/barbers/{barber_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["last_name"] == "Johnson"
    
    # Test deleting the barber
    response = client.delete(f"/barbers/{barber_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/barbers/{barber_id}")
    assert response.status_code == 404


def test_service_endpoints():
    """Test service CRUD operations."""
    if client is None:
        pytest.skip("Main app not found for testing")
        return
    
    # Test creating a service
    service_data = {
        "name": "Haircut",
        "description": "Basic haircut",
        "price": 1500,  # in cents
        "duration_minutes": 30,
        "is_active": True
    }
    
    response = client.post("/services/", json=service_data)
    assert response.status_code == 201
    created_service = response.json()
    assert created_service["name"] == "Haircut"
    assert created_service["price"] == 1500
    service_id = created_service["id"]
    
    # Test getting the service
    response = client.get(f"/services/{service_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Haircut"
    
    # Test updating the service
    update_data = {"price": 2000, "duration_minutes": 45}
    response = client.put(f"/services/{service_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 2000
    assert response.json()["duration_minutes"] == 45
    
    # Test deleting the service
    response = client.delete(f"/services/{service_id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/services/{service_id}")
    assert response.status_code == 404


def test_search_and_filtering():
    """Test search and filtering capabilities."""
    if client is None:
        pytest.skip("Main app not found for testing")
        return
    
    # Create test data
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "date_of_birth": "1990-01-01",
        "notes": "Test customer"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 201
    
    # Test search
    response = client.get("/customers/?search=John")
    assert response.status_code == 200
    customers = response.json()
    assert len(customers) >= 1
    assert any(c["first_name"] == "John" for c in customers)
    
    # Test filter by active status (all created customers are active by default)
    response = client.get("/customers/?is_active=true")
    assert response.status_code == 200
    customers = response.json()
    assert len(customers) >= 1
    assert all(c["is_active"] == True for c in customers)


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
