Project Title

Voice-Enabled Cursor Control & Coding System using Gemini AI

🎯 Overview

This project is an AI-powered voice assistant that allows users to interact with their computer using natural speech instead of keyboard and mouse. It leverages Google Gemini to understand flexible human language and convert it into actionable system commands.

Unlike traditional systems that require fixed commands, this system can interpret natural, conversational instructions like:
👉 “Create a Python file named app.py and write a hello world program”

⚙️ Core Idea

The system works as a pipeline:

🎤 Voice Input → 📝 Speech-to-Text → 🧠 Gemini AI → ⚙️ Command Execution
Voice is captured from the microphone
Converted into text
Sent to Gemini AI
Gemini understands intent and generates structured commands
Commands are executed on the system
🧠 Role of Gemini AI

Google Gemini is the brain of the system:

Understands natural language
Extracts intent (create, delete, edit, move, etc.)
Converts instructions into structured actions
Removes the need for strict command syntax

Example:

Input:

“Make a file called test.py and write a loop”

Output (interpreted):

{
  "action": "create_file",
  "filename": "test.py",
  "content": "for i in range(10): print(i)"
}
🧩 System Components
1. 🎤 Voice Recognition
Captures user speech
Converts audio → text using speech recognition
2. 🧠 AI Processing (Gemini)
Takes text input
Understands meaning
Generates structured commands
3. ⚙️ Command Execution Engine
Executes tasks like:
📁 File creation
✏️ Code writing/editing
❌ File deletion
Can be extended to:
🖱️ Mouse control
⌨️ Keyboard automation
4. 📂 File System Interaction
Handles real file operations
Creates and modifies code files dynamically
🔁 Workflow Example
User says:

“Create a file named hello.py and write a hello world program”

System does:
Converts speech → text
Sends text to Gemini
Gemini understands intent
Generates command
Python script creates file and writes code
🚀 Features
✅ Natural language understanding (no fixed commands)
✅ Code generation using AI
✅ File creation, editing, deletion
✅ Voice-controlled workflow
🔄 Extendable to full system automation
❌ Current Limitation
Does NOT yet control mouse cursor
Focus is mainly on code & file operations
Needs additional libraries (like pyautogui) for full OS control
🔮 Future Enhancements
🖱️ Cursor control via voice
🤖 Full AI agent using workflows (LangGraph)
🧠 Context memory (conversation-aware commands)
🖥️ Application control (open VS Code, browser, etc.)
📊 Smart debugging assistant
💡 Use Cases
👨‍💻 Developers (hands-free coding)
♿ Accessibility (assistive technology)
⚡ Productivity automation
🧪 AI-based system control research
