import pyaudio
import wave
import os
import numpy as np

CHUNK = 1024  # Samples per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44000  # Sample rate (Hz)
OUTPUT_FILENAME = "output.wav"

SAVE_DIR = "uploads"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

OUTPUT_FILENAME = os.path.join(SAVE_DIR, "recorded_audio.wav")

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True, # Enable output for monitoring
                frames_per_buffer=CHUNK)

print("Recording...")

frames = []

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        #stream.write(data) # Plays audio back
except KeyboardInterrupt:
    print("\nStopped recording. Saving file...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {OUTPUT_FILENAME}")