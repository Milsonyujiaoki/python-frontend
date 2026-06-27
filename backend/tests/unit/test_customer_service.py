"""
Unit tests for CustomerService.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest
from uuid import uuid4
from datetime import datetime

from backend.application.services.customer_service import CustomerService
from backend.application.dto.customer_dto import CustomerCreate, CustomerUpdate, CustomerResponse
from backend.domain.entities.customer import Customer


@pytest.fixture
def mock_repository():
    """Create a mock customer repository."""
    return AsyncMock()


@pytest.fixture
def customer_service(mock_repository):
    """Create a customer service instance with a mock repository."""
    return CustomerService(repository=mock_repository)


@pytest.fixture
def sample_customer_data():
    """Return a sample customer create data."""
    return CustomerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1),
        notes="Test customer"
    )


@pytest.mark.asyncio
async def test_create_customer_success(customer_service, mock_repository, sample_customer_data):
    """Test creating a customer successfully."""
    # Mock the repository to return no existing customer with the email
    mock_repository.get_by_email.return_value = None
    # Mock the repository create method to return a customer entity
    created_customer = Customer(
        id=str(uuid4()),
        first_name=sample_customer_data.first_name,
        last_name=sample_customer_data.last_name,
        email=sample_customer_data.email,
        phone=sample_customer_data.phone,
        date_of_birth=sample_customer_data.date_of_birth,
        notes=sample_customer_data.notes,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.create.return_value = created_customer

    # Call the service method
    result = await customer_service.create_customer(sample_customer_data)

    # Assertions
    assert isinstance(result, CustomerResponse)
    assert result.first_name == sample_customer_data.first_name
    assert result.last_name == sample_customer_data.last_name
    assert result.email == sample_customer_data.email
    assert result.phone == sample_customer_data.phone
    assert result.date_of_birth == sample_customer_data.date_of_birth
    assert result.notes == sample_customer_data.notes
    assert result.tenant_id == "default_tenant"
    mock_repository.get_by_email.assert_called_once_with(
        sample_customer_data.email, "default_tenant"
    )
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_customer_email_exists(customer_service, mock_repository, sample_customer_data):
    """Test creating a customer when email already exists."""
    # Mock the repository to return an existing customer with the email
    existing_customer = Customer(
        id=str(uuid4()),
        first_name="Jane",
        last_name="Doe",
        email=sample_customer_data.email,
        phone="0987654321",
        date_of_birth=datetime(1992, 2, 2),
        notes="Existing customer",
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_email.return_value = existing_customer

    # Call the service method and expect an exception
    with pytest.raises(ValueError, match=f"Customer with email {sample_customer_data.email} already exists"):
        await customer_service.create_customer(sample_customer_data)

    # Assertions
    mock_repository.get_by_email.assert_called_once_with(
        sample_customer_data.email, "default_tenant"
    )
    mock_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_get_customer_found(customer_service, mock_repository):
    """Test getting a customer by ID when it exists."""
    # Mock the repository to return a customer
    customer_id = str(uuid4())
    customer = Customer(
        id=customer_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1),
        notes="Test customer",
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = customer

    # Call the service method
    result = await customer_service.get_customer(customer_id)

    # Assertions
    assert isinstance(result, CustomerResponse)
    assert result.id == customer_id
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "john.doe@example.com"
    mock_repository.get_by_id.assert_called_once_with(customer_id)


@pytest.mark.asyncio
async def test_get_customer_not_found(customer_service, mock_repository):
    """Test getting a customer by ID when it does not exist."""
    # Mock the repository to return None
    customer_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Call the service method
    result = await customer_service.get_customer(customer_id)

    # Assertions
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(customer_id)


@pytest.mark.asyncio
async def test_update_customer_success(customer_service, mock_repository):
    """Test updating a customer successfully."""
    # Mock the repository to return an existing customer
    customer_id = str(uuid4())
    existing_customer = Customer(
        id=customer_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1),
        notes="Test customer",
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = existing_customer
    # Mock the repository update method to return the updated customer
    updated_customer = Customer(
        id=customer_id,
        first_name="John",
        last_name="Smith",  # Changed last name
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1),
        notes="Test customer",
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.update.return_value = updated_customer

    # Prepare the update data
    update_data = CustomerUpdate(last_name="Smith")

    # Call the service method
    result = await customer_service.update_customer(customer_id, update_data)

    # Assertions
    assert isinstance(result, CustomerResponse)
    assert result.id == customer_id
    assert result.first_name == "John"
    assert result.last_name == "Smith"
    assert result.email == "john.doe@example.com"
    mock_repository.get_by_id.assert_called_once_with(customer_id)
    mock_repository.update.assert_called_once()
    # Check that the update method was called with a customer object that has the updated last name
    args, _ = mock_repository.update.call_args
    updated_customer_arg = args[0]
    assert updated_customer_arg.last_name == "Smith"


@pytest.mark.asyncio
async def test_update_customer_not_found(customer_service, mock_repository):
    """Test updating a customer that does not exist."""
    # Mock the repository to return None
    customer_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Prepare the update data
    update_data = CustomerUpdate(last_name="Smith")

    # Call the service method
    result = await customer_service.update_customer(customer_id, update_data)

    # Assertions
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(customer_id)
    mock_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_customer_success(customer_service, mock_repository):
    """Test deleting a customer successfully."""
    # Mock the repository to return True (deletion successful)
    customer_id = str(uuid4())
    mock_repository.delete.return_value = True

    # Call the service method
    result = await customer_service.delete_customer(customer_id)

    # Assertions
    assert result is True
    mock_repository.delete.assert_called_once_with(customer_id)


@pytest.mark.asyncio
async def test_delete_customer_not_found(customer_service, mock_repository):
    """Test deleting a customer that does not exist."""
    # Mock the repository to return False (deletion failed)
    customer_id = str(uuid4())
    mock_repository.delete.return_value = False

    # Call the service method
    result = await customer_service.delete_customer(customer_id)

    # Assertions
    assert result is False
    mock_repository.delete.assert_called_once_with(customer_id)


@pytest.mark.asyncio
async def test_list_customers(customer_service, mock_repository):
    """Test listing customers."""
    # Mock the repository to return a list of customers
    customers = [
        Customer(
            id=str(uuid4()),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            date_of_birth=datetime(1990, 1, 1),
            notes="Test customer 1",
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Customer(
            id=str(uuid4()),
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            date_of_birth=datetime(1992, 2, 2),
            notes="Test customer 2",
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    mock_repository.list.return_value = customers

    # Call the service method
    result = await customer_service.list_customers(skip=0, limit=10)

    # Assertions
    assert len(result) == 2
    assert isinstance(result[0], CustomerResponse)
    assert isinstance(result[1], CustomerResponse)
    assert result[0].first_name == "John"
    assert result[1].first_name == "Jane"
    mock_repository.list.assert_called_once_with(skip=0, limit=10)


@pytest.mark.asyncio
async def test_search_customers(customer_service, mock_repository):
    """Test searching customers."""
    # Mock the repository to return a list of customers
    customers = [
        Customer(
            id=str(uuid4()),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            date_of_birth=datetime(1990, 1, 1),
            notes="Test customer",
            tenant_id="test_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    mock_repository.search.return_value = customers

    # Call the service method
    result = await customer_service.search_customers(
        tenant_id="test_tenant",
        query="John",
        limit=10
    )

    # Assertions
    assert len(result) == 1
    assert isinstance(result[0], CustomerResponse)
    assert result[0].first_name == "John"
    assert result[0].email == "john.doe@example.com"
    mock_repository.search.assert_called_once_with(
        tenant_id="test_tenant",
        query="John",
        limit=10
    )
