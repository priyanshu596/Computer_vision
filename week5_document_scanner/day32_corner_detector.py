# Day 32 | Week 5: Document Scanner
# Topic:  Corner Detector for Quadrilaterals
# Goal:   Find the 4 corners of a document in an image
# Output: outputs/day32_corners.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# ─────────────────────────────────────────────
# WHAT YOU'LL LEARN TODAY
# ─────────────────────────────────────────────
# A document in a photo is a quadrilateral (4-sided polygon).
# Today's pipeline:
#   image → grayscale → blur → Canny → findContours → approxPolyDP → largest 4-sided shape
#
# Key insight: approxPolyDP simplifies a contour into fewer points.
# If it simplifies to exactly 4 points → it's a quadrilateral → likely a document.

# ─────────────────────────────────────────────
# RESOURCES — read these if you get stuck
# ─────────────────────────────────────────────
# Contours:    https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
# approxPoly:  https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
# Good guide:  https://pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/

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

def make_test_document():
    canvas = np.ones((500, 600, 3), dtype=np.uint8) * 120
    pts = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.int32)
    cv2.fillPoly(canvas, [pts], (240, 240, 230))
    for y in range(100, 420, 35):
        cv2.line(canvas, (100, y), (500, y - 10), (200, 200, 200), 1)
    return canvas

img = make_test_document()
# img = cv2.imread('document.jpg')

# ─────────────────────────────────────────────
# STEP 1 — Preprocess: gray → blur → edges
# ─────────────────────────────────────────────
# YOUR TASK: Produce a clean edge image
# Use the same pipeline as Day 31 (grayscale → GaussianBlur → Canny)

gray    = None  # YOUR CODE
blurred = None  # YOUR CODE
edges   = None  # YOUR CODE

# ─────────────────────────────────────────────
# STEP 2 — Find all contours
# ─────────────────────────────────────────────
# YOUR TASK: Use cv2.findContours on your edges image
# Use: cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
# Print the total number of contours found

contours = None  # YOUR CODE
# print(f"Found {len(contours)} contours")

# ─────────────────────────────────────────────
# STEP 3 — Filter to 4-sided polygons
# ─────────────────────────────────────────────
# YOUR TASK:
# Loop through contours. For each:
#   1. Compute perimeter: cv2.arcLength(c, True)
#   2. Approximate polygon: cv2.approxPolyDP(c, epsilon, True)
#      epsilon = 0.02 * perimeter  (controls how much simplification)
#   3. If approx has exactly 4 points AND area > 5000 → it's a document candidate
# Keep track of the largest qualifying contour

doc_contour = None  # YOUR CODE — the 4-point approximation of the largest quad

# ─────────────────────────────────────────────
# STEP 4 — Draw corners and outline
# ─────────────────────────────────────────────
# YOUR TASK:
# - Draw the green outline: cv2.drawContours
# - Draw 4 coloured circles at each corner
# - Print the (x, y) coordinates of each corner

corner_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # B G R Y
result = img.copy()

# YOUR CODE HERE

# ─────────────────────────────────────────────
# STEP 5 — Display and save
# ─────────────────────────────────────────────
if edges is not None:
    show_many([img, edges, result], ['Original', 'Edges', 'Detected Corners'])
    cv2.imwrite('../outputs/day32_corners.png', result)
    print("Saved → outputs/day32_corners.png")

# ─────────────────────────────────────────────
# REFLECTION
# ─────────────────────────────────────────────
# Q1: What does epsilon control in approxPolyDP? What happens if it's too large?
# A1:

# Q2: Why do we pick the contour with the LARGEST area?
# A2:

# WHERE THIS LEADS:
# You now have 4 corners. Tomorrow (Day 33) you'll use these to warp
# the perspective and produce a flat, top-down view of the document.
