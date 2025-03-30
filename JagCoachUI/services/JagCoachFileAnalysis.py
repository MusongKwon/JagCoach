import os
import re
from pydub import AudioSegment
from audio_extract import extract_audio
from JagCoachUI.config import config
mysp = __import__("my-voice-analysis")
from io import StringIO
import sys

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    output_dir = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

    print("The output path is: ", output_path)

    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Existing file '{output_path}' deleted.")

    try:
        extract_audio(file_path, output_path, output_format="wav")

        # Need to add SAMPLE_RATE to the confiig file.
        sound = AudioSegment.from_wav(output_path)
        sound = sound.set_frame_rate(config.SAMPLE_RATE).set_channels(1)

        # Export the clean WAV file
        sound.export(output_path, format="wav", codec="pcm_s16le")

        return output_path
    except Exception as e:
        raise RuntimeError(f"Error processing audio file '{file_path}': {e}")

# mysp functions print, so we need to create a text file to capture the output
def get_elements(file_path):
    p = os.path.splitext(os.path.basename(file_path))[0]
    c = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
    output_txt = os.path.join(c, f"{p}_analysis.txt")

    if os.path.exists(output_txt):
        os.remove(output_txt)
        print(f"Existing file '{output_txt}' deleted.")
    
    original_stdout = sys.stdout  # Save the original stdout
    sys.stdout = output_capture = StringIO()  # Redirect stdout to a string buffer

    try:
        mysp.myspgend(p, c)
        mysp.mysppron(p, c)
        mysp.myspsr(p, c)
        mysp.myspatc(p, c)
        mysp.myspbala(p, c)
        mysp.mysppaus(p, c)
    finally:
        sys.stdout = original_stdout
    
    with open(output_txt, "w") as f:
        f.write(output_capture.getvalue())

    return output_txt
    
PRONUNCIATION_SCORES = {95: 24, 90: 21, 80: 18, 75: 12, 70: 6}
PRONUNCIATION_SCORES_WITH_MOOD = {95: 20, 90: 18, 80: 15, 75: 10, 70: 5}
SPEECH_RATE_SCORES = {4.0: (12, 10), 3.0: (7, 6)}
ARTICULATION_SCORES = {5.0: (20, 17), 4.0: (14, 11), 3.0: (6, 5), 6.0: (6, 5)}
SPEAKING_RATIO_SCORES = {0.8: (20, 17), 0.9: (20, 17), 0.7: (15, 12), 0.6: (10, 8), 1.0: (10, 8), 0.5: (6, 5)}
FILLER_WORD_SCORES = {0.97: (24, 20), 0.95: (18, 15), 0.90: (12, 10), 0.85: (6, 5)}

def get_elements_dictionary():

    upload_folder = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
    analysis_file_path = os.path.join(upload_folder, "uploaded_usr_video_analysis.txt")
    filler_file_path = os.path.join(upload_folder, "filler_word_ratio.txt")

    # Initialize the dictionary with None values
    student_results = {
        "mood": None,
        "pronunciation_score": None,
        "speech_rate": None,
        "articulation_rate": None,
        "speaking_ratio": None,
        "filler_word_ratio": None,
        "final_grade": None
    }

    # Extract values from the text file
    try:
        with open(analysis_file_path, 'r') as file:
            for line in file:
                if match := re.search(r"mood of speech: (.+?),", line):
                    mood = match.group(1).strip()
                    student_results["mood"] = 0 if mood == "Showing no emotion" else (8 if mood == "Reading" else 16)
                elif match := re.search(r"Pronunciation_posteriori_probability_score_percentage= :([\d.]+)", line):
                    pronunciation_response = float(match.group(1))
                    score_dict = PRONUNCIATION_SCORES_WITH_MOOD if student_results["mood"] is not None else PRONUNCIATION_SCORES
                    student_results["pronunciation_score"] = next((v for k, v in score_dict.items() if pronunciation_response >= k), 0)
                elif match := re.search(r"rate_of_speech= ([\d.]+)", line):
                    speech_rate = float(match.group(1))
                    student_results["speech_rate"] = SPEECH_RATE_SCORES.get(speech_rate, (0, 0))[student_results["mood"] is not None]
                elif match := re.search(r"articulation_rate= ([\d.]+)", line):
                    articulation_rate = float(match.group(1))
                    student_results["articulation_rate"] = ARTICULATION_SCORES.get(articulation_rate, (0, 0))[student_results["mood"] is not None]
                elif match := re.search(r"balance= ([\d.]+)", line):
                    speaking_ratio = float(match.group(1))
                    student_results["speaking_ratio"] = SPEAKING_RATIO_SCORES.get(speaking_ratio, (0, 0))[student_results["mood"] is not None]
    except Exception as e:
        print(f"Error reading analysis file: {e}")
        return None

    try:
        with open(filler_file_path, 'r') as file:
            for line in file:
                if match := re.search(r"filler_word_ratio= ([\d.]+)", line):
                    filler_word_ratio = float(match.group(1))
                    student_results["filler_word_ratio"] = next((v[student_results["mood"] is not None] for k, v in FILLER_WORD_SCORES.items() if filler_word_ratio >= k), 0)
    except Exception as e:
        print(f"Error reading filler words file: {e}")
        return None

    # Calculate the final grade based on the individual scores
    student_results["final_grade"] = sum(filter(None, student_results.values()))

    return student_results
