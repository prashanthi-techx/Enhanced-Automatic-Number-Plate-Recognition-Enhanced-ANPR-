import cv2
import os
import time
from detect_plate import detect_license_plate
from ocr_recognition import recognize_plate_text
from speed_estimation import SpeedEstimator
from utils import draw_text

# -------------------------------
# Configuration
# -------------------------------
VIDEO_SOURCE = 0  # Use 0 for webcam or give path to video file
OUTPUT_DIR = "outputs"
CASCADE_PATH = "models/haarcascade_russian_plate_number.xml"
TRACKER_TYPE = "CSRT"  # Options: KCF, CSRT, MIL
DISPLAY = True
SPEED_LIMIT = 60  # km/h

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Video Capture
cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened():
    raise IOError("Error: Cannot open video source")

# Load Haar cascade for number plate detection
plate_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Initialize Speed Estimator
speed_estimator = SpeedEstimator(real_distance_m=10.0, fps=30.0)

# Initialize tracker dictionary
trackers = {}
track_start_time = {}

print("[INFO] Starting Enhanced ANPR system... Press 'q' to quit.")

# -------------------------------
# Main Loop
# -------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video stream.")
        break

    frame = cv2.resize(frame, (960, 540))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect plates
    plates = detect_license_plate(gray, plate_cascade)

    for (x, y, w, h) in plates:
        plate_img = frame[y:y + h, x:x + w]

        # Recognize text
        plate_text = recognize_plate_text(plate_img)

        # Track plate (simplified)
        plate_id = hash(plate_text)
        if plate_id not in trackers:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x, y, w, h))
            trackers[plate_id] = tracker
            track_start_time[plate_id] = time.time()
        else:
            success, box = trackers[plate_id].update(frame)
            if success:
                x, y, w, h = [int(v) for v in box]

        # Estimate speed (based on displacement)
        elapsed_time = time.time() - track_start_time[plate_id]
        speed = speed_estimator.estimate_speed(w, elapsed_time)

        # Draw rectangle and info
        color = (0, 255, 0) if speed <= SPEED_LIMIT else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        label = f"{plate_text} | {speed:.1f} km/h"
        draw_text(frame, label, x, y - 10, color)

        # Save snapshot for violations
        if speed > SPEED_LIMIT:
            filename = os.path.join(OUTPUT_DIR, f"violation_{plate_text}_{int(time.time())}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[ALERT] Speed violation detected: {label}")
            del trackers[plate_id]

    # Display
    if DISPLAY:
        cv2.imshow("Enhanced ANPR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# -------------------------------
# Cleanup
# -------------------------------
cap.release()
cv2.destroyAllWindows()
print("[INFO] ANPR system stopped successfully.")
