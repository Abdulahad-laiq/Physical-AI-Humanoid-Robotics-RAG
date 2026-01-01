"""
Chat endpoint for global query mode.

Handles POST /api/v1/chat - ask questions about the entire textbook.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime
import time
import logging

from ...models.schemas import QueryRequest, ChatResponse
from ...services.embeddings import embed_text
from ...services.vector_store import get_vector_store
from ...services.agent import answer_query
from ...models.database import log_query
from ...utils.validators import validate_query_request, sanitize_query
from ...utils.logger import LogContext, PerformanceTimer
from ...config import get_settings
from ...api.middleware import limiter


logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Chat Endpoint
# ============================================================================

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("100/minute")
async def chat(request: Request, query_request: QueryRequest) -> ChatResponse:
    """
    Answer a question about the textbook (global query mode).

    Retrieves relevant chunks from the vector database and generates
    an answer using the LLM agent with proper citations.

    **Request Body:**
    - query (str): User's question (1-1000 characters)
    - session_id (str, optional): Session identifier for tracking
    - debug (bool, optional): Enable debug mode for retrieval metadata

    **Response:**
    - answer (str): Generated answer with citations
    - citations (List[Citation]): Source citations with chapter/section info
    - query_id (str): Unique identifier for this query
    - generation_time_ms (int): Total response time in milliseconds
    - debug_metadata (dict, optional): Debug information if debug=True

    **Error Responses:**
    - 400: Invalid query (empty, too long, or contains malicious content)
    - 429: Rate limit exceeded (>100 requests/minute)
    - 500: Internal server error
    - 503: Service unavailable (Qdrant or agent unavailable)
    """
    # Generate query ID for tracking
    query_id = str(uuid.uuid4())
    start_time = time.time()

    # Set up logging context
    with LogContext(query_id=query_id, session_id=query_request.session_id):
        logger.info(f"Processing chat request: '{query_request.query[:50]}...'")

        try:
            # ================================================================
            # Step 1: Validate and Sanitize Input
            # ================================================================

            is_valid, error_message = validate_query_request(
                query=query_request.query,
                session_id=query_request.session_id
            )

            if not is_valid:
                logger.warning(f"Invalid query request: {error_message}")
                raise HTTPException(status_code=400, detail=error_message)

            # Sanitize query
            sanitized_query = sanitize_query(query_request.query)
            logger.debug(f"Sanitized query: '{sanitized_query}'")

            # ================================================================
            # Step 2: Generate Query Embedding
            # ================================================================

            logger.info("Generating query embedding")
            with PerformanceTimer(logger, "embedding_generation"):
                query_embedding = embed_text(sanitized_query, normalize=True)

            logger.debug(f"Query embedding: {len(query_embedding)} dimensions")

            # ================================================================
            # Step 3: Retrieve Relevant Chunks from Vector Store
            # ================================================================

            settings = get_settings()
            vector_store = get_vector_store()

            logger.info(
                f"Searching vector store (top_k={settings.retrieval_top_k}, "
                f"threshold={settings.retrieval_score_threshold})"
            )

            with PerformanceTimer(logger, "vector_search"):
                search_results = vector_store.search(
                    query_embedding=query_embedding,
                    top_k=settings.retrieval_top_k,
                    score_threshold=settings.retrieval_score_threshold
                )

            logger.info(f"Retrieved {len(search_results)} chunks")

            # Check if any results found
            if not search_results:
                logger.info("No relevant chunks found in vector store")
                # Return "not found" response
                end_time = time.time()
                response_time_ms = int((end_time - start_time) * 1000)

                # Log query
                log_query(
                    query_id=query_id,
                    query_text=sanitized_query,
                    mode="global",
                    response_time_ms=response_time_ms,
                    chunk_count=0,
                    session_id=query_request.session_id
                )

                return ChatResponse(
                    answer="Information not found in the book. Please try rephrasing your question or ask about a different topic covered in the textbook.",
                    citations=[],
                    query_id=query_id,
                    generation_time_ms=response_time_ms,
                    debug_metadata=None
                )

            # ================================================================
            # Step 4: Generate Answer with Agent
            # ================================================================

            logger.info("Generating answer with agent")
            with PerformanceTimer(logger, "agent_generation"):
                answer, citations = await answer_query(
                    query=sanitized_query,
                    context_chunks=search_results,
                    mode="global"
                )

            logger.info(f"Answer generated ({len(answer)} chars, {len(citations)} citations)")

            # ================================================================
            # Step 5: Build Response
            # ================================================================

            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)

            # Build debug metadata if requested
            debug_metadata = None
            if query_request.debug:
                debug_metadata = {
                    "retrieval": {
                        "chunks_retrieved": len(search_results),
                        "top_scores": [r.score for r in search_results[:3]],
                        "search_time_ms": response_time_ms  # Approximate
                    },
                    "chunks": [
                        {
                            "chunk_id": r.chunk_id,
                            "score": r.score,
                            "chapter": r.chapter,
                            "section": r.section,
                            "text_preview": r.text[:100]
                        }
                        for r in search_results
                    ]
                }

            response = ChatResponse(
                answer=answer,
                citations=citations,
                query_id=query_id,
                generation_time_ms=response_time_ms,
                debug_metadata=debug_metadata
            )

            # ================================================================
            # Step 6: Log Query to Database
            # ================================================================

            try:
                log_query(
                    query_id=query_id,
                    query_text=sanitized_query,
                    mode="global",
                    response_time_ms=response_time_ms,
                    chunk_count=len(search_results),
                    session_id=query_request.session_id
                )
            except Exception as e:
                # Don't fail the request if logging fails
                logger.error(f"Failed to log query: {e}", exc_info=True)

            # ================================================================
            # Step 7: Return Response
            # ================================================================

            logger.info(
                f"Chat request completed successfully "
                f"(time={response_time_ms}ms, chunks={len(search_results)})"
            )

            return response

        except HTTPException:
            # Re-raise HTTP exceptions (validation errors, etc.)
            raise

        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Error processing chat request: {e}", exc_info=True)

            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)

            # Log failed query
            try:
                log_query(
                    query_id=query_id,
                    query_text=query_request.query[:1000],  # Truncate for safety
                    mode="global",
                    response_time_ms=response_time_ms,
                    chunk_count=0,
                    session_id=query_request.session_id,
                    error=str(e)[:500]  # Truncate error message
                )
            except Exception as log_error:
                logger.error(f"Failed to log error: {log_error}")

            # Determine error type and status code
            error_message = "An error occurred while processing your request"
            status_code = 500

            if "Qdrant" in str(e) or "vector" in str(e).lower():
                error_message = "Vector search service unavailable"
                status_code = 503
            elif "agent" in str(e).lower() or "Gemini" in str(e):
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
# Health Check for Chat Service
# ============================================================================

@router.get("/chat/health")
async def chat_health():
    """
    Health check for chat service components.

    Returns status of vector store and agent service.
    """
    try:
        vector_store = get_vector_store()
        qdrant_healthy = vector_store.health_check()
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        qdrant_healthy = False

    # Agent health check would require an API call - skip for simple health check
    agent_healthy = True

    return {
        "status": "healthy" if (qdrant_healthy and agent_healthy) else "degraded",
        "components": {
            "vector_store": "healthy" if qdrant_healthy else "unhealthy",
            "agent": "healthy" if agent_healthy else "unhealthy"
        }
    }
