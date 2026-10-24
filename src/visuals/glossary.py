import re
from pathlib import Path

from . import kit
from .kit import T, icon, label, chip, cite, gauge, frame, EXAMPLE, ILLUSTRATIVE, BRAND

PAGES = Path(__file__).resolve().parent.parent / "pages"

TERM_ICONS = {
    "entity": "node",
    "topical-authority": "grid",
    "citation-rate": "gauge",
    "schema-markup": "code",
    "answer-first-content": "pyramid",
    "generative-engine-optimization": "spark",
    "answer-engine-optimization": "question",
    "search-engine-optimization": "search",
    "ai-overviews": "layers",
    "llms-txt": "doc",
}


def arrow():
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{kit.ICONS.get("arrow", "")}</svg>'


def gi(name):
    return icon(name, "gl-i")


def fig(cls, cap, inner, lbl=""):
    return (
        f'<div class="gl-fig {cls}"><div class="gl-cap"><span class="gl-cap-t">{cap}</span>{lbl}</div>{inner}</div>'
    )


def entity(lang):
    sats = [
        ("user", T(lang, "Founder", "Fondateur", "المؤسس"), T(lang, "Person", "Personne", "شخص"), T(lang, "founded by", "fondée par", "أسسها"), 16, 22),
        ("box", T(lang, "Your product", "Votre produit", "منتجك"), T(lang, "Product", "Produit", "منتج"), T(lang, "makes", "fabrique", "تصنع"), 84, 22),
        ("map", T(lang, "Your city", "Votre ville", "مدينتك"), T(lang, "Place", "Lieu", "مكان"), T(lang, "based in", "basée à", "مقرها"), 16, 78),
        ("target", T(lang, "Your field", "Votre domaine", "مجالك"), T(lang, "Topic", "Sujet", "موضوع"), T(lang, "expert in", "experte en", "خبيرة في"), 84, 78),
        ("linkedin", "LinkedIn", T(lang, "Profile", "Profil", "ملف"), T(lang, "same as", "identique à", "نفس الكيان"), 50, 9),
        ("doc", T(lang, "Press article", "Article de presse", "مقال صحفي"), T(lang, "Mention", "Mention", "إشارة"), T(lang, "mentioned in", "citée dans", "ذُكرت في"), 50, 91),
    ]
    lines = "".join(
        f'<line x1="50%" y1="50%" x2="{x}%" y2="{y}%" style="--i:{i}"/>' for i, (_, _, _, _, x, y) in enumerate(sats)
    )
    nodes = "".join(
        f'<div class="gl-en-n pop" style="--x:{x}%;--y:{y}%;--i:{i + 2}"><span class="gl-en-ic">{gi(ic)}</span><span class="gl-en-t"><b>{t}</b><small>{s}</small></span></div>'
        for i, (ic, t, s, _, x, y) in enumerate(sats)
    )
    edges = "".join(
        f'<span class="gl-en-l gl-u" style="--x:{(50 + x) / 2}%;--y:{(50 + y) / 2}%;--i:{i + 5}">{e}</span>'
        for i, (_, _, _, e, x, y) in enumerate(sats)
    )
    core = (
        f'<div class="gl-en-core pop" style="--i:0"><span class="gl-en-pulse" aria-hidden="true"></span>'
        f'<span class="gl-en-ic">{gi("building")}</span><span class="gl-en-t"><b dir="ltr">{BRAND}</b><small>{T(lang, "Organization", "Organisation", "مؤسسة")}</small></span></div>'
    )
    stage = (
        f'<div class="gl-en"><svg class="gl-en-e" aria-hidden="true" focusable="false">{lines}</svg>{edges}{nodes}{core}</div>'
        f'<div class="gl-foot gl-u" style="--i:10">{gi("check")}{T(lang, "One name and one description, repeated the same way on every profile.", "Un seul nom et une seule description, repris à l’identique sur chaque profil.", "اسم واحد ووصف واحد، يتكرران بالصيغة نفسها في كل ملف.")}</div>'
    )
    return fig("gl-entity", T(lang, "How a machine sees your brand", "Comment une machine voit votre marque", "كيف ترى الآلة علامتك"), stage, label(EXAMPLE[lang]))


def topical(lang):
    cells = [
        (T(lang, "Definitions", "Définitions", "التعريفات"), 1),
        (T(lang, "How it works", "Fonctionnement", "طريقة العمل"), 1),
        (T(lang, "Pricing", "Tarifs", "الأسعار"), 1),
        (T(lang, "Comparisons", "Comparatifs", "المقارنات"), 1),
        (T(lang, "Common mistakes", "Erreurs courantes", "الأخطاء الشائعة"), 0),
        (T(lang, "How to choose", "Comment choisir", "كيف تختار"), 1),
        (T(lang, "Use cases", "Cas d’usage", "حالات الاستخدام"), 1),
        (T(lang, "Alternatives", "Alternatives", "البدائل"), 0),
        (T(lang, "FAQ", "FAQ", "الأسئلة الشائعة"), 1),
        (T(lang, "Objections", "Objections", "الاعتراضات"), 0),
        (T(lang, "Tools", "Outils", "الأدوات"), 1),
        (T(lang, "Step by step", "Pas à pas", "خطوة بخطوة"), 1),
        (T(lang, "Regulation", "Réglementation", "التنظيم"), 0),
        (T(lang, "Glossary", "Glossaire", "المصطلحات"), 1),
        (T(lang, "Costs", "Coûts", "التكاليف"), 1),
        (T(lang, "Trends", "Tendances", "الاتجاهات"), 0),
    ]
    out = []
    for i, (name, done) in enumerate(cells):
        cls = "is-on" if done else "is-gap"
        ic = gi("check") if done else gi("plus")
        out.append(f'<div class="gl-tc {cls} gl-u" style="--i:{i}"><span class="gl-tc-f" aria-hidden="true"></span>{ic}<span>{name}</span></div>')
    covered = sum(c for _, c in cells)
    frac = covered / len(cells)
    meter = (
        f'<div class="gl-tm gl-u" style="--i:17"><span class="gl-tm-k">{T(lang, "Coverage", "Couverture", "التغطية")}</span>'
        f'<span class="gl-tm-t"><i style="--s:{frac:.3f}"></i></span>'
        f'<span class="gl-tm-v">{T(lang, f"{covered} of {len(cells)} subtopics", f"{covered} sous-sujets sur {len(cells)}", f"{covered} من {len(cells)} موضوعا فرعيا")}</span></div>'
    )
    legend = (
        f'<div class="gl-leg"><span><i class="is-on"></i>{T(lang, "Covered by a page", "Traité par une page", "تغطيه صفحة")}</span>'
        f'<span><i class="is-gap"></i>{T(lang, "Gap", "Manque", "فجوة")}</span></div>'
    )
    head = f'<div class="gl-tp">{gi("target")}<b>{T(lang, "Topic: your subject", "Sujet : votre domaine", "الموضوع: مجالك")}</b></div>'
    return fig("gl-topical", T(lang, "A coverage map of one subject", "La carte de couverture d’un sujet", "خريطة تغطية موضوع واحد"), f'{head}<div class="gl-tg">{"".join(out)}</div>{meter}{legend}', label(EXAMPLE[lang]))


def citation(lang):
    hits = {1, 6, 10, 13, 17}
    dots = "".join(f'<i class="pop{" is-hit" if k in hits else ""}" style="--i:{k // 2}"></i>' for k in range(20))
    g = gauge(25, 100, T(lang, "ChatGPT, 20 tracked questions", "ChatGPT, 20 questions suivies", "ChatGPT، 20 سؤالا متابَعا"), size=200, unit="%")
    formula = (
        f'<div class="gl-cr-def gl-u" style="--i:1">{T(lang, "Citation rate = cited answers ÷ questions asked", "Taux de citation = réponses qui vous citent ÷ questions posées", "معدل الاستشهاد = الإجابات التي تذكرك ÷ الأسئلة المطروحة")}</div>'
        f'<div class="gl-cr-f gl-u" style="--i:2" dir="ltr">'
        f'<span class="gl-cr-b is-hl"><b>5</b><small>{T(lang, "cited answers", "réponses citantes", "إجابات تذكرك")}</small></span>'
        f'<span class="gl-cr-op">÷</span>'
        f'<span class="gl-cr-b"><b>20</b><small>{T(lang, "questions asked", "questions posées", "سؤالا مطروحا")}</small></span>'
        f'<span class="gl-cr-op">=</span>'
        f'<span class="gl-cr-b is-res"><b>25%</b><small>{T(lang, "citation rate", "taux de citation", "معدل الاستشهاد")}</small></span></div>'
        f'<div class="gl-cr-dots" aria-hidden="true">{dots}</div>'
        f'<div class="gl-leg"><span><i class="is-on"></i>{T(lang, "Answer names you", "La réponse vous nomme", "الإجابة تذكرك")}</span><span><i class="is-gap"></i>{T(lang, "Answer cites others", "La réponse cite d’autres sources", "الإجابة تذكر غيرك")}</span></div>'
    )
    inner = f'<div class="gl-cr"><div class="gl-cr-g pop">{g}</div><div class="gl-cr-r">{formula}</div></div>'
    return fig("gl-citation", T(lang, "How the rate is calculated", "Comment le taux se calcule", "كيف يُحسب المعدل"), inner, label(ILLUSTRATIVE[lang], "illustrative"))


def schema(lang):
    regions = [
        ("BreadcrumbList", '<div class="gl-sc-crumb"><i></i><b>›</b><i></i><b>›</b><i class="is-w"></i></div>', T(lang, "Where the page sits", "La place de la page", "موقع الصفحة")),
        ("Article", '<div class="gl-sc-art"><i class="gl-sc-h"></i><div class="gl-sc-by"><span></span><i></i></div><i style="--w:96%"></i><i style="--w:88%"></i><i style="--w:70%"></i></div>', T(lang, "Title, author, dates", "Titre, auteur, dates", "العنوان والكاتب والتواريخ")),
        ("FAQPage", '<div class="gl-sc-faq">' + "".join(f'<div>{gi("question")}<i style="--w:{w}%"></i>{gi("plus")}</div>' for w in (62, 74, 54)) + "</div>", T(lang, "Questions and answers", "Questions et réponses", "الأسئلة والأجوبة")),
        ("Organization", f'<div class="gl-sc-org"><span class="gl-sc-logo">{gi("building")}</span><b dir="ltr">{BRAND}</b><span class="gl-sc-soc">{gi("linkedin")}{gi("mail")}{gi("globe")}</span></div>', T(lang, "Who publishes it", "Qui la publie", "من ينشرها")),
    ]
    rows = "".join(
        f'<div class="gl-sc-row"><div class="gl-sc-reg gl-u" style="--i:{i}"><span class="gl-sc-out" aria-hidden="true"></span>{body}</div>'
        f'<div class="gl-sc-tag pop" style="--i:{i + 3}"><code dir="ltr">"@type": "{t}"</code><small>{d}</small></div></div>'
        for i, (t, body, d) in enumerate(regions)
    )
    inner = f'<div class="gl-sc"><span class="gl-sc-scan" aria-hidden="true"></span>{rows}</div>'
    return fig("gl-schema", T(lang, "One page, four labels machines can read", "Une page, quatre étiquettes lisibles par les machines", "صفحة واحدة وأربعة وسوم تقرؤها الآلات"), inner, label(EXAMPLE[lang]))


def answer_first(lang):
    layers = [
        ("is-a", T(lang, "Answer", "Réponse", "الإجابة"), T(lang, "Most B2B teams pay between X and Y per month.", "La plupart des équipes B2B paient entre X et Y par mois.", "تدفع معظم فرق B2B ما بين X وY شهريا."), T(lang, "One or two sentences, complete on their own", "Une ou deux phrases, complètes à elles seules", "جملة أو جملتان مكتملتان بذاتهما")),
        ("is-b", T(lang, "Context", "Contexte", "السياق"), "", T(lang, "Why, and what it depends on", "Pourquoi, et de quoi cela dépend", "لماذا، وعلى ماذا يتوقف")),
        ("is-c", T(lang, "Detail", "Détail", "التفاصيل"), "", T(lang, "Examples and nuance", "Exemples et nuances", "أمثلة وفروق دقيقة")),
    ]
    out = []
    for i, (cls, name, quote, note) in enumerate(layers):
        q = f'<span class="gl-af-q">{quote}</span>' if quote else ""
        out.append(f'<div class="gl-af-l {cls} gl-u" style="--i:{i + 1}"><b>{name}</b>{q}<small>{note}</small></div>')
    lift = (
        f'<div class="gl-af-lift pop" style="--i:5"><span class="gl-af-qm">{gi("quote")}</span>'
        f'<span>{T(lang, "AI engines and featured snippets lift this part", "Les moteurs IA et les extraits optimisés reprennent cette partie", "تقتبس محركات الذكاء الاصطناعي والمقتطفات المميزة هذا الجزء")}</span></div>'
    )
    inner = f'<div class="gl-af">{lift}<div class="gl-af-p">{"".join(out)}</div></div>'
    return fig("gl-answer-first", T(lang, "The inverted pyramid", "La pyramide inversée", "الهرم المقلوب"), inner)


def geo(lang):
    srcs = [
        ("industry-report.com", 1, 0),
        (BRAND, 1, 1),
        ("vendor-blog.com", 1, 0),
        ("competitor.com", 0, 0),
    ]
    cards = "".join(
        f'<div class="gl-gs-c gl-u{" is-hl" if hl else ""}{" is-off" if not used else ""}" style="--i:{i}">{gi("doc")}<b dir="ltr">{d}</b><i></i><i style="--w:60%"></i>'
        f'<small>{T(lang, "cited", "cité", "مستشهد به") if hl else (T(lang, "used", "utilisé", "مستخدم") if used else T(lang, "not used", "non retenu", "غير مستخدم"))}</small></div>'
        for i, (d, used, hl) in enumerate(srcs)
    )
    paths = []
    for k, x in enumerate((50, 150, 250, 350)):
        cls = "is-hl" if k == 1 else ("is-off" if k == 3 else "")
        paths.append(f'<path class="{cls}" d="M{x} 0 C{x} 40 200 30 200 70"/>')
    links = f'<svg class="gl-gs-links" viewBox="0 0 400 70" preserveAspectRatio="none" aria-hidden="true" focusable="false">{"".join(paths)}</svg>'
    q = T(lang, "What should I check before choosing a supplier?", "Que vérifier avant de choisir un fournisseur ?", "ما الذي يجب التحقق منه قبل اختيار مورد؟")
    a1 = T(lang, "Start with three checks: delivery times, references in your sector and the terms of the contract.", "Commencez par trois vérifications : les délais, les références dans votre secteur et les conditions du contrat.", "ابدأ بثلاثة أمور: مدة التسليم، والمراجع في قطاعك، وشروط العقد.")
    ans = (
        f'<div class="gl-ga pop" style="--i:5"><div class="gl-ga-h">{chip(T(lang, "AI answer", "Réponse IA", "إجابة الذكاء الاصطناعي"))}<span class="gl-ga-sp">{gi("spark")}</span></div>'
        f'<div class="gl-ga-q">{gi("search")}<span>{q}</span></div>'
        f'<div class="gl-ga-p" data-type="700">{a1}</div><i class="gl-ga-sk"></i><i class="gl-ga-sk" style="--w:72%"></i>'
        f'<div class="gl-ga-s">{cite(BRAND, "is-hl")}<span class="vx-src" dir="ltr">industry-report.com</span><span class="vx-src" dir="ltr">vendor-blog.com</span></div></div>'
    )
    inner = f'<div class="gl-geo"><div class="gl-gs">{cards}</div>{links}{ans}</div>'
    return fig("gl-geo-fig", T(lang, "One answer, written from several sources", "Une réponse, écrite à partir de plusieurs sources", "إجابة واحدة تُكتب من عدة مصادر"), inner, label(EXAMPLE[lang]))


def aeo(lang):
    q = T(lang, "What is a citation rate?", "Qu’est-ce qu’un taux de citation ?", "ما هو معدل الاستشهاد؟")
    a = T(lang, "The share of tracked questions in which an AI engine names your brand.", "La part des questions suivies pour lesquelles un moteur IA nomme votre marque.", "نسبة الأسئلة المتابَعة التي يذكر فيها محرك الذكاء الاصطناعي علامتك.")
    surfaces = [
        ("search", T(lang, "Featured snippet", "Extrait optimisé", "المقتطف المميز")),
        ("mic", T(lang, "Voice assistant", "Assistant vocal", "المساعد الصوتي")),
        ("chat", T(lang, "AI chatbot", "Chatbot IA", "روبوت المحادثة")),
    ]
    surf = "".join(
        f'<div class="gl-ae-s gl-u" style="--i:{i + 4}"><span class="gl-ae-si">{gi(ic)}</span><b>{n}</b>'
        + ('<span class="gl-ae-w" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>' if ic == "mic" else '<span class="gl-ae-k" aria-hidden="true"><i></i><i style="--w:66%"></i></span>')
        + "</div>"
        for i, (ic, n) in enumerate(surfaces)
    )
    inner = (
        f'<div class="gl-ae"><div class="gl-ae-q gl-u">{gi("search")}<span data-type="300">{q}</span></div>'
        f'<span class="gl-ae-c gl-u" style="--i:1" aria-hidden="true"></span>'
        f'<div class="gl-ae-a pop" style="--i:2"><span class="gl-ae-tag">{gi("check")}{T(lang, "One direct answer", "Une seule réponse directe", "إجابة مباشرة واحدة")}</span>'
        f'<div class="gl-ae-ans">{a}</div>{cite(BRAND, "is-hl")}</div>'
        f'<div class="gl-ae-lbl gl-u" style="--i:3">{T(lang, "The same answer, wherever the question is asked", "La même réponse, où que la question soit posée", "الإجابة نفسها أينما طُرح السؤال")}</div>'
        f'<div class="gl-ae-ss">{surf}</div></div>'
    )
    return fig("gl-aeo", T(lang, "A question gets one answer", "Une question, une réponse", "سؤال واحد وإجابة واحدة"), inner, label(EXAMPLE[lang]))


def seo(lang):
    sig = [
        ("shield", T(lang, "Crawlable", "Explorable", "قابلة للزحف"), T(lang, "Technical health", "Santé technique", "السلامة التقنية")),
        ("target", T(lang, "Relevant", "Pertinente", "ذات صلة"), T(lang, "Matches the search", "Répond à la recherche", "تطابق البحث")),
        ("link", T(lang, "Trusted", "Fiable", "موثوقة"), T(lang, "Links from other sites", "Liens d’autres sites", "روابط من مواقع أخرى")),
    ]
    legend = "".join(
        f'<div class="gl-se-sig gl-u" style="--i:{i}"><span class="gl-se-sic" data-n="{i}">{gi(ic)}</span><span><b>{n}</b><small>{d}</small></span></div>'
        for i, (ic, n, d) in enumerate(sig)
    )
    res = [("industry-report.com", 3), (BRAND, 3), ("vendor-blog.com", 2), ("competitor.com", 2), ("old-forum.net", 1)]
    rows = []
    for i, (d, n) in enumerate(res):
        pips = "".join(f'<i class="pop{" is-f" if k < n else ""}" style="--i:{i + k + 3}" data-n="{k}"></i>' for k in range(3))
        hl = " is-hl" if d == BRAND else ""
        rows.append(
            f'<li class="gl-se-r gl-u{hl}" style="--i:{i + 2}"><span class="gl-se-n">{i + 1}</span>'
            f'<span class="gl-se-t"><small dir="ltr">{d}</small><i style="--w:{[82, 90, 74, 68, 58][i]}%"></i><i class="is-s" style="--w:{[60, 66, 52, 56, 40][i]}%"></i></span>'
            f'<span class="gl-se-p" aria-hidden="true">{pips}</span></li>'
        )
    inner = (
        f'<div class="gl-se"><div class="gl-se-l"><div class="gl-se-h">{T(lang, "What search engines weigh", "Ce que pèsent les moteurs", "ما تزنه محركات البحث")}</div>{legend}</div>'
        f'<div class="gl-se-list"><div class="gl-se-bar">{gi("search")}<span>{T(lang, "your topic", "votre sujet", "موضوعك")}</span></div><ol>{"".join(rows)}</ol></div></div>'
    )
    return fig("gl-seo", T(lang, "Ranked results and the signals behind them", "Des résultats classés et les signaux derrière", "نتائج مرتبة والإشارات التي تقف وراءها"), inner, label(ILLUSTRATIVE[lang], "illustrative"))


def aio(lang):
    q = T(lang, "how to plan a content calendar", "comment planifier un calendrier éditorial", "كيف أخطط لتقويم المحتوى")
    srcs = [(BRAND, 1), ("industry-report.com", 0), ("vendor-blog.com", 0)]
    sc = "".join(
        f'<div class="gl-ao-src pop{" is-hl" if hl else ""}" style="--i:{i + 4}">{gi("link")}<b dir="ltr">{d}</b><i></i></div>'
        for i, (d, hl) in enumerate(srcs)
    )
    ov = (
        f'<div class="gl-ao-ov gl-u" style="--i:1"><span class="gl-ao-sh" aria-hidden="true"></span>'
        f'<div class="gl-ao-oh">{gi("spark")}<b>AI Overview</b></div>'
        f'<div class="gl-ao-b"><div class="gl-ao-txt"><div class="gl-ao-p">{T(lang, "Pick one theme per month, map each post to a question your buyers ask, then fix a publishing rhythm you can keep.", "Choisissez un thème par mois, reliez chaque contenu à une question de vos acheteurs, puis fixez un rythme tenable.", "اختر موضوعا لكل شهر، واربط كل منشور بسؤال يطرحه مشتروك، ثم حدد وتيرة نشر تستطيع الالتزام بها.")}</div>'
        f'<i></i><i style="--w:84%"></i><i style="--w:62%"></i></div><div class="gl-ao-ss">{sc}</div></div></div>'
    )
    links = "".join(
        f'<div class="gl-ao-lk gl-u" style="--i:{i + 7}"><small dir="ltr">{d}</small><i style="--w:{w}%"></i><i class="is-s" style="--w:{w - 18}%"></i></div>'
        for i, (d, w) in enumerate([("competitor.com", 70), ("old-forum.net", 58)])
    )
    body = (
        f'<div class="gl-ao"><div class="gl-ao-q">{gi("search")}<span>{q}</span></div>{ov}'
        f'<div class="gl-ao-div gl-u" style="--i:6"><span>{T(lang, "Classic results start here", "Les résultats classiques commencent ici", "تبدأ النتائج التقليدية هنا")}</span></div>{links}</div>'
    )
    inner = frame(body, "browser", "google.com/search")
    return fig("gl-aio", T(lang, "The AI summary sits above the links", "Le résumé IA s’affiche au-dessus des liens", "الملخص الذكي يظهر فوق الروابط"), inner, label(EXAMPLE[lang]))


def llms(lang):
    h = chr(35)
    rows = [
        ("h", f"{h} {BRAND}"),
        ("q", "> " + "<bdi>" + T(lang, "What the company does, in one sentence.", "Ce que fait l’entreprise, en une phrase.", "ما تفعله الشركة في جملة واحدة.") + "</bdi>"),
        ("e", ""),
        ("h", f"{h}{h} <bdi>" + T(lang, "Key pages", "Pages clés", "الصفحات الأساسية") + "</bdi>"),
        ("l", ("pricing", T(lang, "Pricing", "Tarifs", "الأسعار"), T(lang, "plans and prices", "offres et prix", "الباقات والأسعار"))),
        ("l", ("how-it-works", T(lang, "How it works", "Méthode", "طريقة العمل"), T(lang, "the method, step by step", "la méthode, étape par étape", "المنهج خطوة بخطوة"))),
        ("l", ("glossary", T(lang, "Glossary", "Glossaire", "المعجم"), T(lang, "short definitions", "définitions courtes", "تعريفات قصيرة"))),
        ("l", ("about", T(lang, "About", "À propos", "من نحن"), T(lang, "who is behind it", "qui est derrière", "من يقف وراءها"))),
    ]
    out = []
    for i, (kind, v) in enumerate(rows):
        if kind == "l":
            slug, name, desc = v
            txt = f'<span class="gl-lt-m">- [</span><bdi><b>{name}</b></bdi><span class="gl-lt-m">](</span><span class="gl-lt-u" dir="ltr">https://{BRAND}/{slug}</span><span class="gl-lt-m">):</span> <bdi class="gl-lt-d">{desc}</bdi>'
        else:
            txt = v
        out.append(f'<li class="gl-lt-{kind} gl-u" style="--i:{i}"><span class="gl-lt-n" aria-hidden="true">{i + 1}</span><span class="gl-lt-c">{txt}</span></li>')
    file = (
        f'<div class="gl-lf"><div class="gl-lf-h">{gi("doc")}<span dir="ltr">{BRAND}/llms.txt</span><em>{T(lang, "plain text", "texte brut", "نص عادي")}</em></div>'
        f'<ol class="gl-lf-b" dir="ltr">{"".join(out)}</ol></div>'
    )
    readers = "".join(f'<li class="pop" style="--i:{i + 9}">{chip(n)}</li>' for i, n in enumerate(["ChatGPT", "Claude", "Perplexity"]))
    side = (
        f'<div class="gl-lr"><span class="gl-lr-ar" aria-hidden="true">{gi("arrow")}</span>'
        f'<div class="gl-lr-p">{T(lang, "Language models can read it to find your most useful pages first", "Les modèles de langage peuvent le lire pour trouver d’abord vos pages les plus utiles", "يمكن للنماذج اللغوية قراءته لتجد أهم صفحاتك أولا")}</div><ul>{readers}</ul>'
        f'<small>{T(lang, "A voluntary convention, not a guarantee", "Une convention volontaire, pas une garantie", "عرف طوعي وليس ضمانا")}</small></div>'
    )
    return fig("gl-llms", T(lang, "A short file at the root of your site", "Un petit fichier à la racine de votre site", "ملف قصير في جذر موقعك"), f'<div class="gl-ll">{file}{side}</div>', label(EXAMPLE[lang]))


SKY = [
    ("generative-engine-optimization", "GEO", 77, 50),
    ("answer-engine-optimization", "AEO", 87, 22),
    ("search-engine-optimization", "SEO", 79, 78),
    ("ai-overviews", "AI Overviews", 93, 62),
    ("citation-rate", None, 89, 90),
    ("answer-first-content", None, 70, 24),
    ("entity", None, 63, 62),
    ("schema-markup", None, 66, 86),
    ("topical-authority", None, 96, 40),
    ("llms-txt", "llms.txt", 61, 40),
]
SKY_EDGES = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 7), (7, 6), (6, 8), (5, 8), (9, 0), (3, 2), (7, 9), (6, 0), (4, 3)]


def sky_name(lang, slug):
    names = {
        "citation-rate": T(lang, "Citation rate", "Taux de citation", "معدل الاستشهاد"),
        "answer-first-content": T(lang, "Answer-first", "Réponse d’abord", "الإجابة أولا"),
        "entity": T(lang, "Entity", "Entité", "الكيان"),
        "schema-markup": T(lang, "Schema markup", "Balisage schema", "ترميز Schema"),
        "topical-authority": T(lang, "Topical authority", "Autorité thématique", "السلطة الموضوعية"),
    }
    return names[slug]


def sky(lang):
    rtl = lang == "ar"
    pts = [(100 - x if rtl else x, y) for _, _, x, y in SKY]
    lines = "".join(
        f'<line x1="{pts[a][0]}%" y1="{pts[a][1]}%" x2="{pts[b][0]}%" y2="{pts[b][1]}%" style="--i:{k}"/>' for k, (a, b) in enumerate(SKY_EDGES)
    )
    nodes = ""
    for k, (s, n, _, _) in enumerate(SKY):
        x, y = pts[k]
        left = x > 12 if rtl else x >= 85
        cls = (" is-core" if k == 0 else "") + (" is-l" if left else "")
        nodes += f'<span class="gl-sk-n{cls}" style="--x:{x}%;--y:{y}%;--i:{k}"><i></i><b>{n or sky_name(lang, s)}</b></span>'
    return f'<div class="gl-sk"><div class="gl-sk-d"><svg aria-hidden="true" focusable="false">{lines}</svg>{nodes}</div></div>'


def _meta(path):
    raw = path.read_text(encoding="utf-8")
    head = raw.split("\n---\n", 1)[0]
    meta = {}
    for line in head.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta


def index(lang):
    read = T(lang, "Read", "Lire", "اقرأ")
    items = []
    for p in sorted((PAGES / lang / "glossary").glob("*.html")):
        m = _meta(p)
        title = re.sub(r"<[^>]+>", "", m.get("h1", m["title"]))
        items.append((title.lower(), p.stem, title, m.get("summary", m["description"])))
    items.sort()
    cards = "".join(
        f'<a class="glass card list-card gl-ix" href="@glossary/{slug}"><span class="gl-ix-ic">{gi(TERM_ICONS.get(slug, "doc"))}</span>'
        f'<h3>{title}</h3><p>{summary}</p><span class="card-link">{read}{arrow()}</span></a>'
        for _, slug, title, summary in items
    )
    return f'<div class="grid grid-3 glossary-grid">{cards}</div>'


VISUALS = {
    "glossary-sky": sky,
    "glossary-index": index,
    "glossary-entity": entity,
    "glossary-topical-authority": topical,
    "glossary-citation-rate": citation,
    "glossary-schema-markup": schema,
    "glossary-answer-first": answer_first,
    "glossary-geo": geo,
    "glossary-aeo": aeo,
    "glossary-seo": seo,
    "glossary-ai-overviews": aio,
    "glossary-llms-txt": llms,
}
