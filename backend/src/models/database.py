"""
Database connection and session management for Neon PostgreSQL.

Provides database connection pooling, session management, and table definitions
for query logging and analytics.
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
import os
from datetime import datetime
import logging
from src.config import get_settings

logger = logging.getLogger(__name__)

# SQLAlchemy declarative base for all models
Base = declarative_base()


# ============================================================================
# Database Models
# ============================================================================

class QueryLogModel(Base):
    """
    Query log table for storing query metadata and analytics.

    Stores anonymized query data for monitoring, debugging, and usage analytics.
    No PII is stored - session IDs are hashed using SHA-256.
    """
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(String(36), unique=True, nullable=False, index=True)
    query_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    mode = Column(String(20), nullable=False)  # "global" or "selected-text"
    session_id_hash = Column(String(64), nullable=True, index=True)  # SHA-256 hash
    response_time_ms = Column(Integer, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    error = Column(Text, nullable=True)

    def __repr__(self):
        return f"<QueryLog(query_id='{self.query_id}', mode='{self.mode}', timestamp='{self.timestamp}')>"


# ============================================================================
# Database Connection Management
# ============================================================================

class DatabaseManager:
    """
    Manages database connections and sessions for the application.

    Handles connection pooling, session lifecycle, and provides context managers
    for safe database operations.
    """

    def __init__(self, database_url: str = None):
        """
        Initialize database manager with connection URL.

        Args:
            database_url: PostgreSQL connection string. If None, reads from config settings.

        Raises:
            ValueError: If database_url is not provided and not in config.
        """
        # Load settings from config if not provided
        settings = get_settings()
        self.database_url = database_url or settings.neon_database_url

        if not self.database_url:
            raise ValueError(
                "Database URL not provided. Set NEON_DATABASE_URL environment variable "
                "or pass database_url to DatabaseManager constructor."
            )

        # Create engine with connection pooling
        # NullPool is used for serverless deployments to avoid connection pool exhaustion
        self.engine = create_engine(
            self.database_url,
            poolclass=NullPool,  # No connection pooling (suitable for Neon serverless)
            echo=False,  # Set to True for SQL query logging in development
            pool_pre_ping=True,  # Verify connections before using them
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        logger.info("Database manager initialized successfully")

    def create_tables(self):
        """
        Create all database tables defined in models.

        This should be called during application startup or via Alembic migrations.
        For production, prefer Alembic migrations for versioned schema changes.
        """
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise

    def drop_tables(self):
        """
        Drop all database tables.

        WARNING: This will delete all data. Use only for testing or development.
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Error dropping database tables: {e}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions.

        Provides automatic session cleanup and error handling.
        Commits on success, rolls back on exception.

        Usage:
            with db_manager.get_session() as session:
                query_log = QueryLogModel(query_id="...", ...)
                session.add(query_log)
                # Automatic commit on exit

        Yields:
            Session: SQLAlchemy database session
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def get_session_direct(self) -> Session:
        """
        Get a database session directly (without context manager).

        Caller is responsible for closing the session and handling transactions.
        Prefer get_session() context manager for automatic cleanup.

        Returns:
            Session: SQLAlchemy database session
        """
        return self.SessionLocal()

    def health_check(self) -> bool:
        """
        Check database connection health.

        Returns:
            bool: True if database is accessible, False otherwise
        """
        try:
            with self.get_session() as session:
                # Execute a simple query to verify connection
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# ============================================================================
# Global Database Instance
# ============================================================================

# Global database manager instance (initialized on first import)
# This will be used throughout the application for database access
_db_manager: DatabaseManager = None


def get_database_manager() -> DatabaseManager:
    """
    Get or create the global database manager instance.

    Returns:
        DatabaseManager: Global database manager singleton
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_database(database_url: str = None):
    """
    Initialize the global database manager with optional custom URL.

    Args:
        database_url: Optional custom database URL. If None, uses NEON_DATABASE_URL env var.
    """
    global _db_manager
    _db_manager = DatabaseManager(database_url=database_url)
    logger.info("Global database manager initialized")


# ============================================================================
# Utility Functions
# ============================================================================

def hash_session_id(session_id: str) -> str:
    """
    Hash session ID using SHA-256 for privacy-preserving storage.

    Args:
        session_id: Original session ID (e.g., UUID)

    Returns:
        str: SHA-256 hash of session ID (64 hex characters)
    """
    import hashlib
    return hashlib.sha256(session_id.encode()).hexdigest()


def log_query(
    query_id: str,
    query_text: str,
    mode: str,
    response_time_ms: int,
    chunk_count: int,
    session_id: str = None,
    error: str = None
):
    """
    Log a query to the database for analytics and debugging.

    Args:
        query_id: Unique query identifier
        query_text: User's query text
        mode: Query mode ("global" or "selected-text")
        response_time_ms: Response generation time in milliseconds
        chunk_count: Number of chunks retrieved
        session_id: Optional session ID (will be hashed before storage)
        error: Optional error message if query failed
    """
    db_manager = get_database_manager()

    try:
        with db_manager.get_session() as session:
            query_log = QueryLogModel(
                query_id=query_id,
                query_text=query_text,
                timestamp=datetime.utcnow(),
                mode=mode,
                session_id_hash=hash_session_id(session_id) if session_id else None,
                response_time_ms=response_time_ms,
                chunk_count=chunk_count,
                error=error
            )
            session.add(query_log)
            logger.info(f"Query logged: {query_id} (mode={mode}, time={response_time_ms}ms)")
    except Exception as e:
        # Don't fail the request if logging fails
        logger.error(f"Failed to log query {query_id}: {e}")


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of database manager.
    """
    # Initialize database manager
    db_manager = get_database_manager()

    # Create tables
    db_manager.create_tables()

    # Test health check
    is_healthy = db_manager.health_check()
    print(f"Database health check: {'✓ Healthy' if is_healthy else '✗ Failed'}")

    # Example: Log a query
    log_query(
        query_id="550e8400-e29b-41d4-a716-446655440000",
        query_text="What is inverse kinematics?",
        mode="global",
        response_time_ms=1234,
        chunk_count=5,
        session_id="test-session-123"
    )

    # Example: Query logs
    with db_manager.get_session() as session:
        recent_queries = session.query(QueryLogModel).order_by(
            QueryLogModel.timestamp.desc()
        ).limit(10).all()

        print(f"\nRecent queries ({len(recent_queries)}):")
        for q in recent_queries:
            print(f"  - {q.query_id}: {q.query_text[:50]}... ({q.mode}, {q.response_time_ms}ms)")
