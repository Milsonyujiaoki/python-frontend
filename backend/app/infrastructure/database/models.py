"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class CustomerModel(Base):
    """SQLAlchemy model for Customer entity."""
    
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    tenant_id = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indexes for common query patterns
    __table_args__ = (
        Index('ix_customers_tenant_id', 'tenant_id'),
        Index('ix_customers_email_tenant', 'email', 'tenant_id'),
        Index('ix_customers_name', 'first_name', 'last_name'),
    )
    
    def to_entity(self):
        """Convert SQLAlchemy model to domain entity."""
        from ....domain.entities.customer import Customer
        return Customer(
            id=str(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            date_of_birth=self.date_of_birth,
            notes=self.notes,
            tenant_id=self.tenant_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_entity(self, customer):
        """Create SQLAlchemy model from domain entity."""
        return CustomerModel(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone=customer.phone,
            date_of_birth=customer.date_of_birth,
            notes=customer.notes,
            tenant_id=tenant_id,
            is_active=getattr(customer, 'is_active', True),
            created_at=customer.created_at,
            updated_at=customer.updated_at
        )
