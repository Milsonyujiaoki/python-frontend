"""
Main FastAPI application for the barbershop SaaS platform.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time

from app.api.api_v1 import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """Application factory for creating FastAPI instance."""

    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    )

    # CORS Middleware - allows frontend connections
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # Request timing middleware
    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response

    # Global exception handler for HTTP exceptions
    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "path": str(request.url.path),
                }
            },
        )

    # Validation error handler
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "details": exc.errors(),
                }
            },
        )

    # Generic exception handler
    @application.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(exc)}",
                }
            },
        )

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @application.get("/", tags=["root"])
    async def root():
        """Root endpoint with API info."""
        return {
            "success": True,
            "data": {
                "name": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "description": settings.DESCRIPTION,
                "docs": f"{settings.API_V1_PREFIX}/docs",
                "branding": {
                    "primary_color": settings.BRAND_COLOR_PRIMARY,
                    "secondary_color": settings.BRAND_COLOR_SECONDARY,
                }
            }
        }

    @application.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "timestamp": time.time(),
            }
        }

    return application


# Create application instance
app = create_application()