# Week 5 Project | Document Scanner
# Goal:   Complete pipeline — photo → flat clean scan
# Output: outputs/week5_scan_1.png, week5_scan_2.png, week5_scan_3.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# ─────────────────────────────────────────────
# YOUR TASK
# ─────────────────────────────────────────────
# Build scan_document(img) → clean_scan
# Pipeline: detect corners → warp flat → enhance → return
#
# Test on 3 inputs:
#   1. Normal document image
#   2. Same document rotated 20°
#   3. A different image (try a book page or receipt photo)
#
# Requirements:
#   - Works even if the document is slightly tilted (use deskewer as fallback)
#   - Returns a clean, high-contrast grayscale image
#   - Saves each result to outputs/

# ─────────────────────────────────────────────
# KAGGLE PUBLISH CHECKLIST (after you finish)
# ─────────────────────────────────────────────
# 1. Go to kaggle.com/code → New Notebook
# 2. Copy this file's code into the notebook
# 3. Add a markdown cell at the top explaining what you built
# 4. Add a markdown cell at the bottom: "Where this leads → CRAFT text detection"
# 5. Make the notebook public
# 6. Copy the URL into progress/status.json → week5 → kaggle_url
# 7. git add . && git commit -m "Week 5 project done + Kaggle published" && git push

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

# ─────────────────────────────────────────────
# PASTE YOUR BEST IMPLEMENTATIONS FROM DAYS 31-36
# ─────────────────────────────────────────────

def order_corners(pts):
    """Order 4 corner points: TL, TR, BR, BL"""
    # YOUR CODE (from Day 33)
    pass

def warp_to_flat(img, corners):
    """Perspective warp to flat rectangle."""
    # YOUR CODE (from Day 33)
    pass

def enhance_scan(img):
    """Enhance a flat document image to look like a clean scan."""
    # YOUR CODE (from Day 34)
    pass

def detect_skew_angle(img):
    """Detect rotation angle of a document."""
    # YOUR CODE (from Day 35)
    pass

def rotate_image(img, angle):
    """Rotate image by angle degrees."""
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

# ─────────────────────────────────────────────
# THE MAIN FUNCTION
# ─────────────────────────────────────────────

def scan_document(img):
    """
    Complete document scanner pipeline.
    Input:  BGR image (photo of a document, possibly at an angle)
    Output: clean grayscale scanned image

    Pipeline:
    1. Try to find 4 corners (perspective distortion)
    2. If found → warp perspective flat
    3. If not found → try deskew (simple rotation) as fallback
    4. Enhance the result
    5. Return clean scan
    """
    # YOUR COMPLETE PIPELINE HERE
    pass


# ─────────────────────────────────────────────
# TEST INPUTS
# ─────────────────────────────────────────────

def make_test_document(tilt_angle=0):
    canvas = np.ones((500, 600, 3), dtype=np.uint8) * 120
    pts = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.int32)
    cv2.fillPoly(canvas, [pts], (240, 240, 230))
    for y in range(100, 420, 35):
        cv2.line(canvas, (100, y), (500, y - 10), (170, 170, 170), 1)
    cv2.putText(canvas, 'DOCUMENT', (160, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100,100,100), 2)
    if tilt_angle:
        h, w = canvas.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), tilt_angle, 1.0)
        canvas = cv2.warpAffine(canvas, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return canvas

img1 = make_test_document(tilt_angle=0)   # Test 1: normal
img2 = make_test_document(tilt_angle=20)  # Test 2: rotated 20°
img3 = make_test_document(tilt_angle=-8)  # Test 3: different tilt
# Uncomment to use real images:
# img1 = cv2.imread('document.jpg')
# img2 = cv2.imread('receipt.jpg')

for i, (img, name) in enumerate([(img1, 'normal'), (img2, 'rotated_20'), (img3, 'tilted_8')], 1):
    result = scan_document(img)
    if result is not None:
        show_many([img, result], [f'Input {i} ({name})', f'Scanned {i}'])
        cv2.imwrite(f'../outputs/week5_scan_{i}.png', result)
        print(f"Saved → outputs/week5_scan_{i}.png")

# ─────────────────────────────────────────────
# WHERE THIS LEADS
# ─────────────────────────────────────────────
# You just built a classical document scanner from scratch.
# The same pipeline underlies every mobile scanning app.
#
# When you reach deep learning:
#   → Your edge detector gets replaced by a learned feature extractor
#   → Your corner detector gets replaced by a keypoint regression network
#   → Your warp stays exactly the same (it's geometry, not learning)
#
# The DL model that does what you did today: CRAFT (Character Region Awareness
# for Text Detection) — https://arxiv.org/abs/1904.01906
