import os
from pydub import AudioSegment
from audio_extract import extract_audio
mysp = __import__("my-voice-analysis")

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Define output file path (same name, different extension)
    output_dir = "processed_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    # Convert video to audio
    extract_audio(file_path, output_path, output_format="wav")

    return output_path

def clean_wav(file_path):
    output_dir = "cleaned_audio"
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    sample_rate = 44000
    sound = AudioSegment.from_wav(file_path)
    sound = sound.set_frame_rate(sample_rate).set_channels(1)

    sound.export(output_path, format="wav")

    return output_path

#def get_pauses(file_path):
#    p="CybSecCapstone"
#    c=r"processed_audio/"

if __name__ == "__main__":
    # Example usage for testing
    test_file = "uploads/CybSecCapstone.mp4"
    
    try:
        wav_file = process_video(test_file)
        print(f"Audio extracted successfully: {wav_file}")
    except Exception as e:
        print(f"Error: {e}")

    cleaned_file = clean_wav(wav_file)

    #p="CybSecCapstone"
    #c=r"cleaned_audio/"
    #print(mysp.mysppaus(p,c))
