"""
Render README shell prompts as soft floating pills on a stage floor.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eb_garamond_face  # noqa: E402
from depth import card_depth_defs, depth_palette, stage_floor  # noqa: E402
from theme import THEMES  # noqa: E402

ROOT = os.path.join(HERE, "..")

PROMPTS = [
    ("contributions", "ryan@github ~ $ ./contributions.sh"),
    ("whoami", "ryan@github ~ $ whoami"),
]

H = 44
PAD_X = 26
FONT_SIZE = 20
SHADOW = 18


def render(theme_name, text, slug):
    t = THEMES[theme_name]
    d = depth_palette(theme_name)
    fill = t["ink"]
    bg = t["bg2"]
    prefix = f"prompt-{slug}-{theme_name}"
    inner_w = int(PAD_X * 2 + len(text) * FONT_SIZE * 0.52)
    w = inner_w + SHADOW * 2
    h = H + SHADOW + 8
    safe = html.escape(text)
    rx = H / 2
    floor = "".join(stage_floor(prefix, w, h, theme_name))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{eb_garamond_face.FONT_FAMILY}">
<style>{eb_garamond_face.font_face_css()}</style>
<defs>
{card_depth_defs(prefix, theme_name)}
</defs>
{floor}
<g transform="translate({SHADOW},{SHADOW // 2})" filter="url(#{prefix}-shadow)">
  <rect width="{inner_w}" height="{H}" rx="{rx}" fill="{bg}"/>
  <rect width="{inner_w}" height="{H}" rx="{rx}" fill="none" stroke="{d["rim"]}" stroke-opacity="{d["rim_opacity"]}" stroke-width="1"/>
  <path d="M {rx} 1 H {inner_w - rx}" stroke="{d["edge"]}" stroke-opacity="{d["edge_opacity"]}" stroke-width="1" fill="none"/>
  <text x="{inner_w / 2}" y="{H / 2 + 6}" fill="{fill}" font-size="{FONT_SIZE}" text-anchor="middle">{safe}</text>
</g>
</svg>'''


for slug, text in PROMPTS:
    for theme_name in ("dark", "light"):
        out = os.path.join(ROOT, f"prompt-{slug}-{theme_name}.svg")
        svg = render(theme_name, text, slug)
        with open(out, "w") as f:
            f.write(svg)
        print("wrote", out, len(svg), "bytes")
