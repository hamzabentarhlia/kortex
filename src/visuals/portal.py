from . import kit
from .kit import T, icon, label, frame

NAV = ["dashboard", "profile", "engine", "deliverables", "intelligence"]


def _nav(lang, active):
    names = {
        "dashboard": ("grid", T(lang, "Dashboard", "Tableau de bord", "لوحة القيادة")),
        "profile": ("user", T(lang, "Profile", "Profil", "الملف")),
        "engine": ("bolt", T(lang, "Content Engine", "Moteur de contenu", "محرك المحتوى")),
        "deliverables": ("box", T(lang, "Deliverables", "Livrables", "التسليمات")),
        "intelligence": ("eye", T(lang, "Intelligence", "Veille", "الرصد")),
    }
    items = "".join(f'<li class="{"is-on" if k == active else ""}">{icon(names[k][0])}<span>{names[k][1]}</span></li>' for k in NAV)
    return f'<nav class="pt-nav" aria-hidden="true"><span class="pt-logo"><i></i>KORTEX</span><ul>{items}</ul></nav>'


def _head(lang, title):
    return f'<div class="pt-head"><div><small>Acme</small><b>{title}</b></div><span class="pt-plan">SWARM</span>{label(kit.DEMO[lang], "demo")}</div>'


def _status(lang, kind):
    txt = {
        "review": T(lang, "In review", "En relecture", "قيد المراجعة"),
        "ok": T(lang, "Approved", "Validé", "تمت الموافقة"),
        "live": T(lang, "Published", "Publié", "منشور"),
        "draft": T(lang, "Drafting", "Rédaction", "قيد الكتابة"),
    }[kind]
    return f'<span class="pt-st pt-st-{kind}">{txt}</span>'


def _rows(lang):
    return [
        ("doc", T(lang, "Pillar: the supplier audit gap", "Pilier : les angles morts de l'audit fournisseur", "مقال محوري: ثغرات تدقيق الموردين"), "live"),
        ("columns", T(lang, "Comparison: spreadsheet vs monitoring", "Comparatif : tableur ou suivi continu", "مقارنة: جداول البيانات أم المراقبة"), "ok"),
        ("chat", T(lang, "FAQ: reviewing suppliers", "FAQ : revoir ses fournisseurs", "أسئلة شائعة: مراجعة الموردين"), "review"),
        ("mail", T(lang, "Newsletter, week 2", "Newsletter, semaine 2", "النشرة، الأسبوع 2"), "review"),
        ("linkedin", T(lang, "LinkedIn posts, week 2", "Posts LinkedIn, semaine 2", "منشورات لينكدإن، الأسبوع 2"), "draft"),
    ]


def dashboard(lang):
    kpis = [
        ("play", T(lang, "Source this month", "Source du mois", "مصدر هذا الشهر"), T(lang, "Webinar, 52 min", "Webinaire, 52 min", "ندوة، 52 دقيقة")),
        ("box", T(lang, "Assets", "Contenus", "المحتويات"), "20"),
        ("pen", T(lang, "Waiting for you", "En attente de vous", "بانتظار موافقتك"), "3"),
        ("gauge", T(lang, "Citation check", "Vérification des citations", "فحص الاستشهادات"), T(lang, "10 questions", "10 questions", "10 أسئلة")),
    ]
    k = "".join(f'<div class="pt-kpi st" style="--i:{i}"><span>{icon(ic)}{t}</span><b>{v}</b></div>' for i, (ic, t, v) in enumerate(kpis))
    mix = kit.donut([(T(lang, "Articles", "Articles", "مقالات"), 4, "a"), (T(lang, "Newsletters", "Newsletters", "نشرات"), 4, "b"), (T(lang, "Social posts", "Posts sociaux", "منشورات"), 12, "d")], size=120, center="20")
    rows = "".join(f'<li class="st" style="--i:{i + 3}">{icon(ic)}<span>{t}</span>{_status(lang, st)}</li>' for i, (ic, t, st) in enumerate(_rows(lang)))
    body = (
        f'<div class="pt">{_nav(lang, "dashboard")}<div class="pt-main">{_head(lang, T(lang, "Dashboard", "Tableau de bord", "لوحة القيادة"))}'
        f'<div class="pt-kpis">{k}</div>'
        f'<div class="pt-split"><div class="pt-card"><b class="pt-ct">{T(lang, "This month by format", "Ce mois par format", "هذا الشهر حسب الصيغة")}</b>{mix}</div>'
        f'<div class="pt-card"><b class="pt-ct">{T(lang, "Latest deliverables", "Derniers livrables", "آخر التسليمات")}</b><ul class="pt-list">{rows}</ul></div></div></div></div>'
    )
    return body


def deliverables_phone(lang):
    rows = _rows(lang)[1:4]
    items = "".join(
        f'<li class="pop" style="--i:{i + 1}"><span class="pt-ph-ic">{icon(ic)}</span><span class="pt-ph-t"><b>{t}</b>{_status(lang, st)}</span></li>' for i, (ic, t, st) in enumerate(rows)
    )
    return (
        f'<div class="pt-ph"><div class="pt-ph-top"><b>{T(lang, "Deliverables", "Livrables", "التسليمات")}</b>{label(kit.DEMO[lang], "demo")}</div>'
        f'<ul class="pt-ph-list">{items}</ul>'
        f'<div class="pt-ph-cta"><span>{T(lang, "Approve", "Valider", "موافقة")}</span><span>{T(lang, "Comment", "Commenter", "تعليق")}</span></div></div>'
    )


def engine(lang):
    lines = [
        (T(lang, "Most audits happen once a year. Most failures do not wait that long.", "La plupart des audits ont lieu une fois par an. Les défaillances n'attendent pas.", "معظم عمليات التدقيق تتم مرة في السنة، والإخفاقات لا تنتظر كل هذا الوقت."), "12:40", True),
        (T(lang, "We look at payment delays first. They show up months before a missed delivery.", "Nous regardons d'abord les retards de paiement. Ils apparaissent des mois avant une livraison manquée.", "ننظر أولا إلى تأخر المدفوعات، فهو يظهر قبل أشهر من أي تأخر في التسليم."), "18:05", True),
        (T(lang, "A spreadsheet tells you what was true on the day you filled it.", "Un tableur dit ce qui était vrai le jour où vous l'avez rempli.", "جدول البيانات يخبرك بما كان صحيحا يوم ملأته فقط."), "27:30", False),
    ]
    tr = "".join(f'<p class="pt-tr{" is-hl" if hl else ""} st" style="--i:{i}"><span dir="ltr">{ts}</span>{txt}</p>' for i, (txt, ts, hl) in enumerate(lines))
    outs = [
        ("doc", T(lang, "Pillar article", "Article pilier", "مقال محوري"), .92),
        ("columns", T(lang, "Comparison page", "Page comparative", "صفحة مقارنة"), .7),
        ("chat", T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة شائعة"), .55),
        ("linkedin", T(lang, "LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن"), .35),
    ]
    prog = "".join(f'<li class="st" style="--i:{i + 2}">{icon(ic)}<span>{t}</span><span class="pt-prog"><i style="--s:{v}"></i></span></li>' for i, (ic, t, v) in enumerate(outs))
    return (
        f'<div class="pt">{_nav(lang, "engine")}<div class="pt-main">{_head(lang, T(lang, "Content Engine", "Moteur de contenu", "محرك المحتوى"))}'
        f'<div class="pt-split pt-split-eq"><div class="pt-card"><b class="pt-ct">{icon("play")}{T(lang, "Source transcript", "Transcription de la source", "نص المصدر")}</b>{tr}</div>'
        f'<div class="pt-card"><b class="pt-ct">{icon("bolt")}{T(lang, "In production", "En production", "قيد الإنتاج")}</b><ul class="pt-out">{prog}</ul></div></div></div></div>'
    )


def intelligence_phone(lang):
    engines = [("ChatGPT", [1, 0, 1, 1, 0]), ("Perplexity", [1, 1, 0, 1, 1]), ("Gemini", [0, 0, 1, 0, 0]), ("AI Overviews", [1, 0, 0, 1, 0])]
    rows = "".join(
        f'<li><span dir="ltr">{e}</span><span class="pt-dots">' + "".join(f'<i class="{"is-on" if c else ""}" style="--i:{j + n}"></i>' for j, c in enumerate(cs)) + "</span></li>"
        for n, (e, cs) in enumerate(engines)
    )
    return (
        f'<div class="pt-ph"><div class="pt-ph-top"><b>{T(lang, "Intelligence", "Veille", "الرصد")}</b>{label(kit.DEMO[lang], "demo")}</div>'
        f'<p class="pt-ph-sub">{T(lang, "Who gets cited, question by question", "Qui est cité, question par question", "من يُستشهد به، سؤالا بسؤال")}</p>'
        f'<ul class="pt-eng">{rows}</ul></div>'
    )


def profile_card(lang):
    terms = [T(lang, "supplier risk", "risque fournisseur", "مخاطر الموردين"), T(lang, "continuous monitoring", "suivi continu", "المراقبة المستمرة"), T(lang, "risk score", "score de risque", "مؤشر المخاطر")]
    avoid = [T(lang, "vendor danger", "danger vendeur", "خطر البائع"), T(lang, "AI-powered", "propulsé par l'IA", "مدعوم بالذكاء الاصطناعي")]
    chips = "".join(f'<span class="pt-term">{icon("check")}{t}</span>' for t in terms) + "".join(f'<span class="pt-term is-no">{icon("x")}{t}</span>' for t in avoid)
    return (
        f'<div class="pt-profile"><div class="pt-ph-top"><b>{T(lang, "Profile: voice and terms", "Profil : ton et vocabulaire", "الملف: الأسلوب والمصطلحات")}</b>{label(kit.DEMO[lang], "demo")}</div>'
        f'<div class="pt-voice"><span>{T(lang, "Plain", "Simple", "بسيط")}</span><i><b style="--x:.22"></b></i><span>{T(lang, "Technical", "Technique", "تقني")}</span></div>'
        f'<div class="pt-terms">{chips}</div></div>'
    )


def home_workspace(lang):
    ws = T(lang, "Client workspace", "Espace client", "مساحة العميل")
    return (
        '<div class="pw">'
        f'<div class="pw-browser" data-parallax="0.04">{frame(dashboard(lang), "browser", ws)}</div>'
        f'<div class="pw-phone" data-parallax="0.1">{frame(deliverables_phone(lang), "phone")}</div>'
        "</div>"
    )


def hiw_workspace(lang):
    ws = T(lang, "Client workspace", "Espace client", "مساحة العميل")
    return (
        '<div class="pw pw-hiw">'
        f'<div class="pw-browser" data-parallax="0.04">{frame(engine(lang), "browser", ws)}</div>'
        f'<div class="pw-phone" data-parallax="0.1">{frame(intelligence_phone(lang), "phone")}</div>'
        "</div>"
    )


VISUALS = {"portal-home": home_workspace, "portal-hiw": hiw_workspace, "portal-profile": profile_card}
