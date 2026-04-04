# Day 49 | Week 7: Image Search Engine
# Topic:  Feature Normalization + Cosine Similarity
# Goal:   Make combined features (color + HOG) work properly together
# Output: outputs/day49_similarity_matrix.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Day 47 question: "What if color features have values 0-10000
# but HOG features have values 0-1? The color feature dominates."
# Fix: normalize each feature to unit length before combining.
#
# Also: cosine similarity measures the ANGLE between vectors.
# L2 distance is affected by magnitude; cosine is not.
# For image search, cosine similarity is usually better.
#
# This is EXACTLY how neural embedding search works (FAISS, Pinecone etc.)

# RESOURCES
# Feature normalization: https://scikit-learn.org/stable/modules/preprocessing.html
# Cosine similarity:     https://en.wikipedia.org/wiki/Cosine_similarity

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.feature import hog as skimage_hog

os.makedirs('../outputs', exist_ok=True)

def make_test_images():
    imgs, labels = {}, []
    cats = [('red', (0,0,200)), ('blue', (200,0,0)), ('green', (0,200,0))]
    for name, color in cats:
        for i in range(4):
            img = np.ones((64,64,3), dtype=np.uint8) * 200
            cv2.circle(img, (32,32), 20+i, color, -1)
            imgs[f'{name}_{i}'] = img
    return imgs

db = make_test_images()

# ─────────────────────────────────────────────
# STEP 1 — L2 Normalization
# ─────────────────────────────────────────────
def l2_normalize(vec):
    """Scale vector so its L2 norm = 1.0"""
    norm = np.linalg.norm(vec)
    if norm == 0: return vec
    return vec / norm

# ─────────────────────────────────────────────
# STEP 2 — Combined feature: histogram + HOG, both normalized
# ─────────────────────────────────────────────
def extract_combined_features(img):
    """
    Returns a normalized combined feature vector.
    Steps:
      1. Compute color histogram (flatten all channels, 32 bins each)
      2. Compute HOG on 64x64 grayscale
      3. L2 normalize each separately
      4. Concatenate and L2 normalize the combined vector
    """
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 3 — Cosine Similarity
# ─────────────────────────────────────────────
def cosine_similarity(vec1, vec2):
    """
    Returns similarity in [0, 1] where 1 = identical direction.
    Formula: (v1 · v2) / (|v1| * |v2|)
    Note: if vectors are already L2-normalized, this simplifies to np.dot(v1, v2)
    """
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 4 — Build similarity matrix and visualize
# ─────────────────────────────────────────────
# YOUR TASK: Compute pairwise cosine similarity between all 12 images
# Store in a 12x12 matrix. Then visualize as a heatmap.
# You should see 3 blocks of high similarity along the diagonal
# (red-red, blue-blue, green-green).

names = list(db.keys())
features = {n: extract_combined_features(img) for n, img in db.items()}
n = len(names)
sim_matrix = np.zeros((n, n))

for i, n1 in enumerate(names):
    for j, n2 in enumerate(names):
        if features[n1] is not None and features[n2] is not None:
            sim_matrix[i, j] = cosine_similarity(features[n1], features[n2]) or 0

plt.figure(figsize=(8, 6))
plt.imshow(sim_matrix, cmap='viridis', vmin=0, vmax=1)
plt.colorbar(label='Cosine similarity')
plt.xticks(range(n), names, rotation=90, fontsize=7)
plt.yticks(range(n), names, fontsize=7)
plt.title('Pairwise image similarity matrix')
plt.tight_layout()
plt.savefig('../outputs/day49_similarity_matrix.png'); plt.show()
print("Saved → outputs/day49_similarity_matrix.png")

# REFLECTION
# Q1: Why do we L2-normalize each feature BEFORE concatenating them?
# A1:
# Q2: What's the difference between L2 distance and cosine similarity?
#     When would you prefer each?
# A2:

# WHERE THIS LEADS:
# This normalized vector + cosine similarity is EXACTLY how
# embedding databases (FAISS, Pinecone, Weaviate) work with CNN features.
# When you replace extract_combined_features() with a pretrained ResNet,
# the search code stays identical.
