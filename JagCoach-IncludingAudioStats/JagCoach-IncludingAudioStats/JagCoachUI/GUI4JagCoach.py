from flask import Flask, render_template, request, send_from_directory, url_for
import os
import sys
from JagCoachFileAnalysis import process_video, get_elements_dictionary, get_elements
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

            print(f"File received: {file_path}", flush=True)  # Debugging print statement
            print("Calling process_video", flush=True)  # Debugging print statement

            try:
                wav_file = process_video(file_path)
                wav_path = os.path.abspath(wav_file)
                print(f"Conversion done, file saved at: {wav_path}")  # Debugging print
                print(f"File processed: {wav_file}")
                txt_file = get_elements(wav_file)
                elements = get_elements_dictionary(txt_file)
                if not elements:
                    elements = "No elements detected"
                print(f"Info extracted from: {wav_file}")
                print(f"Extracted elements: {elements}")  # Debugging print
                return render_template("index.html", message="File uploaded and processed!", file_path=url_for('uploaded_file', filename=file.filename),
                       elements=elements)
            except Exception as e:
                print(f"Error during conversion: {e}", flush=True)

            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!", file_path=file_path)

    return render_template("index.html", message=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

if __name__ == "__main__":
    # Ensure upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host="0.0.0.0", port=5000, debug=True)
