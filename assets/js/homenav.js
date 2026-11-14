export function init(nav) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const marked = [...document.querySelectorAll('main > section[data-nav]')];
  const secs = marked.length ? marked : [...document.querySelectorAll('main > section[aria-labelledby]')].filter((s) => !s.classList.contains('hero') && !s.classList.contains('cta-band') && s.querySelector('h2')).slice(0, 8);
  const hero = document.querySelector('main > .hero');
  if (secs.length < 3) return;
  const list = document.createElement('ol');
  const items = secs.map((s, i) => {
    if (!s.id) s.id = 'sec-' + (i + 1);
    const label = (s.dataset.nav || s.querySelector('h2').textContent).trim();
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + s.id;
    const dot = document.createElement('i');
    const txt = document.createElement('span');
    txt.textContent = label;
    a.append(dot, txt);
    li.append(a);
    list.append(li);
    a.addEventListener('click', (e) => {
      e.preventDefault();
      s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      history.replaceState(null, '', '#' + s.id);
    });
    return { s, a };
  });
  nav.append(list);
  if (hero) {
    new IntersectionObserver((es) => nav.classList.toggle('is-on', !es[0].isIntersecting && es[0].boundingClientRect.top < 0)).observe(hero);
  } else nav.classList.add('is-on');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      items.forEach((it) => { if (it.s === en.target) it.a.setAttribute('aria-current', 'true'); else it.a.removeAttribute('aria-current'); });
    });
  }, { rootMargin: '-35% 0px -55% 0px' });
  items.forEach((it) => io.observe(it.s));
}
