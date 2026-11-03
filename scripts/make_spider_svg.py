"""
Render the black-widow ASCII spider into a terminal-style SVG.

Writes ryan-ascii-dark.svg and ryan-ascii-light.svg (plus ryan-ascii.svg as dark alias).

    python scripts/make_spider_svg.py [art.txt]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from depth import card_chrome, card_depth_defs, stage_floor  # noqa: E402
from theme import CARD_H, CARD_INNER_H, CARD_INNER_W, CARD_PAD, CARD_W, THEMES  # noqa: E402

ART = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "spider-art.txt")
ROOT = os.path.join(HERE, "..")
STATIC = bool(os.environ.get("STATIC"))
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

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

maxlen = max(len(x) for x in lines)
status_txt = f"ryan@github:~$ whoami {NAME}"
ART_W = maxlen * CELL_W
CANVAS_W, CANVAS_H = CARD_W, CARD_H
OX, OY = CARD_PAD, CARD_PAD
INNER_W, INNER_H = CARD_INNER_W, CARD_INNER_H
LEFT = (INNER_W - ART_W) / 2
ART_H = INNER_H - TITLEBAR_H - STATUS_H - PAD
ROW_DUR, STAGGER = 0.11, 0.11


def esc(s):
    return html.escape(s, quote=False)


def row_text(y, line, ri, ink, hourglass, prefix):
    if ri in RED:
        s, e = RED[ri]
        s = min(s, len(line))
        e = min(e, len(line))
        body = (
            esc(line[:s])
            + f'<tspan fill="{hourglass}">'
            + esc(line[s:e])
            + "</tspan>"
            + esc(line[e:])
        )
    else:
        body = esc(line)
    return (
        f'<text xml:space="preserve" x="{LEFT:.1f}" y="{y:.1f}" fill="{ink}" '
        f'font-family="{MONO}" font-size="{FONT:.1f}">{body}</text>'
    )


def render(theme_name):
    t = THEMES[theme_name]
    bg, bg2 = t["bg"], t["bg2"]
    frame = t["frame"]
    title_text = t["muted"]
    ink = t["ink"]
    hourglass = t["section"]
    cursor = t["ink"]
    prefix = f"port-{theme_name}"
    gid = f"{prefix}-bg"

    content_h = len(lines) * CELL_H
    art_top = TITLEBAR_H + PAD * 0.6 + max(0, (ART_H - content_h - PAD * 0.6) / 2)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'font-family="{eb_garamond_face.FONT_FAMILY}">',
        f'<style>{eb_garamond_face.font_face_css()}</style>',
        "<defs>",
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{bg2}"/><stop offset="1" stop-color="{bg}"/></linearGradient>',
        card_depth_defs(prefix, theme_name),
        "</defs>",
    ]
    parts.extend(stage_floor(prefix, CANVAS_W, CANVAS_H, theme_name))
    parts.append(f'<g transform="translate({OX},{OY})">')
    parts.extend(card_chrome(prefix, INNER_W, INNER_H, TITLEBAR_H, f"url(#{gid})", frame))

    for i, dotcol in enumerate(t["dots"]):
        parts.append(
            f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>'
        )
    parts.append(
        f'<text x="{INNER_W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{title_text}" font-size="12" '
        f'text-anchor="middle">ryan@github: ~$ ./portrait.sh</text>'
    )

    for ri, line in enumerate(lines):
        y = art_top + ri * CELL_H + CELL_H * 0.75
        row_y = art_top + ri * CELL_H
        text = row_text(y, line, ri, ink, hourglass, prefix)
        if STATIC:
            parts.append(text)
            continue
        delay = ri * STAGGER
        parts.append(
            f'<clipPath id="s{theme_name}{ri}">'
            f'<rect x="{LEFT:.1f}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{ART_W:.0f}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<g clip-path="url(#s{theme_name}{ri})">{text}</g>')
        parts.append(
            f'<rect y="{row_y + 1:.1f}" width="{CELL_W:.0f}" height="{CELL_H - 2:.0f}" '
            f'fill="{cursor}" opacity="0">'
            f'<animate attributeName="x" from="{LEFT:.1f}" to="{LEFT + ART_W:.0f}" '
            f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay + ROW_DUR:.3f}s"/></rect>'
        )

    status_line_y = TITLEBAR_H + ART_H + PAD * 0.5
    status_y = status_line_y + 19
    parts.append(
        f'<line x1="1" y1="{status_line_y:.1f}" x2="{INNER_W - 1}" y2="{status_line_y:.1f}" '
        f'stroke="{frame}"/>'
    )
    parts.append(
        f'<text x="{PAD}" y="{status_y:.1f}" fill="{title_text}" font-size="13">'
        f'ryan@github:~$ whoami <tspan fill="{ink}">{NAME}</tspan></text>'
    )
    cur_x = PAD + int(len(status_txt) * 13 * 0.48) + 6
    parts.append(
        f'<rect x="{cur_x}" y="{status_y - 12:.1f}" width="8" height="14" fill="{ink}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
        f'dur="1s" repeatCount="indefinite"/></rect>'
    )
    parts.append("</g></svg>")
    return "".join(parts)


for theme_name in ("dark", "light"):
    out = os.path.join(ROOT, f"ryan-ascii-{theme_name}.svg")
    svg = render(theme_name)
    with open(out, "w") as f:
        f.write(svg)
    print("wrote", out, len(svg), "bytes;", CANVAS_W, "x", CANVAS_H)

alias = os.path.join(ROOT, "ryan-ascii.svg")
with open(alias, "w") as f:
    f.write(render("dark"))
print("wrote", alias, "(dark alias)")
