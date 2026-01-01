"""
Selected-text query service with ephemeral vector store.

Provides isolated question answering for user-selected text.
Creates temporary in-memory vector store to ensure no global embedding leakage.
"""

from typing import List, Tuple
import numpy as np
from dataclasses import dataclass
import logging

from ..models.schemas import Citation
from .chunking import split_text_by_sentences, count_tokens
from .embeddings import embed_texts
from .agent import get_agent_service


logger = logging.getLogger(__name__)


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class EphemeralChunk:
    """
    Temporary chunk from selected text.

    Attributes:
        chunk_id: Temporary identifier (format: selected-{index})
        text: Chunk text content
        embedding: 384-dimensional embedding vector
        chunk_index: Sequential index (0-based)
    """
    chunk_id: str
    text: str
    embedding: List[float]
    chunk_index: int


@dataclass
class EphemeralSearchResult:
    """
    Search result from ephemeral vector store.

    Attributes:
        chunk_id: Temporary chunk identifier
        score: Cosine similarity score (0-1)
        text: Chunk text content
        chunk_index: Sequential index
    """
    chunk_id: str
    score: float
    text: str
    chunk_index: int


# ============================================================================
# Ephemeral Vector Store
# ============================================================================

class EphemeralVectorStore:
    """
    Temporary in-memory vector store for selected text.

    Ensures complete isolation from global Qdrant database.
    Exists only for the duration of a single query.
    """

    def __init__(self, chunks: List[EphemeralChunk]):
        """
        Initialize ephemeral store with chunks.

        Args:
            chunks: List of ephemeral chunks with embeddings
        """
        self.chunks = chunks
        logger.info(f"Ephemeral vector store created with {len(chunks)} chunks")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: float = 0.0
    ) -> List[EphemeralSearchResult]:
        """
        Search ephemeral store for similar chunks.

        Uses cosine similarity for scoring.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            score_threshold: Minimum similarity score

        Returns:
            List[EphemeralSearchResult]: Top-k search results
        """
        if not self.chunks:
            logger.warning("Ephemeral store is empty")
            return []

        # Convert query to numpy array
        query_vec = np.array(query_embedding)

        # Calculate cosine similarity for all chunks
        scores = []
        for chunk in self.chunks:
            chunk_vec = np.array(chunk.embedding)

            # Cosine similarity (vectors already normalized from embedding service)
            similarity = np.dot(query_vec, chunk_vec)
            scores.append((chunk, float(similarity)))

        # Sort by score (descending)
        scores.sort(key=lambda x: x[1], reverse=True)

        # Filter by threshold and take top-k
        results = []
        for chunk, score in scores[:top_k]:
            if score >= score_threshold:
                result = EphemeralSearchResult(
                    chunk_id=chunk.chunk_id,
                    score=score,
                    text=chunk.text,
                    chunk_index=chunk.chunk_index
                )
                results.append(result)

        logger.info(f"Ephemeral search returned {len(results)} results (top_k={top_k})")
        return results


# ============================================================================
# Selected Text Service
# ============================================================================

class SelectedTextService:
    """
    Service for processing selected-text queries.

    Handles chunking, embedding, and query processing for user-selected text.
    """

    def __init__(self, max_chunk_tokens: int = 512):
        """
        Initialize selected-text service.

        Args:
            max_chunk_tokens: Maximum tokens per chunk
        """
        self.max_chunk_tokens = max_chunk_tokens

    def chunk_selected_text(self, text: str) -> List[str]:
        """
        Chunk selected text into smaller pieces if needed.

        Args:
            text: Selected text from user

        Returns:
            List[str]: List of text chunks
        """
        token_count = count_tokens(text)

        # If text fits in one chunk, return as-is
        if token_count <= self.max_chunk_tokens:
            logger.info(f"Selected text fits in one chunk ({token_count} tokens)")
            return [text]

        # Split by sentences
        logger.info(f"Splitting selected text ({token_count} tokens) into chunks")
        chunks = split_text_by_sentences(text, max_tokens=self.max_chunk_tokens)

        logger.info(f"Selected text chunked into {len(chunks)} pieces")
        return chunks

    def create_ephemeral_store(
        self,
        selected_text: str
    ) -> EphemeralVectorStore:
        """
        Create ephemeral vector store from selected text.

        Args:
            selected_text: Text selected by user

        Returns:
            EphemeralVectorStore: Temporary in-memory vector store
        """
        # Chunk the text
        text_chunks = self.chunk_selected_text(selected_text)

        # Generate embeddings for all chunks
        logger.info(f"Generating embeddings for {len(text_chunks)} selected-text chunks")
        embeddings = embed_texts(text_chunks, normalize=True, show_progress=False)

        # Create ephemeral chunks
        ephemeral_chunks = []
        for i, (text, embedding) in enumerate(zip(text_chunks, embeddings)):
            chunk = EphemeralChunk(
                chunk_id=f"selected-{i:03d}",
                text=text,
                embedding=embedding,
                chunk_index=i
            )
            ephemeral_chunks.append(chunk)

        # Create and return ephemeral store
        return EphemeralVectorStore(ephemeral_chunks)

    async def answer_query(
        self,
        query: str,
        selected_text: str,
        top_k: int = 5
    ) -> Tuple[str, List[Citation]]:
        """
        Answer a query about selected text.

        Creates ephemeral vector store, retrieves relevant chunks,
        and generates answer using agent.

        Args:
            query: User's question
            selected_text: Text selected by user
            top_k: Number of chunks to retrieve

        Returns:
            Tuple[str, List[Citation]]: (answer, citations)
        """
        logger.info(f"Processing selected-text query: '{query[:50]}...'")

        # Create ephemeral store
        ephemeral_store = self.create_ephemeral_store(selected_text)

        # Generate query embedding
        from .embeddings import embed_text
        query_embedding = embed_text(query, normalize=True)

        # Search ephemeral store (no global database access)
        search_results = ephemeral_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=0.0  # No threshold for selected text (user chose it)
        )

        if not search_results:
            logger.warning("No chunks retrieved from ephemeral store")
            return "Information not found in the selected text.", []

        # Convert ephemeral results to format agent expects
        from .vector_store import SearchResult

        agent_chunks = []
        for result in search_results:
            # Create SearchResult compatible with agent
            # Note: chapter/section not applicable for selected text
            search_result = SearchResult(
                chunk_id=result.chunk_id,
                score=result.score,
                text=result.text,
                chapter=0,  # Not applicable
                section="selected",  # Indicate this is selected text
                subsection=None,
                url_anchor="",
                metadata={"chunk_index": result.chunk_index}
            )
            agent_chunks.append(search_result)

        # Generate answer with agent
        agent = get_agent_service()
        answer, citations = await agent.generate_answer(
            query=query,
            context_chunks=agent_chunks,
            mode="selected-text"
        )

        # Filter citations to only include selected-text sources
        # (Prevent any leakage from agent's internal knowledge)
        filtered_citations = [
            c for c in citations
            if c.chunk_id.startswith("selected-")
        ]

        logger.info(
            f"Selected-text query answered "
            f"({len(filtered_citations)} citations from selected text)"
        )

        return answer, filtered_citations


# ============================================================================
# Global Service Instance
# ============================================================================

_selected_text_service = None


def get_selected_text_service() -> SelectedTextService:
    """
    Get or create the global selected-text service instance.

    Returns:
        SelectedTextService: Global service singleton
    """
    global _selected_text_service

    if _selected_text_service is None:
        _selected_text_service = SelectedTextService()

    return _selected_text_service


# ============================================================================
# Convenience Functions
# ============================================================================

async def answer_selected_text_query(
    query: str,
    selected_text: str,
    top_k: int = 5
) -> Tuple[str, List[Citation]]:
    """
    Answer a query about selected text using global service.

    Args:
        query: User's question
        selected_text: Text selected by user
        top_k: Number of chunks to retrieve

    Returns:
        Tuple[str, List[Citation]]: (answer, citations)
    """
    service = get_selected_text_service()
    return await service.answer_query(query, selected_text, top_k)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of selected-text service.
    """
    import asyncio

    async def test_selected_text():
        # Sample selected text
        selected_text = """
        Inverse kinematics (IK) is the process of determining joint angles
        that achieve a desired end-effector position and orientation. Unlike
        forward kinematics, which has a unique solution, inverse kinematics
        may have multiple solutions, no solution, or an infinite number of
        solutions depending on the robot's configuration and the target pose.

        The Jacobian matrix J relates joint velocities to end-effector velocities:
        v = J(q) * q_dot, where v is the end-effector velocity and q_dot is the
        joint velocity vector. The inverse Jacobian can be used to compute joint
        velocities needed to achieve a desired end-effector velocity.
        """

        query = "What is the Jacobian matrix used for?"

        print("Testing Selected-Text Service...")
        print(f"Selected text: {len(selected_text)} characters")
        print(f"Query: {query}")
        print()

        try:
            answer, citations = await answer_selected_text_query(
                query=query,
                selected_text=selected_text,
                top_k=3
            )

            print(f"Answer: {answer}")
            print(f"\nCitations ({len(citations)}):")
            for citation in citations:
                print(f"  - {citation.chunk_id} (score: {citation.relevance_score:.2f})")
                print(f"    {citation.text_preview[:100]}...")

        except Exception as e:
            print(f"Error: {e}")

    # Run test
    asyncio.run(test_selected_text())
