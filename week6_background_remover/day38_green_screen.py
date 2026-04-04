# Day 38 | Week 6: Background Remover
# Topic:  Green Screen (Chroma Key) Remover
# Goal:   Remove a solid-color background using color masking
# Output: outputs/day38_green_screen.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# The simplest background remover: if the background is one color, mask it out.
# This is how green screens work in film/TV.
#
# Key insight: work in HSV color space, not BGR.
# HSV separates color (Hue) from brightness (Value) — makes color ranges
# much easier to define. Green in HSV is roughly H: 40-80, S: 50-255, V: 50-255.
#
# Pipeline:
#   BGR image → HSV → cv2.inRange(hsv, lower, upper) → mask → invert → apply

# RESOURCES
# HSV color space:  https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
# inRange:          https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html
# Green screen:     https://learnopencv.com/background-removal-using-a-green-screen/

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

# ─────────────────────────────────────────────
# STEP 1 — Create a test image
# ─────────────────────────────────────────────
# Synthetic: red circle + blue rectangle on green background
test_img = np.zeros((300, 400, 3), dtype=np.uint8)
test_img[:] = (0, 180, 0)               # green background (BGR)
cv2.circle(test_img, (200, 150), 80, (0, 0, 220), -1)        # red circle
cv2.rectangle(test_img, (30, 80), (120, 220), (220, 100, 0), -1)  # blue rect

# ─────────────────────────────────────────────
# STEP 2 — Convert to HSV
# ─────────────────────────────────────────────
# YOUR TASK: Convert test_img to HSV color space
# Why HSV? The Hue channel isolates color regardless of lighting.

hsv = None  # YOUR CODE: cv2.cvtColor(...)

# ─────────────────────────────────────────────
# STEP 3 — Create the background mask
# ─────────────────────────────────────────────
# YOUR TASK: Use cv2.inRange to mask the green background
# Green in HSV: Hue ~40-80, Saturation ~50-255, Value ~50-255
# lower = np.array([40, 50, 50])
# upper = np.array([80, 255, 255])
# mask = cv2.inRange(hsv, lower, upper)
# mask = 255 where green, 0 elsewhere

bg_mask      = None  # YOUR CODE — pixels that ARE background
subject_mask = None  # YOUR CODE — invert bg_mask to get subject

# ─────────────────────────────────────────────
# STEP 4 — Build remove_green_screen()
# ─────────────────────────────────────────────
def remove_green_screen(img, bg_color_hsv_lower, bg_color_hsv_upper, tolerance=20):
    """
    img:                BGR image with solid color background
    bg_color_hsv_lower: lower HSV bound e.g. np.array([40, 50, 50])
    bg_color_hsv_upper: upper HSV bound e.g. np.array([80, 255, 255])
    Returns: (subject_img, subject_mask)
             subject_img has black where background was
    """
    # YOUR CODE HERE
    pass

# Test it
lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])
subject_img, mask = remove_green_screen(test_img, lower_green, upper_green)

# ─────────────────────────────────────────────
# STEP 5 — Replace background with white
# ─────────────────────────────────────────────
# YOUR TASK: Create a white background version
# Hint: make a white canvas, paste subject_img where mask is 255

def replace_background(subject_img, mask, bg_color=(255, 255, 255)):
    """Replaces masked-out area with a solid color."""
    result = np.full_like(subject_img, bg_color)
    # YOUR CODE HERE — paste subject where mask is non-zero
    pass

result_white_bg = replace_background(subject_img, mask)

if subject_img is not None:
    show_many(
        [test_img, mask, subject_img, result_white_bg],
        ['Original', 'BG Mask', 'Subject only', 'White background'],
        cmaps=[None, 'gray', None, None]
    )
    cv2.imwrite('../outputs/day38_green_screen.png', result_white_bg)
    print("Saved → outputs/day38_green_screen.png")

# REFLECTION
# Q1: Why is HSV better than BGR for color range masking?
# A1:
# Q2: What would you change to remove a blue background instead?
# A2:

# WHERE THIS LEADS:
# Green screen only works when the background is one solid color.
# Day 39 handles real photos using GrabCut — much more powerful.
