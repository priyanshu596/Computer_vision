# Day 45 | Week 7: Image Search Engine
# Topic:  Color Histogram Matching
# Goal:   Find similar images using color distribution as a fingerprint
# Output: outputs/day45_histogram_match.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# A color histogram counts how many pixels have each color value.
# Two images with similar colors → similar histograms → low distance score.
# Simple but surprisingly effective for finding images from the same scene.
#
# Key functions:
#   cv2.calcHist(images, channels, mask, histSize, ranges)
#   cv2.compareHist(hist1, hist2, method)
#     methods: HISTCMP_CORREL (higher=similar), HISTCMP_BHATTACHARYYA (lower=similar)

# RESOURCES
# Histogram comparison: https://docs.opencv.org/4.x/d8/dc8/tutorial_histogram_comparison.html
# Good explainer:       https://pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_test_images():
    """Create 8 synthetic images: 4 warm-toned, 4 cool-toned."""
    images, labels = [], []
    for i in range(4):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 2] = np.random.randint(150, 230)  # red channel high
        img[:, :, 1] = np.random.randint(80, 140)
        img[:, :, 0] = np.random.randint(20, 60)
        images.append(img); labels.append(f'warm_{i}')
    for i in range(4):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = np.random.randint(150, 230)  # blue channel high
        img[:, :, 1] = np.random.randint(80, 140)
        img[:, :, 2] = np.random.randint(20, 60)
        images.append(img); labels.append(f'cool_{i}')
    return images, labels

images, labels = make_test_images()

# ─────────────────────────────────────────────
# STEP 1 — Compute a color histogram for one image
# ─────────────────────────────────────────────
# YOUR TASK: Write compute_histogram(img)
# Use all 3 BGR channels, 32 bins per channel, range 0-256
# Normalize with cv2.normalize so histograms are comparable across image sizes

def compute_histogram(img, bins=32):
    """
    Returns a normalized concatenated histogram of all 3 channels.
    Shape: (bins * 3,) — a 1D feature vector.
    """
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 2 — Compare two histograms
# ─────────────────────────────────────────────
# YOUR TASK: Write compare_histograms(hist1, hist2)
# Use cv2.compareHist with cv2.HISTCMP_BHATTACHARYYA
# Returns a distance: 0 = identical, 1 = completely different

def compare_histograms(hist1, hist2):
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 3 — Find top-K matches for a query image
# ─────────────────────────────────────────────
def find_similar(query_img, database_imgs, database_labels, top_k=3):
    """
    Returns top_k most similar images (label, distance) sorted by distance.
    """
    query_hist = compute_histogram(query_img)
    scores = []
    for img, label in zip(database_imgs, database_labels):
        hist = compute_histogram(img)
        dist = compare_histograms(query_hist, hist)
        if dist is not None:
            scores.append((label, dist, img))
    scores.sort(key=lambda x: x[1])
    return scores[:top_k]

# Test: query with a warm image, should find other warm images
query = images[0]
results = find_similar(query, images[1:], labels[1:], top_k=3)

if results:
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(cv2.cvtColor(query, cv2.COLOR_BGR2RGB)); axes[0].set_title('Query'); axes[0].axis('off')
    for i, (label, dist, img) in enumerate(results):
        axes[i+1].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[i+1].set_title(f'{label}\ndist={dist:.3f}'); axes[i+1].axis('off')
    plt.tight_layout(); plt.savefig('../outputs/day45_histogram_match.png'); plt.show()
    print("Saved → outputs/day45_histogram_match.png")

# REFLECTION
# Q1: Why do we normalize histograms before comparing?
# A1:
# Q2: What kind of images would fool this approach (same histogram but look different)?
# A2:

# WHERE THIS LEADS:
# Histograms capture color but not shape or texture.
# Day 46 uses ORB features — robust to rotation and scale changes.
