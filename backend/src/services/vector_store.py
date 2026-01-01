"""
Qdrant vector store service for chunk storage and retrieval.

Provides a high-level interface to Qdrant Cloud for storing and querying
text chunk embeddings with metadata filtering.
"""

from typing import List, Dict, Optional, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    Range,
    SearchParams
)
import os
import logging
from dataclasses import dataclass
from src.config import get_settings

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

EMBEDDING_DIMENSION = 384
DEFAULT_COLLECTION_NAME = "textbook_chunks_v1"
DISTANCE_METRIC = Distance.COSINE


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class SearchResult:
    """
    Single search result from vector store.

    Attributes:
        chunk_id: Unique chunk identifier
        score: Relevance score (cosine similarity, 0-1)
        text: Chunk text content
        chapter: Chapter number
        section: Section identifier
        subsection: Optional subsection identifier
        url_anchor: URL anchor for citation linking
        metadata: Additional metadata fields
    """
    chunk_id: str
    score: float
    text: str
    chapter: int
    section: str
    subsection: Optional[str]
    url_anchor: str
    metadata: Dict[str, Any]


# ============================================================================
# Vector Store Service
# ============================================================================

class VectorStoreService:
    """
    Service for interacting with Qdrant vector database.

    Provides methods for creating collections, upserting chunks,
    and querying with metadata filters.
    """

    def __init__(
        self,
        url: str = None,
        api_key: str = None,
        collection_name: str = None
    ):
        """
        Initialize Qdrant vector store service.

        Args:
            url: Qdrant server URL (defaults to config settings)
            api_key: Qdrant API key (defaults to config settings)
            collection_name: Collection name (defaults to config settings)

        Raises:
            ValueError: If URL or API key not provided and not in config
        """
        # Load settings from config if not provided
        settings = get_settings()

        self.url = url or settings.qdrant_url
        self.api_key = api_key or settings.qdrant_api_key
        self.collection_name = collection_name or settings.qdrant_collection_name

        if not self.url or not self.api_key:
            raise ValueError(
                "Qdrant URL and API key required. Set QDRANT_URL and QDRANT_API_KEY "
                "environment variables or pass to constructor."
            )

        # Initialize client
        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
            timeout=settings.qdrant_timeout
        )

        logger.info(f"Qdrant client initialized (collection: {self.collection_name})")

    def create_collection(
        self,
        collection_name: str = None,
        dimension: int = EMBEDDING_DIMENSION,
        distance: Distance = DISTANCE_METRIC,
        recreate: bool = False
    ):
        """
        Create a new collection in Qdrant.

        Args:
            collection_name: Collection name (defaults to instance collection_name)
            dimension: Embedding vector dimension
            distance: Distance metric (COSINE, EUCLID, or DOT)
            recreate: If True, delete existing collection and recreate

        Raises:
            Exception: If collection creation fails
        """
        collection_name = collection_name or self.collection_name

        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(c.name == collection_name for c in collections)

            if exists:
                if recreate:
                    logger.warning(f"Deleting existing collection: {collection_name}")
                    self.client.delete_collection(collection_name)
                else:
                    logger.info(f"Collection '{collection_name}' already exists")
                    return

            # Create collection
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=dimension,
                    distance=distance
                )
            )

            logger.info(
                f"Created collection '{collection_name}' "
                f"(dimension={dimension}, distance={distance.value})"
            )

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    def upsert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        collection_name: str = None,
        batch_size: int = 100
    ):
        """
        Upsert (insert or update) chunks into the vector store.

        Args:
            chunks: List of chunk dictionaries with fields:
                    - chunk_id (str): Unique identifier
                    - text (str): Text content
                    - embedding (List[float]): 384-dim vector
                    - chapter (int): Chapter number
                    - section (str): Section identifier
                    - subsection (str, optional): Subsection identifier
                    - url_anchor (str): URL anchor
                    - Additional metadata fields
            collection_name: Target collection (defaults to instance collection_name)
            batch_size: Number of chunks to upload per batch

        Raises:
            ValueError: If chunks missing required fields
        """
        collection_name = collection_name or self.collection_name

        if not chunks:
            logger.warning("No chunks to upsert")
            return

        # Validate required fields
        required_fields = ["chunk_id", "text", "embedding", "chapter", "section", "url_anchor"]
        for chunk in chunks:
            missing = [f for f in required_fields if f not in chunk]
            if missing:
                raise ValueError(f"Chunk missing required fields: {missing}")

        # Convert chunks to Qdrant points
        points = []
        for chunk in chunks:
            point = PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload={
                    "text": chunk["text"],
                    "chapter": chunk["chapter"],
                    "section": chunk["section"],
                    "subsection": chunk.get("subsection"),
                    "url_anchor": chunk["url_anchor"],
                    "token_count": chunk.get("token_count", 0),
                    "chunk_index": chunk.get("chunk_index", 0),
                    "source_file": chunk.get("source_file", ""),
                    # Include any additional metadata
                    **{k: v for k, v in chunk.items() if k not in required_fields}
                }
            )
            points.append(point)

        # Upload in batches
        total_chunks = len(points)
        for i in range(0, total_chunks, batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=collection_name,
                points=batch
            )
            logger.info(f"Uploaded batch {i // batch_size + 1}/{(total_chunks + batch_size - 1) // batch_size}")

        logger.info(f"Upserted {total_chunks} chunks to collection '{collection_name}'")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        chapter_filter: Optional[int] = None,
        section_filter: Optional[str] = None,
        score_threshold: Optional[float] = None,
        collection_name: str = None
    ) -> List[SearchResult]:
        """
        Search for similar chunks in the vector store.

        Args:
            query_embedding: Query embedding vector (384 dimensions)
            top_k: Number of results to return
            chapter_filter: Optional filter by chapter number
            section_filter: Optional filter by section identifier
            score_threshold: Minimum similarity score (0-1)
            collection_name: Collection to search (defaults to instance collection_name)

        Returns:
            List[SearchResult]: Top-k search results ordered by relevance
        """
        collection_name = collection_name or self.collection_name

        # Build metadata filter
        filter_conditions = []

        if chapter_filter is not None:
            filter_conditions.append(
                FieldCondition(
                    key="chapter",
                    match=MatchValue(value=chapter_filter)
                )
            )

        if section_filter is not None:
            filter_conditions.append(
                FieldCondition(
                    key="section",
                    match=MatchValue(value=section_filter)
                )
            )

        query_filter = Filter(must=filter_conditions) if filter_conditions else None

        # Execute search
        search_results = self.client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=query_filter,
            score_threshold=score_threshold,
            with_payload=True
        )

        # Convert to SearchResult objects
        results = []
        for hit in search_results:
            result = SearchResult(
                chunk_id=str(hit.id),
                score=hit.score,
                text=hit.payload["text"],
                chapter=hit.payload["chapter"],
                section=hit.payload["section"],
                subsection=hit.payload.get("subsection"),
                url_anchor=hit.payload["url_anchor"],
                metadata={
                    k: v for k, v in hit.payload.items()
                    if k not in ["text", "chapter", "section", "subsection", "url_anchor"]
                }
            )
            results.append(result)

        logger.info(
            f"Search returned {len(results)} results "
            f"(top_k={top_k}, filters={filter_conditions})"
        )

        return results

    def get_chunk(
        self,
        chunk_id: str,
        collection_name: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by ID.

        Args:
            chunk_id: Chunk identifier
            collection_name: Collection to search (defaults to instance collection_name)

        Returns:
            Dict with chunk data or None if not found
        """
        collection_name = collection_name or self.collection_name

        try:
            result = self.client.retrieve(
                collection_name=collection_name,
                ids=[chunk_id],
                with_payload=True,
                with_vectors=False
            )

            if result:
                point = result[0]
                return {
                    "chunk_id": str(point.id),
                    **point.payload
                }

            return None

        except Exception as e:
            logger.error(f"Error retrieving chunk {chunk_id}: {e}")
            return None

    def delete_chunks(
        self,
        chunk_ids: List[str],
        collection_name: str = None
    ):
        """
        Delete chunks by IDs.

        Args:
            chunk_ids: List of chunk IDs to delete
            collection_name: Collection name (defaults to instance collection_name)
        """
        collection_name = collection_name or self.collection_name

        self.client.delete(
            collection_name=collection_name,
            points_selector=chunk_ids
        )

        logger.info(f"Deleted {len(chunk_ids)} chunks from '{collection_name}'")

    def count_chunks(self, collection_name: str = None) -> int:
        """
        Count total chunks in collection.

        Args:
            collection_name: Collection name (defaults to instance collection_name)

        Returns:
            int: Total number of chunks
        """
        collection_name = collection_name or self.collection_name

        collection_info = self.client.get_collection(collection_name)
        return collection_info.points_count

    def health_check(self) -> bool:
        """
        Check if Qdrant is accessible.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False


# ============================================================================
# Global Service Instance
# ============================================================================

_vector_store: Optional[VectorStoreService] = None


def get_vector_store(
    url: str = None,
    api_key: str = None,
    collection_name: str = None
) -> VectorStoreService:
    """
    Get or create the global vector store service instance.

    Args:
        url: Qdrant URL (optional, defaults to env var)
        api_key: Qdrant API key (optional, defaults to env var)
        collection_name: Collection name (optional, defaults to env var)

    Returns:
        VectorStoreService: Global vector store singleton
    """
    global _vector_store

    if _vector_store is None:
        _vector_store = VectorStoreService(
            url=url,
            api_key=api_key,
            collection_name=collection_name
        )

    return _vector_store


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of vector store service.
    """
    # Initialize service
    vector_store = get_vector_store()

    # Health check
    is_healthy = vector_store.health_check()
    print(f"Qdrant health check: {'✓ Healthy' if is_healthy else '✗ Failed'}")

    # Create collection (if needed)
    try:
        vector_store.create_collection(recreate=False)
        print(f"Collection '{vector_store.collection_name}' ready")
    except Exception as e:
        print(f"Error: {e}")

    # Example: Upsert sample chunks
    sample_chunks = [
        {
            "chunk_id": "ch3-s3.2-001",
            "text": "Inverse kinematics solves for joint angles...",
            "embedding": [0.1] * EMBEDDING_DIMENSION,  # Dummy embedding
            "chapter": 3,
            "section": "3.2",
            "subsection": "3.2.1",
            "url_anchor": "#inverse-kinematics",
            "token_count": 150,
            "chunk_index": 1,
            "source_file": "chapter-3.md"
        }
    ]

    try:
        vector_store.upsert_chunks(sample_chunks)
        print(f"Upserted {len(sample_chunks)} sample chunks")
    except Exception as e:
        print(f"Error upserting: {e}")

    # Example: Search
    query_embedding = [0.1] * EMBEDDING_DIMENSION  # Dummy query
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=5,
        chapter_filter=3
    )

    print(f"\nSearch results ({len(results)}):")
    for result in results:
        print(f"  - {result.chunk_id} (score: {result.score:.4f})")
        print(f"    Chapter {result.chapter}, Section {result.section}")
        print(f"    Text: {result.text[:60]}...")

    # Count chunks
    total = vector_store.count_chunks()
    print(f"\nTotal chunks in collection: {total}")
