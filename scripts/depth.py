"""Shared soft elevation for profile SVGs.

Painted shadow stacks (not only SVG filters) so GitHub Camo / <img>
actually shows the lift. Cards get a stronger stack than pills.
"""

from theme import THEMES


def depth_palette(theme_name):
    t = THEMES[theme_name]
    if theme_name == "dark":
        return {
            "ambient_opacity": 0.55,
            "ambient_dy": 12,
            "ambient_blur": 14,
            "contact_opacity": 0.55,
            "contact_dy": 3,
            "contact_blur": 4,
            "rim": t["frame"],
            "rim_opacity": 1.0,
            "edge": "#ffffff",
            "edge_opacity": 0.10,
            "bottom_edge": "#000000",
            "bottom_edge_opacity": 0.45,
            "title_fill": "#ffffff",
            "title_opacity": 0.04,
            # painted layers behind the card (dx, dy, grow, opacity)
            "cast": [
                (0, 18, 10, 0.22),
                (0, 10, 4, 0.28),
                (0, 4, 1, 0.40),
            ],
        }
    return {
        "ambient_opacity": 0.14,
        "ambient_dy": 10,
        "ambient_blur": 12,
        "contact_opacity": 0.12,
        "contact_dy": 2,
        "contact_blur": 3,
        "rim": t["frame"],
        "rim_opacity": 1.0,
        "edge": "#ffffff",
        "edge_opacity": 0.95,
        "bottom_edge": "#8b949e",
        "bottom_edge_opacity": 0.55,
        "title_fill": "#ffffff",
        "title_opacity": 0.55,
        "cast": [
            (0, 16, 8, 0.08),
            (0, 8, 3, 0.10),
            (0, 3, 0, 0.12),
        ],
    }


def card_depth_defs(prefix, theme_name):
    """Filters/gradients for softly elevated cards."""
    d = depth_palette(theme_name)
    return f'''
<filter id="{prefix}-shadow" x="-25%" y="-20%" width="150%" height="160%" color-interpolation-filters="sRGB">
  <feDropShadow dx="0" dy="{d["ambient_dy"]}" stdDeviation="{d["ambient_blur"]}"
    flood-color="#000000" flood-opacity="{d["ambient_opacity"]}"/>
  <feDropShadow dx="0" dy="{d["contact_dy"]}" stdDeviation="{d["contact_blur"]}"
    flood-color="#000000" flood-opacity="{d["contact_opacity"]}"/>
</filter>
<filter id="{prefix}-blur" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
  <feGaussianBlur stdDeviation="7"/>
</filter>
<linearGradient id="{prefix}-title" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{d["title_fill"]}" stop-opacity="{d["title_opacity"]}"/>
  <stop offset="1" stop-color="{d["title_fill"]}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="{prefix}-face" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="{0.05 if theme_name == "dark" else 0.35}"/>
  <stop offset="0.35" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset="1" stop-color="#000000" stop-opacity="{0.18 if theme_name == "dark" else 0.04}"/>
</linearGradient>
'''.strip()


def painted_cast_shadow(prefix, w, h, theme_name, rx=16):
    """Opaque-enough soft blobs under the card (visible even if filters clip)."""
    d = depth_palette(theme_name)
    parts = []
    for dx, dy, grow, opacity in d["cast"]:
        parts.append(
            f'<rect x="{-grow + dx}" y="{dy}" width="{w + grow * 2}" height="{h + grow}" '
            f'rx="{rx + grow // 2}" fill="#000000" opacity="{opacity}" '
            f'filter="url(#{prefix}-blur)"/>'
        )
    return parts


def card_chrome(prefix, w, h, titlebar_h, bg_fill, frame, rx=16):
    """Floating card with painted cast + filter shadow, rim, face gradient."""
    theme = "light" if prefix.endswith("light") else "dark"
    d = depth_palette(theme)
    parts = []
    parts.extend(painted_cast_shadow(prefix, w, h, theme, rx=rx))
    parts.append(f'<g filter="url(#{prefix}-shadow)">')
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{bg_fill}"/>'
    )
    # subtle top-lit / bottom-shaded face
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" '
        f'fill="url(#{prefix}-face)"/>'
    )
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="{d["rim"]}" stroke-opacity="{d["rim_opacity"]}" stroke-width="1"/>'
    )
    # top rim catch-light
    parts.append(
        f'<path d="M {rx + 0.5} 1.2 H {w - rx - 0.5}" stroke="{d["edge"]}" '
        f'stroke-opacity="{d["edge_opacity"]}" stroke-width="1.2" fill="none"/>'
    )
    # bottom rim contact line (grounds the card)
    parts.append(
        f'<path d="M {rx + 0.5} {h - 1.2} H {w - rx - 0.5}" stroke="{d["bottom_edge"]}" '
        f'stroke-opacity="{d["bottom_edge_opacity"]}" stroke-width="1.2" fill="none"/>'
    )
    parts.append(
        f'<rect x="1" y="1" width="{w - 2}" height="{titlebar_h - 1}" rx="{rx}" '
        f'fill="url(#{prefix}-title)"/>'
    )
    parts.append(
        f'<rect x="1" y="{titlebar_h - 5}" width="{w - 2}" height="6" fill="{bg_fill}"/>'
    )
    parts.append(
        f'<line x1="1" y1="{titlebar_h}" x2="{w - 1}" y2="{titlebar_h}" '
        f'stroke="{frame}" stroke-opacity="0.75"/>'
    )
    parts.append("</g>")
    return parts
