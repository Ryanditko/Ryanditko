#!/usr/bin/env python3
"""Generate an animated GitHub-streak SVG (squares light up one by one).
Works standalone; designed to run in a GitHub Action daily to stay live.
Usage: python generate_streak_svg.py [username] [output.svg]
"""
import sys, json, os, datetime, urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "Ryanditko"
OUT  = sys.argv[2] if len(sys.argv) > 2 else "streak.svg"

# 2026-only: show a plain calendar-year graph (Jan 1 -> today), growing day by
# day like a normal contribution graph. From 2027 onward this block is a no-op
# and the script goes back to the regular rolling-last-365-days view.
YEAR_FILTER = 2026
TODAY = datetime.date.today()
YEAR_FILTERED = TODAY.year == YEAR_FILTER

def get_data(user, year_mode):
    url = f"https://github-contributions-api.jogruber.de/v4/{user}?y={year_mode}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        # fallback to a local snapshot if the API is unreachable
        here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contrib.json")
        if os.path.exists(here):
            print("API failed (%s); using local contrib.json" % e)
            return json.load(open(here))
        raise

data = get_data(USER, str(YEAR_FILTER) if YEAR_FILTERED else "last")
contribs = data["contributions"]

if YEAR_FILTERED:
    today_s = TODAY.isoformat()
    by_date = {c["date"]: c for c in contribs}
    jan1 = datetime.date(YEAR_FILTER, 1, 1)
    lead_pad = (jan1.weekday() + 1) % 7  # align first column to Sunday, like GitHub
    days = []
    d = jan1
    while d <= TODAY:
        ds = d.isoformat()
        c = by_date.get(ds)
        days.append({"date": ds, "count": c["count"] if c else 0, "level": c["level"] if c else 0})
        d += datetime.timedelta(days=1)
    contribs = [None] * lead_pad + days
    total = sum(c["count"] for c in days)
else:
    total = data["total"]["lastYear"]

# ---- layout ----
CELL, GAP, RAD, LEFT, TOP = 13, 3, 2.5, 34, 24
COLORS = ["#161b22", "#2a4a3a", "#3d6f52", "#5c9e78", "#a8e6c1"]
FLASH = "#c8f7d8"
GRAY = "#7d8590"
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

total_label = f"contributions in {YEAR_FILTER}" if YEAR_FILTERED else "contributions in the last year"
n = len(contribs)
NW = (n + 6) // 7
W = LEFT + NW*(CELL+GAP) + 6
H = TOP + 7*(CELL+GAP) + 22

# timing (seconds)
REVEAL, DUR = 3.6, 0.55
maxorder = (NW-1) + 6*0.55

rects, labels = [], []
last_m = None
for wk in range(NW):
    col = contribs[wk*7:wk*7+7]
    first = next((c for c in col if c is not None), None)
    if first is None:
        continue
    d = datetime.date.fromisoformat(first["date"])
    if d.month != last_m:
        last_m = d.month
        labels.append(f'<text class="lbl" x="{LEFT+wk*(CELL+GAP)}" y="{TOP-8}">{MONTHS[d.month-1]}</text>')
for name, r in [("Mon",1),("Wed",3),("Fri",5)]:
    labels.append(f'<text class="lbl" x="2" y="{TOP+r*(CELL+GAP)+CELL-2}">{name}</text>')

for i, c in enumerate(contribs):
    if c is None:
        continue
    wk, row, lvl = i//7, i%7, c["level"]
    x = LEFT + wk*(CELL+GAP); y = TOP + row*(CELL+GAP)
    delay = round((wk + row*0.55)/maxorder * REVEAL, 3)
    cls = "c g" if lvl >= 1 else "c e"
    rects.append(
        f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
        f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s"/>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">
<style>
  text.lbl {{ fill:{GRAY}; font-size:13px; font-weight:600; }}
  text.total {{ fill:#e6edf3; font-size:15px; font-weight:700; }}
  .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR+0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(2.4)}} 45%{{filter:brightness(2.4)}} 100%{{filter:brightness(1)}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<rect width="{W}" height="{H}" fill="none"/>
{''.join(labels)}
{''.join(rects)}
<text class="total" x="{LEFT}" y="{H-6}">{total:,} {total_label}</text>
</svg>'''

open(OUT, "w").write(svg)
n_days = sum(1 for c in contribs if c is not None)
print(f"Wrote {OUT}: {n_days} days, {total:,} contributions, {len(svg)//1024} KB")
