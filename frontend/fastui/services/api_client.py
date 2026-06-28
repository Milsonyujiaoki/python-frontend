"""
API service for FastUI frontend.

Provides HTTP client functionality for communicating with the backend API.
"""

import httpx
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class APIResponse:
    """Response wrapper for API calls."""
    data: Any
    status_code: int
    error: Optional[str] = None


class APIClient:
    """
    HTTP client for API communication.

    Features:
    - Base URL configuration
    - Automatic JSON parsing
    - Error handling
    - Request/response logging
    """

    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=10.0,
                headers={"Accept": "application/json"},
            )
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """Make a GET request."""
        client = await self.get_client()
        try:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            return APIResponse(
                data=response.json(),
                status_code=response.status_code,
            )
        except httpx.HTTPStatusError as e:
            return APIResponse(
                data=None,
                status_code=e.response.status_code,
                error=str(e),
            )
        except httpx.RequestError as e:
            return APIResponse(
                data=None,
                status_code=0,
                error=str(e),
            )

    async def post(self, endpoint: str, data: Dict) -> APIResponse:
        """Make a POST request."""
        client = await self.get_client()
        try:
            response = await client.post(endpoint, json=data)
            response.raise_for_status()
            return APIResponse(
                data=response.json(),
                status_code=response.status_code,
            )
        except httpx.HTTPStatusError as e:
            return APIResponse(
                data=None,
                status_code=e.response.status_code,
                error=str(e),
            )
        except httpx.RequestError as e:
            return APIResponse(
                data=None,
                status_code=0,
                error=str(e),
            )

    async def put(self, endpoint: str, data: Dict) -> APIResponse:
        """Make a PUT request."""
        client = await self.get_client()
        try:
            response = await client.put(endpoint, json=data)
            response.raise_for_status()
            return APIResponse(
                data=response.json(),
                status_code=response.status_code,
            )
        except httpx.HTTPStatusError as e:
            return APIResponse(
                data=None,
                status_code=e.response.status_code,
                error=str(e),
            )
        except httpx.RequestError as e:
            return APIResponse(
                data=None,
                status_code=0,
                error=str(e),
            )

    async def delete(self, endpoint: str) -> APIResponse:
        """Make a DELETE request."""
        client = await self.get_client()
        try:
            response = await client.delete(endpoint)
            response.raise_for_status()
            return APIResponse(
                data=None,
                status_code=response.status_code,
            )
        except httpx.HTTPStatusError as e:
            return APIResponse(
                data=None,
                status_code=e.response.status_code,
                error=str(e),
            )
        except httpx.RequestError as e:
            return APIResponse(
                data=None,
                status_code=0,
                error=str(e),
            )


# Global API client instance
api_client = APIClient()


# Convenience functions for common operations
async def fetch_customers() -> APIResponse:
    """Fetch all customers."""
    return await api_client.get("/customers")


async def fetch_customer(customer_id: int) -> APIResponse:
    """Fetch a single customer by ID."""
    return await api_client.get(f"/customers/{customer_id}")


async def create_customer(data: Dict) -> APIResponse:
    """Create a new customer."""
    return await api_client.post("/customers", data)


async def update_customer(customer_id: int, data: Dict) -> APIResponse:
    """Update an existing customer."""
    return await api_client.put(f"/customers/{customer_id}", data)


async def delete_customer(customer_id: int) -> APIResponse:
    """Delete a customer."""
    return await api_client.delete(f"/customers/{customer_id}")


async def fetch_barbers() -> APIResponse:
    """Fetch all barbers."""
    return await api_client.get("/barbers")


async def fetch_barber(barber_id: int) -> APIResponse:
    """Fetch a single barber by ID."""
    return await api_client.get(f"/barbers/{barber_id}")


async def create_barber(data: Dict) -> APIResponse:
    """Create a new barber."""
    return await api_client.post("/barbers", data)


async def update_barber(barber_id: int, data: Dict) -> APIResponse:
    """Update an existing barber."""
    return await api_client.put(f"/barbers/{barber_id}", data)


async def delete_barber(barber_id: int) -> APIResponse:
    """Delete a barber."""
    return await api_client.delete(f"/barbers/{barber_id}")


async def fetch_services() -> APIResponse:
    """Fetch all services."""
    return await api_client.get("/services")


async def fetch_service(service_id: int) -> APIResponse:
    """Fetch a single service by ID."""
    return await api_client.get(f"/services/{service_id}")


async def create_service(data: Dict) -> APIResponse:
    """Create a new service."""
    return await api_client.post("/services", data)


async def update_service(service_id: int, data: Dict) -> APIResponse:
    """Update an existing service."""
    return await api_client.put(f"/services/{service_id}", data)


async def delete_service(service_id: int) -> APIResponse:
    """Delete a service."""
    return await api_client.delete(f"/services/{service_id}")