# Days 50-51 | Week 7: Image Search Engine
# Topic:  Duplicate Image Detector
# Goal:   Find near-identical images using perceptual hashing
# Output: outputs/day50_duplicates.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Perceptual hash (pHash): a short fingerprint of image appearance.
# Two near-identical images → very similar hashes (low Hamming distance).
# Much faster than feature vector comparison for exact/near-duplicate detection.
#
# How pHash works:
#   1. Resize to 32x32 grayscale
#   2. Apply DCT (Discrete Cosine Transform) — like JPEG compression
#   3. Keep top-left 8x8 of DCT (low-frequency components = overall structure)
#   4. Compare each value to the median → 64-bit binary hash
#   5. Hamming distance between two hashes = number of differing bits
#      0-5 bits different → near duplicate
#      >10 bits → different image

# RESOURCES
# pHash explained:  https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
# imagehash lib:    https://github.com/JohannesBuchner/imagehash

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_duplicate_set():
    """Return {name: img} with known near-duplicates."""
    imgs = {}
    base_colors = [(0,0,180), (0,180,0), (180,0,0)]

    for ci, color in enumerate(base_colors):
        base = np.ones((64,64,3), dtype=np.uint8) * 220
        cv2.circle(base, (32,32), 25, color, -1)

        # Original
        imgs[f'cat{ci}_original'] = base.copy()

        # Near-duplicate: slight brightness change
        brightened = np.clip(base.astype(np.int16) + 15, 0, 255).astype(np.uint8)
        imgs[f'cat{ci}_bright'] = brightened

        # Near-duplicate: very slight noise
        noisy = base.copy()
        noise = np.random.randint(-8, 8, base.shape, dtype=np.int16)
        noisy = np.clip(noisy.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        imgs[f'cat{ci}_noisy'] = noisy

        # Different: different shape
        diff = np.ones((64,64,3), dtype=np.uint8) * 220
        cv2.rectangle(diff, (12,12), (52,52), color, -1)
        imgs[f'cat{ci}_different'] = diff

    return imgs

db = make_duplicate_set()

# ─────────────────────────────────────────────
# STEP 1 — Compute perceptual hash
# ─────────────────────────────────────────────
def phash(img, hash_size=8):
    """
    Returns a 64-bit perceptual hash as a numpy array of 0s and 1s.
    Steps:
      1. Convert to grayscale
      2. Resize to (hash_size*4, hash_size*4) = 32x32
      3. Apply cv2.dct on float32 version
      4. Crop top-left (hash_size x hash_size) block of DCT
      5. Compute median of the cropped block
      6. Return binary array: 1 where value > median, else 0
    """
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 2 — Hamming distance between two hashes
# ─────────────────────────────────────────────
def hamming_distance(hash1, hash2):
    """Number of bit positions where the hashes differ. Lower = more similar."""
    # YOUR CODE HERE — np.sum(hash1 != hash2)
    pass

# ─────────────────────────────────────────────
# STEP 3 — Find all duplicate pairs
# ─────────────────────────────────────────────
def find_duplicates(image_dict, threshold=5):
    """
    Returns list of (name1, name2, hamming_dist) for all near-duplicate pairs.
    threshold: max Hamming distance to consider as duplicate (0-64)
    """
    names = list(image_dict.keys())
    hashes = {n: phash(img) for n, img in image_dict.items()}
    duplicates = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            h1, h2 = hashes[names[i]], hashes[names[j]]
            if h1 is not None and h2 is not None:
                dist = hamming_distance(h1, h2)
                if dist is not None and dist <= threshold:
                    duplicates.append((names[i], names[j], dist))
    duplicates.sort(key=lambda x: x[2])
    return duplicates

dupes = find_duplicates(db, threshold=8)
print(f"Found {len(dupes)} duplicate pairs:")
for n1, n2, d in dupes:
    print(f"  {n1} ↔ {n2}  (distance={d})")

# ─────────────────────────────────────────────
# STEP 4 — Visualize duplicate pairs
# ─────────────────────────────────────────────
if dupes:
    pairs_to_show = dupes[:4]
    fig, axes = plt.subplots(len(pairs_to_show), 2, figsize=(6, 3*len(pairs_to_show)))
    for i, (n1, n2, d) in enumerate(pairs_to_show):
        for j, (name, img) in enumerate([(n1, db[n1]), (n2, db[n2])]):
            axes[i][j].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[i][j].set_title(f'{name}\ndist={d}', fontsize=8)
            axes[i][j].axis('off')
    plt.tight_layout()
    plt.savefig('../outputs/day50_duplicates.png'); plt.show()
    print("Saved → outputs/day50_duplicates.png")

# REFLECTION
# Q1: Why is pHash faster than comparing full feature vectors?
# A1:
# Q2: What threshold would you use to catch edited duplicates vs. different images?
# A2:
