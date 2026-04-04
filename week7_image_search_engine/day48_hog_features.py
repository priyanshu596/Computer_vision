# Day 48 | Week 7: Image Search Engine
# Topic:  HOG Features — Shape-Based Image Fingerprinting
# Goal:   Extract HOG descriptors and use them for image search
# Output: outputs/day48_hog.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# HOG = Histogram of Oriented Gradients.
# Instead of color, it captures the SHAPE of objects by looking at
# which direction edges point in small patches of the image.
# This is what made human detection possible before deep learning.
#
# How it works:
#   1. Compute gradients (edge directions) across the image
#   2. Divide image into small cells (e.g. 8x8 pixels)
#   3. In each cell, build a histogram of gradient orientations (9 bins)
#   4. Group cells into blocks, normalize → HOG descriptor
#
# Key property: robust to lighting changes, captures shape not color.

# RESOURCES
# HOG explained: https://learnopencv.com/histogram-of-oriented-gradients/
# skimage HOG:   https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.hog
# Original paper: https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.feature import hog as skimage_hog
from skimage import exposure

os.makedirs('../outputs', exist_ok=True)

def make_shape_images():
    """Images where shape matters more than color."""
    imgs = {}
    # Circle family
    for i in range(3):
        img = np.ones((64, 64, 3), dtype=np.uint8) * 220
        cv2.circle(img, (32, 32), 20 + i*2, (80 + i*30, 40, 40), -1)
        imgs[f'circle_{i}'] = img
    # Rectangle family
    for i in range(3):
        img = np.ones((64, 64, 3), dtype=np.uint8) * 220
        cv2.rectangle(img, (12+i, 12+i), (52-i, 52-i), (40, 80+i*30, 40), -1)
        imgs[f'rect_{i}'] = img
    # Triangle family
    for i in range(3):
        img = np.ones((64, 64, 3), dtype=np.uint8) * 220
        pts = np.array([[32, 10+i], [55-i, 55], [10+i, 55]])
        cv2.fillPoly(img, [pts], (40, 40, 80+i*30))
        imgs[f'tri_{i}'] = img
    return imgs

shape_imgs = make_shape_images()

# ─────────────────────────────────────────────
# STEP 1 — Compute HOG for one image
# ─────────────────────────────────────────────
# YOUR TASK: Write compute_hog(img, resize_to=(64,64))
# Steps:
#   1. Convert to grayscale
#   2. Resize to resize_to (HOG needs fixed input size)
#   3. Call skimage_hog(gray, orientations=9, pixels_per_cell=(8,8),
#                       cells_per_block=(2,2), visualize=True)
#   4. Returns (feature_vector, hog_image)

def compute_hog(img, resize_to=(64, 64)):
    """Returns (hog_vector, hog_visualization_image)"""
    # YOUR CODE HERE
    pass

# Test on one image
sample = list(shape_imgs.values())[0]
hog_vec, hog_vis = compute_hog(sample) or (None, None)
if hog_vec is not None:
    print(f"HOG vector length: {len(hog_vec)}")

# ─────────────────────────────────────────────
# STEP 2 — Visualize HOG
# ─────────────────────────────────────────────
# The HOG visualization shows gradient direction arrows — you can
# see WHY a circle and a rectangle have different HOG descriptors.

if hog_vis is not None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for i, (name, img) in enumerate(list(shape_imgs.items())[:3]):
        vec, vis = compute_hog(img) or (None, None)
        if vis is not None:
            hog_rescaled = exposure.rescale_intensity(vis, in_range=(0, 10))
            axes[i].imshow(hog_rescaled, cmap='gray')
            axes[i].set_title(f'HOG: {name}'); axes[i].axis('off')
    plt.tight_layout()
    plt.savefig('../outputs/day48_hog.png'); plt.show()
    print("Saved → outputs/day48_hog.png")

# ─────────────────────────────────────────────
# STEP 3 — HOG-based image search
# ─────────────────────────────────────────────
# YOUR TASK: Build a small HOG index and search it
# Same structure as Day 47 but using HOG vectors instead of color histograms

hog_index = {}
for name, img in shape_imgs.items():
    result = compute_hog(img)
    if result is not None:
        hog_index[name] = result[0]

def hog_search(query_img, index, top_k=3):
    """Find most similar images by HOG vector L2 distance."""
    result = compute_hog(query_img)
    if result is None: return []
    query_vec = result[0]
    scores = [(name, np.linalg.norm(query_vec - vec)) for name, vec in index.items()]
    scores.sort(key=lambda x: x[1])
    return scores[:top_k]

query = shape_imgs['circle_0']
matches = hog_search(query, hog_index, top_k=3)
print("HOG search results:", [(n, f'{d:.3f}') for n,d in matches])

# REFLECTION
# Q1: Why does HOG capture shape better than color histograms?
# A1:
# Q2: What does pixels_per_cell control? What happens if it's too small?
# A2:

# WHERE THIS LEADS:
# HOG is a hand-designed feature. CNN features (from ResNet etc.) are
# like HOG but learned from millions of images — much more powerful.
# The search mechanism (L2 distance on vectors) is IDENTICAL.
