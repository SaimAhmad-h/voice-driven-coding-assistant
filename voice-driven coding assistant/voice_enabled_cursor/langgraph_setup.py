# langgraph_setup.py
from config import GEMINI_API_KEY, GEMINI_MODEL
from google import genai
import os

# --- Gemini AI client ---
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
client = genai.Client()

def generate_text(prompt: str) -> str:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text
