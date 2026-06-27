"""
Service domain entity.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Service:
    """Service entity representing a service offered by the barbershop."""
    
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        duration_minutes: int,
        tenant_id: str,
        is_active: bool = True,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.price = price
        self.duration_minutes = duration_minutes
        self.tenant_id = tenant_id
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
        
    def __repr__(self):
        return f"<Service {self.id}: {self.name}>"
