# Day 53 | Week 8: People Counter
# Topic:  Blob Detection and Labeling
# Goal:   Find and label each separate person in the foreground mask
# Output: outputs/day53_blobs.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# WHAT YOU'LL LEARN TODAY
# A foreground mask has white blobs — each blob is one person.
# cv2.connectedComponentsWithStats labels each blob with a unique ID
# and gives you: centroid, bounding box, area.
# Filter by min_area to remove noise.

# RESOURCES
# Connected components: https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html
# Guide: https://pyimagesearch.com/2021/02/22/opencv-connected-component-labeling-and-analysis/

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

def make_test_mask():
    mask = np.zeros((300, 400), dtype=np.uint8)
    cv2.circle(mask, (80, 150), 30, 255, -1)
    cv2.circle(mask, (200, 120), 25, 255, -1)
    cv2.circle(mask, (320, 180), 28, 255, -1)
    # Add some noise blobs
    cv2.circle(mask, (150, 270), 5, 255, -1)
    cv2.circle(mask, (350, 50), 4, 255, -1)
    return mask

mask = make_test_mask()

# ─────────────────────────────────────────────
# STEP 1 — Find blobs with connected components
# ─────────────────────────────────────────────
def find_blobs(mask, min_area=200):
    """
    Find connected components in mask.
    Returns list of dicts: {'id', 'centroid', 'bbox', 'area'}
    Filters out blobs smaller than min_area.
    """
    # Use cv2.connectedComponentsWithStats(mask, connectivity=8)
    # Returns: num_labels, labels, stats, centroids
    # stats columns: CC_STAT_LEFT, CC_STAT_TOP, CC_STAT_WIDTH, CC_STAT_HEIGHT, CC_STAT_AREA
    # Label 0 = background — skip it

    # YOUR CODE HERE
    pass

blobs = find_blobs(mask, min_area=200)
if blobs:
    print(f"Found {len(blobs)} blobs:")
    for b in blobs:
        print(f"  ID={b['id']} centroid={b['centroid']} area={b['area']}")

# ─────────────────────────────────────────────
# STEP 2 — Draw blobs on image
# ─────────────────────────────────────────────
def draw_blobs(img_or_mask, blobs):
    """Draw bounding boxes and centroids for each blob."""
    if len(img_or_mask.shape) == 2:
        vis = cv2.cvtColor(img_or_mask, cv2.COLOR_GRAY2BGR)
    else:
        vis = img_or_mask.copy()
    colors = [(255,80,80),(80,255,80),(80,80,255),(255,255,80),(255,80,255)]
    for b in blobs:
        x, y, w, h = b['bbox']
        cx, cy = b['centroid']
        color = colors[b['id'] % len(colors)]
        cv2.rectangle(vis, (x,y), (x+w,y+h), color, 2)
        cv2.circle(vis, (int(cx),int(cy)), 5, color, -1)
        cv2.putText(vis, f"#{b['id']}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return vis

if blobs:
    vis = draw_blobs(mask, blobs)
    fig, axes = plt.subplots(1,2,figsize=(10,4))
    axes[0].imshow(mask, cmap='gray'); axes[0].set_title('Foreground mask'); axes[0].axis('off')
    axes[1].imshow(cv2.cvtColor(vis,cv2.COLOR_BGR2RGB)); axes[1].set_title('Detected blobs'); axes[1].axis('off')
    plt.tight_layout(); plt.savefig('../outputs/day53_blobs.png'); plt.show()
    print("Saved → outputs/day53_blobs.png")

# REFLECTION
# Q1: What is connectivity=8 vs connectivity=4?
# A1:
# Q2: Why do we skip label 0 from connectedComponentsWithStats?
# A2:
