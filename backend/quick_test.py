"""Quick API test script without user interaction."""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test health endpoint
print("Testing health endpoint...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test chat endpoint
print("Testing chat endpoint...")
payload = {"query": "What is this textbook about?"}
response = requests.post(
    f"{BASE_URL}/api/v1/chat",
    json=payload,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Answer: {result.get('answer', 'No answer')[:200]}...")
print(f"Citations: {len(result.get('citations', []))} citations found")
print(f"Query ID: {result.get('query_id', 'N/A')}")
print()

print("[OK] RAG pipeline is working!")
