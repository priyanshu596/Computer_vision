import json, re

with open('progress/status.json') as f:
    s = json.load(f)

week_labels = {
    'week5': ('Week 5', 'Document Scanner', '37'),
    'week6': ('Week 6', 'Background Remover & Virtual BG', '43-44'),
    'week7': ('Week 7', 'Image Search Engine', '52'),
    'week8': ('Week 8', 'People Counter', '60'),
}

def status_icon(done): return '✅' if done else '⬜'

def kaggle_cell(url):
    if url: return f'[📓 Notebook]({url})'
    return '—'

# Build week summary table
rows = []
for key, (wlabel, title, _) in week_labels.items():
    w = s[key]
    done_days = sum(1 for d in w['days'].values() if d['done'])
    total_days = len(w['days'])
    proj = status_icon(w['project_done'])
    kaggle = kaggle_cell(w['kaggle_url'])
    bar = '█' * done_days + '░' * (total_days - done_days)
    rows.append(f'| {wlabel} | {title} | {bar} {done_days}/{total_days} days · project {proj} | {kaggle} |')

table = '\n'.join(rows)
new_block = f"""| Week | Project | Status | Kaggle |
|------|---------|--------|--------|
{table}"""

# Day tables per week
day_sections = []
for key, (wlabel, title, proj_day) in week_labels.items():
    w = s[key]
    rows = []
    for day, info in w['days'].items():
        rows.append(f'| {day} | — | {status_icon(info["done"])} |')
    rows.append(f'| {proj_day} | **Project** | {status_icon(w["project_done"])} |')
    day_sections.append(f'### {wlabel} — {title}\n| Day | Topic | Done |\n|-----|-------|------|\n' + '\n'.join(rows))

day_block = '\n\n'.join(day_sections)

with open('README.md', 'r') as f:
    content = f.read()

content = re.sub(
    r'\| Week \| Project \| Status \| Kaggle \|.*?(?=\n---|\Z)',
    new_block + '\n',
    content, flags=re.DOTALL
)

content = re.sub(
    r'## 📅 Daily Progress\n.*',
    '## 📅 Daily Progress\n\n' + day_block,
    content, flags=re.DOTALL
)

with open('README.md', 'w') as f:
    f.write(content)

print("README updated.")
