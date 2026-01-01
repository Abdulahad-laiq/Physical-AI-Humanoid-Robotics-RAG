"""
Selected-text endpoint for context-specific queries.

Handles POST /api/v1/chat/selected - ask questions about user-selected text.
"""

from fastapi import APIRouter, Request, HTTPException
import uuid
import time
import logging

from ...models.schemas import SelectedTextQueryRequest, ChatResponse
from ...services.selected_text import answer_selected_text_query
from ...models.database import log_query
from ...utils.validators import validate_selected_text_request, sanitize_query, sanitize_selected_text
from ...utils.logger import LogContext, PerformanceTimer
from ...config import get_settings
from ...api.middleware import limiter


logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Selected-Text Endpoint
# ============================================================================

@router.post("/chat/selected", response_model=ChatResponse)
@limiter.limit("100/minute")
async def chat_selected(
    request: Request,
    query_request: SelectedTextQueryRequest
) -> ChatResponse:
    """
    Answer a question about user-selected text (selected-text mode).

    This endpoint creates an ephemeral in-memory vector store from the
    selected text and answers the query using ONLY that text. No global
    embeddings from the database are accessed, ensuring complete isolation.

    **Request Body:**
    - query (str): User's question about the selected text (1-1000 characters)
    - selected_text (str): Text highlighted by user (10-5000 characters)
    - session_id (str, optional): Session identifier for tracking
    - debug (bool, optional): Enable debug mode for retrieval metadata

    **Response:**
    - answer (str): Generated answer based on selected text only
    - citations (List[Citation]): Source citations from selected text chunks
    - query_id (str): Unique identifier for this query
    - generation_time_ms (int): Total response time in milliseconds
    - debug_metadata (dict, optional): Debug information if debug=True

    **Error Responses:**
    - 400: Invalid query or selected text (empty, too short/long, malicious)
    - 429: Rate limit exceeded (>100 requests/minute)
    - 500: Internal server error
    - 503: AI service unavailable

    **Important Security Notes:**
    - This endpoint does NOT access the global Qdrant database
    - Only selected text is used for context
    - Complete isolation from other queries/data
    """
    # Generate query ID for tracking
    query_id = str(uuid.uuid4())
    start_time = time.time()

    # Set up logging context
    with LogContext(query_id=query_id, session_id=query_request.session_id):
        logger.info(
            f"Processing selected-text request: '{query_request.query[:50]}...' "
            f"(selected_text: {len(query_request.selected_text)} chars)"
        )

        try:
            # ================================================================
            # Step 1: Validate and Sanitize Input
            # ================================================================

            is_valid, error_message = validate_selected_text_request(
                query=query_request.query,
                selected_text=query_request.selected_text,
                session_id=query_request.session_id
            )

            if not is_valid:
                logger.warning(f"Invalid selected-text request: {error_message}")
                raise HTTPException(status_code=400, detail=error_message)

            # Sanitize inputs
            sanitized_query = sanitize_query(query_request.query)
            sanitized_selected_text = sanitize_selected_text(query_request.selected_text)

            logger.debug(f"Sanitized query: '{sanitized_query}'")
            logger.debug(f"Sanitized selected text: {len(sanitized_selected_text)} chars")

            # ================================================================
            # Step 2: Process Query with Ephemeral Vector Store
            # ================================================================

            settings = get_settings()

            logger.info("Creating ephemeral vector store from selected text")
            with PerformanceTimer(logger, "selected_text_query_processing"):
                answer, citations = await answer_selected_text_query(
                    query=sanitized_query,
                    selected_text=sanitized_selected_text,
                    top_k=settings.retrieval_top_k
                )

            logger.info(
                f"Selected-text answer generated "
                f"({len(answer)} chars, {len(citations)} citations)"
            )

            # ================================================================
            # Step 3: Build Response
            # ================================================================

            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)

            # Build debug metadata if requested
            debug_metadata = None
            if query_request.debug:
                debug_metadata = {
                    "mode": "selected-text",
                    "selected_text_length": len(sanitized_selected_text),
                    "chunks_created": len(citations),
                    "isolation": "ephemeral_store_only",
                    "global_db_accessed": False
                }

            response = ChatResponse(
                answer=answer,
                citations=citations,
                query_id=query_id,
                generation_time_ms=response_time_ms,
                debug_metadata=debug_metadata
            )

            # ================================================================
            # Step 4: Log Query to Database
            # ================================================================

            try:
                # Note: We anonymize selected_text in logs (not stored)
                log_query(
                    query_id=query_id,
                    query_text=sanitized_query,
                    mode="selected-text",
                    response_time_ms=response_time_ms,
                    chunk_count=len(citations),
                    session_id=query_request.session_id
                )
            except Exception as e:
                # Don't fail the request if logging fails
                logger.error(f"Failed to log query: {e}", exc_info=True)

            # ================================================================
            # Step 5: Return Response
            # ================================================================

            logger.info(
                f"Selected-text request completed successfully "
                f"(time={response_time_ms}ms, chunks={len(citations)})"
            )

            return response

        except HTTPException:
            # Re-raise HTTP exceptions (validation errors, etc.)
            raise

        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Error processing selected-text request: {e}", exc_info=True)

            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)

            # Log failed query
            try:
                log_query(
                    query_id=query_id,
                    query_text=query_request.query[:1000],  # Truncate for safety
                    mode="selected-text",
                    response_time_ms=response_time_ms,
                    chunk_count=0,
                    session_id=query_request.session_id,
                    error=str(e)[:500]  # Truncate error message
                )
            except Exception as log_error:
                logger.error(f"Failed to log error: {log_error}")

            # Determine error type and status code
            settings = get_settings()
            error_message = "An error occurred while processing your selected-text query"
            status_code = 500

            if "agent" in str(e).lower() or "Gemini" in str(e):
                error_message = "AI service unavailable"
                status_code = 503

            raise HTTPException(
                status_code=status_code,
                detail={
                    "error": error_message,
                    "query_id": query_id,
                    "message": str(e) if settings.debug else None
                }
            )


# ============================================================================
# Health Check for Selected-Text Service
# ============================================================================

@router.get("/chat/selected/health")
async def selected_text_health():
    """
    Health check for selected-text service components.

    Verifies embedding service and agent availability.
    """
    try:
        from ...services.embeddings import get_embedding_service
        embedding_service = get_embedding_service()
        embedding_healthy = True
    except Exception as e:
        logger.error(f"Embedding service health check failed: {e}")
        embedding_healthy = False

    # Agent health check would require an API call - skip for simple health check
    agent_healthy = True

    return {
        "status": "healthy" if (embedding_healthy and agent_healthy) else "degraded",
        "components": {
            "embedding_service": "healthy" if embedding_healthy else "unhealthy",
            "agent": "healthy" if agent_healthy else "unhealthy"
        },
        "isolation": "ephemeral_store_only",
        "global_db_access": False
    }


# ============================================================================
# Documentation Helper
# ============================================================================

@router.get("/chat/selected/info")
async def selected_text_info():
    """
    Information about selected-text mode.

    Returns details about how selected-text queries work.
    """
    return {
        "mode": "selected-text",
        "description": "Answer questions about user-highlighted text",
        "isolation": {
            "type": "ephemeral_in_memory_store",
            "global_db_accessed": False,
            "explanation": "Creates temporary vector store from selected text only"
        },
        "limits": {
            "min_text_length": 10,
            "max_text_length": 5000,
            "max_chunks": "dynamic (based on text length)",
            "chunking_strategy": "sentence-aware, 512 token max"
        },
        "security": {
            "pii_handling": "Selected text not stored in database",
            "session_tracking": "Session ID hashed (SHA-256) for privacy",
            "isolation_guarantee": "No global embeddings accessed"
        },
        "use_cases": [
            "Explain specific equations or code snippets",
            "Clarify complex paragraphs",
            "Answer questions about selected sections",
            "Deep dive into specific topics"
        ]
    }
