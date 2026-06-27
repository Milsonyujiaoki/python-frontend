"""
Customer service containing business logic.
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.customer import Customer
from ...domain.repositories.customer_repository import CustomerRepository
from ...application.dto.customer_dto import CustomerCreate, CustomerUpdate, CustomerResponse


class CustomerService:
    """Customer service for handling customer-related business logic."""
    
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    
    async def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Create a new customer."""
        # Check if customer with email already exists
        existing = await self.repository.get_by_email(
            customer_data.email, 
            # In a real app, we'd get tenant_id from auth context
            "default_tenant"  
        )
        if existing:
            raise ValueError(f"Customer with email {customer_data.email} already exists")
        
        # Create customer entity
        customer = Customer(
            first_name=customer_data.first_name,
            last_name=customer_data.last_name,
            email=customer_data.email,
            phone=customer_data.phone,
            date_of_birth=customer_data.date_of_birth,
            notes=customer_data.notes,
            tenant_id="default_tenant"  # Would come from auth context
        )
        
        # Save to database
        created_customer = await self.repository.create(customer)
        
        # Return response DTO
        return CustomerResponse.from_orm(created_customer)
    
    async def get_customer(self, customer_id: str) -> Optional[CustomerResponse]:
        """Get a customer by ID."""
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            return None
        return CustomerResponse.from_orm(customer)
    
    async def update_customer(self, customer_id: str, customer_data: CustomerUpdate) -> Optional[CustomerResponse]:
        """Update an existing customer."""
        # Get existing customer
        existing = await self.repository.get_by_id(customer_id)
        if not existing:
            return None
        
        # Check email uniqueness if email is being updated
        if customer_data.email and customer_data.email != existing.email:
            email_exists = await self.repository.get_by_email(
                customer_data.email, 
                existing.tenant_id
            )
            if email_exists and email_exists.id != existing.id:
                raise ValueError(f"Customer with email {customer_data.email} already exists")
        
        # Update fields
        update_data = customer_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(external, field, value)
        
        # Update timestamp
        customer.update_timestamp()
        
        # Save to database
        updated_customer = await self.repository.update(customer)
        
        return CustomerResponse.from_orm(updated_customer)
    
    async def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer."""
        return await self.repository.delete(customer_id)
    
    async def list_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerResponse]:
        """List customers with pagination."""
        customers = await self.repository.list(skip, limit)
        return [CustomerResponse.from_orm(customer) for customer in customers]
    
    async def search_customers(self, tenant_id: str, query: str, limit: int = 50) -> List[CustomerResponse]:
        """Search customers by name or email."""
        customers = await self.repository.search(tenant_id, query, limit)
        return [CustomerResponse.from_orm(customer) for customer in customers]
