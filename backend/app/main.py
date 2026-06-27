"""
Main FastAPI application for the barbershop SaaS platform.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import logging
import os

from app.api.api_v1 import api_router
from app.core.config import settings
from app.websocket import websocket_handler
from app.middleware.idempotency import IdempotencyMiddleware, IdempotencyStore
import redis

logger = logging.getLogger(__name__)


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

    # Idempotency Middleware - with Redis if available
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_client = None

    try:
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
            socket_connect_timeout=5
        )
        # Test connection
        redis_client.ping()
        logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
    except Exception as e:
        logger.warning(f"Redis not available, using in-memory cache: {e}")

    idempotency_store = IdempotencyStore(
        redis_client=redis_client,
        ttl_seconds=300  # 5 minutes
    )

    application.add_middleware(
        IdempotencyMiddleware,
        store=idempotency_store,
        header_name="X-Request-ID"
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

    # WebSocket endpoint for real-time sync
    application.add_api_websocket_route("/ws", websocket_handler)

    return application


# Create application instance
app = create_application()