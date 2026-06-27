"""
Main FastAPI application for the barbershop SaaS platform.
"""
from fastapi import FastAPI

from app.api.api_v1 import api_router

app = FastAPI(
    title="Barbershop SaaS API",
    description="API for managing barbershop operations including customers, barbers, services, and appointments.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the Barbershop SaaS API"}