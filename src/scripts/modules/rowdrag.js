export function init(row) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let down = false, sx = 0, sl = 0, vx = 0, last = 0, lt = 0, raf = 0, moved = false;
  const stop = () => { cancelAnimationFrame(raf); raf = 0; };
  const glide = () => {
    vx *= 0.94;
    row.scrollLeft -= vx;
    if (Math.abs(vx) > 0.4 && !down) raf = requestAnimationFrame(glide); else raf = 0;
  };
  row.addEventListener('pointerdown', (e) => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    stop();
    down = true; moved = false; sx = e.clientX; sl = row.scrollLeft; last = e.clientX; lt = performance.now(); vx = 0;
    row.setPointerCapture(e.pointerId);
  });
  row.addEventListener('pointermove', (e) => {
    if (!down) return;
    const dx = e.clientX - sx;
    if (!moved && Math.abs(dx) > 4) { moved = true; row.classList.add('is-grab'); }
    if (!moved) return;
    row.scrollLeft = sl - dx;
    const now = performance.now();
    vx = (e.clientX - last) / Math.max(1, now - lt) * 16;
    last = e.clientX; lt = now;
  });
  const end = (e) => {
    if (!down) return;
    down = false;
    row.classList.remove('is-grab');
    if (moved && !reduce) raf = requestAnimationFrame(glide);
    else if (moved) vx = 0;
    if (row.hasPointerCapture(e.pointerId)) row.releasePointerCapture(e.pointerId);
  };
  row.addEventListener('pointerup', end);
  row.addEventListener('pointercancel', end);
  row.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  row.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const card = row.querySelector('.sd');
    const step = card ? card.getBoundingClientRect().width + 16 : 320;
    const dir = (e.key === 'ArrowRight' ? 1 : -1) * (document.documentElement.dir === 'rtl' ? -1 : 1);
    row.scrollBy({ left: dir * step, behavior: reduce ? 'auto' : 'smooth' });
  });
}
