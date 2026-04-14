# Day 35 | Week 5: Document Scanner
# Topic:  Deskewer — Auto-detect and fix rotation
# Goal:   Detect how much a document is rotated and correct it
# Output: outputs/day35_deskewed.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Sometimes a document isn't perspective-distorted — it's just slightly tilted.
# Today: detect the skew angle automatically and rotate to fix it.
# Approach: find edges → run HoughLines → find the dominant angle → rotate by -angle
#
# Key difference from Day 31:
#   HoughLines  → returns (rho, theta) — the full infinite line in polar form
#   HoughLinesP → returns (x1,y1,x2,y2) — a line segment

# RESOURCES
# HoughLines:  https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html
# Rotation:    https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
# Deskew explained: https://learnopencv.com/skew-correction-word-image-using-python-opencv/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def show_many(imgs, titles):
    fig, axes = plt.subplots(1, len(imgs), figsize=(5 * len(imgs), 4))
    if len(imgs) == 1: axes = [axes]
    for ax, img, title in zip(axes, imgs, titles):
        ax.set_title(title); ax.axis('off')
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape)==3 else img, cmap='gray')
    plt.tight_layout(); plt.show()

def make_lined_document():
    doc = np.ones((400, 500, 3), dtype=np.uint8) * 240
    for y in range(60, 380, 35):
        cv2.line(doc, (40, y), (460, y), (160, 160, 160), 1)
    cv2.putText(doc, 'Text line 1', (50, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80,80,80), 1)
    cv2.putText(doc, 'Text line 2', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80,80,80), 1)
    return doc

# ─────────────────────────────────────────────
# STEP 1 — Create a deliberately tilted image
# ─────────────────────────────────────────────
def rotate_image(img, angle):
    """Rotate image by angle degrees around its centre. Returns same-size image."""
    h, w = img.shape[:2]
    centre = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centre, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)

doc    = make_lined_document()
angle  = 12  # degrees of intentional tilt
tilted = rotate_image(doc, angle)

# ─────────────────────────────────────────────
# STEP 2 — Detect the skew angle
# ─────────────────────────────────────────────
# YOUR TASK: Write detect_skew_angle(img)
# Approach:
#   1. Grayscale → Canny
#   2. HoughLines → get array of (rho, theta)
#   3. Convert theta to degrees: angle_deg = np.degrees(theta) - 90
#   4. The dominant angle is the skew → return its median

import cv2
import numpy as np

def detect_skew_angle(img):
    """
    Returns the estimated skew angle in degrees.
    Positive = clockwise tilt, Negative = counter-clockwise.
    """
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Edge detection (IMPORTANT)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Hough Transform
    lines = cv2.HoughLines(edges, 1, np.pi/180, 150)
    
    angle_degrees = []
    
    if lines is not None:
        for i in range(len(lines)):
            rho, theta = lines[i][0]
            
            # Convert to degrees and adjust
            angle_deg = np.degrees(theta) - 90
            angle_degrees.append(angle_deg)
    
    # Handle no lines case
    if len(angle_degrees) == 0:
        return 0.0
    
    # Use median instead of max (robust)
    skew = np.median(angle_degrees)
    
    return skew


# ─────────────────────────────────────────────
# STEP 3 — Correct the skew
# ─────────────────────────────────────────────
detected = detect_skew_angle(tilted)
if detected is not None:
    print(f"Introduced angle: {angle}° | Detected: {detected:.1f}°")
    corrected = rotate_image(tilted, -detected)

    show_many([doc, tilted, corrected],
              ['Original', f'Tilted {angle}°', f'Corrected (detected {detected:.1f}°)'])
    cv2.imwrite('../outputs/day35_deskewed.png', corrected)
    print("Saved → outputs/day35_deskewed.png")

# REFLECTION
# Q1: Why do we take the median of detected angles instead of the mean?
# A1:Mean is verys ensitive to outlier that's why we take meduan value
# Q2: This approach works well for text documents. When might it fail?
# A2:

# WHERE THIS LEADS:
# Day 36 adds a visual UI overlay — showing what the scanner detected
# before the user confirms. Then Day 37 ties everything into one function.
