"""
Customer domain entity.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Customer:
    """Customer entity representing a barbershop customer."""
    
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        date_of_birth: Optional[datetime] = None,
        notes: Optional[str] = None,
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
        self.date_of_birth = date_of_birth
        self.notes = notes
        self.tenant_id = tenant_id or "default_tenant"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Customer {self.id}: {self.first_name} {self.last_name}>"
