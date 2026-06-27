"""
Barber service containing business logic.
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.barber import Barber
from ...domain.repositories.barber_repository import BarberRepository
from ...application.dto.barber_dto import BarberCreate, BarberUpdate, BarberResponse


class BarberService:
    """Barber service for handling barber-related business logic."""

    def __init__(self, repository: BarberRepository):
        self.repository = repository

    async def create_barber(self, barber_data: BarberCreate) -> BarberResponse:
        """Create a new barber."""
        # Check if barber with email already exists
        existing = await self.repository.get_by_email(
            barber_data.email,
            # In a real app, we'd get tenant_id from auth context
            "default_tenant"
        )
        if existing:
            raise ValueError(f"Barber with email {barber_data.email} already exists")

        # Create barber entity
        barber = Barber(
            first_name=barber_data.first_name,
            last_name=barber_data.last_name,
            email=barber_data.email,
            phone=barber_data.phone,
            specialty=barber_data.specialty,
            bio=barber_data.bio,
            is_active=barber_data.is_active if barber_data.is_active is not None else True,
            tenant_id="default_tenant"  # Would come from auth context
        )

        # Save to database
        created_barber = await self.repository.create(barber)

        # Return response DTO
        return BarberResponse.from_orm(created_barber)

    async def get_barber(self, barber_id: str) -> Optional[BarberResponse]:
        """Get a barber by ID."""
        barber = await self.repository.get_by_id(barber_id)
        if not barber:
            return None
        return BarberResponse.from_orm(barber)

    async def update_barber(self, barber_id: str, barber_data: BarberUpdate) -> Optional[BarberResponse]:
        """Update an existing barber."""
        # Get existing barber
        existing = await self.repository.get_by_id(barber_id)
        if not existing:
            return None

        # Check email uniqueness if email is being updated
        if barber_data.email and barber_data.email != existing.email:
            email_exists = await self.repository.get_by_email(
                barber_data.email,
                existing.tenant_id
            )
            if email_exists and email_exists.id != existing.id:
                raise ValueError(f"Barber with email {barber_data.email} already exists")

        # Update fields
        update_data = barber_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing, field, value)

        # Update timestamp
        existing.update_timestamp()

        # Save to database
        updated_barber = await self.repository.update(existing)

        return BarberResponse.from_orm(updated_barber)

    async def delete_barber(self, barber_id: str) -> bool:
        """Delete a barber."""
        return await self.repository.delete(barber_id)

    async def list_barbers(self, skip: int = 0, limit: int = 100) -> List[BarberResponse]:
        """List barbers with pagination."""
        barbers = await self.repository.list(skip, limit)
        return [BarberResponse.from_orm(barber) for barber in barbers]

    async def search_barbers(self, tenant_id: str, query: str, limit: int = 50) -> List[BarberResponse]:
        """Search barbers by name, email, or specialty."""
        barbers = await self.repository.search(tenant_id, query, limit)
        return [BarberResponse.from_orm(barber) for barber in barbers]