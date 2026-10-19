import hashlib
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


def cover_shapes(seed):
    r = _rng(seed)
    shapes = []
    src = (r.randint(70, 150), r.randint(90, 210))
    shapes.append(("source", src[0], src[1], r.choice([84, 96, 108])))
    n = r.randint(3, 5)
    cards = []
    for i in range(n):
        cx = r.randint(250, 420)
        cy = 40 + i * (220 // n) + r.randint(-6, 14)
        cards.append((cx, cy))
    ans = (r.randint(470, 510), r.randint(110, 170))
    for cx, cy in cards:
        shapes.append(("wire", src[0], src[1], cx, cy + 24))
        shapes.append(("wire", cx + 64, cy + 24, ans[0], ans[1] + 32))
    hl = r.randrange(n)
    for i, (cx, cy) in enumerate(cards):
        shapes.append(("card", cx, cy, i == hl))
    shapes.append(("answer", ans[0], ans[1]))
    shapes.append(("cite", ans[0] + 70, ans[1] - 26))
    for _ in range(r.randint(4, 7)):
        shapes.append(("dot", r.randint(20, 620), r.randint(16, 284), r.choice([2, 3, 4])))
    return shapes


def cover_svg(seed, cls="cover"):
    out = []
    for s in cover_shapes(seed):
        k = s[0]
        if k == "wire":
            _, x1, y1, x2, y2 = s
            d = f"M{x1} {y1} C {(x1 + x2) // 2} {y1}, {(x1 + x2) // 2} {y2}, {x2} {y2}"
            out.append(f'<path class="m-wire" d="{d}"/><path class="m-flow" d="{d}"/>')
        elif k == "source":
            _, x, y, size = s
            out.append(_use("m-source", x - size // 2, y - size // 2, size, size))
        elif k == "card":
            _, x, y, hl = s
            out.append(_use("m-card", x, y, 64, 48, "m-hl" if hl else ""))
        elif k == "answer":
            _, x, y = s
            out.append(_use("m-answer", x, y, 96, 64))
        elif k == "cite":
            _, x, y = s
            out.append(f'<g class="m-pulse">{_use("m-cite", x, y, 30, 30)}</g>')
        elif k == "dot":
            _, x, y, rr = s
            out.append(f'<circle cx="{x}" cy="{y}" r="{rr}" class="m-spark"/>')
    return f'<svg class="m-art {cls}" viewBox="0 0 640 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{"".join(out)}</svg>'


DIVIDERS = [
    "M0 40 C 260 40, 340 12, 600 40 S 940 68, 1200 40",
    "M0 40 C 300 68, 420 68, 600 40 S 900 12, 1200 40",
    "M0 40 C 200 20, 420 20, 600 40 S 1000 60, 1200 40",
]


def divider(i):
    d = DIVIDERS[i % len(DIVIDERS)]
    return (
        f'<div class="divider" aria-hidden="true"><svg viewBox="0 0 1200 80" preserveAspectRatio="none" focusable="false">'
        f'<path class="dv-base" d="{d}"/><path class="dv-line" d="{d}"/></svg>'
        f'<span class="dv-node"></span></div>'
    )
