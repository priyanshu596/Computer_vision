# 👥 Week 8 — People Counter

**Goal:** Build a system that counts people (or any objects) passing through a frame — like what stores use to count customers.

**Pipeline:**
```
Video frames → Background subtraction → Blob detection → Tracking + IoU → Counting line → Stats dashboard
```

## Learning Path

| Day | File | What you learn |
|-----|------|----------------|
| 52 | `day52_background_subtraction.py` | MOG2 / frame differencing |
| 53 | `day53_blob_detection.py` | Connected components, labeling |
| 54 | `day54_object_tracker.py` | SimpleTracker class + IoU |
| 55-56 | `day55_56_counting_line.py` | Virtual line crossing detection |
| 57-58 | `day57_58_speed_estimation.py` | Speed in pixels/frame |
| 59 | `day59_stats_dashboard.py` | On-frame UI overlay |
| Project | `project_people_counter.py` | PeopleCounter class, full pipeline |

## Key Concepts This Week
- Background subtraction — separating moving objects from static background
- Connected components — labeling separate blobs
- IoU (Intersection over Union) — matching detections across frames
- Object tracking — maintaining identity of objects across frames
- Centroid crossing — counting objects that cross a virtual line

## Where This Leads (Deep Learning)
This week's tracker is the classical baseline. The DL version:
- Background subtraction → **YOLO** detects people directly
- Blob matching by distance → **DeepSORT** (deep appearance features + Kalman filter)
- IoU you learn here is used **directly** in every modern tracker and detector
