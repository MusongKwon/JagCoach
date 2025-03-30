from flask import Blueprint, render_template, request, current_app, jsonify
import os
from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements
from JagCoachUI.services.LLM import evaluate_speech
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.services.FillerWords import get_filler_word_ratio
from JagCoachUI.config import config

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

            processed_audio_path = process_video(file_path)            

            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)


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

        transcription_text = get_transcript(wav_file)
        get_filler_word_ratio(transcription_text)

        print("Transcription complete bossman")
        return jsonify({"transcription": transcription_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route("/evaluate", methods=["POST"])
def evaluate():
    print(f"Evaluate has been summoned")
    processed_audio_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "processed_audio")
    try:
        wav_file = max(
            [os.path.join(processed_audio_folder, f) for f in os.listdir(processed_audio_folder) if f.endswith(".wav")],
            key=os.path.getctime
        )

        #test()
        print("Begin looking for the wav file\n-------------------------")
        print(f"Found it boss: {wav_file}")
        txt_file = get_elements(wav_file)

        print("Starting Evaluation")
        evaluation_text = evaluate_speech()
        print("Evaluation complete bossman")
        return jsonify({"evaluation": evaluation_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500
