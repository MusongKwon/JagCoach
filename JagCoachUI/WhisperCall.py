import os
import whisper
from audio_extract import extract_audio
from pydub import AudioSegment

# Directories
UPLOAD_FOLDER = "uploads"
TRANSCRIPT_FOLDER = "transcripts"

# Ensure directories exist
for folder in [UPLOAD_FOLDER, TRANSCRIPT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def convert_all_mp4_to_wav():
    """
    Converts all MP4 files in the uploads directory to WAV format.
    """
    processed_wavs = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".mp4"):
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            base_name = os.path.splitext(filename)[0]  # Get filename without extension
            output_path = os.path.join(UPLOAD_FOLDER, base_name + ".wav")

            # Skip if already converted
            if os.path.exists(output_path):
                print(f"Skipping already converted file: {output_path}", flush=True)
                processed_wavs.append(output_path)
                continue

            try:
                print(f"Converting {input_path} to WAV...", flush=True)
                intermediate_wav = os.path.join(UPLOAD_FOLDER, base_name + "_temp.wav")

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

                processed_wavs.append(output_path)

            except Exception as e:
                print(f"Error processing {input_path}: {e}", flush=True)

    return processed_wavs

def transcribe_audio(wav_path):
    """
    Transcribes a WAV file using Whisper.
    """
    print(f"Transcribing {wav_path}...", flush=True)
    model = whisper.load_model("base")
    result = model.transcribe(wav_path, fp16=False, language="English")
    return result["text"]

def save_transcript(filename, text):
    """
    Saves the transcribed text into a .txt file inside the transcripts folder.
    """
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + ".txt")

    try:
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcript saved: {transcript_path}")
    except Exception as e:
        print(f"Error saving transcript for {filename}: {e}")

# Run the process
if __name__ == "__main__":
    processed_wavs = convert_all_mp4_to_wav()

    for wav_file in processed_wavs:
        filename = os.path.splitext(os.path.basename(wav_file))[0]  # Extract name
        transcription = transcribe_audio(wav_file)  # Get transcription
        save_transcript(filename, transcription)  # Save to .txt

    print("All files processed successfully!")
