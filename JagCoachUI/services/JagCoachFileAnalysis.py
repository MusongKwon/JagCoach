import os
from pydub import AudioSegment
from audio_extract import extract_audio
from JagCoachUI.config import config
mysp = __import__("my-voice-analysis")
from io import StringIO
import sys
import json

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Use configured audio output directory
    output_dir = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
    #os.makedirs(output_dir, exist_ok=True)

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
    c = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
    output_txt = os.path.join(c, f"{p}_analysis.txt")
    #print(c + p)

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
    
def get_elements_dictionary(txt_file_path):
    # Generate output JSON file path by replacing .txt with .json
    json_file_path = os.path.splitext(txt_file_path)[0] + ".json"

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
        print(f"Existing file '{json_file_path}' deleted.")

    upload_folder = os.path.join(os.getcwd(), config.UPLOAD_FOLDER, "processed_audio")
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
        with open(txt_file_path, 'r') as file:
            content = file.read()

            if "mood of speech: " in content:
                start_index = content.find("mood of speech: ") + len("mood of speech: ")
                end_index = content.find(",", start_index)
                mood = content[start_index:end_index].strip()
                if mood == "Showing no emotion":
                    student_results["mood"] = 0
                elif mood == "Reading":
                    student_results["mood"] = 8
                elif mood:
                    student_results["mood"] = 16
            
            if "Pronunciation_posteriori_probability_score_percentage= :" in content:
                start_index = content.find("Pronunciation_posteriori_probability_score_percentage= :") + len(
                    "Pronunciation_posteriori_probability_score_percentage= :")
                pronunciation_response = float(content[start_index:].split()[0])
                if student_results["mood"] == None:
                    if pronunciation_response >= 95:
                        student_results["pronunciation_score"] = 24
                    elif pronunciation_response >= 90:
                        student_results["pronunciation_score"] = 21
                    elif pronunciation_response >= 80:
                        student_results["pronunciation_score"] = 18
                    elif pronunciation_response >= 75:
                        student_results["pronunciation_score"] = 12
                    elif pronunciation_response >= 70:
                        student_results["pronunciation_score"] = 6
                    else:
                        student_results["pronunciation_score"] = 0
                else:
                    if pronunciation_response >= 95:
                        student_results["pronunciation_score"] = 20
                    elif pronunciation_response >= 90:
                        student_results["pronunciation_score"] = 18
                    elif pronunciation_response >= 80:
                        student_results["pronunciation_score"] = 15
                    elif pronunciation_response >= 75:
                        student_results["pronunciation_score"] = 10
                    elif pronunciation_response >= 70:
                        student_results["pronunciation_score"] = 5
                    else:
                        student_results["pronunciation_score"] = 0
                
            if "rate_of_speech= " in content:
                start_index = content.find("rate_of_speech= ") + len("rate_of_speech= ")
                speech_rate_response = float(content[start_index:].split()[0])
                if student_results["mood"] == None:
                    if speech_rate_response == 4.0:
                        student_results["speech_rate"] = 12
                    elif speech_rate_response == 3.0:
                        student_results["speech_rate"] = 7
                    else:
                        student_results["speech_rate"] = 0
                else:
                    if speech_rate_response == 4.0:
                        student_results["speech_rate"] = 10
                    elif speech_rate_response == 3.0:
                        student_results["speech_rate"] = 6
                    else:
                        student_results["speech_rate"] = 0
            
            if "articulation_rate= " in content:
                start_index = content.find("articulation_rate= ") + len("articulation_rate= ")
                articulation_rate_result = float(content[start_index:].split()[0])
                if student_results["mood"] == None:
                    if articulation_rate_result == 5.0:
                        student_results["articulation_rate"] = 20
                    elif articulation_rate_result == 4.0:
                        student_results["articulation_rate"] = 14
                    elif articulation_rate_result == 3.0 or articulation_rate_result == 6.0:
                        student_results["articulation_rate"] = 6
                    else:
                        student_results["articulation_rate"] = 0
                else:
                    if articulation_rate_result == 5.0:
                        student_results["articulation_rate"] = 17
                    elif articulation_rate_result == 4.0:
                        student_results["articulation_rate"] = 11
                    elif articulation_rate_result == 3.0 or articulation_rate_result == 6.0:
                        student_results["articulation_rate"] = 5
                    else:
                        student_results["articulation_rate"] = 0

            if "balance= " in content:
                start_index = content.find("balance= ") + len("balance= ")
                balance_response = float(content[start_index:].split()[0])
                if student_results["mood"] == None:
                    if balance_response == 0.8 or balance_response == 0.9:
                        student_results["speaking_ratio"] = 20
                    elif balance_response == 0.7:
                        student_results["speaking_ratio"] = 15
                    elif balance_response == 0.6 or balance_response == 1.0:
                        student_results["speaking_ratio"] = 10
                    elif balance_response == 0.5:
                        student_results["speaking_ratio"] = 6
                    else:
                        student_results["speaking_ratio"] = 0
                else:
                    if balance_response == 0.8 or balance_response == 0.9:
                        student_results["speaking_ratio"] = 17
                    elif balance_response == 0.7:
                        student_results["speaking_ratio"] = 12
                    elif balance_response == 0.6 or balance_response == 1.0:
                        student_results["speaking_ratio"] = 8
                    elif balance_response == 0.5:
                        student_results["speaking_ratio"] = 5
                    else:
                        student_results["speaking_ratio"] = 0
    except Exception as e:
        print(f"Error reading analysis file: {e}")
        return None

    try:
        with open(filler_file_path, 'r') as file:
            content = file.read()

        if "filler_word_ratio= " in content:
            start_index = content.find("filler_word_ratio= ") + len("filler_word_ratio= ")
            filler_word_response = round(float(content[start_index:].split()[0]), 2)
            if student_results["mood"] == None:
                if filler_word_response >= 0.97:
                    student_results["filler_word_ratio"] = 24
                elif filler_word_response >= 0.95:
                    student_results["filler_word_ratio"] = 18
                elif filler_word_response >= 0.90:
                    student_results["filler_word_ratio"] = 12
                elif filler_word_response >= 0.85:
                    student_results["filler_word_ratio"] = 6
                else:
                    student_results["filler_word_ratio"] = 0
            else:
                if filler_word_response >= 0.97:
                    student_results["filler_word_ratio"] = 20
                elif filler_word_response >= 0.95:
                    student_results["filler_word_ratio"] = 15
                elif filler_word_response >= 0.90:
                    student_results["filler_word_ratio"] = 10
                elif filler_word_response >= 0.85:
                    student_results["filler_word_ratio"] = 5
                else:
                    student_results["filler_word_ratio"] = 0
    except Exception as e:
        print(f"Error reading filler words file: {e}")
        return None

    # Calculate the final grade based on the individual scores
    if student_results["mood"] == None:
        student_results["final_grade"] = student_results["pronunciation_score"] + student_results["speech_rate"] + student_results["articulation_rate"] + student_results["speaking_ratio"] + student_results["filler_word_ratio"]
    else:
        student_results["final_grade"] = student_results["mood"] + student_results["pronunciation_score"] + student_results["speech_rate"] + student_results["articulation_rate"] + student_results["speaking_ratio"] + student_results["filler_word_ratio"]

    # Create the final JSON structure
    json_data = {"student_results": student_results}

    # Write to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"JSON file '{json_file_path}' created successfully.")
    return json_file_path
