"""
Calculate when Gemini API quota will reset.

Quotas reset at midnight UTC daily.
"""

import sys
from datetime import datetime, timezone, timedelta

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Gemini API Quota Reset Calculator")
print("=" * 60)
print()

# Get current time
now_utc = datetime.now(timezone.utc)
now_local = datetime.now()

print(f"Current UTC time:   {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Current local time: {now_local.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Calculate next midnight UTC
tomorrow_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# Time until reset
time_until_reset = tomorrow_utc - now_utc
hours = int(time_until_reset.total_seconds() // 3600)
minutes = int((time_until_reset.total_seconds() % 3600) // 60)
seconds = int(time_until_reset.total_seconds() % 60)

print("Daily Quota Reset Information:")
print("-" * 60)
print(f"Resets at:          Midnight UTC (00:00 UTC)")
print(f"Next reset:         {tomorrow_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print()
print(f"Time until reset:   {hours}h {minutes}m {seconds}s")
print()

# Convert to local time
utc_offset = now_local.replace(tzinfo=None) - now_utc.replace(tzinfo=None)
reset_local = tomorrow_utc.replace(tzinfo=None) + utc_offset

print(f"Next reset (local): {reset_local.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Rate limit info (per-minute resets)
print("Rate Limit Information:")
print("-" * 60)
print("Free tier rate limits reset every minute:")
print("  • 15 requests per minute")
print("  • Resets every 60 seconds")
print()

# Recommendations
print("Recommendations:")
print("-" * 60)
if hours < 2:
    print(f"✓ Daily quota resets in {hours}h {minutes}m - Almost there!")
    print("  Wait for reset and try again")
elif hours < 12:
    print(f"⏳ Daily quota resets in {hours}h {minutes}m")
    print("  Consider:")
    print("  • Using a different Google account API key")
    print("  • Upgrading to paid tier for immediate access")
else:
    print(f"⏳ Daily quota resets in {hours}h {minutes}m")
    print("  Recommended:")
    print("  • Generate new API key with different Google account")
    print("  • Or upgrade to paid tier: https://ai.google.dev/pricing")

print()
print("=" * 60)
print("Monitor your usage: https://ai.dev/usage?tab=rate-limit")
print("=" * 60)
