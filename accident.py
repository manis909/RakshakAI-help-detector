import cv2
import numpy as np

# ================= PERSON DETECTOR =================
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

prev_gray = None

# ================= CONFIG =================
MOTION_PIXEL_THRESHOLD = 35000
MIN_PEOPLE = 2
MAX_MOTION_PIXELS = 120000  # for normalization

def detect_accident(frame):
    """
    Returns:
    accident_like (bool)
    person_count (int)
    boxes (list)
    confidence (0-100)
    motion_mask (for heatmap)
    """

    global prev_gray

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    motion_pixels = 0
    motion_mask = np.zeros_like(gray)

    # ================= MOTION =================
    if prev_gray is not None:
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)

        motion_pixels = cv2.countNonZero(thresh)
        motion_mask = thresh

    prev_gray = gray

    motion_detected = motion_pixels > MOTION_PIXEL_THRESHOLD

    # ================= PEOPLE =================
    rects, _ = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    boxes = [(x, y, w, h) for (x, y, w, h) in rects]
    person_count = len(boxes)

    # ================= CONFIDENCE SCORE =================
    motion_score = min(motion_pixels / MAX_MOTION_PIXELS, 1.0)
    people_score = min(person_count / 3, 1.0)

    confidence = int((motion_score * 0.6 + people_score * 0.4) * 100)

    accident_like = (
        motion_detected and
        person_count >= MIN_PEOPLE and
        confidence >= 60
    )

    return accident_like, person_count, boxes, confidence, motion_mask
