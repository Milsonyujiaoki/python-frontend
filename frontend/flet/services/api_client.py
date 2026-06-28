"""API client for Flet application."""

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

    async def get_customers(self) -> list[dict]:
        return await self._request("GET", "/api/customers")

    async def create_customer(self, data: dict) -> dict:
        return await self._request("POST", "/api/customers", data)

    async def update_customer(self, customer_id: int, data: dict) -> dict:
        return await self._request("PUT", f"/api/customers/{customer_id}", data)

    async def delete_customer(self, customer_id: int) -> dict:
        return await self._request("DELETE", f"/api/customers/{customer_id}")

    async def get_barbers(self) -> list[dict]:
        return await self._request("GET", "/api/barbers")

    async def create_barber(self, data: dict) -> dict:
        return await self._request("POST", "/api/barbers", data)

    async def get_services(self) -> list[dict]:
        return await self._request("GET", "/api/services")

    async def create_service(self, data: dict) -> dict:
        return await self._request("POST", "/api/services", data)

    async def login(self, email: str, password: str) -> dict:
        return await self._request("POST", "/api/auth/login", {"email": email, "password": password})
