"""
Qdrant collection initialization script.

Creates the Qdrant collection for textbook chunks with proper configuration
(384 dimensions, cosine distance).
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.vector_store import get_vector_store, EMBEDDING_DIMENSION, DISTANCE_METRIC
from src.config import get_settings, validate_configuration, display_configuration
from src.utils.logger import get_logger
import argparse


logger = get_logger(__name__)


def setup_qdrant_collection(
    collection_name: str = None,
    recreate: bool = False,
    dimension: int = EMBEDDING_DIMENSION
):
    """
    Set up Qdrant collection for textbook chunks.

    Args:
        collection_name: Collection name (defaults to config value)
        recreate: If True, delete existing collection and recreate
        dimension: Embedding vector dimension

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Starting Qdrant collection setup")

        # Get vector store service
        vector_store = get_vector_store()

        if collection_name:
            vector_store.collection_name = collection_name

        logger.info(f"Target collection: {vector_store.collection_name}")

        # Check health
        logger.info("Checking Qdrant connection...")
        if not vector_store.health_check():
            logger.error("Qdrant health check failed - cannot connect to server")
            return False

        logger.info("[OK] Qdrant connection successful")

        # Create collection
        logger.info(f"Creating collection (dimension={dimension}, distance={DISTANCE_METRIC.value})")

        vector_store.create_collection(
            collection_name=vector_store.collection_name,
            dimension=dimension,
            distance=DISTANCE_METRIC,
            recreate=recreate
        )

        logger.info("[OK] Collection created successfully")

        # Verify collection
        count = vector_store.count_chunks()
        logger.info(f"Collection verification: {count} chunks (expected 0 for new collection)")

        logger.info("=" * 60)
        logger.info("Qdrant Setup Complete")
        logger.info("=" * 60)
        logger.info(f"Collection Name: {vector_store.collection_name}")
        logger.info(f"Embedding Dimension: {dimension}")
        logger.info(f"Distance Metric: {DISTANCE_METRIC.value}")
        logger.info(f"Current Chunk Count: {count}")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"Error setting up Qdrant collection: {e}", exc_info=True)
        return False


def main():
    """Main entry point for Qdrant setup script."""
    parser = argparse.ArgumentParser(
        description="Initialize Qdrant collection for RAG chatbot"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Collection name (defaults to QDRANT_COLLECTION_NAME from .env)"
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete existing collection and recreate (WARNING: deletes all data)"
    )
    parser.add_argument(
        "--dimension",
        type=int,
        default=EMBEDDING_DIMENSION,
        help=f"Embedding dimension (default: {EMBEDDING_DIMENSION})"
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Display configuration before setup"
    )

    args = parser.parse_args()

    # Display configuration if requested
    if args.show_config:
        display_configuration()

    # Validate configuration
    try:
        validate_configuration()
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        sys.exit(1)

    # Warn about recreate
    if args.recreate:
        logger.warning("=" * 60)
        logger.warning("WARNING: --recreate flag set")
        logger.warning("This will DELETE all existing data in the collection!")
        logger.warning("=" * 60)

        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Setup cancelled by user")
            sys.exit(0)

    # Run setup
    success = setup_qdrant_collection(
        collection_name=args.collection,
        recreate=args.recreate,
        dimension=args.dimension
    )

    if success:
        logger.info("Setup completed successfully")
        sys.exit(0)
    else:
        logger.error("Setup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
