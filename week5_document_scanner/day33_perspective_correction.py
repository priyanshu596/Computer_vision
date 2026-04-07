# Day 33 | Week 5: Document Scanner
# Topic:  Perspective Correction
# Goal:   Warp a tilted document into a flat rectangle
# Output: outputs/day33_warped.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# ─────────────────────────────────────────────
# WHAT YOU'LL LEARN TODAY
# ─────────────────────────────────────────────
# You have 4 corner points. Now you need to map them to a flat rectangle.
# This is called a "perspective transform" or "homography".
#
# Two key functions:
#   cv2.getPerspectiveTransform(src_pts, dst_pts) → 3x3 matrix M
#   cv2.warpPerspective(img, M, (width, height))  → flat output
#
# The tricky part: corners must be in a consistent order: TL, TR, BR, BL
# If the order is wrong, the output will be flipped or rotated.

# ─────────────────────────────────────────────
# RESOURCES
# ─────────────────────────────────────────────
# Perspective transform: https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html
# Great walkthrough:     https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

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
        cv2.line(canvas, (110, y), (510, y - 10), (180, 180, 180), 1)
    cv2.putText(canvas, 'DOCUMENT', (160, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100,100,100), 2)
    return canvas

img = make_test_document()
#img=cv2.imread("document1.webp",cv2.COLOR_BGR2RGB)
# Known corners of the synthetic document (TL, TR, BR, BL)
known_corners = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.float32)

# ─────────────────────────────────────────────
# STEP 1 — Order corners: TL, TR, BR, BL
# ─────────────────────────────────────────────
# YOUR TASK: Write order_corners(pts)
# Hint: TL has smallest (x+y), BR has largest (x+y)
#       TR has smallest (x-y), BL has largest (x-y)

def order_corners(pts):
    """
    Takes 4 points in any order.
    Returns them ordered: [TL, TR, BR, BL]
    """
    # YOUR CODE HER
    rect=np.zeros((4,2))
    s=pts.sum(axis=1)
    rect[0]=pts[np.argmin(s)]
    rect[2]=pts[np.argmax(s)]
    diff=np.diff(pts,axis=1)
    rect[1]=pts[np.argmin(diff)]
    rect[3]=pts[np.argmax(diff)]

    return rect

# ─────────────────────────────────────────────
# STEP 2 — Compute output dimensions
# ─────────────────────────────────────────────
# YOUR TASK: Write compute_output_size(ordered_pts)
# Width  = max distance between bottom corners OR top corners
# Height = max distance between left corners OR right corners
# Use np.linalg.norm to measure distance between two points

def compute_output_size(ordered_pts):
    """Returns (width, height) of the output flat document."""
    # YOUR CODE HERE
    (tl, tr, br, bl) = ordered_pts

    widthA=np.sqrt(((tl[0]-tr[0])**2)+((tl[1]-tr[1])**2))
    widthB=np.sqrt(((bl[0]-br[0])**2)+((bl[1]-br[1])**2))
    width=max(int(widthA),int(widthB))

    heightA=np.linalg.norm(tl-bl)
    heightB=np.linalg.norm(tr-br)
    height=max(int(heightA),int(heightB))

    return width,height

    

# ─────────────────────────────────────────────
# STEP 3 — Apply perspective transform
# ─────────────────────────────────────────────
# YOUR TASK: Write warp_to_flat(img, corners)
# 1. Order the corners
# 2. Compute output size
# 3. Build dst_pts: the 4 corners of the output rectangle
# 4. cv2.getPerspectiveTransform(src, dst) → M
# 5. cv2.warpPerspective(img, M, (w, h)) → flat image

def warp_to_flat(img, corners):
    ordered = order_corners(corners)
    w, h = compute_output_size(ordered)

    dst = np.array([
        [0, 0],        # top-left
        [w-1, 0],      # top-right
        [w-1, h-1],    # bottom-right
        [0, h-1]       # bottom-left
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(ordered.astype(np.float32), dst)

    flat = cv2.warpPerspective(img, M, (w, h))
    return flat

    
# ─────────────────────────────────────────────
# STEP 4 — Test it
# ─────────────────────────────────────────────
ordered = order_corners(known_corners)
flat    = warp_to_flat(img, known_corners)

if flat is not None:
    show_many([img, flat], ['Original (tilted)', 'Perspective Corrected'])
    cv2.imwrite('../outputs/day33_warped.png', flat)
    print("Saved → outputs/day33_warped.png")

# ─────────────────────────────────────────────
# REFLECTION
# ─────────────────────────────────────────────
# Q1: What happens if you pass corners in the wrong order?
# A1: If corners are passed in wrong then the transformation becomes distorted images are cropped 
# Q2: The transform matrix M is 3x3. Why does a 2D transform need 3x3?
# A2: 

# WHERE THIS LEADS:
# Tomorrow (Day 34) you'll clean up this flat output — removing shadows,
# sharpening text — to make it look like a real scanned document.
