import cv2
import time
import os
import logging
import numpy as np
from datetime import datetime
from ultralytics import YOLO

# --- CONFIGURATION ---
REGULAR_FOLDER = "monitoring_logs/regular_frames"      # Saves 1 frame every second
SUSPICIOUS_FOLDER = "monitoring_logs/suspicious_events" # Saves only when things change
LOG_FILE = "monitoring_logs/security_log.txt"

CHECK_INTERVAL = 1.0          # 1 FPS (One frame per second)
SIMILARITY_THRESHOLD = 1500  # Sensitivity (Lower = more sensitive)

# --- SETUP ---
# Create folders if they don't exist
os.makedirs(REGULAR_FOLDER, exist_ok=True)
os.makedirs(SUSPICIOUS_FOLDER, exist_ok=True)

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load Model (Only runs when needed)
print("Loading AI Model...")
model = YOLO('yolo11n.pt')

def get_image_difference(img1, img2):
    """Returns a score representing how different two images are (0 = identical)."""
    if img1 is None or img2 is None:
        return 0
    
    # Resize to small resolution for fast comparison
    h, w = 300, 300
    i1 = cv2.resize(img1, (w, h))
    i2 = cv2.resize(img2, (w, h))
    
    # Convert to grayscale
    g1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)

    # Calculate Mean Squared Error (MSE)
    err = np.sum((g1.astype("float") - g2.astype("float")) ** 2)
    err /= float(g1.shape[0] * g1.shape[1])
    return err

# --- MAIN LOOP ---
cap = cv2.VideoCapture(0) # 0 for webcam, or 'rtsp://...' for IP camera

last_run_time = time.time()
previous_frame = None

print(f"System Started. Saving 1 FPS to '{REGULAR_FOLDER}'. Detecting changes > {SIMILARITY_THRESHOLD}.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    current_time = time.time()

    # Only process once per second
    if current_time - last_run_time >= CHECK_INTERVAL:
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # 1. ALWAYS SAVE THE REGULAR 1-SECOND FRAME
        reg_filename = f"{REGULAR_FOLDER}/frame_{timestamp}.jpg"
        cv2.imwrite(reg_filename, frame)
        
        # 2. CALCULATE DIFFERENCE
        diff_score = get_image_difference(previous_frame, frame)
        
        log_msg = f"Frame captured. Diff Score: {diff_score:.2f}"
        
        # 3. DECIDE: IS THIS "SIGNIFICANT"?
        if diff_score > SIMILARITY_THRESHOLD:
            print(f"🔴 Significant Change ({diff_score:.2f}) -> Running AI...")
            
            # --- RUN AI MODEL (Only here!) ---
            results = model.predict(frame, classes=[0], verbose=False)
            
            # Check if model actually found a person
            if len(results[0].boxes) > 0:
                count = len(results[0].boxes)
                
                # Save to SUSPICIOUS folder with bounding boxes
                suspicious_filename = f"{SUSPICIOUS_FOLDER}/ALERT_{timestamp}.jpg"
                annotated_frame = results[0].plot()
                cv2.imwrite(suspicious_filename, annotated_frame)
                
                log_msg += f" | ALERT: {count} Person(s) Detected! Saved to {suspicious_filename}"
            else:
                log_msg += " | Change detected, but no humans found."
        else:
            # If similar, we just log that we saved the regular frame
            print(f"⚪ Steady state ({diff_score:.2f}). Saved regular frame.")

        # Write to log file
        logging.info(log_msg)

        # Reset timer and reference frame
        last_run_time = current_time
        previous_frame = frame.copy()

    # Display feed (Optional)
    cv2.imshow('Security Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()