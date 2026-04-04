# Day 46 | Week 7: Image Search Engine
# Topic:  ORB Feature Matching
# Goal:   Match images using keypoints that survive rotation and scale
# Output: outputs/day46_orb_match.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Histograms fail if the same image is cropped or rotated.
# ORB (Oriented FAST and Rotated BRIEF) finds distinctive keypoints
# and describes each one with a binary descriptor.
# Two images of the same thing → many matching keypoints.
#
# Pipeline:
#   image → ORB detector → keypoints + descriptors → BFMatcher → match count

# RESOURCES
# ORB:      https://docs.opencv.org/4.x/d1/d89/tutorial_py_orb.html
# Matching: https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_test_image():
    img = np.ones((300, 400, 3), dtype=np.uint8) * 200
    cv2.rectangle(img, (50, 50), (200, 200), (80, 40, 160), -1)
    cv2.circle(img, (300, 150), 60, (40, 160, 80), -1)
    cv2.line(img, (0, 280), (400, 100), (160, 80, 40), 3)
    return img

def rotate_image(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

img_original = make_test_image()
img_rotated  = rotate_image(img_original, 25)
img_different = np.random.randint(50, 200, img_original.shape, dtype=np.uint8)

# ─────────────────────────────────────────────
# STEP 1 — Detect ORB keypoints and descriptors
# ─────────────────────────────────────────────
# YOUR TASK: Write compute_orb(img, n_features=500)
# Steps:
#   orb = cv2.ORB_create(nfeatures=n_features)
#   kp, des = orb.detectAndCompute(gray, None)
# Returns (keypoints, descriptors)

def compute_orb(img, n_features=500):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb  = cv2.ORB_create(nfeatures=n_features)
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 2 — Match descriptors between two images
# ─────────────────────────────────────────────
# YOUR TASK: Write match_orb(des1, des2)
# Use BFMatcher with NORM_HAMMING (ORB uses binary descriptors)
# Apply ratio test: keep only matches where best_match.distance < 0.75 * second_best
# Returns list of good matches

def match_orb(des1, des2):
    if des1 is None or des2 is None:
        return []
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    # YOUR CODE HERE — use knnMatch with k=2, then ratio test
    pass

# ─────────────────────────────────────────────
# STEP 3 — Similarity score from match count
# ─────────────────────────────────────────────
def orb_similarity(img1, img2):
    """Returns number of good ORB matches (higher = more similar)."""
    kp1, des1 = compute_orb(img1) or (None, None)
    kp2, des2 = compute_orb(img2) or (None, None)
    matches = match_orb(des1, des2)
    return len(matches) if matches else 0

score_same    = orb_similarity(img_original, img_rotated)
score_diff    = orb_similarity(img_original, img_different)
print(f"Same image rotated: {score_same} matches")
print(f"Different image:    {score_diff} matches")

# ─────────────────────────────────────────────
# STEP 4 — Visualize matches
# ─────────────────────────────────────────────
kp1, des1 = compute_orb(img_original) or (None, None)
kp2, des2 = compute_orb(img_rotated) or (None, None)
if kp1 and kp2:
    good = match_orb(des1, des2) or []
    vis  = cv2.drawMatches(img_original, kp1, img_rotated, kp2,
                           good[:30], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(12, 4))
    plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)); plt.axis('off')
    plt.title(f'ORB matches: {len(good)} good matches'); plt.tight_layout()
    plt.savefig('../outputs/day46_orb_match.png'); plt.show()
    print("Saved → outputs/day46_orb_match.png")

# REFLECTION
# Q1: Why does ORB use NORM_HAMMING instead of NORM_L2 for matching?
# A1:
# Q2: What is the ratio test and why does it help reduce false matches?
# A2:
