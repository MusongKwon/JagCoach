import whisper

def get_transcript(wavPath):
    try:
        model = whisper.load_model("base")
        print(f"Transcribing {wavPath}...")

        result = model.transcribe(wavPath, fp16=False, language="English")
        transcribed_text = result["text"]
        
        return transcribed_text     
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise RuntimeError(f"Error processing audio file '{wavPath}': {e}")
