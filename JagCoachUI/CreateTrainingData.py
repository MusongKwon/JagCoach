import os
import re
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


# Function to extract numeric part of filename for sorting
def extract_number(filename):
    match = re.search(r'\d+', filename)  # Find first sequence of digits
    return int(match.group()) if match else float('inf')  # If no number, send to end


# Convert MP4 to WAV
def convert_all_mp4_to_wav():
    processed_wavs = []

    # Get all MP4 files and sort them numerically
    mp4_files = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp4")], key=extract_number)

    for filename in mp4_files:
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(UPLOAD_FOLDER, base_name + ".wav")

        if os.path.exists(output_path):
            print(f"Skipping already converted file: {output_path}", flush=True)
            processed_wavs.append(output_path)
            continue

        try:
            print(f"Converting {input_path} to WAV...", flush=True)
            intermediate_wav = os.path.join(UPLOAD_FOLDER, base_name + "_temp.wav")

            extract_audio(input_path, intermediate_wav, output_format="wav")

            sound = AudioSegment.from_wav(intermediate_wav)
            sound = sound.set_frame_rate(44000).set_channels(1)

            print(f"Exporting final WAV to {output_path}", flush=True)
            sound.export(output_path, format="wav")

            os.remove(intermediate_wav)
            print("Temporary file removed.", flush=True)

            processed_wavs.append(output_path)

        except Exception as e:
            print(f"Error processing {input_path}: {e}", flush=True)

    return processed_wavs


# Transcribe audio
def transcribe_audio(wav_path):
    print(f"Transcribing {wav_path}...", flush=True)
    model = whisper.load_model("base")
    result = model.transcribe(wav_path, fp16=False, language="English")
    return result["text"]


# Save transcript
def save_transcript(filename, text):
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + ".txt")

    if os.path.exists(transcript_path):
        print(f"Skipping transcript save: {transcript_path} already exists.", flush=True)
    else:
        try:
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Transcript saved: {transcript_path}")
        except Exception as e:
            print(f"Error saving transcript for {filename}: {e}")

    # Process transcript for filler words
    get_dictionary_path(transcript_path)


# Load dictionary
def load_dictionary(dictionary_path):
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)


# Analyze transcript
def check_words_in_file(file_path, dictionary):
    total_word_count = 0
    filler_word_count = 0
    statistics = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            total_word_count += len(words)
            for word in words:
                cleaned_word = word.lower().strip('.,!?()[]{}":;')
                if cleaned_word in dictionary:
                    filler_word_count += 1
                    print(f"Match found: {cleaned_word}")

    non_filler_ratio = (total_word_count - filler_word_count) / total_word_count if total_word_count > 0 else 0
    non_filler_ratio = round(float(non_filler_ratio), 2)

    statistics.append(non_filler_ratio)
    statistics.append(filler_word_count)

    print(f"Total words: {total_word_count}")
    print(f"Filler words: {filler_word_count}")
    print(f"Non-filler word ratio: {non_filler_ratio}")

    return statistics


# Dictionary processing
def get_dictionary_path(transcript_path):
    dictionary_path = 'fillerwords.txt'
    dictionary = load_dictionary(dictionary_path)

    stats = check_words_in_file(transcript_path, dictionary)

    # Convert list to a comma-separated string (without brackets)
    stats_str = ", ".join(map(str, stats))

    # Write results to an existing file
    with open("statistic_return.txt", "a", encoding="utf-8") as output_file:
        # Adjusting the length of the path to have a fixed width (e.g., 30 characters)
        path = transcript_path.ljust(30)
        # Write the formatted line with the stats aligned
        output_file.write(f"{path}: {stats_str}\n")


# Run process
if __name__ == "__main__":
    processed_wavs = convert_all_mp4_to_wav()

    # Sort processed WAVs numerically before processing
    processed_wavs.sort(key=extract_number)

    for wav_file in processed_wavs:
        filename = os.path.splitext(os.path.basename(wav_file))[0]
        transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename + ".txt")

        if os.path.exists(transcript_path):
            print(f"Skipping transcription: {transcript_path} already exists.", flush=True)
            get_dictionary_path(transcript_path)  # Ensure it still gets analyzed
            continue

        transcription = transcribe_audio(wav_file)
        save_transcript(filename, transcription)

    print("All files processed successfully!")
