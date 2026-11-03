"""
Render README shell prompts as SVGs with embedded EB Garamond + soft 3D chrome.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from depth import card_depth_defs  # noqa: E402
from theme import THEMES  # noqa: E402

ROOT = os.path.join(HERE, "..")

PROMPTS = [
    ("contributions", "ryan@github ~ $ ./contributions.sh"),
    ("whoami", "ryan@github ~ $ whoami"),
]

H = 52
PAD_X = 28
FONT_SIZE = 22
SHADOW = 8


def render(theme_name, text, slug):
    t = THEMES[theme_name]
    fill = t["ink"]
    bg = t["bg2"]
    prefix = f"prompt-{slug}-{theme_name}"
    inner_w = int(PAD_X * 2 + len(text) * FONT_SIZE * 0.52)
    w = inner_w + SHADOW * 2
    h = H + SHADOW
    safe = html.escape(text)
    rx = H / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{eb_garamond_face.FONT_FAMILY}">
<style>{eb_garamond_face.font_face_css()}</style>
<defs>
{card_depth_defs(prefix, theme_name)}
</defs>
<g transform="translate({SHADOW},{SHADOW // 2})" filter="url(#{prefix}-shadow)">
  <rect width="{inner_w}" height="{H}" rx="{rx}" fill="{bg}"/>
  <rect width="{inner_w}" height="{H}" rx="{rx}" fill="none" stroke="url(#{prefix}-bevel)" stroke-width="1.3"/>
  <rect width="{inner_w}" height="{H / 2}" rx="{rx}" fill="url(#{prefix}-gloss)"/>
  <rect y="{H / 2 - 4}" width="{inner_w}" height="8" fill="{bg}"/>
  <text x="{inner_w / 2}" y="{H / 2 + 7}" fill="{fill}" font-size="{FONT_SIZE}" text-anchor="middle">{safe}</text>
</g>
</svg>'''


for slug, text in PROMPTS:
    for theme_name in ("dark", "light"):
        out = os.path.join(ROOT, f"prompt-{slug}-{theme_name}.svg")
        svg = render(theme_name, text, slug)
        with open(out, "w") as f:
            f.write(svg)
        print("wrote", out, len(svg), "bytes")
