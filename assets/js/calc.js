export function init(root) {
  const lang = root.dataset.lang;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const text = JSON.parse(root.dataset.i18n);
  const fmt = new Intl.NumberFormat(lang === 'fr' ? 'fr-FR' : 'en-IE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  const prices = { GHOST: 2500, SWARM: 5500, TITAN: 12000 };
  const field = (key) => root.querySelector('[data-key=' + key + ']');
  const out = (key) => root.querySelector('[data-out=' + key + ']');
  const el = {
    current: root.querySelector('[data-current]'),
    production: root.querySelector('[data-production]'),
    time: root.querySelector('[data-time]'),
    price: root.querySelector('[data-plan-price]'),
    name: root.querySelector('[data-plan-name]'),
    per: root.querySelector('[data-perasset]'),
    verdict: root.querySelector('[data-verdict]'),
    from: root.querySelector('[data-from-label]'),
    book: root.querySelector('[data-calc-book]'),
  };
  const shown = new Map();
  let interacted = false;
  let lastPlan = null;
  const track = (name, props) => { if (window.kxTrack) window.kxTrack(name, props); };

  const planFor = (assets) => (assets <= 10 ? 'GHOST' : assets <= 24 ? 'SWARM' : 'TITAN');
  const compute = (assets, rate, hours, value) => {
    const production = assets * rate;
    const time = Math.round((hours * 52 / 12) * value);
    return { production, time, current: production + time };
  };

  const setMoney = (node, to) => {
    const from = shown.has(node) ? shown.get(node) : to;
    shown.set(node, to);
    if (reduce || from === to) { node.textContent = fmt.format(to); return; }
    const start = performance.now();
    const step = (now) => {
      const k = Math.min(1, (now - start) / 300);
      node.textContent = fmt.format(Math.round(from + (to - from) * k));
      if (k < 1) requestAnimationFrame(step); else shown.set(node, to);
    };
    requestAnimationFrame(step);
  };

  const render = () => {
    const assets = +field('assets').value;
    const rate = +field('rate').value;
    const hours = +field('hours').value;
    const value = +field('value').value;
    const r = compute(assets, rate, hours, value);
    const plan = planFor(assets);
    const price = prices[plan];
    out('assets').textContent = String(assets);
    out('rate').textContent = fmt.format(rate);
    out('hours').textContent = String(hours);
    setMoney(el.current, r.current);
    setMoney(el.production, r.production);
    setMoney(el.time, r.time);
    setMoney(el.price, price);
    el.name.textContent = plan;
    el.per.textContent = text.perasset[plan];
    el.from.hidden = plan !== 'TITAN';
    el.verdict.textContent = plan === 'TITAN'
      ? text.verdict_titan.replace('{price}', fmt.format(price))
      : price > r.current
        ? text.verdict_more.replace('{plan}', plan)
        : text.verdict_less.replace('{plan}', plan).replace('{diff}', fmt.format(r.current - price));
    const url = new URL(el.book.href);
    url.searchParams.set('notes', root.dataset.planMsg + ': ' + plan + ' (' + assets + ')');
    url.searchParams.set('utm_content', 'plan_' + plan.toLowerCase());
    el.book.href = url.toString();
    if (interacted && plan !== lastPlan) track('calc_result_plan', { plan });
    lastPlan = plan;
  };

  root.querySelector('form').addEventListener('input', () => {
    if (!interacted) { interacted = true; track('calc_interact', {}); }
    render();
  });
  lastPlan = planFor(+field('assets').value);
  render();
}
