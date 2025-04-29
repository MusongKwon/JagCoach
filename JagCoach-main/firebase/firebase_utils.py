import firebase_admin
from firebase_admin import credentials, initialize_app, storage, firestore
from datetime import datetime, timedelta
import os
import re
from datetime import datetime
import os

cred = credentials.Certificate("secrets/firebase-creds.json")

 # Initialize Firebase Admin
firebase_admin.initialize_app(cred, {
    'storageBucket': 'jagcoach-25bd3.firebasestorage.app'  # You can get this from Firebase Console
})

# Get a reference to Firebase Storage
bucket = storage.bucket()

curdate =""

def upload_video_to_firebase(local_path, firebase_path):
    global bucket
    blob = bucket.blob(firebase_path)
    blob.upload_from_filename(local_path)
    blob.make_public()  # Optional: make the URL publicly accessible
    return blob.public_url

def save_transcript(user_email, transcript, next_filename):
    db = firestore.client()
    doc_ref = db.collection("user_presentations").document(user_email).collection("uploads").document(next_filename)
    doc_ref.set({
        "transcript": transcript,
    }, merge=True)  # <- prevent overwriting

def save_eval(user_email, evaluation, next_filename):
    db = firestore.client()
    doc_ref = db.collection("user_presentations").document(user_email).collection("uploads").document(next_filename)
    doc_ref.set({
        "evaluation": evaluation
    }, merge=True)  # <- prevent overwriting

def retrieve_eval(user_email,next_filename):
    try:
        db = firestore.client()
        uploads_ref = db.collection("user_presentations").document(user_email).collection("uploads")
        docs = uploads_ref.stream()

        # Assuming the video is stored with a predictable name like "user_email/doc_id/video.mp4"
        video_path = f"videos/{user_email}/{next_filename}"  # Adjusted path format here
        blob = bucket.blob(video_path)

        video_url = None
        if blob.exists():  # Check if the video exists in Firebase Storage
            print(f"Blob exists for {video_path}")
            # Generate a signed URL for temporary access
            video_url = blob.generate_signed_url(expiration=timedelta(hours=1))
            print(f"Generated video URL: {video_url}")
        else:
            print(f"Video blob does not exist for {video_path}")

        results = []
        for doc in docs:
            data = doc.to_dict()
            doc_id = doc.id
            transcript = data.get("transcript")
            evaluation = data.get("evaluation")

            results.append({
                "doc_id": doc_id,
                "transcript": transcript,
                "evaluation": evaluation,
                "video_url": video_url,  # Include the video URL in the result
            })

        return results
    except Exception as e:
        print(f"Error retrieving evaluations: {e}")
        return []

def retrieve_evals(user_email):
    try:
        db = firestore.client()
        uploads_ref = db.collection("user_presentations").document(user_email).collection("uploads")
        docs = uploads_ref.stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            doc_id = doc.id
            transcript = data.get("transcript")
            evaluation = data.get("evaluation")

            # Dynamically build video path for this document
            video_path = f"videos/{user_email}/{doc_id}"
            blob = bucket.blob(video_path)

            video_url = None
            if blob.exists():
                video_url = blob.generate_signed_url(expiration=timedelta(hours=1))
            else:
                print(f"Video blob does not exist for {video_path}")

            # Extract final grade from evaluation text
            final_grade = None
            if evaluation:
                match = re.search(r"You scored a (\d+)", evaluation)
                if match:
                    final_grade = int(match.group(1))

            results.append({
                "doc_id": doc_id,
                "transcript": transcript,
                "evaluation": evaluation,
                "final_grade": final_grade,
                "video_url": video_url,
            })

        return results
    except Exception as e:
        print(f"Error retrieving evaluations: {e}")
        return []





def get_next_filename(user_email):
    today_str = datetime.now().strftime("%m%d%y")  # e.g., "042825"

    # You should already have a `bucket` object globally configured for your app
    # Example earlier setup: bucket = storage.bucket() if using pyrebase or similar
    blobs = list(bucket.list_blobs(prefix=f"videos/{user_email}/"))


    existing_numbers = []
    for blob in blobs:
        filename = os.path.basename(blob.name)
        if filename.startswith(today_str + "Pres") and filename.endswith(".mp4"):
            num_part = filename.replace(today_str + "Pres", "").replace(".mp4", "")
            if num_part.isdigit():
                existing_numbers.append(int(num_part))

    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    next_filename = f"{today_str}Pres{next_number:03d}.mp4"

    return next_filename


def delete_upload(user_email, filename):
    try:
        db = firestore.client()

        # Delete video from Storage
        video_path = f"videos/{user_email}/{filename}"
        blob = bucket.blob(video_path)
        if blob.exists():
            blob.delete()
            print(f"Deleted video: {video_path}")
        else:
            print(f"Video {video_path} does not exist.")

        # Delete transcript/evaluation from Firestore
        uploads_ref = db.collection("user_presentations").document(user_email).collection("uploads")
        doc_ref = uploads_ref.document(filename)

        if doc_ref.get().exists:
            doc_ref.delete()
            print(f"Deleted Firestore document: {filename}")
        else:
            print(f"Firestore document {filename} does not exist.")

        return True  # Indicate successful deletion
    except Exception as e:
        print(f"Error deleting upload: {e}")
        return False


