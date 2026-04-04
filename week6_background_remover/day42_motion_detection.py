# Day 42 | Week 6: Background Remover
# Topic:  Motion Detection via Frame Differencing
# Goal:   Detect which pixels are moving across video frames
# Output: outputs/day42_motion.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Virtual backgrounds in video need to track what's moving each frame.
# Frame differencing: subtract consecutive frames → large diff = motion.
#
# Pipeline:
#   frame_t, frame_t+1 → grayscale both → |diff| → threshold → motion mask
#
# Limitation: only detects motion relative to the previous frame.
# Day 52 (Week 8) will use background subtraction, which is more robust.

# RESOURCES
# Frame differencing:      https://learnopencv.com/video-stabilization-using-point-feature-matching-in-opencv/
# Background subtraction:  https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_synthetic_video(n_frames=10):
    """Generate frames with a moving circle (simulates a person walking)."""
    frames = []
    for i in range(n_frames):
        frame = np.ones((300, 400, 3), dtype=np.uint8) * 180
        # Add some static background texture
        for y in range(0, 300, 40):
            cv2.line(frame, (0, y), (400, y), (160, 160, 160), 1)
        # Moving circle (subject)
        cx = 50 + i * 30
        cv2.circle(frame, (cx, 150), 50, (80, 120, 200), -1)
        frames.append(frame)
    return frames

frames = make_synthetic_video(n_frames=10)

# ─────────────────────────────────────────────
# STEP 1 — Frame differencing
# ─────────────────────────────────────────────
# YOUR TASK: Write detect_motion(frame1, frame2, threshold=25)
# Steps:
#   1. Convert both frames to grayscale
#   2. Compute absolute difference: cv2.absdiff(gray1, gray2)
#   3. Threshold the diff: pixels > threshold → 255 (motion), else 0
#   4. Clean up with morphological dilation to fill gaps
#   5. Return the motion mask

def detect_motion(frame1, frame2, threshold=25):
    """
    Returns a binary mask where 255 = motion detected.
    """
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 2 — Apply to video frames
# ─────────────────────────────────────────────
# YOUR TASK: Run detect_motion on consecutive frame pairs
# Collect the masks and overlay them on the frames for visualization

motion_results = []
for i in range(len(frames) - 1):
    mask = detect_motion(frames[i], frames[i+1])
    if mask is not None:
        vis = frames[i+1].copy()
        # Tint moving areas red
        vis[mask == 255] = (0, 0, 220)
        motion_results.append((frames[i+1], mask, vis))

# ─────────────────────────────────────────────
# STEP 3 — Display a few frames
# ─────────────────────────────────────────────
if motion_results:
    fig, axes = plt.subplots(3, 3, figsize=(12, 9))
    for i, (frame, mask, vis) in enumerate(motion_results[:3]):
        axes[i][0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)); axes[i][0].set_title(f'Frame {i+1}'); axes[i][0].axis('off')
        axes[i][1].imshow(mask, cmap='gray'); axes[i][1].set_title('Motion mask'); axes[i][1].axis('off')
        axes[i][2].imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)); axes[i][2].set_title('Detected'); axes[i][2].axis('off')
    plt.tight_layout(); plt.show()
    cv2.imwrite('../outputs/day42_motion.png', motion_results[0][2])
    print("Saved → outputs/day42_motion.png")

# REFLECTION
# Q1: Why does frame differencing fail when the subject is stationary?
# A1:
# Q2: How would you reduce false positives from camera shake?
# A2:

# WHERE THIS LEADS:
# Day 42 wraps up the building blocks for Week 6.
# The project combines everything into virtual_bg_app(person_photo, background_photo).
