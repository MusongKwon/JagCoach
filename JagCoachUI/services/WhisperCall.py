import whisper
import re

def get_transcript(wavPath):
    # Load the whisper model, transcribe the wav file, and return the text
    try:
        model = whisper.load_model("base")
        print(f"Transcribing {wavPath}...")

        result = model.transcribe(wavPath, fp16=False, language="English")
        transcribed_text = result["text"]
        transcribed_text = re.sub(r'(?<!\.)\.(?!\.)', '.\n\n', transcribed_text)
        return transcribed_text
    # Otherwise, print error message
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")
