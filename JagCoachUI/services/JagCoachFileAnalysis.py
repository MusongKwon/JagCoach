import os
from pydub import AudioSegment
from audio_extract import extract_audio
from JagCoachUI.config import config  # 🔹 Import centralized config settings
mysp = __import__("my-voice-analysis")
from io import StringIO
import sys
from JagCoachUI.services.LLM import evaluate_speech
import json

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Use configured audio output directory
    output_dir = os.path.join(config.UPLOAD_FOLDER, "processed_audio")
    os.makedirs(output_dir, exist_ok=True)

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
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio\\")
    output_txt = os.path.join(c, f"{p}_analysis.txt")
    print(c + p)

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
    
def get_elements_dictionary(txt_file_path):
    # Generate output JSON file path by replacing .txt with .json
    json_file_path = os.path.splitext(txt_file_path)[0] + ".json"

    # Initialize the dictionary with None values
    student_results = {
        "mood": None,
        "pronunciation_score": None,
        "speech_rate": None,
        "articulation_rate": None,
        "speaking_ratio": None,
        "filler_word_ratio": None
    }

    # Extract values from the text file
    try:
        with open(txt_file_path, 'r') as file:
            content = file.read()

            # Extract "mood of speech"
            if "mood of speech: " in content:
                start_index = content.find("mood of speech: ") + len("mood of speech: ")
                end_index = content.find(",", start_index)
                mood = content[start_index:end_index].strip()
                if mood == "Showing no emotion":
                    student_results["mood"] = 1
                elif mood == "Reading":
                    student_results["mood"] = 2
                elif mood:
                    student_results["mood"] = 3

            # Extract "pronunciation score"
            if "Pronunciation_posteriori_probability_score_percentage= :" in content:
                start_index = content.find("Pronunciation_posteriori_probability_score_percentage= :") + len(
                    "Pronunciation_posteriori_probability_score_percentage= :")
                student_results["pronunciation_score"] = float(content[start_index:].split()[0])

            # Extract "speech rate"
            if "rate_of_speech= " in content:
                start_index = content.find("rate_of_speech= ") + len("rate_of_speech= ")
                student_results["speech_rate"] = float(content[start_index:].split()[0])

            # Extract "articulation rate"
            if "articulation_rate= " in content:
                start_index = content.find("articulation_rate= ") + len("articulation_rate= ")
                student_results["articulation_rate"] = float(content[start_index:].split()[0])

            # Extract "speaking ratio"
            if "balance= " in content:
                start_index = content.find("balance= ") + len("balance= ")
                student_results["speaking_ratio"] = float(content[start_index:].split()[0])

            # Extract "filler word ratio" if present
            if "filler_word_ratio= " in content:
                start_index = content.find("filler_word_ratio= ") + len("filler_word_ratio= ")
                student_results["filler_word_ratio"] = float(content[start_index:].split()[0])

    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Create the final JSON structure
    json_data = {"student_results": student_results}

    # Write to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"JSON file '{json_file_path}' created successfully.")
    return json_file_path  # Returning for reference if needed
