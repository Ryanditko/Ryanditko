"""Shared soft elevation + stage atmosphere for profile SVGs.

Painted shadow stacks (not only SVG filters) so GitHub Camo / <img>
actually shows the lift. Stage washes give the README a shared floor
behind floating cards.
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
            "cast": [
                (0, 18, 10, 0.22),
                (0, 10, 4, 0.28),
                (0, 4, 1, 0.40),
            ],
            "stage": "#0d1117",
            "stage2": "#101a14",
            "glow": t["section"],
            "glow2": t["accent"],
            "grid": "#8fe0a5",
            "grid_opacity": 0.045,
            "vignette": "#000000",
            "vignette_opacity": 0.55,
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
        "stage": "#ffffff",
        "stage2": "#eef7f1",
        "glow": t["section"],
        "glow2": t["accent"],
        "grid": "#1a7f37",
        "grid_opacity": 0.05,
        "vignette": "#8b949e",
        "vignette_opacity": 0.12,
    }


def card_depth_defs(prefix, theme_name):
    """Filters/gradients for elevated cards + local stage floor."""
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
<filter id="{prefix}-glowblur" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">
  <feGaussianBlur stdDeviation="28"/>
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
<radialGradient id="{prefix}-stage" cx="50%" cy="42%" r="68%">
  <stop offset="0" stop-color="{d["stage2"]}"/>
  <stop offset="1" stop-color="{d["stage"]}"/>
</radialGradient>
<radialGradient id="{prefix}-orb" cx="50%" cy="55%" r="45%">
  <stop offset="0" stop-color="{d["glow"]}" stop-opacity="{0.22 if theme_name == "dark" else 0.14}"/>
  <stop offset="1" stop-color="{d["glow"]}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="{prefix}-orb2" cx="18%" cy="20%" r="40%">
  <stop offset="0" stop-color="{d["glow2"]}" stop-opacity="{0.12 if theme_name == "dark" else 0.08}"/>
  <stop offset="1" stop-color="{d["glow2"]}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="{prefix}-vig" cx="50%" cy="50%" r="72%">
  <stop offset="0.55" stop-color="{d["vignette"]}" stop-opacity="0"/>
  <stop offset="1" stop-color="{d["vignette"]}" stop-opacity="{d["vignette_opacity"]}"/>
</radialGradient>
'''.strip()


def stage_floor(prefix, w, h, theme_name):
    """Atmosphere painted on the SVG canvas behind a floating card."""
    d = depth_palette(theme_name)
    # faint terminal grid
    step = 28
    grid = []
    for x in range(0, int(w) + 1, step):
        grid.append(
            f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{d["grid"]}" '
            f'stroke-opacity="{d["grid_opacity"]}" stroke-width="1"/>'
        )
    for y in range(0, int(h) + 1, step):
        grid.append(
            f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{d["grid"]}" '
            f'stroke-opacity="{d["grid_opacity"]}" stroke-width="1"/>'
        )
    return [
        f'<rect width="{w}" height="{h}" fill="url(#{prefix}-stage)"/>',
        f'<ellipse cx="{w * 0.5:.1f}" cy="{h * 0.62:.1f}" rx="{w * 0.42:.1f}" ry="{h * 0.28:.1f}" '
        f'fill="url(#{prefix}-orb)" filter="url(#{prefix}-glowblur)"/>',
        f'<ellipse cx="{w * 0.18:.1f}" cy="{h * 0.22:.1f}" rx="{w * 0.28:.1f}" ry="{h * 0.18:.1f}" '
        f'fill="url(#{prefix}-orb2)" filter="url(#{prefix}-glowblur)"/>',
        f'<g>{"".join(grid)}</g>',
        f'<rect width="{w}" height="{h}" fill="url(#{prefix}-vig)"/>',
    ]


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
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" '
        f'fill="url(#{prefix}-face)"/>'
    )
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="{d["rim"]}" stroke-opacity="{d["rim_opacity"]}" stroke-width="1"/>'
    )
    parts.append(
        f'<path d="M {rx + 0.5} 1.2 H {w - rx - 0.5}" stroke="{d["edge"]}" '
        f'stroke-opacity="{d["edge_opacity"]}" stroke-width="1.2" fill="none"/>'
    )
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
