"""
Customer repository interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.customer import Customer


class CustomerRepository(ABC):
    """Abstract base class for customer repository."""
    
    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        pass
    
    @abstractmethod
    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Customer]:
        """Get customer by email and tenant ID."""
        pass
    
    @abstractmethod
    async def update(self, customer: Customer) -> Customer:
        """Update an existing customer."""
        pass
    
    @abstractmethod
    async def delete(self, customer_id: str) -> bool:
        """Delete a customer by ID."""
        pass
    
    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """List customers with pagination."""
        pass
    
    @abstractmethod
    async def search(self, tenant_id: str, query: str, limit: int = 50) -> List[Customer]:
        """Search customers by name, email, or phone."""
        pass
