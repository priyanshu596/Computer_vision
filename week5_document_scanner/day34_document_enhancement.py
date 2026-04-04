# Day 34 | Week 5: Document Scanner
# Topic:  Document Enhancement
# Goal:   Make the warped document look like a real clean scan
# Output: outputs/day34_enhanced.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# A real scanner does more than flatten — it removes shadows and sharpens text.
# Two approaches to try:
#   1. cv2.adaptiveThreshold — handles uneven lighting (shadows)
#   2. Otsu's threshold      — global, works when lighting is even
# Then: sharpen with a kernel to make text crisp.

# RESOURCES
# adaptiveThreshold: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
# Sharpening:        https://learnopencv.com/image-filtering-using-convolution-in-opencv/

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

# Load your warped output from Day 33, or use this synthetic stand-in
flat = np.ones((400, 300, 3), dtype=np.uint8) * 210
flat[50:350, 30:270] = 230
for y in range(80, 340, 30):
    cv2.line(flat, (50, y), (260, y), (160, 160, 160), 1)
cv2.putText(flat, 'Invoice #123', (60, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80,80,80), 1)
# Add a fake shadow gradient
for x in range(30):
    alpha = (30 - x) / 30 * 0.4
    flat[:, x] = (flat[:, x] * (1 - alpha)).astype(np.uint8)
# flat = cv2.imread('../outputs/day33_warped.png')


# ─────────────────────────────────────────────
# STEP 1 — Convert to grayscale
# ─────────────────────────────────────────────
gray = None  # YOUR CODE

# ─────────────────────────────────────────────
# STEP 2 — Try both thresholding approaches
# ─────────────────────────────────────────────
# YOUR TASK A: Otsu's threshold
# _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# YOUR TASK B: Adaptive threshold
# adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                   cv2.THRESH_BINARY, blockSize=21, C=10)
# blockSize: size of neighbourhood (must be odd). Larger = handles bigger shadows
# C: constant subtracted from mean. Higher = darker threshold

otsu     = None  # YOUR CODE
adaptive = None  # YOUR CODE

# ─────────────────────────────────────────────
# STEP 3 — Sharpen the result
# ─────────────────────────────────────────────
# YOUR TASK: Apply a sharpening kernel to whichever result you prefer
sharpen_kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
sharpened = None  # YOUR CODE: cv2.filter2D(...)

# ─────────────────────────────────────────────
# STEP 4 — Build enhance_scan function
# ─────────────────────────────────────────────
def enhance_scan(img):
    """
    Takes a flat BGR document image.
    Returns a clean, high-contrast grayscale image.
    """
    # YOUR CODE — combine the best steps from above into one function
    pass

# Test it
cleaned = enhance_scan(flat)
if cleaned is not None:
    show_many([flat, cleaned], ['Flat document', 'Enhanced scan'])
    cv2.imwrite('../outputs/day34_enhanced.png', cleaned)
    print("Saved → outputs/day34_enhanced.png")

# REFLECTION
# Q1: When would adaptive threshold fail where Otsu would work better?
# A1:
# Q2: What does blockSize control in adaptiveThreshold?
# A2:

# WHERE THIS LEADS:
# Day 35 handles a different problem: what if the document isn't perspective-distorted
# but just slightly rotated? That needs a different fix — deskewing.
