import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_llm_response(prompt: str) -> dict:
    try:
        # Call Gemini model
        response = model.generate_content(prompt)

        response_text = response.text.strip()

        print("🔍 Gemini raw response:\n", response_text)  # Debugging output

        # Optional: Try to fix common malformed JSON
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Failed to parse Gemini response as JSON: {e}\nRaw response:\n{response_text}")
    except Exception as e:
        raise RuntimeError(f"❌ LLM generation failed: {e}")
