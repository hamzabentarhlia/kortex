from . import kit
from .kit import T, icon, tile, label, cite, chip

SOURCES = ["blog", "youtube", "podcast", "webinar"]


def _src_names(lang):
    return {
        "blog": (T(lang, "Blog post", "Article", "مقال"), "doc"),
        "youtube": (T(lang, "YouTube video", "Vidéo YouTube", "فيديو يوتيوب"), "play"),
        "podcast": (T(lang, "Podcast", "Podcast", "بودكاست"), "mic"),
        "webinar": (T(lang, "Webinar", "Webinaire", "ندوة رقمية"), "screen"),
    }


def _tiles(lang):
    return {
        "blog": [("doc", T(lang, "Refreshed pillar", "Pilier remis à jour", "مقال محوري محدّث")), ("chat", T(lang, "Question pages", "Pages questions", "صفحات الأسئلة")), ("columns", T(lang, "Comparison page", "Page comparative", "صفحة مقارنة")), ("grid", T(lang, "Glossary entries", "Entrées de glossaire", "مداخل المعجم")), ("linkedin", T(lang, "LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن")), ("mail", T(lang, "Newsletter issue", "Numéro de newsletter", "عدد من النشرة"))],
        "youtube": [("doc", T(lang, "Long-form article", "Article long", "مقال مطول")), ("chat", T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة شائعة")), ("columns", T(lang, "Comparison page", "Page comparative", "صفحة مقارنة")), ("film", T(lang, "Short video scripts", "Scripts vidéo courts", "نصوص فيديو قصير")), ("linkedin", T(lang, "LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن")), ("mail", T(lang, "Newsletter issue", "Numéro de newsletter", "عدد من النشرة"))],
        "podcast": [("doc", T(lang, "Episode article", "Article d'épisode", "مقال الحلقة")), ("chat", T(lang, "Question pages", "Pages questions", "صفحات الأسئلة")), ("quote", T(lang, "Quote posts", "Posts citations", "منشورات اقتباس")), ("columns", T(lang, "Guest comparison", "Comparatif invité", "مقارنة مع الضيف")), ("film", T(lang, "Short video scripts", "Scripts vidéo courts", "نصوص فيديو قصير")), ("mail", T(lang, "Newsletter issue", "Numéro de newsletter", "عدد من النشرة"))],
        "webinar": [("doc", T(lang, "Pillar guide", "Guide pilier", "دليل محوري")), ("chat", T(lang, "FAQ cluster", "Cluster FAQ", "مجموعة أسئلة")), ("columns", T(lang, "Comparison page", "Page comparative", "صفحة مقارنة")), ("target", T(lang, "Sales pages", "Pages pour la vente", "صفحات للمبيعات")), ("linkedin", T(lang, "LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن")), ("mail", T(lang, "Follow-up emails", "E-mails de suivi", "رسائل متابعة"))],
    }


def _pulls(lang):
    claim, number, question, opinion, example = (
        T(lang, "Claim", "Affirmation", "فكرة"),
        T(lang, "Number", "Chiffre", "رقم"),
        T(lang, "Question", "Question", "سؤال"),
        T(lang, "Opinion", "Opinion", "رأي"),
        T(lang, "Example", "Exemple", "مثال"),
    )
    para = T(lang, "para.", "§", "فقرة")
    slide = T(lang, "slide", "diapo", "شريحة")
    return {
        "blog": [(claim, f"{para} 4"), (number, f"{para} 7"), (question, f"{para} 11")],
        "youtube": [(opinion, "04:12"), (example, "12:40"), (question, "27:05")],
        "podcast": [(claim, "08:30"), (example, "31:05"), (question, "44:10")],
        "webinar": [(number, f"{slide} 6"), (example, "22:15"), (question, "Q&A")],
    }


def _source_art(kind, lang):
    if kind == "blog":
        rows = "".join(f'<i class="hp-l{" hp-mark" if n in (1, 4) else ""}" style="--w:{w}%"></i>' for n, w in enumerate([92, 86, 95, 70, 90, 82, 60]))
        return f'<div class="hp-doc"><b class="hp-doc-t"></b>{rows}</div>'
    if kind == "youtube":
        return '<div class="hp-player"><span class="hp-play">' + icon("play") + '</span><span class="hp-track"><i class="hp-chap"></i><i class="hp-chap"></i><i class="hp-chap"></i><i class="hp-chap"></i><b class="hp-head"><i></i></b></span></div>'
    if kind == "podcast":
        bars = "".join(f'<i style="--h:{h};--n:{n}"></i>' for n, h in enumerate([.3, .55, .8, .45, .95, .6, .35, .7, .9, .5, .25, .65, .85, .4, .75, .55, .3, .6]))
        return f'<div class="hp-wave">{bars}</div>'
    return '<div class="hp-slide"><b class="hp-slide-t"></b><span class="hp-slide-bars"><i style="--h:.45"></i><i style="--h:.7"></i><i style="--h:.55"></i><i style="--h:.9"></i></span><span class="hp-qa">' + icon("question") + "</span></div>"


def pipeline(lang):
    names = _src_names(lang)
    tiles = _tiles(lang)
    pulls = _pulls(lang)
    built = {
        "blog": T(lang, "Built from your blog post", "Issu de votre article", "مبني على مقالك"),
        "youtube": T(lang, "Built from your video", "Issu de votre vidéo", "مبني على الفيديو"),
        "podcast": T(lang, "Built from your podcast", "Issu de votre podcast", "مبني على البودكاست"),
        "webinar": T(lang, "Built from your webinar", "Issu de votre webinaire", "مبني على الندوة"),
    }
    tabs = "".join(
        f'<button type="button" role="tab" id="hp-{k}" aria-controls="hp-panel" aria-selected="{"true" if k == "blog" else "false"}" tabindex="{0 if k == "blog" else -1}" data-src="{k}">{icon(names[k][1])}<span>{names[k][0]}</span></button>'
        for k in SOURCES
    )
    srcs = "".join(
        f'<div class="hp-src" data-s="{k}"><div class="hp-src-h"><span class="hp-src-ic">{icon(names[k][1])}</span><b>{names[k][0]}</b></div>{_source_art(k, lang)}</div>'
        for k in SOURCES
    )
    pull_html = "".join(
        f'<ul class="hp-pulls" data-s="{k}">' + "".join(f'<li style="--i:{i}"><b>{a}</b><span dir="ltr">{b}</span></li>' for i, (a, b) in enumerate(pulls[k])) + "</ul>"
        for k in SOURCES
    )
    tile_html = "".join(
        f'<div class="hp-tiles" data-s="{k}">' + "".join(tile(ic, t, cls="hp-tile" + (" is-hl" if i == 0 else ""), i=i, lines=0) for i, (ic, t) in enumerate(tiles[k])) + "</div>"
        for k in SOURCES
    )
    q = T(lang, "Which approach to supplier risk works for mid-size manufacturers?", "Quelle approche du risque fournisseur pour une ETI industrielle ?", "ما أفضل طريقة لإدارة مخاطر الموردين في شركة صناعية متوسطة؟")
    built_html = "".join(f'<span class="hp-built" data-s="{k}">{icon(names[k][1])}{built[k]}</span>' for k in SOURCES)
    ans = (
        f'<div class="vx-answer hp-answer"><div class="vx-ans-h">{chip("ChatGPT")}{label(kit.EXAMPLE[lang])}</div>'
        f'<p class="vx-ans-q">{icon("search")}<span>{q}</span></p>'
        '<div class="vx-ans-b"><i class="vx-line" style="--w:96%"></i><i class="vx-line" style="--w:88%"></i><i class="vx-line" style="--w:62%"></i></div>'
        f'<div class="vx-ans-s"><span class="vx-src" dir="ltr">industry-report.com</span>{cite(kit.BRAND, "is-hl hp-cite")}<span class="vx-src" dir="ltr">vendor-blog.com</span></div>'
        f'<div class="hp-built-row">{built_html}</div></div>'
    )
    beam_label = T(lang, "Extract", "Extraction", "استخراج")
    return (
        f'<div class="hpipe run" data-hp data-active="blog">'
        f'<div class="hp-tabs" role="tablist" aria-label="{T(lang, "Pick a source", "Choisissez une source", "اختر مصدرا")}">{tabs}</div>'
        f'<div class="hp-stage" id="hp-panel" role="tabpanel" aria-labelledby="hp-blog">'
        f'<div class="hp-col-a">{srcs}{pull_html}</div>'
        f'<div class="hp-beam" aria-hidden="true"><span class="hp-beam-l">{beam_label}</span>{kit.beam()}</div>'
        f'<div class="hp-col-b">{tile_html}</div>'
        f"{ans}</div></div>"
    )


def collapse(lang):
    q = T(lang, "best way to reduce supplier risk", "meilleure façon de réduire le risque fournisseur", "أفضل طريقة لتقليل مخاطر الموردين")
    domains = ["industry-report.com", "competitor.com", "vendor-blog.com", kit.BRAND, "news-site.com", "forum-thread.com", "directory.com", "another-vendor.com", "review-site.com", "old-guide.com"]
    rows = "".join(
        f'<li class="hc-row{" is-you" if d == kit.BRAND else ""}" style="--r:{n}"><span class="hc-n">{n + 1}</span><span class="hc-t"><b dir="ltr">{d}</b><i style="--w:{w}%"></i></span></li>'
        for n, (d, w) in enumerate(zip(domains, [90, 76, 84, 70, 88, 64, 80, 72, 86, 60]))
    )
    a1 = T(lang, "Ten links. The buyer clicks, compares, decides.", "Dix liens. L'acheteur clique, compare, décide.", "عشرة روابط. المشتري ينقر ويقارن ويقرر.")
    a2 = T(lang, "One answer. Only the cited sources get seen.", "Une réponse. Seules les sources citées sont vues.", "إجابة واحدة. لا تظهر إلا المصادر المستشهد بها.")
    ans_lines = [
        T(lang, "Spreadsheet audits miss most risk events because the data goes stale between reviews.", "Les audits sur tableur ratent la plupart des incidents, car les données vieillissent entre deux revues.", "مراجعات جداول البيانات تفوّت معظم الحوادث لأن البيانات تتقادم بين مراجعة وأخرى."),
        T(lang, "Continuous monitoring tracks supplier data as it changes and flags issues early.", "Le suivi continu met à jour les données fournisseurs et signale les problèmes tôt.", "المراقبة المستمرة تحدّث بيانات الموردين وتنبه إلى المشكلات مبكرا."),
    ]
    return (
        '<div class="hc" data-scrub>'
        f'<div class="hc-search"><div class="hc-head"><span class="hc-k">{T(lang, "Classic search", "Recherche classique", "البحث التقليدي")}</span></div>'
        f'<p class="hc-q">{icon("search")}<span>{q}</span></p><div class="hc-stack"><ol class="hc-list">{rows}</ol><span class="hc-badge" aria-hidden="true">{T(lang, "10 links", "10 liens", "10 روابط")}</span></div><p class="hc-cap">{a1}</p></div>'
        f'<div class="hc-arrow" aria-hidden="true">{icon("arrow", "flip")}</div>'
        f'<div class="hc-ai"><div class="hc-head"><span class="hc-k">{T(lang, "AI answer", "Réponse IA", "إجابة الذكاء الاصطناعي")}</span>{label(kit.EXAMPLE[lang])}</div>'
        f'<div class="vx-answer hc-card"><p class="vx-ans-q">{icon("search")}<span>{q}</span></p>'
        f'<div class="vx-ans-b"><p class="vx-ans-p" data-type="500">{ans_lines[0]}</p><p class="vx-ans-p">{ans_lines[1]}</p></div>'
        f'<div class="vx-ans-s"><span class="vx-src" dir="ltr">industry-report.com</span>{cite(kit.BRAND, "is-hl")}<span class="vx-src" dir="ltr">vendor-blog.com</span></div></div>'
        f'<p class="hc-cap">{a2}</p></div></div>'
    )


def month(lang):
    days = T(lang, "Mon Tue Wed Thu Fri Sat Sun", "Lun Mar Mer Jeu Ven Sam Dim", "إثنين ثلاثاء أربعاء خميس جمعة سبت أحد").split()
    art = T(lang, "Article", "Article", "مقال")
    arts = [T(lang, "Pillar", "Pilier", "محوري"), T(lang, "Comparison", "Comparatif", "مقارنة"), T(lang, "FAQ page", "Page FAQ", "أسئلة شائعة"), T(lang, "Opinion", "Opinion", "رأي")]
    news = T(lang, "Newsletter", "Newsletter", "نشرة")
    post = T(lang, "Post", "Post", "منشور")
    plan = {
        (0, 0): ("node", "doc", T(lang, "Source in", "Source reçue", "وصول المصدر")),
        (0, 2): ("work", "search", T(lang, "Extract", "Extraction", "استخراج")),
        (0, 3): ("work", "pen", T(lang, "Produce", "Production", "إنتاج")),
        (0, 4): ("node", "stamp", T(lang, "Delivered", "Livré", "التسليم")),
    }
    for w in range(1, 5):
        plan[(w, 1)] = ("art", "doc", arts[w - 1])
        plan[(w, 3)] = ("news", "mail", news)
        for d in (0, 2, 4):
            plan[(w, d)] = ("post", "linkedin", post)
    plan[(4, 5)] = ("node", "gauge", T(lang, "Citation check", "Vérif. citations", "فحص الاستشهادات"))
    order = sorted(plan)
    head = "".join(f'<span class="hm-dh">{d}</span>' for d in days)
    cells = []
    for w in range(5):
        for d in range(7):
            item = plan.get((w, d))
            wk = f'<span class="hm-n">{T(lang, "Week", "Sem.", "الأسبوع")} {w + 1}</span>' if d == 0 else ""
            weekend = " is-we" if d >= 5 else ""
            if item:
                kind, ic, txt = item
                t = 0.12 + order.index((w, d)) / len(order) * 0.5
                cells.append(f'<div class="hm-c{weekend}">{wk}<span class="hm-a hm-{kind}" style="--t:{t:.3f}">{icon(ic)}<b>{txt}</b></span></div>')
            else:
                cells.append(f'<div class="hm-c{weekend}">{wk}</div>')
    count = sum(1 for v in plan.values() if v[0] in ("art", "news", "post"))
    legend = (
        f'<ul class="hm-legend"><li><i class="hm-art"></i>4 {T(lang, "articles", "articles", "مقالات")}</li><li><i class="hm-news"></i>4 {T(lang, "newsletter versions", "versions newsletter", "نسخ من النشرة")}</li>'
        f'<li><i class="hm-post"></i>{count - 8} {T(lang, "social posts", "posts sociaux", "منشورا اجتماعيا")}</li></ul>'
    )
    return (
        '<div class="hm" data-scrub>'
        f'<div class="hm-top"><div><span class="hm-plan">SWARM</span><b class="hm-total"><span>{count}</span> {T(lang, "assets from one source", "contenus issus d'une source", "محتوى من مصدر واحد")}</b></div>{label(T(lang, "Example schedule", "Calendrier d'exemple", "جدول توضيحي"))}</div>'
        f'<div class="hm-grid" role="img" aria-label="{T(lang, "Example month on the SWARM plan: the source arrives on day 1, assets are delivered on day 5, then four articles, four newsletter versions and fourteen social posts are published over the following weeks, and the citation check runs at the end of the month.", "Exemple de mois avec l’offre SWARM : la source arrive le jour 1, les contenus sont livrés le jour 5, puis quatre articles, quatre versions de newsletter et quatorze posts sociaux sont publiés les semaines suivantes, et la vérification des citations a lieu en fin de mois.", "مثال لشهر على باقة SWARM: يصل المصدر في اليوم الأول، وتُسلَّم المحتويات في اليوم الخامس، ثم تُنشر أربعة مقالات وأربع نسخ من النشرة وأربعة عشر منشورا اجتماعيا خلال الأسابيع التالية، ويجري فحص الاستشهادات في آخر الشهر.")}">{head}{"".join(cells)}</div>'
        f'<div class="hm-foot">{legend}<span class="hm-bar"><i></i></span></div></div>'
    )


def tracking(lang):
    qs = [
        T(lang, "Best supplier risk software for mid-size manufacturers", "Meilleur logiciel de risque fournisseur pour une ETI", "أفضل برنامج لمخاطر الموردين لشركة متوسطة"),
        T(lang, "How to monitor supplier risk continuously", "Comment suivre le risque fournisseur en continu", "كيف تراقب مخاطر الموردين باستمرار"),
        T(lang, "Spreadsheet vs dedicated tool for supplier audits", "Tableur ou outil dédié pour les audits fournisseurs", "جداول البيانات أم أداة مخصصة لتدقيق الموردين"),
        T(lang, "What is a supplier risk score", "Qu'est-ce qu'un score de risque fournisseur", "ما هو مؤشر مخاطر المورد"),
        T(lang, "How often should suppliers be reviewed", "À quelle fréquence revoir ses fournisseurs", "كم مرة يجب مراجعة الموردين"),
        T(lang, "Supplier risk tools that connect to an ERP", "Outils de risque fournisseur connectés à un ERP", "أدوات مخاطر الموردين المتصلة بنظام ERP"),
        T(lang, "Early signs a supplier is in trouble", "Signes qu'un fournisseur est en difficulté", "علامات مبكرة على تعثر مورد"),
        T(lang, "How to write a supplier risk policy", "Rédiger une politique de risque fournisseur", "كيف تكتب سياسة لمخاطر الموردين"),
        T(lang, "Cost of supplier risk software", "Coût d'un logiciel de risque fournisseur", "تكلفة برامج مخاطر الموردين"),
        T(lang, "Alternatives to annual supplier audits", "Alternatives à l'audit fournisseur annuel", "بدائل التدقيق السنوي للموردين"),
    ]
    engines = ["ChatGPT", "Perplexity", "Gemini", "AI Overviews"]
    pattern = [
        [1, 1, 0, 1], [0, 1, 0, 0], [1, 0, 1, 1], [0, 0, 0, 1], [1, 1, 0, 0],
        [0, 1, 1, 0], [0, 0, 0, 0], [1, 0, 0, 1], [0, 1, 0, 0], [1, 1, 1, 0],
    ]
    head = '<span class="ht-q ht-h">' + T(lang, "Buyer question", "Question d'acheteur", "سؤال المشتري") + "</span>" + "".join(f'<span class="ht-h ht-e" dir="ltr">{e}</span>' for e in engines)
    rows = []
    for i, cells in enumerate(pattern):
        qtext = qs[i]
        rows.append(f'<span class="ht-q" style="--i:{i}"><b>{i + 1:02d}</b>{qtext}</span>' + "".join(
            f'<span class="ht-c{" is-cited" if c else ""}" style="--i:{i}"><i>{icon("check") if c else ""}</i></span>' for c in cells
        ))
    cited = sum(sum(r) for r in pattern)
    total = len(pattern) * len(engines)
    return (
        '<div class="ht">'
        f'<div class="ht-top"><b>{T(lang, "Monthly citation check", "Vérification mensuelle des citations", "الفحص الشهري للاستشهادات")}</b>{label(kit.ILLUSTRATIVE[lang])}</div>'
        f'<div class="ht-grid">{head}{"".join(rows)}<i class="ht-scan" aria-hidden="true"></i></div>'
        f'<div class="ht-foot"><span><b>{cited}/{total}</b> {T(lang, "answers cite yourbrand.com in this illustration", "réponses citent yourbrand.com dans cette illustration", "إجابة تستشهد بـ yourbrand.com في هذا المثال")}</span>'
        f'<span class="ht-key"><i class="is-cited"></i>{T(lang, "cited", "cité", "مستشهد به")}</span></div></div>'
    )


VISUALS = {"home-pipeline": pipeline, "home-collapse": collapse, "home-month": month, "home-tracking": tracking}
