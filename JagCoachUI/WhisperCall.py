import whisper
import os
from StatisticReturn import get_dictionary_path

# Directories
UPLOAD_FOLDER = "uploads"
TRANSCRIPT_FOLDER = "transcripts"

# Ensure directories exist
for folder in [UPLOAD_FOLDER, TRANSCRIPT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def transcript(wavPath):
    try:
        """
        Transcribes the given WAV file using Whisper.
        """
        model = whisper.load_model("base")
        print(f"Transcribing {wavPath}...")

        result = model.transcribe(wavPath, fp16=False, language="English")
        transcribed_text = result["text"]

        filename = os.path.splitext(os.path.basename(wavPath))[0]  # Extract filename without extension

        save_transcript(filename, transcribed_text) # calls save_transcript
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")

def save_transcript(filename, text):
    """
    Saves the transcribed text into a .txt file inside the transcripts folder.
    Removes directory paths and extensions for a clean filename.
    """
    try:
        print("Saving transcript...")

        transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + "Transcript.txt")

        if os.path.exists(transcript_path):
            print(f"Skipping transcript save: {transcript_path} already exists.", flush=True)
            get_dictionary_path(transcript_path)
            return

        else:
            try:
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(text)  # Save transcription text
                print(f"Transcript saved: {transcript_path}")
            except Exception as e:
                print(f"Error saving transcript for {filename}: {e}")
            get_dictionary_path(transcript_path)
    except Exception as e:
        print(f"Error saving transcript for {filename}: {e}")

