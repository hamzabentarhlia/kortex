from .kit import T, icon, chip


def nf_answer(lang):
    links = [("/", T(lang, "Home", "Accueil", "الرئيسية")), ("/how-it-works/", T(lang, "How it works", "Méthode", "طريقة العمل")), ("/pricing/", T(lang, "Pricing", "Tarifs", "الأسعار")), ("/blog/", T(lang, "Blog", "Blog", "المدونة"))]
    pills = "".join(f'<a class="nf-link st" style="--i:{i + 4}" href="{h}">{icon("link")}{t}</a>' for i, (h, t) in enumerate(links))
    return (
        '<div class="nf-card">'
        f'<div class="nf-head st">{chip("KORTEX")}<span class="nf-status">404</span></div>'
        f'<p class="nf-q st" style="--i:1">{icon("search")}<span dir="ltr" class="nf-path" data-nf-path>kortexlab.me/…</span></p>'
        '<div class="nf-scan st" style="--i:2" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>'
        f'<p class="nf-a st" style="--i:3"><strong>No source found for this page.</strong> These pages exist and can answer most questions:</p>'
        f'<div class="nf-links">{pills}</div>'
        '</div>'
    )


VISUALS = {"nf-answer": nf_answer}
