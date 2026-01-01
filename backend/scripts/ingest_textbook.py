"""
Textbook chapter ingestion script.

Reads Markdown chapters, chunks them, generates embeddings,
and uploads to Qdrant vector database.
"""

import sys
import os
from pathlib import Path
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.chunking import chunk_textbook_chapter, ChunkMetadata
from src.services.embeddings import get_embedding_service
from src.services.vector_store import get_vector_store
from src.config import get_settings, validate_configuration
from src.utils.logger import get_logger, PerformanceTimer
import argparse


logger = get_logger(__name__)


def read_chapter_file(file_path: Path) -> str:
    """
    Read chapter file content.

    Args:
        file_path: Path to chapter Markdown file

    Returns:
        str: File content

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Read chapter file: {file_path} ({len(content)} characters)")
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def process_chapter(
    file_path: Path,
    chapter_number: int = None
) -> List[dict]:
    """
    Process a single chapter: chunk and embed.

    Args:
        file_path: Path to chapter Markdown file
        chapter_number: Chapter number (auto-detected if None)

    Returns:
        List[dict]: Chunks with embeddings ready for upload
    """
    logger.info(f"Processing chapter: {file_path}")

    # Read file
    content = read_chapter_file(file_path)

    # Chunk the content
    logger.info("Chunking chapter...")
    with PerformanceTimer(logger, "chunking"):
        chunks = chunk_textbook_chapter(
            markdown_text=content,
            source_file=str(file_path),
            chapter=chapter_number
        )

    logger.info(f"Generated {len(chunks)} chunks")

    # Generate embeddings
    logger.info("Generating embeddings...")
    embedding_service = get_embedding_service()

    texts = [chunk.text for chunk in chunks]

    with PerformanceTimer(logger, "embedding_generation"):
        embeddings = embedding_service.embed_batch(
            texts,
            normalize=True,
            show_progress=True
        )

    # Combine chunks with embeddings
    chunk_dicts = []
    for chunk, embedding in zip(chunks, embeddings):
        chunk_dict = {
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "embedding": embedding,
            "chapter": chunk.chapter,
            "section": chunk.section,
            "subsection": chunk.subsection,
            "url_anchor": chunk.url_anchor,
            "token_count": chunk.token_count,
            "chunk_index": chunk.chunk_index,
            "source_file": chunk.source_file
        }
        chunk_dicts.append(chunk_dict)

    logger.info(f"Chapter processing complete: {len(chunk_dicts)} chunks with embeddings")
    return chunk_dicts


def upload_chunks(chunks: List[dict], collection_name: str = None):
    """
    Upload chunks to Qdrant.

    Args:
        chunks: List of chunk dictionaries with embeddings
        collection_name: Target collection (defaults to config value)
    """
    logger.info(f"Uploading {len(chunks)} chunks to Qdrant...")

    vector_store = get_vector_store()
    if collection_name:
        vector_store.collection_name = collection_name

    with PerformanceTimer(logger, "qdrant_upload"):
        vector_store.upsert_chunks(chunks, batch_size=100)

    logger.info("[OK] Upload complete")


def ingest_chapters(
    chapters_dir: Path,
    pattern: str = "*.md",
    collection_name: str = None
):
    """
    Ingest all chapters from a directory.

    Args:
        chapters_dir: Directory containing chapter Markdown files
        pattern: File pattern to match (default: *.md)
        collection_name: Target Qdrant collection
    """
    logger.info("=" * 60)
    logger.info("Textbook Ingestion Starting")
    logger.info("=" * 60)
    logger.info(f"Chapters Directory: {chapters_dir}")
    logger.info(f"File Pattern: {pattern}")
    logger.info("=" * 60)

    # Find chapter files
    chapter_files = sorted(chapters_dir.glob(pattern))

    if not chapter_files:
        logger.warning(f"No chapter files found matching '{pattern}' in {chapters_dir}")
        return

    logger.info(f"Found {len(chapter_files)} chapter files:")
    for file_path in chapter_files:
        logger.info(f"  - {file_path.name}")

    # Process each chapter
    all_chunks = []
    total_timer = PerformanceTimer(logger, "total_ingestion")
    total_timer.__enter__()

    for i, file_path in enumerate(chapter_files, 1):
        logger.info(f"\n[{i}/{len(chapter_files)}] Processing: {file_path.name}")

        try:
            chunks = process_chapter(file_path)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}", exc_info=True)
            continue

    total_timer.__exit__(None, None, None)

    # Upload all chunks
    if all_chunks:
        logger.info(f"\nTotal chunks generated: {len(all_chunks)}")
        upload_chunks(all_chunks, collection_name=collection_name)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Ingestion Complete")
        logger.info("=" * 60)
        logger.info(f"Chapters Processed: {len(chapter_files)}")
        logger.info(f"Total Chunks: {len(all_chunks)}")
        logger.info(f"Average Chunks/Chapter: {len(all_chunks) / len(chapter_files):.1f}")
        logger.info("=" * 60)

        # Verify upload
        vector_store = get_vector_store()
        if collection_name:
            vector_store.collection_name = collection_name

        total_in_db = vector_store.count_chunks()
        logger.info(f"Verification: {total_in_db} chunks in Qdrant collection")
    else:
        logger.warning("No chunks were generated")


def main():
    """Main entry point for ingestion script."""
    parser = argparse.ArgumentParser(
        description="Ingest textbook chapters into Qdrant vector database"
    )
    parser.add_argument(
        "--chapters-dir",
        type=str,
        required=False,
        help="Directory containing chapter Markdown files"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.md",
        help="File pattern to match (default: *.md)"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help="Qdrant collection name (defaults to config value)"
    )
    parser.add_argument(
        "--single-file",
        type=str,
        default=None,
        help="Process a single file instead of directory"
    )

    args = parser.parse_args()

    # Validate that either --chapters-dir or --single-file is provided
    if not args.single_file and not args.chapters_dir:
        parser.error("Either --chapters-dir or --single-file must be provided")

    # Validate configuration
    try:
        validate_configuration()
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        sys.exit(1)

    # Check Qdrant connection
    logger.info("Checking Qdrant connection...")
    vector_store = get_vector_store()
    if not vector_store.health_check():
        logger.error("Cannot connect to Qdrant - check configuration")
        sys.exit(1)

    logger.info("[OK] Qdrant connection successful")

    # Process single file or directory
    if args.single_file:
        file_path = Path(args.single_file)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            sys.exit(1)

        logger.info(f"Processing single file: {file_path}")
        try:
            chunks = process_chapter(file_path)
            upload_chunks(chunks, collection_name=args.collection)
            logger.info(f"[OK] Successfully ingested {len(chunks)} chunks from {file_path.name}")
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            sys.exit(1)

    else:
        chapters_dir = Path(args.chapters_dir)
        if not chapters_dir.exists():
            logger.error(f"Directory not found: {chapters_dir}")
            sys.exit(1)

        if not chapters_dir.is_dir():
            logger.error(f"Not a directory: {chapters_dir}")
            sys.exit(1)

        ingest_chapters(
            chapters_dir=chapters_dir,
            pattern=args.pattern,
            collection_name=args.collection
        )

    logger.info("Ingestion script completed")


if __name__ == "__main__":
    main()
