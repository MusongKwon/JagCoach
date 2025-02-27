from flask import Blueprint, render_template, request, current_app
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("video_file")
        if file:
            # Use Flask's config for the upload path
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!",
                                   file_path=file_path)
    return render_template("index.html", message=None)