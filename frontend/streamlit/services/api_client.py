"""API client for Streamlit application."""

import httpx
from typing import Optional, Any


class APIClient:
    """HTTP client for backend API communication."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0

    async def _request(
        self, method: str, endpoint: str, data: Optional[dict] = None
    ) -> Any:
        """Make HTTP request to backend API."""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            else:
                raise ValueError(f"Unknown HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    # Customer endpoints
    async def get_customers(self) -> list[dict]:
        """Fetch all customers."""
        return await self._request("GET", "/api/customers")

    async def get_customer(self, customer_id: int) -> dict:
        """Fetch a single customer by ID."""
        return await self._request("GET", f"/api/customers/{customer_id}")

    async def create_customer(self, data: dict) -> dict:
        """Create a new customer."""
        return await self._request("POST", "/api/customers", data)

    async def update_customer(self, customer_id: int, data: dict) -> dict:
        """Update an existing customer."""
        return await self._request("PUT", f"/api/customers/{customer_id}", data)

    async def delete_customer(self, customer_id: int) -> dict:
        """Delete a customer."""
        return await self._request("DELETE", f"/api/customers/{customer_id}")

    # Barber endpoints
    async def get_barbers(self) -> list[dict]:
        """Fetch all barbers."""
        return await self._request("GET", "/api/barbers")

    async def get_barber(self, barber_id: int) -> dict:
        """Fetch a single barber by ID."""
        return await self._request("GET", f"/api/barbers/{barber_id}")

    async def create_barber(self, data: dict) -> dict:
        """Create a new barber."""
        return await self._request("POST", "/api/barbers", data)

    async def update_barber(self, barber_id: int, data: dict) -> dict:
        """Update an existing barber."""
        return await self._request("PUT", f"/api/barbers/{barber_id}", data)

    async def delete_barber(self, barber_id: int) -> dict:
        """Delete a barber."""
        return await self._request("DELETE", f"/api/barbers/{barber_id}")

    # Service endpoints
    async def get_services(self) -> list[dict]:
        """Fetch all services."""
        return await self._request("GET", "/api/services")

    async def get_service(self, service_id: int) -> dict:
        """Fetch a single service by ID."""
        return await self._request("GET", f"/api/services/{service_id}")

    async def create_service(self, data: dict) -> dict:
        """Create a new service."""
        return await self._request("POST", "/api/services", data)

    async def update_service(self, service_id: int, data: dict) -> dict:
        """Update an existing service."""
        return await self._request("PUT", f"/api/services/{service_id}", data)

    async def delete_service(self, service_id: int) -> dict:
        """Delete a service."""
        return await self._request("DELETE", f"/api/services/{service_id}")

    # Auth endpoints
    async def login(self, email: str, password: str) -> dict:
        """Login with email and password."""
        return await self._request(
            "POST", "/api/auth/login", {"email": email, "password": password}
        )

    async def logout(self) -> dict:
        """Logout current user."""
        return await self._request("POST", "/api/auth/logout")


# Singleton instance for Streamlit session state
def get_api_client() -> APIClient:
    """Get or create API client instance."""
    if "api_client" not in st.session_state:
        import streamlit as st

        st.session_state.api_client = APIClient()
    return st.session_state.api_client