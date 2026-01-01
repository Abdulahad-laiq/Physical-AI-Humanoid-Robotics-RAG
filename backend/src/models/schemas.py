"""
Pydantic data models for RAG Chatbot API.

All request/response schemas and internal data structures for the RAG chatbot,
including text chunks, queries, citations, and responses.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid


# ============================================================================
# Core Data Models
# ============================================================================

class TextChunk(BaseModel):
    """
    Represents a chunk of text from the textbook stored in the vector database.

    Attributes:
        chunk_id: Unique identifier (format: ch{chapter}-s{section}-{index})
        text: The actual text content of the chunk
        embedding: 384-dimensional vector from all-MiniLM-L6-v2
        chapter: Chapter number (e.g., 3)
        section: Section identifier (e.g., "3.2")
        subsection: Optional subsection identifier (e.g., "3.2.1")
        url_anchor: URL fragment for citation linking (e.g., "#inverse-kinematics")
        token_count: Number of tokens in the chunk (max 512)
        chunk_index: Sequential index within the section (0-based)
    """
    chunk_id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., min_length=1, max_length=10000, description="Chunk text content")
    embedding: List[float] = Field(..., min_length=384, max_length=384, description="384-dim embedding vector")
    chapter: int = Field(..., ge=1, description="Chapter number")
    section: str = Field(..., description="Section identifier (e.g., '3.2')")
    subsection: Optional[str] = Field(None, description="Subsection identifier (e.g., '3.2.1')")
    url_anchor: str = Field(..., description="URL anchor for citation linking")
    token_count: int = Field(..., ge=1, le=512, description="Token count (max 512)")
    chunk_index: int = Field(..., ge=0, description="Sequential index within section")

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "ch3-s3.2-001",
                "text": "Inverse kinematics (IK) is the process of determining joint angles...",
                "embedding": [0.123, -0.456, 0.789],  # Truncated for example
                "chapter": 3,
                "section": "3.2",
                "subsection": "3.2.1",
                "url_anchor": "#inverse-kinematics",
                "token_count": 487,
                "chunk_index": 1
            }
        }


class Citation(BaseModel):
    """
    Source citation for a chatbot response.

    Attributes:
        chunk_id: ID of the source chunk
        chapter: Chapter number for display
        section: Section identifier for display
        url_anchor: URL fragment for clickable link
        relevance_score: Cosine similarity score (0.0-1.0)
        text_preview: First 200 characters of source text
        source: Human-readable source description
    """
    chunk_id: str = Field(..., description="Source chunk ID")
    chapter: int = Field(..., ge=0, description="Chapter number (0 for non-chapter content)")
    section: str = Field(..., description="Section identifier")
    url_anchor: str = Field(..., description="URL anchor for linking")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0.0-1.0)")
    text_preview: str = Field(..., max_length=200, description="Text preview (max 200 chars)")
    source: str = Field(..., description="Human-readable source description")

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "ch3-s3.2-001",
                "chapter": 3,
                "section": "3.2",
                "url_anchor": "#inverse-kinematics",
                "relevance_score": 0.89,
                "text_preview": "Inverse kinematics (IK) is the process of determining joint angles that achieve a desired end-effector position. This is fundamental to robot motion planning...",
                "source": "Chapter 3, Section 3.2: Inverse Kinematics"
            }
        }


# ============================================================================
# Request Models
# ============================================================================

class QueryRequest(BaseModel):
    """
    Request payload for global query mode (POST /api/v1/chat).

    Attributes:
        query: User's question (1-1000 characters)
        session_id: Optional session identifier for conversation tracking
        debug: Enable debug mode (returns retrieval metadata)
    """
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    session_id: Optional[str] = Field(None, description="Optional session ID")
    debug: bool = Field(False, description="Enable debug mode")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate query is not just whitespace."""
        if not v.strip():
            raise ValueError("Query cannot be empty or only whitespace")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is inverse kinematics?",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "debug": False
            }
        }


class SelectedTextQueryRequest(BaseModel):
    """
    Request payload for selected-text mode (POST /api/v1/chat/selected).

    Attributes:
        query: User's question about the selected text (1-1000 characters)
        selected_text: User-highlighted text from the textbook (10-5000 characters)
        session_id: Optional session identifier for conversation tracking
        debug: Enable debug mode (returns retrieval metadata)
    """
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    selected_text: str = Field(..., min_length=10, max_length=5000, description="Selected text from textbook")
    session_id: Optional[str] = Field(None, description="Optional session ID")
    debug: bool = Field(False, description="Enable debug mode")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate query is not just whitespace."""
        if not v.strip():
            raise ValueError("Query cannot be empty or only whitespace")
        return v.strip()

    @field_validator('selected_text')
    @classmethod
    def validate_selected_text(cls, v: str) -> str:
        """Validate selected text meets minimum length requirement."""
        if len(v.strip()) < 10:
            raise ValueError("Selected text must be at least 10 characters")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Explain this equation",
                "selected_text": "J = ∂f/∂q where J is the Jacobian matrix mapping joint velocities to end-effector velocities. The Jacobian is a fundamental concept in robot kinematics...",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "debug": False
            }
        }


# ============================================================================
# Response Models
# ============================================================================

class ChatResponse(BaseModel):
    """
    Response payload for chat endpoints.

    Attributes:
        answer: Generated answer from the agent
        citations: List of source citations (ordered by relevance)
        query_id: Unique identifier for this query (for debugging/logging)
        generation_time_ms: Total response generation time in milliseconds
        debug_metadata: Optional debug information (only if debug=True in request)
    """
    answer: str = Field(..., description="Generated answer")
    citations: List[Citation] = Field(..., description="Source citations (ordered by relevance)")
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique query ID")
    generation_time_ms: int = Field(..., ge=0, description="Generation time in milliseconds")
    debug_metadata: Optional[dict] = Field(None, description="Debug information (if debug=True)")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Inverse kinematics solves for joint angles that achieve a desired end-effector position. [Chapter 3, Section 3.2]",
                "citations": [
                    {
                        "chunk_id": "ch3-s3.2-001",
                        "chapter": 3,
                        "section": "3.2",
                        "url_anchor": "#inverse-kinematics",
                        "relevance_score": 0.89,
                        "text_preview": "Inverse kinematics (IK) is the process...",
                        "source": "Chapter 3, Section 3.2: Inverse Kinematics"
                    }
                ],
                "query_id": "550e8400-e29b-41d4-a716-446655440000",
                "generation_time_ms": 1234,
                "debug_metadata": None
            }
        }


# ============================================================================
# Database Models (for query logging)
# ============================================================================

class QueryLog(BaseModel):
    """
    Query log entry for Neon PostgreSQL storage.

    Attributes:
        query_id: Unique query identifier
        query_text: The user's query (stored for analytics, not PII)
        timestamp: Query timestamp
        mode: Query mode ("global" or "selected-text")
        session_id_hash: Hashed session ID (SHA-256, for privacy)
        response_time_ms: Response generation time in milliseconds
        chunk_count: Number of chunks retrieved
        error: Error message if query failed (None if successful)
    """
    query_id: str = Field(..., description="Unique query ID")
    query_text: str = Field(..., description="User query text")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Query timestamp")
    mode: str = Field(..., description="Query mode (global or selected-text)")
    session_id_hash: Optional[str] = Field(None, description="Hashed session ID (SHA-256)")
    response_time_ms: int = Field(..., ge=0, description="Response time in milliseconds")
    chunk_count: int = Field(..., ge=0, description="Number of chunks retrieved")
    error: Optional[str] = Field(None, description="Error message if failed")

    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v: str) -> str:
        """Validate mode is one of the allowed values."""
        if v not in ["global", "selected-text"]:
            raise ValueError("Mode must be 'global' or 'selected-text'")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "550e8400-e29b-41d4-a716-446655440000",
                "query_text": "What is inverse kinematics?",
                "timestamp": "2025-01-15T10:30:00Z",
                "mode": "global",
                "session_id_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "response_time_ms": 1234,
                "chunk_count": 5,
                "error": None
            }
        }


# ============================================================================
# Health Check Models
# ============================================================================

class HealthResponse(BaseModel):
    """
    Health check response for monitoring.

    Attributes:
        status: Service status ("healthy" or "degraded")
        qdrant_connected: Qdrant connection status
        neon_connected: Neon PostgreSQL connection status
        timestamp: Health check timestamp
    """
    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    neon_connected: bool = Field(..., description="Neon PostgreSQL connection status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "qdrant_connected": True,
                "neon_connected": True,
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }
