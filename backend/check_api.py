"""
Check API Availability
Just pings the API once to see if we are rate limited or good to go.
"""
from ai_client import get_ai_client
import time

def check_status():
    client = get_ai_client()
    if not client.is_available():
        print("❌ AI Client not configured")
        return

    print("Checking API status...")
    try:
        # Simple generation
        response = client._client.models.generate_content(
            model=client.GEMINI_MODEL if hasattr(client, 'GEMINI_MODEL') else "gemini-2.0-flash",
            contents="Ping"
        )
        print("✅ API IS READY! (Status: OK)")
        print(f"Response: {response.text.strip()}")
    except Exception as e:
        if "429" in str(e):
            print("⚠️ Still Rate Limited (429). Please wait.")
        else:
            print(f"❌ Other Error: {e}")

if __name__ == "__main__":
    check_status()
