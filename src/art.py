import hashlib
import math
import random

SPRITE = (
    '<svg class="sprite" aria-hidden="true" focusable="false"><defs>'
    '<symbol id="m-source" viewBox="0 0 48 48"><circle cx="24" cy="24" r="21" class="m-ring"/><circle cx="24" cy="24" r="13" class="m-core"/><circle cx="24" cy="24" r="4.5" class="m-dot"/></symbol>'
    '<symbol id="m-card" viewBox="0 0 64 48"><rect x="1" y="1" width="62" height="46" rx="9" class="m-card"/><rect x="10" y="12" width="30" height="5" rx="2.5" class="m-ink"/><rect x="10" y="22" width="44" height="4" rx="2" class="m-faint"/><rect x="10" y="31" width="36" height="4" rx="2" class="m-faint"/></symbol>'
    '<symbol id="m-cite" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" class="m-cite"/><path d="M13 23.5c0-4 2-7 5.5-8.5M22 23.5c0-4 2-7 5.5-8.5" class="m-cite-ink"/><circle cx="15" cy="25" r="2.6" class="m-dot"/><circle cx="24" cy="25" r="2.6" class="m-dot"/></symbol>'
    '<symbol id="m-answer" viewBox="0 0 96 64"><path d="M8 2h80a6 6 0 0 1 6 6v36a6 6 0 0 1-6 6H34l-12 12V50H8a6 6 0 0 1-6-6V8a6 6 0 0 1 6-6z" class="m-card"/><rect x="14" y="14" width="64" height="5" rx="2.5" class="m-faint"/><rect x="14" y="25" width="54" height="5" rx="2.5" class="m-faint"/><rect x="14" y="36" width="30" height="7" rx="3.5" class="m-acc"/></symbol>'
    '</defs></svg>'
)

ICON_PATHS = {}


def _use(sym, x, y, w, h, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<use href="#{sym}" x="{x}" y="{y}" width="{w}" height="{h}"{c}/>'


def _glyph(name, cx, cy, size=22):
    s = size / 24
    return f'<g class="m-glyph" transform="translate({cx - size / 2} {cy - size / 2}) scale({s:.3f})">{ICON_PATHS.get(name, "")}</g>'


def _wire(d, delay=0):
    return f'<path class="m-wire" d="{d}"/><path class="m-flow" style="animation-delay:{delay}s" d="{d}"/>'


EXTRAS = {
    "creators": '<g class="m-extra"><path d="M118 132a26 26 0 0 1 0 36M128 122a40 40 0 0 1 0 56" class="m-arc"/></g>',
    "from-podcast": '<g class="m-extra">' + "".join(f'<rect x="{30 + i * 9}" y="{150 + (i % 3) * 6 - 14}" width="5" height="{28 - (i % 3) * 12}" rx="2.5" class="m-faint"/>' for i in range(7)) + "</g>",
    "from-webinar": '<g class="m-extra"><rect x="30" y="226" width="64" height="26" rx="13" class="m-card"/><rect x="40" y="236" width="36" height="5" rx="2.5" class="m-faint"/><rect x="58" y="262" width="56" height="24" rx="12" class="m-card"/><rect x="68" y="271" width="30" height="5" rx="2.5" class="m-faint"/></g>',
    "from-youtube": '<g class="m-extra"><rect x="22" y="96" width="120" height="8" rx="4" class="m-faint"/><rect x="22" y="204" width="80" height="8" rx="4" class="m-faint"/></g>',
    "ecommerce": '<g class="m-extra"><rect x="200" y="22" width="80" height="22" rx="11" class="m-acc-soft"/><rect x="212" y="30" width="40" height="6" rx="3" class="m-ink"/></g>',
    "b2b": '<g class="m-extra"><rect x="196" y="20" width="88" height="26" rx="8" class="m-card"/><path d="M196 33h88M226 20v26M256 20v26" class="m-grid"/></g>',
}

GLYPH = {
    "generic": "spark", "b2b": "building", "creators": "mic", "ecommerce": "cart",
    "from-blog": "doc", "from-youtube": "play", "from-podcast": "mic", "from-webinar": "screen",
}


def hero_art(kind):
    g = GLYPH.get(kind, "spark")
    parts = [
        _wire("M110 150 C 160 150, 170 70, 230 70", 0),
        _wire("M110 150 C 170 150, 170 150, 230 150", 0.4),
        _wire("M110 150 C 160 150, 170 230, 230 230", 0.8),
        _wire("M294 70 C 340 70, 330 150, 372 150", 1.3),
        _wire("M294 150 C 330 150, 340 150, 372 150", 1.5),
        _wire("M294 230 C 340 230, 330 150, 372 150", 1.7),
        EXTRAS.get(kind, ""),
        f'<g class="m-float">{_use("m-source", 54, 94, 112, 112)}{_glyph(g, 110, 150, 30)}</g>',
        f'<g class="m-float m-f2">{_use("m-card", 230, 46, 64, 48)}</g>',
        f'<g class="m-float m-f3">{_use("m-card", 230, 126, 64, 48, "m-hl")}</g>',
        f'<g class="m-float m-f2">{_use("m-card", 230, 206, 64, 48)}</g>',
        f'<g class="m-float m-f3">{_use("m-answer", 372, 116, 96, 64)}</g>',
        f'<g class="m-pulse">{_use("m-cite", 432, 92, 34, 34)}</g>',
    ]
    return f'<svg class="m-art" viewBox="0 0 480 300" aria-hidden="true" focusable="false">{"".join(parts)}</svg>'


def _rng(seed):
    return random.Random(int(hashlib.sha1(seed.encode()).hexdigest()[:8], 16))


def _icon_path(name):
    if name in ICON_PATHS:
        return ICON_PATHS[name]
    from visuals.kit import EXTRA_ICONS
    return EXTRA_ICONS.get(name, "")


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _rect(x, y, w, h, rx, cls, extra=""):
    return f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(rx)}" class="{cls}"{extra}/>'


def _circ(cx, cy, r, cls, extra=""):
    return f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" class="{cls}"{extra}/>'


def _path(d, cls, extra=""):
    return f'<path d="{d}" class="{cls}"{extra}/>'


def _g(inner, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f"<g{c}{extra}>{inner}</g>"


def _glyph(name, cx, cy, size=22, cls="m-glyph", keep=False):
    s = size / 24
    inner = _icon_path(name)
    if keep:
        inner = f'<g class="blog-c-keep">{inner}</g>'
    return f'<g class="{cls}" transform="translate({_f(cx - size / 2)} {_f(cy - size / 2)}) scale({s:.3f})">{inner}</g>'


def _sk(x, y, widths, gap=9, h=4.5, first_ink=False):
    out = []
    for i, w in enumerate(widths):
        cls = "m-ink" if first_ink and i == 0 else "m-faint"
        out.append(_rect(x, y + i * gap, w, h if not (first_ink and i == 0) else h + 1, (h + 1) / 2, cls))
    return "".join(out)


def _card(x, y, w, h, widths=(0.6, 0.85, 0.7), hl=False, ic=None, cls="", rx=10):
    base = _rect(x, y, w, h, rx, "blog-c-card blog-c-hl" if hl else "blog-c-card")
    pad = 12
    inner = ""
    tx = x + pad
    if ic:
        inner += _rect(x + pad, y + pad, 22, 22, 7, "blog-c-icb" if hl else "blog-c-ic")
        inner += _glyph(ic, x + pad + 11, y + pad + 11, 14, "blog-c-icg" if hl else "m-glyph", True)
        tx = x + pad + 30
    iw = x + w - pad - tx
    rows = [iw * f for f in widths]
    gap = 9
    ty = y + pad + (4 if ic else 2)
    inner += _sk(tx, ty, rows[:1], gap, 5, True)
    rest = rows[1:]
    if ic and h > 50:
        inner += _sk(x + pad, y + pad + 32, [(w - 2 * pad) * f for f in widths[1:]], gap)
    else:
        inner += _sk(tx, ty + 12, rest, gap)
    return _g(base + inner, cls)


def _cite(cx, cy, r=17, cls="blog-c-pu"):
    s = r / 18
    return _g(
        _circ(cx, cy, r, "m-cite")
        + f'<g transform="translate({_f(cx - 20 * s)} {_f(cy - 20 * s)}) scale({s:.3f})"><path d="M13 23.5c0-4 2-7 5.5-8.5M22 23.5c0-4 2-7 5.5-8.5" class="m-cite-ink"/><circle cx="15" cy="25" r="2.6" class="m-dot"/><circle cx="24" cy="25" r="2.6" class="m-dot"/></g>',
        cls,
    )


def _answer(x, y, w, h, lines=(0.8, 0.66, 0.74), acc=0.42, cls=""):
    t = 16
    d = (
        f"M{_f(x + 12)} {_f(y)}h{_f(w - 24)}a12 12 0 0 1 12 12v{_f(h - 24)}a12 12 0 0 1-12 12"
        f"H{_f(x + 46)}l-14 {t}v-{t}H{_f(x + 12)}a12 12 0 0 1-12-12v{_f(-(h - 24))}a12 12 0 0 1 12-12z"
    )
    inner = _path(d, "blog-c-ans")
    pad = 16
    for i, f in enumerate(lines):
        inner += _rect(x + pad, y + pad + i * 13, (w - 2 * pad) * f, 5.5, 2.75, "m-faint")
    inner += _rect(x + pad, y + pad + len(lines) * 13 + 4, (w - 2 * pad) * acc, 8, 4, "m-acc")
    return _g(inner, cls)


def _chip(x, y, w, hl=False, cls=""):
    inner = _rect(x, y, w, 20, 10, "blog-c-chip blog-c-chip-hl" if hl else "blog-c-chip")
    inner += _circ(x + 11, y + 10, 3.5, "blog-c-ok")
    inner += _rect(x + 20, y + 8, w - 30, 4, 2, "m-faint")
    return _g(inner, cls)


def _stamp(cx, cy, r=26, cls=""):
    inner = _circ(cx, cy, r, "blog-c-stamp") + _circ(cx, cy, r - 6, "blog-c-stamp blog-c-stamp-in")
    inner += f'<path d="M{_f(cx - 9)} {_f(cy + 1)}l6 6 12-13" class="blog-c-stamp-ck"/>'
    return _g(inner, f"blog-c-stp {cls}".strip(), f' transform="rotate(-12 {_f(cx)} {_f(cy)})"')


def _gauge(cx, cy, r, frac, cls=""):
    a0, a1 = math.pi * 0.75, math.pi * 2.25

    def pt(a, rr=r):
        return cx + rr * math.cos(a), cy + rr * math.sin(a)

    x0, y0 = pt(a0)
    x1, y1 = pt(a1)
    am = a0 + (a1 - a0) * frac
    xm, ym = pt(am)
    big = 1 if (am - a0) > math.pi else 0
    inner = _path(f"M{_f(x0)} {_f(y0)}A{_f(r)} {_f(r)} 0 1 1 {_f(x1)} {_f(y1)}", "blog-c-gtrack")
    inner += _path(f"M{_f(x0)} {_f(y0)}A{_f(r)} {_f(r)} 0 {big} 1 {_f(xm)} {_f(ym)}", "blog-c-gval")
    nx, ny = pt(am, r - 14)
    inner += _path(f"M{_f(cx)} {_f(cy)}L{_f(nx)} {_f(ny)}", "blog-c-needle")
    inner += _circ(cx, cy, 5, "blog-c-hub")
    return _g(inner, cls)


def _node(cx, cy, r, ic, cls=""):
    inner = _circ(cx, cy, r, "m-ring") + _circ(cx, cy, r * 0.66, "m-core") + _glyph(ic, cx, cy, r * 0.62, "m-glyph", True)
    return _g(inner, cls)


def _dots(pts, cls="m-spark"):
    return "".join(_circ(x, y, r, cls) for x, y, r in pts)


def _c_ranked():
    out = []
    rows = 7
    y0, step = 30, 33
    hl = 3
    widths = [150, 128, 160, 140, 118, 150, 104]
    for i in range(rows):
        y = y0 + i * step
        fade = f" blog-c-o{min(i, 5)}" if i != hl else ""
        is_hl = i == hl
        row = _rect(34, y, 238, 24, 8, "blog-c-card blog-c-hl" if is_hl else "blog-c-card")
        row += _rect(42, y + 5, 14, 14, 4, "m-acc" if is_hl else "blog-c-rank")
        row += _rect(66, y + 7, widths[i] * 0.55, 4.5, 2.25, "m-ink" if is_hl else "m-faint")
        row += _rect(66, y + 14.5, widths[i], 3.5, 1.75, "m-faint")
        out.append(_g(row, f"blog-c-row{fade}"))
        sy = y + 12
        d = f"M272 {sy}C330 {sy} 330 140 384 140"
        out.insert(0, _path(d, "blog-c-wire-hot" if is_hl else "blog-c-wire"))
    out.append(_circ(384, 140, 5, "m-dot blog-c-bl"))
    out.append(_g(_answer(404, 62, 206, 136, (0.86, 0.7, 0.8, 0.56), 0.46), "blog-c-fl"))
    for k, (x, w, h2) in enumerate([(420, 52, False), (478, 70, True), (554, 44, False)]):
        out.append(_rect(x, 222, w, 18, 9, "blog-c-chip blog-c-chip-hl" if h2 else "blog-c-chip"))
        out.append(_rect(x + 9, 229, w - 18, 4, 2, "m-acc" if h2 else "m-faint"))
    out.append(_cite(604, 62, 18))
    out.append(_dots([(330, 40, 2.5), (612, 246, 2), (360, 250, 3)]))
    return out


def _c_gates():
    out = []
    out.append(_path("M150 140H520", "blog-c-wire"))
    out.append(_path("M150 140H520", "blog-c-beam"))
    for i, (cx, ry, rx) in enumerate([(250, 92, 26), (340, 78, 22), (424, 64, 18)]):
        out.append(_g(f'<ellipse cx="{cx}" cy="140" rx="{rx}" ry="{ry}" class="blog-c-gate"/><ellipse cx="{cx}" cy="140" rx="{rx - 8}" ry="{ry - 10}" class="blog-c-gate-in"/>', "blog-c-gt", f' style="--k:{i}"'))
        out.append(_circ(cx, 140 - ry, 9, "blog-c-okc"))
        out.append(f'<path d="M{cx - 4} {140 - ry}l3 3 5-6" class="blog-c-okk"/>')
    out.append(_g(_card(40, 76, 112, 128, (0.62, 0.9, 0.74, 0.84, 0.6), False, "doc"), "blog-c-fl2"))
    out.append(_g(_answer(468, 84, 146, 102, (0.84, 0.66), 0.5), "blog-c-fl"))
    out.append(_cite(608, 86, 16))
    out.append(_chip(482, 40, 84, False, "blog-c-fl2"))
    out.append(_chip(456, 214, 86, True, "blog-c-fl"))
    out.append(_chip(548, 214, 66))
    out.append(_chip(500, 240, 76))
    out.append(_dots([(196, 52, 2.5), (380, 236, 2), (172, 236, 3)]))
    return out


def _c_decay():
    out = []
    out.append(_path("M30 246H610", "blog-c-axis"))
    for x in range(90, 611, 80):
        out.append(_path(f"M{x} 246v5", "blog-c-axis"))
    out.append(_path("M30 244C70 244 84 42 112 42S150 236 214 240S420 244 610 244", "blog-c-spike"))
    out.append(_path("M30 244C120 236 170 196 250 176S420 128 470 112", "blog-c-wire-hot blog-c-durable"))
    posts = [(70, 70, -9, 1), (120, 112, 7, 2), (60, 156, -4, 3)]
    for x, y, rot, k in posts:
        out.append(_g(_card(x, y, 84, 40, (0.62, 0.9), False, "linkedin"), f"blog-c-fall blog-c-o{k}", f' style="--k:{k}" transform="rotate({rot} {x + 42} {y + 20})"'))
    for x, y, _, _ in posts:
        out.append(_path(f"M{x + 84} {y + 20}C{x + 200} {y + 20} 360 120 452 120", "blog-c-link"))
    out.append(_g(_card(452, 52, 140, 168, (0.6, 0.9, 0.8, 0.86, 0.7, 0.5), True, "doc"), "blog-c-fl"))
    out.append(_cite(590, 54, 18))
    out.append(_circ(470, 112, 5, "m-dot blog-c-bl"))
    out.append(_dots([(330, 50, 2.5), (380, 220, 2), (250, 120, 2)]))
    return out


def _c_category():
    out = []
    out.append(_circ(320, 140, 112, "blog-c-orbit"))
    out.append(_circ(320, 140, 72, "blog-c-orbit blog-c-orbit-2"))
    out.append(_path("M320 14V266M120 140H520", "blog-c-cross"))
    corners = [(40, 30, "target", False), (470, 30, "layers", False), (40, 196, "x", False), (470, 196, "user", False)]
    for i, (x, y, ic, _) in enumerate(corners):
        ex = x + 130 if x < 320 else x
        ey = y + 27
        tx = 236 if x < 320 else 404
        ty = 118 if y < 140 else 162
        out.append(_path(f"M{ex} {ey}H{(ex + tx) / 2:.0f}V{ty}H{tx}", "blog-c-wire-hot" if i == 1 else "blog-c-wire"))
        out.append(_g(_card(x, y, 130, 54, (0.66, 0.84), False, ic), f"blog-c-fl{'2' if i % 2 else ''}"))
        out.append(_circ(tx, ty, 4, "m-dot"))
    box = _rect(236, 104, 168, 72, 14, "blog-c-card blog-c-hl")
    box += _rect(254, 122, 70, 6, 3, "m-ink") + _rect(330, 122, 52, 6, 3, "m-acc")
    box += _rect(254, 136, 128, 4.5, 2.25, "m-faint") + _rect(254, 146, 104, 4.5, 2.25, "m-faint") + _rect(254, 156, 116, 4.5, 2.25, "m-faint")
    out.append(_g(box, "blog-c-def"))
    out.append(_path("M388 104V58", "blog-c-pole"))
    out.append(_g('<path d="M388 58h36l-8 10 8 10h-36z" class="blog-c-flag"/>', "blog-c-wave"))
    out.append(_dots([(200, 30, 2.5), (440, 250, 2), (180, 250, 3), (450, 100, 2)]))
    return out


def _c_audit():
    out = []
    tones = ["blog-c-s-ok", "blog-c-s-mid", "blog-c-s-mid", "blog-c-s-low", "blog-c-s-ok", "blog-c-s-mid", "blog-c-s-low", "blog-c-s-mid", "blog-c-s-ok", "blog-c-s-low", "blog-c-s-mid", "blog-c-s-ok"]
    i = 0
    for r in range(3):
        for c in range(4):
            x, y = 30 + c * 66, 36 + r * 74
            dim = " blog-c-o2" if tones[i] == "blog-c-s-low" else ""
            t = _rect(x, y, 56, 64, 8, "blog-c-card" + (" blog-c-hl" if i == 5 else ""))
            t += _rect(x + 8, y + 10, 26, 4.5, 2.25, "m-ink") + _rect(x + 8, y + 20, 40, 3.5, 1.75, "m-faint") + _rect(x + 8, y + 28, 32, 3.5, 1.75, "m-faint") + _rect(x + 8, y + 36, 36, 3.5, 1.75, "m-faint")
            t += _circ(x + 46, y + 52, 4.5, tones[i])
            out.append(_g(t, "blog-c-tile" + dim, f' style="--k:{i}"'))
            i += 1
    out.append(_path("M286 122L330 100", "blog-c-wire-hot"))
    lens = _circ(410, 140, 92, "blog-c-lens") + _circ(410, 140, 92, "blog-c-lens-ring")
    rows = ""
    for k, score in enumerate([2, 1, 2, 0, 1]):
        y = 92 + k * 22
        rows += _rect(352, y - 2, 64, 5, 2.5, "m-faint" if k else "m-ink")
        for j in range(2):
            rows += _circ(438 + j * 16, y, 5.5, "m-acc" if j < score else "blog-c-empty")
    rows += _rect(352, 202, 116, 8, 4, "blog-c-s-midbar")
    out.append(_g(lens + rows, "blog-c-fl"))
    out.append(_path("M476 206L516 246", "blog-c-handle"))
    out.append(_gauge(566, 92, 40, 0.5, "blog-c-fl2"))
    out.append(_g(_rect(528, 166, 76, 22, 11, "blog-c-chip") + _circ(541, 177, 4, "blog-c-s-ok") + _rect(551, 175, 42, 4, 2, "m-faint"), ""))
    out.append(_g(_rect(528, 196, 76, 22, 11, "blog-c-chip blog-c-chip-hl") + _circ(541, 207, 4, "blog-c-s-mid") + _rect(551, 205, 42, 4, 2, "m-acc"), ""))
    out.append(_g(_rect(528, 226, 76, 22, 11, "blog-c-chip") + _circ(541, 237, 4, "blog-c-s-low") + _rect(551, 235, 42, 4, 2, "m-faint"), "blog-c-o2"))
    return out


def _c_entity():
    out = []
    cx, cy = 320, 140
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="250" ry="112" class="blog-c-orbit"/>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="160" ry="74" class="blog-c-orbit blog-c-orbit-2"/>')
    sats = [(-1.57, "building"), (-0.6, "target"), (0.45, "layers"), (1.57, "user"), (2.6, "doc"), (3.65, "x")]
    pos = []
    for i, (a, ic) in enumerate(sats):
        x, y = cx + 220 * math.cos(a), cy + 100 * math.sin(a)
        pos.append((x, y, ic, i))
        out.append(_path(f"M{cx} {cy}L{_f(x)} {_f(y)}", "blog-c-wire-hot" if i == 2 else "blog-c-wire"))
    for x, y, _, i in pos:
        for da in (-0.32, 0.32):
            ox, oy = x + 46 * math.cos(math.atan2(y - cy, x - cx) + da), y + 30 * math.sin(math.atan2(y - cy, x - cx) + da)
            out.append(_path(f"M{_f(x)} {_f(y)}L{_f(ox)} {_f(oy)}", "blog-c-wire"))
            out.append(_circ(ox, oy, 3.5, "blog-c-leaf"))
    for x, y, ic, i in pos:
        hl = i == 2
        t = _rect(x - 20, y - 20, 40, 40, 11, "blog-c-card blog-c-hl" if hl else "blog-c-card")
        t += _glyph(ic, x, y, 20, "blog-c-icg" if hl else "m-glyph", True)
        out.append(_g(t, "blog-c-fl2" if i % 2 else "blog-c-fl"))
    out.append(_g(_node(cx, cy, 44, "node"), "blog-c-core"))
    out.append(_cite(cx + 40, cy - 40, 15))
    return out


def _iso(inner, tx, ty, s=1.0):
    return f'<g transform="matrix({0.866 * s:.3f} {0.33 * s:.3f} {-0.866 * s:.3f} {0.33 * s:.3f} {tx} {ty})">{inner}</g>'


def _c_stack():
    out = []
    n = 160
    cx = 320
    levels = [192, 138, 84, 30]
    out.append(_path(f"M{cx} 276V26", "blog-c-wire"))
    for li, ty in enumerate(levels):
        base = _rect(0, 0, n, n, 14, "blog-c-plate" + (" blog-c-plate-hl" if li == 2 else ""))
        if li == 0:
            inner = "".join(_rect(22 + k * 12, 80 - h / 2, 6, h, 3, "m-acc" if 4 <= k <= 6 else "m-faint") for k, h in enumerate([16, 34, 54, 28, 70, 46, 60, 24, 40, 18]))
        elif li == 1:
            inner = _path("M30 80H130", "blog-c-wire") + "".join(_circ(30 + k * 25, 80, 8, "m-dot" if k == 2 else "blog-c-leaf2") for k in range(5))
        elif li == 2:
            inner = "".join(_rect(x, y, 54, 54, 8, "blog-c-card blog-c-hl" if (x, y) == (20, 20) else "blog-c-card") for x in (20, 86) for y in (20, 86))
            inner += "".join(_rect(x + 10, y + 14, 30, 5, 2.5, "m-acc" if (x, y) == (20, 20) else "m-ink") for x in (20, 86) for y in (20, 86))
        else:
            inner = "".join(_rect(20, 22 + k * 30, 120, 18, 9, "blog-c-chip" + (" blog-c-chip-hl" if k == 1 else "")) for k in range(4))
        out.append(_g(_iso(base + inner, cx, ty, 0.78), "blog-c-lvl", f' style="--k:{li}"'))
    for li, (ty, ic) in enumerate(zip(levels, ["wave", "node", "doc", "send"])):
        y = ty + 41
        out.append(_path(f"M{cx + 112} {y}H{cx + 160}", "blog-c-wire-hot" if li == 2 else "blog-c-wire"))
        out.append(_circ(cx + 112, y, 3.5, "m-dot"))
        out.append(_g(_card(cx + 160, y - 19, 112, 38, (0.6,), li == 2, ic), "blog-c-fl2" if li % 2 else "blog-c-fl"))
    for k, (x, y, r) in enumerate([(40, 60, -8), (96, 150, 6), (30, 200, -4), (120, 40, 10)]):
        out.append(_g(_card(x, y, 96, 46, (0.6, 0.8)), "blog-c-o4", f' transform="rotate({r} {x + 48} {y + 23})"'))
    out.append(_path(f"M{cx} 272V30", "blog-c-beam blog-c-beam-v"))
    out.append(_cite(cx, 18, 13))
    out.append(_dots([(240, 250, 2.5), (560, 250, 2), (520, 30, 3)]))
    return out


def _c_video():
    out = []
    vx, vy, vw, vh = 34, 78, 176, 104
    v = _rect(vx, vy, vw, vh, 14, "blog-c-card blog-c-hl")
    v += _circ(vx + vw / 2, vy + vh / 2 - 6, 20, "m-acc")
    v += f'<path d="M{_f(vx + vw / 2 - 6)} {_f(vy + vh / 2 - 16)}v20l17-10z" class="blog-c-play blog-c-keep"/>'
    v += _rect(vx + 14, vy + vh - 18, vw - 28, 4, 2, "m-faint") + _rect(vx + 14, vy + vh - 18, (vw - 28) * 0.38, 4, 2, "m-acc")
    out.append(_g(v, "blog-c-fl"))
    wave = "".join(_rect(vx + 6 + k * 8.4, 214 - h / 2, 4, h, 2, "m-faint" if k % 5 else "m-acc") for k, h in enumerate([8, 14, 22, 12, 30, 18, 26, 10, 20, 34, 16, 24, 12, 28, 18, 8, 22, 14, 10, 6, 12]))
    out.append(wave)
    gx, gy, cw, ch, gap = 290, 54, 40, 30, 7
    out.append(_rect(gx - 12, gy - 32, 7 * (cw + gap) + 17, 5 * (ch + gap) + 44, 16, "blog-c-card"))
    out.append("".join(_rect(gx + k * (cw + gap) + 12, gy - 18, 16, 4, 2, "m-faint") for k in range(7)))
    fills = {0: "m-acc", 3: "blog-c-cell-a", 6: "blog-c-cell-c", 8: "blog-c-cell-b", 9: "blog-c-cell-c", 11: "blog-c-cell-b", 13: "blog-c-cell-c", 15: "m-acc", 16: "blog-c-cell-c", 18: "blog-c-cell-b", 20: "blog-c-cell-c", 22: "blog-c-cell-a", 23: "blog-c-cell-c", 25: "blog-c-cell-b", 27: "blog-c-cell-c", 29: "blog-c-cell-a", 30: "blog-c-cell-c", 32: "blog-c-cell-b"}
    targets = []
    for i in range(35):
        r, c = divmod(i, 7)
        x, y = gx + c * (cw + gap), gy + r * (ch + gap)
        cls = fills.get(i, "blog-c-cell")
        out.append(_rect(x, y, cw, ch, 6, cls, f' style="--k:{i}"'))
        if i in (0, 15, 22, 29):
            targets.append((x, y + ch / 2))
    fan = "".join(_path(f"M{vx + vw} {vy + vh / 2}C250 {vy + vh / 2} 250 {_f(ty)} {_f(tx)} {_f(ty)}", "blog-c-link") for tx, ty in targets)
    out.insert(0, fan)
    out.append(_cite(gx + 7 * (cw + gap) + 2, gy - 30, 16))
    return out


COVERS = {
    "blog/stop-ranking-start-dominating": _c_ranked,
    "blog/answer-engine-visibility-guide": _c_gates,
    "blog/b2b-linkedin-content-dies": _c_decay,
    "blog/category-creation-ai-search": _c_category,
    "blog/content-audit-ai-retrieval": _c_audit,
    "blog/entity-first-content-architecture": _c_entity,
    "blog/new-b2b-content-stack": _c_stack,
    "blog/one-video-authority-system": _c_video,
}


def cover_shapes(seed):
    fn = COVERS.get(seed)
    if fn is None:
        keys = sorted(COVERS)
        fn = COVERS[keys[_rng(seed).randrange(len(keys))]]
    return fn()


def cover_svg(seed, cls="cover"):
    kind = seed.split("/")[-1]
    return f'<svg class="m-art blog-cov {cls}" data-cover="{kind}" viewBox="0 0 640 280" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{"".join(cover_shapes(seed))}</svg>'


DIVIDERS = [
    "M0 40 C 260 40, 340 12, 600 40 S 940 68, 1200 40",
    "M0 40 C 300 68, 420 68, 600 40 S 900 12, 1200 40",
    "M0 40 C 200 20, 420 20, 600 40 S 1000 60, 1200 40",
]


def divider(i):
    d = DIVIDERS[i % len(DIVIDERS)]
    mid = f"dvm-{i}"
    return (
        f'<div class="divider" aria-hidden="true"><svg viewBox="0 0 1200 80" preserveAspectRatio="none" focusable="false">'
        f'<defs><mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="80"><rect class="dv-wipe" x="0" y="0" width="1200" height="80" fill="#fff"/></mask></defs>'
        f'<path class="dv-base" d="{d}"/><path class="dv-line" d="{d}" mask="url(#{mid})"/></svg>'
        f'<span class="dv-node"></span></div>'
    )
