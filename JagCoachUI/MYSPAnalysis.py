import os
from JagCoachUI.config import config  # 🔹 Import centralized config settings

mysp = __import__("my-voice-analysis")
from io import StringIO
import sys

# mysp functions print, so we need to create a text file to capture the output
def get_elements(file_path):
    print(f"Reading {file_path}")
    p = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    c = os.getcwd() + os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    print(p)
    print(c)
    output_txt = os.path.join(c, f"{p}_analysis.txt")
    print(output_txt)

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


def get_pauses(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()

            # Search for the line with "number_of_pauses="
            if "number_of_pauses= " in content:
                # Extract the value after "number_of_pauses="
                start_index = content.find("number_of_pauses= ") + len("number_of_pauses= ")
                pause_value = content[start_index:].split()[0]  # Get the number and split in case there are other words

                # Convert to float (double in Python)
                return float(pause_value)
            else:
                raise ValueError("The 'number_of_pauses' value not found in the file.")

    except Exception as e:
        print(f"Error while extracting pauses: {e}")
        return None


def get_mood(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()

            # Search for the line with "mood="
            if "mood of speech: " in content:
                start_index = content.find("mood of speech: ") + len("mood of speech: ")
                end_index = content.find(",", start_index)
                mood = content[start_index:end_index].strip()
                if mood == "Showing no emotion":
                    mood_value = 1.0
                elif mood == "Reading":
                    mood_value = 2.0
                else:
                    mood_value = 3.0
                return mood_value
            else:
                raise ValueError("The 'mood' value not found in the file.")

    except Exception as e:
        print(f"Error while extracting mood: {e}")
        return None


def get_pronunciation_score(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()

            if "Pronunciation_posteriori_probability_score_percentage= :" in content:
                start_index = content.find("Pronunciation_posteriori_probability_score_percentage= :") + len(
                    "Pronunciation_posteriori_probability_score_percentage= :")
                pronunciation_score = content[start_index:].split()[0]
                return float(pronunciation_score)
            else:
                raise ValueError("The 'pronunciation_score' value not found in the file.")
    except Exception as e:
        print(f"Error while extracting pronunciation score: {e}")
        return None


def get_speech_rate(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()
            if "rate_of_speech= " in content:
                start_index = content.find("rate_of_speech= ") + len("rate_of_speech= ")
                speech_rate = content[start_index:].split()[0]
                return float(speech_rate)
    except Exception as e:
        print(f"Error while extracting speech rate: {e}")
        return None


def get_articulation_rate(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()
            if "articulation_rate= " in content:
                start_index = content.find("articulation_rate= ") + len("articulation_rate= ")
                articulation_rate = content[start_index:].split()[0]
                return float(articulation_rate)
    except Exception as e:
        print(f"Error while extracting articulation rate: {e}")
        return None


def get_speaking_ratio(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()
            if "balance= " in content:
                start_index = content.find("balance= ") + len("balance= ")
                speaking_ratio = content[start_index:].split()[0]
                return float(speaking_ratio)
    except Exception as e:
        print(f"Error while extracting speaking ratio: {e}")
        return None


def get_elements_dictionary(txt_file_path):
    # Initialize the dictionary with default values
    elements_dictionary = {
        "mood": None,
        "pronunciation score": None,
        "speech rate": None,
        "articulation rate": None,
        "speaking ratio": None,
        "number of pauses": None
    }

    # Fill in the dictionary with extracted values
    try:
        elements_dictionary["mood"] = get_mood(txt_file_path)
        elements_dictionary["pronunciation score"] = get_pronunciation_score(txt_file_path)
        elements_dictionary["speech rate"] = get_speech_rate(txt_file_path)
        elements_dictionary["articulation rate"] = get_articulation_rate(txt_file_path)
        elements_dictionary["speaking ratio"] = get_speaking_ratio(txt_file_path)
        elements_dictionary["number of pauses"] = get_pauses(txt_file_path)

        return elements_dictionary

    except Exception as e:
        print(f"Error while extracting elements: {e}")
        return None
