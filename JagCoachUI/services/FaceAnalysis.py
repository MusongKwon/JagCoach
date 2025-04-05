import cv2
import dlib
import mediapipe as mp
import numpy as np
import queue
from deepface import DeepFace
from threading import Thread

class FaceAnalyzer:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True, max_num_faces=1)

        # Define landmarks for pupils
        self.LEFT_PUPIL = 468
        self.RIGHT_PUPIL = 473
        self.LEFT_EYE = [33, 133]
        self.RIGHT_EYE = [362, 263]

    def detect_faces(self, frame):
        """Detect faces using Dlib"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.detector(gray)

    def analyze_emotion(self, face_region):
        """Detect emotion using DeepFace"""
        result = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False, detector_backend="opencv")
        return result[0]['dominant_emotion'] if result else "Unknown"

    def detect_gaze(self, landmarks):
        """Determine gaze direction based on pupil position"""
        if not landmarks:
            return "Unknown"

        left_eye_inner = landmarks[self.LEFT_EYE[0]].x
        left_eye_outer = landmarks[self.LEFT_EYE[1]].x
        right_eye_inner = landmarks[self.RIGHT_EYE[0]].x
        right_eye_outer = landmarks[self.RIGHT_EYE[1]].x

        left_pupil_x = landmarks[self.LEFT_PUPIL].x
        right_pupil_x = landmarks[self.RIGHT_PUPIL].x

        left_pupil_ratio = (left_pupil_x - left_eye_inner) / (left_eye_outer - left_eye_inner)
        right_pupil_ratio = (right_pupil_x - right_eye_inner) / (right_eye_outer - right_eye_inner)

        if 0.4 < left_pupil_ratio < 0.6 and 0.4 < right_pupil_ratio < 0.6:
            return "Eye Contact"
        elif left_pupil_ratio < 0.4 and right_pupil_ratio < 0.4:
            return "Looking Left"
        elif left_pupil_ratio > 0.6 and right_pupil_ratio > 0.6:
            return "Looking Right"
        else:
            return "Looking Away"

    def process_frame(self, frame):
        """Detect face, emotion, and gaze in a single frame"""
        faces = self.detect_faces(frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face_mesh.process(rgb_frame)

        emotions_list = []
        eye_contact_list = []

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            roi = frame[y:y + h, x:x + w]

            emotion = self.analyze_emotion(roi)
            eye_contact = "Unknown"

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                eye_contact = self.detect_gaze(landmarks)

            # Store results
            emotions_list.append(emotion)
            eye_contact_list.append(eye_contact)

            # Draw face rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emotion}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"{eye_contact}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        return frame, emotions_list, eye_contact_list

def capture_frames(cap, input_queue, frame_skip=15):
    """Capture video frames and skip unnecessary ones"""
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip == 0:  # Skip frames for performance boost
            input_queue.put(frame)

    cap.release()

def analyze_face(video_path):
    """Process the video and analyze face emotions and gaze"""
    cap = cv2.VideoCapture(video_path)
    analyzer = FaceAnalyzer()
    input_queue = queue.Queue()

    emotions_list = []
    eye_contact_list = []

    frame_thread = Thread(target=capture_frames, args=(cap, input_queue), daemon=True)
    frame_thread.start()

    while True:
        try:
            frame = input_queue.get(timeout=0.1)  # Prevents CPU overuse when waiting
        except queue.Empty:
            if not frame_thread.is_alive():
                break  # Exit when frames are finished
            continue  # Skip iteration if queue is empty

        processed_frame, emotions, eye_contacts = analyzer.process_frame(frame)

        emotions_list.extend(emotions)
        eye_contact_list.extend(eye_contacts)

        cv2.imshow("Video Analysis", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    c = 0
    for i in range(len(emotions_list) - 1):
        if emotions_list[i+1] != emotions_list[i]:
            c += 1
    emotion_ratio = c / (len(emotions_list)-1)
    print(emotion_ratio)
    eye_contact_ratio = eye_contact_list.count('Eye Contact') / len(eye_contact_list)
    print(eye_contact_ratio)

    return emotion_ratio, eye_contact_ratio
