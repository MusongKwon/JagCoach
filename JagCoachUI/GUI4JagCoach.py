from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the file from the form
        file = request.files.get("video_file")
        if file:
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            return render_template("index.html", message=f"File '{file.filename}' uploaded successfully!", file_path=file_path)
    return render_template("index.html", message=None)

if __name__ == "__main__":
    # Ensure upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host="0.0.0.0", port=5000, debug=True)
