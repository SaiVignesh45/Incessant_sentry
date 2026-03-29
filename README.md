

---

# Smart Surveillance System

## All the versions so it'll be easy to run

built with Python 3.10+ |
ultralytics (YOLOv11) |
OpenCV (cv2) |
numpy

---

## Setup and Running

1. Install Python 3.12 (if not installed)
   Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

2. Install required libraries
   Open terminal in project directory and run:

```bash
pip install ultralytics opencv-python numpy
```

---

3. Clone the repository (if using git)

```bash
git clone <your-repo-link>
```

or download and unzip manually.

---

4. Make sure you have a camera source

* Webcam → default (`0`)
* IP Camera → replace with `rtsp://...`

---

5. Run the main system

```bash
python persim.py
```

---

6. Press `q` to exit the live feed window

---

## What this project is

This project is a **real-time AI-powered surveillance system** that detects human presence in a video feed.

Instead of running AI continuously, it uses:

* frame sampling (1 FPS)
* image difference detection (MSE)
* conditional AI inference (YOLO)

This makes the system:

* faster
* more efficient
* less storage-heavy

---

## What the script does:

---

### *persim.py* (Main System)

This is the **integrated system** that combines:

* frame sampling
* change detection
* AI-based human detection
* logging and storage

#### Workflow:

1. Capture video feed from camera
2. Save 1 frame per second (regular logging)
3. Compare current frame with previous frame
4. If difference exceeds threshold → run YOLO
5. If a person is detected → save + log alert

---

```mermaid
flowchart TD
    A[Camera Feed] --> B[Capture Frame]
    B --> C[Save Regular Frame]
    C --> D[Compare with Previous Frame]
    D --> E{Difference > Threshold?}
    E -->|No| F[Ignore / Log Steady State]
    E -->|Yes| G[Run YOLO Detection]
    G --> H{Person Detected?}
    H -->|No| I[Log Change Only]
    H -->|Yes| J[Save Suspicious Frame]
    J --> K[Log ALERT]
```
## Configuration Options

You can tweak the system behavior using:

* `CHECK_INTERVAL` → frame sampling rate
* `SIMILARITY_THRESHOLD` → sensitivity to motion
* `DETECTION_INTERVAL` → detection frequency

---

## Overall Work Flow

```mermaid
flowchart TD
    A[Camera Feed] --> B[Frame Sampling 1 FPS]
    B --> C[Image Difference Calculation]
    C --> D{Significant Change?}
    D -->|No| E[Save Regular Frame]
    D -->|Yes| F[Run YOLO Detection]
    F --> G{Person Detected?}
    G -->|No| H[Log Change Only]
    G -->|Yes| I[Save Suspicious Frame]
    I --> J[Log Alert Event]
```

---

## Limitations

* Sensitive to lighting changes
* Fixed threshold may need tuning
* No tracking (same person counted multiple times)
* Works best with stable camera

---

## Future Improvements

* Add object tracking (DeepSORT)
* Replace MSE with SSIM (better accuracy)
* Add alert system (email / Telegram)
* Web dashboard for monitoring
* Edge deployment (Raspberry Pi)

---

## Credits


---
