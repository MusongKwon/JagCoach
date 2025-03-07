from flask import Blueprint, render_template, request, current_app, jsonify
import os

from services.file_analysis import process_video
from services.whisper_call import transcript

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("video_file")
        if file:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)

            file_ext = os.path.splitext(file.filename)[1].lower()
            file_path = os.path.join(upload_folder, f"uploaded_usr_video{file_ext}")
            file.save(file_path)
            print(f"Video uploaded successfully: {file_path}")
            processed_audio_path = process_video(file_path) # variable is not used. I had to call it here so it would
            # actually create the process_video subdirectory
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)

# This portion is the Transcribing part I figured I could copy the same structure of what is above
# What is changed is this now just looks for the .wav file. Before it was set up it was processing the video twice
# when already the file_analysis.py file was already doing that. So this just transcribes now and does not create the
# .wav file now. That function has been moved to file_analysis.py
@main_bp.route("/transcribe", methods=["POST"])
def transcribe():

    print(f"Transcribe has been summoned")
    processed_audio_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "processed_audio")

    try:
        wav_file = max(
            [os.path.join(processed_audio_folder, f) for f in os.listdir(processed_audio_folder) if f.endswith(".wav")],
            key=os.path.getctime
        )
        print("Begin looking for the wav file\n-------------------------")
        print(f"Found it boss: {wav_file}")
        transcription_text = transcript(wav_file)
        print("Transcription complete bossman")
        return jsonify({"transcription": transcription_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500
