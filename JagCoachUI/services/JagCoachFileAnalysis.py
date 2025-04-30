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
        #print(f"Existing file '{output_path}' deleted.")

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
    
    original_stdout = sys.stdout  # Save the original stdout
    sys.stdout = output_capture = StringIO()  # Redirect stdout to a string buffer

    try:
        mysp.myspgend(p, c)
        mysp.mysppron(p, c)
        mysp.myspsr(p, c)
        mysp.myspatc(p, c)
        mysp.myspbala(p, c)
    finally:
        sys.stdout = original_stdout

    return output_capture.getvalue()
    
PRONUNCIATION_SCORES = {100: 10, 95: 9, 90: 8, 80: 6, 75: 4, 70: 2}
SPEECH_RATE_SCORES = {4.0: 2, 3.0: 1}
ARTICULATION_SCORES = {5.0: 4, 4.0: 2, 3.0: 1, 6.0: 1}
SPEAKING_RATIO_SCORES = {0.8: 4, 0.9: 4, 0.7: 3, 0.6: 2, 1.0: 2, 0.5: 1}
FILLER_WORD_SCORES = {0.98: 10, 0.97: 9, 0.95: 8, 0.90: 6, 0.85: 3, 0.8: 2}
EYE_CONTACT_SCORES = {0.89: 10, 0.8: 8, 0.75: 7, 0.65: 5, 0.55: 3, 0.5: 2}
FACIAL_EXPRESSION_SCORES = {0.6: 10, 0.55: 9, 0.5: 8, 0.45: 7, 0.3: 4, 0.2: 2}

feedback_dictionary = {"Delivery": {10: "Excellent! It was detected that you were speaking passionately. You will likely make a strong impression on your audience.",
                                    5: "Your delivery came off as if you were reading from a script. Try practicing to sound more natural.",
                                    0: "Your delivery was detected as showing no vocal emotion. This can make your presentation less engaging."},
                       "Pronunciation": {10: "You delivered your words clearly and with good articulation, making it easy to understand what you were saying.",
                                         8: "Your articulation was great overall. With a little more practice, your pronunciation could be even clearer.",
                                         4: "Your articulation was somewhat unclear, which may have made it difficult for your audience to understand you.",
                                         0: "Your articulation needs improvement. I suggest focusing on your pronunciation to enhance clarity."},
                       "Speech Rate": {10: "The pace of your speech was steady and even, making your presentation engaging and easy to follow.",
                                       8: "Your speech rate was great overall. A little more practice could help you maintain a more consistent pace.",
                                       4: "Your speech rate was somewhat uneven, which may have make it difficult for your audience to follow.",
                                       0: "The pace of you speech needs improvement. I suggest practicing to speak in a more consistent rate."},
                       "Filler Words Use": {10: "Your conscious effort to minimize filler words was noticeable, making your speech more polished and professional.",
                                             7: "You appeared to be mindful of filler words and managed them well.",
                                             0: "There were some filler words detected in your speech. I suggest practicing to reduce their usage for a more professional tone."},
                       "Facial Expression": {9: "Your facial expressions clearly convey enthusiasm, engagement, and interest in the topic. This will likely help you connect with your audience.",
                                         7: "Your facial expressions were generally engaging. Some practice could help you enhance your expressiveness.",
                                         0: "There were little to no facial expressions detected. I suggest focusing on being more expressive to convey enthusiasm to the audience."},
                       "Eye Contact": {10: "You maintained strong eye contact with the audience, conveying confidence and sincerity in your delivery.",
                                             7: "While you maintained good eye contact, there may have been moments where it felt a bit inconsistent. A little more practice could help you maintain a more consistent level of eye contact.",
                                             0: "Maintaining eye contact with the audience is crucial in conveying confidence in your delivery. I suggest practicing to improve this aspect."}}

strengths_thresholds={"Delivery": 10,"Pronunciation": 8,"Speech Rate": 8,"Filler Words Use": 7,"Facial Expression": 7,"Eye Contact": 7,}

def get_feedback(emotion_ratio, eye_contact_ratio, analysis_string, filler_ratio):
    # Initialize the dictionary with None values
    student_results = {
        "Delivery": None,
        "Pronunciation": None,
        "Speech Rate": None,
        "Filler Words Use": None,
        "Facial Expression": None,
        "Eye Contact": None
    }

    for line in analysis_string.splitlines():
        if match := re.search(r"mood of speech: (.+?),", line):
            mood = match.group(1).strip()
            student_results["Delivery"] = 0 if mood == "Showing no emotion" else (5 if mood == "Reading" else 10)
        elif match := re.search(r"Pronunciation_posteriori_probability_score_percentage= :([\d.]+)", line):
            pronunciation_response = float(match.group(1))
            student_results["Pronunciation"] = next((v for k, v in PRONUNCIATION_SCORES.items() if pronunciation_response >= k), 0)
        elif match := re.search(r"rate_of_speech= ([\d.]+)", line):
            speech_rate = float(match.group(1))
            student_results["Speech Rate"] = next((v for k, v in SPEECH_RATE_SCORES.items() if speech_rate >= k), 0)
        elif match := re.search(r"articulation_rate= ([\d.]+)", line):
            articulation_rate = float(match.group(1))
            student_results["Speech Rate"] += next((v for k, v in ARTICULATION_SCORES.items() if articulation_rate >= k), 0)
        elif match := re.search(r"balance= ([\d.]+)", line):
            speaking_ratio = float(match.group(1))
            student_results["Speech Rate"] += next((v for k, v in SPEAKING_RATIO_SCORES.items() if speaking_ratio >= k), 0)

    student_results["Filler Words Use"] = next((v for k, v in FILLER_WORD_SCORES.items() if filler_ratio >= k), 0)
    if emotion_ratio is not None and eye_contact_ratio is not None:
        student_results["Facial Expression"] = next((v for k, v in FACIAL_EXPRESSION_SCORES.items() if emotion_ratio >= k), 0)
        student_results["Eye Contact"] = next((v for k, v in EYE_CONTACT_SCORES.items() if eye_contact_ratio >= k), 0)

    # Calculate the final grade based on the individual scores
    non_none_values = [v for v in student_results.values() if v is not None]
    count = len(non_none_values)
    score_sum = sum(non_none_values)
    student_results["final_grade"] = int(score_sum / count * 10)
    feedback = f"You scored a {student_results['final_grade']} out of a 100!\n\n"
    
    strengths = {}
    areas_of_improvement = {}

    # divide into strengths and areas of improvement
    for metric, threshold in strengths_thresholds.items():
        if metric in student_results and student_results[metric] is not None:
            # Find the appropriate feedback message based on the score
            feedback_message = next(
                (msg for score, msg in sorted(feedback_dictionary[metric].items(), reverse=True)
                 if student_results[metric] >= score),
                None
            )
            if student_results[metric] >= threshold:
                strengths[metric] = feedback_message
            else:
                areas_of_improvement[metric] = feedback_message

    # Format the feedback
    if strengths:
        feedback += "***Strengths***\n"
        for metric, message in strengths.items():
            feedback += f"- {metric}: {message} (Score: {student_results[metric]}/10)\n"

    if areas_of_improvement:
        feedback += "\n***Areas of Improvement***\n"
        for metric, message in areas_of_improvement.items():
            feedback += f"- {metric}: {message} (Score: {student_results[metric]}/10)\n"
    
    return feedback
