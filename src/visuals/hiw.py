from . import kit, portal
from .kit import T, icon, tile, label, cite, chip, stamp


def _stations(lang):
    return [
        ("extract", T(lang, "Extract", "Extraire", "الاستخراج"),
         T(lang, "We pull the expertise out", "Nous en tirons l'expertise", "نستخرج الخبرة"),
         T(lang, "The source is transcribed in full. Agents list every claim, example, number, objection and question you answer, with a pointer back to where you said it. Nothing gets invented later.",
           "La source est intégralement transcrite. Les agents listent chaque affirmation, exemple, chiffre, objection et question traitée, avec un renvoi vers le passage d'origine. Rien n'est inventé ensuite.",
           "يُفرَّغ المصدر نصيا بالكامل، ويرصد الوكلاء كل فكرة ومثال ورقم واعتراض وسؤال تجيب عنه، مع الإشارة إلى موضعه في المصدر. فلا يُختلق شيء لاحقا.")),
        ("structure", T(lang, "Structure", "Structurer", "التنظيم"),
         T(lang, "We map it to real questions", "Nous la relions aux vraies questions", "نربطها بالأسئلة الحقيقية"),
         T(lang, "Your ideas are matched to the questions buyers ask AI engines, and each question gets one page. Your company, your method and your category get one name each, used everywhere.",
           "Vos idées sont associées aux questions que vos acheteurs posent aux moteurs IA, et chaque question reçoit une page. Votre entreprise, votre méthode et votre catégorie reçoivent chacune un nom unique, utilisé partout.",
           "نطابق أفكارك مع الأسئلة التي يطرحها المشترون على محركات الذكاء الاصطناعي، ولكل سؤال صفحة. ولشركتك ومنهجك وفئتك اسم واحد لكل منها يُستخدم في كل مكان.")),
        ("produce", T(lang, "Produce", "Produire", "الإنتاج"),
         T(lang, "Agents draft each asset", "Les agents rédigent chaque contenu", "يكتب الوكلاء كل محتوى"),
         T(lang, "Each agent works on one format and follows the same plan, so the pieces link together and say the same thing.",
           "Chaque agent travaille sur un format et suit le même plan, pour que les contenus se répondent et disent la même chose.",
           "يعمل كل وكيل على صيغة واحدة ويتبع الخطة نفسها، فتترابط المحتويات وتقول الشيء نفسه.")),
        ("review", T(lang, "Human review", "Relecture humaine", "المراجعة البشرية"),
         T(lang, "An editor checks, you approve", "Un éditeur vérifie, vous validez", "يتحقق محرر، وتعتمد أنت"),
         T(lang, "A person reads every asset against the extraction list. Any claim we cannot trace to your source is flagged for you, not published. Nothing goes live until you approve it.",
           "Une personne relit chaque contenu au regard de la liste d'extraction. Toute affirmation impossible à rattacher à votre source vous est signalée, jamais publiée. Rien ne part sans votre accord.",
           "يقرأ شخص كل محتوى مقارنة بقائمة الاستخراج، وأي معلومة لا يمكن ردها إلى مصدرك نعرضها عليك ولا ننشرها. ولا يُنشر شيء قبل موافقتك.")),
        ("publish", T(lang, "Publish and measure", "Publier et mesurer", "النشر والقياس"),
         T(lang, "Live, then measured", "En ligne, puis mesuré", "يُنشر ثم يُقاس"),
         T(lang, "Pages ship answer-first, with schema markup and internal links. Each month we ask a fixed set of buyer questions to the main AI engines and record who gets cited.",
           "Les pages répondent d'abord, avec un balisage schema et des liens internes. Chaque mois, nous posons une liste fixe de questions d'acheteurs aux principaux moteurs IA et notons qui est cité.",
           "تبدأ الصفحات بالإجابة، مع ترميز Schema وروابط داخلية. وكل شهر نطرح قائمة ثابتة من أسئلة المشترين على محركات الذكاء الاصطناعي الرئيسية ونسجل من يُستشهد به.")),
    ]


def _art_extract(lang):
    segs = [
        (T(lang, "Most audits happen once a year.", "La plupart des audits ont lieu une fois par an.", "معظم عمليات التدقيق تتم مرة في السنة."), True),
        (T(lang, "And the room nods.", "Et tout le monde acquiesce.", "ويومئ الحاضرون."), False),
        (T(lang, "Payment delays show up months before a missed delivery.", "Les retards de paiement apparaissent des mois avant une livraison manquée.", "تأخر المدفوعات يظهر قبل أشهر من أي تأخر في التسليم."), True),
        (T(lang, "How often should you review a supplier?", "À quelle fréquence revoir un fournisseur ?", "كم مرة يجب مراجعة المورد؟"), True),
    ]
    tr = "".join(f'<span class="hl-seg{" is-hl" if h else ""}">{t}</span> ' for t, h in segs)
    pulls = [(T(lang, "Claim", "Affirmation", "فكرة"), "12:40"), (T(lang, "Number", "Chiffre", "رقم"), "18:05"), (T(lang, "Question", "Question", "سؤال"), "27:30")]
    chips = "".join(f'<li class="hl-k" style="--o:{n}"><b>{a}</b><span dir="ltr">{b}</span></li>' for n, (a, b) in enumerate(pulls))
    return (
        f'<div class="hl-ex"><div class="hl-doc"><div class="hl-doc-h">{icon("mic")}<b>{T(lang, "Transcript", "Transcription", "النص المفرغ")}</b>{label(kit.EXAMPLE[lang])}</div><p>{tr}</p></div>'
        f'<div class="hl-ex-beam">{kit.beam()}</div><ul class="hl-pulls">{chips}</ul></div>'
    )


def _art_structure(lang):
    qs = [T(lang, "How often should suppliers be reviewed?", "À quelle fréquence revoir ses fournisseurs ?", "كم مرة يجب مراجعة الموردين؟"),
          T(lang, "Spreadsheet or dedicated tool?", "Tableur ou outil dédié ?", "جداول البيانات أم أداة مخصصة؟"),
          T(lang, "What is a supplier risk score?", "Qu'est-ce qu'un score de risque ?", "ما هو مؤشر المخاطر؟")]
    pages = [("chat", T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة")), ("columns", T(lang, "Comparison", "Comparatif", "مقارنة")), ("grid", T(lang, "Glossary", "Glossaire", "معجم"))]
    rows = "".join(
        f'<li class="hl-map" style="--o:{n}"><span class="hl-q">{icon("question")}{q}</span><i class="hl-link" aria-hidden="true"></i><span class="hl-page">{icon(ic)}{pt}</span></li>'
        for n, (q, (ic, pt)) in enumerate(zip(qs, pages))
    )
    prof = f'<div class="vx hl-prof" data-v="portal-profile">{portal.profile_card(lang)}</div>'
    return f'<div class="hl-st"><ul class="hl-maps">{rows}</ul>{prof}</div>'


def _art_produce(lang):
    fm = [("doc", T(lang, "Pillar article", "Article pilier", "مقال محوري")), ("columns", T(lang, "Comparison page", "Page comparative", "صفحة مقارنة")),
          ("chat", T(lang, "FAQ page", "Page FAQ", "صفحة أسئلة شائعة")), ("grid", T(lang, "Glossary entries", "Entrées de glossaire", "مداخل المعجم")),
          ("linkedin", T(lang, "LinkedIn posts", "Posts LinkedIn", "منشورات لينكدإن")), ("mail", T(lang, "Newsletter", "Newsletter", "نشرة بريدية")),
          ("film", T(lang, "Short video scripts", "Scripts vidéo courts", "نصوص فيديو قصير"))]
    tiles = "".join(f'<div class="hl-tile" style="--o:{n}">{tile(ic, t, cls="is-hl" if n == 0 else "", lines=2)}</div>' for n, (ic, t) in enumerate(fm))
    return f'<div class="hl-prod">{tiles}</div>'


def _art_review(lang):
    ok = T(lang, "Matches the source at 18:05", "Conforme à la source, 18:05", "مطابق للمصدر عند 18:05")
    flag = T(lang, "No source for this number. Flagged for you.", "Aucune source pour ce chiffre. Signalé pour vous.", "لا مصدر لهذا الرقم. نعرضه عليك.")
    return (
        '<div class="hl-rev"><div class="hl-draft">'
        f'<div class="hl-draft-h">{icon("doc")}<b>{T(lang, "Draft: comparison page", "Brouillon : page comparative", "مسودة: صفحة مقارنة")}</b></div>'
        '<i class="vx-line" style="--w:92%"></i><i class="vx-line hl-ok-line" style="--w:78%"></i><i class="vx-line" style="--w:88%"></i><i class="vx-line hl-flag-line" style="--w:56%"></i><i class="vx-line" style="--w:84%"></i><i class="vx-line" style="--w:70%"></i>'
        f'</div><div class="hl-notes"><p class="hl-note is-ok">{icon("check")}{ok}</p><p class="hl-note is-flag">{icon("flag")}{flag}</p></div>'
        f'<div class="hl-stamp">{stamp(T(lang, "Approved by you", "Validé par vous", "اعتمدته أنت"))}</div></div>'
    )


def _art_publish(lang):
    q = T(lang, "How often should suppliers be reviewed?", "À quelle fréquence revoir ses fournisseurs ?", "كم مرة يجب مراجعة الموردين؟")
    page = (
        f'<div class="hl-page-mini"><div class="hl-pm-bar"><i></i><i></i><i></i><span dir="ltr">yourbrand.com/faq</span></div>'
        f'<div class="hl-pm-b"><b>{q}</b><p class="hl-pm-ans">{T(lang, "Answer first, in two sentences.", "La réponse d’abord, en deux phrases.", "الإجابة أولا، في جملتين.")}</p>'
        '<i class="vx-line" style="--w:90%"></i><i class="vx-line" style="--w:70%"></i>'
        '<span class="hl-schema"><code dir="ltr">FAQPage</code><code dir="ltr">Organization</code><code dir="ltr">BreadcrumbList</code></span></div></div>'
    )
    ans = kit.answer(q, [94, 80, 58], [("industry-report.com", False), (kit.BRAND, True)], engine="Perplexity", tag=label(kit.EXAMPLE[lang]), cls="hl-ans")
    check = f'<p class="hl-check">{icon("gauge")}{T(lang, "Checked every month: 10 buyer questions", "Vérifié chaque mois : 10 questions d’acheteurs", "يُفحص كل شهر: 10 أسئلة من المشترين")}</p>'
    return f'<div class="hl-pub">{page}<div class="hl-pub-r">{ans}{check}</div></div>'


ARTS = {"extract": _art_extract, "structure": _art_structure, "produce": _art_produce, "review": _art_review, "publish": _art_publish}


def line(lang):
    st = _stations(lang)
    rail = "".join(f'<li style="--n:{i}"><i></i><span>{name}</span></li>' for i, (_, name, _, _) in enumerate(st))
    src = T(lang, "Your source", "Votre source", "مصدرك")
    stations = "".join(
        f'<section class="hl-station" style="--s:{i / 4:.2f}" aria-labelledby="hl-{k}"><div class="hl-copy"><span class="hl-num">{i + 1:02d}</span>'
        f'<h3 id="hl-{k}">{h}</h3><p>{p}</p></div><div class="hl-art" aria-hidden="true">{ARTS[k](lang)}</div></section>'
        for i, (k, name, h, p) in enumerate(st)
    )
    return (
        f'<div class="hl" data-scrub="pin"><div class="hl-sticky">'
        f'<div class="hl-rail-wrap"><span class="hl-src">{icon("doc")}{src}</span><ol class="hl-rail">{rail}</ol><span class="hl-fill" aria-hidden="true"><i></i></span></div>'
        f'<div class="hl-track">{stations}</div></div></div>'
    )


VISUALS = {"hiw-line": line}
