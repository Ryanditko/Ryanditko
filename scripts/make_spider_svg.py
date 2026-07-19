"""
Render the black-widow ASCII spider (with its red hourglass) into a terminal-
style SVG that matches the portrait frame: title bar, dark background, a row-by-
row "typing" reveal, and a status line. Pure text -> no image deps.

    python scripts/make_spider_svg.py [art.txt] [out.svg]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "spider-art.txt")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "ryan-ascii.svg")
STATIC = bool(os.environ.get("STATIC"))

# red hourglass columns per 0-indexed art row (start, end) — the black-widow mark
RED = {20: (17, 22), 21: (18, 21), 22: (19, 21), 23: (18, 21), 24: (17, 22)}

lines = open(ART, encoding="utf-8").read().split("\n")
while lines and lines[-1] == "":
    lines.pop()

CELL_W, CELL_H = 8.0, 15.0
FONT = 13.0
PAD = 24
TITLEBAR_H = 30
STATUS_H = 34
NAME = "Ryan Rodrigues"

BG, BG2 = "#0d1117", "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
RED_FILL = "#e23636"
CURSOR = "#c9d1d9"

maxlen = max(len(x) for x in lines)
status_txt = f"ryan@github:~$ whoami {NAME}"
ART_W = maxlen * CELL_W
# match the info-card width so both boxes render at the same size
CANVAS_W = 520
LEFT = (CANVAS_W - ART_W) / 2   # center the spider horizontally
ART_H = len(lines) * CELL_H
CANVAS_H = int(TITLEBAR_H + ART_H + STATUS_H + PAD)

ROW_DUR, STAGGER = 0.11, 0.11


def esc(s):
    return html.escape(s, quote=False)


def row_text(y, line, ri):
    """the line's <text>, splitting the red hourglass segment out."""
    if ri in RED:
        s, e = RED[ri]
        s = min(s, len(line)); e = min(e, len(line))
        body = (esc(line[:s]) + f'<tspan fill="{RED_FILL}">' + esc(line[s:e])
                + "</tspan>" + esc(line[e:]))
    else:
        body = esc(line)
    return (f'<text xml:space="preserve" x="{LEFT:.1f}" y="{y:.1f}" fill="{INK}" '
            f'font-size="{FONT:.1f}">{body}</text>')


art_top = TITLEBAR_H + PAD * 0.6
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#pbg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">ryan@github: ~$ ./portrait.sh</text>')

for ri, line in enumerate(lines):
    y = art_top + ri * CELL_H + CELL_H * 0.75
    row_y = art_top + ri * CELL_H
    text = row_text(y, line, ri)
    if STATIC:
        parts.append(text)
        continue
    delay = ri * STAGGER
    parts.append(
        f'<clipPath id="s{ri}"><rect x="{LEFT:.1f}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W:.0f}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>')
    parts.append(f'<g clip-path="url(#s{ri})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W:.0f}" height="{CELL_H-2:.0f}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{LEFT:.1f}" to="{LEFT+ART_W:.0f}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>')

status_line_y = TITLEBAR_H + ART_H + PAD * 0.5
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'ryan@github:~$ whoami <tspan fill="{INK}">{NAME}</tspan></text>')
cur_x = PAD + int(len(status_txt) * CELL_W) + 4
parts.append(f'<rect x="{cur_x}" y="{status_y-12:.1f}" width="8" height="14" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", CANVAS_W, "x", CANVAS_H)
