export function init(root) {
  const lang = document.documentElement.lang === 'fr' ? 'fr' : 'en';
  const say = { en: { diff: 'Highlight the differences', all: 'Show every row', sel: 'Selected plan', per: 'per month' }, fr: { diff: 'Mettre les différences en évidence', all: 'Afficher toutes les lignes', sel: 'Offre retenue', per: 'par mois' } }[lang];
  const table = document.querySelector('[data-compare]');
  if (table) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-ghost btn-sm pr-diff';
    btn.setAttribute('aria-pressed', 'false');
    btn.textContent = say.diff;
    table.closest('.tbl-wrap').before(btn);
    table.querySelectorAll('tbody tr').forEach((tr) => {
      const cells = [...tr.querySelectorAll('td')];
      if (cells.length < 4) return;
      const vals = cells.slice(1).map((c) => c.textContent.trim());
      if (new Set(vals).size === 1) tr.dataset.same = '1';
    });
    btn.addEventListener('click', () => {
      const on = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', String(on));
      btn.textContent = on ? say.all : say.diff;
      table.classList.toggle('is-diff', on);
    });
  }
  const bar = document.querySelector('[data-bookbar]');
  if (!bar) return;
  const label = bar.querySelector('span');
  const cta = bar.querySelector('a');
  const original = label.textContent;
  const tiers = [...document.querySelectorAll('.tier[data-plan]')];
  const price = (plan) => {
    const t = tiers.find((x) => x.dataset.plan === plan);
    const p = t && t.querySelector('.tier-price strong');
    return p ? p.textContent.trim() : '';
  };
  const apply = (plan) => {
    if (!plan) return;
    label.textContent = say.sel + ': ' + plan.toUpperCase() + ' ' + price(plan.toLowerCase());
    try {
      const u = new URL(cta.href);
      u.searchParams.set('notes', 'Plan I am considering: ' + plan.toUpperCase());
      cta.href = u.toString();
    } catch (e) { }
  };
  const read = () => {
    const m = document.querySelector('.tier.is-match');
    const c = document.querySelector('[data-plan-name]');
    return m ? m.dataset.plan : c ? c.textContent.trim().toLowerCase() : '';
  };
  const mo = new MutationObserver(() => apply(read()));
  tiers.forEach((t) => mo.observe(t, { attributes: true, attributeFilter: ['class'] }));
  const cn = document.querySelector('[data-plan-name]');
  if (cn) mo.observe(cn, { childList: true, characterData: true, subtree: true });
  const done = () => { if (!read()) label.textContent = original; else apply(read()); };
  done();
}
