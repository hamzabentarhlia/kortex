from . import kit
from .kit import T, icon, label


def deliverables(lang):
    ex = label(kit.EXAMPLE[lang])
    article = (
        f'<article class="sd sd-article st" style="--i:0"><div class="sd-k">{icon("doc")}{T(lang, "Article page", "Page article", "صفحة مقال")}</div>'
        f'<h4>{T(lang, "Why yearly supplier audits miss most risk events", "Pourquoi l’audit fournisseur annuel rate la plupart des incidents", "لماذا يفوّت التدقيق السنوي للموردين معظم المخاطر")}</h4>'
        f'<p class="sd-meta">Acme · {T(lang, "8 min read", "8 min de lecture", "8 دقائق قراءة")}</p>'
        f'<p class="sd-lead">{T(lang, "Short answer: an audit shows what was true on one day. Payment delays and order changes show trouble months earlier.", "Réponse courte : un audit montre ce qui était vrai un jour donné. Les retards de paiement et les changements de commande signalent un problème des mois plus tôt.", "الإجابة المختصرة: التدقيق يُظهر ما كان صحيحا في يوم واحد، أما تأخر المدفوعات وتغيّر الطلبيات فتكشف المشكلة قبل أشهر.")}</p>'
        '<i class="vx-line" style="--w:94%"></i><i class="vx-line" style="--w:86%"></i><i class="vx-line" style="--w:70%"></i></article>'
    )
    faq = (
        f'<article class="sd sd-faq st" style="--i:1"><div class="sd-k">{icon("chat")}{T(lang, "FAQ block", "Bloc FAQ", "قسم أسئلة شائعة")}</div>'
        f'<p class="sd-q">{T(lang, "How often should suppliers be reviewed?", "À quelle fréquence revoir ses fournisseurs ?", "كم مرة يجب مراجعة الموردين؟")}</p>'
        f'<p class="sd-a">{T(lang, "Critical suppliers every month, the rest every quarter, with alerts in between.", "Les fournisseurs critiques chaque mois, les autres chaque trimestre, avec des alertes entre deux.", "الموردون الأساسيون كل شهر، والبقية كل ثلاثة أشهر، مع تنبيهات بين المراجعات.")}</p>'
        f'<p class="sd-q is-c">{T(lang, "What is a supplier risk score?", "Qu’est-ce qu’un score de risque fournisseur ?", "ما هو مؤشر مخاطر المورد؟")}</p></article>'
    )
    post = (
        f'<article class="sd sd-post st" style="--i:2"><div class="sd-k">{icon("linkedin")}{T(lang, "LinkedIn post", "Post LinkedIn", "منشور لينكدإن")}</div>'
        '<div class="sd-au"><i></i><span><b>Acme</b><small>2 h</small></span></div>'
        f'<p>{T(lang, "Most supplier failures show up in the data months before the audit does. Three signals we watch every week:", "La plupart des défaillances fournisseurs apparaissent dans les données des mois avant l’audit. Trois signaux que nous suivons chaque semaine :", "معظم إخفاقات الموردين تظهر في البيانات قبل التدقيق بأشهر. ثلاث إشارات نتابعها كل أسبوع:")}</p>'
        f'<ul><li>{T(lang, "Late payments", "Retards de paiement", "تأخر المدفوعات")}</li><li>{T(lang, "Shrinking order sizes", "Commandes qui rétrécissent", "تقلص حجم الطلبيات")}</li><li>{T(lang, "Key staff leaving", "Départs de personnes clés", "مغادرة موظفين أساسيين")}</li></ul></article>'
    )
    news = (
        f'<article class="sd sd-news st" style="--i:3"><div class="sd-k">{icon("mail")}{T(lang, "Newsletter", "Newsletter", "نشرة بريدية")}</div>'
        f'<p class="sd-subj"><small>{T(lang, "Subject", "Objet", "الموضوع")}</small>{T(lang, "The gap between two audits", "L’angle mort entre deux audits", "الفجوة بين تدقيقين")}</p>'
        f'<p class="sd-prev">{T(lang, "This month: why the riskiest period for a supplier is the one nobody checks.", "Ce mois-ci : pourquoi la période la plus risquée est celle que personne ne vérifie.", "هذا الشهر: لماذا تكون أخطر فترة هي الفترة التي لا يراجعها أحد.")}</p>'
        '<i class="vx-line" style="--w:90%"></i><i class="vx-line" style="--w:64%"></i></article>'
    )
    script = (
        f'<article class="sd sd-script st" style="--i:4"><div class="sd-k">{icon("film")}{T(lang, "Short video script", "Script vidéo court", "نص فيديو قصير")}</div>'
        '<ol>'
        f'<li><span dir="ltr">0:00</span>{T(lang, "Your last audit was green. Your supplier still failed.", "Votre dernier audit était au vert. Votre fournisseur a quand même lâché.", "آخر تدقيق كان سليما، ومع ذلك تعثّر المورد.")}</li>'
        f'<li><span dir="ltr">0:06</span>{T(lang, "Here is what the data showed three months before.", "Voici ce que les données montraient trois mois avant.", "إليك ما أظهرته البيانات قبل ثلاثة أشهر.")}</li>'
        f'<li><span dir="ltr">0:20</span>{T(lang, "Watch these three signals instead.", "Surveillez plutôt ces trois signaux.", "راقب هذه الإشارات الثلاث بدلا من ذلك.")}</li>'
        '</ol></article>'
    )
    src = T(lang, "All five come from the same webinar, in Acme's own words.", "Les cinq viennent du même webinaire, avec les mots d’Acme.", "الخمسة مأخوذة من الندوة نفسها، بكلمات Acme.")
    return (
        f'<div class="sdw"><div class="sdw-top">{ex}<span class="sdw-src">{icon("screen")}{src}</span></div>'
        f'<div class="sd-row">{article}{faq}{post}{news}{script}</div></div>'
    )


VISUALS = {"samples-deliverables": deliverables}
