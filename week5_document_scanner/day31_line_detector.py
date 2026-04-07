# Day 31 | Week 5: Document Scanner
# Topic:  Line Detector
# Goal:   Detect all straight lines in an image using Canny + HoughLinesP
# Output: outputs/day31_lines.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# ─────────────────────────────────────────────
# WHAT YOU'LL LEARN TODAY
# ─────────────────────────────────────────────
# Before you can find a document's edges, you need to detect straight lines.
# Today's pipeline:
#   image → grayscale → blur → Canny edges → HoughLinesP → draw lines
#
# Two functions to focus on:
#   cv2.Canny(img, low_threshold, high_threshold)
#   cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength, maxLineGap)

# ─────────────────────────────────────────────
# RESOURCES — read these if you get stuck
# ─────────────────────────────────────────────
# Canny:      https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
# HoughLines: https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html
# Quick ref:  https://learnopencv.com/hough-transform-with-opencv-c-python/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# HELPER — do not modify
# ─────────────────────────────────────────────
def show(img, title=''):
    plt.figure(figsize=(6, 4))
    plt.title(title)
    plt.axis('off')
    if len(img.shape) == 3:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray')
    plt.tight_layout()
    plt.show()

def show_many(imgs, titles):
    fig, axes = plt.subplots(1, len(imgs), figsize=(5 * len(imgs), 4))
    if len(imgs) == 1:
        axes = [axes]
    for ax, img, title in zip(axes, imgs, titles):
        ax.set_title(title)
        ax.axis('off')
        if len(img.shape) == 3:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            ax.imshow(img, cmap='gray')
    plt.tight_layout()
    plt.show()

# ─────────────────────────────────────────────
# STEP 1 — Create or load a test image
# ─────────────────────────────────────────────
# If you have document.jpg in this folder, use:
#   img = cv2.imread('document.jpg')
# Otherwise we create a synthetic document-like image for practice:

def make_test_document():
    """Synthetic image that looks like a tilted document."""
    canvas = np.ones((500, 600, 3), dtype=np.uint8) * 200
    pts = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.int32)
    cv2.fillPoly(canvas, [pts], (255, 255, 255))
    for y in range(100, 420, 35):
        cv2.line(canvas, (100, y), (500, y - 10), (180, 180, 180), 1)
    cv2.rectangle(canvas, (110, 80), (490, 120), (100, 100, 100), 2)
    return canvas

img = make_test_document()
# Uncomment to use a real image instead:
img = cv2.imread('document1.webp')
assert img is not None, "document.jpg not found — place it in this folder"

# ─────────────────────────────────────────────
# STEP 2 — Convert to grayscale and blur
# ─────────────────────────────────────────────
# Why blur first? Canny is sensitive to noise.
# A small Gaussian blur removes noise before edge detection.

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# ─────────────────────────────────────────────
# STEP 3 — Detect edges with Canny
# ─────────────────────────────────────────────
# YOUR TASK: Apply cv2.Canny to blurred
# Try threshold pairs: (50, 150), (100, 200), (30, 90)
# Which gives the cleanest edges on your image?



edges= cv2.Canny(blurred,100,200) 



# ─────────────────────────────────────────────
# STEP 4 — Detect lines with HoughLinesP
# ─────────────────────────────────────────────
# YOUR TASK: Apply cv2.HoughLinesP to your edges
# Parameters to tune:
#   rho = 1              (pixel resolution of accumulator)
#   theta = np.pi/180    (angle resolution in radians)
#   threshold = 80       (minimum votes — increase to get fewer, stronger lines)
#   minLineLength = 100  (reject short segments)
#   maxLineGap = 10      (how much gap is allowed in a line)

lines = cv2.HoughLinesP(edges,1,np.pi/180,80,100,10)  # YOUR CODE HERE

# ─────────────────────────────────────────────
# STEP 5 — Draw each line in a different colour
# ─────────────────────────────────────────────
# YOUR TASK:
# - Copy the original image
# - Loop through each line in `lines`
# - Draw each line segment with a random colour
# - Print the total number of line segments found

result = img.copy()

# YOUR CODE HERE
if lines is not None:
    for i in range(0,len(lines)):
        l=lines[i][0]
        color = (
    random.randint(0,255),
    random.randint(0,255),
    random.randint(0,255)
)
        cv2.line(result, (l[0], l[1]), (l[2], l[3]),color, 10)
        print(f"The total number of line segment is {len(lines)}")

# ─────────────────────────────────────────────
# STEP 6 — Display and save
# ─────────────────────────────────────────────
if edges is not None and result is not None:
    show_many([img, edges, result], ['Original', 'Canny Edges', 'Detected Lines'])
    
    cv2.imwrite('../outputs/day31_lines.png', result)
    print("Saved → outputs/day31_lines.png")

# ─────────────────────────────────────────────
# REFLECTION (answer in a comment before committing)
# ─────────────────────────────────────────────
# Q1: What happens when you increase the HoughLinesP threshold?
# A1:when the Threshold is increasesd then the filtering factor is strict so lines with that many clear intersection passes

# Q2: What's the difference between HoughLines and HoughLinesP?
# A2:In houghlines the ouput is (rho,theta) u don't get the endpoints , but in houghlinep you get the endpoints.

# WHERE THIS LEADS:
# HoughLinesP finds line segments. Tomorrow (Day 32) you'll use contours
# to find the full rectangle outline of the document — more robust than lines alone.