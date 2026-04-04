# Day 47 | Week 7: Image Search Engine
# Topic:  Build a Searchable Image Index
# Goal:   Create a database of images with features, then query it
# Output: outputs/day47_search_results.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

import cv2, numpy as np, matplotlib.pyplot as plt, os
os.makedirs('../outputs', exist_ok=True)

# WHAT YOU'LL LEARN TODAY
# Combine histogram + ORB into a real searchable database.
# Database: dict of {name: feature_vector}
# Query: compute feature for query image, find closest in database.

# RESOURCES
# Image retrieval overview: https://pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/

def make_database():
    """20 images in 4 categories, 5 each."""
    db = {}
    cats = {
        'red_circle':   lambda i: _draw(circle=True,  color=(0,0,200),   noise=i*7),
        'blue_rect':    lambda i: _draw(rect=True,    color=(200,0,0),   noise=i*5),
        'green_tri':    lambda i: _draw(tri=True,     color=(0,200,0),   noise=i*9),
        'mixed':        lambda i: _draw(mixed=True,   color=(150,80,60), noise=i*3),
    }
    for cat, fn in cats.items():
        for i in range(5):
            db[f'{cat}_{i}'] = fn(i)
    return db

def _draw(circle=False, rect=False, tri=False, mixed=False, color=(128,128,128), noise=0):
    img = np.ones((100,100,3), dtype=np.uint8) * 220
    np.random.seed(noise)
    img += np.random.randint(-15, 15, img.shape, dtype=np.int16).clip(0,255).astype(np.uint8)
    if circle: cv2.circle(img, (50,50), 35, color, -1)
    if rect:   cv2.rectangle(img, (20,20), (80,80), color, -1)
    if tri:    cv2.fillPoly(img, [np.array([[50,15],[85,85],[15,85]])], color)
    if mixed:
        cv2.circle(img, (30,30), 20, color, -1)
        cv2.rectangle(img, (55,55), (85,85), (color[2],color[1],color[0]), -1)
    return img

db_images = make_database()

# ─────────────────────────────────────────────
# STEP 1 — Feature extraction (combine histogram + HOG-lite)
# ─────────────────────────────────────────────
def extract_features(img):
    """
    Returns a 1D feature vector combining color histogram and basic texture.
    This is your image 'fingerprint'.
    """
    # Step 1: Compute a normalized color histogram (reuse Day 45 approach)
    # Step 2: Resize image to 32x32 and flatten as a texture feature
    # Step 3: Concatenate and return as a single float32 vector
    # YOUR CODE HERE
    pass

# ─────────────────────────────────────────────
# STEP 2 — Build the index
# ─────────────────────────────────────────────
# YOUR TASK: Compute features for all images in db_images
# Store as: index = {name: feature_vector}

index = {}  # YOUR CODE HERE

# ─────────────────────────────────────────────
# STEP 3 — Search function
# ─────────────────────────────────────────────
def search(query_img, index, top_k=3):
    """Find top_k most similar images using L2 distance on feature vectors."""
    query_feat = extract_features(query_img)
    scores = []
    for name, feat in index.items():
        if query_feat is not None and feat is not None:
            dist = np.linalg.norm(query_feat - feat)
            scores.append((name, dist))
    scores.sort(key=lambda x: x[1])
    return scores[:top_k]

# Test: query with a red circle — should return other red circles
query = db_images['red_circle_0']
results = search(query, index, top_k=4)
print("Top matches:", [(n, f'{d:.3f}') for n,d in results])

if results:
    imgs_to_show = [query] + [db_images[n] for n,_ in results]
    titles = ['Query'] + [f'{n}\n{d:.2f}' for n,d in results]
    fig, axes = plt.subplots(1, len(imgs_to_show), figsize=(3*len(imgs_to_show), 3))
    for ax, img, title in zip(axes, imgs_to_show, titles):
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); ax.set_title(title, fontsize=8); ax.axis('off')
    plt.tight_layout(); plt.savefig('../outputs/day47_search_results.png'); plt.show()
    print("Saved → outputs/day47_search_results.png")

# REFLECTION
# Q1: Why is L2 distance a valid similarity measure for feature vectors?
# A1:
# Q2: What would happen if one feature (e.g. color) has much larger values than another?
# A2: (This is exactly what Day 49 fixes — feature normalization)
