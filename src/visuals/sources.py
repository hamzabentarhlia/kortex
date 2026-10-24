import math

from .kit import T, icon, label, tile, cite, answer, beam, stamp, EXAMPLE, BRAND


def _sk(widths, cls="sb-sk"):
    return f'<span class="{cls}" aria-hidden="true">' + "".join(f'<i style="--w:{w}%"></i>' for w in widths) + "</span>"


def blog(lang):
    passages = [
        T(lang, "A team needs a CRM once deals start slipping between inboxes.", "Une équipe a besoin d'un CRM dès que des affaires se perdent entre les boîtes mail.", "يحتاج الفريق إلى نظام CRM حين تبدأ الصفقات بالضياع بين صناديق البريد."),
        T(lang, "A spreadsheet works until two people edit the same deal.", "Un tableur suffit jusqu'à ce que deux personnes modifient la même affaire.", "يكفي جدول البيانات إلى أن يعدّل شخصان الصفقة نفسها."),
        T(lang, "The best CRM is the one your team opens every day.", "Le meilleur CRM est celui que votre équipe ouvre chaque jour.", "أفضل نظام CRM هو الذي يفتحه فريقك كل يوم."),
        T(lang, "Pipeline hygiene means updating or closing every stale deal each week.", "L'hygiène du pipeline, c'est mettre à jour ou clore chaque affaire dormante chaque semaine.", "نظافة خط المبيعات تعني تحديث كل صفقة راكدة أو إغلاقها كل أسبوع."),
    ]
    fills = [[96, 88, 72], [92, 64], [90, 84, 58], [94, 70]]
    body = ""
    for k, text in enumerate(passages):
        body += _sk(fills[k], "sb-sk")
        body += f'<p class="sources-sb-hl" style="--i:{k}"><b class="sources-sb-n">{k + 1}</b><span>{text}</span></p>'
    body += _sk([90, 46], "sb-sk")
    head = (
        f'<div class="sources-sb-bar"><span class="vx-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="sources-sb-url" dir="ltr">{BRAND}/blog/crm</span></div>'
        f'<div class="sources-sb-body"><div class="sources-sb-meta">{label(EXAMPLE[lang])}<span class="sources-sb-tool">{icon("marker")}{T(lang, "4 key passages", "4 passages clés", "4 مقاطع أساسية")}</span></div>'
        f'<p class="sources-sb-title">{T(lang, "How to choose a CRM for a small team", "Comment choisir un CRM pour une petite équipe", "كيف تختار نظام CRM لفريق صغير")}</p>'
    )
    ok, no = icon("check"), icon("x")
    cards = [
        ("chat", T(lang, "FAQ entry", "Entrée FAQ", "سؤال شائع"),
         f'<p class="sources-sb-q">{T(lang, "When does a small team need a CRM?", "Quand une petite équipe a-t-elle besoin d’un CRM ?", "متى يحتاج فريق صغير إلى نظام CRM؟")}</p>' + _sk([92, 66], "sb-sk")),
        ("columns", T(lang, "Comparison row", "Ligne de comparatif", "صف في صفحة مقارنة"),
         f'<div class="sources-sb-tab"><span></span><b>{T(lang, "Spreadsheet", "Tableur", "جدول بيانات")}</b><b>CRM</b>'
         f'<span>{T(lang, "Shared editing", "Édition à plusieurs", "تعديل مشترك")}</span><i class="sources-is-no">{no}</i><i class="sources-is-ok">{ok}</i></div>'),
        ("linkedin", T(lang, "Social post", "Post social", "منشور اجتماعي"),
         f'<p class="sources-sb-post">{T(lang, "“", "« ", "«")}{passages[2]}{T(lang, "”", " »", "»")}</p><span class="sources-sb-by"><i></i><span dir="ltr">{BRAND}</span></span>'),
        ("grid", T(lang, "Glossary entry", "Entrée de glossaire", "مدخل في المسرد"),
         f'<p class="sources-sb-term">{T(lang, "Pipeline hygiene", "Hygiène du pipeline", "نظافة خط المبيعات")}</p>' + _sk([88, 54], "sb-sk")),
    ]
    out = ""
    for k, (ic, kind, inner) in enumerate(cards):
        out += (
            f'<div class="sources-sb-card" style="--i:{k}"><div class="sources-sb-cin">'
            f'<div class="sources-sb-ch"><b class="sources-sb-n">{k + 1}</b><span class="sources-sb-kind">{icon(ic)}{kind}</span></div>{inner}</div></div>'
        )
    return f'<div class="sources-sb"><div class="sources-sb-page">{head}{body}</div></div><div class="sources-sb-out">{out}</div></div>'


def blog_cluster(lang):
    qs = [
        ("doc", T(lang, "Pillar", "Pilier", "مقال محوري"), T(lang, "How to choose a CRM", "Choisir un CRM", "كيف تختار نظام CRM")),
        ("chat", T(lang, "Question page", "Page question", "صفحة سؤال"), T(lang, "When do you need a CRM?", "Quand faut-il un CRM ?", "متى تحتاج إلى CRM؟")),
        ("layers", T(lang, "Comparison", "Comparatif", "مقارنة"), T(lang, "Spreadsheet or CRM?", "Tableur ou CRM ?", "جدول بيانات أم CRM؟")),
        ("grid", T(lang, "Glossary", "Glossaire", "المسرد"), T(lang, "What is pipeline hygiene?", "Qu'est-ce que l'hygiène du pipeline ?", "ما نظافة خط المبيعات؟")),
        ("linkedin", T(lang, "Social post", "Post social", "منشور اجتماعي"), T(lang, "The CRM your team opens", "Le CRM que l'équipe ouvre", "النظام الذي يفتحه فريقك")),
        ("mail", T(lang, "Newsletter", "Newsletter", "نشرة بريدية"), T(lang, "Five signs you need a CRM", "Cinq signes qu'il vous faut un CRM", "خمس علامات على حاجتك إلى CRM")),
    ]
    marks = "".join(f'<i class="sources-sbc-q" style="--i:{k}">?</i>' for k in range(6))
    lines = "".join(f'<i class="sources-sbc-l" style="--w:{w}%"></i>' for w in [92, 80, 96, 70, 88, 94, 62, 90, 84, 76, 93, 68, 86, 74])
    long_page = (
        f'<div class="sources-sbc-long sources-so-st"><div class="sources-sbc-lh">{icon("doc")}<span>{T(lang, "One long post", "Un long article", "مقال طويل واحد")}</span></div>'
        f'<div class="sources-sbc-lb" aria-hidden="true">{lines}<span class="sources-sbc-qs">{marks}</span></div>'
        f'<p class="sources-sbc-cap">{T(lang, "Six questions answered at once", "Six questions traitées d’un coup", "ست أسئلة في مكان واحد")}</p></div>'
    )
    pages = ""
    for k, (ic, kind, q) in enumerate(qs):
        pages += (
            f'<div class="sources-sbc-pg sources-so-st{" is-hl" if k == 0 else ""}" style="--i:{k + 2}"><span class="sources-sbc-k">{icon(ic)}{kind}</span>'
            f'<b>{q}</b><i class="vx-line" style="--w:86%"></i><i class="vx-line" style="--w:58%"></i>'
            f'<span class="sources-sbc-link" aria-hidden="true">{icon("link")}</span></div>'
        )
    return (
        f'<div class="sources-sbc"><div class="sources-sbc-top">{label(EXAMPLE[lang])}</div><div class="sources-sbc-row">{long_page}'
        f'<div class="sources-sbc-arrow" aria-hidden="true">{beam()}<span>{icon("scissors")}</span></div>'
        f'<div class="sources-sbc-grid">{pages}</div></div>'
        f'<p class="sources-sbc-foot">{T(lang, "Six focused pages, each answering one question first, all linked to each other.", "Six pages ciblées, chacune répond d’abord à une question, toutes reliées entre elles.", "ست صفحات مركزة، تبدأ كل منها بالإجابة عن سؤال واحد، وكلها مترابطة.")}</p></div>'
    )


def _yt_chapters(lang):
    return [
        ("00:00", T(lang, "The problem", "Le problème", "المشكلة"),
         T(lang, "Most onboarding stalls in the first week.", "La plupart des onboardings bloquent dès la première semaine.", "يتعثر معظم الإعداد في الأسبوع الأول."),
         "doc", T(lang, "Pillar article", "Article pilier", "مقال محوري")),
        ("04:40", T(lang, "Your questions", "Vos questions", "أسئلتكم"),
         T(lang, "The question I get most: how long does setup take?", "La question qu'on me pose le plus : combien de temps dure la mise en place ?", "أكثر سؤال يصلني: كم يستغرق الإعداد؟"),
         "chat", T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة شائعة")),
        ("09:20", T(lang, "The method", "La méthode", "الطريقة"),
         T(lang, "Here is the five-step checklist we use.", "Voici la checklist en cinq étapes que nous utilisons.", "هذه قائمة التحقق ذات الخطوات الخمس التي نعتمدها."),
         "grid", T(lang, "How-to guide", "Guide pratique", "دليل عملي")),
        ("14:00", T(lang, "Key takeaways", "À retenir", "الخلاصة"),
         T(lang, "Send the welcome pack on day one.", "Envoyez le kit de bienvenue dès le premier jour.", "أرسل حزمة الترحيب في اليوم الأول."),
         "play", T(lang, "Short-form scripts", "Scripts courts", "نصوص فيديو قصيرة")),
    ]


def youtube(lang):
    ch = _yt_chapters(lang)
    caps = "".join(f'<span style="--k:{k}">{c[2]}</span>' for k, c in enumerate(ch))
    person = (
        '<svg class="sources-yt-art" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
        '<rect x="176" y="26" width="120" height="78" rx="6" class="sources-yt-board"/>'
        '<path d="M190 46h70M190 60h88M190 74h54" class="sources-yt-ink"/><path d="M262 88l12-14 10 8 12-18" class="sources-yt-ink2"/>'
        '<circle cx="112" cy="70" r="24" class="sources-yt-body"/><path d="M58 180c0-38 24-62 54-62s54 24 54 62z" class="sources-yt-body"/></svg>'
    )
    tx = "".join(
        f'<p class="sources-yt-line" style="--k:{k}"><time dir="ltr">{c[0]}</time><span>{c[2]}</span></p>' for k, c in enumerate(ch)
    )
    player = (
        f'<div class="sources-yt-player"><div class="sources-yt-screen">{person}'
        f'<div class="sources-yt-hud">{label(EXAMPLE[lang])}<span class="sources-yt-name">{T(lang, "Onboarding new clients in one week", "Intégrer un client en une semaine", "إعداد العملاء الجدد في أسبوع")}</span></div>'
        f'<div class="sources-yt-caps" aria-hidden="true">{caps}</div></div>'
        f'<div class="sources-yt-ctrl"><span class="sources-yt-btn">{icon("play")}</span><span class="sources-yt-time" dir="ltr">04:40 / 18:40</span>'
        f'<span class="sources-yt-cc">CC</span><span class="sources-yt-btn">{icon("screen")}</span></div></div>'
    )
    trans = (
        f'<div class="sources-yt-tx"><div class="sources-yt-txh">{icon("doc")}<b>{T(lang, "Transcript", "Transcription", "النص المفرّغ")}</b>'
        f'<span>{T(lang, "4 chapters", "4 chapitres", "4 فصول")}</span></div>{tx}'
        f'<p class="sources-yt-rev">{icon("check")}{T(lang, "An editor checks every claim before it becomes a page.", "Un éditeur vérifie chaque affirmation avant publication.", "يراجع محرر كل معلومة قبل أن تصبح صفحة.")}</p></div>'
    )
    bars = "".join(f'<span class="sources-yt-seg" style="--k:{k}"><i></i></span>' for k in range(4))
    names = "".join(
        f'<span class="sources-yt-name-c" style="--k:{k}"><time dir="ltr">{c[0]}</time><b>{c[1]}</b></span>' for k, c in enumerate(ch)
    )
    tiles = "".join(
        f'<div class="sources-yt-slot" style="--k:{k}"><span class="sources-yt-drop" aria-hidden="true">{icon("doc")}</span>'
        f'{tile(c[3], c[4], T(lang, f"From chapter {k + 1}", f"Du chapitre {k + 1}", f"من الفصل {k + 1}"), "sources-yt-tile sources-so-st", k + 2, 2)}</div>'
        for k, c in enumerate(ch)
    )
    timeline = (
        f'<div class="sources-yt-tl"><div class="sources-yt-bars" aria-hidden="true">{bars}<span class="sources-yt-fill"></span><span class="sources-yt-head"><i></i></span></div>'
        f'<div class="sources-yt-names">{names}</div></div>'
    )
    return f'<div class="sources-yt"><div class="sources-yt-top">{player}{trans}</div>{timeline}<div class="sources-yt-out">{tiles}</div></div>'


def youtube_transcript(lang):
    f1, f2, f3 = (T(lang, "um,", "euh,", "يعني،"), T(lang, "you know,", "vous voyez,", "كما تعلمون،"), T(lang, "basically, honestly,", "en gros, franchement,", "بصراحة، في الأساس،"))
    spoken = [
        ("04:41", T(lang, f'So, <s>{f1}</s> the question I get most is, <s>{f2}</s> how long setup really takes.',
                    f'Alors, <s>{f1}</s> la question qu’on me pose le plus, <s>{f2}</s> c’est combien de temps prend vraiment la mise en place.',
                    f'إذن، <s>{f1}</s> أكثر سؤال يصلني، <s>{f2}</s> هو كم يستغرق الإعداد فعلا.')),
        ("04:52", T(lang, f'And <s>{f3}</s> it is about a week if the welcome pack goes out on day one.',
                    f'Et <s>{f3}</s> c’est environ une semaine si le kit de bienvenue part le premier jour.',
                    f'و<s>{f3}</s> يستغرق نحو أسبوع إذا أُرسلت حزمة الترحيب في اليوم الأول.')),
        ("05:07", T(lang, "Then the second thing people ask about is pricing, which we will get to.", "Ensuite on me demande souvent le prix, on y viendra.", "ثم يسألني الناس عن السعر، وسنصل إلى ذلك.")),
    ]
    rows = "".join(
        f'<p class="sources-yv-row sources-so-st" style="--i:{k + 1}"><time dir="ltr">{t}</time><span>{s}</span></p>' for k, (t, s) in enumerate(spoken)
    )
    q = T(lang, "How long does client onboarding take?", "Combien de temps dure l’onboarding d’un client ?", "كم يستغرق إعداد عميل جديد؟")
    a = T(lang, "About one week, when the welcome pack goes out on day one.", "Environ une semaine, si le kit de bienvenue part le premier jour.", "نحو أسبوع واحد، إذا أُرسلت حزمة الترحيب في اليوم الأول.")
    left = (
        f'<div class="sources-yv-pane sources-yv-raw"><div class="sources-yv-h">{icon("mic")}<b>{T(lang, "What you said", "Ce que vous avez dit", "ما قلته")}</b>{label(EXAMPLE[lang])}</div>{rows}</div>'
    )
    right = (
        f'<div class="sources-yv-pane sources-yv-page sources-so-st" style="--i:4"><div class="sources-yv-h">{icon("doc")}<b>{T(lang, "What AI can read", "Ce que l’IA peut lire", "ما يقرؤه الذكاء الاصطناعي")}</b><span class="sources-yv-url" dir="ltr">{BRAND}/faq</span></div>'
        f'<p class="sources-yv-q">{q}</p><p class="sources-yv-a">{a}</p><i class="vx-line" style="--w:94%"></i><i class="vx-line" style="--w:72%"></i>'
        f'<ol class="sources-yv-steps" aria-hidden="true"><li><i class="vx-line" style="--w:70%"></i></li><li><i class="vx-line" style="--w:56%"></i></li><li><i class="vx-line" style="--w:64%"></i></li></ol></div>'
    )
    ans = answer(q, [a, 62], [(BRAND, True), ("industry-report.com", False)], "Perplexity", label(EXAMPLE[lang]), "sources-yv-ans pop")
    mid = f'<div class="sources-yv-mid" aria-hidden="true">{beam()}{stamp(T(lang, "Edited", "Relu", "مراجَع"), "pop")}</div>'
    return f'<div class="sources-yv">{left}{mid}<div class="sources-yv-right">{right}<div class="sources-yv-answ" style="--i:6">{ans}</div></div></div>'


def _wave_heights(n):
    out = []
    for i in range(n):
        v = abs(math.sin(i * 0.47) * 0.6 + math.sin(i * 0.13 + 1.3) * 0.4)
        out.append(round(16 + 84 * v))
    return out


def podcast(lang):
    plan = [("h", 12), ("g", 20), ("h", 9), ("g", 24), ("h", 11), ("g", 16), ("h", 10)]
    hs = _wave_heights(sum(n for _, n in plan))
    bars, i = "", 0
    for who, n in plan:
        for _ in range(n):
            bars += f'<i class="sources-spw-{who}" style="--h:{hs[i]}%;--d:-{(i * 0.173) % 1.6:.2f}s"></i>'
            i += 1
    return f'<div class="sources-spw"><div class="sources-spw-glow"></div><div class="sources-spw-wave">{bars}</div><div class="sources-spw-axis"></div></div>'


def _mini_wave():
    hs = _wave_heights(48)
    seg = [("h", 8), ("g", 14), ("h", 7), ("g", 12), ("h", 7)]
    out, i = "", 0
    for who, n in seg:
        for _ in range(n):
            out += f'<i class="sources-spw-{who}" style="--h:{hs[i]}%;--d:-{(i * 0.21) % 1.6:.2f}s"></i>'
            i += 1
    return out


def podcast_cards(lang):
    host, guest = T(lang, "Host", "Hôte", "المقدّم"), T(lang, "Guest", "Invité", "الضيف")
    quote = T(lang, "“Write the answer first. Then earn the right to explain.”", "« Écrivez d’abord la réponse. Expliquez ensuite. »", "«اكتب الإجابة أولا، ثم اشرح.»")
    faq = T(lang, "How often should a small team publish?", "À quel rythme une petite équipe doit-elle publier ?", "كم مرة ينبغي لفريق صغير أن ينشر؟")
    cmp_rows = [
        (T(lang, "Starts from", "Part de", "نقطة البداية"), T(lang, "Buyer questions", "Questions d’acheteurs", "أسئلة المشترين"), T(lang, "Keywords", "Mots-clés", "الكلمات المفتاحية")),
        (T(lang, "Format", "Format", "الصيغة"), T(lang, "One answer per page", "Une réponse par page", "إجابة واحدة لكل صفحة"), T(lang, "One long guide", "Un long guide", "دليل طويل واحد")),
    ]
    rows = "".join(f'<span>{a}</span><b>{b}</b><em>{c}</em>' for a, b, c in cmp_rows)
    return (
        f'<div class="sources-pc"><div class="sources-pc-wave" aria-hidden="true">{_mini_wave()}</div><div class="sources-pc-legend sources-so-st">{label(EXAMPLE[lang])}<span class="sources-pc-sp sources-pc-h">{host}</span><span class="sources-pc-sp sources-pc-g">{guest}</span></div>'
        f'<div class="sources-pc-card sources-so-st" style="--i:1"><div class="sources-pc-top"><span class="sources-pc-kind">{icon("quote")}{T(lang, "Quote card", "Citation", "بطاقة اقتباس")}</span><span class="sources-pc-t sources-pc-g" dir="ltr">12:04</span></div><p class="sources-pc-quote">{quote}</p></div>'
        f'<div class="sources-pc-card sources-so-st" style="--i:2"><div class="sources-pc-top"><span class="sources-pc-kind">{icon("question")}{T(lang, "FAQ entry", "Entrée FAQ", "سؤال شائع")}</span><span class="sources-pc-t sources-pc-h" dir="ltr">05:30</span></div><p class="sources-pc-q">{faq}</p><i class="vx-line" style="--w:90%"></i><i class="vx-line" style="--w:62%"></i></div>'
        f'<div class="sources-pc-card sources-so-st" style="--i:3"><div class="sources-pc-top"><span class="sources-pc-kind">{icon("columns")}{T(lang, "Guest comparison", "Comparatif de l’invité", "مقارنة الضيف")}</span><span class="sources-pc-t sources-pc-g" dir="ltr">31:15</span></div>'
        f'<div class="sources-pc-cmp"><span></span><b>{guest}</b><em>{T(lang, "Usual", "Habituel", "المعتاد")}</em>{rows}</div></div></div>'
    )


def podcast_month(lang):
    weeks = [
        (T(lang, "Week 1", "Semaine 1", "الأسبوع 1"), T(lang, "Release week", "Semaine de sortie", "أسبوع النشر"),
         [("mic", T(lang, "Episode goes live", "Sortie de l’épisode", "نشر الحلقة"), True), ("doc", T(lang, "Episode article", "Article de l’épisode", "مقال الحلقة"), False), ("quote", T(lang, "Quote cards", "Citations", "بطاقات اقتباس"), False)]),
        (T(lang, "Week 2", "Semaine 2", "الأسبوع 2"), T(lang, "Answers", "Réponses", "إجابات"),
         [("chat", T(lang, "Question page", "Page question", "صفحة سؤال"), False), ("chat", T(lang, "Question page", "Page question", "صفحة سؤال"), False), ("mail", T(lang, "Newsletter issue", "Newsletter", "عدد النشرة"), False)]),
        (T(lang, "Week 3", "Semaine 3", "الأسبوع 3"), T(lang, "Clips", "Extraits", "مقاطع"),
         [("play", T(lang, "Short-form script", "Script court", "نص فيديو قصير"), False), ("grid", T(lang, "Glossary entry", "Entrée de glossaire", "مدخل في المسرد"), False), ("linkedin", T(lang, "Social post", "Post social", "منشور اجتماعي"), False)]),
        (T(lang, "Week 4", "Semaine 4", "الأسبوع 4"), T(lang, "Still working", "Toujours actif", "ما زال يعمل"),
         [("chat", T(lang, "Question page", "Page question", "صفحة سؤال"), False), ("layers", T(lang, "Guest comparison", "Comparatif invité", "مقارنة الضيف"), False), ("linkedin", T(lang, "Social post", "Post social", "منشور اجتماعي"), False)]),
    ]
    cols, n = "", 0
    for k, (w, sub, items) in enumerate(weeks):
        chips = ""
        for ic, t, hl in items:
            n += 1
            chips += f'<span class="sources-pm-c sources-so-st{" is-hl" if hl else ""}" style="--i:{n}">{icon(ic)}{t}</span>'
        cols += f'<div class="sources-pm-w"><div class="sources-pm-h"><b>{w}</b><small>{sub}</small></div>{chips}</div>'
    return f'<div class="sources-pm"><div class="sources-pm-top">{label(EXAMPLE[lang])}<span>{T(lang, "One episode across one month", "Un épisode sur un mois", "حلقة واحدة على امتداد شهر")}</span></div><div class="sources-pm-grid"><span class="sources-pm-now" aria-hidden="true"></span>{cols}</div></div>'


def webinar(lang):
    qs = [
        ("A", T(lang, "How long does onboarding take for a team of ten?", "Combien de temps dure l’onboarding pour une équipe de dix ?", "كم يستغرق الإعداد لفريق من عشرة أشخاص؟")),
        ("M", T(lang, "Does it work with the tools we already use?", "Est-ce compatible avec nos outils actuels ?", "هل يعمل مع الأدوات التي نستخدمها حاليا؟")),
        ("S", T(lang, "What changes for the sales team?", "Qu’est-ce qui change pour l’équipe commerciale ?", "ما الذي يتغير بالنسبة لفريق المبيعات؟")),
    ]
    att = T(lang, "Attendee", "Participant", "مشارك")
    qa = "".join(
        f'<div class="sources-wb-q sources-wb-q{k}"><span class="sources-wb-av">{a}</span><div><small>{att}</small><p>{q}</p></div><span class="sources-wb-to sources-wb-t{k}">{icon("check")}FAQ</span></div>'
        for k, (a, q) in enumerate(qs)
    )
    faq = "".join(f'<div class="sources-wb-f sources-wb-f{k}"><b>{q}</b>{icon("plus")}</div>' for k, (_, q) in enumerate(qs))
    chart = "".join(f'<i style="--s:{s}"></i>' for s in [0.42, 0.58, 0.5, 0.74, 0.92])
    slide = (
        f'<div class="sources-wb-stage"><div class="sources-wb-slide"><span class="sources-wb-kick" dir="ltr">07 / 24</span>'
        f'<p class="sources-wb-so-st">{T(lang, "Three ways to shorten onboarding", "Trois façons d’accélérer l’onboarding", "ثلاث طرق لتقصير مدة الإعداد")}</p>'
        f'<div class="sources-wb-sb"><div class="sources-wb-bul" aria-hidden="true"><i style="--w:86%"></i><i style="--w:70%"></i><i style="--w:78%"></i></div>'
        f'<div class="sources-wb-chart" aria-hidden="true">{chart}</div></div></div>'
        f'<div class="sources-wb-cam"><span class="sources-wb-face">{icon("user")}</span><span class="sources-wb-mic" aria-hidden="true"><i></i><i></i><i></i></span></div></div>'
    )
    return (
        f'<div class="sources-wb"><div class="sources-wb-win"><div class="sources-wb-bar"><span class="sources-wb-live"><i></i>LIVE</span>'
        f'<span class="sources-wb-ttl">{T(lang, "Webinar", "Webinaire", "ندوة رقمية")}</span>{label(EXAMPLE[lang])}</div>'
        f'<div class="sources-wb-grid">{slide}<div class="sources-wb-qa"><div class="sources-wb-qh">{icon("chat")}<b>{T(lang, "Live Q&amp;A", "Questions en direct", "أسئلة مباشرة")}</b></div>{qa}</div></div></div>'
        f'<div class="sources-wb-faq"><div class="sources-wb-fh">{icon("question")}<b>{T(lang, "FAQ page", "Page FAQ", "صفحة الأسئلة الشائعة")}</b><span dir="ltr">{BRAND}/faq</span></div>{faq}</div></div>'
    )


def webinar_layer(lang):
    rows = [
        ("slides", "00:06", T(lang, "The framework on your slides", "Le cadre présenté sur vos slides", "الإطار المعروض في شرائحك"), "doc", T(lang, "Pillar article", "Article pilier", "مقال محوري")),
        ("question", "41:20", T(lang, "Every live question", "Chaque question du direct", "كل سؤال طُرح مباشرة"), "chat", T(lang, "FAQ cluster", "Cluster FAQ", "مجموعة أسئلة شائعة")),
        ("columns", "18:30", T(lang, "Alternatives you compared", "Les alternatives comparées", "البدائل التي قارنتها"), "layers", T(lang, "Comparison page", "Page comparatif", "صفحة مقارنة")),
        ("shield", "44:05", T(lang, "Objections from the chat", "Les objections du chat", "الاعتراضات في المحادثة"), "target", T(lang, "Sales enablement pages", "Pages d’aide à la vente", "صفحات دعم المبيعات")),
        ("user", "52:00", T(lang, "Attendees and no-shows", "Présents et absents", "الحاضرون والغائبون"), "mail", T(lang, "Follow-up emails", "E-mails de suivi", "رسائل متابعة")),
    ]
    out = ""
    for k, (ic, t, src, oic, dst) in enumerate(rows):
        out += (
            f'<div class="sources-wl-r sources-so-st" style="--i:{k + 1}"><div class="sources-wl-s"><span class="sources-wl-ic">{icon(ic)}</span><span><time dir="ltr">{t}</time><b>{src}</b></span></div>'
            f'{beam()}{tile(oic, dst, "", "sources-wl-t" + (" is-hl" if k == 1 else ""), k, 0)}</div>'
        )
    head = (
        f'<div class="sources-wl-h"><span>{T(lang, "In the session", "Pendant la session", "في الجلسة")}</span>{label(EXAMPLE[lang])}'
        f'<span>{T(lang, "On your site", "Sur votre site", "على موقعك")}</span></div>'
    )
    return f'<div class="sources-wl">{head}{out}</div>'


VISUALS = {
    "sources-blog": blog,
    "sources-blog-cluster": blog_cluster,
    "sources-youtube": youtube,
    "sources-youtube-transcript": youtube_transcript,
    "sources-podcast": podcast,
    "sources-podcast-cards": podcast_cards,
    "sources-podcast-month": podcast_month,
    "sources-webinar": webinar,
    "sources-webinar-layer": webinar_layer,
}
