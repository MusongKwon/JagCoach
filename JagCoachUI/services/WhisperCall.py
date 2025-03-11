import whisper
import os
from JagCoachUI.config import config

def get_transcript(wavPath):
    try:
        model = whisper.load_model("base")
        print(f"Transcribing {wavPath}...")

        result = model.transcribe(wavPath, fp16=False, language="English")
        transcribed_text = result["text"]

        filename = os.path.splitext(os.path.basename(wavPath))[0]  # Extract filename without extension

        #transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + "Transcript.txt")
        processed_audio_path = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio\\")
        transcript_path = os.path.join(processed_audio_path, filename + "_transcript.txt")

        if os.path.exists(transcript_path):
            os.remove(transcript_path)
            print(f"Existing file '{transcript_path}' deleted.")

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        
        return transcript_path
            
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")
