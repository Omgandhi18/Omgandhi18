#!/usr/bin/env python3
"""
Wraps the contribution snake from Platane/snk in an iOS-style Activity widget.

    python3 assets/src/frame_activity.py dist/snake.svg dist

Writes activity-light.svg and activity-dark.svg next to it: the progress bar
under the grid is removed, the colours are swapped for the README palette, and
the grid sits inside a rounded widget card with a title.
"""
import re
import sys
from pathlib import Path

FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', "
        "'Segoe UI', Inter, Roboto, 'Helvetica Neue', Arial, sans-serif")

THEMES = {
    "light": dict(card="#FFFFFF", border="#E5E5EA", fg="#000000", muted="#8A8A8E", accent="#E0167A",
                  empty="#EFEFF4", cells=["#FFD3E6", "#FF9CC8", "#FF5EA8", "#E0167A"],
                  snake="#007AFF", outline="#0000000A"),
    "dark": dict(card="#1C1C1E", border="#38383A", fg="#FFFFFF", muted="#98989F", accent="#FF2E8A",
                 empty="#2C2C2E", cells=["#4A1630", "#7A1D4D", "#C2186B", "#FF2E8A"],
                 snake="#0A84FF", outline="#FFFFFF0A"),
}

W, H = 900, 250
GRID_VIEWBOX = "-4 -20 872 152"  # the grid plus the room the snake moves through


def frame(src: str, mode: str) -> str:
    t = THEMES[mode]
    raw = Path(src).read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)
    inner = re.sub(r"<desc>.*?</desc>", "", inner, flags=re.S)
    inner = re.sub(r'<rect class="u[^"]*"[^>]*/>', "", inner)  # the progress bar under the grid
    c1, c2, c3, c4 = t["cells"]
    palette = (f':root{{--cb:{t["outline"]};--cs:{t["snake"]};--ce:{t["empty"]};--c0:{t["empty"]};'
               f'--c1:{c1};--c2:{c2};--c3:{c3};--c4:{c4}}}')
    inner, n = re.subn(r":root\{[^}]*\}", palette, inner, count=1)
    if not n:
        sys.exit("unexpected snake SVG: no :root colour block")

    def text(x, y, s, size, weight, fill, anchor="start", extra=""):
        return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
                f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')

    legend = "".join(
        f'<rect x="{W - 136 + i * 16}" y="49" width="12" height="12" rx="3" fill="{c}"/>'
        for i, c in enumerate([t["empty"], c1, c2, c3, c4]))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        'aria-label="Activity: my contribution graph, eaten by a snake every night">'
        '<title>Activity</title>'
        f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="28" fill="{t["card"]}" '
        f'stroke="{t["border"]}" stroke-width="1.5"/>'
        # small Activity-ring glyph next to the label
        f'<circle cx="34" cy="33" r="8" fill="none" stroke="{t["accent"]}" stroke-width="3.5"/>'
        + text(50, 38, "ACTIVITY", 12.5, 700, t["accent"], extra='letter-spacing="0.8"')
        + text(28, 72, "Contribution graph", 24, 700, t["fg"], extra='letter-spacing="-0.3"')
        + text(W - 146, 59, "Less", 12, 500, t["muted"], "end") + legend
        + text(W - 52, 59, "More", 12, 500, t["muted"])
        + f'<svg x="22" y="92" width="872" height="152" viewBox="{GRID_VIEWBOX}">{inner}</svg>'
        + "</svg>\n")


def main():
    src, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for mode in THEMES:
        (out / f"activity-{mode}.svg").write_text(frame(src, mode))
    print("wrote activity-light.svg and activity-dark.svg")


if __name__ == "__main__":
    main()
