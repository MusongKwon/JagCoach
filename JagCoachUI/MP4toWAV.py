import os
from audio_extract import extract_audio
from pydub import AudioSegment

from JagCoachUI.MYSPAnalysis import get_elements
from WhisperCall import transcript

# convert SINGULAR uploaded mp4 file -> a .wav (creates temp and deletes it)
def convert_mp4_to_wav(input_path, output_path=None):
    """
       Converts an MP4 file to WAV format by extracting audio, adjusting the sample rate, and converting to mono.

       Parameters:
           input_path (str): Path to the input MP4 file.
           output_path (str, optional): Path to save the final WAV file. If not provided, it will be generated.
       """
    # checks if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file not found: {input_path}")

    # try statement converts from mp4 -> temp.wav -> deletes temp.wav -> .wav
    try:
        print("Converting MP4 to WAV...", flush=True)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        base_name = os.path.splitext(input_path)[0]
        intermediate_wav = base_name + "_temp.wav"

        if output_path is None:
            output_path = base_name + ".wav"

        # extracts audio and sets the standards for needed output
        print(f"Extracting audio from {input_path} to {intermediate_wav}", flush=True)
        extract_audio(input_path, intermediate_wav, output_format="wav")

        sound = AudioSegment.from_wav(intermediate_wav)
        sound = sound.set_frame_rate(44000).set_channels(1)

        print(f"Exporting final WAV to {output_path}", flush=True)
        sound.export(output_path, format="wav")

        # deletes temp file
        os.remove(intermediate_wav)
        print("Temporary file removed.", flush=True)

        # call transcript from WhisperCall.py, passes the output_path so it can have the .wav file
        transcript(output_path)
        #get_elements(output_path)

        # useless return here (idk if true dont want to test)
        return output_path

    except Exception as e:
        print(f"Error during conversion: {e}", flush=True)
        raise