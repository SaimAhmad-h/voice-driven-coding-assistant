# 🎙️ Voice-Driven Coding Assistant

A Python-based AI tool that lets you control file operations using natural voice commands. Instead of typing, you speak — the assistant listens, understands your intent using Google Gemini AI, and performs the file operation automatically.

No rigid command syntax. No memorizing shortcuts. Just speak naturally.

---

## 🚀 How It Works

The system is a simple, linear pipeline with four stages:

```
🎤 Microphone Input
      ↓
📝 Whisper Speech-to-Text (local, runs on CPU)
      ↓
🧠 Google Gemini AI (interprets intent, generates JSON command)
      ↓
⚙️ File Operation Executed on your system
```

### Stage 1 — Voice Capture
The microphone is opened using `sounddevice` and audio is streamed continuously in real time. You do not need to press any button to start or stop — the system listens as long as it is running.

### Stage 2 — Speech to Text
The captured audio is passed to **Whisper** (`faster-whisper`, small model, CPU mode) which converts your speech into text. Whisper's VAD (Voice Activity Detection) filter is enabled, which helps ignore silence and background noise.

### Stage 3 — AI Command Parsing
The transcribed text is sent to **Google Gemini 2.5 Flash** with a structured prompt that instructs it to respond only with a JSON object. Gemini identifies the action you want (create, edit, delete, etc.), the filename, and the content — and returns it in this format:

```json
{
  "action": "create_file",
  "filename": "hello.py",
  "content": "print('Hello World')",
  "new_name": ""
}
```

If Gemini's response contains anything other than JSON, the system extracts the JSON block using regex and safely ignores the rest.

### Stage 4 — Execution
The parsed JSON command is passed to the execution engine which performs the actual file operation on your system using Python's built-in `os` and `subprocess` modules.

---

## ✅ Supported Commands

The assistant supports **6 file operations**. You can trigger them using natural language — you don't need to say the exact action name.

| Action | What It Does | Voice Example |
|---|---|---|
| `create_file` | Creates a new file and writes content into it | *"Create a Python file named app.py with a hello world program"* |
| `edit_file` | Overwrites an existing file with new content | *"Edit app.py and change the message to goodbye world"* |
| `append_file` | Adds content to the end of an existing file | *"Append a for loop from 1 to 10 to app.py"* |
| `delete_file` | Deletes a file from the system | *"Delete old_script.py"* |
| `rename_file` | Renames a file | *"Rename app.py to main.py"* |
| `run_script` | Runs a Python file and prints its output | *"Run main.py"* |

---

## 🧩 Project Structure

```
voice_enabled_cursor/
├── main.py               # Entry point — starts the listening loop
├── voice_input_llm.py    # Microphone capture + Whisper transcription + pipeline trigger
├── command_processor.py  # Builds Gemini prompt, parses JSON response
├── executor.py           # Executes the file operation based on parsed command
├── langgraph_setup.py    # Gemini AI client initialization
├── config.py             # Model names, device settings, API key
└── requirements.txt      # Python dependencies
```

### File Responsibilities

**`main.py`**
The entry point. Calls `start_continuous_listening()` and nothing else. Kept intentionally minimal.

**`voice_input_llm.py`**
Handles the entire audio pipeline — opens the microphone stream via `sounddevice`, collects audio chunks in a callback, concatenates them into a numpy array, and passes to Whisper for transcription. On successful transcription, it calls the command processor and then the executor.

**`command_processor.py`**
Takes the transcribed text and builds a structured prompt for Gemini. Sends it via the Gemini client and uses regex (`re.search`) to extract the JSON block from the response. Parses it with `json.loads` and returns the command dict.

**`executor.py`**
Receives the command dict and performs the appropriate file operation. Checks file existence before editing, appending, deleting, or renaming. Wraps everything in try/except to handle errors gracefully without crashing the main loop.

**`langgraph_setup.py`**
Initializes the Google Gemini client using `google-genai` and exposes the `generate_text()` function used by the command processor.

**`config.py`**
Central configuration — Whisper model size (`small`), compute device (`cpu`), Gemini model (`gemini-2.5-flash`), and the API key placeholder.

---

## 🛠️ Technologies Used

| Technology | Role |
|---|---|
| **Python** | Core language |
| **faster-whisper** | Local speech-to-text using OpenAI's Whisper (small model, CPU) |
| **sounddevice** | Real-time microphone audio capture |
| **numpy** | Audio array processing |
| **Google Gemini 2.5 Flash** | Natural language understanding and code generation |
| **google-genai** | Official Python client for Gemini API |
| **os / subprocess** | File system operations and script execution |

---

## ⚙️ Setup & Installation

### Requirements
- Python 3.10 or higher
- A working microphone
- A free Google Gemini API key

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/SaimAhmad-h/voice-driven-coding-assistant
cd "voice-driven coding assistant/voice_enabled_cursor"
```

---

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
pip install google-genai
```

> **Note:** `google-genai` is required but not listed in `requirements.txt`. Install it separately as shown above.

---

### Step 3 — Add your Gemini API key

Open `config.py` and replace the empty string with your key:

```python
GEMINI_API_KEY = "your_api_key_here"
```

Get a free API key at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

The free tier supports `gemini-2.5-flash` which is the model this project uses.

---

### Step 4 — Run the assistant

```bash
python main.py
```

The assistant will print:
```
🎙️ Listening continuously... Speak naturally!
```

Speak your command into the microphone. The assistant will print what it recognized and what action it performed. Press `Ctrl+C` to stop.

---

## 💬 Example Session

```
🎙️ Listening continuously... Speak naturally!
✅ Recognized: Create a Python file named hello.py and print hello world
✅ File created: hello.py

✅ Recognized: Append a for loop from 1 to 5 to hello.py
✅ Content appended to file: hello.py

✅ Recognized: Run hello.py
🖥️ Script output:
Hello World
1
2
3
4
5

✅ Recognized: Delete hello.py
✅ File deleted: hello.py

🛑 Stopped listening.
```

---

## 📌 Known Limitations

### No Conversation Memory
Each voice command is processed independently. The assistant has no knowledge of previous commands in the same session. For example, saying *"edit the file I just created"* will not work — you must always specify the filename explicitly.

### Speech Recognition Accuracy
Whisper may mishear file names, especially ones that sound like common words or have underscores. For example:
- `my_app` might be heard as `my app`
- `reg_toba` might be heard as `regtoba`

Using short, clear, distinct file names reduces these errors.

### English Language Only
Whisper is configured with `language="en"`. Other languages are not supported in the current configuration.

### File Operations Only
The assistant can only create, edit, append, delete, rename, and run Python files. It cannot control the mouse, keyboard, open applications, or interact with the desktop in any way.

### Overwrites on Edit
The `edit_file` action completely overwrites the file. There is no diffing, merging, or partial editing — the entire file content is replaced with what Gemini generates.

### Script Execution Safety
When using `run_script`, the filename comes from Gemini's response. Always verify what file is being run. Avoid using this on files you did not create through this session.

---

## 🔮 Future Enhancements

These features are not yet implemented but are planned for future development:

- **Session memory** — remember previous commands and filenames within a session so you can say *"edit the last file"*
- **LangGraph agent** — multi-step task execution where one voice command triggers a sequence of actions
- **Desktop automation** — mouse and keyboard control using `pyautogui`
- **Application control** — open VS Code, browser, or terminal via voice
- **Smart debugging** — detect errors in generated code and automatically fix them
- **Wake word detection** — only listen when a specific trigger word is spoken

---

## 🤝 Contributions Welcome

This project is open for contributions. Some useful areas:

- **Silence detection** — improve audio processing so commands are only sent after the user finishes speaking
- **Better prompts** — improve Gemini prompt engineering for more accurate command parsing
- **Path validation** — add safety checks before executing or deleting files
- **`.env` support** — move API key out of `config.py` into a `.env` file
- **Error recovery** — handle cases where Gemini returns unexpected output more gracefully

---

## 📄 License

This project is open source. Feel free to use, modify, and build on it.
