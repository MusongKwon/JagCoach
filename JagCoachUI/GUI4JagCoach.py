from flask import Flask, render_template, request
import os
from JagCoachUI.MP4toWAV import convert_mp4_to_wav
import sys
sys.stdout.flush()


app = Flask(__name__)

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the file from the form
        file = request.files.get("video_file")
        if file:
            file = request.files.get("video_file")
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            wav_path = os.path.splitext(file_path)[0] + ".wav"

            print(f"File received: {file_path}", flush=True)  # Debugging print statement
            print("Calling convert_mp4_to_wav", flush=True)  # Debugging print statement

            try:
                convert_mp4_to_wav(file_path, wav_path)
                print(f"Conversion done, file saved at: {wav_path}")  # Debugging print
            except Exception as e:
                print(f"Error during conversion: {e}", flush=True)

            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!", file_path=file_path)

    return render_template("index.html", message=None)

if __name__ == "__main__":
    # Ensure upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host="0.0.0.0", port=5000, debug=True)