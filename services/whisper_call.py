import whisper


def transcript(wavPath):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(wavPath, fp16=False, language="English")
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")
