import math

ICONS = {}

EXTRA_ICONS = {
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "stamp": '<circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.2l2.6 2.6 5-5.4"/>',
    "gauge": '<path d="M4.5 16a7.5 7.5 0 1 1 15 0"/><path d="M12 16l3.5-4.5"/>',
    "wave": '<path d="M3 12h1.5M6.5 8v8M10 5v14M13.5 9v6M17 7v10M20.5 11v2"/>',
    "slides": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M7 20l5-4 5 4M7 8h6M7 11h9"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.5v.6M12 16.8v.2"/>',
    "marker": '<path d="M15 4l5 5-8.5 8.5H7v-4.5z"/><path d="M4 20.5h8"/>',
    "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "box": '<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5L12 12l8.5-4.5M12 12v9"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"/>',
    "tag": '<path d="M3.5 12.5V4h8.5l8.5 8.5-8 8z"/><circle cx="8" cy="8.5" r="1.4"/>',
    "scissors": '<circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8.2 8.3L20 18M8.2 15.7L20 6"/>',
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    "columns": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M12 4v16M6 9h3M15 9h3M6 13h3M15 13h3"/>',
    "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/><path d="M11.5 13.5L20 4"/>',
    "bolt": '<path d="M13 3L5 13.5h6L10 21l9-11h-6z"/>',
    "node": '<circle cx="12" cy="12" r="3"/><circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><path d="M7 7l3 3M17 7l-3 3M7 17l3-3M17 17l-3-3"/>',
    "pyramid": '<path d="M3 5h18l-9 15z"/><path d="M6 10h12M9 15h6"/>',
    "code": '<path d="M8.5 7L3.5 12l5 5M15.5 7l5 5-5 5M13.5 4.5l-3 15"/>',
    "map": '<path d="M3.5 6.5l5.5-2 6 2 5.5-2v13l-5.5 2-6-2-5.5 2z"/><path d="M9 4.5v13M15 6.5v13"/>',
    "inbox": '<path d="M3.5 13.5l2.5-8h12l2.5 8v5h-17z"/><path d="M3.5 13.5H9a3 3 0 0 0 6 0h5.5"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
}

EXAMPLE = {"en": "Example", "fr": "Exemple", "ar": "مثال"}
DEMO = {"en": "Demo data", "fr": "Données de démo", "ar": "بيانات تجريبية"}
ILLUSTRATIVE = {"en": "Illustrative", "fr": "Illustratif", "ar": "توضيحي"}
SAMPLE = {"en": "Sample", "fr": "Exemple", "ar": "نموذج"}
BRAND = "yourbrand.com"
ENGINES = ["ChatGPT", "Perplexity", "Gemini", "Google AI Overviews", "Claude"]

_state = {"prefix": "v", "n": 0}


def reset(prefix):
    _state["prefix"] = prefix
    _state["n"] = 0


def uid():
    _state["n"] += 1
    return f'{_state["prefix"]}-{_state["n"]}'


def T(lang, en, fr, ar):
    return {"en": en, "fr": fr, "ar": ar}[lang]


def icon(name, cls=""):
    path = EXTRA_ICONS.get(name) or ICONS.get(name, "")
    c = f' class="{cls}"' if cls else ""
    return f'<svg viewBox="0 0 24 24"{c} fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{path}</svg>'


def label(text, kind="example"):
    return f'<span class="vx-label vx-label-{kind}">{text}</span>'


def node(ic, title, sub="", cls=""):
    s = f"<small>{sub}</small>" if sub else ""
    return f'<div class="vx-node {cls}"><span class="vx-node-ring">{icon(ic)}</span><span class="vx-node-t"><b>{title}</b>{s}</span></div>'


def beam(cls=""):
    return f'<span class="vx-beam {cls}" aria-hidden="true"><i></i></span>'


def tile(ic, title, sub="", cls="", i=0, lines=2):
    s = f"<small>{sub}</small>" if sub else ""
    sk = "".join(f'<i style="--w:{w}%"></i>' for w in [88, 64, 76][:lines])
    return f'<div class="vx-tile {cls}" style="--i:{i}"><span class="vx-tile-ic">{icon(ic)}</span><span class="vx-tile-t"><b>{title}</b>{s}</span><span class="vx-sk">{sk}</span></div>'


def cite(text=BRAND, cls=""):
    return f'<span class="vx-cite {cls}">{icon("link")}<span dir="ltr">{text}</span></span>'


def chip(name, cls=""):
    return f'<span class="vx-chip {cls}" dir="ltr">{name}</span>'


def stamp(text, cls=""):
    return f'<span class="vx-stamp {cls}"><span>{icon("check")}{text}</span></span>'


def answer(question, lines, sources, engine="", tag="", cls="", typed=False):
    head = f'<div class="vx-ans-h">{chip(engine) if engine else ""}{tag}</div>'
    q = f'<p class="vx-ans-q">{icon("search")}<span>{question}</span></p>' if question else ""
    body = ""
    for ln in lines:
        if isinstance(ln, (int, float)):
            body += f'<i class="vx-line" style="--w:{ln}%"></i>'
        else:
            body += f'<p class="vx-ans-p">{ln}</p>'
    srcs = "".join(cite(s, "is-hl") if hl else f'<span class="vx-src" dir="ltr">{s}</span>' for s, hl in sources)
    typer = " data-typer" if typed else ""
    return f'<div class="vx-answer {cls}"{typer}>{head}{q}<div class="vx-ans-b">{body}</div><div class="vx-ans-s">{srcs}</div></div>'


def wipe_mask(mid, cls="vx-wipe"):
    return f'<mask id="{mid}" maskUnits="userSpaceOnUse"><rect class="{cls}" x="-5%" y="-5%" width="110%" height="110%" fill="#fff"/></mask>'


def gauge(value, maximum, caption="", size=160, cls="", unit=""):
    r = size * 0.4
    cx = cy = size / 2
    frac = max(0.0, min(1.0, value / maximum)) if maximum else 0
    a0, a1 = math.pi * 0.75, math.pi * 2.25
    def pt(a):
        return cx + r * math.cos(a), cy + r * math.sin(a)
    x0, y0 = pt(a0)
    x1, y1 = pt(a1)
    track = f"M{x0:.1f} {y0:.1f} A{r:.1f} {r:.1f} 0 1 1 {x1:.1f} {y1:.1f}"
    ticks = "".join(
        f'<line x1="{cx + (r - 9) * math.cos(a0 + (a1 - a0) * k / 10):.1f}" y1="{cy + (r - 9) * math.sin(a0 + (a1 - a0) * k / 10):.1f}" x2="{cx + (r - 4) * math.cos(a0 + (a1 - a0) * k / 10):.1f}" y2="{cy + (r - 4) * math.sin(a0 + (a1 - a0) * k / 10):.1f}" class="vg-tick"/>'
        for k in range(11)
    )
    deg = -135 + 270 * frac
    shown = f"{value:g}{unit}"
    return (
        f'<div class="vx-gauge {cls}" style="--deg:{deg:.1f}deg"><svg viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
        f'<path d="{track}" class="vg-track"/>{ticks}'
        f'<g class="vg-needle" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy - r + 14} L{cx - 4} {cy} L{cx + 4} {cy}z"/></g><circle cx="{cx}" cy="{cy}" r="7" class="vg-hub"/></svg>'
        f'<span class="vg-val">{shown}</span>{f"<span class=vg-cap>{caption}</span>" if caption else ""}</div>'
    )


def bars(rows, maximum=None, cls="", unit=""):
    m = maximum or max(v for _, v, *_ in rows) or 1
    out = []
    for i, row in enumerate(rows):
        name, v = row[0], row[1]
        hl = len(row) > 2 and row[2]
        txt = row[3] if len(row) > 3 else f"{v:g}{unit}"
        out.append(
            f'<div class="vb-row{" is-hl" if hl else ""}" style="--i:{i}"><span class="vb-k">{name}</span>'
            f'<span class="vb-track"><i style="--s:{v / m:.3f}"></i></span><span class="vb-v">{txt}</span></div>'
        )
    return f'<div class="vx-bars {cls}">{"".join(out)}</div>'


def donut(parts, size=140, cls="", center=""):
    total = sum(v for _, v, _ in parts) or 1
    r, c = size * 0.36, size / 2
    circ = 2 * math.pi * r
    acc = 0.0
    segs = []
    for name, v, tone in parts:
        frac = v / total
        segs.append(
            f'<circle cx="{c}" cy="{c}" r="{r:.1f}" class="vd-seg vd-{tone}" stroke-dasharray="{max(frac * circ - 2, 0.5):.1f} {circ:.1f}" '
            f'transform="rotate({-90 + acc * 360:.1f} {c} {c})"/>'
        )
        acc += frac
    legend = "".join(f'<li><i class="vd-{tone}"></i>{name}<b>{v:g}</b></li>' for name, v, tone in parts)
    mid = f'<span class="vd-mid">{center}</span>' if center else ""
    return (
        f'<div class="vx-donut {cls}"><div class="vd-ring"><svg viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false">'
        f'<circle cx="{c}" cy="{c}" r="{r:.1f}" class="vd-track"/>{"".join(segs)}</svg>{mid}</div><ul class="vd-legend">{legend}</ul></div>'
    )


def spark(values, w=120, h=36, cls=""):
    m, n = max(values) or 1, len(values)
    pts = " ".join(f"{i * w / (n - 1):.1f},{h - 3 - v / m * (h - 8):.1f}" for i, v in enumerate(values))
    mid = uid()
    return (
        f'<svg class="vx-spark {cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{wipe_mask(mid)}</defs>'
        f'<polyline points="{pts}" mask="url(#{mid})"/></svg>'
    )


def frame(inner, kind="browser", url="", cls=""):
    if kind == "phone":
        return f'<div class="vx-phone {cls}"><span class="vx-phone-notch"></span><div class="vx-phone-screen">{inner}</div></div>'
    return (
        f'<div class="vx-browser {cls}"><div class="vx-browser-bar"><span class="vx-dots"><i></i><i></i><i></i></span>'
        f'<span class="vx-url" dir="ltr">{icon("lock")}{url}</span></div><div class="vx-browser-body">{inner}</div></div>'
    )
