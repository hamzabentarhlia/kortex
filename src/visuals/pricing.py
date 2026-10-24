from . import kit
from .kit import T, icon


def stacks(lang):
    art = T(lang, "Articles", "Articles", "مقالات")
    news = T(lang, "Newsletter versions", "Versions newsletter", "نسخ النشرة")
    soc = T(lang, "Social assets", "Contenus sociaux", "محتوى اجتماعي")
    asset = T(lang, "Assets", "Contenus", "محتويات")
    plans = [
        ("ghost", "GHOST", "€2,500", T(lang, "10 assets per source, 1 source a month", "10 contenus par source, 1 source par mois", "10 محتويات لكل مصدر، مصدر واحد شهريا"),
         [("a", 2), ("s", 8)], 0, ""),
        ("swarm", "SWARM", "€5,500", T(lang, "20 to 24 assets per source, 1 source a month", "20 à 24 contenus par source, 1 source par mois", "من 20 إلى 24 محتوى لكل مصدر، مصدر واحد شهريا"),
         [("a", 4), ("n", 4), ("s", 12)], 4, ""),
        ("titan", "TITAN", T(lang, "from €12,000", "dès 12 000 €", "ابتداء من 12000 €"), T(lang, "28+ assets per source, 2 or more sources a month", "28+ contenus par source, 2 sources ou plus par mois", "أكثر من 28 محتوى لكل مصدر، مصدران أو أكثر شهريا"),
         [("t", 28)], 0, "+"),
    ]
    icons = {"a": "doc", "n": "mail", "s": "linkedin", "t": "box"}
    rows = []
    for key, name, price, sub, mix, extra, plus in plans:
        cells = []
        n = 0
        for kind, count in mix:
            for _ in range(count):
                cells.append(f'<i class="ps-t ps-{kind}" style="--i:{n}">{icon(icons[kind])}</i>')
                n += 1
        for _ in range(extra):
            cells.append(f'<i class="ps-t ps-opt" style="--i:{n}">{icon("linkedin")}</i>')
            n += 1
        if plus:
            cells.append(f'<i class="ps-t ps-plus" style="--i:{n}">+</i>')
        total = sum(c for _, c in mix)
        shown = f"{total}" + (f"–{total + extra}" if extra else "") + plus
        rows.append(
            f'<div class="ps-row" data-plan-row="{key}"><div class="ps-head"><b>{name}</b><span>{price}</span><small>{sub}</small></div>'
            f'<div class="ps-grid" role="img" aria-label="{name}: {shown} {asset.lower() if lang != "ar" else asset}">{"".join(cells)}</div><span class="ps-count">{shown}</span></div>'
        )
    legend = (
        f'<ul class="ps-legend"><li><i class="ps-a"></i>{art}</li><li><i class="ps-n2"></i>{news}</li><li><i class="ps-s"></i>{soc}</li>'
        f'<li><i class="ps-opt"></i>{T(lang, "Up to 4 more on SWARM", "Jusqu’à 4 de plus avec SWARM", "حتى 4 إضافية في SWARM")}</li><li><i class="ps-tt"></i>{T(lang, "Mix set per source on TITAN", "Répartition fixée par source avec TITAN", "التوزيع يُحدد لكل مصدر في TITAN")}</li></ul>'
    )
    return f'<div class="ps">{"".join(rows)}{legend}</div>'


def after(lang):
    steps = [
        ("chat", T(lang, "Day 0", "Jour 0", "اليوم 0"), T(lang, "Strategy call", "Appel stratégique", "المكالمة الاستراتيجية"), T(lang, "30 minutes. We look at your field in AI answers together.", "30 minutes. Nous regardons votre domaine dans les réponses IA.", "30 دقيقة. ننظر معا في حضور مجالك داخل إجابات الذكاء الاصطناعي.")),
        ("target", T(lang, "Next", "Ensuite", "بعدها"), T(lang, "Scope", "Cadrage", "تحديد النطاق"), T(lang, "We agree on the plan and the first source.", "Nous fixons l’offre et la première source.", "نتفق على الباقة والمصدر الأول.")),
        ("link", T(lang, "Day 1", "Jour 1", "اليوم 1"), T(lang, "Source in", "Source reçue", "وصول المصدر"), T(lang, "You send one link and a short intake form.", "Vous envoyez un lien et un court questionnaire.", "ترسل رابطا واستبيانا قصيرا.")),
        ("box", T(lang, "Business day 5", "5e jour ouvré", "يوم العمل 5"), T(lang, "First delivery", "Première livraison", "أول تسليم"), T(lang, "5 business days on GHOST and SWARM, 3 to 4 on TITAN.", "5 jours ouvrés avec GHOST et SWARM, 3 à 4 avec TITAN.", "5 أيام عمل في GHOST وSWARM، ومن 3 إلى 4 في TITAN.")),
        ("stamp", T(lang, "Week 2", "Semaine 2", "الأسبوع 2"), T(lang, "You approve, it goes live", "Vous validez, c’est en ligne", "تعتمد أنت، ثم يُنشر"), T(lang, "Comment or approve, we revise and publish.", "Commentez ou validez, nous révisons et publions.", "علّق أو اعتمد، ونحن نعدّل وننشر.")),
        ("gauge", T(lang, "Every month", "Chaque mois", "كل شهر"), T(lang, "Citation check", "Vérification des citations", "فحص الاستشهادات"), T(lang, "10 buyer questions asked to the main AI engines.", "10 questions d’acheteurs posées aux principaux moteurs IA.", "10 أسئلة من المشترين تُطرح على محركات الذكاء الاصطناعي الرئيسية.")),
    ]
    mid = kit.uid()
    items = "".join(
        f'<li class="pa-step{" is-acc" if i in (0, 5) else ""} st" style="--i:{i}"><span class="pa-day">{d}</span><span class="pa-dot">{icon(ic)}</span><b>{h}</b><p>{p}</p></li>'
        for i, (ic, d, h, p) in enumerate(steps)
    )
    line = f'<svg class="pa-line" viewBox="0 0 1000 4" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>{kit.wipe_mask(mid)}</defs><rect width="1000" height="4" rx="2" class="pa-base"/><rect width="1000" height="4" rx="2" class="pa-fill" mask="url(#{mid})"/></svg>'
    loop = T(lang, "Then the next source, every month", "Puis la source suivante, chaque mois", "ثم المصدر التالي، كل شهر")
    return f'<div class="pa">{line}<ol class="pa-steps">{items}</ol><p class="pa-loop">{icon("loop")}{loop}</p></div>'


VISUALS = {"pricing-stacks": stacks, "pricing-after": after}
