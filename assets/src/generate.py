#!/usr/bin/env python3
"""
Builds the SVG graphics used in the profile README.

    python3 assets/src/generate.py

Writes into assets/. Everything is plain SVG with SMIL animation (no scripts,
no external fonts or images), which is what GitHub allows in README images.
Edit the text in the CONTENT section and re-run.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent

FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', "
        "'Segoe UI', Inter, Roboto, 'Helvetica Neue', Arial, sans-serif")

# ── CONTENT ──────────────────────────────────────────────────────────────────
NAME = "Om Gandhi"
ROLE = "Lead Mobile & Frontend Engineer"
WIDGETS = ["iOS · macOS", "React Native", "On-device AI"]

ISLAND = {
    "a": ("Nova Key", "Thinking on-device · 0 bytes sent"),
    "b": ("Release train", "Shipping weekly · used to take days"),
    "c": ("Om Gandhi", "Open to Senior iOS & Lead Mobile roles"),
}

NOTIFICATIONS = [
    # (app label, body, icon kind, gradient)
    ("MAGENTA INSIGHTS", "Leading mobile on a 5-product B2B suite · 500+ customers",
     "m", ("#FF4FA3", "#C2186B")),
    ("RELEASE HEALTH", "Production bugs down ~80% in a single quarter",
     "trend", ("#FF9F0A", "#FF453A")),
    ("OINK!", "Spending charted with Swift Charts · 100% on-device",
     "snout", ("#FF9EC0", "#FF4F8B")),
]

CARDS = [
    # (file stem, name, subtitle, tags, icon kind, gradient)
    ("nova-key", "Nova Key", "AI command palette, no cloud",
     ["Foundation Models", "macOS"], "cmd", ("#7B5CFF", "#FF2E8A")),
    ("oink", "Oink!", "On-device finance tracker",
     ["SwiftData", "Swift Charts"], "snout", ("#FF9EC0", "#FF4F8B")),
    ("translo", "Translo", "Offline ML translator",
     ["MLKit", "No server"], "globe", ("#0A84FF", "#5E5CE6")),
]

ACCENT = "#FF2E8A"
DUR = 18.0  # seconds for one loop of the hero


# ── helpers ──────────────────────────────────────────────────────────────────
def kt(times):
    return ";".join(f"{t / DUR:.4f}" for t in times)


def anim(attr, frames, extra=""):
    """frames: list of (seconds, value). One loop of DUR seconds."""
    times = [f[0] for f in frames]
    values = ";".join(str(f[1]) for f in frames)
    return (f'<animate attributeName="{attr}" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{kt(times)}" values="{values}" {extra}/>')


def spline_anim(attr, frames):
    n = len(frames) - 1
    splines = ";".join(["0.32 0.0 0.18 1"] * n)
    return anim(attr, frames, f'calcMode="spline" keySplines="{splines}"')


def fade(on_from, on_to, fade_in=0.3, fade_out=0.2):
    """Opacity 0 -> 1 between on_from and on_to inside the loop."""
    frames = [(0, 0), (on_from, 0), (on_from + fade_in, 1),
              (on_to - fade_out, 1), (on_to, 0), (DUR, 0)]
    if on_from == 0:
        frames = frames[1:]
        frames[0] = (0, 0)
    return anim("opacity", frames)


def text(x, y, s, size, weight=400, fill="#fff", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>'
            f"{escape(s)}</text>")


def icon(kind, x, y, size, grad_id):
    """App-icon style squircle with a simple white glyph."""
    r = size * 0.23
    s = size
    cx, cy = x + s / 2, y + s / 2
    out = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r:.1f}" fill="url(#{grad_id})"/>']
    if kind == "cmd":
        out.append(text(cx, cy + s * 0.2, "⌘", s * 0.56, 500, anchor="middle"))
    elif kind == "m":
        out.append(text(cx, cy + s * 0.19, "M", s * 0.52, 800, anchor="middle"))
    elif kind == "snout":
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.3:.1f}" ry="{s*0.22:.1f}" fill="#fff"/>')
        for dx in (-0.1, 0.1):
            out.append(f'<ellipse cx="{cx + s*dx:.1f}" cy="{cy}" rx="{s*0.05:.1f}" ry="{s*0.08:.1f}" fill="url(#{grad_id})"/>')
    elif kind == "trend":
        pts = [(0.2, 0.3), (0.4, 0.45), (0.55, 0.38), (0.8, 0.72)]
        p = " ".join(f"{x + s*a:.1f},{y + s*b:.1f}" for a, b in pts)
        out.append(f'<polyline points="{p}" fill="none" stroke="#fff" stroke-width="{s*0.08:.1f}" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        ax, ay = x + s * 0.8, y + s * 0.72
        out.append(f'<polyline points="{ax - s*0.2:.1f},{ay:.1f} {ax:.1f},{ay:.1f} {ax:.1f},{ay - s*0.2:.1f}" '
                   f'fill="none" stroke="#fff" stroke-width="{s*0.08:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "globe":
        rr = s * 0.3
        sw = s * 0.055
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="#fff" stroke-width="{sw:.1f}"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rr*0.45:.1f}" ry="{rr:.1f}" fill="none" stroke="#fff" stroke-width="{sw:.1f}"/>')
        out.append(f'<line x1="{cx-rr:.1f}" y1="{cy}" x2="{cx+rr:.1f}" y2="{cy}" stroke="#fff" stroke-width="{sw:.1f}"/>')
    elif kind == "up":
        out.append(f'<polyline points="{cx-s*0.17:.1f},{cy-s*0.02:.1f} {cx},{cy-s*0.2:.1f} {cx+s*0.17:.1f},{cy-s*0.02:.1f}" '
                   f'fill="none" stroke="#fff" stroke-width="{s*0.09:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<line x1="{cx}" y1="{cy-s*0.18:.1f}" x2="{cx}" y2="{cy+s*0.22:.1f}" stroke="#fff" '
                   f'stroke-width="{s*0.09:.1f}" stroke-linecap="round"/>')
    elif kind == "og":
        out[0] = f'<circle cx="{cx}" cy="{cy}" r="{s/2}" fill="url(#{grad_id})"/>'
        out.append(text(cx, cy + s * 0.15, "OG", s * 0.4, 700, anchor="middle"))
    return "".join(out)


def gradient(gid, c1, c2, x2="1", y2="1"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


# ── hero: an animated lock screen ────────────────────────────────────────────
def hero():
    W, H = 900, 520
    CX = W / 2
    compact = (160, 46, 20)
    expanded = (600, 92, 16)

    # Island geometry keyframes with a little spring on each change.
    def island_frames():
        f = [(0, compact), (0.8, compact)]
        for start, hold_until in ((0.8, 5.0), (6.4, 10.8), (12.2, 16.8)):
            if start != 0.8:
                f.append((start, compact))
            f.append((start + 0.42, (expanded[0] + 18, expanded[1] + 4, expanded[2] - 1)))
            f.append((start + 0.62, expanded))
            f.append((hold_until, expanded))
            f.append((hold_until + 0.38, (compact[0] - 10, compact[1] - 2, compact[2] + 1)))
            f.append((hold_until + 0.55, compact))
        f.append((DUR, compact))
        return f

    frames = island_frames()
    geo = {
        "x": [(t, round(CX - w / 2, 1)) for t, (w, h, y) in frames],
        "y": [(t, y) for t, (w, h, y) in frames],
        "width": [(t, w) for t, (w, h, y) in frames],
        "height": [(t, h) for t, (w, h, y) in frames],
        "rx": [(t, h / 2) for t, (w, h, y) in frames],
    }
    island_anims = "".join(spline_anim(a, v) for a, v in geo.items())

    ex = CX - expanded[0] / 2          # expanded island left edge (150)
    mid = expanded[2] + expanded[1] / 2  # vertical centre (62)

    defs = [
        gradient("wall", "#0B0614", "#140A26", "0", "1"),
        gradient("nameFill", "#FFFFFF", "#FFD3E6", "0", "1"),
        gradient("gA", "#7B5CFF", ACCENT),
        gradient("gB", "#30D158", "#0A84FF"),
        gradient("gC", "#FF9F0A", ACCENT),
        # userSpaceOnUse: a bounding-box gradient on a zero-width line would not render
        f'<linearGradient id="wave" gradientUnits="userSpaceOnUse" x1="0" y1="{mid - 17}" x2="0" y2="{mid + 17}">'
        '<stop offset="0" stop-color="#FF7AC0"/><stop offset="1" stop-color="#7B5CFF"/></linearGradient>',
        '<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="70"/></filter>',
        f'<clipPath id="screen"><rect x="0" y="0" width="{W}" height="{H}" rx="44"/></clipPath>',
    ]
    for i, (_, _, _, (c1, c2)) in enumerate(NOTIFICATIONS):
        defs.append(gradient(f"n{i}", c1, c2))

    blobs = [
        (170, 110, 230, ACCENT, "0 0; 70 50; 0 0", 19),
        (740, 150, 250, "#6D5BFF", "0 0; -60 70; 0 0", 23),
        (520, 560, 220, "#FF8A3D", "0 0; -80 -40; 0 0", 17),
        (90, 470, 160, "#3A2BFF", "0 0; 50 -30; 0 0", 21),
    ]
    blob_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.55">'
        f'<animateTransform attributeName="transform" type="translate" values="{v}" '
        f'dur="{d}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></circle>'
        for x, y, r, c, v, d in blobs)

    # status bar
    status = [text(70, 50, "9:41", 18, 600)]
    bx = 772
    for i, h in enumerate((5, 8, 11, 14)):
        status.append(f'<rect x="{bx + i*6}" y="{46 - h}" width="4" height="{h}" rx="1.2" fill="#fff"/>')
    wx, wy = 812, 46
    for i, r in enumerate((4, 8.5, 13)):
        if i == 0:
            status.append(f'<circle cx="{wx}" cy="{wy - 1}" r="2.2" fill="#fff"/>')
        else:
            status.append(f'<path d="M{wx - r*0.75:.1f},{wy - r*0.66:.1f} A{r},{r} 0 0 1 {wx + r*0.75:.1f},{wy - r*0.66:.1f}" '
                          f'fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>')
    status.append('<rect x="832" y="34" width="27" height="13" rx="4" fill="none" stroke="#fff" stroke-opacity="0.45" stroke-width="1.2"/>'
                  '<rect x="834.5" y="36.5" width="19" height="8" rx="2" fill="#fff"/>'
                  '<rect x="861" y="38.5" width="2" height="4" rx="1" fill="#fff" fill-opacity="0.45"/>')

    # camera lens, visible only while compact
    cam_frames = [(0, 1), (0.8, 1), (0.95, 0)]
    for hold_until, nxt in ((5.0, 6.4), (10.8, 12.2), (16.8, None)):
        cam_frames += [(hold_until + 0.5, 0), (hold_until + 0.7, 1)]
        if nxt:
            cam_frames += [(nxt, 1), (nxt + 0.15, 0)]
    cam_frames.append((DUR, 1))
    camera = (f'<g>{anim("opacity", cam_frames)}<circle cx="{CX + 58}" cy="43" r="7" fill="#15151a"/>'
              f'<circle cx="{CX + 58}" cy="43" r="3" fill="#24243a"/></g>')

    # live activity A: Nova Key, waveform
    bars = []
    pattern = ["8;30;12;24;8", "14;10;32;12;14", "22;34;10;28;22", "10;24;30;8;10",
               "26;12;20;34;26", "12;30;14;22;12", "8;18;28;10;8"]
    for i, p in enumerate(pattern):
        x = ex + 500 + i * 11
        hs = [float(v) for v in p.split(";")]
        y1 = ";".join(f"{mid - h/2:.1f}" for h in hs)
        y2 = ";".join(f"{mid + h/2:.1f}" for h in hs)
        bars.append(f'<line x1="{x}" x2="{x}" y1="{mid-4}" y2="{mid+4}" stroke="url(#wave)" stroke-width="5" stroke-linecap="round">'
                    f'<animate attributeName="y1" values="{y1}" dur="1.1s" begin="-{i*0.13:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y2" values="{y2}" dur="1.1s" begin="-{i*0.13:.2f}s" repeatCount="indefinite"/></line>')

    def activity_text(title, sub):
        return (text(ex + 86, mid - 4, title, 18, 600) +
                text(ex + 86, mid + 20, sub, 14.5, 400, "#fff", extra='fill-opacity="0.62"'))

    act_a = (f'<g opacity="0">{fade(1.25, 4.95)}'
             + icon("cmd", ex + 26, mid - 24, 48, "gA")
             + activity_text(*ISLAND["a"]) + "".join(bars) + "</g>")

    # live activity B: release train, progress ring then check
    circ = 2 * 3.14159 * 17
    ring_frames = [(0, circ), (7.1, circ), (9.6, 0), (10.8, 0), (10.9, circ), (DUR, circ)]
    check_frames = [(0, 0), (9.6, 0), (9.85, 1), (10.6, 1), (10.75, 0), (DUR, 0)]
    rcx = ex + 548
    act_b = (f'<g opacity="0">{fade(6.85, 10.75)}'
             + icon("up", ex + 26, mid - 24, 48, "gB")
             + activity_text(*ISLAND["b"])
             + f'<circle cx="{rcx}" cy="{mid}" r="17" fill="none" stroke="#fff" stroke-opacity="0.14" stroke-width="5"/>'
             + f'<circle cx="{rcx}" cy="{mid}" r="17" fill="none" stroke="#30D158" stroke-width="5" stroke-linecap="round" '
               f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ:.2f}" transform="rotate(-90 {rcx} {mid})">'
             + anim("stroke-dashoffset", ring_frames) + "</circle>"
             + f'<polyline points="{rcx-7},{mid} {rcx-2},{mid+5} {rcx+8},{mid-6}" fill="none" stroke="#30D158" '
               f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
             + anim("opacity", check_frames) + "</polyline></g>")

    # live activity C: open to work, pulsing dot
    dcx = ex + 552
    act_c = (f'<g opacity="0">{fade(12.65, 16.75)}'
             + icon("og", ex + 26, mid - 24, 48, "gC")
             + activity_text(*ISLAND["c"])
             + f'<circle cx="{dcx}" cy="{mid}" r="7" fill="none" stroke="#30D158" stroke-width="2">'
               '<animate attributeName="r" values="7;20" dur="1.6s" repeatCount="indefinite"/>'
               '<animate attributeName="opacity" values="0.8;0" dur="1.6s" repeatCount="indefinite"/></circle>'
             + f'<circle cx="{dcx}" cy="{mid}" r="7" fill="#30D158"/></g>')

    # lock screen text
    lock = [
        text(CX, 176, ROLE, 22, 600, "#fff", "middle", 'fill-opacity="0.9" letter-spacing="0.2"'),
        text(CX, 286, NAME, 118, 700, "url(#nameFill)", "middle", 'letter-spacing="-3"'),
    ]
    # widget pills, widths estimated from text length; text is centred so font differences stay symmetric
    widths = [len(w) * 8.4 + 40 for w in WIDGETS]
    gap = 12
    x = CX - (sum(widths) + gap * (len(widths) - 1)) / 2
    for w, label in zip(widths, WIDGETS):
        lock.append(f'<rect x="{x:.1f}" y="312" width="{w:.1f}" height="34" rx="17" fill="#fff" fill-opacity="0.13" '
                    'stroke="#fff" stroke-opacity="0.12"/>')
        lock.append(text(round(x + w / 2, 1), 334, label, 15, 500, "#fff", "middle", 'fill-opacity="0.92"'))
        x += w + gap

    # notifications: one slot, a stacked card peeking out underneath
    nx, ny, nw, nh = CX - 300, 376, 600, 70
    notes = [f'<rect x="{nx + 22}" y="{ny + 14}" width="{nw - 44}" height="{nh}" rx="20" fill="#fff" fill-opacity="0.07" opacity="0">'
             + anim("opacity", [(0, 0), (0.9, 0), (1.2, 1), (17.7, 1), (18.0, 0)]) + "</rect>"]
    slots = [(0.6, 5.9), (6.2, 11.9), (12.2, 17.7)]
    for i, ((app, body, kind, _), (t_in, t_out)) in enumerate(zip(NOTIFICATIONS, slots)):
        move = [(0, "0 34"), (t_in, "0 34"), (t_in + 0.45, "0 0"), (t_out, "0 0"), (t_out + 0.3, "0 -16"), (DUR, "0 -16")]
        times = [m[0] for m in move]
        vals = ";".join(m[1] for m in move)
        notes.append(
            f'<g opacity="0">{fade(t_in, t_out + 0.3, 0.4, 0.3)}'
            f'<animateTransform attributeName="transform" type="translate" dur="{DUR}s" repeatCount="indefinite" '
            f'keyTimes="{kt(times)}" values="{vals}" calcMode="spline" '
            f'keySplines="{";".join(["0.32 0 0.18 1"] * (len(move) - 1))}"/>'
            f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="20" fill="#fff" fill-opacity="0.16" '
            'stroke="#fff" stroke-opacity="0.1"/>'
            + icon(kind, nx + 16, ny + 15, 40, f"n{i}")
            + text(nx + 70, ny + 29, app, 12, 600, "#fff", extra='fill-opacity="0.6" letter-spacing="0.6"')
            + text(nx + nw - 18, ny + 29, "now", 12, 400, "#fff", "end", 'fill-opacity="0.5"')
            + text(nx + 70, ny + 52, body, 15.5, 500)
            + "</g>")

    # flashlight + camera buttons, home indicator
    buttons = []
    for bcx, kind in ((92, "torch"), (W - 92, "camera")):
        buttons.append(f'<circle cx="{bcx}" cy="468" r="26" fill="#fff" fill-opacity="0.14"/>')
        if kind == "torch":
            buttons.append(f'<path d="M{bcx-6},456 h12 l-2,8 v14 a2,2 0 0 1 -2,2 h-4 a2,2 0 0 1 -2,-2 v-14 z" fill="none" '
                           'stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'
                           f'<circle cx="{bcx}" cy="468" r="1.6" fill="#fff"/>')
        else:
            buttons.append(f'<rect x="{bcx-12}" y="460" width="24" height="17" rx="4" fill="none" stroke="#fff" stroke-width="2"/>'
                           f'<path d="M{bcx-5},460 l2,-4 h6 l2,4" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'
                           f'<circle cx="{bcx}" cy="468.5" r="4.5" fill="none" stroke="#fff" stroke-width="2"/>')
    home = f'<rect x="{CX - 70}" y="503" width="140" height="5" rx="2.5" fill="#fff" fill-opacity="0.85"/>'

    island = (f'<rect x="{CX - compact[0]/2}" y="{compact[2]}" width="{compact[0]}" height="{compact[1]}" '
              f'rx="{compact[1]/2}" fill="#000">{island_anims}</rect>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(NAME)}, {escape(ROLE)}">
<title>{escape(NAME)} · {escape(ROLE)}</title>
<defs>{"".join(defs)}</defs>
<g clip-path="url(#screen)">
<rect width="{W}" height="{H}" fill="url(#wall)"/>
<g filter="url(#blur)">{blob_svg}</g>
<rect width="{W}" height="{H}" fill="#000" fill-opacity="0.12"/>
{"".join(status)}
{"".join(lock)}
{"".join(notes)}
{"".join(buttons)}
{home}
{island}
{camera}
{act_a}
{act_b}
{act_c}
</g>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="43.5" fill="none" stroke="#fff" stroke-opacity="0.14" stroke-width="1.5"/>
</svg>
'''
    return svg


# ── project cards, App Store style ───────────────────────────────────────────
THEMES = {
    "dark": dict(bg="#161B22", border="#30363D", fg="#E6EDF3", muted="#8B949E",
                 chip="#21262D", chip_fg="#C9D1D9", btn="#0A84FF", btn_bg="#0A84FF26"),
    "light": dict(bg="#FFFFFF", border="#D0D7DE", fg="#1F2328", muted="#656D76",
                  chip="#F2F4F7", chip_fg="#424A53", btn="#0071E3", btn_bg="#0071E31A"),
}


def card(name, sub, tags, kind, grad, t):
    W, H = 300, 156
    parts = [f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>',
             icon(kind, 20, 20, 64, "g"),
             text(100, 48, name, 19, 650, t["fg"]),
             text(100, 71, sub, 13.5, 400, t["muted"]),
             f'<rect x="214" y="34" width="66" height="28" rx="14" fill="{t["btn_bg"]}"/>',
             text(247, 53, "VIEW", 13, 700, t["btn"], "middle", 'letter-spacing="0.4"')]
    x = 20
    for tag in tags:
        w = len(tag) * 7.1 + 22
        parts.append(f'<rect x="{x:.1f}" y="106" width="{w:.1f}" height="28" rx="14" fill="{t["chip"]}"/>')
        parts.append(text(round(x + w / 2, 1), 124.5, tag, 12.5, 500, t["chip_fg"], "middle"))
        x += w + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{escape(name)}: {escape(sub)}"><title>{escape(name)}</title>'
            f'<defs>{gradient("g", *grad)}</defs>{"".join(parts)}</svg>\n')


# ── footer: slide to say hi ──────────────────────────────────────────────────
def say_hi(t, mode):
    W, H = 420, 76
    base, shine = (t["muted"], "#FFFFFF") if mode == "dark" else ("#8C959F", "#1F2328")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Slide to say hi: email Om">
<title>Say hi</title>
<defs>
{gradient("knob", "#FF5FA8", ACCENT)}
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="160" y2="0">
<stop offset="0" stop-color="{base}"/><stop offset="0.5" stop-color="{shine}"/><stop offset="1" stop-color="{base}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-60 0; 380 0" dur="2.6s" repeatCount="indefinite"/>
</linearGradient>
</defs>
<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{(H-1.5)/2}" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
<g>
<animateTransform attributeName="transform" type="translate" values="0 0; 16 0; 0 0; 0 0" keyTimes="0;0.12;0.26;1" dur="3.2s" repeatCount="indefinite" calcMode="spline" keySplines="0.3 0 0.2 1;0.3 0 0.2 1;0 0 1 1"/>
<circle cx="38" cy="38" r="28" fill="url(#knob)"/>
<polyline points="33,28 43,38 33,48" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<text x="{(W + 66) / 2}" y="46" font-family="{FONT}" font-size="22" font-weight="500" fill="url(#shine)" text-anchor="middle">slide to say hi</text>
</svg>
'''


def main():
    (OUT / "hero.svg").write_text(hero())
    for mode, t in THEMES.items():
        for stem, name, sub, tags, kind, grad in CARDS:
            (OUT / f"card-{stem}-{mode}.svg").write_text(card(name, sub, tags, kind, grad, t))
        (OUT / f"say-hi-{mode}.svg").write_text(say_hi(t, mode))
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
