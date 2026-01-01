"""
Test Gemini API using native Google AI SDK.

The native SDK might have different quota limits than OpenAI-compatible endpoint.
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

from dotenv import load_dotenv

# Load .env file
env_path = backend_dir / ".env"
load_dotenv(env_path)

print("=" * 60)
print("Testing Native Gemini API")
print("=" * 60)
print()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("✗ ERROR: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

print(f"✓ API Key found: ***{api_key[-8:]}")
print()

# Try importing google-generativeai
try:
    import google.generativeai as genai
    print("✓ Native Gemini SDK found")
except ImportError:
    print("✗ google-generativeai not installed")
    print()
    print("Installing native Gemini SDK...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-generativeai"])
        import google.generativeai as genai
        print("✓ Successfully installed google-generativeai")
    except Exception as e:
        print(f"✗ Failed to install: {e}")
        sys.exit(1)

print()

# Configure API
genai.configure(api_key=api_key)

# Models to test
models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-1.5-flash-8b",
]

print("Testing models with native SDK...")
print("-" * 60)

working_model = None

for model_name in models_to_test:
    print(f"\n[{model_name}]")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Reply with OK")

        answer = response.text
        print(f"  ✓ SUCCESS: {answer}")
        print(f"  ✓ This model is working!")
        working_model = model_name
        break

    except Exception as e:
        error_str = str(e)

        if "404" in error_str or "not found" in error_str.lower() or "does not exist" in error_str.lower():
            print(f"  ✗ Model not available")
        elif "429" in error_str or "quota" in error_str.lower() or "resource_exhausted" in error_str.lower():
            print(f"  ✗ Quota exceeded")
        elif "401" in error_str or "403" in error_str or "invalid" in error_str.lower():
            print(f"  ✗ Authentication failed")
        else:
            print(f"  ✗ Error: {error_str[:150]}")

print()
print("=" * 60)

if working_model:
    print(f"✓ FOUND WORKING MODEL: {working_model}")
    print("=" * 60)
    print()
    print("This model works with the NATIVE Gemini SDK.")
    print()
    print("Your backend currently uses OpenAI-compatible endpoint.")
    print("Both should work, but native SDK might have better model support.")
    print()
    print(f"Recommended: GEMINI_MODEL={working_model}")
    print()
    sys.exit(0)
else:
    print("✗ NO WORKING MODEL FOUND")
    print("=" * 60)
    print()
    print("All available models have exceeded quota limits.")
    print()
    print("Next steps:")
    print("  1. Check your quota usage: https://ai.dev/usage")
    print("  2. Wait for quota reset (usually resets daily)")
    print("  3. Consider upgrading: https://ai.google.dev/pricing")
    print()
    sys.exit(1)
