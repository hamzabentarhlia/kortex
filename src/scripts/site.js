const root = document.documentElement;
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function store(key, value) {
  try {
    if (value === undefined) return localStorage.getItem(key);
    localStorage.setItem(key, value);
  } catch (e) {
    return null;
  }
  return value;
}

function track(name, props) {
  if (window.kxGA && typeof window.gtag === 'function') window.gtag('event', name, props || {});
}

function currentTheme() {
  const set = root.dataset.theme;
  if (set) return set;
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

function initTheme() {
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
    const sync = () => btn.setAttribute('aria-pressed', String(currentTheme() === 'light'));
    sync();
    btn.addEventListener('click', () => {
      const next = currentTheme() === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      store('kx-theme', next);
      document.querySelectorAll('[data-theme-toggle]').forEach((b) => b.setAttribute('aria-pressed', String(next === 'light')));
      if (window.Cal && window.Cal.ns && window.Cal.ns.kx) window.Cal.ns.kx('ui', { theme: next });
    });
  });
}

function initHeader() {
  const header = document.querySelector('[data-header]');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

function initMenus() {
  const toggles = [...document.querySelectorAll('[data-menu-toggle]')];
  const closeAll = (except) => {
    toggles.forEach((t) => {
      if (t === except) return;
      t.setAttribute('aria-expanded', 'false');
      document.getElementById(t.getAttribute('aria-controls')).hidden = true;
    });
  };
  toggles.forEach((toggle) => {
    const menu = document.getElementById(toggle.getAttribute('aria-controls'));
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      closeAll(toggle);
      toggle.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
    });
    menu.addEventListener('keydown', (e) => {
      const items = [...menu.querySelectorAll('a')];
      const i = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); items[(i + 1) % items.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
    });
    toggle.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        closeAll(toggle);
        toggle.setAttribute('aria-expanded', 'true');
        menu.hidden = false;
        const first = menu.querySelector('a');
        if (first) first.focus();
      }
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-menu')) closeAll();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const open = toggles.find((t) => t.getAttribute('aria-expanded') === 'true');
    if (open) { closeAll(); open.focus(); }
  });
  document.addEventListener('focusin', (e) => {
    toggles.forEach((t) => {
      const li = t.parentElement;
      if (t.getAttribute('aria-expanded') === 'true' && !li.contains(e.target)) {
        t.setAttribute('aria-expanded', 'false');
        document.getElementById(t.getAttribute('aria-controls')).hidden = true;
      }
    });
  });
}

function initMobileMenu() {
  const openBtn = document.querySelector('[data-mobile-open]');
  const panel = document.getElementById('mobile-menu');
  if (!openBtn || !panel) return;
  const closeBtn = panel.querySelector('[data-mobile-close]');
  const focusables = () => [...panel.querySelectorAll('a,button')];
  const close = () => {
    panel.hidden = true;
    openBtn.setAttribute('aria-expanded', 'false');
    root.classList.remove('menu-open');
    openBtn.focus();
  };
  openBtn.addEventListener('click', () => {
    panel.hidden = false;
    openBtn.setAttribute('aria-expanded', 'true');
    root.classList.add('menu-open');
    closeBtn.focus();
  });
  closeBtn.addEventListener('click', close);
  panel.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
    if (e.key !== 'Tab') return;
    const f = focusables();
    if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  });
}

function animateCount(el) {
  const target = Number(el.dataset.count);
  if (reduceMotion) { el.textContent = target; return; }
  const start = performance.now();
  const step = (now) => {
    const t = Math.min(1, (now - start) / 1400);
    el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function initReveal() {
  if (!reduceMotion) {
    const vh = innerHeight;
    const late = [...document.querySelectorAll('main .section-head, main .faq, main .compare, main .tbl-wrap, main .answer-block, main .prose > h2, main .vs, main .split > .glass')]
      .filter((el) => !el.closest('.reveal,.reveal-group') && el.getBoundingClientRect().top > vh);
    late.forEach((el) => el.classList.add('reveal'));
  }
  document.querySelectorAll('.draw svg').forEach((svg) => {
    svg.querySelectorAll('rect,text').forEach((el, i) => el.style.setProperty('--i', Math.min(i, 30)));
  });
  document.querySelectorAll('.reveal-group').forEach((g) => {
    [...g.children].forEach((el, i) => el.style.setProperty('--i', Math.min(i, 8)));
  });
  const items = document.querySelectorAll('.reveal,.reveal-group,.draw,.divider,.path-wrap,[data-count],[data-fill],[data-typer]');
  if (!('IntersectionObserver' in window) || reduceMotion) {
    items.forEach((el) => {
      el.classList.add('is-in');
      if (el.dataset.count) el.textContent = el.dataset.count;
      if (el.matches('[data-typer]')) runTyper(el, true);
    });
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      el.classList.add('is-in');
      if (el.dataset.count) animateCount(el);
      if (el.matches('[data-typer]')) runTyper(el);
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  items.forEach((el) => io.observe(el));
}

function initPrefill() {
  const nf = document.querySelector('[data-nf-path]');
  if (nf) nf.textContent = 'kortexlab.me' + location.pathname;
  const params = new URLSearchParams(location.search);
  const source = params.get('source');
  const field = document.querySelector('[data-prefill=source]');
  if (source && field) field.value = source.slice(0, 500);
  const plan = params.get('plan');
  const planField = document.querySelector('[data-prefill=plan]');
  if (plan && planField) planField.value = plan.slice(0, 40);
  if (params.get('sent') === '1') {
    const status = document.querySelector('[data-form-status]');
    if (status) { status.hidden = false; status.focus(); }
    track('Form submitted', { page: location.pathname });
  }
}

function initForms() {
  document.querySelectorAll('form[data-track-form]').forEach((form) => {
    form.addEventListener('submit', () => track('Form submit', { form: form.dataset.trackForm }));
  });
}

function initTracking() {
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-track]');
    if (el) track('CTA click', { cta: el.dataset.track, page: location.pathname });
  });
}

function runTyper(card, instant) {
  const out = card.querySelector('[data-typed]');
  const text = out.dataset.typed;
  const lines = [...card.querySelectorAll('.demo-a p')];
  const hit = card.querySelector('.demo-src .hit');
  const finish = () => {
    lines.forEach((p, i) => setTimeout(() => p.classList.add('on'), instant ? 0 : 350 + i * 450));
    setTimeout(() => hit && hit.classList.add('on'), instant ? 0 : 350 + lines.length * 450 + 200);
  };
  if (instant) { out.textContent = text; finish(); return; }
  let i = 0;
  const tick = () => {
    out.textContent = text.slice(0, ++i);
    if (i < text.length) setTimeout(tick, 34);
    else finish();
  };
  tick();
}

function initConsent() {
  const box = document.querySelector('[data-consent]');
  if (!box) return;
  const html = document.documentElement;
  const show = (focus) => {
    box.hidden = false;
    html.classList.add('consent-open');
    html.style.setProperty('--consent-h', box.offsetHeight + 'px');
    if (focus) box.querySelector('button').focus();
  };
  const hide = () => {
    box.hidden = true;
    html.classList.remove('consent-open');
  };
  const clearGA = () => {
    document.cookie.split(';').map((c) => c.split('=')[0].trim()).filter((n) => n.startsWith('_ga')).forEach((n) => {
      [location.hostname, '.' + location.hostname.replace(/^www\./, '')].forEach((d) => {
        document.cookie = n + '=; Max-Age=0; path=/; domain=' + d;
      });
      document.cookie = n + '=; Max-Age=0; path=/';
    });
  };
  box.querySelectorAll('[data-consent-choice]').forEach((b) => b.addEventListener('click', () => {
    const v = b.dataset.consentChoice;
    try { localStorage.setItem('kx-consent', JSON.stringify({ v, t: Date.now() })); } catch (e) { }
    window.kxConsent = v;
    if (v === 'granted') window.kxLoadGA();
    else {
      if (typeof window.gtag === 'function') window.gtag('consent', 'update', { analytics_storage: 'denied' });
      clearGA();
    }
    hide();
  }));
  document.querySelectorAll('[data-consent-open]').forEach((b) => b.addEventListener('click', () => show(true)));
  if (!window.kxConsent) show(false);
}

function initBookBar() {
  const bar = document.querySelector('[data-bookbar]');
  const hero = document.querySelector('main > section');
  const ends = [...document.querySelectorAll('.site-footer, .cta-band')];
  if (!bar || !hero || !('IntersectionObserver' in window)) return;
  let pastHero = false;
  const seen = new Set();
  const set = () => bar.classList.toggle('is-on', pastHero && !seen.size);
  new IntersectionObserver((es) => { pastHero = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; set(); }).observe(hero);
  const io = new IntersectionObserver((es) => { es.forEach((e) => (e.isIntersecting ? seen.add(e.target) : seen.delete(e.target))); set(); });
  ends.forEach((el) => io.observe(el));
}

function initVisuals() {
  const vx = [...document.querySelectorAll('.vx')];
  if (!('IntersectionObserver' in window) || reduceMotion) {
    vx.forEach((v) => v.classList.add('is-in', 'is-on'));
    return;
  }
  const typeIn = (el, delay) => {
    const text = el.textContent;
    el.style.minHeight = el.offsetHeight + 'px';
    el.textContent = '';
    el.classList.add('is-typing');
    let i = 0;
    const tick = () => {
      el.textContent = text.slice(0, ++i);
      if (i < text.length) setTimeout(tick, 26);
      else el.classList.remove('is-typing');
    };
    setTimeout(tick, delay);
  };
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    const v = e.target;
    v.classList.toggle('is-on', e.isIntersecting);
    if (e.isIntersecting && !v.classList.contains('is-in')) {
      v.classList.add('is-in');
      v.querySelectorAll('[data-type]').forEach((el) => typeIn(el, parseInt(el.dataset.type, 10) || 300));
    }
  }), { rootMargin: '0px 0px -10% 0px', threshold: 0 });
  vx.forEach((v) => io.observe(v));
}

function initScroll() {
  const scrub = [...document.querySelectorAll('[data-scrub]')];
  const para = window.matchMedia('(pointer: fine)').matches ? [...document.querySelectorAll('[data-parallax]')] : [];
  if (reduceMotion || (!scrub.length && !para.length) || !('IntersectionObserver' in window)) {
    scrub.forEach((el) => el.style.setProperty('--p', '1'));
    return;
  }
  const live = new Set();
  const io = new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? live.add(e.target) : live.delete(e.target))));
  scrub.concat(para).forEach((el) => io.observe(el));
  let raf = 0;
  const tick = () => {
    raf = 0;
    const vh = innerHeight;
    live.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (el.dataset.scrub !== undefined) {
        const pin = el.dataset.scrub === 'pin';
        const p = pin ? -r.top / Math.max(1, r.height - vh) : (vh - r.top) / (vh + r.height);
        el.style.setProperty('--p', Math.min(1, Math.max(0, p)).toFixed(3));
      }
      if (el.dataset.parallax !== undefined) {
        const k = parseFloat(el.dataset.parallax) || 0.08;
        el.style.transform = `translate3d(0,${((r.top + r.height / 2 - vh / 2) * -k).toFixed(1)}px,0)`;
      }
    });
  };
  const req = () => { if (!raf) raf = requestAnimationFrame(tick); };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);
  req();
}

function initAnimVisibility() {
  const els = document.querySelectorAll('[data-anim]');
  if (!('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-visible')); return; }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => e.target.classList.toggle('is-visible', e.isIntersecting));
  });
  els.forEach((e) => io.observe(e));
}

function initStory() {
  const vis = document.querySelector('[data-story]');
  const steps = document.querySelectorAll('[data-step]');
  if (!vis || !steps.length || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      vis.dataset.active = e.target.dataset.step;
      steps.forEach((s) => s.classList.toggle('is-active', s === e.target));
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach((s) => io.observe(s));
}

function initCalc() {
  const form = document.querySelector('[data-calc]');
  if (!form) return;
  const lang = document.documentElement.lang;
  const fmt = new Intl.NumberFormat(lang === 'ar' ? 'ar-MA' : lang === 'fr' ? 'fr-FR' : 'en-IE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  const num = (el) => { const n = parseFloat(el.value); return isFinite(n) && n > 0 ? n : 0; };
  const roles = [...form.querySelectorAll('[data-role]')];
  const plan = form.querySelector('[data-plan]');
  const inBar = document.querySelector('[data-bar=in]');
  const kxBar = document.querySelector('[data-bar=kx]');
  const out = document.querySelector('[data-calc-out]');
  const tpl = out.dataset.tpl;
  const run = () => {
    const inh = roles.reduce((a, r) => a + num(r), 0);
    const kx = num(plan);
    const max = Math.max(inh, kx, 1);
    inBar.querySelector('i').style.setProperty('--v', (inh / max).toFixed(3));
    kxBar.querySelector('i').style.setProperty('--v', (kx / max).toFixed(3));
    inBar.querySelector('[data-val]').textContent = fmt.format(inh);
    kxBar.querySelector('[data-val]').textContent = fmt.format(kx);
    out.firstChild.textContent = tpl.replace('{d}', fmt.format(inh - kx));
  };
  form.addEventListener('input', run);
  form.addEventListener('change', () => track('Calculator', { plan: plan.value }));
  run();
}

const calLang = () => ({ en: 'en', fr: 'fr', ar: 'ar' })[document.documentElement.lang] || 'en';
const calConfig = () => ({ theme: currentTheme(), layout: 'month_view', lng: calLang() });

function loadCal() {
  if (window.__calP) return window.__calP;
  window.__calP = new Promise((resolve, reject) => {
    (function (C, A, L) {
      const p = (a, ar) => a.q.push(ar);
      const d = C.document;
      C.Cal = C.Cal || function () {
        const cal = C.Cal; const ar = arguments;
        if (!cal.loaded) {
          cal.ns = {}; cal.q = cal.q || [];
          const sc = d.createElement('script'); sc.src = A; sc.async = true;
          sc.onload = () => resolve(C.Cal); sc.onerror = reject;
          d.head.appendChild(sc); cal.loaded = true;
        }
        if (ar[0] === L) {
          const api = function () { p(api, arguments); };
          const ns = ar[1]; api.q = api.q || [];
          if (typeof ns === 'string') { cal.ns[ns] = cal.ns[ns] || api; p(cal.ns[ns], ar); p(cal, ['initNamespace', ns]); } else p(cal, ar);
          return;
        }
        p(cal, ar);
      };
    })(window, 'https://app.cal.com/embed/embed.js', 'init');
    window.Cal('init', 'kx', { origin: 'https://cal.com' });
    window.Cal.ns.kx('ui', {
      theme: currentTheme(),
      cssVarsPerTheme: { light: { 'cal-brand': '#ec5a1c' }, dark: { 'cal-brand': '#ff6b2c' } },
      hideEventTypeDetails: false,
      layout: 'month_view',
    });
    setTimeout(() => reject(new Error('timeout')), 8000);
  });
  return window.__calP;
}

function initCal() {
  const desktop = window.matchMedia('(min-width: 900px) and (pointer: fine)');
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[data-cal]');
    if (!a || !desktop.matches || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    track('Booking click', { cta: a.dataset.track || 'book', page: location.pathname });
    loadCal().then(() => {
      window.Cal.ns.kx('modal', { calLink: a.dataset.cal, config: calConfig() });
    }).catch(() => { location.href = a.href; });
  });
  const inline = document.getElementById('cal-inline');
  if (!inline) return;
  const start = () => {
    if (inline.dataset.loaded) return;
    inline.dataset.loaded = '1';
    loadCal().then(() => {
      inline.innerHTML = '';
      window.Cal.ns.kx('inline', { elementOrSelector: '#cal-inline', calLink: inline.dataset.calLink, config: calConfig() });
    }).catch(() => { inline.dataset.failed = '1'; });
  };
  const btn = document.querySelector('[data-cal-load]');
  if (btn) btn.addEventListener('click', start);
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((en) => { if (en.some((x) => x.isIntersecting)) { start(); io.disconnect(); } }, { rootMargin: '300px' });
    io.observe(inline);
  }
}

function initPointerFx() {
  if (reduceMotion || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const glow = document.createElement('div');
  glow.className = 'cursor-glow';
  glow.setAttribute('aria-hidden', 'true');
  document.body.appendChild(glow);
  let tx = innerWidth / 2, ty = innerHeight / 3, x = tx, y = ty, raf = 0;
  const loop = () => {
    x += (tx - x) * 0.12; y += (ty - y) * 0.12;
    glow.style.transform = `translate3d(${x}px,${y}px,0)`;
    raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.5 ? requestAnimationFrame(loop) : 0;
  };
  window.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });
  document.querySelectorAll('.glass.card,.tier,.audience,.glass.step,.list-card').forEach((c) => {
    c.classList.add('tilt');
    c.addEventListener('pointermove', (e) => {
      const r = c.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      c.style.setProperty('--mx', `${px * 100}%`); c.style.setProperty('--my', `${py * 100}%`);
      c.style.transform = `perspective(900px) rotateX(${(0.5 - py) * 3}deg) rotateY(${(px - 0.5) * 3}deg)`;
    });
    c.addEventListener('pointerleave', () => { c.style.transform = ''; });
  });
  document.querySelectorAll('.btn-primary').forEach((b) => {
    b.addEventListener('pointermove', (e) => {
      const r = b.getBoundingClientRect();
      b.style.transform = `translate(${((e.clientX - r.left) / r.width - 0.5) * 8}px,${((e.clientY - r.top) / r.height - 0.5) * 6}px)`;
    });
    b.addEventListener('pointerleave', () => { b.style.transform = ''; });
  });
  const links = document.querySelector('.nav-links');
  if (links) {
    const ind = document.createElement('span');
    ind.className = 'nav-ind';
    ind.setAttribute('aria-hidden', 'true');
    links.appendChild(ind);
    const moveTo = (el) => {
      if (!el) { ind.style.opacity = '0'; return; }
      const lr = links.getBoundingClientRect(), r = el.getBoundingClientRect();
      ind.style.opacity = '1';
      ind.style.transform = `translateX(${r.left - lr.left}px) scaleX(${r.width / 100})`;
    };
    const current = () => links.querySelector('[aria-current=page]');
    links.querySelectorAll('.nav-link').forEach((l) => l.addEventListener('pointerenter', () => moveTo(l)));
    links.addEventListener('pointerleave', () => moveTo(current()));
    requestAnimationFrame(() => moveTo(current()));
  }
}

function initPipeline() {
  document.querySelectorAll('[data-hp]').forEach((hp) => {
    const tabs = [...hp.querySelectorAll('[role=tab]')];
    const panel = hp.querySelector('[role=tabpanel]');
    let auto = !reduceMotion;
    let visible = false;
    let timer = 0;
    const schedule = () => {
      clearTimeout(timer);
      if (auto && visible) timer = setTimeout(() => {
        const i = tabs.findIndex((t) => t.getAttribute('aria-selected') === 'true');
        select(tabs[(i + 1) % tabs.length]);
      }, 7000);
    };
    const select = (tab, focus, user) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
      });
      hp.dataset.active = tab.dataset.src;
      panel.setAttribute('aria-labelledby', tab.id);
      hp.classList.remove('run');
      void hp.offsetWidth;
      hp.classList.add('run');
      if (focus) tab.focus();
      if (user) {
        auto = false;
        clearTimeout(timer);
        track('Source picker', { source: tab.dataset.src });
      } else schedule();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(t, false, true));
      t.addEventListener('keydown', (e) => {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        e.preventDefault();
        const dir = document.documentElement.dir === 'rtl' ? -1 : 1;
        const step = (e.key === 'ArrowRight' ? 1 : -1) * dir;
        select(tabs[(i + step + tabs.length) % tabs.length], true, true);
      });
    });
    hp.addEventListener('pointerenter', () => clearTimeout(timer));
    hp.addEventListener('pointerleave', schedule);
    hp.addEventListener('focusin', () => clearTimeout(timer));
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((es) => {
        visible = es[0].isIntersecting;
        if (visible) schedule(); else clearTimeout(timer);
      }, { threshold: 0.3 }).observe(hp);
    }
  });
}

function initFinder() {
  const f = document.querySelector('[data-finder]');
  if (!f) return;
  const tiers = document.querySelectorAll('[data-plan]');
  const out = f.querySelector('[data-finder-out]');
  const run = (first) => {
    const src = (f.querySelector('input[name=fsrc]:checked') || {}).value;
    const comp = (f.querySelector('input[name=fcomp]:checked') || {}).value;
    const plan = src === 'many' || comp === 'own' ? 'titan' : comp === 'some' ? 'swarm' : 'ghost';
    tiers.forEach((t) => t.classList.toggle('is-match', t.dataset.plan === plan));
    out.querySelectorAll('[data-why]').forEach((w) => { w.hidden = w.dataset.why !== plan; });
    if (first === true) return;
    document.querySelectorAll('.tiers').forEach((g) => g.classList.add('has-match'));
    track('Plan finder', { plan });
  };
  f.addEventListener('change', () => run());
  run(true);
}

initTheme();
initConsent();
initHeader();
initMenus();
initMobileMenu();
initReveal();
initPrefill();
initForms();
initAnimVisibility();
initVisuals();
initBookBar();
initScroll();
initPipeline();
initFinder();
const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 1));
[initStory, initCalc, initCal, initTracking, initPointerFx].forEach((fn) => idle(() => fn()));
