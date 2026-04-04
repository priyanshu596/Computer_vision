# 📋 Publish Checklist

Follow this after finishing each week's project file.
Takes ~20 minutes per week. Builds your public portfolio systematically.

---

## After Every Day (2 minutes)

```bash
git add .
git commit -m "Day XX done — <one line what you built>"
git push
```

Update `progress/status.json`:
```json
"31": { "done": true, "output": "day31_lines.png" }
```

---

## After Week 5 Project — Document Scanner

### 1. Kaggle Notebook
- Go to kaggle.com/code → **New Notebook**
- Title: `"Document Scanner with OpenCV — No Deep Learning"`
- Structure your notebook:
  - Markdown: What this project does + pipeline diagram (text is fine)
  - Code: paste your `project_document_scanner.py`
  - Markdown: show 3 output images
  - Markdown: `"Where this leads: CRAFT text detection"` + link to paper
- **Make it public** (Settings → Sharing → Public)
- Copy the notebook URL

### 2. Update status.json
```json
"week5": {
  "project_done": true,
  "kaggle_url": "https://www.kaggle.com/code/priyanshu596/document-scanner-opencv"
}
```

### 3. Push
```bash
git add progress/status.json outputs/
git commit -m "Week 5 done — Document Scanner published on Kaggle"
git push
```
Dashboard auto-updates with the Kaggle badge.

---

## After Week 6 Project — Background Remover

### 1. Kaggle Notebook
- Title: `"Virtual Background App — GrabCut + Alpha Blending"`
- Structure:
  - What GrabCut does (2-3 sentences)
  - Code: full pipeline
  - Side-by-side output: original / mask / composited
  - `"Where this leads: Mask R-CNN"` + arxiv link
- Make public, copy URL

### 2. Update status.json → week6 → kaggle_url
### 3. Push

---

## After Week 7 Project — Image Search Engine

### 1. Kaggle Notebook
- Title: `"Image Search Engine — Histograms, ORB, HOG + Cosine Similarity"`
- Structure:
  - Explain each feature type in one paragraph
  - Show the similarity matrix heatmap (from Day 49)
  - Show search results grid (query + top 4 matches)
  - `"Where this leads: CNN embeddings + FAISS"` + GitHub link
- Make public, copy URL

### 2. Update status.json → week7 → kaggle_url
### 3. Push

---

## After Week 8 Project — People Counter

### 1. Kaggle Notebook
- Title: `"People Counter — MOG2 + Tracking + Counting Line"`
- Structure:
  - Pipeline diagram (text)
  - Code: full PeopleCounter class
  - Show 3 annotated frames
  - Summary bar chart
  - `"Where this leads: YOLO + DeepSORT"` + links
- Make public, copy URL

### 2. OpenCV Contrib PR (optional but high credibility)
- Fork: https://github.com/opencv/opencv
- Copy `project_people_counter.py` to `samples/python/people_counter.py`
- Add docstring at the top explaining how to run it with a real video
- Open PR: title `"Add people counter sample using MOG2 + centroid tracking"`
- Copy PR URL → status.json → week8 → opencv_pr

### 3. Papers With Code
- Go to https://paperswithcode.com/method/hog
- Click "Add implementation"
- Link your Week 7 Kaggle notebook
- Repeat for ORB: https://paperswithcode.com/method/orb

### 4. Update status.json → week8 → all fields
### 5. Final push
```bash
git add .
git commit -m "Level 2 complete — all 4 projects done and published"
git push
```

---

## What Your Profile Looks Like After All 4 Weeks

**GitHub:**
- 30+ commits with meaningful messages
- Live dashboard at priyanshu596.github.io/Computer_vision
- Output images visible in the repo
- 1 merged OpenCV PR (if you do Week 8 bonus)

**Kaggle:**
- 4 public notebooks
- Each linked to the concept it implements
- Upvotes build over time as people find them

**Papers With Code:**
- Your name linked to HOG and ORB paper implementations

This combination — GitHub portfolio + Kaggle notebooks + Papers With Code — is
what sets you apart when you reach deep learning and start applying for roles.
