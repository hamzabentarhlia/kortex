export function init(root) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const lang = root.dataset.lang;
  const run = root.querySelector('[data-demo-run]');
  const status = root.querySelector('[data-demo-status]');
  const flow = root.querySelector('.demo-flow');
  const stages = [...root.querySelectorAll('.ds')];
  const cards = [...root.querySelectorAll('.demo-cards li')];
  const memory = {};
  let data = null;
  let current = 'blog';
  let timers = [];
  const track = (name, props) => { if (window.kxTrack) window.kxTrack(name, props); };
  const at = (fn, ms) => { timers.push(setTimeout(fn, ms)); };
  const stop = () => { timers.forEach(clearTimeout); timers = []; };
  const source = () => data && data.sources.find((s) => s.id === current);
  const setProgress = (n) => flow.style.setProperty('--p', String(n));

  const paint = () => {
    const s = source();
    if (!s) return;
    root.querySelector('[data-demo-title]').textContent = s[lang].title;
    root.querySelector('[data-demo-meta]').textContent = s[lang].meta;
    root.querySelector('[data-demo-desc]').textContent = s[lang].desc;
    stages.forEach((li, i) => { li.querySelector('.ds-log').textContent = s.logs[lang][i]; });
    root.querySelectorAll('details.dc').forEach((d) => { d.querySelector('.dc-body').textContent = s.cards[lang][d.dataset.key]; });
  };

  const idle = () => {
    stop();
    root.dataset.state = 'idle';
    stages.forEach((li) => li.classList.remove('is-lit', 'is-active'));
    cards.forEach((li) => li.classList.remove('is-dealt'));
    root.querySelectorAll('details.dc').forEach((d) => { d.open = false; });
    setProgress(0);
    run.textContent = root.dataset.runLabel;
    status.textContent = '';
  };

  const final = () => {
    stop();
    root.dataset.state = 'done';
    stages.forEach((li) => { li.classList.add('is-lit'); li.classList.remove('is-active'); });
    cards.forEach((li) => li.classList.add('is-dealt'));
    const first = root.querySelector('details.dc');
    if (first) first.open = true;
    setProgress(1);
    run.textContent = root.dataset.replayLabel;
    status.textContent = root.dataset.done;
    memory[current] = true;
  };

  const play = () => {
    if (!data) return;
    track('demo_run', { source: current });
    if (reduce) { final(); return; }
    idle();
    root.dataset.state = 'running';
    run.textContent = root.dataset.runLabel;
    stages.forEach((li, i) => {
      at(() => {
        stages.forEach((x, j) => { x.classList.toggle('is-active', j === i); if (j < i) x.classList.add('is-lit'); });
        stages[i].classList.add('is-lit');
        setProgress(i / (stages.length - 1));
        status.textContent = stages[i].querySelector('.ds-name').textContent + '. ' + stages[i].querySelector('.ds-log').textContent;
      }, i * 600);
    });
    const dealStart = stages.length * 600;
    cards.forEach((li, k) => at(() => li.classList.add('is-dealt'), dealStart + k * 80));
    at(final, dealStart + cards.length * 80 + 100);
  };

  root.addEventListener('toggle', (e) => {
    const d = e.target;
    if (d.matches && d.matches('details.dc') && d.open && root.dataset.state === 'done') track('demo_card_flip', { asset: d.dataset.key });
  }, true);

  run.addEventListener('click', play);
  root.querySelectorAll('input[name=demo-source]').forEach((input) => {
    input.addEventListener('change', () => {
      current = input.value;
      paint();
      if (memory[current] || reduce) final(); else idle();
    });
  });

  fetch('/assets/data/demo.json').then((r) => r.json()).then((d) => {
    data = d;
    if (reduce) { final(); return; }
    idle();
  }).catch(() => { root.dataset.state = 'done'; });
}
