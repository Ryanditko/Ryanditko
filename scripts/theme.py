"""Shared light/dark palettes for profile SVGs (GitHub theme aware)."""

# Portrait + info card must share the same canvas so the README table stays even.
CARD_W = 520
CARD_H = 568

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "bg2": "#111722",
        "frame": "#30363d",
        "muted": "#7d8590",
        "ink": "#c9d1d9",
        "key": "#f0f6fc",
        "section": "#8fe0a5",  # previous pastel green (was blue)
        "accent": "#a8e6c1",
        "total": "#e6edf3",
        # empty -> most: dark green -> brand green (#8fe0a5) -> near-white mint
        "ramp": ["#161b22", "#2d4a3a", "#5c9b74", "#8fe0a5", "#eaf8ef"],
        "dots": ["#ff5f56", "#ffbd2e", "#27c93f"],
    },
    "light": {
        "bg": "#ffffff",
        "bg2": "#f6f8fa",
        "frame": "#d0d7de",
        "muted": "#656d76",
        "ink": "#1f2328",
        "key": "#1f2328",
        "section": "#1a7f37",  # green readable on light bg
        "accent": "#2da44e",
        "total": "#1f2328",
        # empty -> most: pale mint -> brand green -> deeper green
        "ramp": ["#ebedf0", "#cfeeda", "#8fe0a5", "#3f9b6a", "#1a7f37"],
        "dots": ["#ff5f56", "#ffbd2e", "#27c93f"],
    },
}
