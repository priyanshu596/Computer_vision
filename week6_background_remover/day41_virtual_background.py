# Day 41 | Week 6: Background Remover
# Topic:  Virtual Background
# Goal:   Replace background with any image
# Output: outputs/day41_virtual_bg.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Combine everything from Days 38-40:
#   subject image + feathered mask + new background image → composite
# The key: resize the background to match the subject before blending.

# RESOURCES
# Alpha blending: https://learnopencv.com/alpha-blending-using-opencv-cpp-python/

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
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape)==3 else img)
    plt.tight_layout(); plt.show()

def make_subject():
    img = np.random.randint(30, 80, (300, 400, 3), dtype=np.uint8)
    img[:, :, 1] = (img[:, :, 1] * 0.5).astype(np.uint8)
    cv2.ellipse(img, (200, 160), (80, 110), 0, 0, 360, (180, 120, 90), -1)
    cv2.circle(img, (200, 65), 40, (200, 160, 130), -1)
    return img

def make_mask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

def feather_mask(mask, blur_radius=15):
    float_mask = mask.astype(np.float32) / 255.0
    k = blur_radius * 2 + 1
    return cv2.GaussianBlur(float_mask, (k, k), 0)

def make_background():
    """Synthetic outdoor background — gradient sky + ground."""
    bg = np.zeros((300, 400, 3), dtype=np.uint8)
    for y in range(200):
        ratio = y / 200
        bg[y, :] = [int(200 * (1-ratio) + 100 * ratio),
                    int(180 * (1-ratio) + 120 * ratio),
                    int(255 * (1-ratio) + 180 * ratio)]
    bg[200:, :] = (60, 120, 50)
    return bg

subject_img = make_subject()
subject_mask = make_mask(subject_img)
bg_img = make_background()

# ─────────────────────────────────────────────
# STEP 1 — Build apply_virtual_bg()
# ─────────────────────────────────────────────
def apply_virtual_bg(subject_img, subject_mask, bg_img):
    """
    subject_img:  BGR image of subject (with old background)
    subject_mask: uint8 binary mask (255 = subject, 0 = background)
    bg_img:       BGR image for new background (any size)
    Returns: composited BGR image
    """
    # Step 1: Resize bg_img to match subject_img dimensions
    # Step 2: Feather the mask
    # Step 3: Alpha blend: result = subject * alpha + bg * (1 - alpha)
    # YOUR CODE HERE
    pass

result = apply_virtual_bg(subject_img, subject_mask, bg_img)

if result is not None:
    result_uint8 = np.clip(result, 0, 255).astype(np.uint8)
    show_many([subject_img, bg_img, result_uint8],
              ['Subject', 'New Background', 'Composited'])
    cv2.imwrite('../outputs/day41_virtual_bg.png', result_uint8)
    print("Saved → outputs/day41_virtual_bg.png")

# REFLECTION
# Q1: What happens if you skip feathering and use a hard mask?
# A1:
# Q2: How would you handle a subject that's larger than the background?
# A2:
