"""
Test AI Integration
Verifies that the AI client can actually generate structured output with the new model
"""

from ai_client import get_ai_client
import json

def test_integration():
    client = get_ai_client()
    
    if not client.is_available():
        print("❌ AI Client not available")
        return
        
    print(f"✅ AI Client available with model: {client._client}...")
    
    prompt = "Analyze this resume snippet: 'Senior Python Developer with 5 years experience'."
    schema = {
        "grade": "string",
        "score": "number"
    }
    
    print("Testing generation...")
    try:
        result = client.analyze_with_structured_output(prompt, schema)
        if result:
            print(f"✅ Success! Result: {json.dumps(result)}")
        else:
            print("❌ Failed to get result")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_integration()
