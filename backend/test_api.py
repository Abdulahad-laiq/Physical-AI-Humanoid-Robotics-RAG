"""
Simple API test script for RAG Chatbot backend.

Tests all Phase 3 endpoints to verify functionality.
"""

import httpx
import asyncio
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0


def print_header(title):
    """Print formatted test section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_success(message):
    """Print success message in green."""
    print(f"✓ {message}")


def print_error(message):
    """Print error message in red."""
    print(f"✗ {message}")


def print_info(message):
    """Print info message."""
    print(f"  {message}")


async def test_root_endpoint():
    """Test GET / endpoint."""
    print_header("Test 1: Root Endpoint")

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/")

            if response.status_code == 200:
                data = response.json()
                print_success(f"Root endpoint responded: {response.status_code}")
                print_info(f"API Name: {data.get('name')}")
                print_info(f"Version: {data.get('version')}")
                return True
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Failed to connect: {e}")
        return False


async def test_health_endpoint():
    """Test GET /health endpoint."""
    print_header("Test 2: Health Check Endpoint")

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/health")

            if response.status_code == 200:
                data = response.json()
                print_success(f"Health endpoint responded: {response.status_code}")
                print_info(f"Status: {data.get('status')}")
                print_info(f"Qdrant: {'✓ Connected' if data.get('qdrant_connected') else '✗ Disconnected'}")
                print_info(f"Neon: {'✓ Connected' if data.get('neon_connected') else '✗ Disconnected'}")

                if data.get('status') == 'healthy':
                    print_success("All services healthy")
                    return True
                else:
                    print_error("Service degraded - check connections")
                    return False
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Failed to connect: {e}")
        return False


async def test_chat_endpoint_basic():
    """Test POST /api/v1/chat with basic query."""
    print_header("Test 3: Chat Endpoint - Basic Query")

    payload = {
        "query": "What is inverse kinematics?",
        "debug": False
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"Chat endpoint responded: {response.status_code}")
                print_info(f"Query ID: {data.get('query_id')}")
                print_info(f"Response time: {data.get('generation_time_ms')}ms")
                print_info(f"Citations: {len(data.get('citations', []))}")
                print_info(f"Answer preview: {data.get('answer', '')[:100]}...")

                if data.get('generation_time_ms', 0) < 10000:  # < 10 seconds
                    print_success("Response time acceptable")
                else:
                    print_error("Response time too slow (>10s)")

                return True
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                print_info(f"Response: {response.text}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_chat_endpoint_debug():
    """Test POST /api/v1/chat with debug mode."""
    print_header("Test 4: Chat Endpoint - Debug Mode")

    payload = {
        "query": "Explain forward kinematics",
        "debug": True
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"Debug mode responded: {response.status_code}")

                if data.get('debug_metadata'):
                    debug_info = data['debug_metadata']
                    retrieval = debug_info.get('retrieval', {})
                    print_info(f"Chunks retrieved: {retrieval.get('chunks_retrieved', 0)}")
                    print_info(f"Top scores: {retrieval.get('top_scores', [])}")
                    print_success("Debug metadata present")
                else:
                    print_error("Debug metadata missing")

                return True
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_chat_endpoint_session():
    """Test POST /api/v1/chat with session ID."""
    print_header("Test 5: Chat Endpoint - Session Tracking")

    payload = {
        "query": "What is a Jacobian matrix?",
        "session_id": "test-session-123"
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"Session tracking responded: {response.status_code}")
                print_info(f"Query ID: {data.get('query_id')}")
                print_success("Session ID accepted (check database for hashed session)")
                return True
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_error_empty_query():
    """Test error handling for empty query."""
    print_header("Test 6: Error Handling - Empty Query")

    payload = {
        "query": ""
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat",
                json=payload
            )

            if response.status_code == 400:
                print_success("Empty query rejected with 400")
                print_info(f"Error: {response.json().get('detail')}")
                return True
            else:
                print_error(f"Expected 400, got {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_error_long_query():
    """Test error handling for query too long."""
    print_header("Test 7: Error Handling - Query Too Long")

    payload = {
        "query": "a" * 1001  # Exceeds 1000 character limit
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat",
                json=payload
            )

            if response.status_code == 400:
                print_success("Long query rejected with 400")
                print_info(f"Error: {response.json().get('detail')}")
                return True
            else:
                print_error(f"Expected 400, got {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_rate_limiting():
    """Test rate limiting (100 req/min)."""
    print_header("Test 8: Rate Limiting")

    print_info("Sending 105 requests rapidly...")

    payload = {"query": "test"}
    rate_limited = False

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Send 105 requests
            for i in range(105):
                response = await client.post(
                    f"{BASE_URL}/api/v1/chat",
                    json=payload
                )

                if response.status_code == 429:
                    rate_limited = True
                    print_success(f"Rate limit triggered after {i + 1} requests")
                    print_info(f"Error: {response.json().get('message')}")
                    break

            if not rate_limited:
                print_error("Rate limiting not triggered (expected after 100 requests)")
                return False

            return True

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_selected_text_basic():
    """Test POST /api/v1/chat/selected with basic query."""
    print_header("Test 9: Selected-Text - Basic Query")

    payload = {
        "query": "What does the Jacobian matrix do?",
        "selected_text": "The Jacobian matrix J relates joint velocities to end-effector velocities: v = J(q) * q_dot, where v is the end-effector velocity and q_dot is the joint velocity vector."
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat/selected",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"Selected-text endpoint responded: {response.status_code}")
                print_info(f"Query ID: {data.get('query_id')}")
                print_info(f"Response time: {data.get('generation_time_ms')}ms")
                print_info(f"Citations: {len(data.get('citations', []))}")

                # Verify isolation - all citations should be from selected text
                citations = data.get('citations', [])
                all_isolated = all(c.get('chunk_id', '').startswith('selected-') for c in citations)

                if all_isolated:
                    print_success("All citations from selected text (isolation verified)")
                else:
                    print_error("Found citations from global database (isolation broken!)")
                    return False

                return True
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                print_info(f"Response: {response.text}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_selected_text_isolation():
    """Test isolation - query about unrelated topic should fail."""
    print_header("Test 10: Selected-Text - Isolation Verification")

    payload = {
        "query": "What is forward kinematics?",  # Unrelated to selected text
        "selected_text": "Inverse kinematics (IK) determines joint angles from end-effector pose. It may have multiple solutions."
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat/selected",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '').lower()

                # Should say "not found in selected text"
                if 'not found' in answer and 'selected' in answer:
                    print_success("Correctly returned 'not found' for unrelated query")
                    print_info(f"Answer: {answer[:100]}...")
                    return True
                else:
                    print_error("Did not return 'not found' - may have leaked global data")
                    print_info(f"Answer: {answer}")
                    return False
            else:
                print_error(f"Unexpected status code: {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def test_selected_text_too_short():
    """Test error handling for text too short."""
    print_header("Test 11: Selected-Text - Text Too Short")

    payload = {
        "query": "Explain this",
        "selected_text": "Too short"  # Less than 10 characters
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/chat/selected",
                json=payload
            )

            if response.status_code == 400:
                print_success("Short text rejected with 400")
                print_info(f"Error: {response.json().get('detail')}")
                return True
            else:
                print_error(f"Expected 400, got {response.status_code}")
                return False

    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


async def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 70)
    print("  RAG Chatbot Backend - API Test Suite")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)

    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Chat - Basic Query", test_chat_endpoint_basic),
        ("Chat - Debug Mode", test_chat_endpoint_debug),
        ("Chat - Session Tracking", test_chat_endpoint_session),
        ("Error - Empty Query", test_error_empty_query),
        ("Error - Long Query", test_error_long_query),
        ("Rate Limiting", test_rate_limiting),
        ("Selected-Text - Basic", test_selected_text_basic),
        ("Selected-Text - Isolation", test_selected_text_isolation),
        ("Selected-Text - Too Short", test_selected_text_too_short),
    ]

    results = []

    for name, test_func in tests:
        result = await test_func()
        results.append((name, result))
        await asyncio.sleep(0.5)  # Small delay between tests

    # Print summary
    print_header("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print("\n" + "-" * 70)
    print(f"  Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("-" * 70)

    if passed == total:
        print("\n✓ All tests passed! Phase 3 backend is working correctly.")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Review errors above.")

    return passed == total


if __name__ == "__main__":
    """Run all tests."""
    print("\nMake sure the API server is running:")
    print("  uvicorn src.main:app --reload --port 8000\n")

    input("Press Enter to start tests (or Ctrl+C to cancel)...")

    success = asyncio.run(run_all_tests())

    exit(0 if success else 1)
