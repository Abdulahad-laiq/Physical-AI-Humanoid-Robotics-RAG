"""
Structured logging utility.

Provides JSON-formatted structured logging with query_id tracking
and context enrichment for monitoring and debugging.
"""

import logging
import json
import sys
from typing import Any, Dict, Optional
from datetime import datetime
from contextvars import ContextVar
import traceback


# ============================================================================
# Context Variables for Request Tracking
# ============================================================================

# Thread-safe context variable for query_id tracking
query_id_context: ContextVar[Optional[str]] = ContextVar("query_id", default=None)
session_id_context: ContextVar[Optional[str]] = ContextVar("session_id", default=None)


# ============================================================================
# Structured JSON Formatter
# ============================================================================

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Outputs logs as JSON with fields:
    - timestamp: ISO 8601 timestamp
    - level: Log level (INFO, WARNING, ERROR, etc.)
    - logger: Logger name
    - message: Log message
    - query_id: Current query ID (if set in context)
    - session_id: Current session ID (if set in context)
    - extra: Additional fields passed to logger
    - exception: Exception info (if present)
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            str: JSON-formatted log string
        """
        # Base log structure
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add query_id and session_id from context if available
        query_id = query_id_context.get()
        if query_id:
            log_data["query_id"] = query_id

        session_id = session_id_context.get()
        if session_id:
            log_data["session_id"] = session_id

        # Add extra fields from record
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data["extra"] = record.extra

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info)
            }

        # Add file location (useful for debugging)
        log_data["location"] = {
            "file": record.pathname,
            "line": record.lineno,
            "function": record.funcName
        }

        return json.dumps(log_data)


# ============================================================================
# Logger Setup
# ============================================================================

def setup_logger(
    name: str = None,
    level: str = "INFO",
    json_format: bool = True,
    include_console: bool = True
) -> logging.Logger:
    """
    Set up a structured logger.

    Args:
        name: Logger name (defaults to root logger if None)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON formatting (True) or simple text (False)
        include_console: Log to console/stdout

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    if include_console:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.upper())

        if json_format:
            console_handler.setFormatter(JSONFormatter())
        else:
            # Simple text format for development
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    # Prevent propagation to avoid duplicate logs
    logger.propagate = False

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get or create a logger with standard configuration.

    Args:
        name: Logger name (use __name__ from calling module)

    Returns:
        logging.Logger: Logger instance
    """
    # Check if logger already exists and is configured
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Logger not configured yet - set it up
        from ..config import get_settings

        settings = get_settings()
        logger = setup_logger(
            name=name,
            level=settings.log_level,
            json_format=(settings.environment.lower() == "production"),
            include_console=True
        )

    return logger


# ============================================================================
# Context Managers
# ============================================================================

class LogContext:
    """
    Context manager for adding query_id and session_id to logs.

    Usage:
        with LogContext(query_id="abc-123", session_id="xyz-456"):
            logger.info("Processing query")  # Will include query_id and session_id
    """

    def __init__(self, query_id: str = None, session_id: str = None):
        """
        Initialize log context.

        Args:
            query_id: Query ID to add to all logs
            session_id: Session ID to add to all logs
        """
        self.query_id = query_id
        self.session_id = session_id
        self.query_id_token = None
        self.session_id_token = None

    def __enter__(self):
        """Enter context - set query_id and session_id."""
        if self.query_id:
            self.query_id_token = query_id_context.set(self.query_id)
        if self.session_id:
            self.session_id_token = session_id_context.set(self.session_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - reset query_id and session_id."""
        if self.query_id_token:
            query_id_context.reset(self.query_id_token)
        if self.session_id_token:
            session_id_context.reset(self.session_id_token)


# ============================================================================
# Structured Logging Helpers
# ============================================================================

class StructuredLogger:
    """
    Wrapper for structured logging with extra context.

    Provides methods for logging with additional structured data.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize structured logger.

        Args:
            logger: Base logger instance
        """
        self.logger = logger

    def log_with_context(
        self,
        level: str,
        message: str,
        **extra: Any
    ):
        """
        Log message with extra context fields.

        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            **extra: Additional fields to include in log
        """
        # Create a log record with extra fields
        log_method = getattr(self.logger, level.lower())

        # Add extra fields to record
        record = self.logger.makeRecord(
            self.logger.name,
            getattr(logging, level.upper()),
            "(structured)",
            0,
            message,
            (),
            None
        )
        record.extra = extra

        self.logger.handle(record)

    def debug(self, message: str, **extra: Any):
        """Log debug message with extra context."""
        self.log_with_context("debug", message, **extra)

    def info(self, message: str, **extra: Any):
        """Log info message with extra context."""
        self.log_with_context("info", message, **extra)

    def warning(self, message: str, **extra: Any):
        """Log warning message with extra context."""
        self.log_with_context("warning", message, **extra)

    def error(self, message: str, **extra: Any):
        """Log error message with extra context."""
        self.log_with_context("error", message, **extra)

    def critical(self, message: str, **extra: Any):
        """Log critical message with extra context."""
        self.log_with_context("critical", message, **extra)


def get_structured_logger(name: str = None) -> StructuredLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name

    Returns:
        StructuredLogger: Structured logger wrapper
    """
    logger = get_logger(name)
    return StructuredLogger(logger)


# ============================================================================
# Performance Logging
# ============================================================================

class PerformanceTimer:
    """
    Context manager for timing operations and logging performance metrics.

    Usage:
        with PerformanceTimer(logger, "embedding_generation"):
            embeddings = generate_embeddings(texts)
        # Automatically logs: "embedding_generation completed in 150ms"
    """

    def __init__(
        self,
        logger: logging.Logger,
        operation_name: str,
        level: str = "info"
    ):
        """
        Initialize performance timer.

        Args:
            logger: Logger instance
            operation_name: Name of operation being timed
            level: Log level for timing message
        """
        self.logger = logger
        self.operation_name = operation_name
        self.level = level
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        """Start timer."""
        from time import time
        self.start_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and log duration."""
        from time import time
        self.end_time = time()
        duration_ms = (self.end_time - self.start_time) * 1000

        log_method = getattr(self.logger, self.level.lower())
        log_method(
            f"{self.operation_name} completed in {duration_ms:.2f}ms"
        )

    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0


# ============================================================================
# Application Startup Logging
# ============================================================================

def log_startup_info():
    """
    Log application startup information.

    Should be called during application initialization.
    """
    from ..config import get_settings
    import platform

    settings = get_settings()
    logger = get_logger(__name__)

    logger.info("=" * 60)
    logger.info("RAG Chatbot Backend Starting")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Log Level: {settings.log_level}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"Python Version: {platform.python_version()}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Gemini Model: {settings.gemini_model}")
    logger.info(f"Embedding Model: {settings.embedding_model}")
    logger.info(f"Qdrant Collection: {settings.qdrant_collection_name}")
    logger.info("=" * 60)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of logging utilities.
    """
    # Set up logger
    logger = get_logger(__name__)

    # Basic logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Logging with context
    with LogContext(query_id="abc-123", session_id="xyz-456"):
        logger.info("Processing query")
        logger.info("Retrieving chunks from vector store")

    # Structured logging with extra fields
    structured_logger = get_structured_logger(__name__)
    structured_logger.info(
        "Query processed successfully",
        duration_ms=1234,
        chunk_count=5,
        mode="global"
    )

    # Performance timing
    import time
    with PerformanceTimer(logger, "test_operation"):
        time.sleep(0.1)  # Simulate work

    # Exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.error("An error occurred", exc_info=True)

    print("\nCheck logs above - they should be in JSON format if ENVIRONMENT=production")
