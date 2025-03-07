import whisper
import os
import ssl

# For line below put your location of where your whisper model is.
default_cache_dir = os.path.expanduser("~/.cache/whisper")
whisper_cache_dir = os.getenv("WHISPER_CACHE_DIR", default_cache_dir)
os.environ["WHISPER_CACHE_DIR"] = whisper_cache_dir

# honestly dont know what this line did. Had help for this part
ssl._create_default_https_context = ssl._create_unverified_context


def transcript(wavPath):
    try:
        print(f"Loading Whisper model from cache: {os.environ['WHISPER_CACHE_DIR']}")
        model = whisper.load_model("base")  # This will now use the cached model
        print("Model loaded successfully!")

        result = model.transcribe(wavPath, fp16=False, language="English")
        print("Transcription complete!")

        return result["text"]
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")