from flask import Blueprint, render_template, request, current_app, jsonify
import os

from services.file_analysis import process_video
from services.whisper_call import transcript

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("video_file")
        if file:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)

            # this part extracts the video extension (.mp4, .avi, etc...)

            file_ext = os.path.splitext(file.filename)[1].lower()
            # Use Flask's config for the upload path
            file_path = os.path.join(upload_folder, f"uploaded_usr_video{file_ext}")
            file.save(file_path) # think this part overrites. If I have written this correctly it does just that.s
            print(f"Video uploaded successfully: {file_path}")
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)

#### This portion is the Transcribing part I figured I could copy the same structure of what is above
@main_bp.route("/transcribe", methods=["POST"])
def transcribe():
    # Takes care of the video requests
    file = request.files.get("video_file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        wav_file = process_video(file_path)  # Convert to WAV
        transcription_text = transcript(wav_file)  # Call correct function
        return jsonify({"transcription": transcription_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
