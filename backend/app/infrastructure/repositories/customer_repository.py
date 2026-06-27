"""
SQLAlchemy implementation of customer repository.
"""
from typing import List, Optional
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.customer import Customer
from app.domain.repositories.customer_repository import CustomerRepository
from app.infrastructure.database.models import CustomerModel


class CustomerRepositoryImpl(CustomerRepository):
    """SQLAlchemy implementation of customer repository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        # Convert entity to model
        db_customer = CustomerModel(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone=customer.phone,
            date_of_birth=customer.date_of_birth,
            notes=customer.notes,
            tenant_id=customer.tenant_id,
            is_active=getattr(customer, 'is_active', True),
            created_at=customer.created_at,
            updated_at=customer.updated_at
        )
        
        # Add to session and commit
        self.session.add(db_customer)
        await self.session.commit()
        await self.session.refresh(db_customer)
        
        # Convert back to entity
        return db_customer.to_entity()
    
    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        query = select(CustomerModel).where(CustomerModel.id == customer_id)
        result = await self.session.execute(query)
        db_customer = result.scalar_one_or_none()
        
        return db_customer.to_entity() if db_customer else None
    
    async def get_by_email(self, email: str, tenant_id: str) -> Optional[Customer]:
        """Get customer by email and tenant ID."""
        query = select(CustomerModel).where(
            and_(
                CustomerModel.email == email,
                CustomerModel.tenant_id == tenant_id
            )
        )
        result = await self.session.execute(query)
        db_customer = result.scalar_one_or_none()
        
        return db_customer.to_entity() if db_customer else None
    
    async def update(self, customer: Customer) -> Customer:
        """Update an existing customer."""
        # Update the customer in the database
        stmt = (
            update(CustomerModel)
            .where(CustomerModel.id == customer.id)
            .values(
                first_name=customer.first_name,
                last_name=customer.last_name,
                email=customer.email,
                phone=customer.phone,
                date_of_birth=customer.date_of_birth,
                notes=customer.notes,
                updated_at=customer.updated_at
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        # Return updated customer
        return await self.get_by_id(customer.id)
    
    async def delete(self, customer_id: str) -> bool:
        """Delete a customer by ID."""
        stmt = delete(CustomerModel).where(CustomerModel.id == customer_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """List customers with pagination."""
        query = select(CustomerModel).offset(skip).limit(limit)
        result = await self.session.execute(query)
        db_customers = result.scalars().all()
        
        return [customer.to_entity() for customer in db_customers]
    
    async def search(self, tenant_id: str, query: str, limit: int = 50) -> List[Customer]:
        """Search customers by name, email, or phone."""
        search_term = f"%{query}%"
        stmt = select(CustomerModel).where(
            and_(
                CustomerModel.tenant_id == tenant_id,
                or_(
                    CustomerModel.first_name.ilike(search_term),
                    CustomerModel.last_name.ilike(search_term),
                    CustomerModel.email.ilike(search_term),
                    CustomerModel.phone.ilike(search_term)
                )
            )
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        db_customers = result.scalars().all()
        
        return [customer.to_entity() for customer in db_customers]
