"""Chart colours and Plotly layout.

Polymarket's published brand blue (#2E5CFF) doubles as the primary series colour:
it passes every colour check on both surfaces (worst adjacent CVD delta-E 33.4,
contrast >= 3:1). Win/loss reuse Polymarket's own Yes-green / No-red convention.
"""
import streamlit as st

BRAND_BLUE = "#2E5CFF"

LIGHT = {
    "surface": "#fcfcfb",
    "text": "#0b0b0b",
    "text_secondary": "#52514e",
    "muted": "#898781",
    "grid": "#e1e0d9",
    "baseline": "#c3c2b7",
    "series_1": BRAND_BLUE,
    "series_2": "#008300",
    "good": "#0ca30c",
    "critical": "#d03b3b",
}

DARK = {
    "surface": "#1a1a19",
    "text": "#ffffff",
    "text_secondary": "#c3c2b7",
    "muted": "#898781",
    "grid": "#2c2c2a",
    "baseline": "#383835",
    "series_1": BRAND_BLUE,
    "series_2": "#008300",
    "good": "#0ca30c",
    "critical": "#d03b3b",
}

FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def palette():
    theme = getattr(st.context, "theme", None)
    return DARK if getattr(theme, "type", "light") == "dark" else LIGHT


def layout(height=340, showlegend=False):
    c = palette()
    return {
        "height": height,
        "showlegend": showlegend,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": FONT, "color": c["text_secondary"], "size": 13},
        "margin": {"l": 8, "r": 8, "t": 8, "b": 8},
        "hoverlabel": {"font": {"family": FONT, "size": 13}},
        "xaxis": {
            "showgrid": False,
            "linecolor": c["baseline"],
            "tickcolor": c["baseline"],
            "tickfont": {"color": c["muted"], "size": 12},
        },
        "yaxis": {
            "gridcolor": c["grid"],
            "zeroline": False,
            "showline": False,
            "tickfont": {"color": c["muted"], "size": 12},
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "font": {"color": c["text_secondary"]},
        },
    }


def fade(hex_color, alpha=0.12):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alpha})"
