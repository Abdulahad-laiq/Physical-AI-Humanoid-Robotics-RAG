"""
Utilities package.

Contains helper functions and utilities for logging, validation, etc.
"""

from .logger import (
    get_logger,
    get_structured_logger,
    LogContext,
    PerformanceTimer,
    log_startup_info
)
from .validators import (
    validate_query_request,
    validate_selected_text_request,
    sanitize_query,
    sanitize_selected_text,
    is_safe_input
)

__all__ = [
    # Logger
    "get_logger",
    "get_structured_logger",
    "LogContext",
    "PerformanceTimer",
    "log_startup_info",
    # Validators
    "validate_query_request",
    "validate_selected_text_request",
    "sanitize_query",
    "sanitize_selected_text",
    "is_safe_input"
]
