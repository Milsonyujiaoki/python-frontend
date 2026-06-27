"""
Unit tests for ServiceService.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest
from uuid import uuid4
from datetime import datetime

from backend.application.services.service_service import ServiceService
from backend.application.dto.service_dto import ServiceCreate, ServiceUpdate, ServiceResponse
from backend.domain.entities.service import Service


@pytest.fixture
def mock_repository():
    """Create a mock service repository."""
    return AsyncMock()


@pytest.fixture
def service_service(mock_repository):
    """Create a service service instance with a mock repository."""
    return ServiceService(repository=mock_repository)


@pytest.fixture
def sample_service_data():
    """Return a sample service create data."""
    return ServiceCreate(
        name="Haircut",
        description="Basic haircut",
        price=1500,  # in cents
        duration_minutes=30,
        is_active=True
    )


@pytest.mark.asyncio
async def test_create_service_success(service_service, mock_repository, sample_service_data):
    """Test creating a service successfully."""
    # Mock the repository to return no existing service with the name
    mock_repository.get_by_name.return_value = None
    # Mock the repository create method to return a service entity
    created_service = Service(
        id=str(uuid4()),
        name=sample_service_data.name,
        description=sample_service_data.description,
        price=sample_service_data.price,
        duration_minutes=sample_service_data.duration_minutes,
        is_active=sample_service_data.is_active,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.create.return_value = created_service

    # Call the service method
    result = await service_service.create_service(sample_service_data)

    # Assertions
    assert isinstance(result, ServiceResponse)
    assert result.name == sample_service_data.name
    assert result.description == sample_service_data.description
    assert result.price == sample_service_data.price
    assert result.duration_minutes == sample_service_data.duration_minutes
    assert result.is_active == sample_service_data.is_active
    assert result.tenant_id == "default_tenant"
    mock_repository.get_by_name.assert_called_once_with(
        sample_service_data.name, "default_tenant"
    )
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_service_name_exists(service_service, mock_repository, sample_service_data):
    """Test creating a service when name already exists."""
    # Mock the repository to return an existing service with the name
    existing_service = Service(
        id=str(uuid4()),
        name=sample_service_data.name,
        description="Another description",
        price=2000,
        duration_minutes=45,
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_name.return_value = existing_service

    # Call the service method and expect an exception
    with pytest.raises(ValueError, match=f"Service with name {sample_service_data.name} already exists"):
        await service_service.create_service(sample_service_data)

    # Assertions
    mock_repository.get_by_name.assert_called_once_with(
        sample_service_data.name, "default_tenant"
    )
    mock_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_get_service_found(service_service, mock_repository):
    """Test getting a service by ID when it exists."""
    # Mock the repository to return a service
    service_id = str(uuid4())
    service = Service(
        id=service_id,
        name="Haircut",
        description="Basic haircut",
        price=1500,
        duration_minutes=30,
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = service

    # Call the service method
    result = await service_service.get_service(service_id)

    # Assertions
    assert isinstance(result, ServiceResponse)
    assert result.id == service_id
    assert result.name == "Haircut"
    assert result.description == "Basic haircut"
    assert result.price == 1500
    assert result.duration_minutes == 30
    assert result.is_active == True
    mock_repository.get_by_id.assert_called_once_with(service_id)


@pytest.mark.asyncio
async def test_get_service_not_found(service_service, mock_repository):
    """Test getting a service by ID when it does not exist."""
    # Mock the repository to return None
    service_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Call the service method
    result = await service_service.get_service(service_id)

    # Assertions
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(service_id)


@pytest.mark.asyncio
async def test_update_service_success(service_service, mock_repository):
    """Test updating a service successfully."""
    # Mock the repository to return an existing service
    service_id = str(uuid4())
    existing_service = Service(
        id=service_id,
        name="Haircut",
        description="Basic haircut",
        price=1500,
        duration_minutes=30,
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = existing_service
    # Mock the repository update method to return the updated service
    updated_service = Service(
        id=service_id,
        name="Haircut and Shave",
        description="Haircut and shave combo",
        price=2500,
        duration_minutes=45,
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.update.return_value = updated_service

    # Prepare the update data
    update_data = ServiceUpdate(
        name="Haircut and Shave",
        description="Haircut and shave combo",
        price=2500,
        duration_minutes=45
    )

    # Call the service method
    result = await service_service.update_service(service_id, update_data)

    # Assertions
    assert isinstance(result, ServiceResponse)
    assert result.id == service_id
    assert result.name == "Haircut and Shave"
    assert result.description == "Haircut and shave combo"
    assert result.price == 2500
    assert result.duration_minutes == 45
    assert result.is_active == True
    mock_repository.get_by_id.assert_called_once_with(service_id)
    mock_repository.update.assert_called_once()
    # Check that the update method was called with a service object that has the updated name
    args, _ = mock_repository.update.call_args
    updated_service_arg = args[0]
    assert updated_service_arg.name == "Haircut and Shave"


@pytest.mark.asyncio
async def test_update_service_not_found(service_service, mock_repository):
    """Test updating a service that does not exist."""
    # Mock the repository to return None
    service_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Prepare the update data
    update_data = ServiceUpdate(name="Haircut and Shave")

    # Call the service method
    result = await service_service.update_service(service_id, update_data)

    # Assertions
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(service_id)
    mock_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_service_success(service_service, mock_repository):
    """Test deleting a service successfully."""
    # Mock the repository to return True (deletion successful)
    service_id = str(uuid4())
    mock_repository.delete.return_value = True

    # Call the service method
    result = await service_service.delete_service(service_id)

    # Assertions
    assert result is True
    mock_repository.delete.assert_called_once_with(service_id)


@pytest.mark.asyncio
async def test_delete_service_not_found(service_service, mock_repository):
    """Test deleting a service that does not exist."""
    # Mock the repository to return False (deletion failed)
    service_id = str(uuid4())
    mock_repository.delete.return_value = False

    # Call the service method
    result = await service_service.delete_service(service_id)

    # Assertions
    assert result is False
    mock_repository.delete.assert_called_once_with(service_id)


@pytest.mark.asyncio
async def test_list_services(service_service, mock_repository):
    """Test listing services."""
    # Mock the repository to return a list of services
    services = [
        Service(
            id=str(uuid4()),
            name="Haircut",
            description="Basic haircut",
            price=1500,
            duration_minutes=30,
            is_active=True,
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Service(
            id=str(uuid4()),
            name="Shave",
            description="Traditional shave",
            price=800,
            duration_minutes=15,
            is_active=True,
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    mock_repository.list.return_value = services

    # Call the service method
    result = await service_service.list_services(skip=0, limit=10)

    # Assertions
    assert len(result) == 2
    assert isinstance(result[0], ServiceResponse)
    assert isinstance(result[1], ServiceResponse)
    assert result[0].name == "Haircut"
    assert result[1].name == "Shave"
    mock_repository.list.assert_called_once_with(skip=0, limit=10)


@pytest.mark.asyncio
async def test_search_services(service_service, mock_repository):
    """Test searching services."""
    # Mock the repository to return a list of services matching the search
    services = [
        Service(
            id=str(uuid4()),
            name="Haircut",
            description="Basic haircut",
            price=1500,
            duration_minutes=30,
            is_active=True,
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    mock_repository.search.return_value = services

    # Call the service method
    result = await service_service.search_services(tenant_id="default_tenant", query="hair", limit=10)

    # Assertions
    assert len(result) == 1
    assert isinstance(result[0], ServiceResponse)
    assert result[0].name == "Haircut"
    mock_repository.search.assert_called_once_with(tenant_id="default_tenant", query="hair", limit=10)
