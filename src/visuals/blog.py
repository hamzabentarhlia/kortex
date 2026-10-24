import art

from .kit import T, icon, label, cite, chip, stamp, answer, gauge, beam, EXAMPLE, ILLUSTRATIVE, BRAND

SLUGS = [
    "stop-ranking-start-dominating",
    "entity-first-content-architecture",
    "one-video-authority-system",
    "content-audit-ai-retrieval",
    "answer-engine-visibility-guide",
    "new-b2b-content-stack",
    "category-creation-ai-search",
    "b2b-linkedin-content-dies",
]

SIMPLIFIED = {"en": "Simplified model", "fr": "Modèle simplifié", "ar": "نموذج مبسط"}


def blog_hero(lang):
    cols = []
    for c in range(4):
        cells = "".join(f'<div class="blog-h-t">{art.cover_svg("blog/" + SLUGS[(c * 2 + k) % 8], "blog-h-c")}</div>' for k in range(3))
        cols.append(f'<div class="blog-h-col" style="--k:{c}">{cells}</div>')
    return f'<div class="blog-mosaic" aria-hidden="true"><div class="blog-h-grid">{"".join(cols)}</div></div>'


def fig(name, kicker, inner, cap, tag=""):
    lab = label(tag) if tag else ""
    return (
        f'<figure class="blog-fig blog-f-{name}"><div class="blog-h"><span class="blog-k">{kicker}</span>{lab}</div>'
        f'<div class="blog-s">{inner}</div><figcaption>{cap}</figcaption></figure>'
    )


def ic(name, cls="blog-i"):
    return f'<span class="{cls}">{icon(name)}</span>'


def sk(*widths):
    return '<span class="blog-sk">' + "".join(f'<i style="--w:{w}%"></i>' for w in widths) + "</span>"


def con(cls=""):
    return f'<div class="blog-con {cls}" aria-hidden="true">{beam()}{icon("arrow")}</div>'


def rank_vs_cite(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    rows = ""
    for i in range(1, 7):
        hl = i == 4
        dom = f'<span class="blog-dom" dir="ltr">{BRAND}</span>' if hl else sk(70 - i * 4, 46 + i * 3)
        rows += f'<div class="blog-rr st{" is-hl" if hl else ""}" style="--i:{i}"><b class="blog-n">{i}</b>{dom}</div>'
    left = (
        f'<div class="blog-panel"><span class="blog-pt">{ic("search")}{t("Search results", "Résultats de recherche", "نتائج البحث")}</span>'
        f'<div class="blog-rl">{rows}</div><p class="blog-note">{t("Position 4 still earns a few clicks.", "En position 4, quelques clics restent possibles.", "في المرتبة الرابعة ما زالت بعض النقرات ممكنة.")}</p></div>'
    )
    ans = answer(
        t("What is the best approach to B2B content operations?", "Quelle est la meilleure approche des opérations de contenu B2B ?", "ما أفضل طريقة لإدارة محتوى B2B؟"),
        [94, 82, 88, 56],
        [("industry-report.com", False), (BRAND, True), ("vendor-blog.com", False)],
        "Perplexity",
    )
    right = (
        f'<div class="blog-panel is-hot"><span class="blog-pt">{ic("chat")}{t("AI answer", "Réponse IA", "إجابة الذكاء الاصطناعي")}</span>'
        f'<div class="pop" style="--i:3">{ans}</div><p class="blog-note">{t("A few named sources. You are one of them, or absent.", "Quelques sources nommées. Vous en faites partie, ou vous êtes absent.", "مصادر قليلة مسماة: إما أن تكون منها، وإما أن تغيب.")}</p></div>'
    )
    inner = f'<div class="blog-vs">{left}<span class="blog-vs-m" aria-hidden="true">vs</span>{right}</div>'
    return fig(
        "rank",
        t("Ranking against being cited", "Être classé ou être cité", "الترتيب مقابل الاستشهاد"),
        inner,
        t(
            "A results page has ten places. An answer names a few sources, and there is no position four to fall back on.",
            "Une page de résultats offre dix places. Une réponse cite quelques sources, sans quatrième position de repli.",
            "تتسع صفحة النتائج لعشرة روابط، أما الإجابة فتذكر مصادر قليلة، ولا توجد مرتبة رابعة تحتمي بها.",
        ),
        EXAMPLE[lang],
    )


def cited_vs_synth(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    lanes = [
        (
            False,
            t("Hard to cite", "Difficile à citer", "يصعب اقتباسه"),
            t("“Content is more important than ever. Many companies wonder how AI will change marketing.”",
              "« Le contenu n'a jamais été aussi important. Beaucoup d'entreprises se demandent comment l'IA va changer le marketing. »",
              "«لم يكن المحتوى أهم مما هو اليوم، وتتساءل شركات كثيرة كيف سيغير الذكاء الاصطناعي التسويق.»"),
            [("industry-report.com", False), ("vendor-blog.com", False)],
            t("Synthesized around: the idea is used, your name is not.", "Synthétisé : l'idée est reprise, votre nom disparaît.", "إعادة صياغة: تُستعمل الفكرة ويغيب اسمك."),
        ),
        (
            True,
            t("Easy to cite", "Facile à citer", "يسهل اقتباسه"),
            t("“Source extraction turns one founder video into a linked set of answer pages that AI engines can quote.”",
              "« L'extraction de source transforme une vidéo de fondateur en un ensemble lié de pages de réponse que les moteurs IA peuvent citer. »",
              "«استخراج المصدر طريقة تحوّل فيديو واحدا للمؤسس إلى مجموعة مترابطة من صفحات الإجابة تستطيع محركات الإجابة اقتباسها.»"),
            [(BRAND, True)],
            t("Cited: the claim travels with your name.", "Cité : l'affirmation arrive avec votre nom.", "استشهاد: تنتقل الفكرة ومعها اسمك."),
        ),
    ]
    out = ""
    for i, (good, tag, quote, srcs, res) in enumerate(lanes):
        cls = " is-hl" if good else ""
        srcs_html = "".join(cite(d, "is-hl") if h else f'<span class="vx-src" dir="ltr">{d}</span>' for d, h in srcs)
        out += (
            f'<div class="blog-lane{cls}">'
            f'<div class="blog-page st" style="--i:{i * 3}"><span class="blog-tag">{tag}</span><p>{quote}</p></div>'
            f"{con('is-hot' if good else '')}"
            f'<div class="blog-out st" style="--i:{i * 3 + 1}"><span class="blog-ans">{sk(92, 74, 84)}<span class="blog-srcs">{srcs_html}</span></span>'
            f'<p class="blog-res">{ic("check" if good else "x", "blog-ri")}{res}</p></div></div>'
        )
    return fig(
        "lanes",
        t("Cited or synthesized around", "Cité ou simplement repris", "استشهاد أم إعادة صياغة"),
        f'<div class="blog-lanes">{out}</div>',
        t(
            "Both pages carry the same idea. Only the one with a named entity and a quotable claim gets your name into the answer.",
            "Les deux pages portent la même idée. Seule celle qui nomme une entité et formule une affirmation citable fait entrer votre nom dans la réponse.",
            "تحمل الصفحتان الفكرة نفسها، لكن الصفحة التي تسمي كيانا وتقدم جملة قابلة للاقتباس هي وحدها التي تُدخل اسمك في الإجابة.",
        ),
        EXAMPLE[lang],
    )


def three_tests(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    gates = [
        ("search", t("Extractable", "Extractible", "قابل للاقتطاف"),
         t("Is there a clean answer near the top?", "Une réponse nette apparaît-elle en haut de page ?", "هل توجد إجابة واضحة في أعلى الصفحة؟"),
         t("Fails: the page is bypassed", "Échec : la page est ignorée", "الإخفاق: تُتجاوز الصفحة")),
        ("tag", t("Attributable", "Attribuable", "قابل للنسبة"),
         t("Is it tied to a clearly named company or method?", "Est-elle liée à une entreprise ou une méthode clairement nommée ?", "هل ترتبط بشركة أو منهج مسمى بوضوح؟"),
         t("Fails: the idea is used without your name", "Échec : l'idée est reprise sans votre nom", "الإخفاق: تُستعمل الفكرة دون اسمك")),
        ("layers", t("Corroborated", "Corroborée", "مؤكَّد"),
         t("Do related pages say the same thing in the same words?", "D'autres pages disent-elles la même chose, avec les mêmes mots ?", "هل تقول صفحات أخرى الشيء نفسه بالكلمات نفسها؟"),
         t("Fails: one isolated data point", "Échec : un signal isolé", "الإخفاق: إشارة واحدة معزولة")),
    ]
    out = ""
    for i, (icn, name, q, fail) in enumerate(gates):
        out += (
            f'<div class="blog-gate st" style="--i:{i * 2}"><span class="blog-gn">{i + 1}</span>{ic(icn)}<b>{name}</b><p>{q}</p>'
            f'<span class="blog-fail">{icon("x")}{fail}</span></div>{con()}'
        )
    out += f'<div class="blog-win pop" style="--i:7">{cite(BRAND, "is-hl")}<b>{t("Cited", "Cité", "مستشهد به")}</b></div>'
    return fig(
        "gates",
        t("Three tests before a citation", "Trois tests avant une citation", "ثلاثة اختبارات قبل الاستشهاد"),
        f'<div class="blog-gates">{out}</div>',
        t(
            "An engine cites a page only when all three tests pass. Each failure has its own symptom.",
            "Un moteur ne cite une page que si les trois tests passent. Chaque échec a son propre symptôme.",
            "لا يستشهد المحرك بصفحة إلا إذا اجتازت الاختبارات الثلاثة، ولكل إخفاق عرَض خاص به.",
        ),
    )


def four_layers(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    layers = [
        (t("Entity declaration", "Déclaration d'entité", "إعلان الكيان"),
         [t("Organization schema", "Schéma Organization", "ترميز Organization"), t("“What we do” sentence", "Phrase « ce que nous faisons »", "جملة «ماذا نفعل»")]),
        (t("Pillar layer", "Couche pilier", "طبقة المقالات المحورية"),
         [t("Pillar", "Pilier", "مقال محوري"), t("Contrarian", "À contre-courant", "مقال رأي"), t("Comparison", "Comparatif", "صفحة مقارنة")]),
        (t("Retrieval layer", "Couche de récupération", "طبقة الاسترجاع"),
         [t("FAQ cluster", "Grappe de FAQ", "أسئلة شائعة"), t("Definitions", "Définitions", "تعريفات"), t("Tables", "Tableaux", "جداول")]),
        (t("Distribution layer", "Couche de diffusion", "طبقة التوزيع"),
         ["LinkedIn", t("Newsletter", "Newsletter", "نشرة بريدية"), t("Outreach", "Prospection", "تواصل مباشر")]),
    ]
    rings = "".join(f'<i class="blog-ring st" style="--i:{3 - k};--r:{k}"></i>' for k in range(4))
    core = f'<div class="blog-rings" aria-hidden="true">{rings}<span class="blog-core">{icon("building")}</span></div>'
    rows = ""
    for k, (name, items) in enumerate(layers):
        pills = "".join(f'<span class="blog-pill">{x}</span>' for x in items)
        rows += f'<div class="blog-ly st" style="--i:{k + 1}"><span class="blog-gn">{k + 1}</span><b>{name}</b><span class="blog-pills">{pills}</span></div>'
    return fig(
        "layers",
        t("Four layers around one entity", "Quatre couches autour d'une entité", "أربع طبقات حول كيان واحد"),
        f'<div class="blog-lay">{core}<div class="blog-lys">{rows}</div></div>',
        t(
            "Each layer rests on the one inside it. Distribution spreads the vocabulary that the inner layers answer.",
            "Chaque couche repose sur celle qu'elle entoure. La diffusion répand le vocabulaire auquel répondent les couches intérieures.",
            "كل طبقة تستند إلى الطبقة التي بداخلها، والتوزيع ينشر المفردات التي تجيب عنها الطبقات الداخلية.",
        ),
    )


def signal_levels(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    term = t("source extraction", "extraction de source", "استخراج المصدر")
    lv = [
        (3, t("Framing alignment", "Alignement du cadrage", "توافق الطرح"),
         t("The answer describes the problem the way your pages frame it, in other words.", "La réponse décrit le problème comme vos pages le cadrent, avec d'autres mots.", "تصف الإجابة المشكلة كما تطرحها صفحاتك، ولكن بكلمات أخرى."),
         "", 34),
        (2, t("Terminology adoption", "Adoption de la terminologie", "تبني المصطلحات"),
         t(f"The answer uses your term, <mark>{term}</mark>, without naming you.", f"La réponse emploie votre terme, <mark>{term}</mark>, sans vous nommer.", f"تستعمل الإجابة مصطلحك، <mark>{term}</mark>، دون أن تذكر اسمك."),
         "", 66),
        (1, t("Named citation", "Citation nommée", "استشهاد بالاسم"),
         t("The answer names your company and links your page.", "La réponse nomme votre entreprise et renvoie vers votre page.", "تذكر الإجابة اسم شركتك وتحيل إلى صفحتك."),
         cite(BRAND, "is-hl"), 100),
    ]
    out = ""
    for k, (n, name, txt, extra, w) in enumerate(lv):
        out += (
            f'<div class="blog-lv st{" is-hl" if n == 1 else ""}" style="--i:{k}"><div class="blog-lv-h"><span class="blog-gn">{n}</span><b>{name}</b>'
            f'<span class="blog-meter"><i style="--s:{w / 100}"></i></span></div><p class="vx-ans-p">{txt}</p>{extra}</div>'
        )
    return fig(
        "levels",
        t("Three signal levels", "Trois niveaux de signal", "ثلاثة مستويات للإشارة"),
        f'<div class="blog-lvs">{out}</div>',
        t(
            "Track all three each month. Framing and terminology usually show up before your name does.",
            "Suivez les trois chaque mois. Le cadrage et la terminologie apparaissent souvent avant votre nom.",
            "تابع المستويات الثلاثة كل شهر، فالطرح والمصطلحات يظهران عادة قبل اسمك.",
        ),
        EXAMPLE[lang],
    )


def feed_decay(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    svg = (
        '<svg class="blog-chart" viewBox="0 0 600 220" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
        '<path class="blog-grid" d="M0 200H600M0 140H600M0 80H600M0 20H600"/>'
        '<path class="blog-spk" d="M0 198C30 198 40 22 62 22S92 190 140 196S320 199 600 199"/>'
        '<path class="blog-lng" d="M0 198C60 192 90 150 160 132S330 92 600 70"/>'
        '<path class="blog-lng-f" d="M0 198C60 192 90 150 160 132S330 92 600 70V200H0z"/>'
        "</svg>"
    )
    ticks = "".join(f'<span style="--x:{x}%">{s}</span>' for x, s in [(0, t("Post", "Post", "النشر")), (10, "48 h"), (50, t("30 days", "30 jours", "30 يوما")), (96, t("90 days", "90 jours", "90 يوما"))])
    legend = (
        f'<div class="blog-leg"><span class="blog-lg">{ic("linkedin")}<i class="is-spk"></i>{t("Standalone post", "Post isolé", "منشور منفرد")}</span>'
        f'<span class="blog-lg is-hl">{ic("doc")}<i class="is-lng"></i>{t("Post that routes to an answer page", "Post qui renvoie vers une page de réponse", "منشور يحيل إلى صفحة إجابة")}</span></div>'
    )
    marks = (
        f'<span class="blog-pin is-a" style="--x:10%;--y:8%">{t("Feed moves on", "Le fil passe à autre chose", "تنتقل الخلاصة إلى غيره")}</span>'
        f'<span class="blog-pin is-b" style="--x:66%;--y:30%">{t("The page keeps answering", "La page continue de répondre", "الصفحة تواصل الإجابة")}</span>'
    )
    inner = f'{legend}<div class="blog-plot"><div class="blog-cv">{svg}{marks}</div><div class="blog-ticks" aria-hidden="true">{ticks}</div></div>'
    return fig(
        "decay",
        t("Attention over time", "L'attention dans le temps", "الانتباه عبر الزمن"),
        inner,
        t(
            "A feed post peaks within hours and fades in about two days. When it points to a page, the page keeps working long after.",
            "Un post culmine en quelques heures et s'éteint en deux jours environ. S'il renvoie vers une page, la page continue de travailler longtemps après.",
            "يبلغ المنشور ذروته خلال ساعات ويخبو في نحو يومين. وحين يحيل إلى صفحة، تواصل الصفحة عملها بعده بوقت طويل.",
        ),
        ILLUSTRATIVE[lang],
    )


def post_loop(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    pillar = t("Pillar", "Pilier", "المقال المحوري")
    steps = [
        ("1", "doc", t("Pillar article", "Article pilier", "مقال محوري"), t("Retrieval anchor", "Ancre de récupération", "مرساة الاسترجاع"), True),
        ("2–3", "linkedin", t("Hook post", "Post d'accroche", "منشور الافتتاح"), "→ " + pillar, False),
        ("5", "linkedin", t("Mechanism post", "Post mécanisme", "منشور المنهج"), t("No link", "Sans lien", "دون رابط"), False),
        ("8", "linkedin", t("Contrarian post", "Post à contre-courant", "منشور مخالف"), "→ " + pillar, False),
        ("12", "linkedin", t("Decision post", "Post de décision", "منشور القرار"), "→ " + t("Comparison", "Comparatif", "صفحة المقارنة"), False),
        ("16–20", "linkedin", t("Illustration post", "Post illustration", "منشور توضيحي"), "→ " + t("Contact", "Contact", "صفحة التواصل"), False),
        ("25–30", "question", t("FAQ cluster", "Grappe de FAQ", "أسئلة شائعة"), t("Feeds retrieval", "Nourrit la récupération", "يغذي الاسترجاع"), True),
    ]
    day = t("Day", "Jour", "اليوم")
    out = ""
    for i, (d, icn, name, to, hl) in enumerate(steps):
        out += (
            f'<div class="blog-day st{" is-hl" if hl else ""}" style="--i:{i}"><span class="blog-dn">{day} <b dir="ltr">{d}</b></span>'
            f'{ic(icn)}<b class="blog-dt">{name}</b><span class="blog-to">{to}</span></div>'
        )
    return fig(
        "loop",
        t("One source, 30 days, one destination", "Une source, 30 jours, une destination", "مصدر واحد، 30 يوما، وجهة واحدة"),
        f'<div class="blog-days"><i class="blog-track" aria-hidden="true"></i>{out}</div>',
        t(
            "The pillar goes live first. Every post after it routes back to a page that already exists.",
            "Le pilier est publié en premier. Chaque post suivant renvoie vers une page qui existe déjà.",
            "يُنشر المقال المحوري أولا، ثم يحيل كل منشور بعده إلى صفحة موجودة بالفعل.",
        ),
    )


def category_def(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    parts = [
        ("target", t("Named problem", "Problème nommé", "مشكلة مسماة"), t("A specific failure, not an industry challenge", "Un échec précis, pas un défi de secteur", "إخفاق محدد، لا تحدٍّ عام في القطاع")),
        ("layers", t("Named mechanism", "Mécanisme nommé", "منهج مسمى"), t("Your way of solving it, one stable name", "Votre façon de le résoudre, un nom stable", "طريقتك في الحل، باسم ثابت")),
        ("x", t("Named alternative", "Alternative nommée", "بديل مرفوض"), t("What buyers do today, and why it fails", "Ce que font les acheteurs, et pourquoi ça échoue", "ما يفعله المشترون اليوم، ولماذا يفشل")),
        ("user", t("Named audience", "Audience nommée", "جمهور محدد"), t("Who it is for, and who it is not for", "Pour qui, et pour qui ce n'est pas", "لمن هو، ولمن ليس")),
    ]
    tiles = "".join(f'<div class="blog-part st" style="--i:{i}">{ic(a)}<b>{n}</b><small>{s}</small></div>' for i, (a, n, s) in enumerate(parts))
    firms = lambda lit: "".join(f'<span class="blog-firm{" is-on" if k in lit else ""}{" is-you" if k == 2 else ""}">{icon("building")}</span>' for k in range(5))
    tests = (
        f'<div class="blog-test st" style="--i:5"><span class="blog-tag">{t("Two parts or fewer", "Deux éléments ou moins", "عنصران أو أقل")}</span><span class="blog-firms">{firms({0, 1, 2, 3, 4})}</span>'
        f'<p>{t("Fits five companies: nobody owns it", "Convient à cinq entreprises : personne ne la possède", "ينطبق على خمس شركات: لا يملكه أحد")}</p></div>'
        f'<div class="blog-test is-hl st" style="--i:6"><span class="blog-tag">{t("All four parts", "Les quatre éléments", "العناصر الأربعة")}</span><span class="blog-firms">{firms({2})}</span>'
        f'<p>{t("Fits only you: a definition engines can attribute", "Ne correspond qu’à vous : une définition attribuable", "ينطبق عليك وحدك: تعريف يمكن نسبته إليك")}</p></div>'
    )
    return fig(
        "cat",
        t("The four parts of a category", "Les quatre éléments d'une catégorie", "العناصر الأربعة للفئة"),
        f'<div class="blog-cat"><div class="blog-parts">{tiles}</div>{con("is-hot")}<div class="blog-tests">{tests}</div></div>',
        t(
            "If your definition could describe five companies, it is not precise enough to be cited as yours.",
            "Si votre définition peut décrire cinq entreprises, elle n'est pas assez précise pour vous être attribuée.",
            "إذا كان تعريفك يصلح لوصف خمس شركات، فهو ليس دقيقا بما يكفي ليُنسب إليك.",
        ),
    )


def category_phases(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    ph = [
        ("pen", t("Define", "Définir", "التعريف"), t("Entity structure document: name, definition, canon, banned synonyms", "Document de structure d'entité : nom, définition, canon, synonymes interdits", "وثيقة بنية الكيان: الاسم والتعريف والمصطلحات المعتمدة والمرادفات الممنوعة"),
         [t("Canon", "Canon", "المصطلحات")]),
        ("grid", t("Build the footprint", "Construire l'empreinte", "بناء الحضور"), t("Four linked assets, live before any promotion", "Quatre contenus liés, en ligne avant toute promotion", "أربعة أصول مترابطة تُنشر قبل أي ترويج"),
         [t("Pillar", "Pilier", "محوري"), t("Contrarian", "Contre-courant", "رأي"), t("Comparison", "Comparatif", "مقارنة"), "FAQ"]),
        ("send", t("Distribute", "Diffuser", "التوزيع"), t("The same definition from five angles", "La même définition sous cinq angles", "التعريف نفسه من خمس زوايا"),
         [t("Hook", "Accroche", "افتتاح"), t("Mechanism", "Mécanisme", "منهج"), t("Contrarian", "Contre-courant", "مخالف"), t("Decision", "Décision", "قرار"), t("Scenario", "Scénario", "سيناريو")]),
        ("node", t("Deepen", "Approfondir", "التعميق"), t("Each new source cycle adds to the same graph", "Chaque nouveau cycle enrichit le même graphe", "كل دورة مصدر جديدة تضيف إلى الشبكة نفسها"),
         [t("Cycle 1", "Cycle 1", "الدورة 1"), t("Cycle 2", "Cycle 2", "الدورة 2"), t("Cycle 3", "Cycle 3", "الدورة 3")]),
    ]
    out = ""
    for i, (a, name, sub, pills) in enumerate(ph):
        p = "".join(f'<span class="blog-pill">{x}</span>' for x in pills)
        out += f'<div class="blog-ph st{" is-hl" if i == 1 else ""}" style="--i:{i}"><span class="blog-gn">{i + 1}</span>{ic(a)}<b>{name}</b><p>{sub}</p><span class="blog-pills">{p}</span></div>'
    return fig(
        "phases",
        t("The four-phase playbook", "La méthode en quatre phases", "المنهج في أربع مراحل"),
        f'<div class="blog-phs"><i class="blog-track" aria-hidden="true"></i>{out}</div>',
        t(
            "The phases run in order. Skipping one leaves the next with nothing to link back to.",
            "Les phases se suivent dans l'ordre. En sauter une prive la suivante de point d'appui.",
            "تسير المراحل بالترتيب، وتخطي إحداها يترك التالية بلا أساس تحيل إليه.",
        ),
    )


def audit_score(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    crit = [
        (t("Answer-first opening", "Ouverture qui répond d'abord", "افتتاح بالإجابة"), 1, t("Claim appears in section two", "L'affirmation arrive en section deux", "الفكرة تظهر في القسم الثاني")),
        (t("Canonical entity terms", "Termes d'entité canoniques", "مصطلحات الكيان المعتمدة"), 2, ""),
        (t("Structured answer blocks", "Blocs de réponse structurés", "كتل إجابة منظمة"), 1, t("No FAQ yet", "Pas encore de FAQ", "لا أسئلة شائعة بعد")),
        (t("Article + FAQPage schema", "Schéma Article + FAQPage", "ترميز Article وFAQPage"), 1, t("FAQPage missing", "FAQPage absent", "FAQPage غائب")),
        (t("Descriptive internal links", "Liens internes descriptifs", "روابط داخلية وصفية"), 1, t("Generic anchors", "Ancres génériques", "نصوص روابط عامة")),
    ]
    rows = ""
    for i, (name, sc, note) in enumerate(crit):
        dots = "".join(f'<i class="{"is-on" if k < sc else ""}"></i>' for k in range(2))
        n = f'<small>{note}</small>' if note else ""
        rows += f'<div class="blog-cr st" style="--i:{i}"><span class="blog-gn">{i + 1}</span><span class="blog-crt"><b>{name}</b>{n}</span><span class="blog-dots">{dots}</span><b class="blog-sc" dir="ltr">{sc}/2</b></div>'
    side = (
        f'<div class="blog-verdict pop" style="--i:6">{gauge(6, 10, t("GEO readiness", "Lisibilité GEO", "الجاهزية لـ GEO"), unit="/10")}'
        f'<span class="blog-band">{t("Retrofit", "À reprendre", "يحتاج إلى تعديل")} <b dir="ltr">4–7</b></span></div>'
    )
    head = f'<div class="blog-url">{icon("doc")}<span dir="ltr">{BRAND}/blog/content-operations</span></div>'
    return fig(
        "score",
        t("Scoring one page", "Noter une page", "تقييم صفحة واحدة"),
        f'<div class="blog-score"><div class="blog-sheet">{head}{rows}</div>{side}</div>',
        t(
            "Five criteria, 0 to 2 points each. The failure notes become the retrofit instructions.",
            "Cinq critères, de 0 à 2 points chacun. Les notes d'échec deviennent les consignes de reprise.",
            "خمسة معايير، لكل منها من 0 إلى 2. وتتحول ملاحظات الإخفاق إلى تعليمات التعديل.",
        ),
        EXAMPLE[lang],
    )


def audit_sort(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    bins = [
        ("ok", t("Keep", "Garder", "الإبقاء"), "8–10", t("Quarterly maintenance", "Maintenance trimestrielle", "صيانة كل ثلاثة أشهر"), [9, 8]),
        ("mid", t("Retrofit", "Reprendre", "التعديل"), "4–7", t("First, in traffic order", "En premier, par ordre de trafic", "أولا، حسب الزيارات"), [7, 6, 5, 4]),
        ("low", t("Retire or rebuild", "Retirer ou reconstruire", "الحذف أو إعادة البناء"), "0–3", t("Merge, then 301 redirect", "Fusionner, puis redirection 301", "الدمج ثم تحويل 301"), [3, 1]),
    ]
    out = ""
    for i, (tone, name, rng, sub, pages) in enumerate(bins):
        pg = "".join(f'<span class="blog-pg pop" style="--i:{i * 3 + k}">{icon("doc")}<b dir="ltr">{s}</b></span>' for k, s in enumerate(pages))
        out += f'<div class="blog-bin is-{tone} st" style="--i:{i}"><div class="blog-bin-h"><i></i><b>{name}</b><span dir="ltr">{rng}</span></div><div class="blog-pgs">{pg}</div><p>{sub}</p></div>'
    order = [
        t("Missing pillars", "Piliers manquants", "المقالات المحورية الناقصة"),
        t("High-traffic retrofits", "Reprises à fort trafic", "تعديل الصفحات الأكثر زيارة"),
        t("FAQ and comparison gaps", "Manques de FAQ et de comparatifs", "ثغرات الأسئلة والمقارنات"),
        t("The long tail", "La longue traîne", "بقية الصفحات"),
    ]
    ol = "".join(f'<span class="blog-ord st" style="--i:{k + 4}"><b>{k + 1}</b>{x}</span>' for k, x in enumerate(order))
    return fig(
        "sort",
        t("Three groups, one work order", "Trois groupes, un ordre de travail", "ثلاث مجموعات وترتيب عمل واحد"),
        f'<div class="blog-bins">{out}</div><div class="blog-order"><span class="blog-pt">{t("Fill gaps in this order", "Combler les manques dans cet ordre", "سد الثغرات بهذا الترتيب")}</span><div class="blog-ords">{ol}</div></div>',
        t(
            "The score decides the group. Pillar gaps come first because every retrofit needs a page to link back to.",
            "Le score décide du groupe. Les piliers manquants passent en premier, car chaque reprise a besoin d'une page vers laquelle renvoyer.",
            "الدرجة تحدد المجموعة. وتأتي المقالات المحورية الناقصة أولا، لأن كل تعديل يحتاج إلى صفحة يحيل إليها.",
        ),
        EXAMPLE[lang],
    )


def audit_funnel(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    st = [
        ("grid", t("Every page on the site", "Toutes les pages du site", "كل صفحات الموقع"), 100),
        ("target", t("Pages on topics you want to be cited for", "Les pages sur les sujets où vous voulez être cité", "صفحات المواضيع التي تريد أن يُستشهد بك فيها"), 78),
        ("x", t("Pages that fail the answer-first test", "Les pages qui échouent au test de la réponse d'abord", "الصفحات التي تفشل في اختبار الإجابة أولا"), 56),
        ("chart", t("Rewrite list, most visited first", "Liste de réécriture, les plus visitées d'abord", "قائمة إعادة الكتابة، الأكثر زيارة أولا"), 36),
    ]
    out = "".join(
        f'<div class="blog-fn st{" is-hl" if i == 3 else ""}" style="--i:{i};--w:{w}%">{ic(a)}<b>{n}</b></div>'
        for i, (a, n, w) in enumerate(st)
    )
    return fig(
        "funnel",
        t("How the audit narrows the archive", "Comment l'audit réduit les archives", "كيف يضيّق التدقيق قائمة الصفحات"),
        f'<div class="blog-fns">{out}</div>',
        t(
            "Start with everything, end with a short list you can fix this month.",
            "On part de tout, on finit avec une courte liste à corriger ce mois-ci.",
            "تبدأ بكل الصفحات وتنتهي بقائمة قصيرة تستطيع إصلاحها هذا الشهر.",
        ),
    )


def entity_graph(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    rel = [
        (t("is a", "est un", "هي"), t("Category", "Catégorie", "الفئة"), "grid"),
        (t("solves", "résout", "تحل"), t("Named problem", "Problème nommé", "المشكلة"), "target"),
        (t("replaces", "remplace", "تحل محل"), t("Named alternative", "Alternative nommée", "البديل"), "x"),
        (t("is for", "s'adresse à", "تخدم"), t("Audience", "Audience", "الجمهور"), "user"),
        (t("uses", "utilise", "تعتمد"), t("Mechanism", "Mécanisme", "المنهج"), "layers"),
        (t("produces", "produit", "تقدم"), t("Product and deliverables", "Produit et livrables", "المنتج"), "box"),
        (t("is run by", "est dirigée par", "يقودها"), t("Founder", "Fondateur", "المؤسس"), "user"),
    ]
    cells = []
    for i, (verb, noun, icn) in enumerate(rel):
        cells.append(f'<div class="blog-rel st{" is-hl" if i == 4 else ""}" style="--i:{i}"><span class="blog-verb">{verb}</span><span class="blog-noun">{ic(icn)}<b>{noun}</b></span></div>')
    hub = f'<div class="blog-hub pop" style="--i:0">{icon("building")}<b>{t("Your company", "Votre entreprise", "شركتك")}</b><small dir="ltr">Organization</small></div>'
    left = f'<div class="blog-rels is-a">{"".join(cells[:4])}</div>'
    right = f'<div class="blog-rels is-b">{"".join(cells[4:])}</div>'
    return fig(
        "graph",
        t("An entity and its relationships", "Une entité et ses relations", "كيان وعلاقاته"),
        f'<div class="blog-graph">{left}{hub}{right}</div>',
        t(
            "Every relationship you state on a page, link or schema field is one more question an engine can answer with you as the source.",
            "Chaque relation affirmée dans une page, un lien ou un champ de schéma est une question de plus à laquelle un moteur peut répondre en vous citant.",
            "كل علاقة تصرّح بها في صفحة أو رابط أو حقل ترميز سؤال إضافي يستطيع المحرك أن يجيب عنه وأنت مصدره.",
        ),
    )


def entity_pipeline(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    mech = t("Source extraction", "Extraction de source", "استخراج المصدر")
    srcs = [
        ("globe", t("Your site", "Votre site", "موقعك"), [("KORTEX", True), (mech, True)]),
        ("linkedin", "LinkedIn", [("KORTEX", True), (mech, True)]),
        ("building", t("Directory listing", "Annuaire", "دليل الشركات"), [("KORTEX", True), (t("Content repurposing", "Recyclage de contenu", "إعادة تدوير المحتوى"), False)]),
    ]
    col1 = "".join(
        f'<div class="blog-src st" style="--i:{i}">{ic(a)}<b>{n}</b><span class="blog-sig">{"".join(f"<i class=" + chr(34) + ("is-ok" if ok else "is-off") + chr(34) + ">" + s + "</i>" for s, ok in sig)}</span></div>'
        for i, (a, n, sig) in enumerate(srcs)
    )
    clus = (
        f'<div class="blog-clu pop" style="--i:4"><span class="blog-blob" aria-hidden="true"><i></i><i></i><i></i><i></i><i class="is-off"></i></span>'
        f'<b>{t("One consistent cluster", "Un groupe cohérent", "مجموعة متسقة واحدة")}</b><small>{t("The off-canon term stays outside", "Le terme hors canon reste à l'écart", "المصطلح المخالف يبقى خارجها")}</small></div>'
    )
    ans = answer("", [90, 76, 58], [(BRAND, True)], "ChatGPT", cls="blog-mini")
    stages = [t("Extract", "Extraire", "الاستخراج"), t("Cluster", "Regrouper", "التجميع"), t("Retrieve", "Récupérer", "الاسترجاع")]
    heads = "".join(f'<span class="blog-stg"><b>{k + 1}</b>{s}</span>' for k, s in enumerate(stages))
    return fig(
        "pipe",
        t("Extract, cluster, retrieve", "Extraire, regrouper, récupérer", "استخراج ثم تجميع ثم استرجاع"),
        f'<div class="blog-stgs" aria-hidden="true">{heads}</div><div class="blog-pipe"><div class="blog-col">{col1}</div>{con()}{clus}{con("is-hot")}<div class="blog-col pop" style="--i:6">{ans}</div></div>',
        t(
            "Signals that use the same names merge into one entity. A synonym on one source becomes a separate, weaker signal.",
            "Les signaux qui emploient les mêmes noms se rejoignent en une entité. Un synonyme sur une source devient un signal à part, plus faible.",
            "تندمج الإشارات التي تستعمل الأسماء نفسها في كيان واحد، أما المرادف في مصدر ما فيصبح إشارة منفصلة أضعف.",
        ),
        SIMPLIFIED[lang],
    )


def stack_layers(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    if lang == "ar":
        layers = [
            ("wave", "المصدر", ["فيديو", "بودكاست", "ندوة", "مقال"], ""),
            ("doc", "الصفحات المحورية والتعريفات", ["الفئة", "المشكلة", "المنهج"], ""),
            ("question", "الأسئلة الشائعة والمقارنات", ["أسئلة الشراء", "المقارنات"], ""),
            ("send", "التوزيع", ["منشورات", "نشرات", "موارد المبيعات"], ""),
        ]
    else:
        layers = [
            ("wave", t("Raw signal", "Signal brut", ""), [t("Founder video", "Vidéo du fondateur", ""), "Podcast", t("Webinar", "Webinaire", "")], "Whisper"),
            ("node", t("Entity structure", "Structure d'entité", ""), [t("Category", "Catégorie", ""), t("Problem", "Problème", ""), t("Mechanism", "Mécanisme", ""), t("Alternative", "Alternative", ""), t("Audience", "Audience", "")], "Gemini"),
            ("doc", t("Answer assets", "Contenus de réponse", ""), [t("Pillar", "Pilier", ""), t("Contrarian", "Contre-courant", ""), t("Comparison", "Comparatif", ""), "FAQ", t("Use cases", "Cas d'usage", "")], "Gemini + n8n"),
            ("send", t("Distribution", "Diffusion", ""), ["LinkedIn", "Email", t("Clips", "Extraits", ""), t("Outreach", "Prospection", "")], "n8n"),
        ]
    out = ""
    for i, (a, name, items, tool) in enumerate(layers):
        p = "".join(f'<span class="blog-pill">{x}</span>' for x in items)
        tl = f'<span class="blog-tool" dir="ltr">{tool}</span>' if tool else ""
        out = (
            f'<div class="blog-st st{" is-hl" if i == 2 else ""}" style="--i:{i}"><span class="blog-gn">{i + 1}</span>{ic(a)}<span class="blog-stt"><b>{name}</b><span class="blog-pills">{p}</span></span>{tl}</div>'
            + out
        )
    return fig(
        "stack",
        t("The four layers of the stack", "Les quatre couches de la stack", "طبقات المنظومة الأربع"),
        f'<div class="blog-stk"><i class="blog-spine" aria-hidden="true">{beam()}</i>{out}</div>',
        t(
            "Read it bottom up. Each layer feeds the one above and reuses the same definitions; tools automate the mechanics, people approve.",
            "Se lit de bas en haut. Chaque couche nourrit la suivante avec les mêmes définitions ; les outils automatisent, les humains valident.",
            "تُقرأ من الأسفل إلى الأعلى: كل طبقة تغذي التي فوقها بالمصطلحات نفسها.",
        ),
    )


def stack_workflow(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    steps = [
        ("link", t("Trigger", "Déclencheur", "البدء"), t("A source link is submitted", "Un lien source est envoyé", "يُرسل رابط المصدر"), ""),
        ("wave", t("Transcription", "Transcription", "التفريغ"), t("Timestamped transcript", "Transcription horodatée", "نص مؤرخ بالتوقيت"), "Whisper"),
        ("search", t("Extraction", "Extraction", "الاستخراج"), t("Six elements tagged", "Six éléments repérés", "تحديد العناصر الستة"), "Gemini"),
        ("user", t("Human checkpoint 1", "Contrôle humain 1", "مراجعة بشرية 1"), t("Editor builds the entity sheet, founder validates", "L'éditeur construit la fiche d'entité, le fondateur valide", "يبني المحرر ورقة الكيان ويعتمدها المؤسس"), "human"),
        ("pen", t("Drafting", "Rédaction", "الصياغة"), t("Templates with the entity sheet injected", "Gabarits avec la fiche d'entité injectée", "قوالب تتضمن ورقة الكيان"), "Gemini"),
        ("shield", t("Automated checks", "Contrôles automatiques", "فحوص آلية"), t("Banned synonyms, missing links, weak openings", "Synonymes interdits, liens manquants, ouvertures faibles", "مرادفات ممنوعة وروابط ناقصة وافتتاحيات ضعيفة"), "n8n"),
        ("user", t("Human checkpoint 2", "Contrôle humain 2", "مراجعة بشرية 2"), t("Edit, approve, schedule", "Relire, valider, planifier", "التحرير والاعتماد والجدولة"), "human"),
    ]
    out = ""
    for i, (a, name, sub, tool) in enumerate(steps):
        hum = tool == "human"
        tl = stamp(t("Human", "Humain", "بشري"), "blog-stamp") if hum else (f'<span class="blog-tool" dir="ltr">{tool}</span>' if tool else "")
        out += f'<div class="blog-wf st{" is-human" if hum else ""}" style="--i:{i}"><span class="blog-gn">{i + 1}</span>{ic(a)}<b>{name}</b><p>{sub}</p>{tl}</div>'
    return fig(
        "flow",
        t("A content workflow with two human gates", "Un flux de contenu avec deux contrôles humains", "سير عمل بمحطتين للمراجعة البشرية"),
        f'<div class="blog-wfs">{out}</div>',
        t(
            "Nothing downstream runs before the first approval. The two human checkpoints are where judgment lives.",
            "Rien ne s'exécute en aval avant la première validation. Les deux contrôles humains sont là où s'exerce le jugement.",
            "لا يبدأ أي شيء بعد المرحلة الأولى قبل الاعتماد، فالمراجعتان البشريتان هما موضع الحكم.",
        ),
    )


def six_elements(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    sheet = t("Entity sheet, every asset", "Fiche d'entité, tous les contenus", "ورقة الكيان، كل الأصول")
    el = [
        ("04:12", t("Core thesis", "Thèse centrale", "الفكرة الرئيسية"), t("Pillar article", "Article pilier", "المقال المحوري"), True),
        ("09:40", t("Named mechanism", "Mécanisme nommé", "المنهج المسمى"), sheet, False),
        ("15:05", t("Rejected alternative", "Alternative rejetée", "البديل المرفوض"), t("Contrarian article", "Article à contre-courant", "مقال الرأي"), False),
        ("22:30", t("Repeated examples", "Exemples répétés", "الأمثلة المتكررة"), t("LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن"), False),
        ("31:18", t("Audience signals", "Signaux d'audience", "إشارات الجمهور"), sheet, False),
        ("44:02", t("Preemptive objections", "Objections anticipées", "الاعتراضات المسبقة"), t("FAQ cluster", "Grappe de FAQ", "الأسئلة الشائعة"), False),
    ]
    rows = ""
    for i, (ts, name, to, hl) in enumerate(el):
        rows += (
            f'<div class="blog-el st{" is-hl" if hl else ""}" style="--i:{i}"><span class="blog-ts" dir="ltr">{ts}</span>'
            f'<span class="blog-mk"><b>{name}</b>{sk(88, 64)}</span><span class="blog-arr" aria-hidden="true">{icon("arrow")}</span><span class="blog-to">{to}</span></div>'
        )
    head = f'<div class="blog-tx-h">{ic("play")}<b>{t("Founder video transcript", "Transcription de la vidéo du fondateur", "نص فيديو المؤسس")}</b><span dir="ltr">45–60 min</span></div>'
    return fig(
        "six",
        t("Six elements, each with a destination", "Six éléments, chacun sa destination", "ستة عناصر، لكل منها وجهة"),
        f'<div class="blog-tx">{head}{rows}</div>',
        t(
            "Extraction reads for these six elements, not for main points. Each one is mapped to the asset it will serve.",
            "L'extraction cherche ces six éléments, pas un résumé. Chacun est affecté au contenu qu'il servira.",
            "يبحث الاستخراج عن هذه العناصر الستة لا عن ملخص، ويُسند كل عنصر إلى الأصل الذي سيخدمه.",
        ),
        EXAMPLE[lang],
    )


def video_month(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    ev = {
        1: ("ret", t("Pillar article", "Article pilier", "مقال محوري")),
        3: ("dis", t("Hook post", "Post d'accroche", "منشور الافتتاح")),
        5: ("ret", t("Contrarian article", "Article à contre-courant", "مقال رأي")),
        7: ("ret", t("FAQ cluster", "Grappe de FAQ", "أسئلة شائعة")),
        9: ("dis", t("Mechanism post", "Post mécanisme", "منشور المنهج")),
        12: ("ret", t("Comparison + post", "Comparatif + post", "مقارنة ومنشور")),
        20: ("dis", t("Newsletter 1", "Newsletter 1", "النشرة 1")),
        28: ("dis", t("Newsletter 2", "Newsletter 2", "النشرة 2")),
        30: ("sal", t("Sales assets", "Contenus commerciaux", "موارد المبيعات")),
    }
    cells = ""
    for d in range(1, 36):
        if d > 30:
            cells += '<i class="blog-c is-void"></i>'
            continue
        kind, name = ev.get(d, ("wave" if 14 <= d <= 25 else "", ""))
        nm = f"<b>{name}</b>" if name else ""
        cells += f'<i class="blog-c is-{kind or "nil"} pop" style="--i:{d // 3}"><span dir="ltr">{d}</span>{nm}</i>'
    legend = (
        f'<span class="blog-lgd is-ret"><i></i>{t("Retrieval layer", "Couche de récupération", "طبقة الاسترجاع")}</span>'
        f'<span class="blog-lgd is-dis"><i></i>{t("Distribution", "Diffusion", "التوزيع")}</span>'
        f'<span class="blog-lgd is-wave"><i></i>{t("LinkedIn wave, days 14 to 25", "Vague LinkedIn, jours 14 à 25", "موجة لينكدإن، من اليوم 14 إلى 25")}</span>'
        f'<span class="blog-lgd is-sal"><i></i>{t("Sales", "Ventes", "المبيعات")}</span>'
    )
    src = f'<div class="blog-vsrc">{ic("play", "blog-play")}<b>{t("One video", "Une vidéo", "فيديو واحد")}</b><small dir="ltr">45–60 min</small></div>'
    return fig(
        "month",
        t("The 30-day publishing sequence", "La séquence de publication sur 30 jours", "تسلسل النشر على 30 يوما"),
        f'<div class="blog-mo">{src}{con("is-hot")}<div class="blog-cal">{cells}</div></div><div class="blog-lgds">{legend}</div>',
        t(
            "The retrieval layer is live by day 12. Only then does the distribution wave start pointing people to it.",
            "La couche de récupération est en ligne au jour 12. C'est seulement ensuite que la vague de diffusion y envoie du monde.",
            "تكتمل طبقة الاسترجاع بحلول اليوم 12، وبعدها فقط تبدأ موجة التوزيع في توجيه الناس إليها.",
        ),
    )


def video_weeks(lang):
    t = lambda en, fr, ar: T(lang, en, fr, ar)
    wk = [
        ("search", t("Week 1", "Semaine 1", "الأسبوع الأول"), t("Map the ideas", "Cartographier les idées", "خريطة الأفكار"), [t("Thesis", "Thèse", "الفكرة الرئيسية"), t("Objections", "Objections", "الاعتراضات"), t("Terms", "Termes", "المصطلحات"), t("Questions", "Questions", "الأسئلة")]),
        ("pen", t("Weeks 2 and 3", "Semaines 2 et 3", "الأسبوعان الثاني والثالث"), t("Produce", "Produire", "الإنتاج"), [t("Pillar", "Pilier", "مقال محوري"), t("Opinion", "Opinion", "مقال رأي"), t("Comparison", "Comparatif", "صفحة مقارنة"), t("FAQ", "FAQ", "أسئلة شائعة"), t("Posts", "Posts", "منشورات")]),
        ("link", t("Week 4", "Semaine 4", "الأسبوع الرابع"), t("Publish and link", "Publier et relier", "النشر والربط"), [t("Internal links", "Liens internes", "روابط داخلية"), "Schema", t("Scheduled posts", "Posts planifiés", "منشورات مجدولة")]),
    ]
    out = ""
    for i, (a, w, name, items) in enumerate(wk):
        p = "".join(f'<span class="blog-pill">{x}</span>' for x in items)
        out += f'<div class="blog-ph st{" is-hl" if i == 1 else ""}" style="--i:{i}">{ic(a)}<span class="blog-dn">{w}</span><b>{name}</b><span class="blog-pills">{p}</span></div>'
    nxt = f'<div class="blog-next pop" style="--i:4">{icon("loop")}<b>{t("Next source", "Source suivante", "المصدر التالي")}</b></div>'
    return fig(
        "weeks",
        t("One video, four weeks", "Une vidéo, quatre semaines", "فيديو واحد في أربعة أسابيع"),
        f'<div class="blog-phs is-3"><i class="blog-track" aria-hidden="true"></i>{out}</div>{nxt}',
        t(
            "An indicative timeline. Each cycle builds on the pages the previous one published.",
            "Un calendrier indicatif. Chaque cycle s'appuie sur les pages publiées par le précédent.",
            "جدول إرشادي، وكل دورة تبني فوق الصفحات التي نشرتها الدورة السابقة.",
        ),
    )


VISUALS = {
    "blog-hero": blog_hero,
    "blog-rank-vs-cite": rank_vs_cite,
    "blog-cited-vs-synth": cited_vs_synth,
    "blog-three-tests": three_tests,
    "blog-four-layers": four_layers,
    "blog-signal-levels": signal_levels,
    "blog-feed-decay": feed_decay,
    "blog-post-loop": post_loop,
    "blog-category-def": category_def,
    "blog-category-phases": category_phases,
    "blog-audit-score": audit_score,
    "blog-audit-sort": audit_sort,
    "blog-audit-funnel": audit_funnel,
    "blog-entity-graph": entity_graph,
    "blog-entity-pipeline": entity_pipeline,
    "blog-stack-layers": stack_layers,
    "blog-stack-workflow": stack_workflow,
    "blog-six-elements": six_elements,
    "blog-video-month": video_month,
    "blog-video-weeks": video_weeks,
}
