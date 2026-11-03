"""
Build a neofetch-style info card SVG to sit to the RIGHT of the ASCII portrait.

Writes info-card-dark.svg and info-card-light.svg (plus info-card.svg as dark alias).
STATIC=1 emits the frozen state for Quick Look previews.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from theme import CARD_H, CARD_W, THEMES  # noqa: E402

ROOT = os.path.join(HERE, "..")
STATIC = bool(os.environ.get("STATIC"))

W = CARD_W
H = CARD_H
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
TOP_PAD = 30
BOTTOM_PAD = 28

ROWS = [
    ("host",),
    ("kv", "Now", "Software Engineer @ Nubank"),
    ("kv", "Also", "Scientific Researcher"),
    ("kv", "Edu", "ADS @ Impacta University ('24 – '26)"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Backend", "Clojure, Datomic, DynamoDB, SQL, EDN"),
    ("kv", "Languages", "TypeScript, Python, Go, Dart"),
    ("kv", "AI / ML", "Machine Learning"),
    ("kv", "DevOps", "AWS, Docker"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "3rd place — Scientific Research @ Impacta"),
    ("bul", "NASA Space Apps Challenge participant"),
    ("bul", "Creator of E.V."),
    ("gap",),
    ("sec", "Links"),
    ("kv", "Portfolio", "ryanditko.com"),
    ("kv", "LinkedIn", "in/ryanditko"),
    ("kv", "Instagram", "ryan.ditko"),
    ("kv", "YouTube", "@ryanditko"),
    ("kv", "Email", "yryurodriguess@gmail.com"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (
        f'<g opacity="0" transform="translate(0,5)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


def line_height_for_card():
    """Stretch row spacing so the written card fills the same canvas as the portrait."""
    units = 0.0
    for row in ROWS:
        kind = row[0]
        if kind == "gap":
            units += 0.5
        elif kind in ("host", "sec", "kv", "bul"):
            units += 1.0
    available = H - TITLEBAR_H - TOP_PAD - BOTTOM_PAD
    return available / units


def render(theme_name):
    t = THEMES[theme_name]
    bg, bg2 = t["bg"], t["bg2"]
    frame, muted, ink = t["frame"], t["muted"], t["ink"]
    key, section, accent = t["key"], t["section"], t["accent"]
    highlight = t["section"]
    gid = f"ibg-{theme_name}"
    line_h = line_height_for_card()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{eb_garamond_face.FONT_FAMILY}">',
        f'<style>{eb_garamond_face.font_face_css()}</style>',
        '<defs>'
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{bg2}"/><stop offset="1" stop-color="{bg}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#{gid})"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{frame}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{frame}"/>',
    ]
    for i, dotcol in enumerate(t["dots"]):
        parts.append(
            f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>'
        )
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{muted}" font-size="12" '
        f'text-anchor="middle">ryan@github: ~$ neofetch</text>'
    )

    y = TITLEBAR_H + TOP_PAD
    for i, row in enumerate(ROWS):
        kind = row[0]
        if kind == "gap":
            y += line_h * 0.5
            continue
        if kind == "host":
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                f'<tspan fill="{highlight}">ryan</tspan><tspan fill="{muted}">@</tspan>'
                f'<tspan fill="{accent}">github</tspan></text>'
                f'<line x1="{KEY_X + 96}" y1="{y - 4:.1f}" x2="{W - PAD}" y2="{y - 4:.1f}" '
                f'stroke="{frame}" stroke-opacity="0.8"/>'
            )
        elif kind == "sec":
            title = esc(row[1])
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" fill="{section}" font-size="12.5" font-weight="700">'
                f'&#8212; {title}</text>'
                f'<line x1="{KEY_X + 12 + len(row[1]) * 8}" y1="{y - 4:.1f}" x2="{W - PAD}" y2="{y - 4:.1f}" '
                f'stroke="{frame}" stroke-opacity="0.8"/>'
            )
        elif kind == "kv":
            k, val = esc(row[1]), esc(row[2])
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" fill="{key}" font-size="12.5" font-weight="700">{k}</text>'
                f'<text x="{VAL_X}" y="{y:.1f}" fill="{ink}" font-size="12.5">{val}</text>'
            )
        elif kind == "bul":
            txt = esc(row[1])
            inner = (
                f'<circle cx="{KEY_X + 3}" cy="{y - 4:.1f}" r="2.5" fill="{highlight}"/>'
                f'<text x="{KEY_X + 14}" y="{y:.1f}" fill="{ink}" font-size="12.5">{txt}</text>'
            )
        else:
            continue
        parts.append(rise(inner, i))
        y += line_h

    parts.append("</svg>")
    return "".join(parts)


for theme_name in ("dark", "light"):
    out = os.path.join(ROOT, f"info-card-{theme_name}.svg")
    svg = render(theme_name)
    with open(out, "w") as f:
        f.write(svg)
    print("wrote", out, len(svg), "bytes;", W, "x", H)

alias = os.path.join(ROOT, "info-card.svg")
with open(alias, "w") as f:
    f.write(render("dark"))
print("wrote", alias, "(dark alias)")
