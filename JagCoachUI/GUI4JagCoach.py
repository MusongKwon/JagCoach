from flask import Flask, render_template, request
import os
from JagCoachUI.MP4toWAV import convert_all_mp4_to_wav
import sys

sys.stdout.flush()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the file from the form
        file = request.files.get("video_file")
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            print(f"File received: {file_path}", flush=True)  # Debugging print statement
            print("Calling convert_mp4_to_wav", flush=True)  # Debugging print statement

        processed_files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.endswith(".mp4"):
                mp4_path = os.path.join(UPLOAD_FOLDER, filename)
                wav_path = os.path.splitext(UPLOAD_FOLDER)[0] + ".wav"

                print(f"Processing: {mp4_path}", flush=True)

            try:
                convert_all_mp4_to_wav(mp4_path, wav_path)
                processed_files.append(wav_path)
                print(f"Conversion done, {wav_path}", flush=True)  # Debugging print
            except Exception as e:
                print(f"Error during conversion {mp4_path}: {e}", flush=True)

            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!", file_path=file_path)

    return render_template("index.html", message=None)

if __name__ == "__main__":
    # Ensure upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host="0.0.0.0", port=5000, debug=True)
