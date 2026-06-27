"""
API v1 router configuration.
"""
from fastapi import APIRouter

from .customers import router as customers_router
from .barbers import router as barbers_router
from .services import router as services_router

api_router = APIRouter()

# Include routers
api_router.include_router(customers_router, prefix="/customers", tags=["customers"])
api_router.include_router(barbers_router, prefix="/barbers", tags=["barbers"])
api_router.include_router(services_router, prefix="/services", tags=["services"])

# Other routers will be added here as they are implemented
# etc.

__all__ = ["api_router"]
