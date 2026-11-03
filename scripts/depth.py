"""Shared soft elevation for profile SVGs.

Keeps the look minimal: ambient + contact shadow, hairline rim,
and a faint top edge highlight. No bevel gradients or neon glow.
"""

from theme import THEMES


def depth_palette(theme_name):
    t = THEMES[theme_name]
    if theme_name == "dark":
        return {
            "ambient_opacity": 0.38,
            "ambient_dy": 10,
            "ambient_blur": 18,
            "contact_opacity": 0.45,
            "contact_dy": 2,
            "contact_blur": 3,
            "rim": t["frame"],
            "rim_opacity": 0.95,
            "edge": "#ffffff",
            "edge_opacity": 0.06,
            "title_fill": "#ffffff",
            "title_opacity": 0.03,
        }
    return {
        "ambient_opacity": 0.10,
        "ambient_dy": 8,
        "ambient_blur": 16,
        "contact_opacity": 0.08,
        "contact_dy": 1.5,
        "contact_blur": 2.5,
        "rim": t["frame"],
        "rim_opacity": 1.0,
        "edge": "#ffffff",
        "edge_opacity": 0.85,
        "title_fill": "#ffffff",
        "title_opacity": 0.45,
    }


def card_depth_defs(prefix, theme_name):
    """Filters/gradients for softly elevated cards."""
    d = depth_palette(theme_name)
    return f'''
<filter id="{prefix}-shadow" x="-20%" y="-15%" width="140%" height="150%" color-interpolation-filters="sRGB">
  <feDropShadow dx="0" dy="{d["ambient_dy"]}" stdDeviation="{d["ambient_blur"]}"
    flood-color="#000000" flood-opacity="{d["ambient_opacity"]}"/>
  <feDropShadow dx="0" dy="{d["contact_dy"]}" stdDeviation="{d["contact_blur"]}"
    flood-color="#000000" flood-opacity="{d["contact_opacity"]}"/>
</filter>
<linearGradient id="{prefix}-title" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{d["title_fill"]}" stop-opacity="{d["title_opacity"]}"/>
  <stop offset="1" stop-color="{d["title_fill"]}" stop-opacity="0"/>
</linearGradient>
'''.strip()


def card_chrome(prefix, w, h, titlebar_h, bg_fill, frame, rx=16):
    """Soft floating card: dual shadow, fill, hairline rim, faint title wash."""
    theme = "light" if prefix.endswith("light") else "dark"
    d = depth_palette(theme)
    return [
        f'<g filter="url(#{prefix}-shadow)">',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{bg_fill}"/>',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="{d["rim"]}" stroke-opacity="{d["rim_opacity"]}" stroke-width="1"/>',
        # faint top highlight along the rim
        f'<path d="M {rx + 0.5} 1 H {w - rx - 0.5}" stroke="{d["edge"]}" '
        f'stroke-opacity="{d["edge_opacity"]}" stroke-width="1" fill="none"/>',
        f'<rect x="1" y="1" width="{w - 2}" height="{titlebar_h - 1}" rx="{rx}" '
        f'fill="url(#{prefix}-title)"/>',
        f'<rect x="1" y="{titlebar_h - 5}" width="{w - 2}" height="6" fill="{bg_fill}"/>',
        f'<line x1="1" y1="{titlebar_h}" x2="{w - 1}" y2="{titlebar_h}" '
        f'stroke="{frame}" stroke-opacity="0.75"/>',
        "</g>",
    ]
