# Week 6 Project | Virtual Background App
# Goal:   Complete pipeline — person photo + background photo → composited result
# Output: outputs/week6_virtual_bg.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# YOUR TASK
# Build virtual_bg_app(person_photo, background_photo) that:
#   1. Removes the background from person_photo using GrabCut
#   2. Refines the mask with morphological ops
#   3. Feathers the mask edges
#   4. Adds a soft drop shadow (bonus — see add_shadow below)
#   5. Composites person onto background_photo
#   6. Returns the final composited image

# KAGGLE PUBLISH CHECKLIST
# 1. Go to kaggle.com/code → New Notebook
# 2. Paste your working code
# 3. Add markdown: "How GrabCut works" + your pipeline diagram (text is fine)
# 4. Add markdown at bottom: "Where this leads → Mask R-CNN"
# 5. Make public, copy URL into progress/status.json → week6 → kaggle_url
# 6. git add . && git commit -m "Week 6 project done + Kaggle published" && git push

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

# ─────────────────────────────────────────────
# PASTE YOUR BEST IMPLEMENTATIONS FROM DAYS 38-42
# ─────────────────────────────────────────────

def grabcut_remove_bg(img, margin=0.1):
    # YOUR CODE (from Day 39)
    pass

def clean_mask(mask, kernel_size=5):
    # YOUR CODE (from Day 39)
    pass

def feather_mask(mask, blur_radius=15):
    # YOUR CODE (from Day 40)
    pass

# ─────────────────────────────────────────────
# BONUS — Drop Shadow Effect
# ─────────────────────────────────────────────
def add_shadow(subject_img, mask, offset=(8, 8), blur_radius=12, opacity=0.5):
    """
    Adds a soft drop shadow behind the subject.
    offset: (x, y) shadow displacement in pixels
    opacity: 0.0 = invisible, 1.0 = solid black
    Returns: subject_img with shadow added (BGR)
    """
    # YOUR CODE HERE
    # Hint:
    #   1. Create a black canvas same size as subject_img
    #   2. Shift the mask by offset using np.roll or warpAffine
    #   3. Blur the shifted mask heavily
    #   4. Use the blurred mask to paint a semi-transparent dark area
    #   5. Composite shadow behind the subject
    pass

# ─────────────────────────────────────────────
# THE MAIN FUNCTION
# ─────────────────────────────────────────────
def virtual_bg_app(person_photo, background_photo):
    """
    person_photo:     BGR image of a person (with any background)
    background_photo: BGR image for the new background
    Returns: composited BGR image
    """
    # Step 1: Remove background using GrabCut
    # Step 2: Clean + feather the mask
    # Step 3: Add drop shadow (optional but looks great)
    # Step 4: Composite onto background_photo
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# TEST IT
# ─────────────────────────────────────────────
def make_person():
    img = np.random.randint(40, 90, (400, 300, 3), dtype=np.uint8)
    img[:, :, 1] = (img[:, :, 1] * 0.5).astype(np.uint8)
    cv2.ellipse(img, (150, 230), (70, 100), 0, 0, 360, (160, 110, 80), -1)
    cv2.circle(img, (150, 110), 50, (190, 150, 120), -1)
    return img

def make_background():
    bg = np.zeros((400, 300, 3), dtype=np.uint8)
    for y in range(250):
        r = int(y / 250)
        bg[y, :] = [int(220*(1-r)+100*r), int(200*(1-r)+130*r), int(255*(1-r)+180*r)]
    bg[250:, :] = (50, 110, 40)
    cv2.rectangle(bg, (80, 160), (220, 250), (40, 90, 30), -1)
    return bg

person = make_person()
background = make_background()

result = virtual_bg_app(person, background)
if result is not None:
    result_uint8 = np.clip(result, 0, 255).astype(np.uint8)
    show_many([person, background, result_uint8],
              ['Person (original bg)', 'New background', 'Final composite'])
    cv2.imwrite('../outputs/week6_virtual_bg.png', result_uint8)
    print("Saved → outputs/week6_virtual_bg.png")

# WHERE THIS LEADS
# You built this with a handcrafted segmentation algorithm (GrabCut).
# The DL equivalent: Mask R-CNN generates per-pixel masks automatically,
# no bounding box needed, works on any subject.
# Paper: https://arxiv.org/abs/1703.06870
