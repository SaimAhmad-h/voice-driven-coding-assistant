# command_processor.py
import json
import re
from langgraph_setup import generate_text, graph

def parse_command(text: str):
    """
    Convert natural language to JSON command via Gemini AI.
    """
    prompt = f"""
You are a code assistant. Convert this instruction to JSON:
Instruction: "{text}"
JSON format: {{
  "action": "create_file/edit_file/append_file/delete_file/rename_file/run_script",
  "filename": "<file name>",
  "content": "<text to write>",
  "new_name": "<new file name if rename>"
}}
Respond ONLY with JSON, nothing else.
"""
    try:
        response_text = generate_text(prompt)

        # Extract JSON block from response
        json_match = re.search(r"\{.*\}", response_text, flags=re.DOTALL)
        if not json_match:
            print(f"⚠️ No JSON found in Gemini response: {response_text}")
            return None

        cmd = json.loads(json_match.group(0))

        # --- Update LangGraph session state ---
        graph["session_1"] = {
            "current_file": cmd.get("filename", ""),
            "last_command": cmd.get("action", ""),
            "file_history": {cmd.get("filename", ""): cmd.get("content", "")}
        }

        return cmd

    except json.JSONDecodeError:
        print(f"⚠️ Failed to parse JSON: {response_text}")
        return None
    except Exception as e:
        print(f"⚠️ Gemini command parsing failed: {e}")
        return None