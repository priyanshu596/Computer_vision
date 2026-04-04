# Week 7 Project | Image Search Engine
# Goal:   ImageSearchEngine class with add, search, find_duplicates methods
# Output: outputs/week7_search_results.png
# Status: [ ] Not started  [ ] In progress  [ ] Done

# YOUR TASK
# Build the ImageSearchEngine class:
#
#   engine = ImageSearchEngine()
#   engine.add_images(image_dict)         # index a collection
#   results = engine.search(query, top_k=5)  # returns [(name, score), ...]
#   dupes = engine.find_duplicates(threshold=5)
#   engine.save_index('my_index.pkl')
#   engine.load_index('my_index.pkl')

# KAGGLE PUBLISH CHECKLIST
# 1. Go to kaggle.com/code → New Notebook
# 2. Paste your working code
# 3. Add a markdown intro: "Building an Image Search Engine without Deep Learning"
# 4. Show the similarity matrix visualization (from Day 49)
# 5. Add markdown at bottom: "Where this leads → CNN embeddings + FAISS"
#    Link: https://github.com/facebookresearch/faiss
# 6. Make public, copy URL → progress/status.json → week7 → kaggle_url
# 7. git add . && git commit -m "Week 7 project done + Kaggle published" && git push

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from skimage.feature import hog as skimage_hog

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# PASTE YOUR BEST IMPLEMENTATIONS FROM DAYS 45-51
# ─────────────────────────────────────────────

def extract_combined_features(img):
    # YOUR CODE (from Day 49) — normalized histogram + HOG
    pass

def cosine_similarity(v1, v2):
    # YOUR CODE (from Day 49)
    pass

def phash(img, hash_size=8):
    # YOUR CODE (from Day 50)
    pass

def hamming_distance(h1, h2):
    # YOUR CODE (from Day 50)
    pass

# ─────────────────────────────────────────────
# THE MAIN CLASS
# ─────────────────────────────────────────────

class ImageSearchEngine:
    def __init__(self):
        self.index   = {}   # name → feature_vector
        self.hashes  = {}   # name → phash
        self.images  = {}   # name → img (optional, for display)

    def add_images(self, image_dict, store_images=True):
        """
        Index a collection of images.
        image_dict: {name: BGR_image}
        """
        for name, img in image_dict.items():
            self.index[name]  = extract_combined_features(img)
            self.hashes[name] = phash(img)
            if store_images:
                self.images[name] = img
        print(f"Indexed {len(image_dict)} images. Total: {len(self.index)}")

    def search(self, query_img, top_k=5):
        """
        Returns top_k most similar images as [(name, similarity_score), ...]
        Higher score = more similar (cosine similarity, 0-1)
        """
        query_feat = extract_combined_features(query_img)
        if query_feat is None: return []
        scores = []
        for name, feat in self.index.items():
            if feat is not None:
                sim = cosine_similarity(query_feat, feat)
                if sim is not None:
                    scores.append((name, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def find_duplicates(self, threshold=5):
        """
        Returns list of (name1, name2, hamming_dist) for near-duplicate pairs.
        """
        # YOUR CODE HERE (reuse Day 50 logic)
        pass

    def save_index(self, path):
        """Save index to disk."""
        with open(path, 'wb') as f:
            pickle.dump({'index': self.index, 'hashes': self.hashes}, f)
        print(f"Index saved to {path}")

    def load_index(self, path):
        """Load index from disk."""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.index  = data['index']
        self.hashes = data['hashes']
        print(f"Loaded {len(self.index)} images from {path}")


# ─────────────────────────────────────────────
# TEST IT
# ─────────────────────────────────────────────

def make_test_db():
    db = {}
    cats = [('red', (0,0,200)), ('blue', (200,0,0)), ('green', (0,200,0)), ('yellow', (0,200,200))]
    for name, color in cats:
        for i in range(5):
            img = np.ones((64,64,3), dtype=np.uint8) * 220
            cv2.circle(img, (32,32), 20+i, color, -1)
            noise = np.random.randint(-10,10,img.shape,dtype=np.int16)
            img = np.clip(img.astype(np.int16)+noise,0,255).astype(np.uint8)
            db[f'{name}_{i}'] = img
    return db

db = make_test_db()
engine = ImageSearchEngine()
engine.add_images(db)

# Search
query = db['red_0']
results = engine.search(query, top_k=4)
print("\nSearch results for 'red_0':")
for name, score in results:
    print(f"  {name}: {score:.4f}")

# Duplicates
dupes = engine.find_duplicates(threshold=8)
if dupes:
    print(f"\nFound {len(dupes)} duplicate pairs")

# Save and reload
engine.save_index('../outputs/week7_index.pkl')
engine2 = ImageSearchEngine()
engine2.load_index('../outputs/week7_index.pkl')
print(f"Reloaded engine has {len(engine2.index)} images")

# Visualize search results
if results and engine.images:
    imgs_show = [query] + [engine.images.get(n, np.zeros((64,64,3),dtype=np.uint8)) for n,_ in results]
    titles = ['Query'] + [f'{n}\n{s:.3f}' for n,s in results]
    fig, axes = plt.subplots(1, len(imgs_show), figsize=(3*len(imgs_show), 3))
    for ax, img, title in zip(axes, imgs_show, titles):
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); ax.set_title(title, fontsize=8); ax.axis('off')
    plt.tight_layout()
    plt.savefig('../outputs/week7_search_results.png'); plt.show()
    print("Saved → outputs/week7_search_results.png")

# WHERE THIS LEADS
# You built a complete image search engine with classical features.
# The only thing that changes in the DL version:
#   extract_combined_features() → replaced by resnet(img)[-1] (the embedding layer)
# Everything else — cosine similarity, index, search, duplicates — stays identical.
# Libraries that do this at scale: FAISS (Meta), Annoy (Spotify), ScaNN (Google)
