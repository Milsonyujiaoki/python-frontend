"""
Barber domain entity.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Barber:
    """Barber entity representing a barbershop employee/barber."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        specialty: Optional[str] = None,
        bio: Optional[str] = None,
        is_active: bool = True,
        tenant_id: str = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.specialty = specialty
        self.bio = bio
        self.is_active = is_active
        self.tenant_id = tenant_id or "default_tenant"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<Barber {self.id}: {self.first_name} {self.last_name}>"