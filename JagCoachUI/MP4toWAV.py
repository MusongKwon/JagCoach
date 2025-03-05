import os
from audio_extract import extract_audio
from pydub import AudioSegment

UPLOAD_FOLDER = "uploads"

def convert_all_mp4_to_wav():
    """
    Converts all MP4 files in the uploads directory to WAV format.
    Calls transcript() on each successfully converted WAV file.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        print(f"Creating upload folder: {UPLOAD_FOLDER}")
        os.makedirs(UPLOAD_FOLDER)

    processed_files = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".mp4"):
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            base_name = os.path.splitext(input_path)[0]
            output_path = base_name + ".wav"

            # Skip if the WAV file already exists
            if os.path.exists(output_path):
                print(f"Skipping already converted file: {output_path}", flush=True)
                processed_files.append(output_path)
                continue

            try:
                print(f"Converting {input_path} to WAV...", flush=True)
                intermediate_wav = base_name + "_temp.wav"

                # Extract audio
                extract_audio(input_path, intermediate_wav, output_format="wav")

                # Convert to correct format
                sound = AudioSegment.from_wav(intermediate_wav)
                sound = sound.set_frame_rate(44000).set_channels(1)

                # Export final WAV file
                print(f"Exporting final WAV to {output_path}", flush=True)
                sound.export(output_path, format="wav")

                # Remove temporary file
                os.remove(intermediate_wav)
                print("Temporary file removed.", flush=True)

                # Run transcription
                #transcript(output_path)

                # Store processed file path
                processed_files.append(output_path)

            except Exception as e:
                print(f"Error processing {input_path}: {e}", flush=True)

    return processed_files

# Example usage
if __name__ == "__main__":
    processed_wavs = convert_all_mp4_to_wav()
    print("Processed WAV files:", processed_wavs)


#def convert_mp4_to_wav(input_path, output_path=None):
#    """
#       Converts an MP4 file to WAV format by extracting audio, adjusting the sample rate, and converting to mono.
#
#       Parameters:
#           input_path (str): Path to the input MP4 file.
#           output_path (str, optional): Path to save the final WAV file. If not provided, it will be generated.
#       """
#    if not os.path.exists(input_path):
#        raise FileNotFoundError("Input file not found: {input_path}")
#
#    try:
#        print("Converting MP4 to WAV...", flush=True)
#
#        if not os.path.exists(input_path):
#            raise FileNotFoundError(f"Input file not found: {input_path}")
#
#        base_name = os.path.splitext(input_path)[0]
#        intermediate_wav = base_name + "_temp.wav"
#
#        if output_path is None:
#            output_path = base_name + ".wav"
#
#        print(f"Extracting audio from {input_path} to {intermediate_wav}", flush=True)
#        extract_audio(input_path, intermediate_wav, output_format="wav")
#
#        sound = AudioSegment.from_wav(intermediate_wav)
#        sound = sound.set_frame_rate(44000).set_channels(1)
#
#        print(f"Exporting final WAV to {output_path}", flush=True)
#        sound.export(output_path, format="wav")
#
#        os.remove(intermediate_wav)
#        print("Temporary file removed.", flush=True)
#        transcript(output_path)
#
#        return output_path
#
#    except Exception as e:
#        print(f"Error during conversion: {e}", flush=True)
#        raise