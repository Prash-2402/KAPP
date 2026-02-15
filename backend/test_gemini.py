"""
Test script to debug Gemini API connection
"""

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "")
print(f"API Key found: {API_KEY[:20]}..." if API_KEY else "❌ No API key!")

try:
    from google import genai
    print("✅ google-genai package imported")
    
    client = genai.Client(api_key=API_KEY)
    print("✅ Client created")
    
    # List available models
    print("\n📋 Available models:")
    models = client.models.list()
    for model in models:
        print(f"  - {model.name}")
    
    # Try simple content generation
    print("\n🧪 Testing content generation...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Say 'Hello, AI is working!'"
    )
    print(f"✅ Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
