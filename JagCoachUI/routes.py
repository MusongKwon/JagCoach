from flask import Blueprint, render_template, request, current_app, jsonify, redirect, session
import os
from JagCoachUI.services.JagCoachFileAnalysis import process_video, get_elements, get_feedback
from JagCoachUI.services.FaceAnalysis import analyze_face
from JagCoachUI.services.WhisperCall import get_transcript
from JagCoachUI.services.FillerWords import get_filler_word_ratio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from firebase_admin import auth as firebase_auth
from firebase.firebase_utils import retrieve_evals, upload_video_to_firebase, save_transcript, save_eval, retrieve_eval, get_next_filename, delete_upload

processed_audio_path = ""
filler_ratio = 0.0
executor = ThreadPoolExecutor(max_workers=2)
process_executor = ProcessPoolExecutor(max_workers=1)
processing_results = {}
user_email=""
next_filename=""

main_bp = Blueprint("main", __name__)

@main_bp.route("/auth")
def auth():
    return render_template("auth.html")

@main_bp.route("/sessionLogin", methods=["POST", "GET"])
def session_login():
    try:
        data = request.get_json()
        id_token = data.get("idToken")
        if not id_token:
            return jsonify({"error": "Missing ID token"}), 400

        decoded_token = firebase_auth.verify_id_token(id_token)
        session["firebase_user"] = id_token
        print("User authenticated:", decoded_token.get("email"))
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error verifying ID token:", e)
        return jsonify({"error": str(e)}), 401

@main_bp.route("/", methods=["GET", "POST"])
def index():

    id_token = session.get("firebase_user")
    if not id_token:
        return redirect("/auth")
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)

        print("Logged-in user email:", decoded_token.get("email"))
        global user_email
        user_email = decoded_token.get("email")
        # Optionally, grab user info here: decoded_token["email"], etc.
        if request.method == "POST":
            file = request.files.get("video_file")
            if file:
                upload_folder = current_app.config["UPLOAD_FOLDER"]

                file_ext = os.path.splitext(file.filename)[1].lower()
                file_path = os.path.join(upload_folder, f"uploaded_usr_video{file_ext}")

                if os.path.exists(file_path):
                    os.remove(file_path)
                    #print(f"Existing file '{file_path}' deleted.")

                try:
                    file.save(file_path)
                    #print(f"Video uploaded successfully: {file_path}")
                except Exception as e:
                    print(f"Error saving file: {e}")

                global processed_audio_path
                # time.sleep(2)  # Wait for 2 seconds before processing the file
                processed_audio_path = process_video(file_path)
                # DEBUG STATEMENTS
                if processed_audio_path and os.path.exists(processed_audio_path):
                    print("Processed audio path:", processed_audio_path)
                else:
                    print("Error: Processed audio file was not found at", processed_audio_path)

                processing_results["voice_analysis"] = process_executor.submit(get_elements, processed_audio_path)
                processing_results["face_analysis"] = executor.submit(analyze_face, file_path)

                uploads_dir = os.path.join(current_app.root_path, 'uploads')
                video_filename = 'uploaded_usr_video.mp4'
                video_path = os.path.abspath(os.path.join(uploads_dir, video_filename))
                # --- New naming logic ---
                global next_filename
                next_filename = get_next_filename(decoded_token['email'])

                firebase_video_url = upload_video_to_firebase(
                    video_path,
                    f"videos/{decoded_token['email']}/{next_filename}"
                )
                print("Video uploaded to Firebase:", firebase_video_url)

                return jsonify({"message": f"File '{file.filename}' uploaded successfully!"})
        return render_template("index.html", message=None)
    except Exception as e:
        print("Token verification failed:", e)
        return redirect("/auth")

@main_bp.route("/transcribe", methods=["POST"])
def transcribe():
    print(f"[PID {os.getpid()}] Transcribe has been summoned")
    try:
        global processed_audio_path

        transcription_text = get_transcript(processed_audio_path)
        global filler_ratio
        filler_ratio = get_filler_word_ratio(transcription_text)
        print("filler ratio: ", filler_ratio)

        print("Transcription complete bossman")
        save_transcript(user_email, transcription_text, next_filename)
        session["transcript"] = transcription_text
        return jsonify({"transcription": transcription_text})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        global filler_ratio

        future = processing_results.get("face_analysis")
        voice_analysis_future = processing_results.get("voice_analysis")


        if future:
            emotion_ratio, eye_contact_ratio = future.result()

        if voice_analysis_future:
            elements = voice_analysis_future.result()

        student_results = get_feedback(emotion_ratio, eye_contact_ratio, elements, filler_ratio)
        session["evaluation"] = student_results

        save_eval(user_email, student_results, next_filename)
        return jsonify({"evaluation": student_results})
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route("/profile")
def profile():
    id_token = session.get("firebase_user")
    if not id_token:
        print("Session expired or missing.")
        return redirect("/auth")

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        user_email = decoded_token.get("email")
        username = user_email.split("@")[0]

        print("Loading profile for user:", user_email)

        db_results = retrieve_evals(user_email)
        print("Retrieved evals:", db_results)

        history = []
        for item in db_results:
            history.append({
                "date": item.get("doc_id")[:6],
                "final_grade": item.get("final_grade") if item.get("final_grade") else 0,  # use extracted grade
                "id": item.get("doc_id"),
                "word_count": len(item.get("transcript", "").split()) if item.get("transcript") else 0,
                "video_length": "Unknown",
                "highlight_feedback": item.get("evaluation", "")[:60] + "..." if item.get("evaluation") else "",
                "video_title": item.get("doc_id")
            })

        return render_template(
            "profile.html",
            user={"username": username, "email": user_email},
            history=history
        )
    except Exception as e:
        print("[PROFILE ERROR] Exception during profile load:", e)
        import traceback
        traceback.print_exc()
        return redirect("/auth")


@main_bp.route("/delete_upload", methods=["POST"])
def delete_upload_route():
    try:
        id_token = session.get("firebase_user")
        if not id_token:
            return jsonify({"error": "User not authenticated"}), 401

        decoded_token = firebase_auth.verify_id_token(id_token)
        user_email = decoded_token.get("email")

        data = request.get_json()
        filename = data.get("filename")

        if not filename:
            return jsonify({"error": "Missing filename"}), 400

        success = delete_upload(user_email, filename)
        if success:
            return jsonify({"message": "Upload deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete upload"}), 500
    except Exception as e:
        print("Error deleting upload:", e)
        return jsonify({"error": str(e)}), 500

@main_bp.route("/get_presentation_details/<filename>")
def get_presentation_details(filename):
    id_token = session.get("firebase_user")
    if not id_token:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        global user_email

        result_list = retrieve_eval(user_email, filename)
        if not result_list or not isinstance(result_list, list):
            return jsonify({"error": "No data found"}), 404

        result = result_list[0]  # Get the first result dict

        return jsonify({
            "video_url": result.get("video_url", ""),
            "transcript": result.get("transcript", ""),
            "evaluation": result.get("evaluation", "")
        })

    except Exception as e:
        print("Error in get_presentation_details:", e)
        return jsonify({"error": str(e)}), 500

@main_bp.route("/present-live", methods=["GET"])
def present_live():
    return render_template("present_live.html")

@main_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/auth")

@main_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@main_bp.route("/upload-rubric", methods=["GET"])
def upload_rubric():
    transcript = session.get("transcript", "")
    student_results = session.get("evaluation", "")
    return render_template("rubric.html", transcript=transcript, student_results=student_results)
