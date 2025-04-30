from flask import Blueprint, render_template, request, current_app, jsonify
import os
from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements, get_feedback
from JagCoachUI.services.FaceAnalysis import analyze_face
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.services.FillerWords import get_filler_word_ratio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

processed_audio_path = ""
filler_ratio = 0.0
executor = ThreadPoolExecutor(max_workers=2)
process_executor = ProcessPoolExecutor(max_workers=1)
processing_results = {}

main_bp = Blueprint("main", __name__)

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

            try:
                file.save(file_path)
            except Exception as e:
                print(f"Error saving file: {e}")

            global processed_audio_path
            processed_audio_path = process_video(file_path)

            processing_results["voice_analysis"] = process_executor.submit(get_elements, processed_audio_path)
            processing_results["face_analysis"] = executor.submit(analyze_face, file_path)
            
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)

@main_bp.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        global processed_audio_path
        transcription_text = get_transcript(processed_audio_path)

        global filler_ratio
        filler_ratio = get_filler_word_ratio(transcription_text)

        return jsonify({"transcription": transcription_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        global filler_ratio

        future = processing_results.get("face_analysis")
        voice_analysis_future = processing_results.get("voice_analysis")
        if future:
            emotion_ratio, eye_contact_ratio = future.result()

        if voice_analysis_future:
            elements = voice_analysis_future.result()

        student_results = get_feedback(emotion_ratio, eye_contact_ratio, elements, filler_ratio)

        return jsonify({"evaluation": student_results})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500
    
@main_bp.route("/present-live", methods=["GET"])
def present_live():
    return render_template("present_live.html")
