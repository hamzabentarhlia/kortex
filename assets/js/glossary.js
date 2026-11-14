export function init(root) {
  const i18n = JSON.parse(root.dataset.i18n);
  root.classList.add('gt-js');
  root.querySelectorAll('.gt').forEach((card) => {
    const front = card.querySelector('.gt-front');
    const back = card.querySelector('.gt-back');
    if (!back.querySelector('p')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'gt-flip';
    btn.setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-label', i18n.flip);
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 0 1 14-5.3M20 4v4h-4M20 12a8 8 0 0 1-14 5.3M4 20v-4h4"/></svg>';
    card.append(btn);
    back.inert = true;
    btn.addEventListener('click', () => {
      const on = !card.classList.contains('is-flipped');
      card.classList.toggle('is-flipped', on);
      btn.setAttribute('aria-pressed', String(on));
      btn.setAttribute('aria-label', on ? i18n.back : i18n.flip);
      front.inert = on;
      back.inert = !on;
    });
  });
  const links = [...root.querySelectorAll('.gl-rail a')];
  const secs = [...root.querySelectorAll('.gl-letter')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  links.forEach((a) => a.addEventListener('click', (e) => {
    const t = root.querySelector(a.hash);
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', a.hash);
  }));
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      links.forEach((a) => { if (a.dataset.letter === en.target.dataset.letter) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  secs.forEach((s) => io.observe(s));
}
