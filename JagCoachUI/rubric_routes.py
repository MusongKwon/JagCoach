from flask import Blueprint, request, current_app, jsonify, session
import os
from JagCoachUI.services.LLM import custom_evaluate_speech

rubric_bp = Blueprint("rubric", __name__)

@rubric_bp.route("/rubric-evaluate", methods=["POST"])
def evaluate():
    rubric_file = request.files.get("rubric_file")
    print(rubric_file)
    if rubric_file:
        rubric_upload_folder = current_app.config["UPLOAD_FOLDER"]
        rubric_file_path = os.path.join(rubric_upload_folder, "uploaded_rubric.csv")

        if os.path.exists(rubric_file_path):
            os.remove(rubric_file_path)
        rubric_file.save(rubric_file_path)

    # Get transcript and evaluation from session
    transcription_text = session.get("transcript", "")
    student_results = session.get("evaluation", "")

    # Run comparison using your LLM method
    evaluation_text = custom_evaluate_speech(student_results, rubric_file_path, transcription_text)
    print(evaluation_text)

    return jsonify({"custom_evaluation": evaluation_text})
