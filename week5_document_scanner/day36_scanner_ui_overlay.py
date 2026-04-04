# Day 36 | Week 5: Document Scanner
# Topic:  Scanner UI Overlay
# Goal:   Draw a live preview showing detected document before scanning
# Output: outputs/day36_preview.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Real scanner apps show a preview: green overlay on detected area, numbered corners,
# and a status bar. Today you build exactly that using cv2.addWeighted.
#
# Key function:
#   cv2.addWeighted(src1, alpha, src2, beta, gamma)
#   → blends two images: output = src1*alpha + src2*beta + gamma
#   Use alpha=0.6, beta=0.4 to make the overlay semi-transparent

# RESOURCES
# addWeighted: https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gafafb2513349db3bcff51f54ee5592a19
# Good example: https://pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_test_document():
    canvas = np.ones((500, 600, 3), dtype=np.uint8) * 120
    pts = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.int32)
    cv2.fillPoly(canvas, [pts], (240, 240, 230))
    for y in range(100, 420, 35):
        cv2.line(canvas, (100, y), (500, y - 10), (180, 180, 180), 1)
    return canvas, pts

img, doc_pts = make_test_document()

# ─────────────────────────────────────────────
# STEP 1 — Detect the document outline
# ─────────────────────────────────────────────
# YOUR TASK: Reuse your Day 32 approach to find the 4 corners
# (or just use doc_pts directly for testing while you build the UI)

def find_document_corners(img):
    """Returns 4 corner points of the largest quadrilateral, or None."""
    # YOUR CODE HERE — copy from Day 32
    pass

corners = find_document_corners(img)
if corners is None:
    corners = doc_pts  # fallback to known corners for testing

# ─────────────────────────────────────────────
# STEP 2 — Semi-transparent green overlay
# ─────────────────────────────────────────────
# YOUR TASK:
# 1. Create a copy of the image
# 2. On that copy, fill the document polygon with green: cv2.fillPoly
# 3. Blend with original using cv2.addWeighted (alpha=0.7, beta=0.3)

def draw_transparent_overlay(img, pts, color=(0, 200, 80)):
    """Draws a semi-transparent filled polygon over the document area."""
    overlay = img.copy()
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 3 — Numbered corner circles
# ─────────────────────────────────────────────
# YOUR TASK:
# For each corner (i, point):
#   - Draw a filled circle in a distinct colour
#   - Draw the number (1,2,3,4) inside it using cv2.putText

def draw_numbered_corners(img, pts):
    """Draws numbered circles at each corner."""
    corner_colors = [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80)]
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 4 — Bottom status bar
# ─────────────────────────────────────────────
# YOUR TASK:
# Draw a dark semi-transparent rectangle at the bottom of the image
# Add text: "Document detected — tap to scan"

def draw_status_bar(img, text="Document detected — tap to scan"):
    """Adds a dark status bar at the bottom with white text."""
    result = img.copy()
    h, w = result.shape[:2]
    # YOUR CODE HERE — dark bar + white text
    return result

# ─────────────────────────────────────────────
# STEP 5 — Combine into scanner_preview()
# ─────────────────────────────────────────────
def scanner_preview(img):
    """Full scanner UI overlay."""
    result = img.copy()
    corners = find_document_corners(result)
    if corners is None:
        return result
    result = draw_transparent_overlay(result, corners)
    draw_numbered_corners(result, corners)
    result = draw_status_bar(result)
    return result

preview = scanner_preview(img)
if preview is not None:
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
    plt.axis('off'); plt.title('Scanner Preview UI'); plt.tight_layout(); plt.show()
    cv2.imwrite('../outputs/day36_preview.png', preview)
    print("Saved → outputs/day36_preview.png")

# REFLECTION
# Q1: What does the alpha parameter in addWeighted control?
# A1:
# Q2: How would you add a "confidence score" percentage to the UI?
# A2:

# WHERE THIS LEADS:
# Tomorrow is the Week 5 project — you'll combine Days 31-36 into
# one clean scan_document() function and test it on 3 inputs.
