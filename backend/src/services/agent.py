"""
Agent orchestration service using OpenAI Assistants SDK with Gemini-2.0-flash.

Provides LLM-powered question answering with retrieval-augmented generation (RAG).
Uses Gemini model via OpenAI-compatible endpoint.
"""

from typing import List, Dict, Optional, Tuple
import re
from openai import AsyncOpenAI
import asyncio
import logging

from ..config import get_settings
from ..models.schemas import Citation
from .vector_store import SearchResult


logger = logging.getLogger(__name__)


# ============================================================================
# Agent Configuration
# ============================================================================

class AgentService:
    """
    Service for LLM-based question answering with RAG.

    Uses Gemini-2.0-flash via AsyncOpenAI client for OpenAI-compatible access.
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        base_url: str = None,
        system_prompt: str = None,
        max_tokens: int = None,
        temperature: float = None
    ):
        """
        Initialize agent service.

        Args:
            api_key: Gemini API key (defaults to config)
            model: Model name (defaults to config)
            base_url: API base URL (defaults to config)
            system_prompt: System instructions (defaults to config)
            max_tokens: Max tokens for response (defaults to config)
            temperature: Temperature for generation (defaults to config)
        """
        settings = get_settings()

        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        self.base_url = base_url or settings.gemini_base_url
        self.system_prompt = system_prompt or settings.agent_system_prompt
        self.max_tokens = max_tokens or settings.gemini_max_tokens
        self.temperature = temperature or settings.gemini_temperature

        # Initialize AsyncOpenAI client pointing to Gemini
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        logger.info(
            f"Agent service initialized (model={self.model}, "
            f"max_tokens={self.max_tokens}, temperature={self.temperature})"
        )

    async def generate_answer(
        self,
        query: str,
        context_chunks: List[SearchResult],
        mode: str = "global"
    ) -> Tuple[str, List[Citation]]:
        """
        Generate answer to query using retrieved context.

        Args:
            query: User's question
            context_chunks: Retrieved chunks from vector store
            mode: Query mode ("global" or "selected-text")

        Returns:
            Tuple[str, List[Citation]]: (answer, citations)

        Raises:
            Exception: If agent call fails
        """
        logger.info(f"Generating answer (mode={mode}, chunks={len(context_chunks)})")

        # Format context for agent
        context_text = self._format_context(context_chunks)

        # Build messages
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": self._build_user_message(query, context_text, mode)
            }
        ]

        try:
            # Call Gemini via AsyncOpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            # Extract answer
            answer = response.choices[0].message.content.strip()

            # Parse citations from answer
            citations = self._extract_citations(answer, context_chunks)

            logger.info(f"Answer generated ({len(answer)} chars, {len(citations)} citations)")

            return answer, citations

        except Exception as e:
            logger.error(f"Error calling agent: {e}", exc_info=True)
            raise

    def _format_context(self, chunks: List[SearchResult]) -> str:
        """
        Format retrieved chunks into context string.

        Args:
            chunks: Retrieved search results

        Returns:
            str: Formatted context
        """
        if not chunks:
            return "No relevant information found in the textbook."

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Source {i}] Chapter {chunk.chapter}, Section {chunk.section}"
                + (f", Subsection {chunk.subsection}" if chunk.subsection else "")
                + f"\n{chunk.text}\n"
            )

        return "\n".join(context_parts)

    def _build_user_message(
        self,
        query: str,
        context: str,
        mode: str
    ) -> str:
        """
        Build user message with query and context.

        Args:
            query: User's question
            context: Formatted context from retrieval
            mode: Query mode

        Returns:
            str: Complete user message
        """
        if mode == "selected-text":
            return (
                f"Based on the following selected text from the textbook, answer the question.\n\n"
                f"Selected Text:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Answer the question using ONLY information from the selected text above. "
                f"If the answer is not in the selected text, say 'Information not found in the selected text.'"
            )
        else:
            return (
                f"Based on the following excerpts from the textbook, answer the question.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Provide a clear answer based on the context. "
                f"Always cite sources using [Chapter X, Section Y.Z] format. "
                f"If the answer is not in the context, say 'Information not found in the book.'"
            )

    def _extract_citations(
        self,
        answer: str,
        chunks: List[SearchResult]
    ) -> List[Citation]:
        """
        Extract citations from answer text and match to chunks.

        Looks for patterns like [Chapter 3, Section 3.2] in the answer.

        Args:
            answer: Generated answer text
            chunks: Retrieved chunks

        Returns:
            List[Citation]: Parsed citations
        """
        citations = []

        # Find citation patterns in answer
        # Patterns: [Chapter X, Section Y.Z], [Chapter X], etc.
        citation_pattern = r'\[Chapter\s+(\d+)(?:,\s*Section\s+([\d.]+))?\]'
        matches = re.finditer(citation_pattern, answer, re.IGNORECASE)

        cited_chunks = set()  # Track which chunks were cited

        for match in matches:
            chapter_num = int(match.group(1))
            section_id = match.group(2)  # May be None

            # Find matching chunks
            for chunk in chunks:
                if chunk.chapter == chapter_num:
                    # Match section if specified
                    if section_id and chunk.section != section_id:
                        continue

                    # Avoid duplicate citations
                    chunk_key = (chunk.chunk_id, chunk.chapter, chunk.section)
                    if chunk_key in cited_chunks:
                        continue

                    cited_chunks.add(chunk_key)

                    # Create citation
                    citation = Citation(
                        chunk_id=chunk.chunk_id,
                        chapter=chunk.chapter,
                        section=chunk.section,
                        url_anchor=chunk.url_anchor,
                        relevance_score=chunk.score,
                        text_preview=chunk.text[:200],
                        source=f"Chapter {chunk.chapter}, Section {chunk.section}"
                        + (f", Subsection {chunk.subsection}" if chunk.subsection else "")
                    )
                    citations.append(citation)

        # If no citations found in text but chunks were provided, add top chunks
        if not citations and chunks:
            logger.warning("No citations found in answer text, adding top chunks as citations")
            for chunk in chunks[:3]:  # Add top 3 chunks
                citation = Citation(
                    chunk_id=chunk.chunk_id,
                    chapter=chunk.chapter,
                    section=chunk.section,
                    url_anchor=chunk.url_anchor,
                    relevance_score=chunk.score,
                    text_preview=chunk.text[:200],
                    source=f"Chapter {chunk.chapter}, Section {chunk.section}"
                    + (f", Subsection {chunk.subsection}" if chunk.subsection else "")
                )
                citations.append(citation)

        # Sort by relevance score (descending)
        citations.sort(key=lambda c: c.relevance_score, reverse=True)

        return citations

    async def health_check(self) -> bool:
        """
        Check if agent service is accessible.

        Returns:
            bool: True if service is healthy, False otherwise
        """
        try:
            # Simple test call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"Agent health check failed: {e}")
            return False


# ============================================================================
# Global Agent Instance
# ============================================================================

_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """
    Get or create the global agent service instance.

    Returns:
        AgentService: Global agent singleton
    """
    global _agent_service

    if _agent_service is None:
        _agent_service = AgentService()

    return _agent_service


# ============================================================================
# Convenience Functions
# ============================================================================

async def answer_query(
    query: str,
    context_chunks: List[SearchResult],
    mode: str = "global"
) -> Tuple[str, List[Citation]]:
    """
    Generate answer to query using global agent service.

    Args:
        query: User's question
        context_chunks: Retrieved chunks
        mode: Query mode

    Returns:
        Tuple[str, List[Citation]]: (answer, citations)
    """
    agent = get_agent_service()
    return await agent.generate_answer(query, context_chunks, mode)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of agent service.
    """
    import asyncio
    from ..services.vector_store import SearchResult

    async def test_agent():
        # Initialize agent
        agent = get_agent_service()

        # Mock search results
        mock_chunks = [
            SearchResult(
                chunk_id="ch3-s3.2-001",
                score=0.89,
                text="Inverse kinematics (IK) is the process of determining joint angles that achieve a desired end-effector position and orientation.",
                chapter=3,
                section="3.2",
                subsection="3.2.1",
                url_anchor="#inverse-kinematics",
                metadata={}
            )
        ]

        # Test query
        query = "What is inverse kinematics?"

        print("Testing agent service...")
        print(f"Query: {query}")
        print(f"Context chunks: {len(mock_chunks)}")

        try:
            answer, citations = await agent.generate_answer(
                query=query,
                context_chunks=mock_chunks,
                mode="global"
            )

            print(f"\nAnswer: {answer}")
            print(f"\nCitations ({len(citations)}):")
            for citation in citations:
                print(f"  - {citation.source} (score: {citation.relevance_score:.2f})")
                print(f"    {citation.text_preview[:100]}...")

        except Exception as e:
            print(f"Error: {e}")

        # Health check
        is_healthy = await agent.health_check()
        print(f"\nHealth check: {'[OK] Healthy' if is_healthy else '[FAILED]'}")

    # Run test
    asyncio.run(test_agent())
