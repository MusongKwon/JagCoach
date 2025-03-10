import whisper
import os
from JagCoachUI.services.FillerWords import get_filler_word_ratio

# Directories
UPLOAD_FOLDER = "uploads"
TRANSCRIPT_FOLDER = "uploads/transcripts"

# Ensure directories exist
for folder in [UPLOAD_FOLDER, TRANSCRIPT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_transcript(wavPath):
    try:
        """
        Transcribes the given WAV file using Whisper.
        """
        model = whisper.load_model("base")
        print(f"Transcribing {wavPath}...")

        result = model.transcribe(wavPath, fp16=False, language="English")
        transcribed_text = result["text"]

        filename = os.path.splitext(os.path.basename(wavPath))[0]  # Extract filename without extension

        transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + "Transcript.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)

        return transcript_path
            
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")
