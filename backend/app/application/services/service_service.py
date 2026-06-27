"""
Service service containing business logic.
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.service import Service
from ...domain.repositories.service_repository import ServiceRepository
from ...application.dto.service_dto import ServiceCreate, ServiceUpdate, ServiceResponse


class ServiceService:
    """Service service for handling service-related business logic."""
    
    def __init__(self, repository: ServiceRepository):
        self.repository = repository
    
    async def create_service(self, service_data: ServiceCreate) -> ServiceResponse:
        """Create a new service."""
        # Check if service with name already exists for the tenant
        existing = await self.repository.get_by_name(
            service_data.name,
            # In a real app, we'd get tenant_id from auth context
            "default_tenant"
        )
        if existing:
            raise ValueError(f"Service with name {service_data.name} already exists")
        
        # Create service entity
        service = Service(
            name=service_data.name,
            description=service_data.description,
            price=service_data.price,
            duration_minutes=service_data.duration_minutes,
            is_active=service_data.is_active,
            tenant_id="default_tenant"  # Would come from auth context
        )
        
        # Save to database
        created_service = await self.repository.create(service)
        
        # Return response DTO
        return ServiceResponse.from_orm(created_service)
    
    async def get_service(self, service_id: str) -> Optional[ServiceResponse]:
        """Get a service by ID."""
        service = await self.repository.get_by_id(service_id)
        if not service:
            return None
        return ServiceResponse.from_orm(service)
    
    async def update_service(self, service_id: str, service_data: ServiceUpdate) -> Optional[ServiceResponse]:
        """Update an existing service."""
        # Get existing service
        existing = await self.repository.get_by_id(service_id)
        if not existing:
            return None
        
        # Check name uniqueness if name is being updated
        if service_data.name and service_data.name != existing.name:
            name_exists = await self.repository.get_by_name(
                service_data.name,
                existing.tenant_id
            )
            if name_exists and name_exists.id != existing.id:
                raise ValueError(f"Service with name {service_data.name} already exists")
        
        # Update fields
        update_data = service_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing, field, value)
        
        # Update timestamp
        existing.update_timestamp()
        
        # Save to database
        updated_service = await self.repository.update(existing)
        
        return ServiceResponse.from_orm(updated_service)
    
    async def delete_service(self, service_id: str) -> bool:
        """Delete a service."""
        return await self.repository.delete(service_id)
    
    async def list_services(self, skip: int = 0, limit: int = 100) -> List[ServiceResponse]:
        """List services with pagination."""
        services = await self.repository.list(skip, limit)
        return [ServiceResponse.from_orm(service) for service in services]
    
    async def search_services(self, tenant_id: str, query: str, limit: int = 50) -> List[ServiceResponse]:
        """Search services by name or description."""
        services = await self.repository.search(tenant_id, query, limit)
        return [ServiceResponse.from_orm(service) for service in services]
