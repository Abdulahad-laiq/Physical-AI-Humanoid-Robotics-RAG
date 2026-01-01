"""
Data models package.

Contains Pydantic schemas and database models.
"""

from .schemas import (
    TextChunk,
    Citation,
    QueryRequest,
    SelectedTextQueryRequest,
    ChatResponse,
    QueryLog,
    HealthResponse
)
from .database import (
    Base,
    QueryLogModel,
    DatabaseManager,
    get_database_manager,
    log_query
)

__all__ = [
    # Schemas
    "TextChunk",
    "Citation",
    "QueryRequest",
    "SelectedTextQueryRequest",
    "ChatResponse",
    "QueryLog",
    "HealthResponse",
    # Database
    "Base",
    "QueryLogModel",
    "DatabaseManager",
    "get_database_manager",
    "log_query"
]
