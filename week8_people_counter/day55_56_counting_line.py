# Days 55-56 | Week 8: People Counter
# Topic:  Counting Line
# Goal:   Count how many tracks cross a virtual line
# Output: outputs/day55_counting.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# A vertical counting line at x=200.
# Each track has a history of centroid positions.
# When a centroid crosses x=200 from left→right: entered += 1
# When it crosses right→left: exited += 1
# Key: only count once per crossing (track a "which side was it last on")

import cv2, numpy as np, matplotlib.pyplot as plt, os
os.makedirs('../outputs', exist_ok=True)

class CountingLine:
    def __init__(self, x_position):
        self.x         = x_position
        self.entered   = 0
        self.exited    = 0
        self._track_sides = {}   # track_id → 'left' or 'right'

    def update(self, tracks):
        """
        tracks: dict of {track_id: {'centroid': (cx,cy), ...}}
        Call this every frame after tracker.update().
        """
        for tid, track in tracks.items():
            cx = track['centroid'][0]
            current_side = 'right' if cx >= self.x else 'left'

            if tid not in self._track_sides:
                self._track_sides[tid] = current_side
                continue

            prev_side = self._track_sides[tid]
            if prev_side != current_side:
                # Crossing detected
                if prev_side == 'left' and current_side == 'right':
                    self.entered += 1
                else:
                    self.exited += 1
            self._track_sides[tid] = current_side

    def draw(self, frame):
        """Draw the counting line and counts on the frame."""
        h = frame.shape[0]
        cv2.line(frame, (self.x, 0), (self.x, h), (0, 255, 255), 2)
        cv2.putText(frame, f'IN:  {self.entered}', (self.x+8, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80,255,80), 2)
        cv2.putText(frame, f'OUT: {self.exited}', (self.x+8, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80,80,255), 2)
        return frame

# Test it with simulated tracks crossing the line
from day54_object_tracker import SimpleTracker

def simulate_crossings():
    people = [
        {'x': 50,  'y': 80,  'speed': 18},   # left → right (enters)
        {'x': 350, 'y': 150, 'speed': -15},  # right → left (exits)
        {'x': 30,  'y': 220, 'speed': 20},   # left → right (enters)
    ]
    all_dets = []
    for _ in range(20):
        dets = []
        for p in people:
            x, y = int(p['x']), p['y']
            dets.append({'bbox': (x-20,y-20,40,40), 'centroid': (x,y), 'area': 400})
            p['x'] += p['speed']
        all_dets.append(dets)
    return all_dets

tracker = SimpleTracker(iou_threshold=0.2)
counter = CountingLine(x_position=200)
frames_vis = []

for dets in simulate_crossings():
    tracks = tracker.update(dets)
    counter.update(tracks)
    frame = np.ones((300,400,3),dtype=np.uint8)*190
    colors = [(255,80,80),(80,255,80),(80,80,255)]
    for tid, t in tracks.items():
        x,y,w,h = t['bbox']
        cv2.rectangle(frame,(x,y),(x+w,y+h),colors[tid%3],2)
        cv2.circle(frame,(int(t['centroid'][0]),int(t['centroid'][1])),5,colors[tid%3],-1)
    counter.draw(frame)
    frames_vis.append(frame)

print(f"Final count — Entered: {counter.entered}, Exited: {counter.exited}")

fig, axes = plt.subplots(1,3,figsize=(12,4))
for i,fi in enumerate([5,12,19]):
    axes[i].imshow(cv2.cvtColor(frames_vis[fi],cv2.COLOR_BGR2RGB))
    axes[i].set_title(f'Frame {fi}'); axes[i].axis('off')
plt.tight_layout(); plt.savefig('../outputs/day55_counting.png'); plt.show()
print("Saved → outputs/day55_counting.png")

# REFLECTION
# Q1: What happens if a person hovers on the line (oscillates back and forth)?
# A1:
# Q2: How would you extend this to a horizontal counting line?
# A2:
