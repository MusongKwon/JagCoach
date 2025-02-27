import os
from pydub import AudioSegment
from audio_extract import extract_audio
from config import config  # 🔹 Import centralized config settings
mysp = __import__("my-voice-analysis")

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Use configured audio output directory
    output_dir = os.path.join(config.UPLOAD_FOLDER, "processed_audio")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    # Convert video to audio
    extract_audio(file_path, output_path, output_format="wav")

    return output_path  # Return path to extracted audio file

def clean_wav(file_path):
    output_dir = os.path.join(config.UPLOAD_FOLDER, "cleaned_audio")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    try:
        sample_rate = 44000  # 🔹 Could be made configurable in `config.py`
        sound = AudioSegment.from_wav(file_path)
        sound = sound.set_frame_rate(sample_rate).set_channels(1)  # Convert to mono
        sound.export(output_path, format="wav")
        return output_path  # Return path to cleaned audio file
    except Exception as e:
        raise RuntimeError(f"Error processing audio file '{file_path}': {e}")

# Optional: Get pauses in the speech (if needed)
def get_pauses(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.path.join(config.UPLOAD_FOLDER, "cleaned_audio") + "/"  # Use config path
    return mysp.mysppaus(p, c)

if __name__ == "__main__":
    test_file = os.path.join(config.UPLOAD_FOLDER, "CybSecCapstone.mp4")

    try:
        wav_file = process_video(test_file)
        print(f"Audio extracted successfully: {wav_file}")

        cleaned_file = clean_wav(wav_file)
        print(f"Cleaned audio file saved: {cleaned_file}")

    except Exception as e:
        print(f"Error: {e}")
