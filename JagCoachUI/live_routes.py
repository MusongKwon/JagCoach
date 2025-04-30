from flask import Blueprint, request, jsonify, current_app, render_template, session
import os
import shutil
import time
from werkzeug.utils import secure_filename

from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements, get_feedback
from JagCoachUI.services.FaceAnalysis import analyze_face
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.services.FillerWords import get_filler_word_ratio

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from firebase_admin import auth as firebase_auth
from firebase.firebase_utils import upload_video_to_firebase, save_transcript, save_eval, get_next_filename
import subprocess

live_bp = Blueprint("live", __name__)

transcription_accumulator = []
evaluation_accumulator = []
executor = ThreadPoolExecutor(max_workers=2)
process_executor = ProcessPoolExecutor(max_workers=1)
processing_results = {}
filler_ratios = {}
processed_audio_paths = {}

@live_bp.route("/live-index", methods=["POST"])
def live_index():
    file = request.files.get("video_file")
    segment_number = request.form.get("segment_number")

    if file and segment_number is not None:
        segments_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "live_segments")
        os.makedirs(segments_folder, exist_ok=True)

        filename = secure_filename(f"{segment_number}_segment.webm")
        file_path = os.path.join(segments_folder, filename)
        file.save(file_path)
        time.sleep(0.1)

        processed_audio_paths[segment_number] = process_video(file_path)
        processing_results["voice_analysis"] = process_executor.submit(get_elements, processed_audio_paths[segment_number])
        processing_results["face_analysis"] = executor.submit(analyze_face, file_path)
        return "", 200
    return "No file or segment number provided", 400

@live_bp.route("/live-transcribe", methods=["POST"])
def live_transcribe():
    try:
        segment_number = request.form.get("segment_number")
        transcription_text = get_transcript(processed_audio_paths[segment_number])
        filler_ratios[segment_number] = get_filler_word_ratio(transcription_text)
        transcription_accumulator.append(transcription_text)

        return jsonify({"transcription": transcription_accumulator})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@live_bp.route("/live-evaluate", methods=["POST"])
def live_evaluate():
    try:
        segment_number = request.form.get("segment_number")
        voice_analysis_future = processing_results.get("voice_analysis")
        face_analysis_future = processing_results.get("face_analysis")

        if face_analysis_future:
            emotion_ratio, eye_contact_ratio = face_analysis_future.result()

        if voice_analysis_future:
            elements = voice_analysis_future.result()

        student_results = get_feedback(emotion_ratio, eye_contact_ratio, elements, filler_ratios[segment_number])
        evaluation_accumulator.append(student_results)
        return jsonify({"evaluation": student_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@live_bp.route("/live-stop", methods=["POST"])
def live_stop():
    try:
        print("start")
        id_token = session.get("firebase_user")
        print("problem 1")
        decoded_token = firebase_auth.verify_id_token(id_token)
        print("problem 2")
        user_email = decoded_token.get("email")
        print("problem 3")
        next_filename = get_next_filename(decoded_token['email'])
        print("problem 4")

        
        segment_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "live_segments")
        final_output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "final_recording.mp4")
        if os.path.exists(final_output_path):
            os.remove(final_output_path)
        print("problem 5")

        # Get all segment files in order
        segments = sorted(
            [f for f in os.listdir(segment_folder) if f.endswith(".webm")],
            key=lambda name: int(name.split("_")[0])
        )
        print("problem 6")

        concat_list_path = os.path.join(segment_folder, "concat_list.txt")
        with open(concat_list_path, "w") as f:
            for filename in segments:
                segment_path = os.path.join(segment_folder, filename)
                # Convert to intermediate mp4 first
                mp4_path = segment_path.replace(".webm", ".mp4")
                subprocess.run([
                    "ffmpeg", "-y", "-i", segment_path,
                    "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
                    mp4_path
                ])
                f.write(f"file '{os.path.basename(mp4_path)}'\n")
        print("problem 7")

        # Combine all .mp4 files into one
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
            "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
            final_output_path
        ])
        print("problem 8")

        upload_video_to_firebase(final_output_path, f"videos/{decoded_token['email']}/{next_filename}")
        print("problem 9")

        final_transcript = "\n".join(transcription_accumulator)
        final_evaluations = "\n".join(evaluation_accumulator)
        print("problem 10")
        save_transcript(user_email, final_transcript, next_filename)
        save_eval(user_email, final_evaluations, next_filename)
        print("problem 11")
        transcription_accumulator.clear()
        evaluation_accumulator.clear()

        # Clean up
        shutil.rmtree(segment_folder)
        upload_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "processed_audio")
        for file_name in os.listdir(upload_folder):
            if file_name.endswith(".wav") or file_name.endswith(".TextGrid"):
                file_path = os.path.join(upload_folder, file_name)
                os.remove(file_path)
        os.remove(final_output_path)

        return {"message": "Recording complete", "output": "final_recording.mp4"}
    except Exception as e:
        return {"error": str(e)}, 500

@live_bp.route("/upload-video", methods=["GET"])
def upload_video():
    return render_template("index.html")
