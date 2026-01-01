"""Detailed API test with error information."""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test chat endpoint with detailed error info
print("Testing chat endpoint...")
payload = {"query": "What is this textbook about?"}
response = requests.post(
    f"{BASE_URL}/api/v1/chat",
    json=payload,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
