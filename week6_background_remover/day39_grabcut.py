# Day 39 | Week 6: Background Remover
# Topic:  GrabCut — Smart Background Removal
# Goal:   Remove background from a real photo using GrabCut
# Output: outputs/day39_grabcut.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# GrabCut is how Photoshop's "remove background" works.
# You give it a bounding box around the subject — it figures out fg vs bg.
#
# How it works internally (you don't need to implement this):
#   1. Pixels outside the box → definitely background
#   2. Pixels inside → could be fg or bg
#   3. It models color distributions of fg and bg using Gaussian Mixture Models
#   4. Iterates to refine the boundary
#
# You just need: cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode)

# RESOURCES
# GrabCut tutorial: https://docs.opencv.org/4.x/d8/d83/tutorial_py_grabcut.html
# Deep dive:        https://learnopencv.com/grabcut-foreground-extraction-using-opencv/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def show_many(imgs, titles, cmaps=None):
    fig, axes = plt.subplots(1, len(imgs), figsize=(5 * len(imgs), 4))
    if len(imgs) == 1: axes = [axes]
    cmaps = cmaps or [None] * len(imgs)
    for ax, img, title, cmap in zip(axes, imgs, titles, cmaps):
        ax.set_title(title); ax.axis('off')
        if cmap:
            ax.imshow(img, cmap=cmap)
        else:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape)==3 else img)
    plt.tight_layout(); plt.show()

def make_test_scene():
    """Synthetic scene: colored subject on textured background."""
    scene = np.zeros((300, 400, 3), dtype=np.uint8)
    # Noisy background
    noise = np.random.randint(30, 80, scene.shape, dtype=np.uint8)
    scene = noise.copy()
    scene[:, :, 1] = (noise[:, :, 1] * 0.6).astype(np.uint8)  # greenish bg
    # Subject: person-like blob in center
    cv2.ellipse(scene, (200, 150), (80, 110), 0, 0, 360, (180, 120, 90), -1)   # body
    cv2.circle(scene, (200, 60), 40, (200, 160, 130), -1)                        # head
    return scene

img = make_test_scene()
# img = cv2.imread('scene.jpg')   # use a real image if you have one
h, w = img.shape[:2]

# ─────────────────────────────────────────────
# STEP 1 — Run GrabCut
# ─────────────────────────────────────────────
# YOUR TASK: Write grabcut_remove_bg(img, margin=0.1)
#
# Key steps:
#   1. Define rect = (x, y, width, height) leaving margin% on each side
#   2. Create mask, bgdModel, fgdModel (all zeros with specific shapes/types)
#   3. Run cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
#   4. Build binary mask: pixels where mask == cv2.GC_FGD or mask == cv2.GC_PR_FGD → 255
#   5. Return (foreground_img, binary_mask)
#
# GrabCut mask values:
#   cv2.GC_BGD (0)    = definite background
#   cv2.GC_FGD (1)    = definite foreground
#   cv2.GC_PR_BGD (2) = probable background
#   cv2.GC_PR_FGD (3) = probable foreground

def grabcut_remove_bg(img, margin=0.1):
    """
    margin: fraction of image edges to treat as definite background
    Returns: (foreground_img, binary_mask)
    """
    # YOUR CODE HERE
    pass

fg_img, mask = grabcut_remove_bg(img, margin=0.1)

# ─────────────────────────────────────────────
# STEP 2 — Clean up the mask
# ─────────────────────────────────────────────
# YOUR TASK: Remove small noise and fill small holes in the mask
# Use morphological operations:
#   kernel = np.ones((5,5), np.uint8)
#   cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)   # fill holes
#   cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)  # remove noise

def clean_mask(mask, kernel_size=5):
    """Remove noise and fill holes in a binary mask."""
    # YOUR CODE HERE
    pass

cleaned_mask = clean_mask(mask) if mask is not None else None

# ─────────────────────────────────────────────
# STEP 3 — Apply mask to get clean foreground
# ─────────────────────────────────────────────
if cleaned_mask is not None:
    result = cv2.bitwise_and(img, img, mask=cleaned_mask)
    show_many(
        [img, mask, cleaned_mask, result],
        ['Original', 'Raw GrabCut mask', 'Cleaned mask', 'Foreground'],
        cmaps=[None, 'gray', 'gray', None]
    )
    cv2.imwrite('../outputs/day39_grabcut.png', result)
    print("Saved → outputs/day39_grabcut.png")

# REFLECTION
# Q1: What does increasing the number of GrabCut iterations do?
# A1:
# Q2: What happens if your margin is too small (e.g. 0.02)?
# A2:

# WHERE THIS LEADS:
# GrabCut masks have hard jagged edges. Day 40 fixes this with feathering —
# blurring the mask to create smooth transitions between subject and background.
