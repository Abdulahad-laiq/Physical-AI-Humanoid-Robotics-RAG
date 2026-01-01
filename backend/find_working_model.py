"""
Find a working Gemini model with available quota.

Tests multiple Gemini models to find one that works.
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

from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
env_path = backend_dir / ".env"
load_dotenv(env_path)

print("=" * 60)
print("Finding Available Gemini Model")
print("=" * 60)
print()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("✗ ERROR: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

print(f"✓ API Key found: ***{api_key[-8:]}")
print()

# Initialize client
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Models to test (ordered by preference)
models_to_test = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash-exp",
    "gemini-exp-1206",
    "gemini-2.0-flash",
]

print("Testing models...")
print("-" * 60)

working_model = None

for model in models_to_test:
    print(f"\n[{model}]")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Reply with OK"}
            ],
            max_tokens=10,
            temperature=0.3
        )

        answer = response.choices[0].message.content
        print(f"  ✓ SUCCESS: {answer}")
        print(f"  ✓ This model is working!")
        working_model = model
        break

    except Exception as e:
        error_str = str(e)

        if "404" in error_str or "not found" in error_str.lower():
            print(f"  ✗ Model not available")
        elif "429" in error_str or "quota" in error_str.lower():
            print(f"  ✗ Quota exceeded")
        elif "401" in error_str or "unauthorized" in error_str.lower():
            print(f"  ✗ Authentication failed")
        else:
            print(f"  ✗ Error: {error_str[:100]}")

print()
print("=" * 60)

if working_model:
    print(f"✓ FOUND WORKING MODEL: {working_model}")
    print("=" * 60)
    print()
    print("Update your backend/.env file:")
    print(f"  GEMINI_MODEL={working_model}")
    print()
    sys.exit(0)
else:
    print("✗ NO WORKING MODEL FOUND")
    print("=" * 60)
    print()
    print("Possible causes:")
    print("  1. All models have exceeded quota")
    print("  2. API key is invalid or expired")
    print("  3. Wait a few minutes and retry")
    print()
    print("Solutions:")
    print("  • Wait for quota to reset (check https://ai.dev/usage)")
    print("  • Generate new API key at https://aistudio.google.com/apikey")
    print("  • Upgrade to paid plan for higher limits")
    print()
    sys.exit(1)
