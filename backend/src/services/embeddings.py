"""
Embedding generation service using Sentence-Transformers.

Provides text embedding generation using the all-MiniLM-L6-v2 model
(384 dimensions). Supports batch processing and caching for performance.
"""

from typing import List, Union, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
BATCH_SIZE = 32  # Process embeddings in batches for efficiency
NORMALIZE_EMBEDDINGS = True  # Normalize for cosine similarity


# ============================================================================
# Embedding Service
# ============================================================================

class EmbeddingService:
    """
    Service for generating text embeddings using Sentence-Transformers.

    Uses all-MiniLM-L6-v2 model (384 dimensions) with local inference.
    Supports batch processing and optional caching.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str = None,
        cache_enabled: bool = True
    ):
        """
        Initialize embedding service.

        Args:
            model_name: Sentence-Transformers model name
            device: Device to run model on ("cpu", "cuda", or None for auto-detect)
            cache_enabled: Enable LRU caching for repeated embeddings
        """
        self.model_name = model_name
        self.cache_enabled = cache_enabled

        logger.info(f"Loading embedding model: {model_name}")

        # Load model
        self.model = SentenceTransformer(model_name, device=device)

        # Verify embedding dimension
        test_embedding = self.model.encode("test", convert_to_numpy=True)
        actual_dimension = len(test_embedding)

        if actual_dimension != EMBEDDING_DIMENSION:
            logger.warning(
                f"Expected {EMBEDDING_DIMENSION} dimensions, got {actual_dimension}. "
                f"Update EMBEDDING_DIMENSION constant."
            )

        logger.info(
            f"Embedding model loaded successfully "
            f"(dimension={actual_dimension}, device={self.model.device})"
        )

    def embed(
        self,
        texts: Union[str, List[str]],
        normalize: bool = NORMALIZE_EMBEDDINGS,
        show_progress: bool = False
    ) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text(s).

        Args:
            texts: Single text string or list of texts
            normalize: Normalize embeddings to unit length (for cosine similarity)
            show_progress: Show progress bar for batch processing

        Returns:
            Embedding vector(s) as list(s) of floats
        """
        # Handle single text vs. batch
        is_single = isinstance(texts, str)
        if is_single:
            texts = [texts]

        # Check cache for single embedding
        if is_single and self.cache_enabled:
            cached = self._get_cached_embedding(texts[0])
            if cached is not None:
                return cached

        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            batch_size=BATCH_SIZE
        )

        # Convert to list format
        if is_single:
            embedding = embeddings[0].tolist()
            if self.cache_enabled:
                self._cache_embedding(texts[0], embedding)
            return embedding
        else:
            return [emb.tolist() for emb in embeddings]

    def embed_batch(
        self,
        texts: List[str],
        normalize: bool = NORMALIZE_EMBEDDINGS,
        show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Optimized for large batches with progress tracking.

        Args:
            texts: List of text strings
            normalize: Normalize embeddings to unit length
            show_progress: Show progress bar

        Returns:
            List of embedding vectors
        """
        logger.info(f"Generating embeddings for {len(texts)} texts")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            batch_size=BATCH_SIZE
        )

        logger.info(f"Generated {len(embeddings)} embeddings")
        return [emb.tolist() for emb in embeddings]

    def similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            float: Cosine similarity score (-1 to 1, higher = more similar)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)

    def _get_cached_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get cached embedding for text.

        Args:
            text: Input text

        Returns:
            Cached embedding or None if not found
        """
        if not self.cache_enabled:
            return None

        cache_key = self._hash_text(text)
        return _embedding_cache.get(cache_key)

    def _cache_embedding(self, text: str, embedding: List[float]):
        """
        Cache embedding for text.

        Args:
            text: Input text
            embedding: Generated embedding
        """
        if not self.cache_enabled:
            return

        cache_key = self._hash_text(text)
        _embedding_cache[cache_key] = embedding

    @staticmethod
    def _hash_text(text: str) -> str:
        """
        Generate hash for text (for cache key).

        Args:
            text: Input text

        Returns:
            str: MD5 hash of text
        """
        return hashlib.md5(text.encode()).hexdigest()


# ============================================================================
# Global Service Instance
# ============================================================================

# Global embedding service instance (initialized on first use)
_embedding_service: Optional[EmbeddingService] = None

# Simple in-memory cache for embeddings (LRU with max 1000 entries)
_embedding_cache = {}
_CACHE_MAX_SIZE = 1000


def get_embedding_service(
    model_name: str = MODEL_NAME,
    device: str = None,
    force_reload: bool = False
) -> EmbeddingService:
    """
    Get or create the global embedding service instance.

    Args:
        model_name: Sentence-Transformers model name
        device: Device to run model on
        force_reload: Force reload of the model

    Returns:
        EmbeddingService: Global embedding service singleton
    """
    global _embedding_service

    if _embedding_service is None or force_reload:
        _embedding_service = EmbeddingService(
            model_name=model_name,
            device=device,
            cache_enabled=True
        )

    return _embedding_service


# ============================================================================
# Convenience Functions
# ============================================================================

def embed_text(text: str, normalize: bool = NORMALIZE_EMBEDDINGS) -> List[float]:
    """
    Generate embedding for a single text.

    Convenience function that uses the global embedding service.

    Args:
        text: Input text
        normalize: Normalize embedding to unit length

    Returns:
        List[float]: 384-dimensional embedding vector
    """
    service = get_embedding_service()
    return service.embed(text, normalize=normalize)


def embed_texts(
    texts: List[str],
    normalize: bool = NORMALIZE_EMBEDDINGS,
    show_progress: bool = True
) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.

    Convenience function that uses the global embedding service.

    Args:
        texts: List of input texts
        normalize: Normalize embeddings to unit length
        show_progress: Show progress bar

    Returns:
        List[List[float]]: List of 384-dimensional embedding vectors
    """
    service = get_embedding_service()
    return service.embed_batch(texts, normalize=normalize, show_progress=show_progress)


def calculate_similarity(
    embedding1: List[float],
    embedding2: List[float]
) -> float:
    """
    Calculate cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        float: Cosine similarity score (-1 to 1)
    """
    service = get_embedding_service()
    return service.similarity(embedding1, embedding2)


# ============================================================================
# Batch Processing Utilities
# ============================================================================

def embed_chunks_with_metadata(
    chunks: List[dict],
    text_field: str = "text",
    show_progress: bool = True
) -> List[dict]:
    """
    Embed chunks and add embedding field to each chunk.

    Args:
        chunks: List of chunk dictionaries
        text_field: Field name containing the text to embed
        show_progress: Show progress bar

    Returns:
        List[dict]: Chunks with added "embedding" field
    """
    # Extract texts
    texts = [chunk[text_field] for chunk in chunks]

    # Generate embeddings
    embeddings = embed_texts(texts, show_progress=show_progress)

    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    logger.info(f"Embedded {len(chunks)} chunks")
    return chunks


# ============================================================================
# Performance Testing
# ============================================================================

def benchmark_embedding_speed(num_texts: int = 100, text_length: int = 512):
    """
    Benchmark embedding generation speed.

    Args:
        num_texts: Number of texts to embed
        text_length: Approximate length of each text (in characters)
    """
    import time

    # Generate sample texts
    sample_text = "This is a sample sentence for embedding. " * (text_length // 40)
    texts = [sample_text] * num_texts

    # Benchmark
    service = get_embedding_service()

    start_time = time.time()
    embeddings = service.embed_batch(texts, show_progress=True)
    elapsed_time = time.time() - start_time

    # Calculate metrics
    texts_per_second = num_texts / elapsed_time
    ms_per_text = (elapsed_time / num_texts) * 1000

    print(f"\nEmbedding Benchmark Results:")
    print(f"  Texts: {num_texts}")
    print(f"  Total time: {elapsed_time:.2f}s")
    print(f"  Throughput: {texts_per_second:.2f} texts/second")
    print(f"  Latency: {ms_per_text:.2f} ms/text")
    print(f"  Embedding dimension: {len(embeddings[0])}")


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of embedding service.
    """
    # Initialize service
    service = get_embedding_service()

    # Single text embedding
    text = "What is inverse kinematics?"
    embedding = embed_text(text)
    print(f"Embedded text: '{text}'")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print()

    # Batch embedding
    texts = [
        "Inverse kinematics solves for joint angles.",
        "Forward kinematics computes end-effector position.",
        "The Jacobian maps joint velocities to Cartesian velocities."
    ]
    embeddings = embed_texts(texts, show_progress=False)
    print(f"Embedded {len(embeddings)} texts")
    print()

    # Similarity calculation
    sim_score = calculate_similarity(embeddings[0], embeddings[1])
    print(f"Similarity between first two texts: {sim_score:.4f}")
    print()

    # Benchmark (optional)
    print("Running benchmark...")
    benchmark_embedding_speed(num_texts=50, text_length=256)
