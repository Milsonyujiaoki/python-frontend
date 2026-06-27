"""
Unit tests for BarberService.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest
from uuid import uuid4
from datetime import datetime

from backend.application.services.barber_service import BarberService
from backend.application.dto.barber_dto import BarberCreate, BarberUpdate, BarberResponse
from backend.domain.entities.barber import Barber


@pytest.fixture
def mock_repository():
    """Create a mock barber repository."""
    return AsyncMock()


@pytest.fixture
def barber_service(mock_repository):
    """Create a barber service instance with a mock repository."""
    return BarberService(repository=mock_repository)


@pytest.fixture
def sample_barber_data():
    """Return a sample barber create data."""
    return BarberCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        specialty="Haircut",
        bio="Experienced barber"
    )


@pytest.mark.asyncio
async def test_create_barber_success(barber_service, mock_repository, sample_barber_data):
    """Test creating a barber successfully."""
    # Mock the repository to return no existing barber with the email
    mock_repository.get_by_email.return_value = None
    # Mock the repository create method to return a barber entity
    created_barber = Barber(
        id=str(uuid4()),
        first_name=sample_barber_data.first_name,
        last_name=sample_barber_data.last_name,
        email=sample_barber_data.email,
        phone=sample_barber_data.phone,
        specialty=sample_barber_data.specialty,
        bio=sample_barber_data.bio,
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.create.return_value = created_barber

    # Call the service method
    result = await barber_service.create_barber(sample_barber_data)

    # Assertions
    assert isinstance(result, BarberResponse)
    assert result.first_name == sample_barber_data.first_name
    assert result.last_name == sample_barber_data.last_name
    assert result.email == sample_barber_data.email
    assert result.phone == sample_barber_data.phone
    assert result.specialty == sample_barber_data.specialty
    assert result.bio == sample_barber_data.bio
    assert result.is_active == True
    assert result.tenant_id == "default_tenant"
    mock_repository.get_by_email.assert_called_once_with(
        sample_barber_data.email, "default_tenant"
    )
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_barber_email_exists(barber_service, mock_repository, sample_barber_data):
    """Test creating a barber when email already exists."""
    # Mock the repository to return an existing barber with the email
    existing_barber = Barber(
        id=str(uuid4()),
        first_name="Jane",
        last_name="Doe",
        email=sample_barber_data.email,
        phone="0987654321",
        specialty="Shave",
        bio="Experienced barber",
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_email.return_value = existing_barber

    # Call the service method and expect an exception
    with pytest.raises(ValueError, match=f"Barber with email {sample_barber_data.email} already exists"):
        await barber_service.create_barber(sample_barber_data)

    # Assertions
    mock_repository.get_by_email.assert_called_once_with(
        sample_barber_data.email, "default_tenant"
    )
    mock_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_get_barber_found(barber_service, mock_repository):
    """Test getting a barber by ID when it exists."""
    # Mock the repository to return a barber
    barber_id = str(uuid4())
    barber = Barber(
        id=barber_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        specialty="Haircut",
        bio="Experienced barber",
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = barber

    # Call the service method
    result = await barber_service.get_barber(barber_id)

    # Assertions
    assert isinstance(result, BarberResponse)
    assert result.id == barber_id
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "john.doe@example.com"
    mock_repository.get_by_id.assert_called_once_with(barber_id)


@pytest.mark.asyncio
async def test_get_barber_not_found(barber_service, mock_repository):
    """Test getting a barber by ID when it does not exist."""
    # Mock the repository to return None
    barber_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Call the service method
    result = await barber_service.get_barber(barber_id)

    # Assertions
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(barber_id)


@pytest.mark.asyncio
async def test_update_barber_success(barber_service, mock_repository):
    """Test updating a barber successfully."""
    # Mock the repository to return an existing barber
    barber_id = str(uuid4())
    existing_barber = Barber(
        id=barber_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        specialty="Haircut",
        bio="Experienced barber",
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.get_by_id.return_value = existing_barber
    # Mock the repository update method to return the updated barber
    updated_barber = Barber(
        id=barber_id,
        first_name="John",
        last_name="Smith",  # Changed last name
        email="john.doe@example.com",
        phone="1234567890",
        specialty="Haircut",
        bio="Experienced barber",
        is_active=True,
        tenant_id="default_tenant",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_repository.update.return_value = updated_barber

    # Prepare the update data
    update_data = BarberUpdate(last_name="Smith")

    # Call the service method
    result = await barber_service.update_barber(barber_id, update_data)

    # Assertions
    assert isinstance(result, BarberResponse)
    assert result.id == barber_id
    assert result.first_name == "John"
    assert result.last_name == "Smith"
    assert result.email == "john.doe@example.com"
    mock_repository.get_by_id.assert_called_once_with(barber_id)
    mock_repository.update.assert_called_once()
    # Check that the update method was called with a barber object that has the updated last name
    args, _ = mock_repository.update.call_args
    updated_barber_arg = args[0]
    assert updated_barber_arg.last_name == "Smith"


@pytest.mark.asyncio
async def test_update_barber_not_found(barber_service, mock_repository):
    """Test updating a barber that does not exist."""
    # Mock the repository to return None
    barber_id = str(uuid4())
    mock_repository.get_by_id.return_value = None

    # Prepare the update data
    update_data = BarberUpdate(last_name="Smith")

    # Call the service method
    result = await barber_service.update_barber(barber_id, update_data)

    # Assertions
    assert result is None
    mock_reparator.get_by_id.assert_called_once_with(barber_id)
    mock_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_barber_success(barber_service, mock_repository):
    """Test deleting a barber successfully."""
    # Mock the repository to return True (deletion successful)
    barber_id = str(uuid4())
    mock_repository.delete.return_value = True

    # Call the service method
    result = await barber_service.delete_barber(barber_id)

    # Assertions
    assert result is True
    mock_repository.delete.assert_called_once_with(barber_id)


@pytest.mark.asyncio
async def test_delete_barber_not_found(barber_service, mock_repository):
    """Test deleting a barber that does not exist."""
    # Mock the repository to return False (deletion failed)
    barber_id = str(uuid4())
    mock_repository.delete.return_value = False

    # Call the service method
    result = await barber_service.delete_barber(barber_id)

    # Assertions
    assert result is False
    mock_repository.delete.assert_called_once_with(barber_id)


@pytest.mark.asyncio
async def test_list_barbers(barber_service, mock_repository):
    """Test listing barbers."""
    # Mock the repository to return a list of barbers
    barbers = [
        Barber(
            id=str(uuid4()),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            specialty="Haircut",
            bio="Experienced barber",
            is_active=True,
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Barber(
            id=str(uuid4()),
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            specialty="Shave",
            bio="Experienced barber",
            is_active=True,
            tenant_id="default_tenant",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    mock_repository.list.return_value = barbers

    # Call the service method
    result = await barber_service.list_barbers(skip=0, limit=10)

    # Assertions
    assert len(result) == 2
    assert isinstance(result[0], BarberResponse)
    assert isinstance(result[1], BarberResponse)
    assert result[0].first_name == "John"
    assert result[1].first_name == "Jane"
    mock_repository.list.assert_called_once_with(skip=0, limit=10)


@pytest.mark.asyncio
async def test_search_barbers(barber_service, mock_repository):
    """Note: BarberService does not have a search method in the current implementation.
    This test is a placeholder for if we add a search method in the future."""
    # For now, we'll just pass.
    assert True
