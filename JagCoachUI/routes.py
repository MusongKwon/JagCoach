from flask import Blueprint, render_template, request, current_app, jsonify
import os

from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements, get_elements_dictionary
from JagCoachUI.services.LLM import evaluate_speech
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.config import config

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("video_file")
        if file:
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            #os.makedirs(upload_folder, exist_ok=True)

            file_ext = os.path.splitext(file.filename)[1].lower()
            file_path = os.path.join(upload_folder, f"uploaded_usr_video{file_ext}")
            try:
                file.save(file_path)
                print(f"Video uploaded successfully: {file_path}")  # Debugging print
            except Exception as e:
                print(f"Error saving file: {e}")
            print(f"Video uploaded successfully: {file_path}")
            processed_audio_path = process_video(file_path)
            audio_txt_path = get_elements(processed_audio_path)
            transcription_text_path = get_transcript(processed_audio_path)
            audio_json_path = get_elements_dictionary(audio_txt_path)
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)


@main_bp.route("/transcribe", methods=["POST"])
def transcribe():
    print(f"Transcribe has been summoned")
    transcripts_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "transcripts")

    try:
        txt_file = max(
            [os.path.join(transcripts_folder, f) for f in os.listdir(transcripts_folder) if f.endswith(".txt")],
            key=os.path.getctime
        )

        print("Begin looking for the wav file\n-------------------------")
        print(f"Found it boss: {txt_file}")

        with open(txt_file, "r") as f:
            transcription_text = f.read()

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
        json_file = max(
            [os.path.join(processed_audio_folder, f) for f in os.listdir(processed_audio_folder) if f.endswith("analysis.json")],
            key=os.path.getctime
        )
        optimal_file = max(
            [os.path.join(processed_audio_folder, f) for f in os.listdir(processed_audio_folder) if f.endswith("metrics.json")],
            key=os.path.getctime
        )

        print("Begin looking for the json file\n-------------------------")
        print(f"Found it boss: {json_file}")
        print("Begin looking for the optimal file\n-------------------------")
        print(f"Found it boss: {optimal_file}")
        evaluation_text = evaluate_speech(json_file,optimal_file)
        print("Evaluation complete bossman")
        return jsonify({"evaluation": evaluation_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500
