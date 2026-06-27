"""
Service repository interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.service import Service


class ServiceRepository(ABC):
    """Abstract base class for service repository."""
    
    @abstractmethod
    async def create(self, service: Service) -> Service:
        """Create a new service."""
        pass
    
    @abstractmethod
    async def get_by_id(self, service_id: str) -> Optional[Service]:
        """Get service by ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str, tenant_id: str) -> Optional[Service]:
        """Get service by name and tenant ID."""
        pass
    
    @abstractmethod
    async def update(self, service: Service) -> Service:
        """Update an existing service."""
        pass
    
    @abstractmethod
    async def delete(self, service_id: str) -> bool:
        """Delete a service by ID."""
        pass
    
    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Service]:
        """List services with pagination."""
        pass
    
    @abstractmethod
    async def search(self, tenant_id: str, query: str, limit: int = 50) -> List[Service]:
        """Search services by name or description."""
        pass
