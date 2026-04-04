# Day 52 | Week 8: People Counter
# Topic:  Background Subtraction
# Goal:   Separate moving objects from the static background
# Output: outputs/day52_bg_subtraction.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Background subtraction: maintain a model of the "empty" background,
# then flag pixels that deviate significantly as foreground (moving objects).
#
# Two approaches:
#   1. Frame differencing (Day 42) — simple, no memory of background
#   2. MOG2 (Mixture of Gaussians) — OpenCV's built-in, handles gradual lighting changes
#
# cv2.createBackgroundSubtractorMOG2() — learns background over time.
# Feed it frames; it gets better as it sees more of the static background.

# RESOURCES
# Background subtraction: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html
# MOG2 explained:         https://docs.opencv.org/4.x/d7/d7b/classcv_1_1BackgroundSubtractorMOG2.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_people_video(n_frames=20, n_people=3):
    """Synthetic video: circles = people moving across frame left to right."""
    np.random.seed(42)
    people = [{'x': np.random.randint(-40, 0), 'y': np.random.randint(60, 240),
               'speed': np.random.randint(12, 22), 'r': np.random.randint(18, 28),
               'color': tuple(np.random.randint(60,200,3).tolist())} for _ in range(n_people)]
    frames = []
    for _ in range(n_frames):
        frame = np.ones((300, 400, 3), dtype=np.uint8) * 190
        for y in range(0, 300, 50):
            cv2.line(frame, (0,y), (400,y), (170,170,170), 1)
        for p in people:
            if 0 <= p['x'] <= 440:
                cv2.circle(frame, (int(p['x']), p['y']), p['r'], p['color'], -1)
            p['x'] += p['speed']
            if p['x'] > 440: p['x'] = -40
        frames.append(frame)
    return frames

frames = make_people_video()

# ─────────────────────────────────────────────
# STEP 1 — MOG2 Background Subtractor
# ─────────────────────────────────────────────
# YOUR TASK: Apply MOG2 to the video frames
# Steps:
#   1. Create: bg_sub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=40)
#   2. For each frame: fg_mask = bg_sub.apply(frame)
#      fg_mask: 255 = foreground (moving), 0 = background
#   3. Clean mask: morphological opening to remove noise

def apply_mog2(frames):
    """Returns list of foreground masks, one per frame."""
    bg_sub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=40, detectShadows=False)
    masks = []
    kernel = np.ones((5,5), np.uint8)
    for frame in frames:
        fg = bg_sub.apply(frame)
        # YOUR CODE — clean mask with morphological opening
        cleaned = None  # YOUR CODE
        masks.append(cleaned if cleaned is not None else fg)
    return masks

fg_masks = apply_mog2(frames)

# ─────────────────────────────────────────────
# STEP 2 — Compare frame differencing vs MOG2
# ─────────────────────────────────────────────
def frame_diff(f1, f2, threshold=25):
    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(g1, g2)
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return mask

diff_mask = frame_diff(frames[8], frames[9])
mog2_mask = fg_masks[9] if fg_masks else None

if mog2_mask is not None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(cv2.cvtColor(frames[9], cv2.COLOR_BGR2RGB)); axes[0].set_title('Frame 9'); axes[0].axis('off')
    axes[1].imshow(diff_mask, cmap='gray'); axes[1].set_title('Frame Diff'); axes[1].axis('off')
    axes[2].imshow(mog2_mask, cmap='gray'); axes[2].set_title('MOG2'); axes[2].axis('off')
    plt.tight_layout(); plt.savefig('../outputs/day52_bg_subtraction.png'); plt.show()
    print("Saved → outputs/day52_bg_subtraction.png")

# REFLECTION
# Q1: Why does MOG2 give a cleaner mask than frame differencing?
# A1:
# Q2: What does the `history` parameter in MOG2 control?
# A2:
