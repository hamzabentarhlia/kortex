export function init(host) {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cv = document.createElement('canvas');
  cv.className = 'kx-field';
  cv.setAttribute('aria-hidden', 'true');
  host.prepend(cv);
  const ctx = cv.getContext('2d');
  if (!ctx) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let w = 0, h = 0, nodes = [], raf = 0, visible = true, ink = '244,237,227';
  const pointer = { x: -999, y: -999 };

  const readInk = () => {
    const hex = getComputedStyle(document.documentElement).getPropertyValue('--text').trim();
    const m = /^#?([0-9a-f]{6})$/i.exec(hex);
    if (m) ink = [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16)).join(',');
  };

  const size = () => {
    const r = host.getBoundingClientRect();
    w = Math.max(1, Math.round(r.width));
    h = Math.max(1, Math.round(r.height));
    cv.width = w * dpr;
    cv.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = w < 700 ? 22 : 44;
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.18, vy: (Math.random() - 0.5) * 0.18,
    }));
  };

  const draw = () => {
    ctx.clearRect(0, 0, w, h);
    const link = w < 700 ? 110 : 140;
    for (const n of nodes) {
      if (!reduce) {
        const dx = pointer.x - n.x, dy = pointer.y - n.y, d = Math.hypot(dx, dy);
        if (d < 170 && d > 1) { n.vx += (dx / d) * 0.012; n.vy += (dy / d) * 0.012; }
        n.vx *= 0.985; n.vy *= 0.985;
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;
      }
    }
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < link) {
          ctx.strokeStyle = 'rgba(' + ink + ',' + (0.14 * (1 - d / link)).toFixed(3) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
    }
    ctx.fillStyle = 'rgba(' + ink + ',0.22)';
    for (const n of nodes) { ctx.beginPath(); ctx.arc(n.x, n.y, 1.6, 0, 6.2832); ctx.fill(); }
  };

  const loop = () => { draw(); raf = visible && !document.hidden ? requestAnimationFrame(loop) : 0; };
  const start = () => { if (!raf && !reduce) raf = requestAnimationFrame(loop); };

  readInk();
  size();
  draw();
  if (reduce) return;

  host.addEventListener('pointermove', (e) => {
    const r = host.getBoundingClientRect();
    pointer.x = e.clientX - r.left; pointer.y = e.clientY - r.top;
  }, { passive: true });
  host.addEventListener('pointerleave', () => { pointer.x = -999; pointer.y = -999; });
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; if (visible) start(); }).observe(host);
  document.addEventListener('visibilitychange', start);
  let t = 0;
  new ResizeObserver(() => { clearTimeout(t); t = setTimeout(size, 150); }).observe(host);
  new MutationObserver(readInk).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  start();
}
