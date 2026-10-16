// ═══════════════════════════════════════════════════════════════════
// KORTEX — CORE INTERACTION ENGINE v5.0  (drop-in replacement)
//
// • Native system cursor (no custom cursor, no cursor:none).
// • NEURON SWARM: thousands-of-tiny-dots feeling, built from ~80-190 tiny
//   neurons resting at home positions all over the viewport. When the
//   cursor moves, nearby neurons wake up, leave home on unpredictable
//   (multi-sine) paths, orbit/follow the cursor, link to each other with
//   synapse lines, then spring back home (or fade to rest) once the
//   cursor moves elsewhere or stops. Works over blocks, tables, cards.
// • Card spotlight, button ripple, smoother tilt, hero-blob mouse parallax.
// • Everything from v3/v4 preserved (reveal, magnetic, counters, nav...).
//
// ZERO HTML changes required.
// ═══════════════════════════════════════════════════════════════════
(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', () => {
    initPageLoad();
    initProgressBar();
    initNavbarScroll();
    initActiveNav();
    initScrollReveal();
    initMagneticElements();
    initTiltCards();
    initCounters();
    initParallax();
    initTextScramble();
    initLanguageSwitcher();
    initSmoothAnchors();

    initCardGlow();
    initButtonRipple();
    initBlobMouseParallax();
    initNeuronField();
  });

  function isTouchDevice() {
    return window.matchMedia('(pointer: coarse)').matches || 'ontouchstart' in window;
  }

  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

  function initPageLoad() {
    document.body.classList.add('is-ready');
  }

  // ═══════════════════════════════════════════════════════════════
  // NEURON FIELD
  // ═══════════════════════════════════════════════════════════════
  function initNeuronField() {
    if (prefersReducedMotion) return;

    const coarse = isTouchDevice();
    const TAU = Math.PI * 2;

    // ── Tunables ─────────────────────────────────────────────────
    const REST_ALPHA   = 0.09;   // brightness of sleeping neurons (set 0 to make them vanish at rest)
    const RECRUIT_R    = coarse ? 140 : 210;  // radius around the cursor where neurons light up
    const ORBIT        = coarse ? 6 : 10;     // max px a lit neuron breathes around its home
    const PUSH         = coarse ? 10 : 18;    // max px lit neurons are nudged away from the cursor
    const LINK_DIST    = coarse ? 70 : 92;    // max synapse length
    const IDLE_RELEASE = 2500;   // ms without movement before the field dims back to rest
    const HOT_SELECTOR = 'a,button,input,textarea,select,.feature-card,.pricing-card,.blog-card,.pipeline-step,' +
                         '.faq-item,.stat-card,.contact-method-card,.toc,.geo-visual-card,table,.data-table,.deliverables-table';

    // Brand colours (RGB)
    const VIOLET  = [139, 92, 246];
    const CRIMSON = [229, 9, 20];
    const CYAN    = [6, 182, 212];

    // ── Canvas ───────────────────────────────────────────────────
    const canvas = document.createElement('canvas');
    canvas.id = 'kx-neuron-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9000;';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let W = 0, H = 0, dpr = 1, builtW = 0, builtH = 0;
    let neurons = [];

    // Pre-rendered glow sprites (cheap additive-looking halos)
    function makeSprite(rgb) {
      const s = document.createElement('canvas');
      s.width = s.height = 64;
      const c = s.getContext('2d');
      const g = c.createRadialGradient(32, 32, 0, 32, 32, 32);
      g.addColorStop(0, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},0.9)`);
      g.addColorStop(0.35, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},0.25)`);
      g.addColorStop(1, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},0)`);
      c.fillStyle = g;
      c.fillRect(0, 0, 64, 64);
      return s;
    }
    const SPR_VIOLET = makeSprite(VIOLET);
    const SPR_CYAN = makeSprite(CYAN);
    const SPR_CRIMSON = makeSprite(CRIMSON);

    // ── Pointer state ────────────────────────────────────────────
    let mx = -9999, my = -9999;
    let lastMove = -1e9;
    let hot = false;
    let boost = 0;

    function setPointer(x, y, target) {
      mx = x; my = y;
      lastMove = performance.now();
      hot = !!(target && target.closest && target.closest(HOT_SELECTOR));
    }
    function release() { mx = -9999; my = -9999; hot = false; }

    window.addEventListener('pointermove', (e) => {
      if (e.pointerType === 'touch') return;
      setPointer(e.clientX, e.clientY, e.target);
    }, { passive: true });

    window.addEventListener('touchstart', (e) => {
      const t = e.touches[0];
      if (t) setPointer(t.clientX, t.clientY, e.target);
    }, { passive: true });
    window.addEventListener('touchmove', (e) => {
      const t = e.touches[0];
      if (t) setPointer(t.clientX, t.clientY, e.target);
    }, { passive: true });
    window.addEventListener('touchend', () => { lastMove = performance.now() - (IDLE_RELEASE - 600); }, { passive: true });

    document.documentElement.addEventListener('mouseleave', release);
    window.addEventListener('blur', release);

    // Click = shockwave: neurons burst outward, then spring back
    window.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'touch') return;
      const R = 270;
      for (let i = 0; i < neurons.length; i++) {
        const n = neurons[i];
        const dx = n.x - e.clientX, dy = n.y - e.clientY;
        const d = Math.hypot(dx, dy) || 1;
        if (d < R) {
          const imp = (1 - d / R) * 320;
          n.vx += (dx / d) * imp;
          n.vy += (dy / d) * imp;
          n.s = Math.max(n.s, 0.6);
        }
      }
    }, { passive: true });

    // ── Build neurons ────────────────────────────────────────────
    function build() {
      builtW = W; builtH = H;
      neurons = [];
      const count = coarse
        ? clamp(Math.round((W * H) / 5200), 70, 150)
        : clamp(Math.round((W * H) / 3000), 220, 420);
      const cell = Math.sqrt((W * H) / count);
      const cols = Math.ceil(W / cell), rows = Math.ceil(H / cell);

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const hx = (c + 0.5 + (Math.random() - 0.5) * 0.92) * cell;
          const hy = (r + 0.5 + (Math.random() - 0.5) * 0.92) * cell;
          if (hx < -8 || hx > W + 8 || hy < -8 || hy > H + 8) continue;
          neurons.push({
            hx, hy, x: hx, y: hy, vx: 0, vy: 0,
            s: 0,                                   // activation 0..1
            h: 0,                                   // heat (closeness to cursor) 0..1
            size: 0.6 + Math.random() * 0.8,       // tiny
            tint: Math.random() < 0.14 ? 1 : 0,     // 14% cyan accents
            // unpredictable orbit parameters (incommensurate frequencies)
            a0: Math.random() * TAU,
            r0: 10 + Math.pow(Math.random(), 0.8) * (coarse ? 62 : 108),
            ra: 8 + Math.random() * 28,
            f1: 0.35 + Math.random() * 0.55, f2: 0.21 + Math.random() * 0.42, f3: 0.6 + Math.random() * 0.75,
            p1: Math.random() * TAU, p2: Math.random() * TAU, p3: Math.random() * TAU,
            k: 0.75 + Math.random() * 0.7,          // personal stiffness / reaction speed
            driftA: 2 + Math.random() * 5,          // idle float amplitude at home
            dp: Math.random() * TAU, df: 0.15 + Math.random() * 0.25,
            tw: Math.random() * TAU                 // twinkle phase
          });
        }
      }
    }

    function resize() {
      W = window.innerWidth; H = window.innerHeight;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      // Avoid rebuilding on mobile URL-bar height jitter
      if (!neurons.length || Math.abs(W - builtW) > 1 || Math.abs(H - builtH) > 140) build();
    }
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 120);
    }, { passive: true });
    resize();

    // ── Frame loop ───────────────────────────────────────────────
    let last = performance.now(), t = 0;

    function mixRGB(a, b, m) {
      return [
        (a[0] + (b[0] - a[0]) * m) | 0,
        (a[1] + (b[1] - a[1]) * m) | 0,
        (a[2] + (b[2] - a[2]) * m) | 0
      ];
    }

    function frame(now) {
      requestAnimationFrame(frame);
      const dt = Math.min((now - last) / 1000, 0.04);
      last = now;
      t += dt;

      const idle = (now - lastMove) > IDLE_RELEASE;
      const have = mx > -1000 && !idle;
      boost += ((hot && have ? 1 : 0) - boost) * Math.min(1, dt * 6);

      const R = RECRUIT_R * (1 + 0.4 * boost);
      const LINK = LINK_DIST * (1 + 0.18 * boost);
      const LINK2 = LINK * LINK;

      ctx.clearRect(0, 0, W, H);

      // ── Update ──
      for (let i = 0; i < neurons.length; i++) {
        const n = neurons[i];

        // Neurons NEVER leave their home: the cursor only lights up the ones nearby,
        // nudges them slightly outward and lets them breathe in a tiny orbit.
        // As soon as the cursor moves away, they dim and spring back to their exact place.
        const dxh = n.hx - mx, dyh = n.hy - my;
        const dh = have ? Math.hypot(dxh, dyh) : Infinity;
        const want = have ? clamp(1 - dh / R, 0, 1) : 0;
        const rate = want > n.s ? 7 * n.k : 2.6;          // light up fast, fade a bit slower
        n.s += (want - n.s) * Math.min(1, rate * dt);
        const e = n.s * n.s * (3 - 2 * n.s);

        // resting target: gentle float around home
        let tx = n.hx + Math.sin(t * n.df + n.dp) * n.driftA;
        let ty = n.hy + Math.cos(t * n.df * 1.13 + n.dp * 1.7) * n.driftA;

        if (e > 0.001) {
          // small organic orbit around HOME (not around the cursor)
          const ang = n.a0 + Math.sin(t * n.f1 + n.p1) * 1.9 + Math.sin(t * n.f3 + n.p3) * 1.1;
          const orb = ORBIT * e * (0.6 + 0.4 * Math.sin(t * n.f2 + n.p2));
          tx += Math.cos(ang) * orb;
          ty += Math.sin(ang) * orb;
          // soft outward push: opens a "lens" around the cursor instead of a clump on it
          if (have && dh > 0.001) {
            const push = PUSH * e * (1 - dh / R);
            tx += (dxh / dh) * push;
            ty += (dyh / dh) * push;
          }
        }

        // critically-damped spring back to the target (no overshoot, no wandering)
        const k = 34 * n.k;
        const c = 2 * Math.sqrt(k) * 0.95;
        n.vx += ((tx - n.x) * k - n.vx * c) * dt;
        n.vy += ((ty - n.y) * k - n.vy * c) * dt;
        n.x += n.vx * dt;
        n.y += n.vy * dt;

        n.h = have ? clamp(1 - Math.hypot(n.x - mx, n.y - my) / (R * 0.6), 0, 1) * e : 0;
      }

      // ── Synapses ──
      ctx.lineWidth = 0.7;
      for (let i = 0; i < neurons.length; i++) {
        const a = neurons[i];
        if (a.s < 0.06) continue;
        for (let j = i + 1; j < neurons.length; j++) {
          const b = neurons[j];
          if (b.s < 0.06) continue;
          const dx = a.x - b.x, dy = a.y - b.y;
          const d2 = dx * dx + dy * dy;
          if (d2 > LINK2) continue;
          const d = Math.sqrt(d2);
          const al = (1 - d / LINK) * Math.sqrt(a.s * b.s) * 0.5;
          if (al < 0.01) continue;
          const heat = clamp((a.h + b.h) * 0.5 + boost * 0.25, 0, 1);
          const col = mixRGB(VIOLET, CRIMSON, heat);
          ctx.strokeStyle = `rgba(${col[0]},${col[1]},${col[2]},${al.toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }

      // cursor → nearest woken neurons (the cursor is the "source" synapse)
      if (have) {
        const hubD = LINK * 1.35;
        for (let i = 0; i < neurons.length; i++) {
          const n = neurons[i];
          if (n.s < 0.1) continue;
          const d = Math.hypot(n.x - mx, n.y - my);
          if (d > hubD) continue;
          const al = (1 - d / hubD) * n.s * 0.22;
          ctx.strokeStyle = `rgba(${CRIMSON[0]},${CRIMSON[1]},${CRIMSON[2]},${al.toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(mx, my);
          ctx.lineTo(n.x, n.y);
          ctx.stroke();
        }
      }

      // ── Neurons ──
      for (let i = 0; i < neurons.length; i++) {
        const n = neurons[i];
        const e = n.s * n.s * (3 - 2 * n.s);
        const twinkle = 0.85 + 0.15 * Math.sin(t * 1.6 + n.tw);
        const a = (REST_ALPHA + (0.95 - REST_ALPHA) * e) * twinkle;
        if (a < 0.01) continue;
        const size = n.size * (1 + 0.9 * e);
        const heat = clamp(n.h + boost * 0.3 * e, 0, 1);
        const base = n.tint ? CYAN : VIOLET;
        const col = mixRGB(base, CRIMSON, heat);

        if (e > 0.08) {
          const g = size * 6;
          ctx.globalAlpha = Math.min(1, a * 0.6 * e);
          ctx.drawImage(heat > 0.5 ? SPR_CRIMSON : (n.tint ? SPR_CYAN : SPR_VIOLET), n.x - g, n.y - g, g * 2, g * 2);
          ctx.globalAlpha = 1;
        }
        ctx.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${a.toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(n.x, n.y, size, 0, TAU);
        ctx.fill();
      }
    }
    requestAnimationFrame(frame);
  }

  // ═══════════════════════════════════════════════════════════════
  // CARD SPOTLIGHT — soft glow that follows the cursor inside blocks
  // ═══════════════════════════════════════════════════════════════
  function initCardGlow() {
    if (isTouchDevice()) return;
    const sel = '.feature-card,.pricing-card,.blog-card,.pipeline-step,.faq-item,.stat-card,.contact-method-card,' +
                '.toc,.callout,.authority-box,.geo-visual-card,.metric,.portal-card,.intel-card,.deliverable-card';
    document.querySelectorAll(sel).forEach((el) => {
      if (el.querySelector(':scope > .kx-glow')) return;
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
      const g = document.createElement('span');
      g.className = 'kx-glow';
      g.setAttribute('aria-hidden', 'true');
      el.appendChild(g);
      el.classList.add('kx-spot');
    });

    let raf = 0, ev = null;
    document.addEventListener('pointermove', (e) => {
      ev = e;
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const el = ev.target.closest && ev.target.closest('.kx-spot');
        if (!el) return;
        const r = el.getBoundingClientRect();
        el.style.setProperty('--cx', (ev.clientX - r.left) + 'px');
        el.style.setProperty('--cy', (ev.clientY - r.top) + 'px');
      });
    }, { passive: true });
  }

  // ═══════════════════════════════════════════════════════════════
  // BUTTON RIPPLE
  // ═══════════════════════════════════════════════════════════════
  function initButtonRipple() {
    if (prefersReducedMotion) return;
    document.addEventListener('click', (e) => {
      const b = e.target.closest && e.target.closest('.btn-primary,.btn-secondary,.form-submit');
      if (!b) return;
      const r = b.getBoundingClientRect();
      const size = Math.max(r.width, r.height) * 1.6;
      if (getComputedStyle(b).position === 'static') b.style.position = 'relative';
      const s = document.createElement('span');
      s.className = 'kx-ripple';
      s.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - r.left - size / 2}px;top:${e.clientY - r.top - size / 2}px`;
      b.appendChild(s);
      setTimeout(() => s.remove(), 700);
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // HERO BLOBS — drift opposite to the mouse (depth)
  // ═══════════════════════════════════════════════════════════════
  function initBlobMouseParallax() {
    if (prefersReducedMotion || isTouchDevice()) return;
    const blobs = document.querySelectorAll('.hero-blob');
    if (!blobs.length) return;
    let raf = 0, ex = 0, ey = 0;
    window.addEventListener('pointermove', (e) => {
      ex = e.clientX; ey = e.clientY;
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const px = (ex / window.innerWidth - 0.5) * 2;
        const py = (ey / window.innerHeight - 0.5) * 2;
        blobs.forEach((b) => {
          b.style.setProperty('--px', px.toFixed(3));
          b.style.setProperty('--py', py.toFixed(3));
        });
      });
    }, { passive: true });
  }

  // ═══════════════════════════════════════════════════════════════
  // PRESERVED CORE INTERACTIONS
  // ═══════════════════════════════════════════════════════════════
  function initProgressBar() {
    const bar = document.createElement('div');
    bar.className = 'progress-bar';
    document.body.prepend(bar);

    const update = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      bar.style.width = pct + '%';
    };

    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update, { passive: true });
  }

  function initNavbarScroll() {
    const nav = document.querySelector('.navbar');
    if (!nav) return;
    const update = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  function initActiveNav() {
    const path = window.location.pathname.replace(/index\.html$/, '');
    document.querySelectorAll('.nav-links a').forEach((a) => {
      const href = (a.getAttribute('href') || '').replace(/index\.html$/, '');
      if (href === path || (href !== '/' && href !== '/en/' && path.indexOf(href.replace(/\.html$/, '')) === 0 && href.length > 4)) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
      }
    });
  }


  function initScrollReveal() {
    const els = document.querySelectorAll('.reveal, .reveal-left, .reveal-scale');
    if (!els.length) return;
    if (prefersReducedMotion) {
      els.forEach((el) => el.classList.add('visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add('visible'), index * 40);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -40px 0px' });
    // threshold 0 = reveal as soon as ANY part enters the screen. A % threshold never
    // fires on very tall blocks (e.g. a 20 000px article body), leaving them invisible.

    els.forEach((el) => io.observe(el));
    // Safety net: anything already scrolled past or on screen gets revealed.
    const sweep = () => els.forEach((el) => {
      if (!el.classList.contains('visible') && el.getBoundingClientRect().top < window.innerHeight) el.classList.add('visible');
    });
    window.addEventListener('load', () => setTimeout(sweep, 1200));
    window.addEventListener('scroll', () => { clearTimeout(sweep.t); sweep.t = setTimeout(sweep, 250); }, { passive: true });
  }

  function initMagneticElements() {
    if (prefersReducedMotion || isTouchDevice()) return;
    document.querySelectorAll('.btn-primary, .btn-secondary, .magnetic').forEach((el) => {
      el.addEventListener('mousemove', (e) => {
        const r = el.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        const dx = (e.clientX - cx) * 0.18;
        const dy = (e.clientY - cy) * 0.18;
        el.style.transform = `translate(${dx}px, ${dy}px)`;
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = '';
      });
    });
  }

  function initTiltCards() {
    if (prefersReducedMotion || isTouchDevice()) return;
    const TILT = 6;
    document.querySelectorAll('.pricing-card, .feature-card, .blog-card, .faq-item, .pipeline-step').forEach((card) => {
      card.addEventListener('mouseenter', () => card.classList.add('is-tilting'));
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        const rx = ((e.clientY - cy) / (r.height / 2)) * -TILT;
        const ry = ((e.clientX - cx) / (r.width / 2)) * TILT;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-4px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.classList.remove('is-tilting');
        card.style.transform = '';
      });
    });
  }

  function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (!counters.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.45 });
    counters.forEach((c) => io.observe(c));
  }

  function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const decimal = el.dataset.decimal ? parseInt(el.dataset.decimal, 10) : 0;
    const duration = 1400;
    const start = performance.now();

    function step(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 4);
      const val = target * ease;
      el.textContent = prefix + val.toFixed(decimal) + suffix;
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function initParallax() {
    if (prefersReducedMotion) return;
    const blobs = document.querySelectorAll('.hero-blob');
    if (!blobs.length) return;
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      blobs.forEach((blob, i) => {
        const speed = i % 2 === 0 ? 0.10 : 0.16;
        blob.style.transform = `translateY(${y * speed}px)`;
      });
    }, { passive: true });
  }

  function initTextScramble() {
    if (prefersReducedMotion) return;
    const chars = '!<>-_\\/[]{}—=+*^?#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    document.querySelectorAll('[data-scramble]').forEach((el) => {
      const original = el.textContent;
      let frame = 0;
      let raf;

      el.addEventListener('mouseenter', () => {
        cancelAnimationFrame(raf);
        frame = 0;
        function update() {
          el.textContent = original.split('').map((c, i) => {
            if (c === ' ') return ' ';
            if (i < frame) return original[i];
            return chars[Math.floor(Math.random() * chars.length)];
          }).join('');
          frame += 1.5;
          if (frame < original.length + 4) raf = requestAnimationFrame(update);
          else el.textContent = original;
        }
        update();
      });
    });
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener('click', (e) => {
        const href = a.getAttribute('href');
        if (!href || href === '#') return;
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  function initLanguageSwitcher() {
    const langBtn = document.getElementById('langBtn');
    const langMenu = document.getElementById('langMenu');
    if (!langBtn || !langMenu) return;
    const close = () => {
      langMenu.classList.remove('active');
      langBtn.setAttribute('aria-expanded', 'false');
      langMenu.setAttribute('aria-hidden', 'true');
    };
    langBtn.addEventListener('click', () => {
      const isOpen = langMenu.classList.toggle('active');
      langBtn.setAttribute('aria-expanded', String(isOpen));
      langMenu.setAttribute('aria-hidden', String(!isOpen));
    });
    // Options are real <a hreflang> links to the translated page (crawlable). Remember the choice.
    langMenu.querySelectorAll('a[data-lang]').forEach((a) => {
      a.addEventListener('click', () => {
        try { localStorage.setItem('kortex_lang', a.dataset.lang); } catch (e) {}
      });
    });
    document.addEventListener('click', (e) => { if (!e.target.closest('.lang-switcher')) close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  }

})();
