"""
Barber repository interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.barber import Barber


class BarberRepository(ABC):
    """Abstract base class for barber repository."""

    @abstractmethod
    async def create(self, barber: Barber) -> Barber:
        """Create a new barber."""
        pass

    @abstractmethod
    async def get_by_id(self, barber_id: str) -> Optional[Barber]:
        """Get barber by ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Barber]:
        """Get barber by email and tenant ID."""
        pass

    @abstractmethod
    async def update(self, barber: Barber) -> Barber:
        """Update an existing barber."""
        pass

    @abstractmethod
    async def delete(self, barber_id: str) -> bool:
        """Delete a barber by ID."""
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Barber]:
        """List barbers with pagination."""
        pass

    @abstractmethod
    async def search(self, tenant_id: str, query: str, limit: int = 50) -> List[Barber]:
        """Search barbers by name, email, or specialty."""
        pass