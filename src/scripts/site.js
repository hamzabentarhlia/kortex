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
  if (typeof window.plausible === 'function') window.plausible(name, { props });
  if (typeof window.gtag === 'function') window.gtag('event', name, props || {});
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
  const items = document.querySelectorAll('.reveal,.draw,[data-count],[data-fill]');
  if (!('IntersectionObserver' in window) || reduceMotion) {
    items.forEach((el) => {
      el.classList.add('is-in');
      if (el.dataset.count) el.textContent = el.dataset.count;
    });
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      el.classList.add('is-in');
      if (el.dataset.count) animateCount(el);
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  items.forEach((el) => io.observe(el));
}

function initPrompt() {
  document.querySelectorAll('[data-prompt]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const input = form.querySelector('input');
      const value = input.value.trim();
      if (!value) { e.preventDefault(); input.focus(); return; }
      if (!/^https?:\/\//i.test(value)) input.value = 'https://' + value;
      track('Prompt submit');
    });
  });
}

function initPrefill() {
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

initTheme();
initHeader();
initMenus();
initMobileMenu();
initReveal();
initPrompt();
initPrefill();
initForms();
initTracking();
