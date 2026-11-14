export function init(root) {
  const i18n = JSON.parse(root.dataset.i18n);
  const items = [...root.querySelectorAll('.ck-list li')];
  const total = items.length;
  const boxes = items.map((li, i) => {
    const text = li.querySelector('span:not(.ck-n)');
    const label = document.createElement('label');
    label.className = 'ck-row';
    const box = document.createElement('input');
    box.type = 'checkbox';
    box.id = 'ckb-' + i;
    label.htmlFor = box.id;
    label.append(box);
    while (li.firstChild) label.append(li.firstChild);
    li.append(label);
    return box;
  });
  const out = document.createElement('div');
  out.className = 'ck-score glass';
  out.setAttribute('role', 'region');
  out.setAttribute('aria-label', i18n.tick);
  out.innerHTML = '<p class="ck-tick"></p><p class="ck-count" aria-live="polite" aria-atomic="true"></p><div class="ck-bar" aria-hidden="true"><i></i></div><p class="ck-advice"></p><p class="ck-cta"></p><p class="ck-note"></p><button type="button" class="btn btn-ghost btn-sm ck-reset"></button>';
  out.querySelector('.ck-tick').textContent = i18n.tick;
  out.querySelector('.ck-note').textContent = i18n.note;
  out.querySelector('.ck-reset').textContent = i18n.reset;
  root.append(out);
  const count = out.querySelector('.ck-count');
  const fill = out.querySelector('.ck-bar i');
  const advice = out.querySelector('.ck-advice');
  const cta = out.querySelector('.ck-cta');
  const track = (n, p) => { if (window.kxTrack) window.kxTrack(n, p); };
  let reported = false;
  const update = () => {
    const n = boxes.filter((b) => b.checked).length;
    count.textContent = i18n.score.replace('{n}', String(n)).replace('{t}', String(total));
    fill.style.transform = 'scaleX(' + (n / total).toFixed(3) + ')';
    const band = n <= 13 ? 'b1' : n <= 26 ? 'b2' : 'b3';
    advice.textContent = i18n[band];
    const href = band === 'b1' ? root.dataset.book : root.dataset.audit;
    const label = band === 'b1' ? i18n.c1 : i18n.c2;
    cta.replaceChildren();
    const a = document.createElement('a');
    a.className = 'btn btn-primary btn-sm';
    a.href = href;
    a.textContent = label;
    a.dataset.cta = 'ck-score-' + band;
    cta.append(a);
    if (n > 0 && !reported) { reported = true; track('checklist_self_score', { page: location.pathname }); }
  };
  boxes.forEach((b) => b.addEventListener('change', update));
  out.querySelector('.ck-reset').addEventListener('click', () => { boxes.forEach((b) => { b.checked = false; }); reported = false; update(); });
  update();
}
