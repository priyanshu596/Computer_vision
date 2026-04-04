# 🚀 First-Time Setup Guide

Run these commands **once** to connect this folder to your GitHub repo
and get the dashboard live.

---

## Step 1 — Enable GitHub Pages

1. Go to: https://github.com/priyanshu596/Computer_vision/settings/pages
2. Under **Source** → select **Deploy from a branch**
3. Branch: `main` | Folder: `/docs`
4. Click **Save**

Your live URL will be:
**https://priyanshu596.github.io/Computer_vision**

(Takes ~2 minutes to go live after first push)

---

## Step 2 — Connect this folder to GitHub

Open a terminal inside this `Computer_vision` folder and run:

```bash
git init
git remote add origin https://github.com/priyanshu596/Computer_vision.git
git branch -M main
```

---

## Step 3 — Python environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

---

## Step 4 — First push

```bash
git add .
git commit -m "initial setup — CV Level 2 folder"
git push -u origin main
```

After this push:
- GitHub Actions runs automatically
- Dashboard goes live at your Pages URL
- README progress table is ready

---

## Step 5 — Verify

- Visit https://github.com/priyanshu596/Computer_vision
  → You should see the README with the progress table
- Visit https://priyanshu596.github.io/Computer_vision
  → You should see the dark dashboard with 4 week cards

---

## Daily Workflow (after setup)

```bash
# 1. Activate environment
venv\Scripts\activate          # Windows

# 2. Work on today's script
cd week5_document_scanner
python day31_line_detector.py

# 3. Update progress (30 seconds)
# Open progress/status.json, set "31": { "done": true, "output": "day31_lines.png" }

# 4. Commit and push
cd ..
git add .
git commit -m "Day 31 done — line detector"
git push
```

GitHub Actions runs, dashboard updates automatically. Done.

---

## Troubleshooting

**GitHub Actions fails:**
Go to your repo → Actions tab → click the failed run → read the error log.
Most common issue: `pip install` fails → check requirements.txt

**Dashboard doesn't update:**
Actions may need write permissions.
Go to: Settings → Actions → General → Workflow permissions → Read and write

**Pages not showing:**
Wait 5 minutes after first push. If still not working, check Settings → Pages
to confirm source is set to `/docs` folder on `main` branch.
