"""Verify Qdrant chunk count using direct API call."""
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials
url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION_NAME")

# Initialize client
client = QdrantClient(url=url, api_key=api_key)

# Try to get collection info
try:
    # Use scroll to count points (more reliable)
    count = 0
    offset = None
    while True:
        result = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=False,
            with_vectors=False
        )
        records, offset = result
        count += len(records)
        if offset is None:
            break

    print(f"[OK] Total chunks in Qdrant: {count}")

    # Breakdown by content
    print("\nIngestion Summary:")
    print("  - intro.md + glossary.md: 21 chunks (previous)")
    print("  - ch01 Introduction: 19 chunks")
    print("  - ch02 Robot Fundamentals: 29 chunks")
    print("  - ch03 Kinematics: 21 chunks")
    print("  - ch04 Dynamics: 34 chunks")
    print("  - bibliography.md: 18 chunks")
    print(f"  Total Expected: 142 chunks")
    print(f"  Total Actual: {count} chunks")

    if count == 142:
        print("\n[OK] All chunks successfully ingested!")
    else:
        print(f"\n[WARNING] Chunk count mismatch: expected 142, got {count}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
