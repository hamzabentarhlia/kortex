import math

from . import kit
from .kit import T, icon, label, chip, cite, uid, wipe_mask, frame, BRAND


def _book(lang, cls="btn btn-primary"):
    txt = T(lang, "Book a strategy call", "Réserver un appel stratégique", "احجز مكالمة استراتيجية")
    return f'<a class="{cls}" href="@@book" data-track="audience-visual-book">{txt}{icon("arrow", "flip")}</a>'


def b2b_route(lang):
    wid, gid, grad = uid(), uid(), uid()
    d = "M0 22 Q62.5 40 125 22 T250 22 T375 22 T500 22 T625 22 T750 22 T875 22 T1000 22"
    svg = (
        f'<svg class="au-rt-line" viewBox="0 0 1000 44" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{wipe_mask(wid)}'
        f'<linearGradient id="{grad}"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="{gid}" maskUnits="userSpaceOnUse"><rect class="au-rt-glide" x="-220" y="-10" width="220" height="64" fill="url(#{grad})"/></mask></defs>'
        f'<path class="au-rt-base" d="{d}"/><path class="au-rt-draw" d="{d}" mask="url(#{wid})"/><path class="au-rt-hot" d="{d}" mask="url(#{gid})"/></svg>'
    )
    steps = [
        (
            T(lang, "Problem question", "Question sur le problème", "سؤال عن المشكلة"),
            T(lang, "Why do supplier risks slip past quarterly audits?", "Pourquoi les risques fournisseurs échappent-ils aux audits trimestriels ?", "لماذا تفلت مخاطر الموردين من التدقيق الفصلي؟"),
            "ChatGPT",
            [92, 74, 58],
            [(BRAND, True), ("industry-report.com", False)],
        ),
        (
            T(lang, "Comparison question", "Question de comparaison", "سؤال مقارنة"),
            T(lang, "Spreadsheets or a dedicated supplier risk tool?", "Tableur ou outil dédié au risque fournisseur ?", "جداول البيانات أم أداة مخصصة لمخاطر الموردين؟"),
            "Perplexity",
            [88, 66, 80],
            [(BRAND, True), ("vendor-blog.com", False)],
        ),
    ]
    stops = []
    for n, (kind, q, eng, lines, srcs) in enumerate(steps):
        card = kit.answer(q, lines, srcs, eng, "", "au-rt-card pop")
        stops.append((kind, card))
    short = [(BRAND, True), ("competitor.com", False), ("vendor-blog.com", False)]
    rows = "".join(
        f'<li class="{"au-hl" if hl else ""}"><span class="au-rt-n">{k + 1}</span><span dir="ltr">{dom}</span>{icon("link") if hl else ""}</li>'
        for k, (dom, hl) in enumerate(short)
    )
    q3 = T(lang, "Best supplier risk tools for mid-size manufacturers?", "Meilleurs outils de risque fournisseur pour une PME industrielle ?", "أفضل أدوات مخاطر الموردين للمصانع المتوسطة؟")
    card3 = (
        f'<div class="vx-answer au-rt-card pop"><div class="vx-ans-h">{chip("Gemini")}</div>'
        f'<p class="vx-ans-q">{icon("search")}<span>{q3}</span></p><ol class="au-rt-list">{rows}</ol></div>'
    )
    stops.append((T(lang, "Shortlist question", "Question de présélection", "سؤال القائمة المختصرة"), card3))
    days = T(lang, "MTWTFSS", "LMMJVSD", "نثرخجسح")
    head = "".join(f"<b>{c}</b>" for c in days)
    cells = "".join(f'<i class="{"au-on" if k == 10 else ""}">{k + 8}</i>' for k in range(14))
    cal = (
        f'<div class="au-rt-cal pop"><div class="au-rt-cal-h"><span class="au-rt-cal-ic">{icon("calendar")}</span>'
        f'<span><b>{T(lang, "Discovery call", "Appel découverte", "مكالمة تعارف")}</b><small dir="ltr">{BRAND}</small></span></div>'
        f'<div class="au-rt-days" aria-hidden="true">{head}{cells}</div>'
        f'<p class="au-rt-booked"><span>{icon("check")}</span>{T(lang, "Booked, Thursday 10:00", "Réservé, jeudi 10 h", "تم الحجز، الخميس 10:00")}</p></div>'
    )
    stops.append((T(lang, "First call", "Premier appel", "أول مكالمة"), cal))
    items = []
    for n, (kind, card) in enumerate(stops):
        end = n == len(stops) - 1
        pin = icon("flag") if end else str(n + 1)
        items.append(
            f'<li class="au-rt-stop{" au-end" if end else ""}" style="--i:{n};--d:{300 + n * 380}ms">'
            f'<span class="au-rt-pin pop">{pin}</span><span class="au-rt-kind au-in">{kind}</span>{card}</li>'
        )
    title = T(lang, "A buyer's path before the first call", "Le parcours d'un acheteur avant le premier appel", "مسار المشتري قبل أول مكالمة")
    cta = T(lang, "We build the answers that sit on this path.", "Nous produisons les réponses qui jalonnent ce parcours.", "نحن نصنع الإجابات التي تظهر على هذا المسار.")
    return (
        f'<div class="au-rt"><div class="au-rt-top au-in"><span class="au-rt-title">{icon("route")}{title}</span>{label(kit.EXAMPLE[lang])}</div>'
        f'<div class="au-rt-track">{svg}<ol class="au-rt-stops">{"".join(items)}</ol></div>'
        f'<div class="au-rt-cta au-in" style="--d:1700ms"><p>{cta}</p>{_book(lang)}</div></div>'
    )


def _heights(n, seed):
    out = []
    for i in range(n):
        v = 0.28 + 0.6 * abs(math.sin(i * 0.61 + seed) * math.cos(i * 0.17 + seed * 2)) + ((i * 37 + seed * 11) % 9) / 40
        out.append(min(1.0, round(v, 2)))
    return out


def creators_slice(lang):
    segs = [(7, False), (14, True), (6, False), (12, True), (5, False), (13, True), (6, False)]
    chapters = [
        T(lang, "Why start lighter", "Commencer plus léger", "لماذا تبدأ بأوزان أخف"),
        T(lang, "Recovery", "Récupération", "التعافي"),
        T(lang, "A weekly plan", "Un plan par semaine", "خطة أسبوعية"),
    ]
    html, k, c = [], 0, 0
    for count, is_ch in segs:
        hs = _heights(count, k + 3)
        bars = "".join(f'<i style="--h:{h};--b:{(k + j) % 9}"></i>' for j, h in enumerate(hs))
        k += count
        if is_ch:
            cut = f'<span class="au-cr-cut" aria-hidden="true">{icon("scissors")}</span>'
            html.append(
                f'<div class="au-cr-seg au-ch" style="flex:{count};--c:{c}">{cut}<span class="au-cr-ch">{chapters[c]}</span><span class="au-cr-bars">{bars}</span></div>'
            )
            c += 1
        else:
            html.append(f'<div class="au-cr-seg" style="flex:{count}"><span class="au-cr-bars">{bars}</span></div>')
    ruler = "".join(f"<span>{t}</span>" for t in ["00:00", "12:00", "24:00", "36:00", "48:00"])
    player = (
        f'<div class="au-cr-player au-in"><div class="au-cr-head"><span class="au-cr-ep"><span class="au-cr-play">{icon("play")}</span>'
        f'<span><b>{T(lang, "Episode 42", "Épisode 42", "الحلقة 42")}</b><small>{T(lang, "Video podcast, 48 min", "Podcast vidéo, 48 min", "بودكاست مصور، 48 دقيقة")}</small></span></span>'
        f'{label(kit.EXAMPLE[lang])}</div>'
        f'<div class="au-cr-wave" aria-hidden="true">{"".join(html)}</div><div class="au-cr-ruler" aria-hidden="true">{ruler}</div></div>'
    )
    quote = T(lang, "Start lighter than your ego wants.", "Commencez plus léger que votre ego ne le voudrait.", "ابدأ بوزن أخف مما يريده غرورك.")
    article = T(lang, "How to start strength training after 40", "Reprendre la musculation après 40 ans", "كيف تبدأ تمارين القوة بعد الأربعين")
    assets = [
        ("film", T(lang, "Clip", "Extrait", "مقطع"), f'<span class="au-cr-thumb">{icon("play")}<em dir="ltr">0:42</em></span>'),
        ("quote", T(lang, "Quote", "Citation", "اقتباس"), f'<p class="au-cr-q">{quote}</p>'),
        ("doc", T(lang, "Article", "Article", "مقال"), f'<p class="au-cr-at">{article}</p><span class="vx-sk"><i style="--w:92%"></i><i style="--w:70%"></i></span>'),
        ("linkedin", T(lang, "Post", "Post", "منشور"), '<span class="vx-sk"><i style="--w:90%"></i><i style="--w:76%"></i><i style="--w:54%"></i></span><span class="au-cr-react"><i></i><i></i><i></i></span>'),
    ]
    cards = "".join(
        f'<div class="au-cr-slot" style="--r:{r}deg;--y:{y}px"><div class="au-cr-asset au-in" style="--i:{n};--d:900ms">'
        f'<span class="au-cr-kind">{icon(ic)}{name}</span>{body}</div></div>'
        for n, ((ic, name, body), r, y) in enumerate(zip(assets, [-5, -1.5, 1.5, 5], [10, 0, 0, 10]))
    )
    lid = uid()
    lines = "".join(
        f'<path d="M{a} 0 C {a} 30, {b} 18, {b} 46"/>' for a, b in [(22, 12.5), (22, 37.5), (52, 62.5), (80, 87.5), (52, 37.5)]
    )
    links = f'<svg class="au-cr-links" viewBox="0 0 100 46" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{wipe_mask(lid)}</defs><g mask="url(#{lid})">{lines}</g></svg>'
    return f'<div class="au-cr">{player}{links}<div class="au-cr-fan">{cards}</div></div>'


def creators_decay(lang):
    mid = uid()
    flat = "M0 150 C 30 20, 60 10, 95 110 S 220 168, 400 172"
    kept = "M0 160 C 60 110, 120 92, 180 88 S 320 80, 400 72"
    return (
        f'<div class="au-dc glass"><div class="au-dc-top"><b>{T(lang, "Attention after release", "L’attention après la sortie", "الانتباه بعد النشر")}</b>{label(kit.ILLUSTRATIVE[lang], "illustrative")}</div>'
        f'<div class="au-dc-plot"><svg viewBox="0 0 400 180" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{wipe_mask(mid)}</defs>'
        f'<path class="au-dc-grid" d="M0 45H400M0 90H400M0 135H400"/>'
        f'<g mask="url(#{mid})"><path class="au-dc-a" d="{flat}"/><path class="au-dc-b" d="{kept}"/></g></svg>'
        f'<span class="au-dc-tag au-dc-tag-a au-in" style="--d:600ms">{T(lang, "Video alone", "La vidéo seule", "الفيديو وحده")}</span>'
        f'<span class="au-dc-tag au-dc-tag-b au-in" style="--d:900ms">{T(lang, "With written assets", "Avec des contenus écrits", "مع محتوى مكتوب")}</span></div>'
        f'<div class="au-dc-axis"><span>{T(lang, "Release", "Sortie", "النشر")}</span><span>{T(lang, "Months later", "Des mois plus tard", "بعد أشهر")}</span></div></div>'
    )


def _grinder():
    return (
        '<svg class="au-ec-grinder" viewBox="0 0 80 100" aria-hidden="true" focusable="false">'
        '<path d="M22 8h36l-7 24H29z"/><rect x="24" y="32" width="32" height="44" rx="6"/><circle cx="40" cy="50" r="8"/>'
        '<path d="M40 44v6"/><rect x="34" y="76" width="12" height="7" rx="2"/><rect x="14" y="86" width="52" height="8" rx="3"/></svg>'
    )


def ecommerce_assistant(lang):
    ask = T(lang, "I make espresso at home. Which grinder should I get?", "Je fais mes espressos à la maison. Quel moulin choisir ?", "أحضّر الإسبريسو في البيت. أي مطحنة أختار؟")
    ans = T(
        lang,
        "Pick a conical burr grinder with fine, stepped settings. This model fits most home machines.",
        "Prenez un moulin à meules coniques avec un réglage fin par crans. Ce modèle convient à la plupart des machines.",
        "اختر مطحنة بشفرات مخروطية وضبط دقيق متدرج. هذا الطراز يناسب معظم الآلات المنزلية.",
    )
    refs = (
        f'<span class="au-ec-ref"><b>1</b><span dir="ltr">{BRAND}</span></span>'
        f'<span class="au-ec-ref"><b>2</b><span dir="ltr">{BRAND}</span></span>'
    )
    chat = (
        f'<div class="au-ec-chat"><div class="au-ec-bar"><span class="au-ec-av">{icon("spark")}</span><b>{T(lang, "Shopping assistant", "Assistant d’achat", "مساعد التسوق")}</b></div>'
        f'<p class="au-ec-me au-in" style="--i:1">{ask}</p>'
        f'<div class="au-ec-bot au-in" style="--i:3"><p data-type="900">{ans}</p><div class="au-ec-refs">{refs}</div></div>'
        f'<div class="au-ec-input" aria-hidden="true"><span>{T(lang, "Ask a follow-up", "Poser une autre question", "اطرح سؤالا آخر")}</span>{icon("send")}</div></div>'
    )
    src = T(lang, "Source", "Source", "مصدر")
    product = (
        f'<div class="au-ec-card pop" style="--d:1500ms"><span class="au-ec-mark"><b>1</b>{src}</span>'
        f'<div class="au-ec-img">{_grinder()}</div><div class="au-ec-meta"><small>{T(lang, "Product page", "Fiche produit", "صفحة المنتج")}</small>'
        f'<b>{T(lang, "Conical burr grinder, 40 mm", "Moulin à meules coniques, 40 mm", "مطحنة بشفرات مخروطية، 40 مم")}</b>'
        f'<ul><li>{icon("check")}{T(lang, "Stepped espresso range", "Plage espresso par crans", "نطاق إسبريسو متدرج")}</li><li>{icon("check")}{T(lang, "Fits most home machines", "Compatible avec la plupart des machines", "يناسب معظم الآلات المنزلية")}</li></ul>'
        f'{cite(BRAND + "/grinders", "is-hl")}</div></div>'
    )
    guide = (
        f'<div class="au-ec-card au-ec-guide pop" style="--d:1800ms"><span class="au-ec-mark"><b>2</b>{src}</span>'
        f'<span class="au-ec-gi">{icon("doc")}</span><div class="au-ec-meta"><small>{T(lang, "Buying guide", "Guide d’achat", "دليل شراء")}</small>'
        f'<b>{T(lang, "How to choose an espresso grinder", "Comment choisir un moulin à espresso", "كيف تختار مطحنة إسبريسو")}</b>'
        f'<span class="vx-sk"><i style="--w:90%"></i><i style="--w:68%"></i></span>{cite(BRAND + "/guides", "is-hl")}</div></div>'
    )
    return (
        f'<div class="au-ec"><div class="au-ec-lbl">{label(kit.EXAMPLE[lang])}</div>'
        f'<div class="au-ec-phone au-in">{frame(chat, "phone")}</div><div class="au-ec-srcs">{product}{guide}</div></div>'
    )


def solutions_matrix(lang):
    cols = [
        ("doc", T(lang, "Blog post", "Article", "مقال")),
        ("play", T(lang, "YouTube", "YouTube", "يوتيوب")),
        ("mic", T(lang, "Podcast", "Podcast", "بودكاست")),
        ("screen", T(lang, "Webinar", "Webinaire", "ندوة")),
    ]
    rows = [
        ("building", "B2B"),
        ("mic", T(lang, "Creators", "Créateurs", "صناع المحتوى")),
        ("cart", T(lang, "E-commerce", "E-commerce", "تجارة إلكترونية")),
    ]
    order = [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7]
    out = ['<span class="au-mx-corner"></span>']
    out += [f'<span class="au-mx-col">{icon(ic)}<em>{t}</em></span>' for ic, t in cols]
    for r, (ic, t) in enumerate(rows):
        out.append(f'<span class="au-mx-row">{icon(ic)}<em>{t}</em></span>')
        for c in range(4):
            k = order[r * 4 + c]
            out.append(f'<i class="au-mx-c" style="--k:{k}"><b></b><b></b><b></b></i>')
    return f'<div class="au-mx"><div class="au-mx-grid">{"".join(out)}</div></div>'


def _preview(main, scene):
    return f'<div class="au-pv" aria-hidden="true"><span class="au-pv-ic">{icon(main)}</span><span class="au-pv-scene">{scene}</span></div>'


def pv_b2b(lang):
    dots = "".join(f'<i style="--i:{n}"></i>' for n in range(3))
    return _preview("building", f'<span class="au-pv-route">{dots}<span class="au-pv-end">{icon("calendar")}</span></span>')


def pv_creators(lang):
    bars = "".join(f'<i class="{"au-hl" if 6 <= n <= 11 else ""}" style="--h:{h}"></i>' for n, h in enumerate(_heights(18, 2)))
    return _preview("mic", f'<span class="au-pv-wave">{bars}<span class="au-pv-cut">{icon("scissors")}</span></span>')


def pv_ecommerce(lang):
    return _preview("cart", f'<span class="au-pv-chat"><i></i><i></i><span class="au-pv-tag">{icon("tag")}<b></b></span></span>')


def _src_preview(main, kind):
    if kind == "doc":
        scene = '<span class="au-pv-doc"><i></i><i></i><i></i></span><span class="au-pv-fan"><i></i><i></i><i></i></span>'
    elif kind == "play":
        scene = '<span class="au-pv-film"><i></i><i></i><i></i><i></i></span>'
    elif kind == "mic":
        scene = '<span class="au-pv-wave au-sm">' + "".join(f'<i style="--h:{h}"></i>' for h in _heights(14, 5)) + "</span>"
    else:
        scene = '<span class="au-pv-qa"><i></i><i></i><i></i></span>'
    return _preview(main, scene)


VISUALS = {
    "audience-b2b-route": b2b_route,
    "audience-creators-slice": creators_slice,
    "audience-creators-decay": creators_decay,
    "audience-ecommerce-assistant": ecommerce_assistant,
    "audience-solutions-matrix": solutions_matrix,
    "audience-pv-b2b": pv_b2b,
    "audience-pv-creators": pv_creators,
    "audience-pv-ecommerce": pv_ecommerce,
    "audience-pv-blog": lambda lang: _src_preview("doc", "doc"),
    "audience-pv-youtube": lambda lang: _src_preview("play", "play"),
    "audience-pv-podcast": lambda lang: _src_preview("mic", "mic"),
    "audience-pv-webinar": lambda lang: _src_preview("screen", "screen"),
}
