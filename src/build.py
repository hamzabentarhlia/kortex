import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import urllib.parse
from pathlib import Path

import art
import visuals

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
GA_ID = "G-4440VPDMPW"
CAL_LINK = "hamza-bentarhlia"
CAL_URL = "https://cal.com/" + CAL_LINK
SITE = json.loads((Path(__file__).resolve().parent.parent / "data" / "site.json").read_text(encoding="utf-8"))
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEMO = json.loads((DATA_DIR / "demo.json").read_text(encoding="utf-8"))
PAGECLIP = "https://send.pageclip.co/"
CONTACT_ACTION = PAGECLIP + SITE["contactFormKey"]
LEADS_ACTION = PAGECLIP + (SITE["leadsFormKey"] or SITE["contactFormKey"])
INDEXNOW_KEY = "6f1c9b2e8a4d47f3b0e5c7a19d2f4e83"
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
    "audit": "/audit/",
    "checklist": "/checklist/",
    "proof": "/proof/",
    "thanks": "/thanks/",
    "thanks-audit": "/thanks-audit/",
    "about": "/about/",
    "compare": "/compare/",
    "case-studies": "/case-studies/",
    "security": "/security/",
    "glossary": "/glossary/",
    "resources": "/resources/",
    "blog": "/blog/",
    "contact": "/contact/",
    "privacy": "/legal/privacy/",
    "terms": "/legal/terms/",
    "cookies": "/legal/cookies/",
    "login": "/login/",
    "404": "/404/",
}

HUBS = {"blog": "blog", "glossary": "glossary", "compare": "compare", "solutions": "solutions"}

for _file in sorted((Path(__file__).resolve().parent / "pages").glob("*/*/*.html")):
    _id = f"{_file.parent.name}/{_file.stem}"
    PAGES.setdefault(_id, f"/{_id}/")

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
        "book_bar": "30-minute call",
        "see_pricing": "See pricing",
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
        "consent_label": "Cookie choice", "consent_text": "We use Google Analytics cookies to count visits, only if you agree. The site works the same either way.", "consent_more": "Cookie details", "consent_yes": "Accept", "consent_no": "Decline", "consent_settings": "Cookie settings",
        "cta_kicker": "Next step",
        "cta_title": "Make your expertise the answer",
        "cta_text": "Tell us where your expertise lives today. We show you where AI engines already mention your field, and what it would take for them to mention you.",
        "cta_terms": "No setup fees. No commitment.",
        "home_crumb": "Home",
        "photo_alt": "Hamza Bentarhlia, founder of KORTEX",
        "book_note": "30 minutes, no deck, you leave with three fixes whether we work together or not.",
        "audit": "AI Citation Audit",
        "checklist": "GEO Audit Checklist",
        "proof": "Citation log",
        "audit_cta": "Get the AI Citation Audit, €490",
        "audit_cta_short": "AI Citation Audit, €490",
        "audit_note": "Credited in full against your first month on any plan.",
        "post_kicker": "Next step",
        "post_audit_title": "Want this tested on your own site?",
        "post_audit_text": "The AI Citation Audit tests your brand on 40 buyer questions in four engines and tells you what to fix first. 490 euros, five business days, credited against your first month.",
        "post_call_title": "Want this applied to your own expertise?",
        "post_call_text": "Book a 30-minute call. We look at where AI engines mention your field today and what it would take for them to mention you.",
        "nl_title": "One GEO teardown, twice a month",
        "nl_text": "One teardown of how a real page gets cited in AI answers, and what changed in AI search. Twice a month, no filler.",
        "nl_label": "Work email",
        "nl_btn": "Subscribe",
        "nl_ok": "You are on the list. Check your inbox to confirm.",
        "nl_err": "That did not send. Check your connection and try again.",
        "nl_close": "Close",
        "nl_slide_title": "Get the next teardown",
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
        "book_bar": "Appel de 30 minutes",
        "see_pricing": "Voir les tarifs",
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
        "consent_label": "Choix des cookies", "consent_text": "Nous utilisons les cookies de Google Analytics pour compter les visites, seulement si vous l'acceptez. Le site fonctionne de la même façon dans les deux cas.", "consent_more": "Détails sur les cookies", "consent_yes": "Accepter", "consent_no": "Refuser", "consent_settings": "Paramètres des cookies",
        "cta_kicker": "Prochaine étape",
        "cta_title": "Faites de votre expertise la réponse",
        "cta_text": "Dites-nous où vit votre expertise aujourd'hui. Nous vous montrons où les moteurs IA parlent déjà de votre domaine, et ce qu'il faudrait pour qu'ils parlent de vous.",
        "cta_terms": "Sans frais d'installation. Sans engagement.",
        "home_crumb": "Accueil",
        "photo_alt": "Hamza Bentarhlia, fondateur de KORTEX",
        "book_note": "30 minutes, sans présentation, vous repartez avec trois corrections concrètes, que nous travaillions ensemble ou non.",
        "audit": "Audit de citations IA",
        "checklist": "Checklist d'audit GEO",
        "proof": "Journal des citations",
        "audit_cta": "Commander l'audit de citations IA, 490 €",
        "audit_cta_short": "Audit de citations IA, 490 €",
        "audit_note": "Déduit en totalité de votre premier mois, quelle que soit l'offre.",
        "post_kicker": "Étape suivante",
        "post_audit_title": "Envie de le tester sur votre propre site ?",
        "post_audit_text": "L'audit de citations IA teste votre marque sur 40 questions d'acheteurs dans quatre moteurs et vous dit quoi corriger en premier. 490 euros, cinq jours ouvrés, déduits de votre premier mois.",
        "post_call_title": "Envie de l'appliquer à votre propre expertise ?",
        "post_call_text": "Réservez un appel de 30 minutes. Nous regardons où les moteurs d'IA parlent aujourd'hui de votre domaine et ce qu'il faudrait pour qu'ils parlent de vous.",
        "nl_title": "Une analyse GEO, deux fois par mois",
        "nl_text": "L'analyse d'une vraie page citée dans les réponses d'IA, et ce qui a changé dans la recherche IA. Deux fois par mois, sans remplissage.",
        "nl_label": "E-mail professionnel",
        "nl_btn": "S'abonner",
        "nl_ok": "Vous êtes inscrit. Vérifiez votre boîte de réception pour confirmer.",
        "nl_err": "L'envoi a échoué. Vérifiez votre connexion et réessayez.",
        "nl_close": "Fermer",
        "nl_slide_title": "Recevoir la prochaine analyse",
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
        "book_bar": "مكالمة من 30 دقيقة",
        "see_pricing": "اطلع على الأسعار",
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
        "consent_label": "اختيار ملفات تعريف الارتباط", "consent_text": "نستخدم ملفات تعريف الارتباط من Google Analytics لإحصاء الزيارات، وذلك فقط إن وافقت. ويعمل الموقع بالطريقة نفسها في الحالتين.", "consent_more": "تفاصيل ملفات تعريف الارتباط", "consent_yes": "قبول", "consent_no": "رفض", "consent_settings": "إعدادات ملفات تعريف الارتباط",
        "cta_kicker": "الخطوة التالية",
        "cta_title": "اجعل خبرتك هي الإجابة",
        "cta_text": "أخبرنا أين توجد خبرتك اليوم. سنريك أين تذكر محركات الذكاء الاصطناعي مجالك حاليا، وما الذي يلزم لكي تذكرك أنت.",
        "cta_terms": "بدون رسوم إعداد. بدون التزام.",
        "home_crumb": "الرئيسية",
        "photo_alt": "حمزة بنتغليا، مؤسس KORTEX",
        "book_note": "30 دقيقة دون عرض تقديمي، وتخرج بثلاثة إصلاحات سواء عملنا معا أم لا.",
        "post_kicker": "الخطوة التالية",
        "post_audit_title": "هل تريد تجربة هذا على موقعك؟",
        "post_audit_text": "يختبر تدقيق الاستشهادات علامتك على 40 سؤالا من أسئلة المشترين في أربعة محركات ويخبرك بما تصلحه أولا.",
        "post_call_title": "هل تريد تطبيق هذا على خبرتك؟",
        "post_call_text": "احجز مكالمة من 30 دقيقة. نرى أين تذكر محركات الذكاء الاصطناعي مجالك اليوم، وما الذي يلزم لتذكرك.",
        "nl_title": "تحليل واحد لـ GEO، مرتين في الشهر",
        "nl_text": "تحليل لصفحة حقيقية يُستشهد بها في إجابات الذكاء الاصطناعي، وما تغيّر في البحث بالذكاء الاصطناعي. مرتين في الشهر، دون حشو.",
        "nl_label": "البريد المهني",
        "nl_btn": "اشترك",
        "nl_ok": "تم تسجيلك. تحقق من بريدك لتأكيد الاشتراك.",
        "nl_err": "لم يُرسل الطلب. تحقق من اتصالك وحاول مرة أخرى.",
        "nl_close": "إغلاق",
        "nl_slide_title": "احصل على التحليل القادم",
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

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><defs><radialGradient id="kxg" cx="70%" cy="75%" r="70%"><stop offset="0" stop-color="#FF8576"/><stop offset=".55" stop-color="#FF6B5B"/><stop offset="1" stop-color="#FF6B5B"/></radialGradient></defs><rect width="32" height="32" rx="9" fill="url(#kxg)"/><path d="M11 8.5v15M11 16l9-7.5M13.8 13.6l7.2 9.9" stroke="#14213D" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg>'


art.ICON_PATHS = ICONS
visuals.kit.ICONS = ICONS


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def source_path(lang, pid):
    return SRC / "pages" / lang / f"{pid}.html"


_EXISTS = {}


def exists(lang, pid):
    key = (lang, pid)
    if key not in _EXISTS:
        path = source_path(lang, pid)
        draft = path.exists() and "\ndraft: yes\n" in path.read_text(encoding="utf-8").split("\n---\n", 1)[0] + "\n"
        _EXISTS[key] = path.exists() and (not draft or os.environ.get("KX_DRAFTS") == "1")
    return _EXISTS[key]


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
    menu = f'<div class="nav-menu" id="menu-{key}" hidden>{links}</div>'
    if exists(lang, key):
        cur = ' aria-current="page"' if current == key else ""
        return (
            f'<li class="nav-split"><a class="nav-link" href="{url(lang, key)}"{cur}>{label}</a>'
            f'<button class="nav-caret" type="button" aria-expanded="false" aria-controls="menu-{key}" data-menu-toggle aria-label="{label}">{icon("chevron")}</button>{menu}</li>'
        )
    return (
        f'<li><button class="nav-link" type="button" aria-expanded="false" aria-controls="menu-{key}" data-menu-toggle>{label}{icon("chevron")}</button>{menu}</li>'
    )


SOLUTION_GROUPS = lambda t: [(t["by_audience"], ["b2b", "creators", "ecommerce"]), (t["by_source"], ["from-blog", "from-youtube", "from-podcast", "from-webinar"])]
RESOURCE_GROUPS = [(None, ["resources", "blog", "glossary", "compare", "about"])]


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
{login}<a class="btn btn-primary btn-sm" href="{book}" {BOOK_ATTRS} data-track="nav-book">{t["book"]}</a>
<button class="icon-btn nav-burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="{t["menu"]}" data-mobile-open>{icon("menu")}</button>
</div>
</nav>
<div class="mobile-menu" id="mobile-menu" hidden>
<button class="icon-btn mobile-close" type="button" aria-label="{t["close"]}" data-mobile-close>{icon("close")}</button>
<ul>{"".join(mobile)}</ul>
<div class="mobile-foot">{mobile_langs}{mobile_login}<a class="btn btn-primary" href="{book}" {BOOK_ATTRS} data-track="mobile-book">{t["book"]}</a></div>
</div>
</header>'''


def book_href(lang):
    return f"{CAL_URL}?lng={lang}"


def book_bar(lang, pid):
    if pid in ("contact", "login", "404", "privacy", "terms", "cookies", "thanks", "thanks-audit"):
        return ""
    t = UI[lang]
    return f'<div class="book-bar" data-bookbar><span>{t["book_bar"]}</span><a class="btn btn-primary btn-sm" href="{book_href(lang)}" {BOOK_ATTRS} data-track="bar-book">{t["book"]}</a></div>'


BOOK_ATTRS = f'data-cal="{CAL_LINK}" rel="noopener"'


PHOTO = {
    "portrait": ("founder-portrait", [480, 608], (608, 760), "(min-width: 960px) 440px, 90vw"),
    "wide": ("founder-wide", [640, 1080], (1080, 608), "(min-width: 1200px) 1100px, 100vw"),
    "avatar": ("founder-avatar", [64, 128, 256], (256, 256), "88px"),
}


def photo(lang, kind, eager=False):
    base, widths, (w, h), sizes = PHOTO[kind]
    alt = UI[lang]["photo_alt"]
    srcset = lambda ext: ", ".join(f"/assets/img/{base}-{x}.{ext} {x}w" for x in widths)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
        f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
        f'<img src="/assets/img/{base}-{widths[-1]}.jpg" srcset="{srcset("jpg")}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {loading}></picture>'
    )


def footer(lang):
    t = UI[lang]

    def col(title, entries):
        lis = "".join(f'<li><a href="{url(lang, pid)}">{label}</a></li>' for pid, label in entries if exists(lang, pid))
        return f'<div class="footer-col"><h2>{title}</h2><ul>{lis}</ul></div>' if lis else ""

    tup = lambda pid: t[pid][0]
    cols = [
        col(t["col_product"], [("how-it-works", t["how"]), ("pricing", t["pricing"]), ("audit", t.get("audit", "")), ("checklist", t.get("checklist", "")), ("proof", t.get("proof", "")), ("security", t["security"])]),
        col(t["col_solutions"], [(p, tup(p)) for p in ["b2b", "creators", "ecommerce", "from-blog", "from-youtube", "from-podcast", "from-webinar"]]),
        col(t["col_resources"], [("resources", t["resources"]), ("blog", t["blog"]), ("glossary", t["glossary"]), ("compare", t["compare"])]),
        col(t["col_company"], [("about", t["about"]), ("contact", t["contact"]), ("login", t["login"])]),
    ]
    legal = "".join(f'<a href="{url(lang, p)}">{t[p]}</a>' for p in ["privacy", "terms", "cookies"] if exists(lang, p))
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer-nl">{newsletter_block(lang, "footer", "footer")}</div>
<div class="footer-grid">
<div class="footer-brand"><a class="brand" href="{url(lang, "home")}">{LOGO}<span>KORTEX</span></a><p>{t["footer_blurb"]}</p><p>{t["footer_place"]}</p>
<p><a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><a class="text-link" href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></p></div>
{"".join(cols)}
</div>
<div class="footer-bottom"><span>&copy; 2026 {t["rights"]}</span><nav aria-label="Legal">{legal}<button type="button" class="link-btn" data-consent-open>{t["consent_settings"]}</button></nav></div>
</div>
</footer>'''



CHECKLIST = json.loads((Path(__file__).resolve().parent.parent / "data" / "checklist.json").read_text(encoding="utf-8"))
CHECKLIST_FORM = {
    "en": {"label": "Work email", "btn": "Send me the checklist", "note": "One email with the PDF link, then the twice-monthly teardown. Unsubscribe any time.", "err": "That did not send. Check your connection and try again."},
    "fr": {"label": "E-mail professionnel", "btn": "Recevoir la checklist", "note": "Un e-mail avec le lien du PDF, puis l'analyse bimensuelle. Désinscription à tout moment.", "err": "L'envoi a échoué. Vérifiez votre connexion et réessayez."},
}


def checklist_items(lang):
    code = lang if lang in ("en", "fr") else "en"
    n = 0
    out = []
    for group in CHECKLIST["groups"]:
        items = []
        for c in CHECKLIST["checks"]:
            if c["group"] != group["id"]:
                continue
            n += 1
            items.append(f'<li><span class="ck-n">{n}</span><span>{html.escape(c[code]["title"])}</span></li>')
        out.append(f'<section class="glass card ck-group" aria-labelledby="ck-{group["id"]}"><h3 id="ck-{group["id"]}">{html.escape(group[code])}</h3><ol class="ck-list" start="{n - len(items) + 1}">{"".join(items)}</ol></section>')
    return f'<div class="grid grid-2 ck-grid">{"".join(out)}</div>'


def checklist_form(lang, place):
    code = lang if lang in ("en", "fr") else "en"
    f = CHECKLIST_FORM[code]
    NL_COUNTER[0] += 1
    fid = f"ck-{NL_COUNTER[0]}"
    thanks = url(lang, "thanks") + "?f=checklist"
    return (
        f'<form class="nl-form ck-form pageclip-form" action="{LEADS_ACTION}" method="post" data-lead-form data-form-name="checklist" data-track-form="checklist" data-thanks="{thanks}">'
        f'{lead_fields("checklist", lang, "checklist")}'
        f'<label class="visually-hidden" for="{fid}">{f["label"]}</label>'
        f'<div class="nl-row"><input id="{fid}" type="email" name="email" required autocomplete="email" inputmode="email" placeholder="{f["label"]}">'
        f'<button class="btn btn-primary pageclip-form__submit" type="submit" data-cta="checklist-{place}">{f["btn"]}</button></div>'
        f'<p class="form-note">{f["note"]}</p>'
        f'<p class="nl-status is-error" data-form-error hidden role="alert">{f["err"]}</p></form>'
    )


PROOF = json.loads((Path(__file__).resolve().parent.parent / "data" / "citations.json").read_text(encoding="utf-8"))
CASES = json.loads((Path(__file__).resolve().parent.parent / "data" / "case-studies.json").read_text(encoding="utf-8"))
PROOF_TEXT = {
    "en": {"date": "Date", "engine": "Engine and surface", "question": "Question", "named": "Named", "cited": "Cited", "others": "Others cited", "yes": "Yes", "no": "No", "none": "The first dated run has not been published yet. When it is, the full results land here: every question, every engine, what we found and what we changed.", "caption": "Citation log for kortexlab.me", "changes": "Date", "change": "What changed", "case_none": "No case study is published yet. This page is the layout future case studies will use, and it stays out of the sitemap and the navigation until a real one exists.", "challenge": "Challenge", "approach": "Approach", "results": "Results", "quote": "In the client's words", "asof": "Measured"},
    "fr": {"date": "Date", "engine": "Moteur et interface", "question": "Question", "named": "Nommé", "cited": "Cité", "others": "Autres cités", "yes": "Oui", "no": "Non", "none": "La première série datée n'est pas encore publiée. Quand elle le sera, les résultats complets arriveront ici : chaque question, chaque moteur, ce que nous avons trouvé et ce que nous avons changé.", "caption": "Journal des citations de kortexlab.me", "changes": "Date", "change": "Ce qui a changé", "case_none": "Aucune étude de cas n'est encore publiée. Cette page est la mise en page que les futures études de cas utiliseront, et elle reste hors du sitemap et de la navigation tant qu'une vraie étude n'existe pas.", "challenge": "Enjeu", "approach": "Approche", "results": "Résultats", "quote": "Dans les mots du client", "asof": "Mesuré"},
}


def proof_log(lang):
    t = PROOF_TEXT.get(lang, PROOF_TEXT["en"])
    runs = PROOF["runs"]
    if not runs:
        return f'<div class="glass card"><p>{t["none"]}</p></div>'
    rows = "".join(
        f'<tr><td>{html.escape(r["date"])}</td><td>{html.escape(r["engine"])}</td><td>{html.escape(r["question"])}</td><td>{t["yes"] if r["named"] else t["no"]}</td><td>{t["yes"] if r["cited"] else t["no"]}</td><td>{html.escape(r.get("others", ""))}</td></tr>'
        for r in runs
    )
    return (
        f'<div class="tbl-wrap"><table class="tbl proof-log"><caption class="visually-hidden">{t["caption"]}</caption>'
        f'<thead><tr><th scope="col">{t["date"]}</th><th scope="col">{t["engine"]}</th><th scope="col">{t["question"]}</th><th scope="col">{t["named"]}</th><th scope="col">{t["cited"]}</th><th scope="col">{t["others"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
    )


def proof_screens(lang):
    shots = [r for r in PROOF["runs"] if r.get("screenshot")]
    if not shots:
        return ""
    figs = "".join(f'<figure class="glass card" style="margin:0"><img src="{html.escape(r["screenshot"])}" alt="{html.escape(r["engine"] + " , " + r["date"])}" loading="lazy" width="640" height="400"><figcaption class="vx-caption">{html.escape(r["engine"])}, {html.escape(r["date"])}</figcaption></figure>' for r in shots)
    return f'<div class="grid grid-2">{figs}</div>'


def proof_changelog(lang):
    t = PROOF_TEXT.get(lang, PROOF_TEXT["en"])
    code = lang if lang in ("en", "fr") else "en"
    rows = "".join(f'<tr><td>{html.escape(c["date"])}</td><td>{html.escape(c[code])}</td></tr>' for c in sorted(PROOF["changelog"], key=lambda c: c["date"], reverse=True))
    return f'<div class="tbl-wrap"><table class="tbl"><caption class="visually-hidden">Changelog</caption><thead><tr><th scope="col">{t["changes"]}</th><th scope="col">{t["change"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'


def case_studies(lang):
    t = PROOF_TEXT.get(lang, PROOF_TEXT["en"])
    if not CASES:
        return f'<div class="glass card"><p>{t["case_none"]}</p></div>'
    out = []
    for c in CASES:
        results = "".join(f'<li>{icon("check")}<span><strong>{html.escape(r["metric"])}</strong> {html.escape(r["value"])} <small>{t["asof"]} {html.escape(r["date"])}</small></span></li>' for r in c["results"])
        quote = f'<blockquote class="glass card"><p>{html.escape(c["quote"]["text"])}</p><footer>{html.escape(c["quote"]["by"])}</footer></blockquote>' if c.get("quote") else ""
        out.append(
            f'<article class="glass card"><h2>{html.escape(c["title"])}</h2><h3>{t["challenge"]}</h3><p>{html.escape(c["challenge"])}</p>'
            f'<h3>{t["approach"]}</h3><p>{html.escape(c["approach"])}</p><h3>{t["results"]}</h3><ul class="checklist">{results}</ul>{quote}</article>'
        )
    return "".join(out)


DEMO_TEXT = {
    "en": {
        "eyebrow": "See it run",
        "title": "Watch one source become ten assets",
        "lead": "Pick a sample source and run the pipeline. Everything here is example content, so you can see the stages and the output without sending us anything.",
        "choose": "Choose a sample source",
        "run": "Run the pipeline",
        "replay": "Replay",
        "caption": "Sample run with example content",
        "example": "Example",
        "count": "10 assets from one source, the size of a GHOST month. SWARM runs 20 to 24 per source.",
        "done": "Run complete. 10 assets ready for review.",
        "assets": "Assets from this source",
        "stages": "Pipeline stages",
        "open": "Open an asset to read an example excerpt",
    },
    "fr": {
        "eyebrow": "Voyez-le tourner",
        "title": "Regardez une source devenir dix contenus",
        "lead": "Choisissez une source d'exemple et lancez la chaîne. Tout ici est du contenu d'exemple : vous voyez les étapes et le résultat sans rien nous envoyer.",
        "choose": "Choisir une source d'exemple",
        "run": "Lancer la chaîne",
        "replay": "Rejouer",
        "caption": "Essai avec du contenu d'exemple",
        "example": "Exemple",
        "count": "10 contenus à partir d'une source, la taille d'un mois GHOST. SWARM en produit 20 à 24 par source.",
        "done": "Essai terminé. 10 contenus prêts pour la relecture.",
        "assets": "Contenus issus de cette source",
        "stages": "Étapes de la chaîne",
        "open": "Ouvrez un contenu pour lire un extrait d'exemple",
    },
}


def demo_block(lang):
    if lang not in DEMO_TEXT:
        return ""
    t = DEMO_TEXT[lang]
    first = DEMO["sources"][0]
    chips = "".join(
        f'<label class="demo-chip"><input type="radio" name="demo-source" value="{src["id"]}"{" checked" if i == 0 else ""}><span>{icon(src["icon"])}{html.escape(src[lang]["label"])}</span></label>'
        for i, src in enumerate(DEMO["sources"])
    )
    stages = "".join(
        f'<li class="ds" data-i="{i}"><span class="ds-dot" aria-hidden="true"></span><span class="ds-name">{html.escape(n)}</span><span class="ds-log">{html.escape(first["logs"][lang][i])}</span></li>'
        for i, n in enumerate(DEMO["stages"][lang])
    )
    cards = []
    for k, key in enumerate(DEMO["labels"][lang]):
        n = DEMO["counts"][key]
        badge = f'<span class="dc-n">x{n}</span>' if n > 1 else ""
        mono = " dc-mono" if key == "schema" else ""
        cards.append(
            f'<li><details class="dc"{" open" if k == 0 else ""} data-key="{key}"><summary><span class="dc-name">{html.escape(DEMO["labels"][lang][key])}</span>{badge}</summary>'
            f'<p class="dc-body{mono}">{html.escape(first["cards"][lang][key])}</p></details></li>'
        )
    line_h = '<svg class="demo-line demo-line-h" viewBox="0 0 100 2" preserveAspectRatio="none" aria-hidden="true"><line x1="0" y1="1" x2="100" y2="1" pathLength="1" vector-effect="non-scaling-stroke"/></svg>'
    line_v = '<svg class="demo-line demo-line-v" viewBox="0 0 2 100" preserveAspectRatio="none" aria-hidden="true"><line x1="1" y1="0" x2="1" y2="100" pathLength="1" vector-effect="non-scaling-stroke"/></svg>'
    return (
        f'<section class="section section-tint" data-ix="demo" aria-labelledby="demo-title"><div class="wrap">'
        f'<div class="section-head"><span class="eyebrow">{t["eyebrow"]}</span><h2 id="demo-title">{t["title"]}</h2><p>{t["lead"]}</p></div>'
        f'<div class="demo glass" data-module="demo" data-lang="{lang}" data-state="done" data-run-label="{t["run"]}" data-replay-label="{t["replay"]}" data-done="{t["done"]}">'
        f'<div class="demo-top"><fieldset class="demo-sources"><legend class="visually-hidden">{t["choose"]}</legend>{chips}</fieldset><span class="demo-tag">{t["example"]}</span></div>'
        f'<div class="demo-src"><strong data-demo-title>{html.escape(first[lang]["title"])}</strong><span data-demo-meta>{html.escape(first[lang]["meta"])}</span><p data-demo-desc>{html.escape(first[lang]["desc"])}</p></div>'
        f'<div class="demo-bar"><button class="btn btn-primary demo-run" type="button" data-demo-run data-cta="demo-run">{t["run"]}</button><p class="demo-caption">{t["caption"]}</p></div>'
        f'<div class="demo-flow" role="group" aria-label="{t["stages"]}">{line_h}{line_v}<ol class="demo-stages">{stages}</ol></div>'
        f'<h3 class="demo-h">{t["assets"]}</h3><ul class="demo-cards" aria-label="{t["open"]}">{"".join(cards)}</ul>'
        f'<p class="demo-count">{t["count"]}</p><p class="visually-hidden" role="status" aria-live="polite" data-demo-status></p>'
        f'</div></div></section>'
    )


CALC_TEXT = {
    "en": {
        "eyebrow": "Your numbers",
        "title": "Compare what you spend with what KORTEX costs",
        "lead": "Move the sliders to match how you work today. The numbers update as you go, and nothing leaves this page.",
        "assets": "Assets you need per month",
        "rate": "What you pay per asset today",
        "hours": "Hours you spend on content each week",
        "value": "Value of your time",
        "per_hour": "per hour",
        "current": "Your current monthly cost",
        "kortex": "KORTEX plan for that volume",
        "production": "Production",
        "time": "your time",
        "from": "from",
        "per_month": "per month",
        "verdict_more": "At your volume, {plan} costs more than your current spend. It wins on consistency and citations, not on price.",
        "verdict_less": "At your volume, {plan} costs about {diff} less than your current spend.",
        "verdict_titan": "At your volume, TITAN starts at {price}. Scope and price are set together on a call.",
        "note": "Price does not capture assets built to be cited, with schema, interlinking and a human editor.",
        "fit": "Which plan fits: up to 10 assets a month maps to GHOST, 11 to 24 to SWARM, and 25 or more to TITAN.",
        "book": "Book a strategy call",
        "perasset": {"GHOST": "10 assets, about €250 each.", "SWARM": "20 to 24 assets, about €230 to €275 each.", "TITAN": "28 or more assets per source, two or more sources, about €215 each or less."},
        "price_note": "Rates and hours are your own inputs. This compares budgets, not identical output.",
        "plan_msg": "Plan from the calculator",
    },
    "fr": {
        "eyebrow": "Vos chiffres",
        "title": "Comparez ce que vous dépensez avec ce que coûte KORTEX",
        "lead": "Réglez les curseurs selon votre façon de travailler aujourd'hui. Les chiffres se mettent à jour en direct, et rien ne quitte cette page.",
        "assets": "Contenus dont vous avez besoin par mois",
        "rate": "Ce que vous payez par contenu aujourd'hui",
        "hours": "Heures que vous passez sur le contenu chaque semaine",
        "value": "Valeur de votre temps",
        "per_hour": "de l'heure",
        "current": "Votre coût mensuel actuel",
        "kortex": "L'offre KORTEX pour ce volume",
        "production": "Production",
        "time": "votre temps",
        "from": "dès",
        "per_month": "par mois",
        "verdict_more": "À votre volume, {plan} coûte plus que votre dépense actuelle. Elle l'emporte sur la régularité et les citations, pas sur le prix.",
        "verdict_less": "À votre volume, {plan} coûte environ {diff} de moins que votre dépense actuelle.",
        "verdict_titan": "À votre volume, TITAN démarre à {price}. Le périmètre et le prix se fixent ensemble lors d'un appel.",
        "note": "Le prix ne mesure pas des contenus conçus pour être cités, avec schema, maillage interne et une relecture humaine.",
        "fit": "Quelle offre convient : jusqu'à 10 contenus par mois correspond à GHOST, 11 à 24 à SWARM, et 25 ou plus à TITAN.",
        "book": "Réserver un appel stratégique",
        "perasset": {"GHOST": "10 contenus, environ 250 € chacun.", "SWARM": "20 à 24 contenus, environ 230 à 275 € chacun.", "TITAN": "28 contenus ou plus par source, deux sources ou plus, environ 215 € chacun ou moins."},
        "price_note": "Les tarifs et les heures sont vos propres données. Cela compare des budgets, pas des livrables identiques.",
        "plan_msg": "Offre issue du calculateur",
    },
}
CALC_DEFAULTS = {"assets": 12, "rate": 250, "hours": 4, "value": 60}
CALC_PLANS = {"GHOST": 2500, "SWARM": 5500, "TITAN": 12000}


def calc_plan(assets):
    return "GHOST" if assets <= 10 else "SWARM" if assets <= 24 else "TITAN"


def calc_money(lang, n):
    digits = f"{int(n):,}"
    if lang == "fr":
        return digits.replace(",", " ") + " €"
    return "€" + digits


def calc_numbers(assets, rate, hours, value):
    production = assets * rate
    own_time = int(hours * 52 / 12 * value + 0.5)
    return production, own_time, production + own_time


def calc_block(lang):
    if lang not in CALC_TEXT:
        return ""
    t = CALC_TEXT[lang]
    d = CALC_DEFAULTS
    production, own_time, current = calc_numbers(d["assets"], d["rate"], d["hours"], d["value"])
    plan = calc_plan(d["assets"])
    price = CALC_PLANS[plan]
    m = lambda n: calc_money(lang, n)
    if plan == "TITAN":
        verdict = t["verdict_titan"].format(price=m(price))
    elif price > current:
        verdict = t["verdict_more"].format(plan=plan)
    else:
        verdict = t["verdict_less"].format(plan=plan, diff=m(current - price))
    options = "".join(f'<option value="{v}"{" selected" if v == d["value"] else ""}>{m(v)} {t["per_hour"]}</option>' for v in (30, 60, 100))
    notes = urllib.parse.quote(f'{t["plan_msg"]}: {plan}')
    book = f'{CAL_URL}?lng={lang}&notes={notes}'
    return (
        f'<section class="section" data-ix="calc" aria-labelledby="calc2-title"><div class="wrap">'
        f'<div class="section-head"><span class="eyebrow">{t["eyebrow"]}</span><h2 id="calc2-title">{t["title"]}</h2><p>{t["lead"]}</p></div>'
        f'<div class="calc2 glass" data-module="calc" data-lang="{lang}" data-book="{CAL_URL}?lng={lang}" data-from="{t["from"]}" data-plan-msg="{t["plan_msg"]}" data-i18n="{html.escape(json.dumps({k: t[k] for k in ("verdict_more", "verdict_less", "verdict_titan", "perasset")}, ensure_ascii=False))}">'
        f'<form class="calc2-form" onsubmit="return false">'
        f'<div class="cf"><label for="cx-assets">{t["assets"]}</label><output for="cx-assets" data-out="assets">{d["assets"]}</output><input id="cx-assets" type="range" min="4" max="40" step="1" value="{d["assets"]}" data-key="assets"></div>'
        f'<div class="cf"><label for="cx-rate">{t["rate"]}</label><output for="cx-rate" data-out="rate">{m(d["rate"])}</output><input id="cx-rate" type="range" min="50" max="600" step="10" value="{d["rate"]}" data-key="rate"></div>'
        f'<div class="cf"><label for="cx-hours">{t["hours"]}</label><output for="cx-hours" data-out="hours">{d["hours"]}</output><input id="cx-hours" type="range" min="0" max="20" step="1" value="{d["hours"]}" data-key="hours"></div>'
        f'<div class="cf cf-select"><label for="cx-value">{t["value"]}</label><select id="cx-value" data-key="value">{options}</select></div>'
        f'</form>'
        f'<div class="calc2-out" aria-live="polite" aria-atomic="true">'
        f'<div class="co-grid"><div class="co-col"><h3>{t["current"]}</h3><p class="co-big" data-current>{m(current)}</p><p class="co-sub">{t["production"]} <span data-production>{m(production)}</span>, {t["time"]} <span data-time>{m(own_time)}</span></p></div>'
        f'<div class="co-col"><h3>{t["kortex"]}</h3><p class="co-big"><span class="co-from" data-from-label{" hidden" if plan != "TITAN" else ""}>{t["from"]} </span><span data-plan-price>{m(price)}</span></p><p class="co-sub"><strong data-plan-name>{plan}</strong> {t["per_month"]}. <span data-perasset>{t["perasset"][plan]}</span></p></div></div>'
        f'<p class="co-verdict" data-verdict>{verdict}</p>'
        f'<p class="co-note">{t["note"]}</p><p class="co-note" data-fit>{t["fit"]}</p><p class="co-note">{t["price_note"]}</p>'
        f'<a class="btn btn-primary" href="{book}" {BOOK_ATTRS} data-cta="calc" data-calc-book>{t["book"]}{icon("arrow", "flip")}</a>'
        f'</div></div></div></section>'
    )


TEASER = json.loads((DATA_DIR / "citation-teaser.json").read_text(encoding="utf-8"))
TEASER_TEXT = {
    "en": {
        "eyebrow": "Citation teaser",
        "title": "Ask the question your buyer asks",
        "lead": "Pick a question a buyer in your market would type into an AI assistant. See what kinds of sources an answer draws on, and who tends to get cited.",
        "label": "Pick a buyer question",
        "placeholder": "Choose a question",
        "you": "Buyer",
        "assistant": "AI answer, summarized",
        "sources": "Sources it draws on",
        "checked": "Checked on {date} in {engine}. Sources are described by type, not by brand.",
        "skip": "Show the full answer",
        "industries": {"b2b-saas": "B2B software", "e-commerce": "E-commerce", "agencies": "Agencies", "local-services": "Local services"},
        "form_title": "Get this run for your own brand",
        "form_text": "Send your site and we run one buyer question for your market and send back who gets cited. Free, in 3 business days.",
        "email": "Work email",
        "site": "Website",
        "send": "Send me my run",
        "err": "That did not send. Check your connection and try again.",
        "audit": "Need all 40 questions, faster? See the AI Citation Audit, 490 euros, 5 business days.",
    },
    "fr": {
        "eyebrow": "Aperçu des citations",
        "title": "Posez la question que pose votre acheteur",
        "lead": "Choisissez une question qu'un acheteur de votre marché taperait dans un assistant IA. Voyez sur quels types de sources s'appuie une réponse, et qui tend à être cité.",
        "label": "Choisir une question d'acheteur",
        "placeholder": "Choisir une question",
        "you": "Acheteur",
        "assistant": "Réponse d'IA, résumée",
        "sources": "Sources sur lesquelles elle s'appuie",
        "checked": "Vérifié le {date} dans {engine}. Les sources sont décrites par type, pas par marque.",
        "skip": "Afficher la réponse complète",
        "industries": {"b2b-saas": "Logiciels B2B", "e-commerce": "E-commerce", "agencies": "Agences", "local-services": "Services locaux"},
        "form_title": "Obtenez cet essai pour votre marque",
        "form_text": "Envoyez votre site : nous lançons une question d'acheteur pour votre marché et nous vous renvoyons qui est cité. Gratuit, sous 3 jours ouvrés.",
        "email": "E-mail professionnel",
        "site": "Site web",
        "send": "Recevoir mon essai",
        "err": "L'envoi a échoué. Vérifiez votre connexion et réessayez.",
        "audit": "Besoin des 40 questions, plus vite ? Voir l'audit de citations IA, 490 euros, 5 jours ouvrés.",
    },
}


def teaser_block(lang, pid):
    if not SITE.get("citationTeaser") or lang not in TEASER_TEXT:
        return ""
    entries = [e for e in TEASER["entries"] if e["lang"] == lang]
    unverified = [e["qid"] for e in entries if not e.get("verified") or not e.get("dateChecked") or not e.get("engine")]
    if unverified:
        raise SystemExit("citationTeaser is on but these entries are not verified: " + ", ".join(unverified))
    t = TEASER_TEXT[lang]
    groups = {}
    for e in entries:
        groups.setdefault(e["industry"], []).append(e)
    options = "".join(
        f'<optgroup label="{html.escape(t["industries"][ind])}">' + "".join(f'<option value="{e["qid"]}">{html.escape(e["question"])}</option>' for e in items) + "</optgroup>"
        for ind, items in groups.items()
    )
    static = "".join(
        f'<div class="tz-item"><dt>{html.escape(e["question"])}</dt><dd><strong>{t["sources"]}:</strong> {html.escape(", ".join(e["citedTypes"]))}. {html.escape(e["summary"])}</dd></div>'
        for e in entries
    )
    payload = json.dumps({"entries": entries, "punchline": TEASER["punchline"][lang], "text": {k: t[k] for k in ("you", "assistant", "sources", "checked", "skip")}}, ensure_ascii=False).replace("</", "<\\/")
    NL_COUNTER[0] += 1
    fid = f"tz-{NL_COUNTER[0]}"
    audit = f'<a class="text-link" href="{url(lang, "audit")}" data-cta="teaser-audit">{t["audit"]}</a>' if exists(lang, "audit") else ""
    return (
        f'<section class="section" data-ix="teaser" aria-labelledby="tz-title"><div class="wrap">'
        f'<div class="section-head"><span class="eyebrow">{t["eyebrow"]}</span><h2 id="tz-title">{t["title"]}</h2><p>{t["lead"]}</p></div>'
        f'<div class="tz glass" data-module="teaser" data-lang="{lang}"><script type="application/json" data-tz-data>{payload}</script>'
        f'<div class="tz-ui"><label class="tz-label" for="tz-q">{t["label"]}</label><select id="tz-q" data-tz-select><option value="">{t["placeholder"]}</option>{options}</select>'
        f'<div class="tz-pane" data-tz-pane aria-live="polite"></div></div>'
        f'<dl class="tz-static">{static}</dl>'
        f'<form class="tz-form pageclip-form" action="{LEADS_ACTION}" method="post" data-lead-form data-form-name="teaser" data-track-form="teaser">{lead_fields("teaser", lang, pid)}'
        f'<h3>{t["form_title"]}</h3><p>{t["form_text"]}</p>'
        f'<div class="nl-row"><label class="visually-hidden" for="{fid}-e">{t["email"]}</label><input id="{fid}-e" type="email" name="email" required autocomplete="email" placeholder="{t["email"]}">'
        f'<label class="visually-hidden" for="{fid}-w">{t["site"]}</label><input id="{fid}-w" type="url" name="website" required inputmode="url" placeholder="{t["site"]} (https://)">'
        f'<button class="btn btn-primary pageclip-form__submit" type="submit" data-cta="teaser-lead">{t["send"]}</button></div>'
        f'<p class="nl-status" data-form-ok hidden role="status"></p><p class="nl-status is-error" data-form-error hidden role="alert">{t["err"]}</p></form>'
        f'<p class="tz-audit">{audit}</p></div></div></section>'
    )


NL_COUNTER = [0]


def lead_fields(form_name, lang, pid):
    return (
        f'<input type="hidden" name="form" value="{form_name}"><input type="hidden" name="source" value="{pid}"><input type="hidden" name="language" value="{lang}">'
        '<input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">'
    )


def newsletter_form(lang, pid, place):
    t = UI[lang]
    NL_COUNTER[0] += 1
    fid = f"nl-{NL_COUNTER[0]}"
    return (
        f'<form class="nl-form pageclip-form" action="{LEADS_ACTION}" method="post" data-lead-form data-form-name="newsletter" data-track-form="newsletter">'
        f'{lead_fields("newsletter", lang, pid)}'
        f'<label class="visually-hidden" for="{fid}">{t["nl_label"]}</label>'
        f'<div class="nl-row"><input id="{fid}" type="email" name="email" required autocomplete="email" inputmode="email" placeholder="{t["nl_label"]}">'
        f'<button class="btn btn-primary pageclip-form__submit" type="submit" data-cta="newsletter-{place}">{t["nl_btn"]}</button></div>'
        f'<p class="nl-status" data-form-ok hidden role="status">{t["nl_ok"]}</p>'
        f'<p class="nl-status is-error" data-form-error hidden role="alert">{t["nl_err"]}</p>'
        '</form>'
    )


def newsletter_block(lang, pid, place):
    t = UI[lang]
    inner = f'<div class="nl-copy"><h2 id="nl-title-{place}">{t["nl_title"]}</h2><p>{t["nl_text"]}</p></div>{newsletter_form(lang, pid, place)}'
    if place == "footer":
        return f'<div class="nl-block glass">{inner}</div>'
    return f'<section class="nl-block glass" aria-labelledby="nl-title-{place}">{inner}</section>'


def newsletter_slide(lang, pid):
    t = UI[lang]
    return (
        f'<aside class="nl-slide glass" data-slide hidden aria-labelledby="nl-slide-title"><button class="nl-close" type="button" data-slide-close aria-label="{t["nl_close"]}">{icon("x")}</button>'
        f'<h2 id="nl-slide-title">{t["nl_slide_title"]}</h2><p>{t["nl_text"]}</p>{newsletter_form(lang, pid, "slide")}</aside>'
    )


AUDIT_FORM = {
    "en": {"name": "Name", "company": "Company", "site": "Website or content link", "email": "Work email", "send": "Request the audit", "note": "Payment is taken after a short fit check, not before.", "ok": "Request received.", "err": "That did not send. Check your connection and try again.", "pay": "Pay and start the audit"},
    "fr": {"name": "Nom", "company": "Entreprise", "site": "Site ou lien de contenu", "email": "E-mail professionnel", "send": "Demander l'audit", "note": "Le paiement intervient après un court échange pour vérifier l'adéquation, pas avant.", "ok": "Demande reçue.", "err": "L'envoi a échoué. Vérifiez votre connexion et réessayez.", "pay": "Payer et lancer l'audit"},
}


def audit_request(lang):
    f = AUDIT_FORM.get(lang, AUDIT_FORM["en"])
    if SITE["stripeAuditUrl"]:
        return f'<div class="audit-pay"><a class="btn btn-primary" href="{SITE["stripeAuditUrl"]}" rel="noopener" data-cta="audit-pay" data-audit-pay>{f["pay"]}{icon("arrow", "flip")}</a><p class="form-note">{UI.get(lang, UI["en"]).get("audit_note", UI["en"]["audit_note"])}</p></div>'
    return (
        f'<form class="form pageclip-form" action="{CONTACT_ACTION}" method="post" data-lead-form data-form-name="audit" data-track-form="audit" data-thanks="{url(lang, "thanks-audit")}">'
        f'{lead_fields("audit", lang, "audit")}'
        f'<div class="form-row"><div class="field"><label for="a-name">{f["name"]}</label><input id="a-name" name="name" type="text" required autocomplete="name"></div>'
        f'<div class="field"><label for="a-company">{f["company"]}</label><input id="a-company" name="company" type="text" required autocomplete="organization"></div></div>'
        f'<div class="form-row"><div class="field"><label for="a-site">{f["site"]}</label><input id="a-site" name="website" type="url" required inputmode="url" placeholder="https://"></div>'
        f'<div class="field"><label for="a-email">{f["email"]}</label><input id="a-email" name="email" type="email" required autocomplete="email"></div></div>'
        f'<button class="btn btn-primary pageclip-form__submit" type="submit" data-cta="audit-request">{f["send"]}{icon("arrow", "flip")}</button>'
        f'<p class="form-note">{f["note"]} {UI.get(lang, UI["en"]).get("audit_note", UI["en"]["audit_note"])}</p>'
        f'<p class="form-status is-error" data-form-error hidden role="alert">{f["err"]}</p></form>'
    )


def tag_ctas(page, pid):
    counter = [0]
    medium = pid.replace("/", "-")

    def one(m):
        attrs = m.group(1)
        is_cal = f'href="{CAL_URL}' in attrs
        is_btn = bool(re.search(r'class="[^"]*\bbtn\b', attrs))
        if not (is_cal or is_btn):
            return m.group(0)
        track = re.search(r'data-track="([^"]+)"', attrs)
        existing = re.search(r'data-cta="([^"]+)"', attrs)
        if existing:
            cta = existing.group(1)
        else:
            counter[0] += 1
            cta = track.group(1) if track else f"{medium}-cta{counter[0]}"
            attrs += f' data-cta="{cta}"'
        if is_cal and "utm_source" not in attrs:
            attrs = re.sub(r'href="(' + re.escape(CAL_URL) + r'[^"]*)"', lambda h: f'href="{h.group(1)}&amp;utm_source=site&amp;utm_medium={medium}&amp;utm_campaign={cta}"' if "?" in h.group(1) else f'href="{h.group(1)}?utm_source=site&amp;utm_medium={medium}&amp;utm_campaign={cta}"', attrs, count=1)
        return f"<a{attrs}>"

    return re.sub(r"<a\b([^>]*)>", one, page)


def article_cta(lang, pid, body):
    if not pid.startswith("blog/"):
        return body
    slug = pid.split("/", 1)[1]
    t = UI[lang]
    audit = slug in AUDIT_POSTS and exists(lang, "audit")
    if '<div id="cta">' not in body:
        if audit:
            block = f'<div id="cta"><p>{t["post_kicker"]}</p><h2>{t["post_audit_title"]}</h2><p>{t["post_audit_text"]}</p><a href="@audit" data-cta="post-audit">{t["audit_cta"]}</a><p class="cta-second"><a class="text-link" href="@@book" data-cta="post-book">{t["book"]}</a></p></div>'
        else:
            block = f'<div id="cta"><p>{t["post_kicker"]}</p><h2>{t["post_call_title"]}</h2><p>{t["post_call_text"]}</p><a href="@@book" data-cta="post-book">{t["book"]}</a></div>'
        return body.rstrip() + "\n" + block
    contact = r'<a href="@contact">[^<]*</a>'
    if audit:
        replacement = f'<a href="@audit" data-cta="post-audit">{t["audit_cta"]}</a><a href="@@book" data-cta="post-book">{t["book"]}</a>'
    else:
        replacement = f'<a href="@@book" data-cta="post-book">{t["book"]}</a>'
    return re.sub(contact, replacement, body, count=1)


AUDIT_POSTS = {"llms-txt-what-to-do", "schema-markup-ai-engines-read", "measure-ai-citations", "get-cited-by-chatgpt-perplexity-gemini", "webinar-to-content-system", "content-audit-ai-retrieval", "answer-engine-visibility-guide"}


def cta_band(lang):
    t = UI[lang]
    second = f'<a class="btn btn-ghost" href="{url(lang, "audit")}" data-track="band-audit">{t["audit_cta"]}</a>' if exists(lang, "audit") else (f'<a class="btn btn-ghost" href="{url(lang, "pricing")}" data-track="band-pricing">{t["see_pricing"]}</a>' if exists(lang, "pricing") else "")
    return f'''<section class="cta-band" aria-labelledby="cta-band-title">
<div class="wrap">
<span class="eyebrow">{t["cta_kicker"]}</span>
<h2 id="cta-band-title">{t["cta_title"]}</h2>
<p>{t["cta_text"]}</p>
<div class="hero-actions"><a class="btn btn-primary" href="{book_href(lang)}" {BOOK_ATTRS} data-track="band-book">{t["book"]}{icon("arrow", "flip")}</a>{second}</div>
<p class="book-note">{t["book_note"]}</p>
<p class="hero-note">{t["cta_terms"]}</p>
</div>
</section>'''


def resolve(body, lang):
    def block(m):
        pid = m.group(1)
        return m.group(2) if exists(lang, pid) else ""

    body = re.sub(r"<!--if:([a-z0-9/-]+)-->(.*?)<!--endif-->", block, body, flags=re.S)

    def anchor(m):
        pid, inner = m.group(1), m.group(2)
        if pid in PAGES and exists(lang, pid):
            return m.group(0)
        return inner

    body = re.sub(r'<a[^>]*?href="@([a-z0-9/-]+)[^"]*"[^>]*>(.*?)</a>', anchor, body, flags=re.S)
    body = re.sub(r'(href|action)="@([a-z0-9/-]+)', lambda m: f'{m.group(1)}="{url(lang, m.group(2))}', body)
    body = re.sub(r"\{\{list:([a-z]+)\}\}", lambda m: listing(lang, m.group(1)), body)
    body = re.sub(r'(<div class="hero-actions">(?:(?!</div>).)*?href="@@book".*?</div>)(?!\s*<p class="book-note")', lambda m: m.group(1) + f'<p class="book-note">{UI[lang]["book_note"]}</p>', body, flags=re.S)
    body = body.replace("{{booknote}}", UI[lang]["book_note"])
    body = body.replace('href="@@book"', f'href="{book_href(lang)}" {BOOK_ATTRS}')
    body = body.replace("@@book", book_href(lang))
    body = re.sub(r"\{\{photo:([a-z]+)(\|eager)?\}\}", lambda m: photo(lang, m.group(1), bool(m.group(2))), body)
    body = body.replace("@@email", EMAIL)
    body = body.replace("{{audit_request}}", audit_request(lang))
    body = body.replace("{{newsletter}}", newsletter_block(lang, "inline", "inline"))
    body = body.replace("{{demo}}", demo_block(lang))
    body = body.replace("{{teaser}}", teaser_block(lang, "teaser"))
    body = body.replace("{{calc}}", calc_block(lang))
    body = body.replace("{{checklist_items}}", checklist_items(lang))
    body = body.replace("{{proof_log}}", proof_log(lang)).replace("{{proof_screens}}", proof_screens(lang)).replace("{{proof_changelog}}", proof_changelog(lang)).replace("{{case_studies}}", case_studies(lang))
    body = body.replace("{{checklist_form_top}}", checklist_form(lang, "top")).replace("{{checklist_form_bottom}}", checklist_form(lang, "bottom"))
    body = body.replace("@@contact_action", CONTACT_ACTION).replace("@@leads_action", LEADS_ACTION)
    body = body.replace("@@linkedin", LINKEDIN)
    body = re.sub(r"\{\{icon:([a-z]+)(?:\|([a-z -]+))?\}\}", lambda m: icon(m.group(1), m.group(2) or ""), body)
    body = body.replace("{{cta_band}}", cta_band(lang))
    return body


LIST_TEXT = {
    "en": {"read": "Read", "min": "min read", "by": "By", "updated": "Updated", "in_short": "In short", "author": "Hamza Bentarhlia", "related": "Keep reading"},
    "fr": {"read": "Lire", "min": "min de lecture", "by": "Par", "updated": "Mis à jour le", "in_short": "En bref", "author": "Hamza Bentarhlia", "related": "À lire ensuite"},
    "ar": {"read": "اقرأ", "min": "دقائق قراءة", "by": "بقلم", "updated": "آخر تحديث", "in_short": "باختصار", "author": "حمزة بنتغليا", "related": "اقرأ أيضا"},
}
MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    "ar": ["يناير", "فبراير", "مارس", "أبريل", "ماي", "يونيو", "يوليوز", "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر"],
}


def human_date(lang, iso):
    y, m, d = iso.split("-")
    month = MONTHS[lang][int(m) - 1]
    if lang == "en":
        return f"{month} {int(d)}, {y}"
    return f"{int(d)} {month} {y}"


def children(lang, hub):
    items = []
    for pid in PAGES:
        if pid.startswith(hub + "/") and exists(lang, pid):
            meta, body = parse_page(source_path(lang, pid))
            items.append((pid, meta, body))
    if hub == "blog":
        items.sort(key=lambda x: x[1].get("date", ""), reverse=True)
    else:
        items.sort(key=lambda x: strip_tags(x[1].get("h1", x[1]["title"])).lower())
    return items


def reading_time(body):
    return max(3, round(len(strip_tags(body).split()) / 220))


def listing(lang, hub):
    t = LIST_TEXT[lang]
    cards = []
    for pid, meta, body in children(lang, hub):
        title = meta.get("h1", meta["title"])
        summary = meta.get("summary", meta["description"])
        kicker = meta.get("kicker", "")
        extra = f'<span class="kicker">{kicker}</span>' if kicker else ""
        foot = ""
        if hub == "blog":
            foot = f'<p class="card-meta">{human_date(lang, meta["date"])} · {reading_time(body)} {t["min"]}</p>'
        cover = f'<div class="card-cover" data-anim>{art.cover_svg(pid)}</div>' if hub == "blog" else ""
        cards.append(
            f'<a class="glass card list-card" href="{url(lang, pid)}">{cover}{extra}<h3>{strip_tags(title)}</h3><p>{summary}</p>{foot}'
            f'<span class="card-link">{t["read"]}{icon("arrow")}</span></a>'
        )
    cls = "grid grid-3" if hub in ("blog", "compare") else "grid grid-3 glossary-grid"
    return f'<div class="{cls}">{"".join(cards)}</div>'


def article_wrap(lang, pid, meta, body):
    t = LIST_TEXT[lang]
    hub = pid.split("/")[0]
    hub_label = UI[lang].get(hub, hub)
    about = url(lang, "about") if exists(lang, "about") else None
    author = f'<a class="text-link" href="{about}" rel="author">{t["author"]}</a>' if about else t["author"]
    meta_line = ""
    avatar = f'<a class="byline-avatar" href="{about}" tabindex="-1" aria-hidden="true">{photo(lang, "avatar")}</a>' if about else ""
    if meta.get("date"):
        meta_line = (
            f'<p class="article-meta">{avatar}<span>{t["by"]} {author} · <time datetime="{meta.get("modified", meta["date"])}">{t["updated"]} {human_date(lang, meta.get("modified", meta["date"]))}</time>'
            f' · {reading_time(body)} {t["min"]}</span></p>'
        )
    short = ""
    if meta.get("in_short"):
        short = f'<aside class="glass in-short" aria-label="{t["in_short"]}"><span class="kicker">{t["in_short"]}</span><p>{meta["in_short"]}</p></aside>'
    related = ""
    sibs = [c for c in children(lang, hub) if c[0] != pid][:3] if hub == "blog" else []
    if sibs:
        cards = "".join(
            f'<a class="glass card list-card" href="{url(lang, c[0])}"><h3>{strip_tags(c[1].get("h1", c[1]["title"]))}</h3><span class="card-link">{t["read"]}{icon("arrow")}</span></a>'
            for c in sibs
        )
        related = f'<section class="section" aria-labelledby="related-title"><div class="wrap"><h2 id="related-title" class="kicker" style="margin-bottom:20px">{t["related"]}</h2><div class="grid grid-3">{cards}</div></div></section>'
    kicker = meta.get("kicker", hub_label)
    cover_block = f'<div class="article-cover glass" data-anim>{art.cover_svg(pid)}</div>' if hub == "blog" else ""
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{url(lang, hub)}">{hub_label}</a></nav>' if "/" in pid and exists(lang, hub) else ""
    return f'''<article>
<header class="page-hero article-hero"><div class="wrap narrow">
{crumbs}
<span class="eyebrow">{kicker}</span>
<h1 class="display display-sm">{meta.get("h1", meta["title"])}</h1>
{meta_line}
{cover_block}
{short}
</div></header>
<div class="wrap narrow article-body prose">
{article_cta(lang, pid, body)}
{newsletter_block(lang, pid, "post") if hub == "blog" else ""}
</div>
</article>
{related}'''


def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def faq_entities(body):
    items = re.findall(r'<details(?: class="faq-item")?>\s*<summary>(.*?)</summary>\s*<div(?: class="faq-a")?>(.*?)</div>\s*</details>', body, flags=re.S)
    return [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for q, a in items
    ]


def og_image(lang, pid, meta):
    if meta.get("image"):
        return meta["image"]
    own = f"/assets/og/{pid}-{lang}.jpg"
    return own if (OUT / own.lstrip("/")).exists() else f"/assets/og/home-{lang}.jpg"


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
            "logo": {"@type": "ImageObject", "url": DOMAIN + "/logo.svg"},
            "image": DOMAIN + "/assets/og/home-en.jpg",
            "alternateName": "KORTEX Lab",
            "email": EMAIL,
            "description": "KORTEX is a GEO, SEO and content creation studio. It turns one source, such as a blog post, YouTube video, podcast episode or webinar, into up to 30+ assets built to be cited by AI answer engines and ranked by search engines.",
            "founder": {"@type": "Person", "@id": person_id, "name": "Hamza Bentarhlia", "image": DOMAIN + "/assets/img/founder-portrait-608.jpg", "sameAs": [LINKEDIN]},
            "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL, "url": CAL_URL, "availableLanguage": ["English", "French", "Arabic"]},
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
    if "/" in pid and exists(lang, pid.split("/")[0]):
        hub = pid.split("/")[0]
        crumbs.append({"@type": "ListItem", "position": 2, "name": UI[lang].get(hub, hub), "item": abs_url(lang, hub)})
    if pid != "home":
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": strip_tags(meta.get("crumb", meta.get("h1", meta["title"]))), "item": page_url})
    graph.append({"@type": "BreadcrumbList", "@id": page_url + "#breadcrumb", "itemListElement": crumbs})
    extras = [x.strip() for x in meta.get("schema", "").split(",") if x.strip()]
    if "person" in extras:
        graph.append({
            "@type": "Person",
            "@id": person_id,
            "name": "Hamza Bentarhlia",
            "jobTitle": "Founder",
            "image": DOMAIN + "/assets/img/founder-portrait-608.jpg",
            "worksFor": {"@id": org_id},
            "homeLocation": {"@type": "Place", "name": "Fès, Morocco"},
            "sameAs": [LINKEDIN],
            "knowsAbout": ["Customer retention", "Business intelligence", "Automation", "Generative Engine Optimization"],
        })
    if "audit" in extras:
        graph.append({
            "@type": "Service",
            "@id": page_url + "#service",
            "name": "AI Citation Audit",
            "serviceType": "Generative Engine Optimization audit",
            "description": meta["description"],
            "provider": {"@id": org_id},
            "areaServed": "Worldwide",
            "offers": {
                "@type": "Offer",
                "name": "AI Citation Audit",
                "price": str(SITE["auditPriceEur"]),
                "priceCurrency": "EUR",
                "url": page_url,
                "availability": "https://schema.org/InStock",
            },
        })
    if "service" in extras:
        offers = [
            ("GHOST", "2500", "1 source per month, 10 assets per source, monthly citation check on 10 buyer questions, editorial review, delivery in 5 business days."),
            ("SWARM", "5500", "1 source per month, 20 to 24 assets per source, schema markup and internal linking, monthly citation check on 10 buyer questions, monthly strategy call."),
            ("TITAN", "12000", "2 or more sources per month, 28 or more assets per source, full citation tracking with competitors, off-site authority work, dedicated operator."),
        ]
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
                    "description": desc,
                    "priceCurrency": "EUR",
                    "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "EUR", "unitText": "MONTH", **({"minPrice": price} if name == "TITAN" else {})},
                }
                for name, price, desc in offers
            ],
        })
    if (meta.get("kind") == "article" or "article" in meta.get("schema", "")) and meta.get("date"):
        graph.append({
            "@type": "BlogPosting" if pid.startswith("blog/") else "Article",
            "@id": page_url + "#article",
            "headline": strip_tags(meta.get("h1", meta["title"]))[:110],
            "description": meta["description"],
            "inLanguage": lang,
            "mainEntityOfPage": {"@id": page_url + "#webpage"},
            "author": {"@type": "Person", "@id": person_id, "name": "Hamza Bentarhlia", "image": DOMAIN + "/assets/img/founder-portrait-608.jpg", "url": abs_url(lang, "about") if exists(lang, "about") else DOMAIN + "/", "sameAs": [LINKEDIN]},
            "publisher": {"@id": org_id},
            **({"datePublished": meta["date"], "dateModified": meta.get("modified", meta["date"])} if meta.get("date") else {}),
            "image": DOMAIN + og_image(lang, pid, meta),
        })
    if pid == "glossary":
        terms = children(lang, "glossary")
        graph.append({
            "@type": "DefinedTermSet",
            "@id": page_url + "#termset",
            "name": strip_tags(meta.get("h1", meta["title"])),
            "url": page_url,
            "inLanguage": lang,
            "hasDefinedTerm": [{"@type": "DefinedTerm", "name": strip_tags(m.get("h1", m["title"])), "description": strip_tags(m.get("in_short") or m["description"]), "url": abs_url(lang, p)} for p, m, _ in terms],
        })
    if meta.get("kind") == "term":
        graph.append({"@type": "DefinedTerm", "name": strip_tags(meta.get("h1", meta["title"])), "description": meta["description"], "inDefinedTermSet": abs_url(lang, "glossary") + "#termset", "url": page_url})
    faqs = faq_entities(body)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": page_url + "#faq", "mainEntity": faqs})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(lang, pid, meta, body, critical, css_v, js_v):
    alts = [] if pid == "404" else available(pid)
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(l, pid)}">' for l in alts)
    if "en" in alts:
        hreflang += f'<link rel="alternate" hreflang="x-default" href="{abs_url("en", pid)}">'
    robots = '<meta name="robots" content="noindex, follow">' if meta.get("noindex") else ""
    fonts = ["alexandria-arabic"] if lang == "ar" else ["archivo-display", "inter"]
    preload = "".join(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for f in fonts)
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in alts if l != lang)
    title = html.escape(meta["title"], quote=True)
    desc = html.escape(meta["description"], quote=True)
    image = DOMAIN + og_image(lang, pid, meta)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}{"" if pid == "404" else f'<link rel="canonical" href="{abs_url(lang, pid)}">'}
{feed_link(lang, pid)}{hreflang}
<meta name="theme-color" content="#0B1327" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#F4EDE3" media="(prefers-color-scheme: light)">
<meta property="og:type" content="{meta.get("og_type", "website")}">
<meta property="og:site_name" content="KORTEX">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{"" if pid == "404" else f'<meta property="og:url" content="{abs_url(lang, pid)}">'}
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta property="og:locale" content="{LOCALE[lang]}">{og_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image}">
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
{"" if pid == "404" else f'<script type="application/ld+json">{schema(lang, pid, meta, body)}</script>'}'''


ANALYTICS = (
    '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
    'gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied"});'
    'window.kxLoadGA=function(){if(window.kxGA)return;window.kxGA=1;gtag("consent","update",{analytics_storage:"granted"});'
    'gtag("js",new Date());gtag("config","%s");var s=document.createElement("script");s.async=true;'
    's.src="https://www.googletagmanager.com/gtag/js?id=%s";document.head.appendChild(s)};'
    'try{var c=JSON.parse(localStorage.getItem("kx-consent")||"null");if(c&&c.t>Date.now()-15768e6){window.kxConsent=c.v;'
    'if(c.v==="granted")addEventListener("load",function(){setTimeout(window.kxLoadGA,800)})}}catch(e){}</script>' % (GA_ID, GA_ID)
)


def consent_banner(lang):
    t = UI[lang]
    return (
        f'<div class="consent" data-consent role="region" aria-label="{t["consent_label"]}" hidden>'
        f'<p>{t["consent_text"]} <a href="{url(lang, "cookies")}">{t["consent_more"]}</a></p>'
        f'<div class="consent-actions"><button type="button" class="btn btn-ghost btn-sm" data-consent-choice="granted">{t["consent_yes"]}</button>'
        f'<button type="button" class="btn btn-ghost btn-sm" data-consent-choice="denied">{t["consent_no"]}</button></div></div>'
    )


def mirror_path(d, w):
    tokens = re.findall(r"[MLHVCSQTZmlhvcsqtz]|-?\d*\.?\d+", d)
    out, cmd, idx = [], None, 0
    for tok in tokens:
        if tok.isalpha():
            cmd, idx = tok, 0
            out.append(tok)
            continue
        val = float(tok)
        if cmd == "H" or (cmd in "MLCSQT" and idx % 2 == 0):
            val = w - val
        idx += 1
        out.append(f"{val:g}")
    return " ".join(out)


def mirror_svg(svg):
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not vb:
        return svg
    w = float(vb.group(1))

    def rect(m):
        tag = m.group(0)
        x = re.search(r' x="([\d.-]+)"', tag)
        wd = re.search(r' width="([\d.-]+)"', tag)
        if x and wd:
            tag = tag.replace(x.group(0), f' x="{w - float(x.group(1)) - float(wd.group(1)):g}"', 1)
        return tag

    def text(m):
        tag = m.group(0)
        x = re.search(r' x="([\d.-]+)"', tag)
        if x:
            tag = tag.replace(x.group(0), f' x="{w - float(x.group(1)):g}"', 1)
        return tag

    svg = re.sub(r"<rect\b[^>]*>", rect, svg)
    svg = re.sub(r"<text\b[^>]*>", text, svg)
    svg = re.sub(r'(<circle\b[^>]*?) cx="([\d.-]+)"', lambda m: f'{m.group(1)} cx="{w - float(m.group(2)):g}"', svg)
    svg = re.sub(r' d="([^"]+)"', lambda m: f' d="{mirror_path(m.group(1), w)}"', svg)
    return svg


def mirror_diagrams(body):
    return re.sub(r'<svg class="frag-lines".*?</svg>|<svg class="hero-pipe".*?</svg>|<figure class="glass diagram[^"]*"[^>]*>\s*<svg.*?</svg>', lambda m: mirror_svg(m.group(0)), body, flags=re.S)


HERO_KINDS = {"split", "stage", "backdrop", "editorial"}


def decorate(body, pid, meta, lang):
    body = re.sub(r"\{\{v:([a-z0-9-]+)\}\}", lambda m: visuals.render(m.group(1), lang), body)
    vis = meta.get("visual", "")
    inline = ""
    if vis.startswith("#"):
        found = re.search(r'<(\w+)[^>]*\bid="%s".*?</\1>\n?' % re.escape(vis[1:]), body, re.S)
        if found:
            inline = found.group(0).strip()
            body = body.replace(found.group(0), "", 1)
    head = re.search(r'<section class="page-hero[^"]*"[^>]*>\n<div class="wrap">', body)
    if head:
        end = body.find("</div>\n</section>", head.end())
        copy = body[head.end() : end]
        if meta.get("case") == "sentence":
            copy = re.sub(r'(<h1[^>]*class="display)', r"\1 display-sentence", copy, count=1)
        kind = meta.get("hero", "")
        panel = inline or (visuals.render(vis, lang) if vis else "")
        section = head.group(0)
        if kind in HERO_KINDS and panel:
            section = section.replace('class="page-hero', f'class="page-hero hero-{kind}', 1)
            if kind in ("split", "editorial"):
                inner = f'<div class="hero-grid"><div class="hero-copy">{copy}</div><div class="hero-visual">{panel}</div></div>'
            elif kind == "stage":
                inner = f'<div class="hero-copy">{copy}</div><div class="hero-visual">{panel}</div>'
            else:
                inner = f'<div class="hero-visual" aria-hidden="true">{panel}</div><div class="hero-copy">{copy}</div>'
            body = body[: head.start()] + section + inner + body[end:]
        else:
            body = body[: head.start()] + section + copy + body[end:]
    count = [0]

    def sep(m):
        count[0] += 1
        return "</section>\n" + (art.divider(count[0]) if count[0] in (2, 6) else "") + "\n<section"

    body = re.sub(r"</section>\s*\n\s*<section", sep, body)
    return body


def fr_typo(text):
    text = re.sub(r" ([?!;:»])", "\u202f\\1", text)
    text = text.replace("« ", "«\u202f")
    text = re.sub(r"(\d) (\d{3})\b", "\\1\u202f\\2", text)
    text = re.sub(r"(\d) €", "\\1\u00a0€", text)
    return text


VCSS = {}


def visual_css(body, pid=""):
    used = visuals.modules_in(body)
    if pid.startswith("blog/") and "blog" not in used:
        used = sorted(used + ["blog"])
    used = sorted(set(used + [k for k in ("ix-" + m for m in re.findall(r'data-ix="([a-z]+)"', body)) if k in VCSS]))
    if not used:
        return ""
    return VCSS["kit"] + "".join(VCSS.get(n, "") for n in used)


AR_LATIN = r"[A-Za-z][A-Za-z0-9.+&-]*(?:\s(?:[A-Z][A-Za-z0-9.+&-]*|AI))*"


def ar_latin_plain(text):
    return re.sub(r"(?<![\w\u0600-\u06FF])و\u200c?\s?(?=[A-Za-z])", "و ", text)


def ar_latin(body):
    def text_node(m):
        t = re.sub(r"(?<![\w\u0600-\u06FF])و\u200c?\s?(" + AR_LATIN + ")", r"و <bdi>\1</bdi>", m.group(1))
        return ">" + t + "<"
    def attr(m):
        return m.group(1) + '="' + ar_latin_plain(m.group(2)) + '"'
    parts = re.split(r"(<svg\b.*?</svg>|<script\b.*?</script>|<style\b.*?</style>)", body, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(re.sub(r">([^<]+)<", lambda m: ">" + ar_latin_plain(m.group(1)) + "<", part))
        else:
            part = re.sub(r">([^<]+)<", text_node, part)
            out.append(re.sub(r'\b(aria-label|alt|title|content|placeholder|data-tip)="([^"]*)"', attr, part))
    return "".join(out)


def render(lang, pid, critical, css_v, js_v):
    meta, body = parse_page(source_path(lang, pid))
    body = decorate(body, pid, meta, lang)
    if lang == "ar":
        body = mirror_diagrams(body)
        meta = {k: ar_latin_plain(v) for k, v in meta.items()}
    if lang == "fr":
        body = re.sub(r">([^<]+)<", lambda m: ">" + fr_typo(m.group(1)) + "<", body)
        meta = {k: fr_typo(v) for k, v in meta.items()}
    if meta.get("kind") in ("article", "term"):
        body = article_wrap(lang, pid, meta, body)
    if pid == "blog":
        body = body + newsletter_block(lang, pid, "index")
    body = resolve(body, lang)
    direction = ' dir="rtl"' if lang == "ar" else ""
    band = "" if meta.get("band") == "no" else cta_band(lang)
    page = f'''<!doctype html>
<html lang="{lang}"{direction}>
<head>
{head(lang, pid, meta, body, critical + visual_css(body, pid), css_v, js_v)}
</head>
<body>
{header(lang, pid)}
<main id="main" tabindex="-1">
{art.SPRITE}
<div class="ambient" aria-hidden="true"></div>
{body.strip()}
{art.divider(0) if band else ""}
{band}
</main>
{book_bar(lang, pid)}
{newsletter_slide(lang, pid) if pid.startswith("blog/") else ""}
{footer(lang)}
{consent_banner(lang)}
{ANALYTICS}
</body>
</html>
'''
    page = tag_ctas(page, pid)
    if lang == "ar":
        start = page.find("<body>")
        head_part = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', lambda m: m.group(1) + ar_latin_plain(m.group(2)) + m.group(3), page[:start], flags=re.S)
        page = head_part + ar_latin(page[start:])
    return re.sub(r"\n{2,}", "\n", page)


def output_path(lang, pid):
    if pid == "404":
        return OUT / "404.html"
    rel = url(lang, pid).strip("/")
    return OUT / rel / "index.html" if rel else OUT / "index.html"


def feed_link(lang, pid):
    if pid != "blog" and not pid.startswith("blog/"):
        return ""
    title = html.escape(f"KORTEX {t_blog_label(lang)}", quote=True)
    return f'<link rel="alternate" type="application/rss+xml" title="{title}" href="{DOMAIN}{url(lang, "blog")}feed.xml">\n'


def t_blog_label(lang):
    return {"en": "Blog", "fr": "Blog", "ar": "المدونة"}[lang]


def rfc822(iso):
    return datetime.date.fromisoformat(iso).strftime("%a, %d %b %Y 00:00:00 +0000")


def feed_xml(lang):
    items = []
    for pid, meta, _ in children(lang, "blog"):
        link = abs_url(lang, pid)
        items.append(
            f"<item><title>{html.escape(strip_tags(meta.get('h1', meta['title'])))}</title><link>{link}</link>"
            f'<guid isPermaLink="true">{link}</guid><pubDate>{rfc822(meta["date"])}</pubDate>'
            f"<description>{html.escape(strip_tags(meta.get('summary', meta['description'])))}</description></item>"
        )
    home = abs_url(lang, "blog")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f"<title>KORTEX {t_blog_label(lang)}</title><link>{home}</link><description>{html.escape(parse_page(source_path(lang, 'blog'))[0]['description'])}</description>"
        f'<language>{lang}</language><atom:link href="{home}feed.xml" rel="self" type="application/rss+xml"/>'
        + "".join(items)
        + "</channel></rss>\n"
    )


def git_lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)], capture_output=True, text=True, cwd=OUT, check=True).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        out = ""
    return out or BUILD_DATE


def sitemap():
    rows = []
    for pid in PAGES:
        for lang in available(pid):
            meta, _ = parse_page(source_path(lang, pid))
            if meta.get("noindex") or pid == "404":
                continue
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(l, pid)}"/>' for l in available(pid))
            if "en" in available(pid):
                alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{abs_url("en", pid)}"/>'
            rows.append(f'<url><loc>{abs_url(lang, pid)}</loc><lastmod>{meta.get("modified") or git_lastmod(source_path(lang, pid))}</lastmod>{alts}</url>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n"


BLOG_SLUGS = {
    "answer-engine-visibility-guide": "guide-visibilite-moteurs-de-reponse",
    "b2b-linkedin-content-dies": "pourquoi-contenu-linkedin-b2b-meurt",
    "category-creation-ai-search": "creation-de-categorie-recherche-ia",
    "content-audit-ai-retrieval": "audit-contenu-recuperation-ia",
    "entity-first-content-architecture": "architecture-contenu-entite-first",
    "new-b2b-content-stack": "nouvelle-stack-contenu-b2b",
    "one-video-authority-system": "une-video-systeme-autorite",
    "stop-ranking-start-dominating": "arretez-de-ranker-soyez-cite",
}


def redirects():
    table = {
        "tarifs.html": ("fr", "pricing"),
        "en/index.html": ("en", "home"),
        "en/solutions.html": ("en", "how-it-works"),
        "en/pricing.html": ("en", "pricing"),
        "en/blog.html": ("en", "blog"),
        "en/contact.html": ("en", "contact"),
        "en/login.html": ("en", "login"),
        "free-geo-audit/index.html": ("en", "contact"),
        "fr/free-geo-audit/index.html": ("fr", "contact"),
        "ar/free-geo-audit/index.html": ("ar", "contact"),
        "contact_v2.html": ("fr", "contact"),
        "legal/index.html": ("en", "privacy"),
        "fr/legal/index.html": ("fr", "privacy"),
        "ar/legal/index.html": ("ar", "privacy"),
    }
    for en_slug, fr_slug in BLOG_SLUGS.items():
        table[f"blog-{fr_slug}.html"] = ("fr", f"blog/{en_slug}")
        table[f"blog-{en_slug}.html"] = ("en", f"blog/{en_slug}")
        table[f"en/blog-{en_slug}.html"] = ("en", f"blog/{en_slug}")
    return table


def redirect_page(target_lang, pid, old=""):
    lang, path = target_lang, url(target_lang, pid)
    if not exists(lang, pid):
        lang, path = "en", url("en", pid) if exists("en", pid) else "/"
    full = DOMAIN + path
    return (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>KORTEX</title>'
        f'<link rel="canonical" href="{full}"><meta name="robots" content="noindex, follow">'
        f'<meta http-equiv="refresh" content="0; url={path}"></head>'
        f'<body><p><a href="{path}">{full}</a></p></body></html>\n'
    )


def llms_txt():
    lines = [
        "# KORTEX",
        "",
        "> KORTEX is a GEO, SEO and content creation studio based in Fès, Morocco, serving clients worldwide. A client provides one source (a blog post, YouTube video, podcast episode or webinar) and KORTEX turns it into up to 30+ assets built to be cited by AI answer engines such as ChatGPT, Perplexity, Gemini, Google AI Overviews and Claude, and ranked by search engines. Expertise is extracted from the client's own content, never invented, and a person reviews everything before publication.",
        "",
        "## Plans",
        "- GHOST: €2,500 per month. 1 source per month, 10 assets per source, monthly citation check on 10 buyer questions, delivery in 5 business days.",
        "- SWARM: €5,500 per month. 1 source per month, 20 to 24 assets per source, schema markup and internal linking, monthly citation check on 10 buyer questions, monthly strategy call.",
        "- TITAN: from €12,000 per month. 2 or more sources per month, 28 or more assets per source, full citation tracking with competitors, off-site authority work, delivery in 3 to 4 business days.",
        "- Every plan: no setup fees, month to month with 30 days' notice, the client owns 100% of the content.",
        "",
        "Founder: Hamza Bentarhlia. Contact: " + EMAIL + ". Book a strategy call: " + CAL_URL,
        "",
        "## Key pages",
    ]
    for pid in ["home", "how-it-works", "pricing", "audit", "checklist", "proof", "solutions", "b2b", "creators", "ecommerce", "resources", "compare", "glossary", "blog", "about", "contact"]:
        if exists("en", pid):
            meta, _ = parse_page(source_path("en", pid))
            lines.append(f"- [{strip_tags(meta.get('h1', meta['title']))}]({abs_url('en', pid)}): {meta['description']}")
    for hub, label in (("glossary", "Glossary"), ("compare", "Comparisons"), ("blog", "Articles")):
        items = children("en", hub)
        if items:
            lines += ["", f"## {label}"]
            lines += [f"- [{strip_tags(m.get('h1', m['title']))}]({abs_url('en', p)}): {m['description']}" for p, m, _ in items]
    lines += ["", "## Other languages", f"- French: {DOMAIN}/fr/", f"- Arabic: {DOMAIN}/ar/", ""]
    return "\n".join(lines)


def robots_txt():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended", "CCBot"]
    rules = "\n".join(f"User-agent: {b}\nAllow: /\n" for b in bots)
    return f"User-agent: *\nAllow: /\nDisallow: /login/\nDisallow: /fr/login/\nDisallow: /ar/login/\n\n{rules}\nSitemap: {DOMAIN}/sitemap.xml\n"


def main():
    critical = minify_css((SRC / "styles" / "tokens.css").read_text(encoding="utf-8") + (SRC / "styles" / "critical.css").read_text(encoding="utf-8"))
    site_css = minify_css((SRC / "styles" / "site.css").read_text(encoding="utf-8"))
    for f in sorted((SRC / "styles" / "v").glob("*.css")):
        VCSS[f.stem] = minify_css(f.read_text(encoding="utf-8"))
    css_out = OUT / "assets" / "css" / "site.css"
    css_out.parent.mkdir(parents=True, exist_ok=True)
    css_out.write_text(site_css, encoding="utf-8")
    js_out = OUT / "assets" / "js" / "site.js"
    js_out.parent.mkdir(parents=True, exist_ok=True)
    js_out.write_text((SRC / "scripts" / "site.js").read_text(encoding="utf-8"), encoding="utf-8")
    for mod in sorted((SRC / "scripts" / "modules").glob("*.js")):
        (OUT / "assets" / "js" / mod.name).write_text(mod.read_text(encoding="utf-8"), encoding="utf-8")
    data_out = OUT / "assets" / "data"
    data_out.mkdir(parents=True, exist_ok=True)
    (data_out / "demo.json").write_text(json.dumps(DEMO, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    css_v, js_v = asset_version(css_out), asset_version(js_out)
    built = 0
    for pid in PAGES:
        for lang in available(pid):
            target = output_path(lang, pid)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(lang, pid, critical, css_v, js_v), encoding="utf-8")
            built += 1
    for old, (lang, pid) in redirects().items():
        target = OUT / old
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(redirect_page(lang, pid, old), encoding="utf-8")
    (OUT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    for lang in LANGS:
        feed_path = OUT / url(lang, "blog").lstrip("/") / "feed.xml"
        feed_path.write_text(feed_xml(lang), encoding="utf-8")
    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (OUT / "llms.txt").write_text(llms_txt(), encoding="utf-8")
    (OUT / "robots.txt").write_text(robots_txt(), encoding="utf-8")
    print(f"built {built} pages")


if __name__ == "__main__":
    main()
