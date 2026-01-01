"""
Input validation and sanitization utilities.

Provides validators for API inputs, query sanitization, and security checks.
"""

import re
from typing import Optional, Tuple
import html


# ============================================================================
# Query Validation
# ============================================================================

def validate_query_text(
    query: str,
    min_length: int = 1,
    max_length: int = 1000,
    allow_empty: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Validate query text input.

    Args:
        query: User query text
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allow_empty: Allow empty queries after stripping whitespace

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Check if query is None
    if query is None:
        return False, "Query cannot be None"

    # Strip whitespace
    query_stripped = query.strip()

    # Check empty
    if not allow_empty and len(query_stripped) == 0:
        return False, "Query cannot be empty or only whitespace"

    # Check length
    if len(query_stripped) < min_length:
        return False, f"Query must be at least {min_length} characters"

    if len(query_stripped) > max_length:
        return False, f"Query must not exceed {max_length} characters"

    return True, None


def validate_selected_text(
    text: str,
    min_length: int = 10,
    max_length: int = 5000
) -> Tuple[bool, Optional[str]]:
    """
    Validate selected text input.

    Args:
        text: Selected text from user
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Check if text is None
    if text is None:
        return False, "Selected text cannot be None"

    # Strip whitespace
    text_stripped = text.strip()

    # Check length
    if len(text_stripped) < min_length:
        return False, f"Selected text must be at least {min_length} characters"

    if len(text_stripped) > max_length:
        return False, f"Selected text must not exceed {max_length} characters"

    return True, None


# ============================================================================
# Sanitization
# ============================================================================

def sanitize_query(query: str) -> str:
    """
    Sanitize query text to prevent injection attacks.

    Removes or escapes potentially dangerous characters while preserving
    the query's meaning.

    Args:
        query: Raw query text

    Returns:
        str: Sanitized query text
    """
    # Strip leading/trailing whitespace
    sanitized = query.strip()

    # Escape HTML entities to prevent XSS
    sanitized = html.escape(sanitized)

    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')

    # Normalize whitespace (collapse multiple spaces)
    sanitized = re.sub(r'\s+', ' ', sanitized)

    return sanitized


def sanitize_selected_text(text: str) -> str:
    """
    Sanitize selected text.

    Less aggressive than query sanitization to preserve formatting.

    Args:
        text: Raw selected text

    Returns:
        str: Sanitized text
    """
    # Remove null bytes
    sanitized = text.replace('\x00', '')

    # Escape HTML entities
    sanitized = html.escape(sanitized)

    # Normalize line endings
    sanitized = sanitized.replace('\r\n', '\n').replace('\r', '\n')

    # Trim excessive whitespace while preserving structure
    lines = sanitized.split('\n')
    lines = [line.rstrip() for line in lines]  # Remove trailing whitespace per line
    sanitized = '\n'.join(lines)

    return sanitized.strip()


# ============================================================================
# Session ID Validation
# ============================================================================

def validate_session_id(session_id: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate session ID format.

    Expects UUID format or alphanumeric string.

    Args:
        session_id: Session identifier

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if session_id is None:
        return True, None  # Session ID is optional

    # Strip whitespace
    session_id = session_id.strip()

    # Check length (reasonable bounds for UUID or custom ID)
    if len(session_id) < 1 or len(session_id) > 128:
        return False, "Session ID length must be between 1 and 128 characters"

    # Allow alphanumeric, hyphens, and underscores only
    if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
        return False, "Session ID must contain only alphanumeric characters, hyphens, and underscores"

    return True, None


# ============================================================================
# Metadata Validation
# ============================================================================

def validate_chapter_number(chapter: Optional[int]) -> Tuple[bool, Optional[str]]:
    """
    Validate chapter number.

    Args:
        chapter: Chapter number

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if chapter is None:
        return True, None  # Chapter filter is optional

    if not isinstance(chapter, int):
        return False, "Chapter must be an integer"

    if chapter < 1 or chapter > 100:  # Reasonable bounds for textbook chapters
        return False, "Chapter must be between 1 and 100"

    return True, None


def validate_section_identifier(section: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate section identifier format.

    Expects format like "3.2" or "3.2.1".

    Args:
        section: Section identifier

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if section is None:
        return True, None  # Section filter is optional

    # Check format: digits separated by dots
    if not re.match(r'^\d+(\.\d+)*$', section):
        return False, "Section identifier must be in format like '3.2' or '3.2.1'"

    return True, None


def validate_top_k(top_k: int, min_k: int = 1, max_k: int = 20) -> Tuple[bool, Optional[str]]:
    """
    Validate top-k parameter for retrieval.

    Args:
        top_k: Number of results to retrieve
        min_k: Minimum allowed value
        max_k: Maximum allowed value

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not isinstance(top_k, int):
        return False, "top_k must be an integer"

    if top_k < min_k or top_k > max_k:
        return False, f"top_k must be between {min_k} and {max_k}"

    return True, None


def validate_score_threshold(
    score: Optional[float],
    min_score: float = 0.0,
    max_score: float = 1.0
) -> Tuple[bool, Optional[str]]:
    """
    Validate similarity score threshold.

    Args:
        score: Score threshold
        min_score: Minimum allowed value
        max_score: Maximum allowed value

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if score is None:
        return True, None  # Score threshold is optional

    if not isinstance(score, (int, float)):
        return False, "Score threshold must be a number"

    if score < min_score or score > max_score:
        return False, f"Score threshold must be between {min_score} and {max_score}"

    return True, None


# ============================================================================
# Security Checks
# ============================================================================

def check_for_sql_injection(text: str) -> bool:
    """
    Check if text contains potential SQL injection patterns.

    Args:
        text: Input text to check

    Returns:
        bool: True if suspicious patterns detected, False otherwise
    """
    # Common SQL injection patterns (case-insensitive)
    sql_patterns = [
        r"('\s*OR\s+'?[a-z0-9]+'?\s*=\s*'?[a-z0-9]+'?)",  # ' OR '1'='1'
        r"(--)",  # SQL comment
        r"(;\s*DROP\s+TABLE)",  # DROP TABLE
        r"(;\s*DELETE\s+FROM)",  # DELETE FROM
        r"(;\s*UPDATE\s+)",  # UPDATE
        r"(UNION\s+SELECT)",  # UNION SELECT
        r"(EXEC\s*\()",  # EXEC(
    ]

    text_upper = text.upper()
    for pattern in sql_patterns:
        if re.search(pattern, text_upper, re.IGNORECASE):
            return True

    return False


def check_for_xss(text: str) -> bool:
    """
    Check if text contains potential XSS (Cross-Site Scripting) patterns.

    Args:
        text: Input text to check

    Returns:
        bool: True if suspicious patterns detected, False otherwise
    """
    # Common XSS patterns
    xss_patterns = [
        r"<script[^>]*>",  # <script> tag
        r"javascript:",  # javascript: protocol
        r"on\w+\s*=",  # event handlers (onclick=, onload=, etc.)
        r"<iframe[^>]*>",  # <iframe> tag
        r"<embed[^>]*>",  # <embed> tag
        r"<object[^>]*>",  # <object> tag
    ]

    for pattern in xss_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def is_safe_input(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if input is safe (no SQL injection or XSS).

    Args:
        text: Input text to check

    Returns:
        Tuple[bool, Optional[str]]: (is_safe, warning_message)
    """
    if check_for_sql_injection(text):
        return False, "Potential SQL injection detected"

    if check_for_xss(text):
        return False, "Potential XSS attack detected"

    return True, None


# ============================================================================
# Combined Validation
# ============================================================================

def validate_query_request(
    query: str,
    session_id: Optional[str] = None,
    min_length: int = 1,
    max_length: int = 1000
) -> Tuple[bool, Optional[str]]:
    """
    Validate a complete query request.

    Performs all validation checks for a query request.

    Args:
        query: User query text
        session_id: Optional session identifier
        min_length: Minimum query length
        max_length: Maximum query length

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Validate query text
    is_valid, error = validate_query_text(query, min_length, max_length)
    if not is_valid:
        return False, error

    # Security checks
    is_safe, warning = is_safe_input(query)
    if not is_safe:
        return False, f"Security check failed: {warning}"

    # Validate session ID
    is_valid, error = validate_session_id(session_id)
    if not is_valid:
        return False, error

    return True, None


def validate_selected_text_request(
    query: str,
    selected_text: str,
    session_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate a complete selected-text query request.

    Args:
        query: User query text
        selected_text: Selected text from user
        session_id: Optional session identifier

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Validate query
    is_valid, error = validate_query_text(query, min_length=1, max_length=1000)
    if not is_valid:
        return False, error

    # Validate selected text
    is_valid, error = validate_selected_text(selected_text, min_length=10, max_length=5000)
    if not is_valid:
        return False, error

    # Security checks on query
    is_safe, warning = is_safe_input(query)
    if not is_safe:
        return False, f"Query security check failed: {warning}"

    # Security checks on selected text (less strict)
    if check_for_sql_injection(selected_text):
        return False, "Selected text security check failed: Potential SQL injection"

    # Validate session ID
    is_valid, error = validate_session_id(session_id)
    if not is_valid:
        return False, error

    return True, None


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of validation utilities.
    """
    # Test query validation
    test_queries = [
        ("What is inverse kinematics?", True),
        ("", False),
        ("   ", False),
        ("x" * 1001, False),
        ("' OR '1'='1'", False),  # SQL injection
        ("<script>alert('xss')</script>", False),  # XSS
    ]

    print("Query Validation Tests:")
    for query, expected_valid in test_queries:
        is_valid, error = validate_query_request(query)
        status = "✓" if is_valid == expected_valid else "✗"
        print(f"{status} '{query[:30]}...' - Valid: {is_valid}, Error: {error}")

    print("\nSanitization Tests:")
    dirty_queries = [
        "  What   is   kinematics?  ",
        "Query with <script>alert('xss')</script>",
        "Query\x00with\x00nulls",
    ]

    for query in dirty_queries:
        sanitized = sanitize_query(query)
        print(f"Original: '{query}'")
        print(f"Sanitized: '{sanitized}'")
        print()

    print("Session ID Validation Tests:")
    test_session_ids = [
        ("550e8400-e29b-41d4-a716-446655440000", True),  # UUID
        ("session_123", True),  # Alphanumeric with underscore
        ("session-abc-def", True),  # With hyphens
        ("session@123", False),  # Invalid character
        ("", False),  # Empty
        (None, True),  # None (optional)
    ]

    for session_id, expected_valid in test_session_ids:
        is_valid, error = validate_session_id(session_id)
        status = "✓" if is_valid == expected_valid else "✗"
        print(f"{status} '{session_id}' - Valid: {is_valid}, Error: {error}")
