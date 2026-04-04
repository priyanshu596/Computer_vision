# 🔍 Week 7 — Image Search Engine

**Goal:** Build a reverse image search — given a query image, find the most similar ones from a collection.

**Pipeline:**
```
Image collection → Extract features → Build index → Query image → Return top-K matches
```

## Learning Path

| Day | File | What you learn |
|-----|------|----------------|
| 45 | `day45_histogram_matching.py` | Color histograms, compareHist |
| 46 | `day46_orb_features.py` | ORB keypoints + BFMatcher |
| 47 | `day47_search_index.py` | Build a searchable image database |
| 48 | `day48_hog_features.py` | HOG — shape-based features |
| 49 | `day49_cosine_similarity.py` | Feature normalization + cosine similarity |
| 50-51 | `day50_51_duplicate_detector.py` | Perceptual hashing, similarity matrix |
| Project | `project_image_search_engine.py` | ImageSearchEngine class |

## Key Functions This Week
- `cv2.calcHist` + `cv2.compareHist` — color histogram comparison
- `cv2.ORB_create` + `cv2.BFMatcher` — feature matching
- `skimage.feature.hog` — Histogram of Oriented Gradients
- `np.dot` / cosine similarity — vector comparison
- Perceptual hashing — near-duplicate detection

## Where This Leads (Deep Learning)
HOG and ORB are hand-engineered features. In DL, a pretrained CNN (ResNet, EfficientNet)
extracts a feature vector automatically — called an **embedding**. Your search index
logic stays identical; only the feature extractor changes. This is how Google Image Search,
Pinterest visual search, and face recognition all work at their core.
