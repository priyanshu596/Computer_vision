# Day 59 | Week 8: People Counter
# Topic:  Live Stats Dashboard (On-Frame Display)
# Goal:   Draw real-time stats directly onto video frames
# Output: outputs/day59_dashboard.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# Real surveillance systems show stats overlaid on the video itself.
# You'll build draw_dashboard(frame, stats_dict) that draws:
#   - A semi-transparent panel (top or side)
#   - Active object count, total counted, current frame number
#   - A mini speed bar for the fastest moving object
#   - Color-coded: green = normal, orange = fast, red = very fast

# RESOURCES
# cv2.putText:    https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html
# addWeighted:    https://docs.opencv.org/4.x/d2/de8/group__core__array.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# STEP 1 — Draw the dashboard panel
# ─────────────────────────────────────────────
def draw_dashboard(frame, stats):
    """
    stats = {
        'frame':          int,
        'active_objects': int,
        'total_counted':  int,
        'max_speed':      float  (pixels/frame)
    }
    Returns: annotated frame (does not modify in place)
    """
    result = frame.copy()
    h, w   = result.shape[:2]

    # ── Step 1: Semi-transparent dark panel (top-left corner)
    # YOUR TASK: Draw a filled dark rectangle, then blend with addWeighted
    panel_w, panel_h = 220, 120
    overlay = result.copy()
    cv2.rectangle(overlay, (0, 0), (panel_w, panel_h), (20, 20, 20), -1)
    # YOUR CODE: cv2.addWeighted to blend overlay onto result with alpha=0.65

    # ── Step 2: Text lines inside the panel
    # YOUR TASK: Draw 4 lines of white text using cv2.putText
    # Line 1: f"Frame:   {stats['frame']}"
    # Line 2: f"Active:  {stats['active_objects']}"
    # Line 3: f"Counted: {stats['total_counted']}"
    # Line 4: speed bar (see Step 3)
    font       = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.52
    thickness  = 1
    # YOUR CODE HERE — place text at y=22, 45, 68, 91 with x=10

    # ── Step 3: Speed bar
    # YOUR TASK: Draw a horizontal bar whose width represents max_speed
    # Color: green if < 15, orange if < 30, red if >= 30
    max_spd = stats.get('max_speed', 0)
    bar_max_px = 180
    bar_fill   = int(min(max_spd / 50, 1.0) * bar_max_px)
    if max_spd < 15:
        bar_color = (80, 200, 80)
    elif max_spd < 30:
        bar_color = (40, 160, 240)
    else:
        bar_color = (60, 60, 240)
    # YOUR CODE: draw background bar (gray) then filled bar (bar_color) at y~95

    return result


# ─────────────────────────────────────────────
# STEP 2 — Test with synthetic data
# ─────────────────────────────────────────────
test_frame = np.ones((300, 500, 3), dtype=np.uint8) * 180
# Add some fake people
cv2.circle(test_frame, (120, 150), 30, (80,120,200), -1)
cv2.circle(test_frame, (300, 100), 25, (80,200,120), -1)
cv2.circle(test_frame, (420, 200), 28, (200,120,80), -1)

stats = {
    'frame':          42,
    'active_objects': 3,
    'total_counted':  7,
    'max_speed':      22.5,
}

result = draw_dashboard(test_frame, stats)

plt.figure(figsize=(8, 5))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.axis('off'); plt.title('Stats Dashboard'); plt.tight_layout()
plt.savefig('../outputs/day59_dashboard.png'); plt.show()
print("Saved → outputs/day59_dashboard.png")

# ─────────────────────────────────────────────
# STEP 3 — Try different speed thresholds
# ─────────────────────────────────────────────
# YOUR TASK: Call draw_dashboard 3 times with different max_speed values
# (5.0, 22.0, 45.0) and display side by side to verify color changes work.

speeds    = [5.0, 22.0, 45.0]
speed_vis = []
for spd in speeds:
    s = {**stats, 'max_speed': spd}
    speed_vis.append(draw_dashboard(test_frame, s))

if all(v is not None for v in speed_vis):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, vis, spd in zip(axes, speed_vis, speeds):
        ax.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
        ax.set_title(f'Speed={spd}'); ax.axis('off')
    plt.tight_layout(); plt.show()

# REFLECTION
# Q1: Why use addWeighted for the panel instead of just drawing on the frame?
# A1:
# Q2: How would you add a mini bar chart showing speed history over the last 10 frames?
# A2:

# WHERE THIS LEADS:
# Tomorrow is the Week 8 Final Project — you'll combine all 8 days
# into one PeopleCounter class and run the complete pipeline on a video.
