import whisper

def transcript(wavPath):
    model = whisper.load_model("base")
    result = model.transcribe(wavPath, fp16=False, language="English")
    print(result["text"])