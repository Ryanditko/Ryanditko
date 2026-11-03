"""
Render README shell prompts as SVGs with embedded EB Garamond.

GitHub README markdown cannot load custom fonts for <h3>/<code>, so these
prompts must be images to match the rest of the profile.

Writes prompt-<slug>-{dark,light}.svg for each entry below.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from theme import THEMES  # noqa: E402

ROOT = os.path.join(HERE, "..")

PROMPTS = [
    ("contributions", "ryan@github ~ $ ./contributions.sh"),
    ("whoami", "ryan@github ~ $ whoami"),
]

# Capsule sizing (approx; EB Garamond is proportional so keep generous width).
H = 44
PAD_X = 28
FONT_SIZE = 22


def render(theme_name, text):
    t = THEMES[theme_name]
    # On dark GitHub: light text in a soft dark pill.
    # On light GitHub: dark text in a soft light pill.
    fill = t["ink"]
    bg = t["bg2"]
    frame = t["frame"]
    # Rough width estimate for serif at 22px.
    w = int(PAD_X * 2 + len(text) * FONT_SIZE * 0.52)
    safe = html.escape(text)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" font-family="{eb_garamond_face.FONT_FAMILY}">
<style>{eb_garamond_face.font_face_css()}</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{H - 1}" rx="{H / 2}" fill="{bg}" stroke="{frame}"/>
<text x="{w / 2}" y="{H / 2 + 7}" fill="{fill}" font-size="{FONT_SIZE}" text-anchor="middle">{safe}</text>
</svg>'''


for slug, text in PROMPTS:
    for theme_name in ("dark", "light"):
        out = os.path.join(ROOT, f"prompt-{slug}-{theme_name}.svg")
        svg = render(theme_name, text)
        with open(out, "w") as f:
            f.write(svg)
        print("wrote", out, len(svg), "bytes")
