#!/usr/bin/env python3
"""
Builds the iOS-themed SVGs used in the profile README.

    python3 assets/src/generate.py

Writes into assets/. Everything is plain SVG with SMIL animation (no scripts,
no external fonts or images), which is what GitHub allows in README images.
Edit the CONTENT section and re-run. The Activity widget is built separately by
frame_activity.py inside the snake workflow, because it wraps a file generated
there every night.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent

FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', "
        "'Segoe UI', Inter, Roboto, 'Helvetica Neue', Arial, sans-serif")

# ── CONTENT ──────────────────────────────────────────────────────────────────
NAME = "Om Gandhi"
ROLE = "Lead Mobile & Frontend Engineer"
LOCATION = "Ahmedabad, India · Remote · Open to visa sponsorship"
WIDGET_PILLS = ["iOS · macOS", "React Native", "On-device AI"]

ISLAND = {
    "a": ("Nova Key", "Thinking on-device · 0 bytes sent"),
    "b": ("Release train", "Shipping weekly · used to take days"),
    "c": ("Om Gandhi", "Open to Senior iOS & Lead Mobile roles"),
}

NOTIFICATIONS = [
    ("MAGENTA INSIGHTS", "Leading mobile on a 5-product B2B suite · 500+ customers",
     "m", ("#FF4FA3", "#C2186B")),
    ("RELEASE HEALTH", "Production bugs down ~80% in a single quarter",
     "trend", ("#FF9F0A", "#FF453A")),
    ("OINK!", "Spending charted with Swift Charts · 100% on-device",
     "snout", ("#FF9EC0", "#FF4F8B")),
]

# iMessage: the viewer asks (blue, right), Om answers (grey, left)
CHAT = [
    ("me", ["Hey Om! What do you build?"]),
    ("om", ["Mobile products that ship and stay shipped."]),
    ("om", ["I lead iOS, macOS and cross-platform engineering",
            "at Magenta Insights, on a 5-product B2B suite."]),
    ("me", ["What are you into lately?"]),
    ("om", ["On-device AI: features that run fully local,",
            "protect privacy, and cost nothing to serve."]),
    ("me", ["Open to new roles?"]),
    ("om", ["Yes! Senior iOS, Lead Mobile or Senior Frontend.",
            "Remote, and open to visa sponsorship."]),
]

APPS = [
    # (file stem, name, subtitle, details, icon, gradient)
    ("nova-key", "Nova Key", "AI command palette for macOS",
     "Apple Foundation Models · Zero data egress · App Store", "cmd", ("#7B5CFF", "#FF2E8A")),
    ("oink", "Oink!", "Personal finance tracker",
     "SwiftData · Swift Charts · Fully on-device · App Store", "snout", ("#FF9EC0", "#FF4F8B")),
    ("translo", "Translo", "Offline ML translator",
     "Google MLKit · No server · No latency · No cost", "globe", ("#0A84FF", "#5E5CE6")),
]

WIDGETS = [
    # (label, big value, caption, decoration)
    ("LEADING MOBILE", "3+ yrs", "iOS · macOS · RN", None),
    ("MAGENTA INSIGHTS", "500+", "customers · 5 products", None),
    ("PRODUCTION BUGS", "−80%", "in a single quarter", "spark"),
    ("RELEASES", "Weekly", "used to take days", "bars"),
]

# Home Screen icons: (label, monogram or glyph, gradient)
STACK = [
    ("Swift", "Sw", ("#FF8A50", "#F0432B")),
    ("SwiftUI", "UI", ("#5AC8FA", "#0A84FF")),
    ("UIKit", "Kit", ("#9AA6FF", "#5E5CE6")),
    ("Core ML", "ML", ("#3EE6A8", "#00A36C")),
    ("Foundation", "spark", ("#B07CFF", "#FF2E8A")),
    ("SwiftData", "SD", ("#62DCEB", "#0E8FA0")),
    ("React Native", "RN", ("#2E2F3E", "#121218")),
    ("React", "Re", ("#3A4B66", "#1B2333")),
    ("TypeScript", "ts", ("#7290FF", "#3557D9")),
    ("Kotlin", "Kt", ("#C77DFF", "#FF7A45")),
    ("Fastlane", "FL", ("#45D483", "#1E8E5A")),
    ("CodePush", "CP", ("#98A2B3", "#4B5563")),
]
DOCK = [
    ("EAS", "EAS", ("#2B2B33", "#000000")),
    ("CI/CD", "CI", ("#FFD60A", "#FF9F0A")),
    ("Mail", "env", ("#5AC8FA", "#0A84FF")),
    ("Web", "globe", ("#64D2FF", "#5E5CE6")),
]

ACCENT = "#FF2E8A"
DUR = 18.0  # one loop of the lock screen

THEMES = {
    "light": dict(card="#FFFFFF", border="#E5E5EA", fg="#000000", muted="#8A8A8E",
                  fill="#F2F2F7", blue="#007AFF", blue_bg="#007AFF1A", bar="#F7F7F9",
                  incoming="#E9E9EB", incoming_fg="#000000", chat_bg="#FFFFFF"),
    "dark": dict(card="#1C1C1E", border="#38383A", fg="#FFFFFF", muted="#98989F",
                 fill="#2C2C2E", blue="#0A84FF", blue_bg="#0A84FF26", bar="#1C1C1E",
                 incoming="#2C2C2E", incoming_fg="#FFFFFF", chat_bg="#000000"),
}


# ── helpers ──────────────────────────────────────────────────────────────────
def anim(attr, frames, extra="", dur=DUR):
    """frames: list of (seconds, value) across one loop of `dur` seconds."""
    times = ";".join(f"{f[0] / dur:.4f}" for f in frames)
    values = ";".join(str(f[1]) for f in frames)
    return (f'<animate attributeName="{attr}" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{times}" values="{values}" {extra}/>')


def ease(n):
    return f'calcMode="spline" keySplines="{";".join(["0.32 0 0.18 1"] * n)}"'


def transform(kind, frames, dur=DUR, spline=True):
    times = ";".join(f"{f[0] / dur:.4f}" for f in frames)
    values = ";".join(str(f[1]) for f in frames)
    extra = ease(len(frames) - 1) if spline else ""
    return (f'<animateTransform attributeName="transform" type="{kind}" dur="{dur}s" '
            f'repeatCount="indefinite" keyTimes="{times}" values="{values}" {extra}/>')


def fade(on_from, on_to, fade_in=0.3, fade_out=0.2, dur=DUR):
    return anim("opacity", [(0, 0), (on_from, 0), (on_from + fade_in, 1),
                            (on_to - fade_out, 1), (on_to, 0), (dur, 0)], dur=dur)


def text(x, y, s, size, weight=400, fill="#fff", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>'
            f"{escape(s)}</text>")


def gradient(gid, c1, c2, x2="1", y2="1"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


def icon(kind, x, y, size, grad_id):
    """App-icon squircle with a simple white glyph, or a monogram when kind is plain text."""
    s = size
    cx, cy = x + s / 2, y + s / 2
    sw = s * 0.055
    out = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * 0.225:.1f}" fill="url(#{grad_id})"/>',
           # soft top highlight, like an icon's glass
           f'<rect x="{x}" y="{y}" width="{s}" height="{s / 2:.1f}" rx="{s * 0.225:.1f}" fill="#fff" fill-opacity="0.08"/>']
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
                   'stroke-linecap="round" stroke-linejoin="round"/>')
        ax, ay = x + s * 0.8, y + s * 0.72
        out.append(f'<polyline points="{ax - s*0.2:.1f},{ay:.1f} {ax:.1f},{ay:.1f} {ax:.1f},{ay - s*0.2:.1f}" '
                   f'fill="none" stroke="#fff" stroke-width="{s*0.08:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "globe":
        rr = s * 0.3
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="#fff" stroke-width="{sw:.1f}"/>'
                   f'<ellipse cx="{cx}" cy="{cy}" rx="{rr*0.45:.1f}" ry="{rr:.1f}" fill="none" stroke="#fff" stroke-width="{sw:.1f}"/>'
                   f'<line x1="{cx-rr:.1f}" y1="{cy}" x2="{cx+rr:.1f}" y2="{cy}" stroke="#fff" stroke-width="{sw:.1f}"/>')
    elif kind == "env":
        w, h = s * 0.58, s * 0.42
        out.append(f'<rect x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{s*0.06:.1f}" fill="#fff"/>'
                   f'<polyline points="{cx-w/2+2:.1f},{cy-h/2+3:.1f} {cx:.1f},{cy+s*0.03:.1f} {cx+w/2-2:.1f},{cy-h/2+3:.1f}" '
                   f'fill="none" stroke="url(#{grad_id})" stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    elif kind == "spark":
        def star(px, py, r):
            return (f'<path d="M{px},{py-r:.1f} Q{px},{py} {px+r:.1f},{py} Q{px},{py} {px},{py+r:.1f} '
                    f'Q{px},{py} {px-r:.1f},{py} Q{px},{py} {px},{py-r:.1f} Z" fill="#fff"/>')
        out.append(star(cx - s * 0.04, cy + s * 0.04, s * 0.27) + star(cx + s * 0.2, cy - s * 0.2, s * 0.11))
    elif kind == "up":
        out.append(f'<polyline points="{cx-s*0.17:.1f},{cy-s*0.02:.1f} {cx},{cy-s*0.2:.1f} {cx+s*0.17:.1f},{cy-s*0.02:.1f}" '
                   f'fill="none" stroke="#fff" stroke-width="{s*0.09:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<line x1="{cx}" y1="{cy-s*0.18:.1f}" x2="{cx}" y2="{cy+s*0.22:.1f}" stroke="#fff" '
                   f'stroke-width="{s*0.09:.1f}" stroke-linecap="round"/>')
    elif kind == "og":
        out = [f'<circle cx="{cx}" cy="{cy}" r="{s/2}" fill="url(#{grad_id})"/>',
               text(cx, cy + s * 0.15, "OG", s * 0.4, 700, anchor="middle")]
    else:  # monogram
        size_ = s * (0.42 if len(kind) <= 2 else 0.32)
        out.append(text(cx, cy + size_ * 0.36, kind, size_, 700, anchor="middle", extra='letter-spacing="-0.5"'))
    return "".join(out)


def status_bar(W):
    out = [text(70, 50, "9:41", 18, 600)]
    bx = W - 128
    for i, h in enumerate((5, 8, 11, 14)):
        out.append(f'<rect x="{bx + i*6}" y="{46 - h}" width="4" height="{h}" rx="1.2" fill="#fff"/>')
    wx, wy = W - 88, 46
    out.append(f'<circle cx="{wx}" cy="{wy - 1}" r="2.2" fill="#fff"/>')
    for r in (8.5, 13):
        out.append(f'<path d="M{wx - r*0.75:.1f},{wy - r*0.66:.1f} A{r},{r} 0 0 1 {wx + r*0.75:.1f},{wy - r*0.66:.1f}" '
                   'fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>')
    out.append(f'<rect x="{W-68}" y="34" width="27" height="13" rx="4" fill="none" stroke="#fff" stroke-opacity="0.45" stroke-width="1.2"/>'
               f'<rect x="{W-65.5}" y="36.5" width="19" height="8" rx="2" fill="#fff"/>'
               f'<rect x="{W-39}" y="38.5" width="2" height="4" rx="1" fill="#fff" fill-opacity="0.45"/>')
    return "".join(out)


def wallpaper(W, H, blobs):
    defs = (gradient("wall", "#0B0614", "#140A26", "0", "1")
            + '<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="70"/></filter>'
            + f'<clipPath id="screen"><rect x="0" y="0" width="{W}" height="{H}" rx="44"/></clipPath>')
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.55">'
        f'<animateTransform attributeName="transform" type="translate" values="{v}" '
        f'dur="{d}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></circle>'
        for x, y, r, c, v, d in blobs)
    body = (f'<rect width="{W}" height="{H}" fill="url(#wall)"/><g filter="url(#blur)">{circles}</g>'
            f'<rect width="{W}" height="{H}" fill="#000" fill-opacity="0.12"/>')
    frame = (f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="43.5" fill="none" '
             'stroke="#fff" stroke-opacity="0.14" stroke-width="1.5"/>')
    return defs, body, frame


def svg_doc(W, H, label, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
            f'<defs>{defs}</defs>{body}</svg>\n')


def card_bg(W, H, t, rx=28):
    return (f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="{rx}" fill="{t["card"]}" '
            f'stroke="{t["border"]}" stroke-width="1.5"/>')


# ── 1. Lock Screen ───────────────────────────────────────────────────────────
def lock_screen():
    W, H = 900, 520
    CX = W / 2
    compact = (160, 46, 20)
    expanded = (600, 92, 16)

    frames = [(0, compact), (0.8, compact)]
    for start, hold_until in ((0.8, 5.0), (6.4, 10.8), (12.2, 16.8)):
        if start != 0.8:
            frames.append((start, compact))
        frames += [(start + 0.42, (expanded[0] + 18, expanded[1] + 4, expanded[2] - 1)),
                   (start + 0.62, expanded), (hold_until, expanded),
                   (hold_until + 0.38, (compact[0] - 10, compact[1] - 2, compact[2] + 1)),
                   (hold_until + 0.55, compact)]
    frames.append((DUR, compact))
    geo = {"x": [(t, round(CX - w / 2, 1)) for t, (w, h, y) in frames],
           "y": [(t, y) for t, (w, h, y) in frames],
           "width": [(t, w) for t, (w, h, y) in frames],
           "height": [(t, h) for t, (w, h, y) in frames],
           "rx": [(t, h / 2) for t, (w, h, y) in frames]}
    island_anims = "".join(anim(a, v, ease(len(v) - 1)) for a, v in geo.items())

    ex = CX - expanded[0] / 2
    mid = expanded[2] + expanded[1] / 2

    wall_defs, wall, frame = wallpaper(W, H, [
        (170, 110, 230, ACCENT, "0 0; 70 50; 0 0", 19),
        (740, 150, 250, "#6D5BFF", "0 0; -60 70; 0 0", 23),
        (520, 560, 220, "#FF8A3D", "0 0; -80 -40; 0 0", 17),
        (90, 470, 160, "#3A2BFF", "0 0; 50 -30; 0 0", 21)])
    defs = [wall_defs,
            gradient("nameFill", "#FFFFFF", "#FFD3E6", "0", "1"),
            gradient("gA", "#7B5CFF", ACCENT), gradient("gB", "#30D158", "#0A84FF"),
            gradient("gC", "#FF9F0A", ACCENT),
            # userSpaceOnUse: a bounding-box gradient on a zero-width line would not render
            f'<linearGradient id="wave" gradientUnits="userSpaceOnUse" x1="0" y1="{mid - 17}" x2="0" y2="{mid + 17}">'
            '<stop offset="0" stop-color="#FF7AC0"/><stop offset="1" stop-color="#7B5CFF"/></linearGradient>']
    defs += [gradient(f"n{i}", *n[3]) for i, n in enumerate(NOTIFICATIONS)]

    cam = [(0, 1), (0.8, 1), (0.95, 0)]
    for hold_until, nxt in ((5.0, 6.4), (10.8, 12.2), (16.8, None)):
        cam += [(hold_until + 0.5, 0), (hold_until + 0.7, 1)]
        if nxt:
            cam += [(nxt, 1), (nxt + 0.15, 0)]
    cam.append((DUR, 1))
    camera = (f'<g>{anim("opacity", cam)}<circle cx="{CX + 58}" cy="43" r="7" fill="#15151a"/>'
              f'<circle cx="{CX + 58}" cy="43" r="3" fill="#24243a"/></g>')

    def activity_text(title, sub):
        return (text(ex + 86, mid - 4, title, 18, 600) +
                text(ex + 86, mid + 20, sub, 14.5, 400, "#fff", extra='fill-opacity="0.62"'))

    bars = []
    for i, p in enumerate(["8;30;12;24;8", "14;10;32;12;14", "22;34;10;28;22", "10;24;30;8;10",
                           "26;12;20;34;26", "12;30;14;22;12", "8;18;28;10;8"]):
        x = ex + 500 + i * 11
        hs = [float(v) for v in p.split(";")]
        y1 = ";".join(f"{mid - h/2:.1f}" for h in hs)
        y2 = ";".join(f"{mid + h/2:.1f}" for h in hs)
        bars.append(f'<line x1="{x}" x2="{x}" y1="{mid-4}" y2="{mid+4}" stroke="url(#wave)" stroke-width="5" stroke-linecap="round">'
                    f'<animate attributeName="y1" values="{y1}" dur="1.1s" begin="-{i*0.13:.2f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y2" values="{y2}" dur="1.1s" begin="-{i*0.13:.2f}s" repeatCount="indefinite"/></line>')
    act_a = (f'<g opacity="0">{fade(1.25, 4.95)}' + icon("cmd", ex + 26, mid - 24, 48, "gA")
             + activity_text(*ISLAND["a"]) + "".join(bars) + "</g>")

    circ = 2 * 3.14159 * 17
    rcx = ex + 548
    act_b = (f'<g opacity="0">{fade(6.85, 10.75)}' + icon("up", ex + 26, mid - 24, 48, "gB")
             + activity_text(*ISLAND["b"])
             + f'<circle cx="{rcx}" cy="{mid}" r="17" fill="none" stroke="#fff" stroke-opacity="0.14" stroke-width="5"/>'
             + f'<circle cx="{rcx}" cy="{mid}" r="17" fill="none" stroke="#30D158" stroke-width="5" stroke-linecap="round" '
               f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ:.2f}" transform="rotate(-90 {rcx} {mid})">'
             + anim("stroke-dashoffset", [(0, circ), (7.1, circ), (9.6, 0), (10.8, 0), (10.9, circ), (DUR, circ)]) + "</circle>"
             + f'<polyline points="{rcx-7},{mid} {rcx-2},{mid+5} {rcx+8},{mid-6}" fill="none" stroke="#30D158" '
               'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
             + anim("opacity", [(0, 0), (9.6, 0), (9.85, 1), (10.6, 1), (10.75, 0), (DUR, 0)]) + "</polyline></g>")

    dcx = ex + 552
    act_c = (f'<g opacity="0">{fade(12.65, 16.75)}' + icon("og", ex + 26, mid - 24, 48, "gC")
             + activity_text(*ISLAND["c"])
             + f'<circle cx="{dcx}" cy="{mid}" r="7" fill="none" stroke="#30D158" stroke-width="2">'
               '<animate attributeName="r" values="7;20" dur="1.6s" repeatCount="indefinite"/>'
               '<animate attributeName="opacity" values="0.8;0" dur="1.6s" repeatCount="indefinite"/></circle>'
             + f'<circle cx="{dcx}" cy="{mid}" r="7" fill="#30D158"/></g>')

    lock = [text(CX, 176, ROLE, 22, 600, "#fff", "middle", 'fill-opacity="0.9" letter-spacing="0.2"'),
            text(CX, 286, NAME, 118, 700, "url(#nameFill)", "middle", 'letter-spacing="-3"')]
    widths = [len(w) * 8.4 + 40 for w in WIDGET_PILLS]
    x = CX - (sum(widths) + 12 * (len(widths) - 1)) / 2
    for w, label in zip(widths, WIDGET_PILLS):
        lock.append(f'<rect x="{x:.1f}" y="312" width="{w:.1f}" height="34" rx="17" fill="#fff" fill-opacity="0.13" '
                    'stroke="#fff" stroke-opacity="0.12"/>'
                    + text(round(x + w / 2, 1), 334, label, 15, 500, "#fff", "middle", 'fill-opacity="0.92"'))
        x += w + 12

    nx, ny, nw, nh = CX - 300, 376, 600, 70
    notes = [f'<rect x="{nx + 22}" y="{ny + 14}" width="{nw - 44}" height="{nh}" rx="20" fill="#fff" fill-opacity="0.07">'
             + anim("opacity", [(0, 0), (0.9, 0), (1.2, 1), (17.7, 1), (18.0, 0)]) + "</rect>"]
    for i, ((app, body, kind, _), (t_in, t_out)) in enumerate(zip(NOTIFICATIONS, [(0.6, 5.9), (6.2, 11.9), (12.2, 17.7)])):
        move = [(0, "0 34"), (t_in, "0 34"), (t_in + 0.45, "0 0"), (t_out, "0 0"), (t_out + 0.3, "0 -16"), (DUR, "0 -16")]
        # the first notification is visible in renderers that don't animate (e.g. some mobile apps)
        notes.append(f'<g opacity="{1 if i == 0 else 0}">{fade(t_in, t_out + 0.3, 0.4, 0.3)}{transform("translate", move)}'
                     f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="20" fill="#fff" fill-opacity="0.16" '
                     'stroke="#fff" stroke-opacity="0.1"/>'
                     + icon(kind, nx + 16, ny + 15, 40, f"n{i}")
                     + text(nx + 70, ny + 29, app, 12, 600, "#fff", extra='fill-opacity="0.6" letter-spacing="0.6"')
                     + text(nx + nw - 18, ny + 29, "now", 12, 400, "#fff", "end", 'fill-opacity="0.5"')
                     + text(nx + 70, ny + 52, body, 15.5, 500) + "</g>")

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

    body = (f'<g clip-path="url(#screen)">{wall}{status_bar(W)}{"".join(lock)}{"".join(notes)}'
            f'{"".join(buttons)}{home}{island}{camera}{act_a}{act_b}{act_c}</g>{frame}')
    return svg_doc(W, H, f"{NAME} · {ROLE}", "".join(defs), body)


# ── 2. iMessage ──────────────────────────────────────────────────────────────
def imessage(t):
    W = 900
    LOOP = 20.0
    appear = [0.6, 2.4, 3.2, 4.6, 6.4, 8.0, 9.8]
    typing = {1: (1.1, 2.4), 4: (5.1, 6.4), 6: (8.5, 9.8)}
    out_at = 18.6

    body, y = [], 118
    rows = []
    for i, (who, lines) in enumerate(CHAT):
        if i:
            y += 4 if CHAT[i - 1][0] == who else 14
        h = 17 + 21 * len(lines)
        w = max(len(l) for l in lines) * 8.1 + 30
        x = W - 24 - w if who == "me" else 24
        last = i == len(CHAT) - 1 or CHAT[i + 1][0] != who
        rows.append((who, lines, x, y, w, h, last))
        y += h
    H = int(y + 34)

    # header
    body.append(f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{t["chat_bg"]}"/>'
                f'<rect width="{W}" height="78" fill="{t["bar"]}"/>'
                f'<rect y="78" width="{W}" height="1" fill="{t["border"]}"/></g>')
    body.append(f'<polyline points="34,28 24,39 34,50" fill="none" stroke="{t["blue"]}" stroke-width="3.2" '
                'stroke-linecap="round" stroke-linejoin="round"/>')
    body.append(icon("og", W / 2 - 20, 12, 40, "av"))
    body.append(text(W / 2, 68, "Om Gandhi ›", 12.5, 500, t["fg"], "middle"))
    body.append(f'<rect x="{W-62}" y="31" width="22" height="16" rx="4" fill="none" stroke="{t["blue"]}" stroke-width="2.4"/>'
                f'<path d="M{W-38},36 l9,-5 v16 l-9,-5 z" fill="{t["blue"]}"/>')
    body.append(text(W / 2, 104, "iMessage · Today 9:41", 12, 500, t["muted"], "middle"))

    for i, (who, lines, x, y, w, h, last) in enumerate(rows):
        a = appear[i]
        color = t["blue"] if who == "me" else t["incoming"]
        fg = "#FFFFFF" if who == "me" else t["incoming_fg"]
        shape = f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="19" fill="{color}"/>'
        if last:  # the little tail on the last bubble of a group
            if who == "me":
                r, b = x + w, y + h
                shape += (f'<path d="M{r-16:.1f},{b-14} C{r-14:.1f},{b-3} {r-6:.1f},{b} {r+5:.1f},{b} '
                          f'C{r-1:.1f},{b-3} {r-2:.1f},{b-8} {r-2:.1f},{b-14} Z" fill="{color}"/>')
            else:
                l, b = x, y + h
                shape += (f'<path d="M{l+16:.1f},{b-14} C{l+14:.1f},{b-3} {l+6:.1f},{b} {l-5:.1f},{b} '
                          f'C{l+1:.1f},{b-3} {l+2:.1f},{b-8} {l+2:.1f},{b-14} Z" fill="{color}"/>')
        words = "".join(text(round(x + 15, 1), y + 25 + 21 * k, line, 16, 400, fg) for k, line in enumerate(lines))
        # base opacity 1, so renderers without animation still show the whole chat
        body.append(f'<g>{anim("opacity", [(0, 0), (a, 0), (a + 0.25, 1), (out_at, 1), (out_at + 0.5, 0), (LOOP, 0)], dur=LOOP)}'
                    f'{transform("translate", [(0, "0 10"), (a, "0 10"), (a + 0.35, "0 0"), (LOOP, "0 0")], dur=LOOP)}'
                    f'{shape}{words}</g>')
        if i in typing:
            s, e = typing[i]
            dots = "".join(
                f'<circle cx="{24 + 20 + k * 12}" cy="{y + 19}" r="4" fill="{t["muted"]}">'
                f'<animate attributeName="opacity" values="0.35;1;0.35" dur="1.2s" begin="{k * 0.2}s" repeatCount="indefinite"/></circle>'
                for k in range(3))
            body.append(f'<g opacity="0">{anim("opacity", [(0, 0), (s, 0), (s + 0.2, 1), (e - 0.1, 1), (e, 0), (LOOP, 0)], dur=LOOP)}'
                        f'<rect x="24" y="{y}" width="64" height="38" rx="19" fill="{t["incoming"]}"/>{dots}</g>')

    defs = (gradient("av", "#FF9F0A", ACCENT)
            + f'<clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="28"/></clipPath>')
    edge = (f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="28" fill="none" '
            f'stroke="{t["border"]}" stroke-width="1.5"/>')
    return svg_doc(W, H, "iMessage chat with Om Gandhi", defs, "".join(body) + edge)


# ── 3. App Store rows ────────────────────────────────────────────────────────
def app_row(name, sub, details, kind, grad, t):
    W, H = 900, 116
    body = [card_bg(W, H, t, 24),
            icon(kind, 20, 20, 76, "g"),
            text(116, 48, name, 20, 600, t["fg"]),
            text(116, 72, sub, 15, 400, t["muted"]),
            text(116, 95, details, 13, 500, t["muted"], extra='fill-opacity="0.85"'),
            f'<rect x="{W-110}" y="42" width="86" height="32" rx="16" fill="{t["blue_bg"]}"/>',
            text(W - 67, 63, "VIEW", 14, 700, t["blue"], "middle", 'letter-spacing="0.3"')]
    return svg_doc(W, H, f"{name}: {sub}", gradient("g", *grad), "".join(body))


# ── 4. Home Screen ───────────────────────────────────────────────────────────
def home_screen():
    W, H = 900, 548
    LOOP = 14.0
    wall_defs, wall, frame = wallpaper(W, H, [
        (730, 120, 240, ACCENT, "0 0; -60 50; 0 0", 21),
        (150, 180, 250, "#6D5BFF", "0 0; 60 60; 0 0", 19),
        (430, 580, 240, "#FF8A3D", "0 0; 70 -40; 0 0", 23),
        (880, 470, 180, "#3A2BFF", "0 0; -40 -30; 0 0", 17)])
    defs = [wall_defs]
    body = [wall, status_bar(W)]

    # widgets, 2 x 2 on the left
    ww, wh, gap, wx0, wy0 = 182, 148, 16, 48, 84
    for i, (label, big, caption, deco) in enumerate(WIDGETS):
        x = wx0 + (i % 2) * (ww + gap)
        y = wy0 + (i // 2) * (wh + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{wh}" rx="26" fill="#fff" fill-opacity="0.15" '
                    'stroke="#fff" stroke-opacity="0.12"/>')
        body.append(text(x + 16, y + 28, label, 10.5, 700, "#fff", extra='fill-opacity="0.62" letter-spacing="0.7"'))
        body.append(text(x + 15, y + 74, big, 36, 700, "#fff", extra='letter-spacing="-1"'))
        body.append(text(x + 16, y + 97, caption, 12.5, 500, "#fff", extra='fill-opacity="0.78"'))
        if deco == "spark":
            pts = [(0, 6), (18, 4), (34, 12), (52, 10), (70, 22), (92, 20), (112, 30), (132, 32), (150, 36)]
            d = " ".join(f"{x + 16 + a},{y + 108 + b * 0.75:.1f}" for a, b in pts)
            body.append(f'<polyline points="{d}" fill="none" stroke="#30D158" stroke-width="3" stroke-linecap="round" '
                        'stroke-linejoin="round" stroke-dasharray="190" stroke-dashoffset="0">'
                        '<animate attributeName="stroke-dashoffset" values="190;0;0;190" keyTimes="0;0.3;0.9;1" '
                        'dur="6s" repeatCount="indefinite"/></polyline>')
        elif deco == "bars":
            for k in range(8):
                bx = x + 16 + k * 19
                body.append(f'<rect x="{bx}" y="{y + 114}" width="11" height="18" rx="3" fill="#30D158" fill-opacity="{0.55 + k * 0.06:.2f}">'
                            f'<animate attributeName="height" values="0;18;18;0" keyTimes="0;0.25;0.9;1" dur="6s" begin="{k * 0.12:.2f}s" repeatCount="indefinite"/>'
                            f'<animate attributeName="y" values="{y+132};{y+114};{y+114};{y+132}" keyTimes="0;0.25;0.9;1" dur="6s" begin="{k * 0.12:.2f}s" repeatCount="indefinite"/></rect>')

    # app grid, 4 x 3 on the right, with an occasional jiggle-mode wiggle
    def jiggle(cx, cy, phase):
        frames, t, sign = [(0, f"0 {cx} {cy}"), (10.4, f"0 {cx} {cy}")], 10.4, phase
        while t < 12.4:
            t = round(t + 0.13, 2)
            frames.append((t, f"{1.8 * sign} {cx} {cy}"))
            sign *= -1
        frames += [(12.6, f"0 {cx} {cy}"), (LOOP, f"0 {cx} {cy}")]
        return transform("rotate", frames, dur=LOOP, spline=False)

    isz, pitch_x, pitch_y, gx0, gy0 = 64, 98, 110, 452, 84
    for i, (label, glyph, grad) in enumerate(STACK):
        col, row = i % 4, i // 4
        x = gx0 + col * pitch_x + (pitch_x - isz) / 2
        y = gy0 + row * pitch_y
        gid = f"s{i}"
        defs.append(gradient(gid, *grad))
        body.append(f'<g>{jiggle(x + isz / 2, y + isz / 2, 1 if i % 2 else -1)}'
                    + icon(glyph, x, y, isz, gid)
                    + text(round(x + isz / 2, 1), y + isz + 18, label, 12, 500, "#fff", "middle")
                    + "</g>")

    # dock
    dsz, dgap, dpad = 60, 22, 18
    dw = len(DOCK) * dsz + (len(DOCK) - 1) * dgap + dpad * 2
    dx, dy = (W - dw) / 2, 436
    body.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dsz + dpad * 2 - 4}" rx="32" fill="#fff" '
                'fill-opacity="0.16" stroke="#fff" stroke-opacity="0.12"/>')
    for i, (label, glyph, grad) in enumerate(DOCK):
        gid = f"d{i}"
        defs.append(gradient(gid, *grad))
        x = dx + dpad + i * (dsz + dgap)
        body.append(f'<g>{jiggle(x + dsz / 2, dy + dpad - 2 + dsz / 2, -1 if i % 2 else 1)}'
                    + icon(glyph, x, dy + dpad - 2, dsz, gid) + "</g>")
    body.append(f'<rect x="{W / 2 - 70}" y="{H - 17}" width="140" height="5" rx="2.5" fill="#fff" fill-opacity="0.85"/>')

    return svg_doc(W, H, "Home Screen: stats widgets and my stack as apps", "".join(defs),
                   f'<g clip-path="url(#screen)">{"".join(body)}</g>{frame}')


# ── 5. Contacts ──────────────────────────────────────────────────────────────
def contact_card(t):
    W, H = 900, 236
    body = [card_bg(W, H, t),
            icon("og", W / 2 - 46, 26, 92, "av"),
            text(W / 2, 154, NAME, 30, 700, t["fg"], "middle", 'letter-spacing="-0.4"'),
            text(W / 2, 182, ROLE, 15.5, 500, t["muted"], "middle"),
            text(W / 2, 206, LOCATION, 13.5, 400, t["muted"], "middle", 'fill-opacity="0.85"')]
    return svg_doc(W, H, f"Contact card: {NAME}, {ROLE}", gradient("av", "#FF9F0A", ACCENT), "".join(body))


def action_button(kind, label, t):
    W, H = 210, 88
    cx = W / 2
    if kind == "mail":
        glyph = (f'<rect x="{cx-15}" y="20" width="30" height="22" rx="4" fill="{t["blue"]}"/>'
                 f'<polyline points="{cx-13},22 {cx},33 {cx+13},22" fill="none" stroke="{t["card"]}" stroke-width="2.2" stroke-linejoin="round"/>')
    else:
        glyph = (f'<circle cx="{cx}" cy="31" r="13" fill="none" stroke="{t["blue"]}" stroke-width="2.6"/>'
                 f'<ellipse cx="{cx}" cy="31" rx="6" ry="13" fill="none" stroke="{t["blue"]}" stroke-width="2.2"/>'
                 f'<line x1="{cx-13}" y1="31" x2="{cx+13}" y2="31" stroke="{t["blue"]}" stroke-width="2.2"/>')
    body = card_bg(W, H, t, 20) + glyph + text(cx, 68, label, 14, 500, t["blue"], "middle")
    return svg_doc(W, H, label, "", body)


def main():
    old = list(OUT.glob("*.svg"))
    for p in old:
        p.unlink()
    (OUT / "lock-screen.svg").write_text(lock_screen())
    (OUT / "home-screen.svg").write_text(home_screen())
    for mode, t in THEMES.items():
        (OUT / f"imessage-{mode}.svg").write_text(imessage(t))
        for stem, name, sub, details, kind, grad in APPS:
            (OUT / f"app-{stem}-{mode}.svg").write_text(app_row(name, sub, details, kind, grad, t))
        (OUT / f"contact-{mode}.svg").write_text(contact_card(t))
        (OUT / f"button-mail-{mode}.svg").write_text(action_button("mail", "mail", t))
        (OUT / f"button-web-{mode}.svg").write_text(action_button("web", "website", t))
    print("wrote", len(list(OUT.glob("*.svg"))), "files")


if __name__ == "__main__":
    main()
