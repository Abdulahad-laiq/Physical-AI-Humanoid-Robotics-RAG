"""
FastAPI application entry point for RAG Chatbot backend.

Initializes the FastAPI app, configures CORS, registers routes,
and sets up health monitoring.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from .config import get_settings, validate_configuration, is_production
from .utils.logger import setup_logger, log_startup_info
from .models.schemas import HealthResponse
from .services.vector_store import get_vector_store
from .services.embeddings import get_embedding_service
from .services.agent import get_agent_service
from .models.database import get_database_manager


# Initialize logger
logger = setup_logger(
    name=__name__,
    level="INFO",
    json_format=is_production()
)


# ============================================================================
# Application Lifespan
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events for service initialization.
    """
    # Startup
    logger.info("Starting RAG Chatbot Backend...")

    # Log startup information
    log_startup_info()

    # Validate configuration
    try:
        validate_configuration()
        logger.info("[OK] Configuration validated")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

    # Initialize services (lazy loading)
    try:
        # Vector store
        vector_store = get_vector_store()
        if vector_store.health_check():
            logger.info("[OK] Qdrant connection successful")
        else:
            logger.warning("[WARNING] Qdrant connection failed - vector search may not work")

        # Database
        db_manager = get_database_manager()
        if db_manager.health_check():
            logger.info("[OK] Neon PostgreSQL connection successful")
        else:
            logger.warning("[WARNING] Database connection failed - query logging may not work")

        # Embedding service
        embedding_service = get_embedding_service()
        logger.info(f"[OK] Embedding service loaded (model={embedding_service.model_name})")

        # Agent service
        agent_service = get_agent_service()
        logger.info(f"[OK] Agent service initialized (model={agent_service.model})")

        logger.info("=" * 60)
        logger.info("RAG Chatbot Backend is ready to accept requests")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error initializing services: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot Backend...")
    logger.info("[OK] Shutdown complete")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================================
# CORS Middleware
# ============================================================================

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured: {settings.cors_origins_list}")


# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns service status and connection health for Qdrant and Neon.
    """
    # Check Qdrant
    try:
        vector_store = get_vector_store()
        qdrant_connected = vector_store.health_check()
    except Exception as e:
        logger.error(f"Qdrant health check error: {e}")
        qdrant_connected = False

    # Check Neon
    try:
        db_manager = get_database_manager()
        neon_connected = db_manager.health_check()
    except Exception as e:
        logger.error(f"Database health check error: {e}")
        neon_connected = False

    # Determine overall status
    if qdrant_connected and neon_connected:
        status = "healthy"
    else:
        status = "degraded"

    return HealthResponse(
        status=status,
        qdrant_connected=qdrant_connected,
        neon_connected=neon_connected
    )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "RAG Chatbot API",
        "version": "1.0.0",
        "description": "Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics textbook",
        "docs": "/docs",
        "health": "/health"
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# ============================================================================
# Route Registration
# ============================================================================

# Import and register API routes
from .api.routes import chat, selected_text
from .api.middleware import setup_middleware

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(selected_text.router, prefix="/api/v1", tags=["Selected Text"])

# Setup middleware (rate limiting, logging, security headers)
setup_middleware(app)


# ============================================================================
# Development Server
# ============================================================================

if __name__ == "__main__":
    """
    Run development server directly.

    For production, use: uvicorn src.main:app --host 0.0.0.0 --port 8000
    """
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
