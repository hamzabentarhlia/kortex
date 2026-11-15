export function init(nav) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const marked = [...document.querySelectorAll('main > section[data-nav]')];
  const indexed = [...document.querySelectorAll('main > section')].filter((s) => s.querySelector('.sx-n'));
  const secs = marked.length ? marked : indexed.slice(0, 10);
  if (secs.length < 3) return;
  const hero = document.querySelector('main > .hero');
  const covers = [...document.querySelectorAll('.site-footer, .band-invert, .cta-band')];
  const list = document.createElement('ol');
  const items = secs.map((s, i) => {
    if (!s.id) s.id = 'sec-' + (i + 1);
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + s.id;
    const dot = document.createElement('i');
    const n = document.createElement('b');
    const sx = s.querySelector('.sx-n');
    n.textContent = sx ? sx.textContent : String(i + 1).padStart(2, '0');
    const txt = document.createElement('span');
    const eb = s.querySelector('.eyebrow');
    txt.textContent = (s.dataset.nav || (eb ? eb.textContent.replace(/^\d+\s*\/?\s*/, '') : s.querySelector('h2').textContent)).trim();
    a.title = txt.textContent;
    a.append(dot, n, txt);
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
  let past = !hero;
  const over = new Set();
  const sync = () => nav.classList.toggle('is-on', past && over.size === 0);
  if (hero) new IntersectionObserver((es) => { past = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; sync(); }).observe(hero);
  const cio = new IntersectionObserver((es) => {
    es.forEach((en) => { if (en.isIntersecting) over.add(en.target); else over.delete(en.target); });
    sync();
  }, { rootMargin: '-46% 0px -46% 0px' });
  covers.forEach((c) => cio.observe(c));
  sync();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      items.forEach((it) => { if (it.s === en.target) it.a.setAttribute('aria-current', 'true'); else it.a.removeAttribute('aria-current'); });
    });
  }, { rootMargin: '-35% 0px -55% 0px' });
  items.forEach((it) => io.observe(it.s));
}
