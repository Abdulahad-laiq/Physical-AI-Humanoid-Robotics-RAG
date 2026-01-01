"""
API middleware for rate limiting and request processing.

Implements IP-based rate limiting using slowapi to prevent abuse
and ensure fair usage of the API.
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

from ..config import get_settings


logger = logging.getLogger(__name__)


# ============================================================================
# Rate Limiter Configuration
# ============================================================================

def get_limiter() -> Limiter:
    """
    Create and configure rate limiter.

    Returns:
        Limiter: Configured slowapi limiter instance
    """
    settings = get_settings()

    limiter = Limiter(
        key_func=get_remote_address,  # Rate limit by IP address
        default_limits=[f"{settings.rate_limit_per_minute}/minute"],
        enabled=settings.rate_limit_enabled,
        storage_uri="memory://",  # In-memory storage (for single instance)
        strategy="fixed-window"  # Fixed window strategy
    )

    logger.info(
        f"Rate limiter configured: {settings.rate_limit_per_minute} req/min per IP "
        f"(enabled={settings.rate_limit_enabled})"
    )

    return limiter


# Global limiter instance
limiter = get_limiter()


# ============================================================================
# Rate Limit Exceeded Handler
# ============================================================================

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.

    Returns a structured JSON response instead of plain text.

    Args:
        request: FastAPI request
        exc: RateLimitExceeded exception

    Returns:
        JSONResponse: 429 error response
    """
    client_ip = get_remote_address(request)

    logger.warning(
        f"Rate limit exceeded for IP {client_ip} "
        f"(path={request.url.path}, method={request.method})"
    )

    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Please try again later.",
            "detail": str(exc.detail) if hasattr(exc, 'detail') else None,
            "retry_after": "60 seconds"
        }
    )


# ============================================================================
# Request Logging Middleware
# ============================================================================

async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests.

    Args:
        request: FastAPI request
        call_next: Next middleware/handler in chain

    Returns:
        Response: Response from downstream handlers
    """
    client_ip = get_remote_address(request)

    logger.info(
        f"Request: {request.method} {request.url.path} from {client_ip}"
    )

    # Process request
    response = await call_next(request)

    logger.info(
        f"Response: {request.method} {request.url.path} -> {response.status_code}"
    )

    return response


# ============================================================================
# Security Headers Middleware
# ============================================================================

async def add_security_headers(request: Request, call_next):
    """
    Middleware to add security headers to responses.

    Args:
        request: FastAPI request
        call_next: Next middleware/handler in chain

    Returns:
        Response: Response with security headers added
    """
    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response


# ============================================================================
# Helper Functions
# ============================================================================

def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request.

    Handles X-Forwarded-For header for proxied requests.

    Args:
        request: FastAPI request

    Returns:
        str: Client IP address
    """
    # Check X-Forwarded-For header (for proxied requests)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take first IP in the chain
        return forwarded_for.split(",")[0].strip()

    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    # Fallback to direct connection IP
    return get_remote_address(request)


# ============================================================================
# Apply Middleware to FastAPI App
# ============================================================================

def setup_middleware(app):
    """
    Register all middleware with FastAPI app.

    Args:
        app: FastAPI application instance
    """
    from slowapi.middleware import SlowAPIMiddleware

    # Add rate limiting middleware
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # Add request logging middleware
    app.middleware("http")(log_requests)

    # Add security headers middleware
    app.middleware("http")(add_security_headers)

    logger.info("✓ Middleware configured successfully")


# ============================================================================
# Rate Limit Decorators
# ============================================================================

def rate_limit(limit: str = None):
    """
    Decorator for applying custom rate limits to endpoints.

    Args:
        limit: Rate limit string (e.g., "10/minute", "100/hour")

    Usage:
        @app.get("/endpoint")
        @rate_limit("10/minute")
        async def endpoint():
            ...
    """
    settings = get_settings()
    limit_str = limit or f"{settings.rate_limit_per_minute}/minute"

    def decorator(func):
        return limiter.limit(limit_str)(func)

    return decorator


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example middleware configuration.
    """
    from fastapi import FastAPI

    app = FastAPI()

    # Setup middleware
    setup_middleware(app)

    @app.get("/test")
    @limiter.limit("5/minute")
    async def test_endpoint(request: Request):
        return {"message": "This endpoint is rate limited to 5 requests per minute"}

    print("Middleware configured successfully")
    print(f"Rate limit: {get_settings().rate_limit_per_minute} req/min")
