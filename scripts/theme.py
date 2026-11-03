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
        # empty -> most contributions
        "ramp": ["#161b22", "#3d444d", "#6e7681", "#b1bac4", "#f0f6fc"],
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
        # empty -> most contributions (darker = more on light bg)
        "ramp": ["#ebedf0", "#c8cdd3", "#8b949e", "#484f58", "#1f2328"],
        "dots": ["#ff5f56", "#ffbd2e", "#27c93f"],
    },
}
