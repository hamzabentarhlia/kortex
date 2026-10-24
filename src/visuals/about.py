from . import kit
from .kit import icon


def b1(lang):
    lines = "".join(f'<i class="ab-l{" is-hl" if n in (1, 3) else ""}" style="--w:{w}%;--i:{n}"></i>' for n, w in enumerate([90, 74, 86, 62]))
    return f'<div class="ab ab-1"><span class="ab-src">{icon("mic")}</span><span class="ab-lines">{lines}</span><span class="ab-x">{icon("x")}{icon("spark")}</span></div>'


def b2(lang):
    faint = "".join(f'<i style="--i:{n}"></i>' for n in range(9))
    return f'<div class="ab ab-2"><span class="ab-many">{faint}</span><span class="ab-one">{icon("doc")}</span></div>'


def b3(lang):
    return f'<div class="ab ab-3"><span class="ab-page"><i></i><i></i><i></i></span><span class="ab-mark">{icon("check")}</span></div>'


def b4(lang):
    return f'<div class="ab ab-4">{kit.gauge(10, 10, "", size=110)}</div>'


def b5(lang):
    return f'<div class="ab ab-5"><span class="ab-fork"><i class="ab-a"></i><i class="ab-b"></i></span><span class="ab-yes">{icon("check")}</span><span class="ab-no">{icon("x")}</span></div>'


VISUALS = {"about-b1": b1, "about-b2": b2, "about-b3": b3, "about-b4": b4, "about-b5": b5}
