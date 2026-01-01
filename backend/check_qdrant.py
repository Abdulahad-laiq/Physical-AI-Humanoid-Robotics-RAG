"""Check Qdrant collection status."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.vector_store import get_vector_store
from src.config import get_settings

# Get Qdrant instance
vector_store = get_vector_store()

# Check health
print(f"Health check: {vector_store.health_check()}")

# Count chunks
try:
    count = vector_store.count_chunks()
    print(f"Total chunks in collection: {count}")
except Exception as e:
    print(f"Error counting chunks: {e}")

# Try a simple search
try:
    print("\nAttempting search...")
    from src.services.embeddings import embed_text
    query_embedding = embed_text("test", normalize=True)
    print(f"Query embedding generated: {len(query_embedding)} dims")

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=5,
        score_threshold=0.0
    )
    print(f"Search results: {len(results)} chunks found")
    if results:
        print(f"Top result score: {results[0].score}")
except Exception as e:
    print(f"Search error: {e}")
    import traceback
    traceback.print_exc()
