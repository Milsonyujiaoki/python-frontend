"""
CRUD operations for Customer, Barber, and Service.
"""
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas


def get_customer(db: Session, customer_id: int):
    """Get a customer by ID."""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    """Get a customer by email."""
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get multiple customers with optional search and filtering."""
    query = db.query(models.Customer)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Customer.first_name.ilike(search_term)) |
            (models.Customer.last_name.ilike(search_term)) |
            (models.Customer.email.ilike(search_term))
        )
    if is_active is not None:
        query = query.filter(models.Customer.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    """Create a new customer."""
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    """Update a customer."""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    """Delete a customer."""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


# Barber CRUD
def get_barber(db: Session, barber_id: int):
    """Get a barber by ID."""
    return db.query(models.Barber).filter(models.Barber.id == barber_id).first()


def get_barber_by_email(db: Session, email: str):
    """Get a barber by email."""
    return db.query(models.Barber).filter(models.Barber.email == email).first()


def get_barbers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get multiple barbers with optional search and filtering."""
    query = db.query(models.Barber)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Barber.first_name.ilike(search_term)) |
            (models.Barber.last_name.ilike(search_term)) |
            (models.Barber.email.ilike(search_term))
        )
    if is_active is not None:
        query = query.filter(models.Barber.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_barber(db: Session, barber: schemas.BarberCreate):
    """Create a new barber."""
    db_barber = models.Barber(**barber.model_dump())
    db.add(db_barber)
    db.commit()
    db.refresh(db_barber)
    return db_barber


def update_barber(db: Session, barber_id: int, barber: schemas.BarberUpdate):
    """Update a barber."""
    db_barber = get_barber(db, barber_id)
    if db_barber:
        update_data = barber.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_barber, field, value)
        db.commit()
        db.refresh(db_barber)
    return db_barber


def delete_barber(db: Session, barber_id: int):
    """Delete a barber."""
    db_barber = get_barber(db, barber_id)
    if db_barber:
        db.delete(db_barber)
        db.commit()
    return db_barber


# Service CRUD
def get_service(db: Session, service_id: int):
    """Get a service by ID."""
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_service_by_name(db: Session, name: str):
    """Get a service by name."""
    return db.query(models.Service).filter(models.Service.name == name).first()


def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get multiple services with optional search and filtering."""
    query = db.query(models.Service)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Service.name.ilike(search_term)) |
            (models.Service.description.ilike(search_term))
        )
    if is_active is not None:
        query = query.filter(models.Service.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_service(db: Session, service: schemas.ServiceCreate):
    """Create a new service."""
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, service_id: int, service: schemas.ServiceUpdate):
    """Update a service."""
    db_service = get_service(db, service_id)
    if db_service:
        update_data = service.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_service, field, value)
        db.commit()
        db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int):
    """Delete a service."""
    db_service = get_service(db, service_id)
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service