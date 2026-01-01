"""
Quick test to verify GEMINI_API_KEY is working.

Tests the API key by making a simple call to Gemini API.
"""

import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from openai import OpenAI
    from dotenv import load_dotenv

    # Load .env file
    env_path = backend_dir / ".env"
    load_dotenv(env_path)

    print("=" * 60)
    print("Testing Gemini API Key")
    print("=" * 60)
    print()

    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("✗ ERROR: GEMINI_API_KEY not found in .env file")
        sys.exit(1)

    print(f"✓ API Key found: ***{api_key[-8:]}")
    print()

    # Initialize OpenAI client with Gemini endpoint
    print("Initializing Gemini client...")
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    print("✓ Client initialized")
    print()

    # Make a test call
    print("Testing API with a simple query...")
    models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-2.0-flash"]

    for model in models_to_try:
        print(f"Trying model: {model}...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Say 'API key is working!' if you can read this."}
                ],
                max_tokens=50,
                temperature=0.3
            )
            break  # Success, exit loop
        except Exception as model_error:
            if "429" in str(model_error) or "quota" in str(model_error).lower():
                print(f"  Model {model}: Quota exceeded, trying next...")
                if model == models_to_try[-1]:
                    raise  # Re-raise if last model
                continue
            else:
                raise  # Re-raise non-quota errors

    try:

        answer = response.choices[0].message.content
        print(f"✓ API Response: {answer}")
        print()

        # Verify response
        if "working" in answer.lower() or "api" in answer.lower():
            print("=" * 60)
            print("✓ SUCCESS: Gemini API key is working correctly!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("⚠ WARNING: Got response but content unexpected")
            print(f"   Response: {answer}")
            sys.exit(0)

    except Exception as e:
        print(f"✗ ERROR: API call failed")
        print(f"   Error: {str(e)}")
        print()

        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("   Cause: Invalid or expired API key")
            print("   Solution: Generate a new API key at:")
            print("   https://aistudio.google.com/apikey")
        elif "403" in str(e) or "forbidden" in str(e).lower():
            print("   Cause: API key doesn't have required permissions")
        elif "429" in str(e) or "quota" in str(e).lower():
            print("   Cause: Rate limit or quota exceeded")
        else:
            print("   Cause: Network or configuration issue")

        print()
        print("=" * 60)
        print("✗ FAILED: Gemini API key verification failed")
        print("=" * 60)
        sys.exit(1)

except ImportError as e:
    print(f"✗ ERROR: Missing required package: {e}")
    print()
    print("Install dependencies with:")
    print("  pip install openai python-dotenv")
    sys.exit(1)
