export function init(root) {
  const i18n = JSON.parse(root.dataset.i18n);
  const chips = [...root.querySelectorAll('.bx-chip')];
  const cards = [...root.querySelectorAll('.bx-card')];
  const secs = [...root.querySelectorAll('.bx-cat')];
  const feat = root.querySelector('.bx-featured');
  const input = root.querySelector('#bx-q');
  const status = root.querySelector('.bx-status');
  const none = root.querySelector('.bx-none');
  let cat = '';
  let hits = null;
  let rows = null;
  const track = (n, p) => { if (window.kxTrack) window.kxTrack(n, p); };

  const all = document.createElement('button');
  all.type = 'button';
  all.className = 'bx-chip';
  all.dataset.cat = '';
  all.textContent = i18n.all;
  chips[0].parentNode.prepend(all);
  chips.unshift(all);
  chips.forEach((c) => {
    if (c.tagName === 'A') {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'bx-chip';
      b.dataset.cat = c.dataset.cat;
      b.innerHTML = c.innerHTML;
      c.replaceWith(b);
      chips[chips.indexOf(c)] = b;
    }
  });
  const buttons = chips;

  const render = () => {
    let shown = 0;
    cards.forEach((c) => {
      const okCat = !cat || c.dataset.cat === cat;
      const okQ = !hits || hits.has(c.getAttribute('href'));
      c.hidden = !(okCat && okQ);
      if (!c.hidden) shown++;
    });
    secs.forEach((s) => { s.hidden = !s.querySelector('.bx-card:not([hidden])'); });
    if (feat) feat.hidden = !(feat.querySelector('.bx-card:not([hidden])'));
    none.hidden = shown !== 0;
    status.textContent = hits || cat ? i18n.found.replace('{n}', String(shown)) : '';
    buttons.forEach((b) => b.setAttribute('aria-pressed', String((b.dataset.cat || '') === cat)));
  };

  buttons.forEach((b) => b.addEventListener('click', () => { cat = b.dataset.cat || ''; if (cat) track('blog_filter', { category: cat }); render(); }));

  const load = () => rows ? Promise.resolve(rows) : fetch(root.dataset.index).then((r) => r.json()).then((d) => { rows = d; return d; });
  let timer = 0;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const q = input.value.trim().toLowerCase();
      if (!q) { hits = null; render(); return; }
      load().then((d) => {
        const words = q.split(/\s+/);
        hits = new Set(d.filter((r) => { const hay = (r.t + ' ' + r.d).toLowerCase(); return words.every((w) => hay.includes(w)); }).map((r) => r.u));
        render();
        track('blog_search', { length: q.length });
      }).catch(() => { hits = null; render(); });
    }, 120);
  });
  render();
}
