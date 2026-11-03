#!/usr/bin/env python3
"""Generate an animated GitHub-streak SVG (squares light up one by one).
Works standalone; designed to run in a GitHub Action daily to stay live.
Usage: python generate_streak_svg.py [username] [output-stem]
Writes <stem>-dark.svg and <stem>-light.svg (default stem: contrib-heatmap).
Also copies the dark variant to <stem>.svg for backwards compatibility.
"""
import sys
import json
import os
import datetime
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from depth import card_depth_defs  # noqa: E402
from theme import THEMES  # noqa: E402

USER = sys.argv[1] if len(sys.argv) > 1 else "Ryanditko"
STEM = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap"
if STEM.endswith(".svg"):
    STEM = STEM[:-4]

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
        here = os.path.join(HERE, "contrib.json")
        if os.path.exists(here):
            print("API failed (%s); using local contrib.json" % e)
            return json.load(open(here))
        raise


data = get_data(USER, str(YEAR_FILTER) if YEAR_FILTERED else "last")
contribs = data["contributions"]

if YEAR_FILTERED:
    by_date = {c["date"]: c for c in contribs}
    jan1 = datetime.date(YEAR_FILTER, 1, 1)
    lead_pad = (jan1.weekday() + 1) % 7
    days = []
    d = jan1
    while d <= TODAY:
        ds = d.isoformat()
        c = by_date.get(ds)
        days.append({
            "date": ds,
            "count": c["count"] if c else 0,
            "level": c["level"] if c else 0,
        })
        d += datetime.timedelta(days=1)
    contribs = [None] * lead_pad + days
    total = sum(c["count"] for c in days)
else:
    total = data["total"]["lastYear"]

CELL, GAP, RAD, LEFT, TOP = 13, 3, 2.5, 34, 24
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
total_label = (
    f"contributions in {YEAR_FILTER}"
    if YEAR_FILTERED
    else "contributions in the last year"
)
n = len(contribs)
NW = (n + 6) // 7
W = LEFT + NW * (CELL + GAP) + 6
H = TOP + 7 * (CELL + GAP) + 22
REVEAL, DUR = 3.6, 0.55
maxorder = (NW - 1) + 6 * 0.55


def build_rects(colors, pad=0):
    rects = []
    for i, c in enumerate(contribs):
        if c is None:
            continue
        wk, row, lvl = i // 7, i % 7, c["level"]
        x = LEFT + wk * (CELL + GAP) + pad
        y = TOP + row * (CELL + GAP) + pad
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RAD}" fill="{colors[lvl]}" style="animation-delay:{delay}s"/>'
        )
    return rects


def render(theme_name):
    t = THEMES[theme_name]
    colors = t["ramp"]
    gray = t["muted"]
    total_fill = t["total"]
    bg, bg2, frame = t["bg"], t["bg2"], t["frame"]
    prefix = f"heat-{theme_name}"
    pad = 12
    panel_w, panel_h = W + pad * 2, H + pad * 2
    labels = []
    last_m = None
    for wk in range(NW):
        col = contribs[wk * 7:wk * 7 + 7]
        first = next((c for c in col if c is not None), None)
        if first is None:
            continue
        d = datetime.date.fromisoformat(first["date"])
        if d.month != last_m:
            last_m = d.month
            labels.append(
                f'<text class="lbl" x="{LEFT + pad + wk * (CELL + GAP)}" y="{TOP - 8 + pad}">'
                f"{MONTHS[d.month - 1]}</text>"
            )
    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(
            f'<text class="lbl" x="{2 + pad}" y="{TOP + pad + r * (CELL + GAP) + CELL - 2}">{name}</text>'
        )
    rects = build_rects(colors, pad=pad)
    edge = "#ffffff"
    edge_op = 0.06 if theme_name == "dark" else 0.9
    glow = t["section"]
    glow_op = 0.06 if theme_name == "dark" else 0.04

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{panel_w}" height="{panel_h}" viewBox="0 0 {panel_w} {panel_h}" font-family="{eb_garamond_face.FONT_FAMILY}">
<style>
  {eb_garamond_face.font_face_css()}
  text.lbl {{ fill:{gray}; font-size:13px; font-weight:600; }}
  text.total {{ fill:{total_fill}; font-size:15px; font-weight:700; }}
  .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR + 0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(2.4)}} 45%{{filter:brightness(2.4)}} 100%{{filter:brightness(1)}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<defs>
  <linearGradient id="{prefix}-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{bg2}"/><stop offset="1" stop-color="{bg}"/>
  </linearGradient>
  <radialGradient id="{prefix}-ambience" cx="50%" cy="0%" r="80%">
    <stop offset="0" stop-color="{glow}" stop-opacity="{glow_op}"/>
    <stop offset="1" stop-color="{glow}" stop-opacity="0"/>
  </radialGradient>
  {card_depth_defs(prefix, theme_name)}
</defs>
<g filter="url(#{prefix}-shadow)">
  <rect x="0.5" y="0.5" width="{panel_w - 1}" height="{panel_h - 1}" rx="16" fill="url(#{prefix}-bg)"/>
  <rect x="0.5" y="0.5" width="{panel_w - 1}" height="{panel_h - 1}" rx="16" fill="url(#{prefix}-ambience)"/>
  <rect x="0.5" y="0.5" width="{panel_w - 1}" height="{panel_h - 1}" rx="16" fill="none" stroke="{frame}" stroke-width="1"/>
  <path d="M 16.5 1 H {panel_w - 16.5}" stroke="{edge}" stroke-opacity="{edge_op}" stroke-width="1" fill="none"/>
</g>
{''.join(labels)}
{''.join(rects)}
<text class="total" x="{LEFT + pad}" y="{H - 6 + pad}">{total:,} {total_label}</text>
</svg>'''
    return svg


n_days = sum(1 for c in contribs if c is not None)
for theme_name in ("dark", "light"):
    out = f"{STEM}-{theme_name}.svg"
    open(out, "w").write(render(theme_name))
    print(f"Wrote {out}: {n_days} days, {total:,} contributions")

# Back-compat alias used by older README links / workflow patterns.
open(f"{STEM}.svg", "w").write(render("dark"))
print(f"Wrote {STEM}.svg (dark alias)")
