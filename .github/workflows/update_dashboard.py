import json, os

with open('progress/status.json') as f:
    s = json.load(f)

username = s['github_username']
repo = s['repo']

weeks = [
    ('week5', 'Week 5', 'Document Scanner', '📄', ['31','32','33','34','35','36'], '37',
     'Canny edges → contour detection → perspective warp → clean output'),
    ('week6', 'Week 6', 'Background Remover', '🎭', ['38','39','40','41','42'], '43',
     'Color masking → GrabCut → feathered edges → virtual background'),
    ('week7', 'Week 7', 'Image Search Engine', '🔍', ['45','46','47','48','49','50','51'], '52',
     'Histograms → ORB → HOG → cosine similarity → duplicate detection'),
    ('week8', 'Week 8', 'People Counter', '👥', ['52','53','54','55','56','57','58','59'], '60',
     'Background subtraction → blob detection → tracking + IoU → counting line'),
]

def day_pip(key, days, proj_day, data):
    html = '<div class="days">'
    for d in days:
        info = data[key]['days'].get(d, {})
        done = info.get('done', False)
        cls = 'day done' if done else 'day'
        out = info.get('output')
        img = f'<img src="../outputs/{out}" class="thumb"/>' if out else ''
        html += f'<div class="{cls}" title="Day {d}">{img}<span>{d}</span></div>'
    proj = data[key]['project_done']
    cls = 'day proj done' if proj else 'day proj'
    html += f'<div class="{cls}" title="Project">🏆</div>'
    html += '</div>'
    return html

def kaggle_badge(url):
    if url:
        return f'<a href="{url}" class="badge kaggle" target="_blank">📓 Live on Kaggle</a>'
    return '<span class="badge pending">Kaggle — not published yet</span>'

def pr_badge(url):
    if url:
        return f'<a href="{url}" class="badge pr" target="_blank">🔀 OpenCV PR merged</a>'
    return ''

cards = ''
for key, wlabel, title, icon, days, proj_day, pipeline in weeks:
    w = s[key]
    done_count = sum(1 for d in w['days'].values() if d['done'])
    total = len(w['days'])
    pct = int(done_count / total * 100)
    proj_done = w['project_done']
    cards += f'''
    <div class="card {'complete' if proj_done else ''}">
      <div class="card-header">
        <span class="icon">{icon}</span>
        <div>
          <div class="week-label">{wlabel}</div>
          <div class="week-title">{title}</div>
        </div>
        {kaggle_badge(w["kaggle_url"])}
        {pr_badge(w.get("opencv_pr"))}
      </div>
      <div class="pipeline">{pipeline}</div>
      {day_pip(key, days, proj_day, s)}
      <div class="progress-bar"><div class="fill" style="width:{pct}%"></div></div>
      <div class="progress-label">{done_count}/{total} days complete</div>
    </div>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CV Level 2 — priyanshu596</title>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
    --green: #3fb950; --purple: #bc8cff; --orange: #f0883e;
    --done-bg: #1a2e1a;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 2rem 1rem; }}
  .hero {{ text-align: center; margin-bottom: 2.5rem; }}
  .hero h1 {{ font-size: 1.8rem; font-weight: 600; margin-bottom: .4rem; }}
  .hero .sub {{ color: var(--muted); font-size: .95rem; }}
  .hero a {{ color: var(--accent); text-decoration: none; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.2rem; max-width: 1100px; margin: 0 auto; }}
  .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem; transition: border-color .2s; }}
  .card.complete {{ border-color: var(--green); }}
  .card-header {{ display: flex; align-items: flex-start; gap: .8rem; margin-bottom: .8rem; flex-wrap: wrap; }}
  .icon {{ font-size: 1.6rem; line-height: 1; }}
  .week-label {{ font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }}
  .week-title {{ font-size: 1rem; font-weight: 600; }}
  .pipeline {{ font-size: .78rem; color: var(--muted); margin-bottom: .9rem; font-family: monospace; }}
  .days {{ display: flex; flex-wrap: wrap; gap: .35rem; margin-bottom: .8rem; }}
  .day {{ width: 32px; height: 32px; border-radius: 6px; background: var(--border); display: flex; align-items: center; justify-content: center; font-size: .7rem; color: var(--muted); position: relative; flex-direction: column; gap: 1px; }}
  .day.done {{ background: var(--done-bg); color: var(--green); border: 1px solid var(--green); }}
  .day.proj {{ width: 36px; font-size: .85rem; }}
  .day.proj.done {{ background: #1e1a2e; border-color: var(--purple); color: var(--purple); }}
  .thumb {{ width: 28px; height: 22px; object-fit: cover; border-radius: 3px; }}
  .progress-bar {{ height: 4px; background: var(--border); border-radius: 2px; margin-bottom: .4rem; }}
  .fill {{ height: 100%; background: var(--green); border-radius: 2px; transition: width .4s; }}
  .progress-label {{ font-size: .75rem; color: var(--muted); }}
  .badge {{ display: inline-block; font-size: .72rem; padding: .2rem .55rem; border-radius: 20px; text-decoration: none; margin-left: auto; }}
  .badge.kaggle {{ background: #1fb8c3; color: #fff; }}
  .badge.pr {{ background: var(--purple); color: #fff; margin-left: .4rem; }}
  .badge.pending {{ color: var(--muted); border: 1px dashed var(--border); }}
  footer {{ text-align: center; color: var(--muted); font-size: .8rem; margin-top: 3rem; }}
  footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>
<div class="hero">
  <h1>Computer Vision — Level 2</h1>
  <div class="sub">
    <a href="https://github.com/{username}/{repo}" target="_blank">github.com/{username}/{repo}</a>
    &nbsp;·&nbsp; Building real CV projects, one day at a time
  </div>
</div>
<div class="grid">{cards}
</div>
<footer>
  Built by <a href="https://github.com/{username}" target="_blank">{username}</a> &nbsp;·&nbsp;
  Dashboard auto-updates on every push
</footer>
</body>
</html>'''

os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w') as f:
    f.write(html)

print("Dashboard updated → docs/index.html")
