# voice_input_llm.py
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from command_processor import parse_command
from executor import execute_command
from config import WHISPER_MODEL, DEVICE

# Load Whisper
model = WhisperModel(WHISPER_MODEL, device=DEVICE, compute_type="int8")

recording = False
audio_chunks = []

def audio_callback(indata, frames, time, status):
    if recording:
        audio_chunks.append(indata.copy())

def process_audio():
    global audio_chunks
    audio = np.concatenate(audio_chunks, axis=0).flatten()
    audio_chunks = []

    segments, _ = model.transcribe(audio, beam_size=5, language="en", vad_filter=True)
    text = "".join([s.text for s in segments]).strip()

    if text:
        print(f"✅ Recognized: {text}")
        cmd = parse_command(text)
        if cmd is not None:
            execute_command(cmd)

def start_continuous_listening():
    global recording, audio_chunks
    recording = True
    audio_chunks = []

    print("🎙️ Listening continuously... Speak naturally!")
    stream = sd.InputStream(samplerate=16000, channels=1, callback=audio_callback, dtype='float32')
    stream.start()

    try:
        while recording:
            if len(audio_chunks) > 0:
                process_audio()
    except KeyboardInterrupt:
        recording = False
        stream.stop()
        stream.close()
        print("\n🛑 Stopped listening.")