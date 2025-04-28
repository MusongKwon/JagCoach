from flask import Blueprint, render_template, request, current_app, jsonify
import os
from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements, get_elements_dictionary
from JagCoachUI.services.FaceAnalysis import analyze_face
from JagCoachUI.services.LLM import evaluate_speech
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.services.FillerWords import get_filler_word_ratio
from JagCoachUI.config import config
from concurrent.futures import ThreadPoolExecutor
import re

processed_audio_path = ""
filler_ratio = 0.0
executor = ThreadPoolExecutor(max_workers=2)
processing_results = {}

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        file = request.files.get("video_file")
        if file:
            upload_folder = current_app.config["UPLOAD_FOLDER"]

            file_ext = os.path.splitext(file.filename)[1].lower()
            file_path = os.path.join(upload_folder, f"uploaded_usr_video{file_ext}")

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Existing file '{file_path}' deleted.")

            try:
                file.save(file_path)
                print(f"Video uploaded successfully: {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
            print(f"Video uploaded successfully: {file_path}")

            global processed_audio_path
            processed_audio_path = process_video(file_path)

            processing_results["face_analysis"] = executor.submit(analyze_face, file_path)

            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)


# This portion will help restructure the format of the transcript look

def split_transcription(text):
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def get_transcript_metadata(text):
    sentences = split_transcription(text)
    return {
        "line_count": len(sentences),
        "word_count": len(text.split())
    }


# Below I added the lines to add the above implementation to format the transcript.
@main_bp.route("/transcribe", methods=["POST"])
def transcribe():
    print("Transcribe has been summoned")
    try:
        global processed_audio_path
        transcription_text = get_transcript(processed_audio_path)

        sentences = split_transcription(transcription_text)
        metadata = get_transcript_metadata(transcription_text)

        global filler_ratio
        filler_ratio = get_filler_word_ratio(transcription_text)

        print("Transcription complete bossman")
        return jsonify({
            "lines": sentences,
            "metadata": metadata,
            "filler_ratio": filler_ratio
        })
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500



# Strictly mock data. This will change once a database is added.
@main_bp.route("/evaluate", methods=["POST"])
def evaluate():
    print(f"Evaluate has been summoned")
    try:
        global processed_audio_path
        global filler_ratio
        elements = get_elements(processed_audio_path)

        future = processing_results.get("face_analysis")
        if future:
            emotion_ratio, eye_contact_ratio = future.result()
        else:
            emotion_ratio, eye_contact_ratio = 0.0, 0.0

        student_results = get_elements_dictionary(emotion_ratio, eye_contact_ratio, elements, filler_ratio)
        print(student_results)

        print("Starting Evaluation")
        evaluation_text = evaluate_speech(student_results)
        print("Evaluation complete bossman")
        return jsonify({"evaluation": evaluation_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route("/profile")
def profile():
    class DummyUser:
        username = "Redhouse"
        email = "redhouse@example.com"

    dummy_history = [
        {"date": "2025-04-27", "final_grade": 90, "id": 1, "word_count": 1200, "video_length": "9:24",
         "highlight_feedback": "Strong delivery, clear pronunciation.", "video_title": "Final Project Presentation"},
        {"date": "2025-04-20", "final_grade": 85, "id": 2, "word_count": 950, "video_length": "7:15",
         "highlight_feedback": "Good effort, needs better pacing and eye contact.",
         "video_title": "Practice Session 1"},

        # Just duplicate or make variations
        {"date": "2025-04-15", "final_grade": 78, "id": 3, "word_count": 870, "video_length": "8:03",
         "highlight_feedback": "Speech rate was too fast.", "video_title": "Mid-Term Update"},
        {"date": "2025-04-10", "final_grade": 92, "id": 4, "word_count": 1300, "video_length": "10:12",
         "highlight_feedback": "Excellent use of pauses and facial expression.", "video_title": "Demo Day Pitch"},
        {"date": "2025-04-05", "final_grade": 88, "id": 5, "word_count": 1100, "video_length": "8:50",
         "highlight_feedback": "Minor pronunciation issues.", "video_title": "Weekly Team Update"},
        {"date": "2025-04-01", "final_grade": 76, "id": 6, "word_count": 900, "video_length": "7:30",
         "highlight_feedback": "Good energy but rushed ending.", "video_title": "Introductory Speech"},
        {"date": "2025-03-28", "final_grade": 83, "id": 7, "word_count": 950, "video_length": "7:55",
         "highlight_feedback": "Good structure, filler words used.", "video_title": "Module Review"},
        {"date": "2025-03-22", "final_grade": 80, "id": 8, "word_count": 890, "video_length": "7:40",
         "highlight_feedback": "Clear articulation but pacing varied.", "video_title": "First Presentation"},
        {"date": "2025-04-15", "final_grade": 78, "id": 3, "word_count": 870, "video_length": "8:03",
         "highlight_feedback": "Speech rate was too fast.", "video_title": "Mid-Term Update"},
        {"date": "2025-04-10", "final_grade": 92, "id": 4, "word_count": 1300, "video_length": "10:12",
         "highlight_feedback": "Excellent use of pauses and facial expression.", "video_title": "Demo Day Pitch"},
        {"date": "2025-04-05", "final_grade": 88, "id": 5, "word_count": 1100, "video_length": "8:50",
         "highlight_feedback": "Minor pronunciation issues.", "video_title": "Weekly Team Update"},
        {"date": "2025-04-01", "final_grade": 76, "id": 6, "word_count": 900, "video_length": "7:30",
         "highlight_feedback": "Good energy but rushed ending.", "video_title": "Introductory Speech"},
        {"date": "2025-03-28", "final_grade": 83, "id": 7, "word_count": 950, "video_length": "7:55",
         "highlight_feedback": "Good structure, filler words used.", "video_title": "Module Review"},
        {"date": "2025-03-22", "final_grade": 80, "id": 8, "word_count": 890, "video_length": "7:40",
         "highlight_feedback": "Clear articulation but pacing varied.", "video_title": "First Presentation"},
    ]
    return render_template(
        "profile.html",
        user=DummyUser(),
        history=dummy_history
    )