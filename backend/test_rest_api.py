"""
Direct REST API Test for Gemini
Bypasses SDK to find exact available models and connectivity
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "")

def test_rest_api():
    print(f"🔑 Testing API Key: {API_KEY[:10]}...")
    
    # 1. Test List Models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    print(f"\n📡 Calling: {url.replace(API_KEY, 'API_KEY')}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ AVAILABLE MODELS:")
            found_models = []
            for model in data.get('models', []):
                name = model['name'].replace('models/', '')
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    print(f"  - {name}")
                    found_models.append(name)
            
            # 2. Test Generation with first found model
            if found_models:
                test_model = "gemini-1.5-flash" if "gemini-1.5-flash" in found_models else found_models[0]
                print(f"\n🧪 Testing generation with: {test_model}")
                
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_model}:generateContent?key={API_KEY}"
                payload = {
                    "contents": [{
                        "parts": [{"text": "Hello, are you working?"}]
                    }]
                }
                
                gen_response = requests.post(gen_url, json=payload)
                print(f"Generation Status: {gen_response.status_code}")
                if gen_response.status_code == 200:
                    print(f"✅ SUCCESS: {gen_response.json()['candidates'][0]['content']['parts'][0]['text']}")
                else:
                    print(f"❌ Generation Failed: {gen_response.text}")
                    
        else:
            print(f"❌ List Models Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_rest_api()
