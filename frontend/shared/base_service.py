"""
Abstract base class for API services.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseApiService(ABC):
    """Abstract base class for API services."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        pass

    @abstractmethod
    def post(self, endpoint: str, data: Any) -> Any:
        """Make a POST request."""
        pass

    @abstractmethod
    def put(self, endpoint: str, data: Any) -> Any:
        """Make a PUT request."""
        pass

    @abstractmethod
    def delete(self, endpoint: str) -> Any:
        """Make a DELETE request."""
        pass

    def _build_url(self, endpoint: str) -> str:
        """Build a full URL from the base URL and endpoint."""
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"