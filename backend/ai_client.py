"""
AI Client for Resume Analysis
Uses NEW Google Gemini SDK (google-genai)
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from google import genai
    from google.genai.types import GenerateContentConfig
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-genai not installed. AI features disabled.")

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")
GEMINI_MODEL = "gemini-2.5-flash"  # Latest available model


class AIClient:
    """Singleton AI client for resume analysis"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the AI client"""
        if not GEMINI_AVAILABLE:
            print("❌ Gemini SDK not available")
            return
        
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            print("⚠️  GEMINI_API_KEY not configured. AI features will use fallback.")
            return
        
        try:
            self._client = genai.Client(api_key=GEMINI_API_KEY)
            print(f"✅ AI Client initialized with {GEMINI_MODEL}")
        except Exception as e:
            print(f"❌ Failed to initialize AI client: {e}")
    
    def is_available(self) -> bool:
        """Check if AI client is ready"""
        return self._client is not None
    
    def analyze_with_structured_output(
        self, 
        prompt: str, 
        response_schema: Dict[str, Any]
    ) -> Optional[Dict]:
        """
        Call AI with structured JSON output
        
        Args:
            prompt: The analysis prompt
            response_schema: Expected JSON schema for validation
            
        Returns:
            Parsed JSON dict or None if failed
        """
        if not self.is_available():
            print("⚠️  AI not available, using fallback")
            return None
        
        try:
            # Add JSON instruction to prompt
            full_prompt = f"""{prompt}

IMPORTANT: Respond ONLY with valid JSON matching this schema.
Keep text descriptions CONCISE and professional to ensure valid JSON output.
{json.dumps(response_schema, indent=2)}

Do not include any explanation or markdown formatting. Just the raw JSON."""
            
            # Retry logic with exponential backoff
            import time
            import random
            
            max_retries = 3
            base_delay = 2
            
            for attempt in range(max_retries):
                try:
                    # Make API call with NEW SDK
                    response = self._client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=full_prompt,
                        config=GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=8192 # Increased to prevent truncation
                        )
                    )
                    break # Success!
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                        print(f"⚠️ Rate limit hit. Retrying in {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise e # Re-raise if not 429 or max retries reached
            
            # Parse response
            if not response.text:
                print("❌ Empty response from AI")
                return None
                
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            # Handle ```json ... ``` and just ``` ... ```
            if "```" in response_text:
                # Find the first { and last }
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}")
                if start_idx != -1 and end_idx != -1:
                    response_text = response_text[start_idx:end_idx+1]
            
            # Parse JSON
            try:
                result = json.loads(response_text)
                print(f"✅ AI Analysis successful!")
                return result
            except json.JSONDecodeError:
                # Last ditch effort: try to repair common JSON issues
                import re
                # Fix trailing commas
                response_text = re.sub(r',(\s*})', r'\1', response_text)
                response_text = re.sub(r',(\s*])', r'\1', response_text)
                result = json.loads(response_text)
                print(f"✅ AI Analysis successful (after repair)!")
                return result
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse AI response as JSON: {e}")
            print(f"Raw Response: {response.text[:500]}...")  # Log start of response
            return None
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            # Check for rate limit specifically
            if "429" in str(e):
                print("⚠️ Retries exhausted. Rate limit persist.")
            return None


# Global instance
ai_client = AIClient()


def get_ai_client() -> AIClient:
    """Get the global AI client instance"""
    return ai_client
