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
