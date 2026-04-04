# Days 57-58 | Week 8: People Counter
# Topic:  Speed Estimation
# Goal:   Measure how fast tracked objects are moving (pixels/frame)
# Output: outputs/day57_speed.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Now that you're tracking, you can measure speed.
# Speed = distance moved per frame = |pos[t] - pos[t-1]|
# Smooth it over a window to avoid jitter from noisy detections.
#
# Real-world conversion:
#   If you know the camera's field of view (e.g. 5 meters wide = 400 pixels)
#   then pixels/frame × (5/400) × fps = meters/second

# RESOURCES
# np.linalg.norm: https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
# Smoothing:      https://numpy.org/doc/stable/reference/generated/numpy.convolve.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# STEP 1 — Compute speed from position history
# ─────────────────────────────────────────────
def compute_speed(positions, smooth_window=3):
    """
    positions: list of (x, y) centroids over time
    Returns: list of speeds (pixels/frame), same length as positions.
             First value is 0 (no previous position to compare).

    Steps:
      1. For each consecutive pair, compute Euclidean distance
      2. Apply a moving average with smooth_window to reduce jitter
         Use np.convolve(speeds, np.ones(w)/w, mode='same')
    """
    if len(positions) < 2:
        return [0.0] * len(positions)

    # YOUR CODE HERE
    pass

# Test
test_positions = [(50 + i*15, 100 + i*3) for i in range(20)]
speeds = compute_speed(test_positions, smooth_window=3)
if speeds:
    print(f"Sample speeds: {[f'{s:.1f}' for s in speeds[:5]]} px/frame")

# ─────────────────────────────────────────────
# STEP 2 — Attach speed computation to tracker
# ─────────────────────────────────────────────
# Each track already stores 'positions' (list of centroids).
# Write get_track_speed(track, smooth_window=3) that returns
# the current speed of a track (last value from compute_speed).

def get_track_speed(track, smooth_window=3):
    """Returns current speed of a track in pixels/frame."""
    positions = track.get('positions', [])
    speeds = compute_speed(positions, smooth_window)
    if speeds:
        return speeds[-1]
    return 0.0

# ─────────────────────────────────────────────
# STEP 3 — Visualize speed on tracked frames
# ─────────────────────────────────────────────
# Simulate tracks with known speeds
from day54_object_tracker import SimpleTracker

def make_speed_video(n_frames=25):
    people = [
        {'x': 20,  'y': 80,  'speed': 10},  # slow
        {'x': 20,  'y': 160, 'speed': 20},  # medium
        {'x': 20,  'y': 240, 'speed': 35},  # fast
    ]
    all_dets = []
    for _ in range(n_frames):
        dets = []
        for p in people:
            x, y = int(p['x']), p['y']
            if 0 <= x <= 450:
                dets.append({'bbox': (x-18,y-18,36,36), 'centroid': (x,y), 'area': 324})
            p['x'] += p['speed']
        all_dets.append(dets)
    return all_dets

tracker  = SimpleTracker(iou_threshold=0.2)
all_dets = make_speed_video()
frames_vis = []

for dets in all_dets:
    tracks = tracker.update(dets)
    frame  = np.ones((300, 500, 3), dtype=np.uint8) * 190
    colors = [(255,80,80),(80,255,80),(80,80,255)]
    for tid, t in tracks.items():
        x, y, w, h = t['bbox']
        spd = get_track_speed(t, smooth_window=3)
        color = colors[tid % len(colors)]
        cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
        cv2.putText(frame, f'ID:{tid} {spd:.0f}px/f',
                    (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        # Draw trail
        positions = t.get('positions', [])
        for pi in range(1, len(positions)):
            p1 = (int(positions[pi-1][0]), int(positions[pi-1][1]))
            p2 = (int(positions[pi][0]),   int(positions[pi][1]))
            cv2.line(frame, p1, p2, color, 1)
    frames_vis.append(frame)

if frames_vis:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for i, fi in enumerate([5, 12, 22]):
        axes[i].imshow(cv2.cvtColor(frames_vis[fi], cv2.COLOR_BGR2RGB))
        axes[i].set_title(f'Frame {fi}'); axes[i].axis('off')
    plt.tight_layout()
    plt.savefig('../outputs/day57_speed.png'); plt.show()
    print("Saved → outputs/day57_speed.png")

# REFLECTION
# Q1: Why do we smooth the speed instead of using raw frame-to-frame distance?
# A1:
# Q2: How would you convert pixels/frame to km/h given camera FOV and FPS?
# A2:
