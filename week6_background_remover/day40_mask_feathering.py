# Day 40 | Week 6: Background Remover
# Topic:  Edge-Aware Mask Feathering
# Goal:   Smooth the hard edges of a GrabCut mask for natural-looking composites
# Output: outputs/day40_feathered.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# GrabCut gives you a binary mask (0 or 255) — the edges look jagged and fake.
# Real apps use a "feathered" mask: the edges fade gradually from 255 → 0.
# Technique: Gaussian blur the mask → use the blurred float values (0.0–1.0)
# as per-pixel blend weights instead of a hard cut.

# RESOURCES
# Mask feathering: https://learnopencv.com/alpha-blending-using-opencv-cpp-python/
# Compositing:     https://pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/

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

# Reuse the synthetic scene from Day 39
def make_test_scene():
    scene = np.random.randint(30, 80, (300, 400, 3), dtype=np.uint8)
    scene[:, :, 1] = (scene[:, :, 1] * 0.6).astype(np.uint8)
    cv2.ellipse(scene, (200, 150), (80, 110), 0, 0, 360, (180, 120, 90), -1)
    cv2.circle(scene, (200, 60), 40, (200, 160, 130), -1)
    return scene

def make_binary_mask(img):
    """Simple threshold to simulate a GrabCut mask."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    return mask

img  = make_test_scene()
mask = make_binary_mask(img)

# ─────────────────────────────────────────────
# STEP 1 — Feather the mask
# ─────────────────────────────────────────────
# YOUR TASK: Write feather_mask(mask, blur_radius=15)
# Steps:
#   1. Convert mask to float32, divide by 255 → values 0.0 to 1.0
#   2. Apply cv2.GaussianBlur with kernel size (blur_radius*2+1, blur_radius*2+1)
#   3. Return the blurred float mask

def feather_mask(mask, blur_radius=15):
    """
    mask: uint8 binary mask (0 or 255)
    Returns: float32 mask (0.0–1.0) with soft edges
    """
    # YOUR CODE HERE
    pass

soft_mask = feather_mask(mask, blur_radius=15)

# ─────────────────────────────────────────────
# STEP 2 — Composite using feathered mask
# ─────────────────────────────────────────────
# YOUR TASK: Blend subject onto a white background using the soft mask
# Formula per pixel: result = subject * alpha + background * (1 - alpha)
# where alpha = soft_mask value at that pixel

def composite(subject, soft_mask, background_color=(255, 255, 255)):
    """Alpha-blend subject onto background using a soft float mask."""
    bg = np.full_like(subject, background_color, dtype=np.float32)
    fg = subject.astype(np.float32)
    alpha = soft_mask[:, :, np.newaxis]  # expand to 3 channels
    # YOUR CODE HERE — blend fg and bg using alpha
    pass

result_hard = cv2.bitwise_and(img, img, mask=mask)
result_soft = composite(img, soft_mask) if soft_mask is not None else None

if result_soft is not None:
    result_soft_uint8 = np.clip(result_soft, 0, 255).astype(np.uint8)
    show_many(
        [img, mask, result_hard, result_soft_uint8],
        ['Original', 'Hard mask', 'Hard composite', 'Feathered composite'],
        cmaps=[None, 'gray', None, None]
    )
    cv2.imwrite('../outputs/day40_feathered.png', result_soft_uint8)
    print("Saved → outputs/day40_feathered.png")

# REFLECTION
# Q1: What happens to the edges as you increase blur_radius?
# A1:
# Q2: Why do we expand soft_mask to 3 channels before blending?
# A2:
