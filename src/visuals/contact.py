import math

from .kit import T, icon, chip


def ci(name):
    return icon(name, "ct-i")


def arc(a0, a1, r=50, c=60):
    p0 = (c + r * math.sin(math.radians(a0)), c - r * math.cos(math.radians(a0)))
    p1 = (c + r * math.sin(math.radians(a1)), c - r * math.cos(math.radians(a1)))
    big = 1 if a1 - a0 > 180 else 0
    return f"M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {big} 1 {p1[0]:.1f} {p1[1]:.1f}"


def call(lang):
    arcs = "".join(f'<path class="ct-arc ct-arc-{k}" d="{arc(k * 120 + 6, k * 120 + 114)}"/>' for k in range(3))
    ticks = "".join(
        f'<line x1="{60 + 41 * math.sin(math.radians(a)):.1f}" y1="{60 - 41 * math.cos(math.radians(a)):.1f}" x2="{60 + 37 * math.sin(math.radians(a)):.1f}" y2="{60 - 37 * math.cos(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 30)
    )
    clock = (
        f'<div class="ct-clock ct-pop" aria-hidden="true"><svg viewBox="0 0 120 120" focusable="false">'
        f'<circle class="ct-track" cx="60" cy="60" r="50"/>{arcs}<g class="ct-ticks">{ticks}</g>'
        f'<g class="ct-hand"><line x1="60" y1="60" x2="60" y2="24"/></g><circle class="ct-hub" cx="60" cy="60" r="4"/></svg></div>'
    )
    head = (
        f'<div class="ct-head">{clock}<div class="ct-ht ct-up" style="--i:1"><span class="ct-min"><b>30</b> {T(lang, "minutes", "minutes", "دقيقة")}</span>'
        f'<h2 class="ct-sub">{T(lang, "What happens on the call", "Ce qui se passe pendant l’appel", "ماذا يحدث في المكالمة")}</h2></div></div>'
    )
    engines = "".join(chip(n) for n in ["ChatGPT", "Perplexity", "Gemini"])
    sources = "".join(
        f'<span class="ct-src">{ci(ic)}</span>' for ic in ["doc", "play", "mic", "screen"]
    )
    plan = (
        f'<span class="ct-plan"><span class="ct-plan-l">{ci("check")}<i></i></span><span class="ct-plan-l">{ci("check")}<i style="--w:62%"></i></span>'
        f'<span class="ct-next">{ci("flag")}{T(lang, "Next step", "Prochaine étape", "الخطوة التالية")}</span></span>'
    )
    steps = [
        (
            T(lang, "How AI engines answer in your field", "Comment les moteurs IA répondent dans votre domaine", "كيف تجيب محركات الذكاء الاصطناعي في مجالك"),
            T(lang, "We ask a few of your buyers’ questions and see who gets cited today.", "Nous posons quelques questions de vos acheteurs et regardons qui est cité aujourd’hui.", "نطرح بعض أسئلة مشتريك ونرى من يُستشهد به اليوم."),
            f'<span class="ct-mini ct-eng">{engines}</span>',
        ),
        (
            T(lang, "What you already publish", "Ce que vous publiez déjà", "ما تنشره حاليا"),
            T(lang, "Blog, videos, podcast or webinars: we look for the expertise engines could quote.", "Blog, vidéos, podcast ou webinaires : nous repérons l’expertise que les moteurs pourraient citer.", "مدونة أو فيديوهات أو بودكاست أو ندوات: نبحث عن الخبرة التي يمكن للمحركات اقتباسها."),
            f'<span class="ct-mini ct-srcs" aria-hidden="true">{sources}</span>',
        ),
        (
            T(lang, "Your recommended plan and next step", "Votre plan recommandé et la prochaine étape", "خطتك المقترحة والخطوة التالية"),
            T(lang, "You leave with a clear recommendation. If KORTEX is not the right fit, we say so.", "Vous repartez avec une recommandation claire. Si KORTEX ne vous convient pas, nous vous le disons.", "تخرج بتوصية واضحة. وإن لم تكن KORTEX مناسبة لك، نقول لك ذلك."),
            f'<span class="ct-mini" aria-hidden="true">{plan}</span>',
        ),
    ]
    items = "".join(
        f'<li class="ct-step ct-step-{k} ct-up" style="--i:{k + 2}"><span class="ct-num"><b>{k + 1}</b></span>'
        f'<div class="ct-body"><h3>{title}</h3><p>{body}</p>{mini}</div></li>'
        for k, (title, body, mini) in enumerate(steps)
    )
    foot = f'<p class="ct-foot ct-up" style="--i:6">{ci("clock")}{T(lang, "Video call. You decide what happens next.", "Appel vidéo. Vous décidez de la suite.", "مكالمة فيديو، وأنت من يقرر الخطوة التالية.")}</p>'
    return f'<div class="ct-call">{head}<ol class="ct-steps">{items}</ol>{foot}</div>'


VISUALS = {"contact-call": call}
