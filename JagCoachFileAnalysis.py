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

    try:
        extract_audio(file_path, output_path, output_format="wav")

        # Need to add SAMPLE_RATE to the confiig file.
        sound = AudioSegment.from_wav(output_path)
        sound = sound.set_frame_rate(config.SAMPLE_RATE).set_channels(1)

        # Export the clean WAV file
        sound.export(output_path, format="wav", codec="pcm_s16le")
        print(f"Cleaned audio file saved: {output_path}")

        return output_path
    except Exception as e:
        raise RuntimeError(f"Error processing audio file '{file_path}': {e}")

# Get gender of presenter
def get_gender_mood(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.myspgend(p, c)

# Get pronunciation score
def get_pronunciation_score(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.mysppron(p, c)

# Get speech rate
def get_speech_rate(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.myspsr(p, c)

# Get articulation rate
def get_articulation_rate(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.myspatc(p, c)

# Get ratio of speaking time excl. fillers/pauses and total speaking time
def get_speaking_time_ratio(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.myspbala(p, c)

# Get pauses in the speech
def get_pauses(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    return mysp.mysppaus(p, c)


if __name__ == "__main__":
    test_file = os.path.join(config.UPLOAD_FOLDER, "vid1.mp4")

    try:
        wav_file = process_video(test_file)
        print(f"Audio extracted successfully: {wav_file}")
        get_pauses(wav_file)
        get_gender_mood(wav_file)
        get_pronunciation_score(wav_file)
        get_speech_rate(wav_file)
        get_articulation_rate(wav_file)
        get_speaking_time_ratio(wav_file)

    except Exception as e:
        print(f"Error: {e}")
