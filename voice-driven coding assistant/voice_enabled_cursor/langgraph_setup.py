# langgraph_setup.py
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict
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

# --- LangGraph state schema ---
class VoiceState(TypedDict):
    current_file: str
    last_command: str
    file_history: dict

# --- SQLite saver ---
graph_saver = SqliteSaver("voice_assistant.db")

# --- Initialize LangGraph ---
graph = StateGraph(state_schema=VoiceState, saver=graph_saver)