from .kit import T, icon, chip, cite, label, node, uid, wipe_mask, EXAMPLE, ILLUSTRATIVE, BRAND


def _ex(lang):
    return label(EXAMPLE[lang])


def _typed(text, delay=600):
    return f'<p class="vx-ans-p"><span data-type="{delay}">{text}</span></p>'


def _ans(lang, q, text, engine="Perplexity", delay=700, cls="", extra=""):
    srcs = cite(BRAND, "is-hl compare-m-hit") + f'<span class="vx-src" dir="ltr">industry-report.com</span>'
    return (
        f'<div class="vx-answer {cls}">'
        f'<div class="vx-ans-h">{chip(engine)}{_ex(lang)}</div>'
        f'<p class="vx-ans-q">{icon("search")}<span>{q}</span></p>'
        f'<div class="vx-ans-b">{_typed(text, delay)}<i class="vx-line" style="--w:92%"></i><i class="vx-line" style="--w:70%"></i>{extra}</div>'
        f'<div class="vx-ans-s">{srcs}</div></div>'
    )


def _q(lang):
    return T(lang, "How do we stop new B2B users from churning?", "Comment éviter que les nouveaux utilisateurs B2B partent ?", "كيف نمنع المستخدمين الجدد في B2B من المغادرة؟")


def _a(lang):
    return T(lang, "Give each role one short checklist during the first 14 days.", "Donnez à chaque rôle une courte check-list pendant les 14 premiers jours.", "امنح كل دور قائمة مهام قصيرة خلال أول 14 يوما.")


def paths(lang):
    m = uid()
    xs = [125, 375, 625, 875]
    lines = "".join(
        f'<path d="M500 0C500 70 {x} 50 {x} 120" class="{"compare-p-k" if i == 3 else "compare-p-l"}"/>' for i, x in enumerate(xs)
    )
    fan = (
        f'<svg class="compare-p-fan" viewBox="0 0 1000 120" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
        f'<defs><mask id="{m}" maskUnits="userSpaceOnUse"><rect class="compare-p-wipe" x="0" y="0" width="1000" height="120" fill="#fff"/></mask></defs>'
        f'<g mask="url(#{m})">{lines}</g></svg>'
    )
    rank = "".join(
        f'<li><span>{n}</span><i style="--w:{w}%"></i></li>'
        for n, w in zip(range(1, 9), [86, 70, 78, 62, 74, 66, 80, 58])
    )
    cols = [
        ("01", T(lang, "SEO agency", "Agence SEO", "وكالة SEO"), T(lang, "Ends in a ranked list", "Finit en liste classée", "تنتهي بقائمة مرتبة"),
         f'<div class="compare-p-card"><ol class="compare-p-rank">{rank}</ol><p class="compare-p-foot">{icon("chart")}{T(lang, "Rankings report", "Rapport de classement", "تقرير الترتيب")}</p></div>'),
        ("02", T(lang, "ChatGPT alone", "ChatGPT seul", "ChatGPT وحده"), T(lang, "Ends in generic text", "Finit en texte générique", "ينتهي بنص عام"),
         f'<div class="compare-p-card compare-p-gen"><p>{T(lang, "Onboarding is important for every business. A good process helps users understand the product.", "L’onboarding est important pour toute entreprise. Un bon processus aide les utilisateurs à comprendre le produit.", "التهيئة مهمة لكل شركة. والعملية الجيدة تساعد المستخدمين على فهم المنتج.")}</p>'
         f'<i class="vx-line" style="--w:94%"></i><i class="vx-line" style="--w:80%"></i><i class="vx-line" style="--w:60%"></i><span class="compare-p-none">{T(lang, "No sources", "Aucune source", "بلا مصادر")}</span></div>'),
        ("03", T(lang, "Freelance writer", "Rédacteur freelance", "كاتب مستقل"), T(lang, "Ends in one article", "Finit en un article", "ينتهي بمقال واحد"),
         f'<div class="compare-p-card compare-p-doc"><span class="compare-p-doc-h">{icon("doc")}<b></b></span><i class="vx-line" style="--w:96%"></i><i class="vx-line" style="--w:88%"></i><i class="vx-line" style="--w:92%"></i><i class="vx-line" style="--w:54%"></i>'
         f'<p class="compare-p-foot">{icon("pen")}{T(lang, "1 article", "1 article", "مقال واحد")}</p></div>'),
        ("04", "KORTEX", T(lang, "Ends in a cited AI answer", "Finit cité dans une réponse IA", "تنتهي باستشهاد في إجابة ذكاء اصطناعي"),
         _ans(lang, _q(lang), _a(lang), delay=1400, cls="compare-p-card")),
    ]
    out = "".join(
        f'<div class="compare-p-col st{" compare-k" if i == 3 else ""}" style="--i:{i + 2}"><p class="compare-p-h"><span>{n}</span><b>{t}</b><small>{s}</small></p>{card}</div>'
        for i, (n, t, s, card) in enumerate(cols)
    )
    src = node("layers", T(lang, "Your expertise", "Votre expertise", "خبرتك"), T(lang, "Same starting point", "Même point de départ", "نقطة الانطلاق نفسها"))
    return f'<div class="compare-p"><div class="compare-p-src pop">{src}</div>{fan}<div class="compare-p-cols">{out}</div></div>'


DOMAINS = ["competitor.com", "industry-report.com", "vendor-blog.com", "directory-site.com", "news-site.com", "forum-thread.com", BRAND, "review-site.com", "wiki-page.org", "another-blog.com"]


def collapse(lang, mini=False):
    n = 5 if mini else 10
    rows = "".join(
        f'<li class="compare-c-row{" compare-me" if d == BRAND else ""}" style="--i:{i}"><span class="compare-c-n">{i + 1}</span><span class="compare-c-t"><span dir="ltr">{d}</span><i style="--w:{[84, 66, 76, 58, 72][i % 5]}%"></i></span></li>'
        for i, d in enumerate((DOMAINS[:4] + [BRAND]) if mini else DOMAINS)
    )
    head = f'<p class="compare-c-h">{icon("search")}<span>{T(lang, "Search results", "Résultats de recherche", "نتائج البحث")}</span><b dir="ltr">1–{n}</b></p>'
    note = f'<p class="compare-c-note">{icon("arrow")}{T(lang, "The answer comes first", "La réponse passe en premier", "الإجابة تأتي أولا")}</p>'
    lst = f'<div class="compare-c-list st" data-scrub><div>{head}<ol>{rows}</ol>{note}</div></div>'
    if mini:
        ans = f'<div class="compare-c-ans pop" style="--i:2"><div class="vx-answer"><div class="vx-ans-h">{chip("ChatGPT")}</div><div class="vx-ans-b"><i class="vx-line" style="--w:94%"></i><i class="vx-line" style="--w:76%"></i></div><div class="vx-ans-s">{cite(BRAND, "is-hl compare-m-hit")}</div></div></div>'
        return f'<div class="compare-c compare-mini" aria-hidden="true">{lst}{ans}</div>'
    ans = f'<div class="compare-c-ans st" style="--i:2" data-scrub>{_ans(lang, _q(lang), _a(lang), "Google AI Overviews", 900)}</div>'
    return f'<div class="compare-c">{lst}{ans}</div>'


def mine(lang, mini=False):
    trans = [
        ("04:12", T(lang, "Most churn we see happens in", "L’essentiel du churn arrive", "معظم المغادرة التي نراها تحدث"), T(lang, "the first 14 days", "dans les 14 premiers jours", "في أول 14 يوما"), T(lang, ", before a second login.", ", avant la deuxième connexion.", "، قبل الدخول الثاني.")),
        ("11:38", T(lang, "We stopped sending feature tours and sent", "Nous avons arrêté les visites guidées pour envoyer", "توقفنا عن جولات الميزات وأرسلنا"), T(lang, "one checklist per role", "une check-list par rôle", "قائمة مهام لكل دور"), "."),
        ("23:05", T(lang, "Ask which report their manager reads, then", "Demandez quel rapport lit leur manager, puis", "اسأل عن التقرير الذي يقرؤه مديرهم، ثم"), T(lang, "build that report first", "construisez ce rapport d’abord", "ابن ذلك التقرير أولا"), "."),
    ]
    claims = [
        T(lang, "Churn concentrates in the first 14 days.", "Le churn se concentre sur les 14 premiers jours.", "تتركز المغادرة في أول 14 يوما."),
        T(lang, "One checklist per role beats a generic tour.", "Une check-list par rôle remplace la visite générique.", "قائمة لكل دور بدل جولة عامة."),
        T(lang, "Build the report the manager reads first.", "Construire d’abord le rapport que lit le manager.", "ابن أولا التقرير الذي يقرؤه المدير."),
    ]
    tip = T(lang, "Links back to {t} in the source transcript", "Renvoie à {t} dans la transcription source", "يحيل إلى {t} في النص المفرغ للمصدر")
    if mini:
        left = '<div class="compare-m-p compare-m-gray"><i class="vx-line" style="--w:92%"></i><i class="vx-line" style="--w:78%"></i><i class="vx-line" style="--w:86%"></i><i class="vx-line" style="--w:60%"></i></div>'
        right = "".join(f'<p class="compare-m-claim st" style="--i:{i + 1}"><i class="vx-line" style="--w:{w}%"></i><span class="compare-m-mk" dir="ltr">{t}</span></p>' for i, ((t, *_), w) in enumerate(zip(trans, [80, 64, 72])))
        return f'<div class="compare-m compare-mini" aria-hidden="true">{left}<div class="compare-m-p compare-m-hot">{right}</div></div>'
    lines = "".join(
        f'<p class="compare-m-ln st" style="--i:{i + 2}"><span class="compare-m-ts" dir="ltr">{t}</span><span>{a} <mark style="--i:{i}">{b}</mark>{c}</span></p>'
        for i, (t, a, b, c) in enumerate(trans)
    )
    cl = "".join(
        f'<li class="compare-m-claim st" style="--i:{i};--d:1500ms"><span>{c}</span><span class="compare-m-mk" dir="ltr" tabindex="0" data-tip="{tip.format(t=t)}">{icon("link")}{t}</span></li>'
        for i, ((t, *_), c) in enumerate(zip(trans, claims))
    )
    generic = T(lang, "Customer onboarding is essential for any business. A good onboarding process helps users understand your product and improves satisfaction over time.", "L’onboarding client est essentiel pour toute entreprise. Un bon processus aide les utilisateurs à comprendre votre produit et améliore leur satisfaction.", "تهيئة العملاء أمر أساسي لأي شركة. والعملية الجيدة تساعد المستخدمين على فهم منتجك وترفع رضاهم مع الوقت.")
    left = (
        f'<div class="compare-m-p compare-m-gray st" style="--i:0"><p class="compare-m-tag">{T(lang, "ChatGPT alone", "ChatGPT seul", "ChatGPT وحده")}</p>'
        f'<p class="compare-m-prompt">{icon("chat")}<span data-type="500">{T(lang, "Write a post about customer onboarding", "Écris un post sur l’onboarding client", "اكتب منشورا عن تهيئة العملاء")}</span></p>'
        f'<p class="compare-m-out">{generic}</p><i class="vx-line" style="--w:94%"></i><i class="vx-line" style="--w:82%"></i><i class="vx-line" style="--w:66%"></i>'
        f'<p class="compare-m-flags"><span>{T(lang, "No sources", "Aucune source", "بلا مصادر")}</span><span>{T(lang, "Could be anyone’s", "Pourrait venir de n’importe qui", "قد يكون لأي أحد")}</span></p>'
        f'<p class="compare-m-same">{T(lang, "Same prompt, other companies", "Même prompt, autres entreprises", "الطلب نفسه، شركات أخرى")}</p>'
        + "".join(f'<div class="compare-m-dupe st" style="--i:{i + 3}"><span dir="ltr">{d}</span><i class="vx-line" style="--w:92%"></i><i class="vx-line" style="--w:74%"></i></div>' for i, d in enumerate(["competitor.com", "vendor-blog.com"]))
        + '</div>'
    )
    right = (
        f'<div class="compare-m-p compare-m-hot st" style="--i:1"><p class="compare-m-tag">KORTEX{_ex(lang)}</p>'
        f'<div class="compare-m-src"><p class="compare-m-src-h">{icon("play")}<span>{T(lang, "Your webinar transcript", "Transcription de votre webinaire", "النص المفرغ لندوتك")}</span></p>{lines}</div>'
        f'<p class="compare-m-arrow st" style="--i:5" aria-hidden="true">{icon("scissors")}{T(lang, "Mined into claims", "Extrait en affirmations", "استخراج إلى معلومات")}</p>'
        f'<ul class="compare-m-claims">{cl}</ul></div>'
    )
    return f'<div class="compare-m">{left}<span class="compare-m-vs" aria-hidden="true">vs</span>{right}</div>'


NODES = [
    ("pillar", "doc", 50, 6),
    ("faq", "question", 76, 24),
    ("compare", "columns", 76, 80),
    ("gloss", "tag", 50, 95),
    ("social", "linkedin", 24, 80),
    ("news", "mail", 24, 24),
]
EDGES = [(0, 1), (0, 2), (0, 3), (1, 3), (4, 5), (5, 0), (2, 4)]


def _names(lang):
    return {
        "pillar": (T(lang, "Pillar article", "Article pilier", "مقال محوري"), T(lang, "The long piece every asset links back to", "Le texte long vers lequel tout renvoie", "النص الطويل الذي تحيل إليه كل المواد")),
        "faq": (T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة شائعة"), T(lang, "Direct answers to buyer questions", "Des réponses directes aux questions d’acheteurs", "إجابات مباشرة عن أسئلة المشترين")),
        "compare": (T(lang, "Comparison page", "Page comparatif", "صفحة مقارنة"), T(lang, "Your approach next to the alternatives", "Votre approche face aux alternatives", "نهجك إلى جانب البدائل")),
        "gloss": (T(lang, "Glossary entry", "Entrée de glossaire", "مدخل معجم"), T(lang, "One term, defined in your words", "Un terme, défini avec vos mots", "مصطلح واحد بتعريفك أنت")),
        "social": (T(lang, "Social posts", "Posts sociaux", "منشورات اجتماعية"), T(lang, "Short takes that point to the pillar", "Des formats courts qui renvoient au pilier", "مقتطفات قصيرة تحيل إلى المقال المحوري")),
        "news": (T(lang, "Newsletter", "Newsletter", "النشرة البريدية"), T(lang, "The same ideas for your list", "Les mêmes idées pour vos abonnés", "الأفكار نفسها لمشتركيك")),
    }


def _web(lang, mini=False):
    m = uid()
    ln = "".join(f'<line x1="50" y1="48" x2="{x}" y2="{y}" class="compare-w-s"/>' for _, _, x, y in NODES)
    ln += "".join(f'<line x1="{NODES[a][2]}" y1="{NODES[a][3]}" x2="{NODES[b][2]}" y2="{NODES[b][3]}" class="compare-w-e"/>' for a, b in EDGES)
    svg = (
        f'<svg class="compare-w-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{wipe_mask(m)}</defs>'
        f'<g mask="url(#{m})">{ln}</g></svg>'
    )
    names = _names(lang)
    if mini:
        dots = "".join(f'<span class="compare-w-at" style="left:{x}%;top:{y}%"><span class="compare-w-n">{icon(ic)}</span></span>' for _, ic, x, y in NODES)
        return f'<div class="compare-w-map">{svg}<span class="compare-w-at" style="left:50%;top:48%"><span class="compare-w-core">{icon("play")}</span></span>{dots}</div>'
    dots = "".join(
        f'<span class="compare-w-at" style="left:{x}%;top:{y}%"><span class="compare-w-n pop" style="--i:{i + 3}" tabindex="0" data-tip="{names[k][1]}">{icon(ic)}<b>{names[k][0]}</b></span></span>'
        for i, (k, ic, x, y) in enumerate(NODES)
    )
    core = f'<span class="compare-w-at" style="left:50%;top:48%"><span class="compare-w-core pop" style="--i:1">{icon("play")}<b>{T(lang, "Your source", "Votre source", "مصدرك")}</b></span></span>'
    return f'<div class="compare-w-map">{svg}{core}{dots}</div>'


def web(lang, mini=False):
    if mini:
        art = '<div class="compare-w-art compare-mini"><span class="compare-w-art-h"></span><i class="vx-line" style="--w:90%"></i><i class="vx-line" style="--w:76%"></i><i class="vx-line" style="--w:84%"></i><i class="vx-line" style="--w:50%"></i></div>'
        return f'<div class="compare-w compare-mini" aria-hidden="true">{art}{_web(lang, True)}</div>'
    names = _names(lang)
    art = (
        f'<div class="compare-w-art st" style="--i:0"><p class="compare-m-tag">{T(lang, "Freelance writer", "Rédacteur freelance", "كاتب مستقل")}</p>'
        f'<div class="compare-w-paper"><span class="compare-w-kick">{T(lang, "Article", "Article", "مقال")}</span>'
        f'<b class="compare-w-title">{T(lang, "Why onboarding decides renewal", "Pourquoi l’onboarding décide du renouvellement", "لماذا تحسم التهيئة قرار التجديد")}</b>'
        f'<i class="vx-line" style="--w:96%"></i><i class="vx-line" style="--w:90%"></i><i class="vx-line" style="--w:94%"></i>'
        f'<span class="compare-w-quote"></span><i class="vx-line" style="--w:88%"></i><i class="vx-line" style="--w:62%"></i></div>'
        f'<p class="compare-w-cap">{icon("pen")}{T(lang, "One polished article", "Un article soigné", "مقال واحد متقن")}</p></div>'
    )
    legend = "".join(f'<li class="st" style="--i:{i + 6}">{icon(NODES[i][1])}<b>{names[NODES[i][0]][0]}</b><span>{names[NODES[i][0]][1]}</span></li>' for i in range(len(NODES)))
    sys = (
        f'<div class="compare-w-sys st" style="--i:1"><p class="compare-m-tag">KORTEX{_ex(lang)}</p>{_web(lang)}</div>'
    )
    return f'<div class="compare-w">{art}{sys}<ul class="compare-w-leg">{legend}</ul></div>'


def _mini(lang, inner):
    return f'{inner}<span class="compare-lbl">{label(ILLUSTRATIVE[lang])}</span>'


VISUALS = {
    "compare-paths": paths,
    "compare-collapse": collapse,
    "compare-mine": mine,
    "compare-web": web,
    "compare-mini-agency": lambda lang: _mini(lang, collapse(lang, True)),
    "compare-mini-chatgpt": lambda lang: _mini(lang, mine(lang, True)),
    "compare-mini-writer": lambda lang: _mini(lang, web(lang, True)),
}
