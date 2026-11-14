export function init(root) {
  const radios = [...root.querySelectorAll('input[name=mix-source]')];
  const panels = [...root.querySelectorAll('.mix-panel')];
  root.classList.add('mix-js');
  const track = (n, p) => { if (window.kxTrack) window.kxTrack(n, p); };
  const show = (id, fire) => {
    panels.forEach((p) => { p.hidden = p.dataset.panel !== id; });
    if (fire) track('mix_source', { source: id });
  };
  radios.forEach((r) => r.addEventListener('change', () => show(r.value, true)));
  const on = radios.find((r) => r.checked);
  show(on ? on.value : panels[0].dataset.panel, false);
}
