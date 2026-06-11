import cv2
import mediapipe as mp
import urllib.request
import os
from gesture_classifier import fingers_up, classify_gesture
from action_mapper import get_action

MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading model (~8MB)...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Model downloaded!")

BaseOptions           = mp.tasks.BaseOptions
HandLandmarker        = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode     = mp.tasks.vision.RunningMode

CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),
    (15,16),(13,17),(17,18),(18,19),(19,20),(0,17)
]

def draw_ui(frame, gesture, action, lms):
    h, w = frame.shape[:2]
    if lms:
        pts = [(int(l.x * w), int(l.y * h)) for l in lms]
        for a, b in CONNECTIONS:
            cv2.line(frame, pts[a], pts[b], (0, 200, 255), 2)
        for x, y in pts:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h-110), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    cv2.putText(frame, f"Gesture : {gesture}", (20, h-65), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,120), 2)
    cv2.putText(frame, f"Action  : {action}", (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (0,200,255), 2)
    cv2.putText(frame, "Press Q to quit", (w-200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180,180,180), 1)

def main():
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6
    )
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam. Try VideoCapture(1)")
        return
    print("Starting... Press Q to quit.")
    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Cannot read frame.")
                break
            frame  = cv2.flip(frame, 1)
            rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result  = landmarker.detect(mp_img)
            gesture = "No Hand"
            action  = "--"
            lms     = None
            if result.hand_landmarks:
                lms = result.hand_landmarks[0]
                h, w = frame.shape[:2]
                pts     = [(int(l.x * w), int(l.y * h), l.z) for l in lms]
                fingers = fingers_up(pts)
                gesture = classify_gesture(fingers)
                action  = get_action(gesture)
            draw_ui(frame, gesture, action, lms)
            cv2.imshow("Hand Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    print("Exited.")

if __name__ == "__main__":
    main()