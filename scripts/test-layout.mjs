import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const results = [];
const check = (name, ok, detail = '') => { results.push(ok); console.log(`${ok ? 'pass' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`); };
const IGNORE = /ERR_TUNNEL|cal\.com|googletagmanager|pageclip/i;
const browser = await chromium.launch();
const templates = ['/', '/how-it-works/', '/pricing/', '/audit/', '/about/', '/proof/', '/checklist/', '/contact/', '/blog/', '/blog/entity-seo-for-founders/', '/glossary/', '/glossary/entity/', '/compare/', '/compare/kortex-vs-freelance-writer/', '/solutions/', '/solutions/b2b/', '/solutions/from-a-blog/', '/resources/', '/teardowns/', '/teardowns/our-pricing-page/', '/case-studies/', '/security/', '/fr/', '/fr/pricing/', '/fr/solutions/'];
const widths = [375, 768, 1024, 1440, 1920];

async function open(path, w, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce', ...opts });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base + path, { waitUntil: 'load' });
  await page.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ v: 'denied', t: Date.now() })); } catch (e) { } });
  await page.reload({ waitUntil: 'load' });
  await page.waitForTimeout(350);
  return { ctx, page, errors };
}

let overflow = 0, narrow = [], midword = [];
for (const path of templates) {
  for (const w of widths) {
    const { ctx, page } = await open(path, w);
    const r = await page.evaluate(() => {
      const out = { sw: document.documentElement.scrollWidth, iw: window.innerWidth, narrow: [], mid: [] };
      document.querySelectorAll('main .grid > .card, main .grid > .glass, main .audiences > .audience, main .tiers > .tier').forEach((c) => {
        const w = c.getBoundingClientRect().width;
        if (w > 0 && w < 279) out.narrow.push(Math.round(w) + ' ' + (c.className || '').slice(0, 30));
      });
      document.querySelectorAll('main h1, main h2, main h3').forEach((h) => {
        if (h.classList.contains('visually-hidden') || h.closest('.visually-hidden')) return;
        if (h.scrollWidth > h.clientWidth + 2) out.mid.push((h.textContent || '').trim().slice(0, 30));
      });
      return out;
    });
    if (r.sw > r.iw + 1) { overflow++; console.log('OVERFLOW', path, w, r.sw, r.iw); }
    if (r.narrow.length) { narrow.push([path, w, r.narrow[0]]); }
    if (r.mid.length) { midword.push([path, w, r.mid[0]]); }
    await ctx.close();
  }
}
check(`no horizontal scroll on ${templates.length} templates at ${widths.join(', ')}`, overflow === 0, `${overflow} overflows`);
check('cards in grids are never narrower than 280px', narrow.length === 0, JSON.stringify(narrow.slice(0, 4)));
check('headings never overflow their box (no clipped or mid-word display type)', midword.length === 0, JSON.stringify(midword.slice(0, 4)));

{
  const { ctx, page } = await open('/', 1440);
  const stats = await page.evaluate(() => {
    const out = {};
    document.querySelectorAll('main section[data-layout]').forEach((s) => {
      const id = s.getAttribute('aria-labelledby');
      out[id] = s.dataset.layout;
    });
    return out;
  });
  check('card-grid sections are stacked, single-visual sections are split', stats['who-title'] === 'stack' && stats['samples-title'] === 'stack' && stats['labnotes-title'] === 'stack' && stats['portal-title'] === 'split', JSON.stringify(stats));
  const head = await page.evaluate(() => { const h = document.querySelector('#who-title'); const cs = getComputedStyle(h); return { hy: cs.hyphens, wrap: cs.textWrap, w: h.getBoundingClientRect().width }; });
  check('headings use balance and no hyphenation', head.hy === 'none' && /balance/.test(head.wrap), JSON.stringify(head));
  const font = await page.evaluate(() => Math.min(...[...document.querySelectorAll('.audience p')].map((p) => parseFloat(getComputedStyle(p).fontSize))));
  check('card body text is at least 14px', font >= 14, String(font));
  const sd = await page.evaluate(() => { const li = document.querySelector('.sd-script li, .sd-script ol'); const cs = getComputedStyle(li); return { fs: parseFloat(cs.fontSize), w: document.querySelector('.sd').getBoundingClientRect().width }; });
  check('asset cards are at least 300px wide with 14px text', sd.w >= 300 && sd.fs >= 14, JSON.stringify(sd));
  await ctx.close();
}

{
  const { ctx, page } = await open('/', 1440, { reducedMotion: 'no-preference' });
  await page.locator('.audiences').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1200);
  const bb = await page.locator('.audience').first().boundingBox();
  await page.mouse.move(bb.x + 60, bb.y + 60);
  await page.waitForTimeout(300);
  const g = await page.evaluate(() => { const c = document.querySelector('.audience'); return { gx: c.style.getPropertyValue('--gx'), op: getComputedStyle(c, '::before').opacity }; });
  check('card glow follows the pointer and fades in on hover', /px$/.test(g.gx) && Number(g.op) > 0.3, JSON.stringify(g));
  const draw = await page.evaluate(() => { const p = document.querySelector('.audience .card-icon svg path'); return p ? getComputedStyle(p).strokeDashoffset : 'none'; });
  check('audience icon draws itself (stroke offset reaches 0)', draw === '0px' || draw === '0', draw);
  const ul = await page.evaluate(() => getComputedStyle(document.querySelector('.audience .card-link')).backgroundSize);
  check('card link underlines on card hover', /^(9\d|100)(\.\d+)?%/.test(ul), ul);
  await ctx.close();
}

{
  const { ctx, page } = await open('/', 1440, { reducedMotion: 'no-preference' });
  await page.locator('.facts').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2600);
  const f = await page.evaluate(() => ({ odo: document.querySelectorAll('.fact .odo').length, landed: document.querySelectorAll('.fact.is-landed').length, sr: [...document.querySelectorAll('.fact .odo-sr')].map((e) => e.textContent).join(',') }));
  check('counters roll like an odometer and captions land after', f.odo >= 4 && f.landed >= 4 && f.sr === '4,5,2,5', JSON.stringify(f));
  const hl = await page.evaluate(() => document.querySelectorAll('.section-head h2 .hl-mark').length);
  check('display headings carry a highlighter phrase', hl >= 8, String(hl));
  await ctx.close();
}

{
  const { ctx, page } = await open('/', 1440, { reducedMotion: 'no-preference' });
  const row = page.locator('.sd-row');
  await row.scrollIntoViewIfNeeded();
  await page.waitForTimeout(900);
  const before = await row.evaluate((e) => e.scrollLeft);
  await row.focus();
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(700);
  const after = await row.evaluate((e) => e.scrollLeft);
  check('asset row moves card to card with the arrow keys', after > before + 100, `${before} to ${after}`);
  const bb = await row.boundingBox();
  await page.mouse.move(bb.x + 500, bb.y + 120);
  await page.mouse.down();
  await page.mouse.move(bb.x + 200, bb.y + 120, { steps: 8 });
  const grab = await row.evaluate((e) => e.classList.contains('is-grab'));
  await page.mouse.up();
  await page.waitForTimeout(600);
  const dragged = await row.evaluate((e) => e.scrollLeft);
  check('asset row drags with the mouse and lifts the cards on grab', grab && dragged > after, `${after} to ${dragged}`);
  const snap = await row.evaluate((e) => getComputedStyle(e).scrollSnapType);
  check('asset row uses scroll snap', /mandatory/.test(snap), snap);
  await ctx.close();
}

{
  const { ctx, page } = await open('/compare/kortex-vs-freelance-writer/', 1440, { reducedMotion: 'no-preference' });
  await page.locator('.table-wrap').first().scrollIntoViewIfNeeded();
  await page.waitForTimeout(1500);
  const w = await page.evaluate(() => ({ wins: document.querySelectorAll('td.win').length, clip: getComputedStyle(document.querySelector('td.win'), '::after').clipPath }));
  check('comparison tables mark the winning cells with a check that draws on reveal', w.wins >= 4 && /inset\(0(px)? 0(px)? 0(px)? 0(px)?\)|none/.test(w.clip), JSON.stringify(w));
  const row = page.locator('tbody tr').first();
  await row.hover();
  await page.waitForTimeout(300);
  const c = await page.evaluate(() => getComputedStyle(document.querySelector('tbody tr:hover td.win') || document.body).color);
  check('hovered row turns the winning value to the ember text colour', c !== 'rgb(0, 0, 0)', c);
  await ctx.close();
}

{
  const { ctx, page } = await open('/', 1440, { reducedMotion: 'no-preference' });
  await page.waitForTimeout(1800);
  const v = await page.evaluate(() => { const h = document.querySelector('.hero-visual'); return !!h && !!h.querySelector('.hp-col-a'); });
  const box = await page.locator('.hero-visual').boundingBox();
  await page.mouse.move(box.x + box.width * 0.1, box.y + box.height * 0.1, { steps: 4 });
  await page.mouse.move(box.x + box.width * 0.95, box.y + box.height * 0.95, { steps: 6 });
  await page.waitForTimeout(600);
  const t = await page.evaluate(() => getComputedStyle(document.querySelector('.hero-visual .hp-col-a')).translate);
  check('signature moment: hero diagram layers follow the pointer', v && t !== 'none' && t !== '0px', t);
  await ctx.close();
}

{
  let hits = 0, shown = 0, hiddenOverBand = true;
  for (const w of [1440, 1920]) {
    for (const path of ['/', '/how-it-works/', '/pricing/', '/audit/']) {
      const { ctx, page } = await open(path, w);
      const total = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
      for (const f of [0.2, 0.4, 0.6, 0.8]) {
        await page.evaluate((y) => window.scrollTo(0, y), total * f);
        await page.waitForTimeout(650);
        const r = await page.evaluate(() => {
          const nav = document.querySelector('.homenav');
          if (!nav) return null;
          const on = nav.classList.contains('is-on') && getComputedStyle(nav).opacity > 0.5;
          const rb = nav.getBoundingClientRect();
          const inter = [...document.querySelectorAll('main .card, main .glass, main .sd, main .tier, main .audience, main figure, main .tbl-wrap')].filter((c) => { const b = c.getBoundingClientRect(); return b.width > 0 && !(b.right < rb.left || b.left > rb.right || b.bottom < rb.top || b.top > rb.bottom); }).length;
          const cover = [...document.querySelectorAll('.band-invert, .site-footer, .cta-band')].some((c) => { const b = c.getBoundingClientRect(); const mid = innerHeight / 2; return b.top < mid + innerHeight * 0.04 && b.bottom > mid - innerHeight * 0.04; });
          return { on, inter, cover };
        });
        if (r) { if (r.on) { shown++; hits += r.inter; } if (r.cover && r.on) hiddenOverBand = false; }
      }
      await ctx.close();
    }
  }
  check('rail never overlaps cards or visuals at 1440 and 1920', hits === 0 && shown > 0, `${hits} overlaps over ${shown} visible states`);
  check('rail is hidden whenever a band or the footer is at its height', hiddenOverBand);
  const narrow = await open('/', 1280);
  await narrow.page.mouse.wheel(0, 3000);
  await narrow.page.waitForTimeout(500);
  check('rail is not rendered below 1440px', (await narrow.page.evaluate(() => getComputedStyle(document.querySelector('.homenav')).display)) === 'none');
  await narrow.ctx.close();
}

{
  for (const scheme of ['light', 'dark']) {
    const { ctx, page } = await open('/pricing/', 1440, { colorScheme: scheme });
    const n = await page.evaluate(() => document.querySelectorAll('.band-invert').length);
    check(`theme bleed (${scheme}): exactly one inverted band on pricing`, n === 1, String(n));
    await ctx.close();
  }
}

await browser.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
