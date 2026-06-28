"""
Idempotency middleware for FastAPI.

This middleware ensures that duplicate requests (based on X-Request-ID header)
return cached responses, preventing duplicate operations like double-click form submissions.

Features:
- Extract and validate X-Request-ID header (UUID format)
- Store responses in Redis with TTL
- Return cached responses for duplicate request_ids
- Add X-Idempotency-Key header to all responses
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Optional, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# =============================================================================
# REDS CLIENT
# =============================================================================

class IdempotencyStore:
    """Redis-backed store for idempotent responses."""

    def __init__(self, redis_client=None, ttl_seconds: int = 300):
        """
        Args:
            redis_client: Redis client instance (from redis.Redis)
            ttl_seconds: Time-to-live for cached responses (default: 5 minutes)
        """
        self.redis = redis_client
        self.ttl_seconds = ttl_seconds
        self._local_cache: dict = {}
        self._local_cache_ttl: dict = {}

    async def get(self, request_id: str) -> Optional[dict]:
        """Get cached response for request_id."""
        # Check local cache first
        if request_id in self._local_cache:
            if time.time() < self._local_cache_ttl.get(request_id, 0):
                return self._local_cache[request_id]
            else:
                # Expired, remove from local cache
                del self._local_cache[request_id]
                del self._local_cache_ttl[request_id]

        # Try Redis
        if self.redis:
            try:
                cached = self.redis.get(f"idempotency:{request_id}")
                if cached:
                    result = json.loads(cached)
                    # Update local cache
                    self._local_cache[request_id] = result
                    self._local_cache_ttl[request_id] = time.time() + self.ttl_seconds
                    return result
            except Exception as e:
                logger.warning(f"Redis get failed: {e}")

        return None

    async def set(self, request_id: str, response_data: dict):
        """Cache response for request_id."""
        # Store in local cache
        self._local_cache[request_id] = response_data
        self._local_cache_ttl[request_id] = time.time() + self.ttl_seconds

        # Store in Redis
        if self.redis:
            try:
                self.redis.setex(
                    f"idempotency:{request_id}",
                    self.ttl_seconds,
                    json.dumps(response_data)
                )
            except Exception as e:
                logger.warning(f"Redis set failed: {e}")

    async def exists(self, request_id: str) -> bool:
        """Check if request_id has cached response."""
        cached = await self.get(request_id)
        return cached is not None


# =============================================================================
# IDEMPOTENCY MIDDLEWARE
# =============================================================================

class IdempotencyMiddleware(BaseHTTPMiddleware):
    """Middleware that adds idempotency to HTTP requests."""

    def __init__(self, app, store: IdempotencyStore = None, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.store = store or IdempotencyStore()
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with idempotency handling."""
        # Extract request ID from header
        request_id = request.headers.get(self.header_name)

        # Generate new request ID if not provided
        generated_id = False
        if not request_id:
            request_id = str(uuid.uuid4())
            generated_id = True

        # Validate UUID format
        if not self._is_valid_uuid(request_id):
            # Return error for invalid UUID
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": f"Invalid {self.header_name} format. Must be UUID.",
                        "valid_format": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    }
                }
            )

        # Check for cached response (only for safe methods or idempotent POST/PUT)
        if request.method in ("GET", "POST", "PUT", "DELETE"):
            cached = await self.store.get(request_id)
            if cached:
                logger.info(f"Returning cached response for request_id: {request_id}")
                response = JSONResponse(
                    content=cached.get("data", cached),
                    status_code=cached.get("status_code", 200),
                    headers={"X-Idempotency-Key": request_id}
                )
                return response

        # Process the request
        response = await call_next(request)

        # Cache successful responses
        if request.method in ("POST", "PUT", "DELETE") and response.status_code in (200, 201, 204):
            # Read response content
            if hasattr(response, "body"):
                response_data = {
                    "data": response.body.decode() if isinstance(response.body, bytes) else response.body,
                    "status_code": response.status_code,
                }
            else:
                response_data = {
                    "data": {},
                    "status_code": response.status_code,
                }

            await self.store.set(request_id, response_data)

        # Add idempotency key to response
        response.headers["X-Idempotency-Key"] = request_id

        # Add generated request ID if it was created by us
        if generated_id:
            response.headers["X-Request-ID"] = request_id

        return response

    def _is_valid_uuid(self, uid: str) -> bool:
        """Check if string is a valid UUID."""
        try:
            uuid.UUID(uid)
            return True
        except (ValueError, AttributeError):
            return False


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_request_id(headers: dict) -> Optional[str]:
    """Extract request ID from headers."""
    return headers.get("X-Request-ID") or headers.get("x-request-id")


def validate_request_id(request_id: str) -> bool:
    """Validate request ID format (UUID)."""
    try:
        uuid.UUID(request_id)
        return True
    except (ValueError, AttributeError):
        return False


# =============================================================================
# DEBUG/UTILITIES
# =============================================================================

class IdempotencyDebugger:
    """Utilities for debugging idempotency."""

    @staticmethod
    def generate_request_id() -> str:
        """Generate a valid request ID."""
        return str(uuid.uuid4())

    @staticmethod
    def format_request_id() -> str:
        """Return format description."""
        return "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"


__all__ = [
    "IdempotencyMiddleware",
    "IdempotencyStore",
    "extract_request_id",
    "validate_request_id",
    "IdempotencyDebugger",
]