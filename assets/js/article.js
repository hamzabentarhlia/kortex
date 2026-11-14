export function init(body) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const bar = document.createElement('div');
  bar.className = 'read-progress';
  bar.setAttribute('aria-hidden', 'true');
  const fill = document.createElement('i');
  bar.append(fill);
  document.body.append(bar);

  let tick = 0;
  const update = () => {
    tick = 0;
    const r = body.getBoundingClientRect();
    const total = r.height - window.innerHeight * 0.6;
    const p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    fill.style.transform = 'scaleX(' + p.toFixed(4) + ')';
  };
  const onScroll = () => { if (!tick) tick = requestAnimationFrame(update); };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();

  const heads = [...body.querySelectorAll(':scope > h2')].filter((h) => h.textContent.trim());
  if (heads.length < 3) return;
  const used = new Set([...document.querySelectorAll('[id]')].map((e) => e.id));
  heads.forEach((h, i) => {
    if (h.id) return;
    let id = h.textContent.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48) || 'section-' + (i + 1);
    while (used.has(id)) id += '-x';
    used.add(id);
    h.id = id;
  });

  const nav = document.createElement('nav');
  nav.className = 'toc';
  nav.setAttribute('aria-label', document.documentElement.lang === 'fr' ? 'Sommaire' : document.documentElement.lang === 'ar' ? 'المحتويات' : 'Contents');
  const title = document.createElement('h2');
  title.textContent = nav.getAttribute('aria-label');
  const ol = document.createElement('ol');
  const links = heads.map((h) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent.trim();
    li.append(a);
    ol.append(li);
    return a;
  });
  nav.append(title, ol);
  body.append(nav);

  const setCurrent = (id) => links.forEach((a) => {
    if (a.hash === '#' + id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) setCurrent(en.target.id); });
  }, { rootMargin: '-15% 0px -75% 0px' });
  heads.forEach((h) => io.observe(h));
  const foot = document.querySelector('.site-footer, #cta, .cta-band');
  if (foot) {
    new IntersectionObserver((es) => nav.classList.toggle('is-off', es[0].isIntersecting)).observe(foot);
  }
  links.forEach((a) => a.addEventListener('click', (e) => {
    const t = document.getElementById(a.hash.slice(1));
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', a.hash);
  }));
}
