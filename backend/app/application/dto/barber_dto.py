"""
Barber Data Transfer Objects.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BarberBase(BaseModel):
    """Base barber schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    specialty: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    is_active: Optional[bool] = True


class BarberCreate(BarberBase):
    """Barber creation schema."""
    pass


class BarberUpdate(BaseModel):
    """Barber update schema."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    specialty: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    is_active: Optional[bool] = None


class BarberResponse(BarberBase):
    """Barber response schema."""
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True