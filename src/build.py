import hashlib
import html
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
DOMAIN = "https://www.kortexlab.me"
LANGS = ["en", "fr", "ar"]
PREFIX = {"en": "", "fr": "/fr", "ar": "/ar"}
LOCALE = {"en": "en_US", "fr": "fr_FR", "ar": "ar_MA"}
LANG_NAME = {"en": "English", "fr": "Français", "ar": "العربية"}
LANG_SHORT = {"en": "EN", "fr": "FR", "ar": "AR"}
EMAIL = "contact@kortexlab.me"
LINKEDIN = "https://www.linkedin.com/in/hamza-bentarhlia/"
WEB3FORMS_KEY = "0aa868e7-7559-439c-a911-1f246b2d03e3"
GA_ID = "G-4440VPDMPW"
BUILD_DATE = "2026-10-18"

PAGES = {
    "home": "/",
    "how-it-works": "/how-it-works/",
    "solutions": "/solutions/",
    "b2b": "/solutions/b2b/",
    "creators": "/solutions/creators/",
    "ecommerce": "/solutions/ecommerce/",
    "from-blog": "/solutions/from-a-blog/",
    "from-youtube": "/solutions/from-youtube/",
    "from-podcast": "/solutions/from-a-podcast/",
    "from-webinar": "/solutions/from-a-webinar/",
    "pricing": "/pricing/",
    "about": "/about/",
    "compare": "/compare/",
    "vs-seo-agency": "/compare/kortex-vs-seo-agency/",
    "vs-chatgpt": "/compare/kortex-vs-chatgpt/",
    "vs-freelance": "/compare/kortex-vs-freelance-writer/",
    "security": "/security/",
    "glossary": "/glossary/",
    "blog": "/blog/",
    "audit": "/free-geo-audit/",
    "contact": "/contact/",
    "privacy": "/legal/privacy/",
    "terms": "/legal/terms/",
    "cookies": "/legal/cookies/",
    "login": "/login/",
}

UI = {
    "en": {
        "skip": "Skip to main content",
        "nav_label": "Main",
        "how": "How it works",
        "solutions": "Solutions",
        "by_audience": "By audience",
        "by_source": "By source",
        "pricing": "Pricing",
        "resources": "Resources",
        "blog": "Blog",
        "glossary": "Glossary",
        "compare": "Comparisons",
        "about": "About",
        "login": "Login",
        "book": "Book a strategy call",
        "audit": "Get a free GEO audit",
        "menu": "Open menu",
        "close": "Close menu",
        "theme": "Switch light and dark theme",
        "language": "Language",
        "b2b": ("B2B companies", "SaaS, consulting, services, industry"),
        "creators": ("Creators and experts", "YouTube, podcasts, coaching, teaching"),
        "ecommerce": ("E-commerce brands", "Products, categories, buying guides"),
        "from-blog": ("From a blog post", "Your best article, rebuilt"),
        "from-youtube": ("From a YouTube video", "Talks, tutorials, interviews"),
        "from-podcast": ("From a podcast", "Episodes and guest interviews"),
        "from-webinar": ("From a webinar", "Live sessions and recorded demos"),
        "footer_blurb": "GEO, SEO and content studio. One source becomes a month of content that AI answer engines can quote and search engines can rank.",
        "footer_place": "Based in Fès, Morocco. Working with clients worldwide.",
        "col_product": "Product",
        "col_solutions": "Solutions",
        "col_resources": "Resources",
        "col_company": "Company",
        "contact": "Contact",
        "security": "Security and data",
        "privacy": "Privacy",
        "terms": "Terms",
        "cookies": "Cookies",
        "rights": "KORTEX. All rights reserved.",
        "cta_kicker": "Next step",
        "cta_title": "Make your expertise the answer",
        "cta_text": "Tell us where your expertise lives today. We show you where AI engines already mention your field, and what it would take for them to mention you.",
        "cta_terms": "No setup fees. No commitment.",
        "home_crumb": "Home",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "nav_label": "Principale",
        "how": "Méthode",
        "solutions": "Solutions",
        "by_audience": "Par profil",
        "by_source": "Par source",
        "pricing": "Tarifs",
        "resources": "Ressources",
        "blog": "Blog",
        "glossary": "Glossaire",
        "compare": "Comparatifs",
        "about": "À propos",
        "login": "Connexion",
        "book": "Réserver un appel stratégique",
        "audit": "Obtenir un audit GEO gratuit",
        "menu": "Ouvrir le menu",
        "close": "Fermer le menu",
        "theme": "Basculer entre thème clair et sombre",
        "language": "Langue",
        "b2b": ("Entreprises B2B", "SaaS, conseil, services, industrie"),
        "creators": ("Créateurs et experts", "YouTube, podcasts, coaching, formation"),
        "ecommerce": ("Marques e-commerce", "Produits, catégories, guides d'achat"),
        "from-blog": ("À partir d'un article", "Votre meilleur article, reconstruit"),
        "from-youtube": ("À partir d'une vidéo YouTube", "Conférences, tutoriels, interviews"),
        "from-podcast": ("À partir d'un podcast", "Épisodes et interviews d'invités"),
        "from-webinar": ("À partir d'un webinaire", "Sessions live et démos enregistrées"),
        "footer_blurb": "Studio GEO, SEO et contenu. Une source devient un mois de contenus que les moteurs de réponse IA peuvent citer et que les moteurs de recherche peuvent classer.",
        "footer_place": "Basé à Fès, au Maroc. Clients dans le monde entier.",
        "col_product": "Offre",
        "col_solutions": "Solutions",
        "col_resources": "Ressources",
        "col_company": "Entreprise",
        "contact": "Contact",
        "security": "Sécurité et données",
        "privacy": "Confidentialité",
        "terms": "Conditions",
        "cookies": "Cookies",
        "rights": "KORTEX. Tous droits réservés.",
        "cta_kicker": "Prochaine étape",
        "cta_title": "Faites de votre expertise la réponse",
        "cta_text": "Dites-nous où vit votre expertise aujourd'hui. Nous vous montrons où les moteurs IA parlent déjà de votre domaine, et ce qu'il faudrait pour qu'ils parlent de vous.",
        "cta_terms": "Sans frais d'installation. Sans engagement.",
        "home_crumb": "Accueil",
    },
    "ar": {
        "skip": "الانتقال إلى المحتوى الرئيسي",
        "nav_label": "القائمة الرئيسية",
        "how": "طريقة العمل",
        "solutions": "الحلول",
        "by_audience": "حسب الفئة",
        "by_source": "حسب المصدر",
        "pricing": "الأسعار",
        "resources": "الموارد",
        "blog": "المدونة",
        "glossary": "المصطلحات",
        "compare": "مقارنات",
        "about": "من نحن",
        "login": "تسجيل الدخول",
        "book": "احجز مكالمة استراتيجية",
        "audit": "احصل على تدقيق GEO مجاني",
        "menu": "فتح القائمة",
        "close": "إغلاق القائمة",
        "theme": "التبديل بين الوضع الفاتح والداكن",
        "language": "اللغة",
        "b2b": ("شركات B2B", "البرمجيات، الاستشارات، الخدمات، الصناعة"),
        "creators": ("صناع المحتوى والخبراء", "يوتيوب، بودكاست، تدريب، تعليم"),
        "ecommerce": ("علامات التجارة الإلكترونية", "منتجات، فئات، أدلة شراء"),
        "from-blog": ("انطلاقا من مقال", "أفضل مقالاتك، بصيغة جديدة"),
        "from-youtube": ("انطلاقا من فيديو يوتيوب", "محاضرات، شروحات، مقابلات"),
        "from-podcast": ("انطلاقا من بودكاست", "حلقات ومقابلات مع ضيوف"),
        "from-webinar": ("انطلاقا من ندوة رقمية", "جلسات مباشرة وعروض مسجلة"),
        "footer_blurb": "استوديو GEO وSEO وصناعة المحتوى. مصدر واحد يتحول إلى شهر كامل من المحتوى تستطيع محركات الإجابة بالذكاء الاصطناعي الاستشهاد به ومحركات البحث ترتيبه.",
        "footer_place": "مقرنا في فاس، المغرب. نعمل مع عملاء حول العالم.",
        "col_product": "الخدمة",
        "col_solutions": "الحلول",
        "col_resources": "الموارد",
        "col_company": "الشركة",
        "contact": "تواصل معنا",
        "security": "الأمان والبيانات",
        "privacy": "الخصوصية",
        "terms": "الشروط",
        "cookies": "ملفات تعريف الارتباط",
        "rights": "KORTEX. جميع الحقوق محفوظة.",
        "cta_kicker": "الخطوة التالية",
        "cta_title": "اجعل خبرتك هي الإجابة",
        "cta_text": "أخبرنا أين توجد خبرتك اليوم. سنريك أين تذكر محركات الذكاء الاصطناعي مجالك حاليا، وما الذي يلزم لكي تذكرك أنت.",
        "cta_terms": "بدون رسوم إعداد. بدون التزام.",
        "home_crumb": "الرئيسية",
    },
}

ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>',
    "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "play": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10.5 9.5v5l4-2.5z"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/>',
    "screen": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4M8 9.5l2.5 2 5-4"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.5 2.5M15.2 15.2l2.5 2.5M6.3 17.7l2.5-2.5M15.2 8.8l2.5-2.5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "quote": '<path d="M5 18h5v-6H6.5A3.5 3.5 0 0 1 10 8.5V6A6 6 0 0 0 4 12v5a1 1 0 0 0 1 1zM14 18h5v-6h-3.5A3.5 3.5 0 0 1 19 8.5V6a6 6 0 0 0-6 6v5a1 1 0 0 0 1 1z"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V17M8 7.2v.1M12 17v-6.5M12 13.5c0-2 1.2-3 2.6-3S17 11.4 17 13.3V17"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5L12 13l8.5-6.5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.8-3.8"/>',
    "building": '<path d="M4 21V5l8-2v18M12 8l8 2v11M3 21h18M7.5 8h1M7.5 12h1M7.5 16h1M15.5 13h1M15.5 17h1"/>',
    "cart": '<path d="M3 4h2.5l2.2 11h10.6L20.5 8H6.8"/><circle cx="9" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/>',
    "pen": '<path d="M4 20l4.5-1 10-10a2.1 2.1 0 0 0-3-3l-10 10z"/><path d="M14 7l3 3"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "loop": '<path d="M20 12a8 8 0 0 1-14.3 4.9M4 12A8 8 0 0 1 18.3 7.1"/><path d="M18.5 3v4.2h-4.2M5.5 21v-4.2h4.2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "grid": '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
}

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><defs><radialGradient id="kxg" cx="70%" cy="75%" r="70%"><stop offset="0" stop-color="#ffb648"/><stop offset=".55" stop-color="#ff6b2c"/><stop offset="1" stop-color="#c9341f"/></radialGradient></defs><rect width="32" height="32" rx="9" fill="url(#kxg)"/><path d="M11 8.5v15M11 16l9-7.5M13.8 13.6l7.2 9.9" stroke="#1b0c05" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg>'


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def source_path(lang, pid):
    return SRC / "pages" / lang / f"{pid}.html"


def exists(lang, pid):
    return source_path(lang, pid).exists()


def url(lang, pid):
    return PREFIX[lang] + PAGES[pid]


def abs_url(lang, pid):
    return DOMAIN + url(lang, pid)


def available(pid):
    return [l for l in LANGS if exists(l, pid)]


def asset_version(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:8]


def minify_css(css):
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def parse_page(path):
    raw = path.read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def nav_item(lang, pid, current, label):
    if not exists(lang, pid):
        return ""
    cur = ' aria-current="page"' if pid == current else ""
    return f'<li><a class="nav-link" href="{url(lang, pid)}"{cur}>{label}</a></li>'


def menu_links(lang, groups, current):
    t = UI[lang]
    out = []
    for heading, ids in groups:
        items = []
        for pid in ids:
            if not exists(lang, pid):
                continue
            cur = ' aria-current="page"' if pid == current else ""
            value = t.get(pid)
            if isinstance(value, tuple):
                items.append(f'<a href="{url(lang, pid)}"{cur}>{value[0]}<span>{value[1]}</span></a>')
            else:
                items.append(f'<a href="{url(lang, pid)}"{cur}>{value}</a>')
        if items:
            if heading:
                out.append(f'<span class="menu-label">{heading}</span>')
            out.extend(items)
    return "".join(out)


def dropdown(lang, key, label, groups, current):
    links = menu_links(lang, groups, current)
    if not links:
        return ""
    return (
        f'<li><button class="nav-link" type="button" aria-expanded="false" aria-controls="menu-{key}" data-menu-toggle>{label}{icon("chevron")}</button>'
        f'<div class="nav-menu" id="menu-{key}" hidden>{links}</div></li>'
    )


SOLUTION_GROUPS = lambda t: [(t["by_audience"], ["b2b", "creators", "ecommerce"]), (t["by_source"], ["from-blog", "from-youtube", "from-podcast", "from-webinar"])]
RESOURCE_GROUPS = [(None, ["blog", "glossary", "compare", "about"])]


def lang_links(lang, pid, mobile=False):
    out = []
    for l in available(pid):
        cur = ' aria-current="true"' if l == lang else ""
        if mobile:
            out.append(f'<a class="btn btn-ghost btn-sm" href="{url(l, pid)}" hreflang="{l}" lang="{l}"{cur}>{LANG_NAME[l]}</a>')
        else:
            out.append(f'<a href="{url(l, pid)}" hreflang="{l}" lang="{l}"{cur}>{LANG_NAME[l]}</a>')
    return "".join(out)


def header(lang, pid):
    t = UI[lang]
    items = [
        nav_item(lang, "how-it-works", pid, t["how"]),
        dropdown(lang, "solutions", t["solutions"], SOLUTION_GROUPS(t), pid),
        nav_item(lang, "pricing", pid, t["pricing"]),
        dropdown(lang, "resources", t["resources"], RESOURCE_GROUPS, pid),
    ]
    langs = ""
    if len(available(pid)) > 1:
        langs = (
            f'<div class="lang-switch"><button class="nav-link" type="button" aria-expanded="false" aria-controls="menu-lang" data-menu-toggle>'
            f'<span class="visually-hidden">{t["language"]}: </span>{LANG_SHORT[lang]}{icon("chevron")}</button>'
            f'<div class="nav-menu" id="menu-lang" hidden>{lang_links(lang, pid)}</div></div>'
        )
    login = f'<a class="btn btn-outline btn-sm" href="{url(lang, "login")}">{t["login"]}</a>' if exists(lang, "login") else ""
    book = book_href(lang)
    sol = menu_links(lang, SOLUTION_GROUPS(t), pid)
    res = menu_links(lang, RESOURCE_GROUPS, pid)
    mobile = []
    if exists(lang, "how-it-works"):
        mobile.append(f'<li><a href="{url(lang, "how-it-works")}">{t["how"]}</a></li>')
    for label, block in ((t["solutions"], sol), (t["resources"], res)):
        if block:
            links = re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)', block)
            sub = "".join(f'<li class="mobile-sub"><a href="{h}">{x}</a></li>' for h, x in links)
            mobile.append(f'<li><span class="kicker" style="display:block;padding:22px 0 6px">{label}</span></li>{sub}')
    if exists(lang, "pricing"):
        mobile.append(f'<li><a href="{url(lang, "pricing")}">{t["pricing"]}</a></li>')
    if exists(lang, "contact"):
        mobile.append(f'<li><a href="{url(lang, "contact")}">{t["contact"]}</a></li>')
    mobile_langs = f'<div class="mobile-langs">{lang_links(lang, pid, True)}</div>' if len(available(pid)) > 1 else ""
    mobile_login = f'<a class="btn btn-outline" href="{url(lang, "login")}">{t["login"]}</a>' if exists(lang, "login") else ""
    return f'''<a class="skip-link" href="#main">{t["skip"]}</a>
<header class="site-header" data-header>
<nav class="nav-pill" aria-label="{t["nav_label"]}">
<a class="brand" href="{url(lang, "home")}" aria-label="KORTEX">{LOGO}<span>KORTEX</span></a>
<ul class="nav-links">{"".join(items)}</ul>
<div class="nav-actions">{langs}
<button class="icon-btn" type="button" data-theme-toggle aria-pressed="false" aria-label="{t["theme"]}">{icon("sun", "theme-icon-light")}{icon("moon", "theme-icon-dark")}</button>
{login}<a class="btn btn-primary btn-sm" href="{book}" data-track="nav-book">{t["book"]}</a>
<button class="icon-btn nav-burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="{t["menu"]}" data-mobile-open>{icon("menu")}</button>
</div>
</nav>
<div class="mobile-menu" id="mobile-menu" hidden>
<button class="icon-btn mobile-close" type="button" aria-label="{t["close"]}" data-mobile-close>{icon("close")}</button>
<ul>{"".join(mobile)}</ul>
<div class="mobile-foot">{mobile_langs}{mobile_login}<a class="btn btn-primary" href="{book}" data-track="mobile-book">{t["book"]}</a></div>
</div>
</header>'''


def book_href(lang):
    return url(lang, "contact") if exists(lang, "contact") else url(lang, "audit")


def footer(lang):
    t = UI[lang]

    def col(title, entries):
        lis = "".join(f'<li><a href="{url(lang, pid)}">{label}</a></li>' for pid, label in entries if exists(lang, pid))
        return f'<div class="footer-col"><h2>{title}</h2><ul>{lis}</ul></div>' if lis else ""

    tup = lambda pid: t[pid][0]
    cols = [
        col(t["col_product"], [("how-it-works", t["how"]), ("pricing", t["pricing"]), ("audit", t["audit"]), ("security", t["security"])]),
        col(t["col_solutions"], [(p, tup(p)) for p in ["b2b", "creators", "ecommerce", "from-blog", "from-youtube", "from-podcast", "from-webinar"]]),
        col(t["col_resources"], [("blog", t["blog"]), ("glossary", t["glossary"]), ("compare", t["compare"])]),
        col(t["col_company"], [("about", t["about"]), ("contact", t["contact"]), ("login", t["login"])]),
    ]
    legal = "".join(f'<a href="{url(lang, p)}">{t[p]}</a>' for p in ["privacy", "terms", "cookies"] if exists(lang, p))
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer-grid">
<div class="footer-brand"><a class="brand" href="{url(lang, "home")}">{LOGO}<span>KORTEX</span></a><p>{t["footer_blurb"]}</p><p>{t["footer_place"]}</p>
<p><a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><a class="text-link" href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></p></div>
{"".join(cols)}
</div>
<div class="footer-bottom"><span>&copy; 2026 {t["rights"]}</span><nav aria-label="Legal">{legal}</nav></div>
</div>
</footer>'''


def cta_band(lang):
    t = UI[lang]
    audit = f'<a class="btn btn-ghost" href="{url(lang, "audit")}" data-track="band-audit">{t["audit"]}</a>' if exists(lang, "audit") else ""
    return f'''<section class="cta-band" aria-labelledby="cta-band-title">
<div class="wrap">
<span class="eyebrow">{t["cta_kicker"]}</span>
<h2 id="cta-band-title">{t["cta_title"]}</h2>
<p>{t["cta_text"]}</p>
<div class="hero-actions"><a class="btn btn-primary" href="{book_href(lang)}" data-track="band-book">{t["book"]}{icon("arrow", "flip")}</a>{audit}</div>
<p class="hero-note">{t["cta_terms"]}</p>
</div>
</section>'''


def resolve(body, lang):
    def block(m):
        pid = m.group(1)
        return m.group(2) if exists(lang, pid) else ""

    body = re.sub(r"<!--if:([a-z0-9-]+)-->(.*?)<!--endif-->", block, body, flags=re.S)

    def anchor(m):
        pid, inner = m.group(1), m.group(2)
        if pid in PAGES and exists(lang, pid):
            return m.group(0)
        return inner

    body = re.sub(r'<a[^>]*?href="@([a-z0-9-]+)[^"]*"[^>]*>(.*?)</a>', anchor, body, flags=re.S)
    body = re.sub(r'(href|action)="@([a-z0-9-]+)', lambda m: f'{m.group(1)}="{url(lang, m.group(2))}', body)
    body = body.replace("@@book", book_href(lang))
    body = body.replace("@@email", EMAIL)
    body = body.replace("@@linkedin", LINKEDIN)
    body = body.replace("@@web3forms", WEB3FORMS_KEY)
    body = re.sub(r"\{\{icon:([a-z]+)(?:\|([a-z -]+))?\}\}", lambda m: icon(m.group(1), m.group(2) or ""), body)
    body = body.replace("{{cta_band}}", cta_band(lang))
    return body


def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def faq_entities(body):
    items = re.findall(r'<details class="faq-item"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq-a">(.*?)</div>\s*</details>', body, flags=re.S)
    return [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for q, a in items
    ]


def schema(lang, pid, meta, body):
    org_id = DOMAIN + "/#organization"
    person_id = DOMAIN + "/#founder"
    page_url = abs_url(lang, pid)
    graph = [
        {
            "@type": "Organization",
            "@id": org_id,
            "name": "KORTEX",
            "url": DOMAIN + "/",
            "logo": DOMAIN + "/logo.svg",
            "email": EMAIL,
            "description": "KORTEX is a GEO, SEO and content creation studio. It turns one source, such as a blog post, YouTube video, podcast episode or webinar, into 30+ assets built to be cited by AI answer engines and ranked by search engines.",
            "founder": {"@id": person_id},
            "address": {"@type": "PostalAddress", "addressLocality": "Fès", "addressCountry": "MA"},
            "areaServed": "Worldwide",
            "knowsLanguage": ["en", "fr", "ar"],
            "sameAs": [LINKEDIN],
            "knowsAbout": ["Generative Engine Optimization", "Answer Engine Optimization", "Search Engine Optimization", "Content strategy", "AI citation tracking"],
        },
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "KORTEX", "inLanguage": ["en", "fr", "ar"], "publisher": {"@id": org_id}},
        {
            "@type": "WebPage",
            "@id": page_url + "#webpage",
            "url": page_url,
            "name": meta["title"],
            "description": meta["description"],
            "inLanguage": lang,
            "isPartOf": {"@id": DOMAIN + "/#website"},
            "about": {"@id": org_id},
            "dateModified": meta.get("modified", BUILD_DATE),
        },
    ]
    crumbs = [{"@type": "ListItem", "position": 1, "name": UI[lang]["home_crumb"], "item": abs_url(lang, "home")}]
    if pid != "home":
        crumbs.append({"@type": "ListItem", "position": 2, "name": meta.get("crumb", meta["title"]), "item": page_url})
    graph.append({"@type": "BreadcrumbList", "@id": page_url + "#breadcrumb", "itemListElement": crumbs})
    extras = [x.strip() for x in meta.get("schema", "").split(",") if x.strip()]
    if "person" in extras:
        graph.append({
            "@type": "Person",
            "@id": person_id,
            "name": "Hamza Bentarhlia",
            "jobTitle": "Founder",
            "worksFor": {"@id": org_id},
            "homeLocation": {"@type": "Place", "name": "Fès, Morocco"},
            "sameAs": [LINKEDIN],
            "knowsAbout": ["Customer retention", "Business intelligence", "Automation", "Generative Engine Optimization"],
        })
    if "service" in extras:
        offers = [("GHOST", "2500"), ("SWARM", "5500"), ("TITAN", "12000")]
        graph.append({
            "@type": "Service",
            "@id": DOMAIN + "/#service",
            "name": "KORTEX GEO, SEO and content system",
            "serviceType": "Generative Engine Optimization",
            "provider": {"@id": org_id},
            "areaServed": "Worldwide",
            "offers": [
                {
                    "@type": "Offer",
                    "name": name,
                    "priceCurrency": "EUR",
                    "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "EUR", "unitText": "MONTH", **({"minPrice": price} if name == "TITAN" else {})},
                }
                for name, price in offers
            ],
        })
    faqs = faq_entities(body)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": page_url + "#faq", "mainEntity": faqs})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(lang, pid, meta, body, critical, css_v, js_v):
    alts = available(pid)
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(l, pid)}">' for l in alts)
    if "en" in alts:
        hreflang += f'<link rel="alternate" hreflang="x-default" href="{abs_url("en", pid)}">'
    robots = '<meta name="robots" content="noindex, follow">' if meta.get("noindex") else ""
    fonts = ["alexandria-arabic"] if lang == "ar" else ["archivo-display", "inter"]
    preload = "".join(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for f in fonts)
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in alts if l != lang)
    title = html.escape(meta["title"], quote=True)
    desc = html.escape(meta["description"], quote=True)
    image = DOMAIN + meta.get("image", "/og-image.png")
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{abs_url(lang, pid)}">
{hreflang}
<meta name="theme-color" content="#0e0907" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#faf4ec" media="(prefers-color-scheme: light)">
<meta property="og:type" content="{meta.get("og_type", "website")}">
<meta property="og:site_name" content="KORTEX">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{abs_url(lang, pid)}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[lang]}">{og_alt}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<script>(function(d){{d.classList.add("js");try{{var t=localStorage.getItem("kx-theme");if(t==="light"||t==="dark")d.dataset.theme=t}}catch(e){{}}}})(document.documentElement)</script>
{preload}
<style>{critical}</style>
<link rel="preload" href="/assets/css/site.css?v={css_v}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/assets/css/site.css?v={css_v}"></noscript>
<script type="module" src="/assets/js/site.js?v={js_v}"></script>
<script type="application/ld+json">{schema(lang, pid, meta, body)}</script>'''


ANALYTICS = f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");addEventListener("load",function(){{setTimeout(function(){{var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id={GA_ID}";document.head.appendChild(s)}},1500)}})</script>'


def render(lang, pid, critical, css_v, js_v):
    meta, body = parse_page(source_path(lang, pid))
    body = resolve(body, lang)
    direction = ' dir="rtl"' if lang == "ar" else ""
    band = "" if meta.get("band") == "no" else cta_band(lang)
    page = f'''<!doctype html>
<html lang="{lang}"{direction}>
<head>
{head(lang, pid, meta, body, critical, css_v, js_v)}
</head>
<body>
{header(lang, pid)}
<main id="main" tabindex="-1">
<div class="ambient" aria-hidden="true"></div>
{body.strip()}
{band}
</main>
{footer(lang)}
{ANALYTICS}
</body>
</html>
'''
    return re.sub(r"\n{2,}", "\n", page)


def output_path(lang, pid):
    rel = url(lang, pid).strip("/")
    return OUT / rel / "index.html" if rel else OUT / "index.html"


def sitemap():
    rows = []
    for pid in PAGES:
        for lang in available(pid):
            meta, _ = parse_page(source_path(lang, pid))
            if meta.get("noindex"):
                continue
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(l, pid)}"/>' for l in available(pid))
            if "en" in available(pid):
                alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{abs_url("en", pid)}"/>'
            rows.append(f'<url><loc>{abs_url(lang, pid)}</loc><lastmod>{meta.get("modified", BUILD_DATE)}</lastmod>{alts}</url>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n"


def main():
    critical = minify_css((SRC / "styles" / "critical.css").read_text(encoding="utf-8"))
    site_css = minify_css((SRC / "styles" / "site.css").read_text(encoding="utf-8"))
    css_out = OUT / "assets" / "css" / "site.css"
    css_out.parent.mkdir(parents=True, exist_ok=True)
    css_out.write_text(site_css, encoding="utf-8")
    js_out = OUT / "assets" / "js" / "site.js"
    js_out.parent.mkdir(parents=True, exist_ok=True)
    js_out.write_text((SRC / "scripts" / "site.js").read_text(encoding="utf-8"), encoding="utf-8")
    css_v, js_v = asset_version(css_out), asset_version(js_out)
    built = 0
    for pid in PAGES:
        for lang in available(pid):
            target = output_path(lang, pid)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(lang, pid, critical, css_v, js_v), encoding="utf-8")
            built += 1
    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print(f"built {built} pages")


if __name__ == "__main__":
    main()
