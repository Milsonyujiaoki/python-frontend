"""
Barber API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .... import crud, models, schemas
from ....database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.BarberResponse, status_code=status.HTTP_201_CREATED)
def create_barber(barber: schemas.BarberCreate, db: Session = Depends(get_db)):
    """Create a new barber."""
    # Check if barber with this email already exists
    db_barber = crud.get_barber_by_email(db, email=barber.email)
    if db_barber:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_barber(db=db, barber=barber)


@router.get("/{barber_id}", response_model=schemas.BarberResponse)
def read_barber(barber_id: int, db: Session = Depends(get_db)):
    """Get a barber by ID."""
    db_barber = crud.get_barber(db, barber_id=barber_id)
    if db_barber is None:
        raise HTTPException(status_code=404, detail="Barber not found")
    return db_barber


@router.get("/", response_model=List[schemas.BarberResponse])
def read_barbers(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = Query(None, description="Search by name or email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get list of barbers with optional search and filtering."""
    barbers = crud.get_barbers(db, skip=skip, limit=limit, search=search, is_active=is_active)
    return barbers


@router.put("/{barber_id}", response_model=schemas.BarberResponse)
def update_barber(barber_id: int, barber: schemas.BarberUpdate, db: Session = Depends(get_db)):
    """Update a barber."""
    db_barber = crud.update_barber(db, barber_id=barber_id, barber=barber)
    if db_barber is None:
        raise HTTPException(status_code=404, detail="Barber not found")
    return db_barber


@router.delete("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_barber(barber_id: int, db: Session = Depends(get_db)):
    """Delete a barber."""
    db_barber = crud.get_barber(db, barber_id=barber_id)
    if db_barber is None:
        raise HTTPException(status_code=404, detail="Barber not found")
    crud.delete_barber(db=db, barber_id=barber_id)
    return None
