"""Shared soft-3D chrome for profile SVGs (shadow + bevel + title gloss)."""

from theme import THEMES


def depth_palette(theme_name):
    t = THEMES[theme_name]
    if theme_name == "dark":
        return {
            "shadow_opacity": 0.55,
            "shadow_dy": 7,
            "shadow_blur": 10,
            "bevel_top": "#3a424c",
            "bevel_bottom": "#1a1f26",
            "gloss": "#ffffff",
            "gloss_opacity": 0.07,
            "inset": "#000000",
            "inset_opacity": 0.28,
            "glow": t["section"],
            "glow_opacity": 0.35,
        }
    return {
        "shadow_opacity": 0.16,
        "shadow_dy": 6,
        "shadow_blur": 9,
        "bevel_top": "#ffffff",
        "bevel_bottom": "#afb8c1",
        "gloss": "#ffffff",
        "gloss_opacity": 0.55,
        "inset": "#000000",
        "inset_opacity": 0.08,
        "glow": t["section"],
        "glow_opacity": 0.22,
    }


def card_depth_defs(prefix, theme_name):
    """Filters/gradients for elevated terminal cards."""
    d = depth_palette(theme_name)
    return f'''
<filter id="{prefix}-shadow" x="-12%" y="-10%" width="124%" height="130%" color-interpolation-filters="sRGB">
  <feDropShadow dx="0" dy="{d["shadow_dy"]}" stdDeviation="{d["shadow_blur"]}"
    flood-color="#000000" flood-opacity="{d["shadow_opacity"]}"/>
</filter>
<filter id="{prefix}-glow" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
  <feDropShadow dx="0" dy="0" stdDeviation="2.2"
    flood-color="{d["glow"]}" flood-opacity="{d["glow_opacity"]}"/>
</filter>
<linearGradient id="{prefix}-bevel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{d["bevel_top"]}"/>
  <stop offset="1" stop-color="{d["bevel_bottom"]}"/>
</linearGradient>
<linearGradient id="{prefix}-gloss" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{d["gloss"]}" stop-opacity="{d["gloss_opacity"]}"/>
  <stop offset="1" stop-color="{d["gloss"]}" stop-opacity="0"/>
</linearGradient>
'''.strip()


def card_chrome(prefix, w, h, titlebar_h, bg_fill, frame, rx=14):
    """Elevated card shell: shadow, fill, bevel stroke, title gloss, inset title rule."""
    return [
        f'<g filter="url(#{prefix}-shadow)">',
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="{bg_fill}"/>',
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="none" '
        f'stroke="url(#{prefix}-bevel)" stroke-width="1.4"/>',
        f'<rect x="1.5" y="1.5" width="{w - 3}" height="{titlebar_h - 1.5}" rx="{rx}" '
        f'fill="url(#{prefix}-gloss)"/>',
        # square off gloss under the titlebar so only the top is glassy
        f'<rect x="1.5" y="{titlebar_h - 6}" width="{w - 3}" height="8" fill="{bg_fill}"/>',
        f'<line x1="1" y1="{titlebar_h}" x2="{w - 1}" y2="{titlebar_h}" '
        f'stroke="{frame}" stroke-opacity="0.9"/>',
        f'<line x1="1" y1="{titlebar_h + 1}" x2="{w - 1}" y2="{titlebar_h + 1}" '
        f'stroke="#000000" stroke-opacity="0.18"/>',
        "</g>",
    ]
