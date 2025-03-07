import os
from pydub import AudioSegment
from audio_extract import extract_audio
from config import config  # Import centralized config settings


def process_video(file_path):

    print(f"processing_video() called! Processing: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Use configured audio output directory
    output_dir = os.path.join(config.UPLOAD_FOLDER, "processed_audio")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(output_dir):
        print(f"ERROR: Could not create directory {output_dir}")
    else:
        print(f"Output directory created: {output_dir}")

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    try:
        print(f"Extracting audio from '{file_path}'")
        extract_audio(file_path, output_path, output_format="wav")

        # Need to add SAMPLE_RATE to the confiig file.
        sound = AudioSegment.from_wav(output_path)
        sound = sound.set_frame_rate(config.SAMPLE_RATE).set_channels(1)

        # Export the clean WAV file
        sound.export(output_path, format="wav")
        print(f"Cleaned audio file saved: {output_path}")

        return output_path
    except Exception as e:
        raise RuntimeError(f"Error processing audio file '{file_path}': {e}")
