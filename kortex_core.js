
// ═══════════════════════════════════════════════════
// KORTEX — CORE INTERACTION ENGINE v3.0
// Cleaned: reduced duplication, safer interactions,
// accessible motion toggles, active nav, language switcher
// ═══════════════════════════════════════════════════
(function () {
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

    if (!isTouchDevice() && !prefersReducedMotion) {
      initCursor();
      initCanvasParticles();
    }

    initSmoothAnchors();
  });

  function isTouchDevice() {
    return window.matchMedia('(pointer: coarse)').matches || 'ontouchstart' in window;
  }

  function initPageLoad() {
    document.body.classList.add('is-ready');
  }

  function initCursor() {
    document.body.classList.add('has-custom-cursor');
    const dot = document.createElement('div');
    const ring = document.createElement('div');
    dot.className = 'cursor-dot';
    ring.className = 'cursor-ring';
    document.body.append(dot, ring);

    let mx = -999, my = -999;
    let rx = -999, ry = -999;

    document.addEventListener('mousemove', (e) => {
      mx = e.clientX;
      my = e.clientY;
      dot.style.left = mx + 'px';
      dot.style.top = my + 'px';
    }, { passive: true });

    function animateRing() {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      ring.style.left = rx + 'px';
      ring.style.top = ry + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    const hoverTargets = 'a, button, .pricing-card, .feature-card, .blog-card, .pipeline-step, .faq-item, .stat-card, .form-input, select, textarea';
    document.querySelectorAll(hoverTargets).forEach((el) => {
      el.addEventListener('mouseenter', () => {
        dot.classList.add('hovered');
        ring.classList.add('hovered');
      });
      el.addEventListener('mouseleave', () => {
        dot.classList.remove('hovered');
        ring.classList.remove('hovered');
      });
    });

    document.addEventListener('mousedown', () => dot.classList.add('clicking'));
    document.addEventListener('mouseup', () => dot.classList.remove('clicking'));

    document.addEventListener('mouseleave', () => {
      dot.style.opacity = '0';
      ring.style.opacity = '0';
    });
    document.addEventListener('mouseenter', () => {
      dot.style.opacity = '1';
      ring.style.opacity = '1';
    });
  }

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

  function initCanvasParticles() {

  if (prefersReducedMotion) return;

  const canvas =
    document.getElementById('webgl-canvas');

  if (!canvas) return;

  const ctx =
    canvas.getContext('2d');

  if (!ctx) return;

  let width;
  let height;

  const mouse = {
    x: -9999,
    y: -9999
  };

  const nodes = [];

  const spacing = 42;
  const influenceRadius = 180;

  function resize() {

    width =
      canvas.width =
      window.innerWidth *
      window.devicePixelRatio;

    height =
      canvas.height =
      window.innerHeight *
      window.devicePixelRatio;

    canvas.style.width =
      window.innerWidth + 'px';

    canvas.style.height =
      window.innerHeight + 'px';

    ctx.setTransform(
      window.devicePixelRatio,
      0,
      0,
      window.devicePixelRatio,
      0,
      0
    );

    buildGrid();
  }

  function buildGrid() {

    nodes.length = 0;

    const cols =
      Math.ceil(
        window.innerWidth / spacing
      );

    const rows =
      Math.ceil(
        window.innerHeight / spacing
      );

    for (let y = 0; y < rows; y++) {

      for (let x = 0; x < cols; x++) {

        nodes.push({

          baseX:
            x * spacing,

          baseY:
            y * spacing,

          x:
            x * spacing,

          y:
            y * spacing
        });
      }
    }
  }

  function render() {

    ctx.clearRect(
      0,
      0,
      window.innerWidth,
      window.innerHeight
    );

    nodes.forEach(node => {

      const dx =
        mouse.x -
        node.baseX;

      const dy =
        mouse.y -
        node.baseY;

      const distance =
        Math.hypot(dx, dy);

      let intensity =
        Math.max(
          0,
          1 -
          (
            distance /
            influenceRadius
          )
        );

      let targetX =
        node.baseX;

      let targetY =
        node.baseY;

      if (intensity > 0) {

        targetX -=
          dx *
          intensity *
          0.20;

        targetY -=
          dy *
          intensity *
          0.20;
      }

      node.x +=
        (
          targetX -
          node.x
        ) *
        0.12;

      node.y +=
        (
          targetY -
          node.y
        ) *
        0.12;

      const size =
        1.4 +
        intensity * 2.8;

      const alpha =
        0.12 +
        intensity * 0.88;

      ctx.beginPath();

      ctx.arc(
        node.x,
        node.y,
        size,
        0,
        Math.PI * 2
      );

      ctx.fillStyle =
        `rgba(139,92,246,${alpha})`;

      ctx.fill();
    });

    requestAnimationFrame(
      render
    );
  }

  document.addEventListener(
    'mousemove',
    e => {

      mouse.x =
        e.clientX;

      mouse.y =
        e.clientY;

      document.documentElement
        .style
        .setProperty(
          '--mx',
          `${e.clientX}px`
        );

      document.documentElement
        .style
        .setProperty(
          '--my',
          `${e.clientY}px`
        );

    },
    {
      passive: true
    }
  );

  window.addEventListener(
    'mouseleave',
    () => {

      mouse.x = -9999;
      mouse.y = -9999;

    }
  );

  window.addEventListener(
    'resize',
    resize,
    {
      passive: true
    }
  );

  resize();
  render();
}

  function initNavbarScroll() {
    const nav = document.querySelector('.navbar');
    if (!nav) return;
    const update = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  function initActiveNav() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach((a) => {
      const href = a.getAttribute('href');
      if (href === page) a.classList.add('active');
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
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    els.forEach((el) => io.observe(el));
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
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        const rx = ((e.clientY - cy) / (r.height / 2)) * -TILT;
        const ry = ((e.clientX - cx) / (r.width / 2)) * TILT;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-4px)`;
      });
      card.addEventListener('mouseleave', () => {
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
        const target = document.querySelector(a.getAttribute('href'));
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
    const currentLangSpan = document.getElementById('currentLang');
    const langOptions = document.querySelectorAll('.lang-option');
    if (!langBtn || !langMenu || !currentLangSpan || !langOptions.length) return;

    const savedLang = localStorage.getItem('kortex_lang') || document.documentElement.lang || 'fr';
    setLanguage(savedLang, false);

    langBtn.addEventListener('click', () => {
      const isOpen = langMenu.classList.toggle('active');
      langBtn.setAttribute('aria-expanded', String(isOpen));
      langMenu.setAttribute('aria-hidden', String(!isOpen));
    });

    langOptions.forEach((option) => {
      option.addEventListener('click', () => {
        const lang = option.dataset.lang || 'fr';
        setLanguage(lang, true);
        langMenu.classList.remove('active');
        langBtn.setAttribute('aria-expanded', 'false');
        langMenu.setAttribute('aria-hidden', 'true');
      });
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.lang-switcher')) {
        langMenu.classList.remove('active');
        langBtn.setAttribute('aria-expanded', 'false');
        langMenu.setAttribute('aria-hidden', 'true');
      }
    });

    function setLanguage(lang, persist) {
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      currentLangSpan.textContent = lang.toUpperCase();
      langOptions.forEach((option) => option.classList.toggle('active', option.dataset.lang === lang));
      if (persist) localStorage.setItem('kortex_lang', lang);
    }
  }
})();
