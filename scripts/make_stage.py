"""
Wide atmospheric stage bands for the profile README.

GitHub cannot layer a true page background behind markdown, so these
bands frame the profile and share the same glow / grid language as the
card floors. Writes stage-top-*.svg and stage-bottom-*.svg.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from depth import card_depth_defs, depth_palette, stage_floor  # noqa: E402

ROOT = os.path.join(HERE, "..")
W = 920


def render(theme_name, kind):
    """kind: top (aurora header) or bottom (soft fade out)."""
    d = depth_palette(theme_name)
    prefix = f"stage-{kind}-{theme_name}"
    h = 160 if kind == "top" else 110
    # reuse stage_floor for the full band, then add a stronger hero orb on top
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">',
        "<defs>",
        card_depth_defs(prefix, theme_name),
        f'<linearGradient id="{prefix}-fade" x1="0" y1="0" x2="0" y2="1">',
    ]
    if kind == "top":
        parts.extend(
            [
                f'<stop offset="0" stop-color="{d["stage"]}" stop-opacity="1"/>',
                f'<stop offset="0.55" stop-color="{d["stage"]}" stop-opacity="0.85"/>',
                f'<stop offset="1" stop-color="{d["stage"]}" stop-opacity="0"/>',
                "</linearGradient>",
                "</defs>",
            ]
        )
        parts.extend(stage_floor(prefix, W, h, theme_name))
        # hero glow behind the contributions prompt
        parts.append(
            f'<ellipse cx="{W / 2}" cy="90" rx="260" ry="70" fill="{d["glow"]}" '
            f'opacity="{0.16 if theme_name == "dark" else 0.10}" '
            f'filter="url(#{prefix}-glowblur)"/>'
        )
        parts.append(f'<rect width="{W}" height="{h}" fill="url(#{prefix}-fade)"/>')
    else:
        parts.extend(
            [
                f'<stop offset="0" stop-color="{d["stage"]}" stop-opacity="0"/>',
                f'<stop offset="0.4" stop-color="{d["stage"]}" stop-opacity="0.7"/>',
                f'<stop offset="1" stop-color="{d["stage"]}" stop-opacity="1"/>',
                "</linearGradient>",
                "</defs>",
            ]
        )
        parts.extend(stage_floor(prefix, W, h, theme_name))
        parts.append(
            f'<ellipse cx="{W / 2}" cy="20" rx="300" ry="50" fill="{d["glow"]}" '
            f'opacity="{0.10 if theme_name == "dark" else 0.07}" '
            f'filter="url(#{prefix}-glowblur)"/>'
        )
        parts.append(f'<rect width="{W}" height="{h}" fill="url(#{prefix}-fade)"/>')
    parts.append("</svg>")
    return "".join(parts)


for kind in ("top", "bottom"):
    for theme_name in ("dark", "light"):
        out = os.path.join(ROOT, f"stage-{kind}-{theme_name}.svg")
        svg = render(theme_name, kind)
        with open(out, "w") as f:
            f.write(svg)
        print("wrote", out, len(svg), "bytes")
