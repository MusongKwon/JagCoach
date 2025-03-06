import os
from pydub import AudioSegment
from audio_extract import extract_audio
from config import config  # 🔹 Import centralized config settings
mysp = __import__("my-voice-analysis")
from io import StringIO
import sys

def process_video(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    # Use configured audio output directory
    output_dir = os.path.join(config.UPLOAD_FOLDER, "processed_audio")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".wav")

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
    c = os.getcwd()+os.path.join(config.UPLOAD_FOLDER, "\\uploads\\processed_audio\\")  # Use config path
    output_txt = os.path.join(c, f"{p}_analysis.txt")

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
        with open(txt_file_path, 'r') as file:
            # Read the file content
            content = file.read()

            # Search for the line with "mood="
            if "mood of speech: " in content:
                start_index = content.find("mood of speech: ") + len("mood of speech: ")
                end_index = content.find(",", start_index)
                mood = content[start_index:end_index].strip()
                if mood == "Showing no emotion":
                    elements_dictionary["mood"] = 1.0
                elif mood == "Reading":
                    elements_dictionary["mood"] = 2.0
                else:
                    elements_dictionary["mood"] = 3.0
            
            if "Pronunciation_posteriori_probability_score_percentage= :" in content:
                start_index = content.find("Pronunciation_posteriori_probability_score_percentage= :") + len("Pronunciation_posteriori_probability_score_percentage= :")
                elements_dictionary["pronunciation score"] = float(content[start_index:].split()[0])

            if "rate_of_speech= " in content:
                start_index = content.find("rate_of_speech= ") + len("rate_of_speech= ")
                elements_dictionary["speech rate"] = float(content[start_index:].split()[0])

            if "articulation_rate= " in content:
                start_index = content.find("articulation_rate= ") + len("articulation_rate= ")
                elements_dictionary["articulation rate"] = float(content[start_index:].split()[0])
            
            if "balance= " in content:
                start_index = content.find("balance= ") + len("balance= ")
                elements_dictionary["speaking ratio"] = float(content[start_index:].split()[0])

            if "number_of_pauses= " in content:
                start_index = content.find("number_of_pauses= ") + len("number_of_pauses= ")
                elements_dictionary["number of pauses"] = float(content[start_index:].split()[0])
            
        return elements_dictionary

    except Exception as e:
        print(f"Error while extracting elements: {e}")
        return None

if __name__ == "__main__":
    test_file = os.path.join(config.UPLOAD_FOLDER, "vid2.mp4")

    try:
        wav_file = process_video(test_file)
        txt_file = get_elements(wav_file)
        print(get_elements_dictionary(txt_file))
        
    except Exception as e:
        print(f"Error: {e}")
