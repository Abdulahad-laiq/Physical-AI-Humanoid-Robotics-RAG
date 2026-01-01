"""
Services package.

Contains core business logic services for the RAG chatbot.
"""

from .chunking import chunk_textbook_chapter, ChunkMetadata
from .embeddings import embed_text, embed_texts, get_embedding_service
from .vector_store import get_vector_store, SearchResult
from .agent import answer_query, get_agent_service
from .selected_text import answer_selected_text_query, get_selected_text_service

__all__ = [
    # Chunking
    "chunk_textbook_chapter",
    "ChunkMetadata",
    # Embeddings
    "embed_text",
    "embed_texts",
    "get_embedding_service",
    # Vector Store
    "get_vector_store",
    "SearchResult",
    # Agent
    "answer_query",
    "get_agent_service",
    # Selected Text
    "answer_selected_text_query",
    "get_selected_text_service"
]
