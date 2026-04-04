# 🎭 Week 6 — Background Remover & Virtual Background

**Goal:** Remove the background from a photo and replace it with a new one — like Zoom's virtual background, but for still images.

**Pipeline you'll build piece by piece:**
```
Photo → Detect subject → Create mask → Feather edges → Paste new background
```

## Learning Path

| Day | File | What you learn |
|-----|------|----------------|
| 38 | `day38_green_screen.py` | HSV masking, color-based removal |
| 39 | `day39_grabcut.py` | cv2.grabCut, morphological cleanup |
| 40 | `day40_mask_feathering.py` | Gaussian blur on mask, soft compositing |
| 41 | `day41_virtual_background.py` | Alpha blending, background replacement |
| 42 | `day42_motion_detection.py` | Frame differencing, moving object detection |
| Project | `project_virtual_bg_app.py` | Full pipeline + drop shadow |

## Key Functions This Week
- `cv2.inRange` — color range masking
- `cv2.grabCut` — smart foreground/background segmentation
- `cv2.GaussianBlur` on a mask — feathered (soft) edges
- `cv2.addWeighted` — alpha blending for compositing
- Background subtraction — separating moving objects from static background

## Where This Leads (Deep Learning)
GrabCut is a graphical model algorithm. The DL equivalent is **Mask R-CNN** — instead of you providing a bounding box, the network finds subjects and generates masks automatically. The compositing step (blending fg + new bg) stays identical.
