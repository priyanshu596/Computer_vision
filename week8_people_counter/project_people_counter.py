# Week 8 Final Project | People Counter
# Goal:   Complete pipeline — video frames → annotated output + count stats
# Output: outputs/week8_people_counter.png, outputs/week8_summary.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# YOUR TASK
# Build PeopleCounter class that wraps the full pipeline:
#   Input:  list of video frames
#   Output: annotated frames + final stats dict
#
# Pipeline inside:
#   frame → MOG2 foreground mask → blob detection → SimpleTracker
#         → CountingLine → speed estimation → draw_dashboard

# KAGGLE PUBLISH CHECKLIST
# 1. Go to kaggle.com/code → New Notebook
# 2. Paste your working code
# 3. Add markdown intro: "Building a People Counter with Classical CV"
# 4. Show 3 annotated frames side by side as output
# 5. Add markdown: "Where this leads → YOLO + DeepSORT"
#    Link: https://github.com/nwojke/deep_sort
# 6. Make public → copy URL → progress/status.json → week8 → kaggle_url
# 7. git add . && git commit -m "Week 8 final project done + Kaggle published" && git push

# ── ALSO: OpenCV Contrib PR opportunity ──────────────────────────
# Your PeopleCounter is exactly the kind of sample script OpenCV wants
# in opencv/opencv/samples/python/
# Steps after finishing:
#   1. Fork https://github.com/opencv/opencv
#   2. Add your script to samples/python/people_counter.py
#   3. Add a docstring explaining how to run it
#   4. Open a PR with title: "Add people counter sample using MOG2 + centroid tracking"
# Update progress/status.json → week8 → opencv_pr with your PR URL
# ─────────────────────────────────────────────────────────────────

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# PASTE YOUR BEST CODE FROM DAYS 52-59
# ─────────────────────────────────────────────

def find_blobs(mask, min_area=200):
    # YOUR CODE (from Day 53)
    pass

def compute_speed(positions, smooth_window=3):
    # YOUR CODE (from Day 57)
    pass

def draw_dashboard(frame, stats):
    # YOUR CODE (from Day 59)
    return frame

class SimpleTracker:
    # YOUR CODE (from Day 54) — paste the full class here
    def __init__(self, iou_threshold=0.3, max_missing=5):
        self.tracks    = {}
        self.next_id   = 0
        self.iou_threshold = iou_threshold
        self.max_missing   = max_missing

    def update(self, detections):
        # YOUR CODE
        pass

    def _add_track(self, det):
        self.tracks[self.next_id] = {
            'bbox': det['bbox'], 'centroid': det['centroid'],
            'positions': [det['centroid']], 'missing': 0
        }
        self.next_id += 1

class CountingLine:
    # YOUR CODE (from Day 55) — paste the full class here
    def __init__(self, x_position):
        self.x = x_position
        self.entered = 0
        self.exited  = 0
        self._track_sides = {}

    def update(self, tracks):
        # YOUR CODE
        pass

    def draw(self, frame):
        h = frame.shape[0]
        cv2.line(frame, (self.x, 0), (self.x, h), (0,255,255), 2)
        cv2.putText(frame, f'IN:  {self.entered}', (self.x+8, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80,255,80), 2)
        cv2.putText(frame, f'OUT: {self.exited}',  (self.x+8, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80,80,255), 2)
        return frame


# ─────────────────────────────────────────────
# THE MAIN CLASS
# ─────────────────────────────────────────────

class PeopleCounter:
    def __init__(self, count_line_x=200, min_blob_area=150, max_track_distance=60):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=50, varThreshold=40, detectShadows=False)
        self.tracker     = SimpleTracker(iou_threshold=0.25, max_missing=5)
        self.count_line  = CountingLine(x_position=count_line_x)
        self.min_blob_area = min_blob_area
        self.frame_num   = 0
        self.morph_kernel = np.ones((5,5), np.uint8)

    def process_frame(self, frame):
        """
        Process one frame through the full pipeline.
        Returns annotated frame.
        """
        self.frame_num += 1

        # Step 1: Background subtraction → foreground mask
        fg_mask = self.bg_subtractor.apply(frame)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN,  self.morph_kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, self.morph_kernel)

        # Step 2: Detect blobs
        blobs = find_blobs(fg_mask, min_area=self.min_blob_area)
        detections = [{'bbox': b['bbox'], 'centroid': b['centroid'], 'area': b['area']}
                      for b in (blobs or [])]

        # Step 3: Update tracker
        tracks = self.tracker.update(detections)

        # Step 4: Update counting line
        self.count_line.update(tracks)

        # Step 5: Draw everything
        result = frame.copy()
        colors = [(255,80,80),(80,255,80),(80,80,255),(255,255,80),(255,80,255),(80,255,255)]

        for tid, t in tracks.items():
            x, y, w, h = t['bbox']
            color = colors[tid % len(colors)]
            cv2.rectangle(result, (x,y), (x+w,y+h), color, 2)

            # Draw trail
            for pi in range(1, len(t['positions'])):
                p1 = (int(t['positions'][pi-1][0]), int(t['positions'][pi-1][1]))
                p2 = (int(t['positions'][pi][0]),   int(t['positions'][pi][1]))
                cv2.line(result, p1, p2, color, 1)

            # Speed label
            speeds = compute_speed(t['positions'], smooth_window=3)
            spd = speeds[-1] if speeds else 0
            cv2.putText(result, f'ID:{tid} {spd:.0f}px/f',
                        (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1)

        # Draw counting line
        self.count_line.draw(result)

        # Draw dashboard
        max_spd = 0
        for t in tracks.values():
            spds = compute_speed(t['positions'])
            if spds: max_spd = max(max_spd, spds[-1])

        stats = {
            'frame':          self.frame_num,
            'active_objects': len(tracks),
            'total_counted':  self.count_line.entered + self.count_line.exited,
            'max_speed':      max_spd,
        }
        result = draw_dashboard(result, stats)
        return result

    def run(self, frames):
        """Process all frames, return (annotated_frames, final_stats)."""
        annotated = [self.process_frame(f) for f in frames]
        final_stats = {
            'total_frames':  self.frame_num,
            'entered':       self.count_line.entered,
            'exited':        self.count_line.exited,
            'total_counted': self.count_line.entered + self.count_line.exited,
        }
        return annotated, final_stats


# ─────────────────────────────────────────────
# TEST IT
# ─────────────────────────────────────────────

def make_test_video(n_frames=30, n_people=4):
    np.random.seed(7)
    people = [
        {'x': -30,  'y': 80,  'speed': 14, 'r': 22, 'color': (80,100,200)},
        {'x': 430,  'y': 140, 'speed': -16,'r': 20, 'color': (80,200,100)},
        {'x': -30,  'y': 200, 'speed': 20, 'r': 24, 'color': (200,80,80)},
        {'x': -30,  'y': 250, 'speed': 10, 'r': 18, 'color': (200,200,60)},
    ]
    frames = []
    for _ in range(n_frames):
        frame = np.ones((300, 400, 3), dtype=np.uint8) * 185
        for py in range(0, 300, 50):
            cv2.line(frame, (0,py), (400,py), (165,165,165), 1)
        for p in people:
            if -50 <= p['x'] <= 450:
                cv2.circle(frame, (int(p['x']), p['y']), p['r'], p['color'], -1)
            p['x'] += p['speed']
            if p['x'] > 450:  p['x'] = -30
            if p['x'] < -50:  p['x'] = 430
        frames.append(frame)
    return frames

frames = make_test_video(n_frames=30)
counter = PeopleCounter(count_line_x=200, min_blob_area=100)
annotated, final_stats = counter.run(frames)

print("\n── Final Stats ──────────────────")
for k, v in final_stats.items():
    print(f"  {k}: {v}")

# Show 3 key frames
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
for i, fi in enumerate([5, 15, 28]):
    axes[i].imshow(cv2.cvtColor(annotated[fi], cv2.COLOR_BGR2RGB))
    axes[i].set_title(f'Frame {fi}'); axes[i].axis('off')
plt.suptitle(f"People Counter — IN:{final_stats['entered']} OUT:{final_stats['exited']}")
plt.tight_layout()
plt.savefig('../outputs/week8_people_counter.png'); plt.show()
print("Saved → outputs/week8_people_counter.png")

# Summary stats chart
fig, ax = plt.subplots(figsize=(6, 3))
bars = ax.bar(['Entered', 'Exited', 'Total'],
              [final_stats['entered'], final_stats['exited'], final_stats['total_counted']],
              color=['#3fb950','#f0883e','#58a6ff'])
ax.set_title('People Counter — Final Summary')
ax.set_ylabel('Count')
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            str(int(bar.get_height())), ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('../outputs/week8_summary.png'); plt.show()
print("Saved → outputs/week8_summary.png")

# WHERE THIS LEADS
# You just built a complete people counter from scratch.
# The DL upgrade path:
#   MOG2 background subtraction → YOLO object detection (finds people directly)
#   Centroid + IoU matching      → DeepSORT (adds appearance embedding)
#   CountingLine                 → stays IDENTICAL, works with any detector
#   draw_dashboard               → stays IDENTICAL
#
# YOLO paper:    https://arxiv.org/abs/1506.02640
# DeepSORT:      https://arxiv.org/abs/1703.07402
