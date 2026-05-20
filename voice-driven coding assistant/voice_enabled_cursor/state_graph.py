# state_graph.py
state = {
    "current_file": None,
    "last_command": None,
    "file_history": {}  # filename -> content
}

def set_current_file(filename: str, content: str):
    state["current_file"] = filename
    if filename:
        state["file_history"][filename] = content

def get_context():
    return state

def remember_command(command: str):
    state["last_command"] = command