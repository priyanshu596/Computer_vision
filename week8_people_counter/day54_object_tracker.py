# Day 54 | Week 8: People Counter
# Topic:  Object Tracker + IoU (Intersection over Union)
# Goal:   Maintain consistent IDs for objects across video frames
# Output: outputs/day54_tracking.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY — TWO CONCEPTS IN ONE DAY
#
# 1. IoU (Intersection over Union)
#    Used in EVERY modern object detector (YOLO, Faster R-CNN, etc.)
#    IoU = area of overlap / area of union between two bounding boxes
#    If IoU > 0.3, two boxes probably contain the same object.
#    You WILL see this again when you reach deep learning.
#
# 2. SimpleTracker
#    Frame N: detect blobs → get bounding boxes
#    Frame N+1: detect new blobs → match to existing tracks using IoU
#    High IoU match → same object → keep ID
#    No match → new object → assign new ID
#    Not seen for N frames → remove track

# RESOURCES
# IoU explained:   https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
# Object tracking: https://learnopencv.com/object-tracking-using-opencv-cpp-python/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# IoU — LEARN THIS, YOU'LL USE IT AGAIN IN DL
# ─────────────────────────────────────────────
def compute_iou(box1, box2):
    """
    box format: (x, y, w, h)
    Returns IoU score between 0.0 and 1.0.

    Steps:
      1. Convert both boxes to (x1,y1,x2,y2) format
      2. Find intersection: max(x1s), max(y1s), min(x2s), min(y2s)
      3. If intersection has negative width or height → IoU = 0
      4. intersection_area = inter_w * inter_h
      5. union_area = area1 + area2 - intersection_area
      6. IoU = intersection_area / union_area
    """
    # YOUR CODE HERE
    pass

# Quick test — these should print roughly 0.14 and 0.0
box_a = (10, 10, 50, 50)
box_b = (40, 40, 50, 50)
box_c = (200, 200, 50, 50)
print(f"IoU overlapping boxes: {compute_iou(box_a, box_b):.3f}")  # expect ~0.14
print(f"IoU non-overlapping:   {compute_iou(box_a, box_c):.3f}")  # expect 0.0

# ─────────────────────────────────────────────
# SimpleTracker
# ─────────────────────────────────────────────
class SimpleTracker:
    def __init__(self, max_distance=50, max_missing=5, iou_threshold=0.3):
        self.tracks       = {}    # track_id → {'bbox', 'centroid', 'positions', 'missing'}
        self.next_id      = 0
        self.max_missing  = max_missing
        self.iou_threshold = iou_threshold

    def update(self, detections):
        """
        detections: list of {'bbox': (x,y,w,h), 'centroid': (cx,cy), 'area': int}
        Returns: updated tracks dict
        """
        if not self.tracks:
            # No existing tracks — create one for each detection
            for det in detections:
                self._add_track(det)
            return self.tracks

        # Match detections to existing tracks using IoU
        matched_track_ids = set()
        matched_det_ids   = set()

        for det_i, det in enumerate(detections):
            best_iou   = self.iou_threshold
            best_track = None
            for tid, track in self.tracks.items():
                # YOUR CODE — compute IoU between det['bbox'] and track['bbox']
                # If iou > best_iou, update best_iou and best_track
                pass
            if best_track is not None:
                # YOUR CODE — update the matched track with new detection
                matched_track_ids.add(best_track)
                matched_det_ids.add(det_i)

        # Unmatched detections → new tracks
        for det_i, det in enumerate(detections):
            if det_i not in matched_det_ids:
                self._add_track(det)

        # Unmatched tracks → increment missing counter, remove if too old
        for tid in list(self.tracks.keys()):
            if tid not in matched_track_ids:
                self.tracks[tid]['missing'] += 1
                if self.tracks[tid]['missing'] > self.max_missing:
                    del self.tracks[tid]

        return self.tracks

    def _add_track(self, det):
        self.tracks[self.next_id] = {
            'bbox':      det['bbox'],
            'centroid':  det['centroid'],
            'positions': [det['centroid']],
            'missing':   0,
        }
        self.next_id += 1

# ─────────────────────────────────────────────
# TEST — synthetic moving blobs
# ─────────────────────────────────────────────
def make_video_detections(n_frames=15):
    np.random.seed(0)
    people = [{'x': i*100+50, 'y': 80+i*50, 'speed': 15+i*3} for i in range(3)]
    all_dets = []
    for _ in range(n_frames):
        dets = []
        for p in people:
            x, y, r = int(p['x']), p['y'], 25
            bbox = (x-r, y-r, r*2, r*2)
            dets.append({'bbox': bbox, 'centroid': (x,y), 'area': r*r*3})
            p['x'] += p['speed']
        all_dets.append(dets)
    return all_dets

all_detections = make_video_detections()
tracker = SimpleTracker(iou_threshold=0.2)

frames_vis = []
for frame_i, dets in enumerate(all_detections):
    tracks = tracker.update(dets)
    frame = np.ones((300,500,3),dtype=np.uint8)*190
    colors = [(255,80,80),(80,255,80),(80,80,255),(255,255,80),(255,80,255)]
    for tid, t in tracks.items():
        x,y,w,h = t['bbox']; cx,cy = t['centroid']
        color = colors[tid % len(colors)]
        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
        cv2.circle(frame,(int(cx),int(cy)),5,color,-1)
        cv2.putText(frame,f'ID:{tid}',(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1)
    frames_vis.append(frame)

if frames_vis:
    fig, axes = plt.subplots(1,3,figsize=(12,4))
    for i, fi in enumerate([3,7,12]):
        axes[i].imshow(cv2.cvtColor(frames_vis[fi],cv2.COLOR_BGR2RGB))
        axes[i].set_title(f'Frame {fi}'); axes[i].axis('off')
    plt.tight_layout(); plt.savefig('../outputs/day54_tracking.png'); plt.show()
    print("Saved → outputs/day54_tracking.png")

# REFLECTION
# Q1: What happens if two people walk very close together (IoU > threshold between them)?
# A1:
# Q2: Why is IoU better than Euclidean centroid distance for matching?
# A2:

# WHERE THIS LEADS:
# IoU is used directly in:
#   - NMS (Non-Maximum Suppression) in YOLO — removes duplicate detections
#   - DeepSORT tracker — combines IoU + deep appearance features
#   - mAP metric — evaluates how accurate a detector is
