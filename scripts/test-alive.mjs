import { createRequire } from 'node:module';
import { mkdirSync, readFileSync } from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const videos = process.argv.find((a) => a.startsWith('--video='))?.slice(8);
if (videos) mkdirSync(videos, { recursive: true });
const results = [];
const check = (name, ok, detail = '') => { results.push(ok); console.log(`${ok ? 'pass' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`); };
const IGNORE = /ERR_TUNNEL|cal\.com|googletagmanager|pageclip/i;
const browser = await chromium.launch();

async function open(path, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, ...opts });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base + path, { waitUntil: 'load' });
  return { ctx, page, errors };
}

const running = (page) => page.evaluate(() => document.getAnimations().filter((a) => a.playState === 'running' || a.playState === 'pending').map((a) => (a.effect && a.effect.getKeyframes ? a.effect.getKeyframes().map((k) => Object.keys(k).join(',')).join(';') : '')).filter((k) => /transform|translate|scale|rotate|clipPath|clip-path/.test(k)).length);

{
  const { ctx, page } = await open('/', { reducedMotion: 'no-preference' });
  await page.waitForTimeout(150);
  const words = await page.evaluate(() => document.querySelector('.hero h1').getAnimations({ subtree: true }).length);
  check('entry: headline words animate on first load', words >= 6, String(words));
  await page.waitForTimeout(2200);
  await Promise.all([page.waitForURL('**/pricing/'), page.locator('header a[href="/pricing/"]').first().click()]);
  await page.waitForLoadState('load');
  await page.waitForTimeout(150);
  check('entry: second page in the session skips the sequence', await page.evaluate(() => document.documentElement.classList.contains('no-entry') && document.querySelector('h1').getAnimations({ subtree: true }).length === 0));
  await ctx.close();
}

for (const path of ['/', '/how-it-works/', '/pricing/']) {
  const { ctx, page, errors } = await open(path, { reducedMotion: 'reduce' });
  let peak = 0;
  for (let y = 0; y < 8; y++) {
    await page.mouse.wheel(0, 900);
    await page.waitForTimeout(250);
    peak = Math.max(peak, await running(page));
  }
  check(`reduced motion: zero animated transforms while scrolling ${path}`, peak === 0, `peak ${peak}`);
  check(`reduced motion: no console errors ${path}`, errors.length === 0, errors.join(' | '));
  const wipe = await page.evaluate(() => { const b = document.querySelector('.band-invert'); return b ? getComputedStyle(b).animationName : 'none'; });
  check(`reduced motion: inverted band is not animated ${path}`, wipe === 'none' || wipe === '', wipe);
  await ctx.close();
}

{
  const { ctx, page } = await open('/', { reducedMotion: 'no-preference' });
  await page.mouse.wheel(0, 3000);
  await page.waitForTimeout(500);
  const wipe = await page.evaluate(() => { const b = document.querySelector('.band-invert'); return getComputedStyle(b).animationName; });
  const supports = await page.evaluate(() => CSS.supports('animation-timeline: view()'));
  check('scroll choreography: inverted band wipe is attached when supported', !supports || wipe.includes('kx-wipe'), wipe);
  check('scroll choreography: section rules present', (await page.locator('.section').count()) > 5);
  const ticks = await page.evaluate(() => [...document.querySelectorAll('.sx-n')].every((e) => /^\d\d$/.test(e.textContent)));
  check('mono indexes keep a two digit format', ticks);
  await ctx.close();
}

for (const scheme of ['light', 'dark']) {
  const { ctx, page } = await open('/', { colorScheme: scheme });
  const btn = page.locator('[data-theme-toggle]').first();
  check(`theme (${scheme}): toggle is 44px and exposes aria-pressed`, (await btn.boundingBox()).width >= 44 && ['true', 'false'].includes(await btn.getAttribute('aria-pressed')));
  const before = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  await btn.click();
  await page.waitForTimeout(500);
  const after = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  check(`theme (${scheme}): toggle changes the page ground`, before !== after, `${before} to ${after}`);
  await page.reload({ waitUntil: 'domcontentloaded' });
  check(`theme (${scheme}): choice is set before first paint on reload`, await page.evaluate(() => !!document.documentElement.dataset.theme));
  const metas = await page.evaluate(() => [...document.querySelectorAll('meta[name=theme-color]')].length);
  check(`theme (${scheme}): two theme-color metas`, metas === 2);
  await ctx.close();
}

for (const theme of ['light', 'dark']) {
  const { ctx, page } = await open('/pricing/', { colorScheme: theme });
  await page.addInitScript(() => { try { localStorage.setItem('kx-theme', theme); } catch (e) { } });
  const band = await page.evaluate(() => { const b = document.querySelector('.band-invert'); const c = getComputedStyle(b).backgroundColor; return c; });
  const m = band.match(/\d+/g).map(Number);
  check(`inverted band legible in ${theme}: background is navy`, m[2] > m[0] && m[0] < 40, band);
  await ctx.close();
}

{
  const { ctx, page } = await open('/pricing/');
  check('ladder: three steps on pricing', (await page.locator('.ld-step').count()) === 3);
  check('ladder: price points are real', /€490/.test(await page.locator('.ld').textContent()) && /2,500/.test(await page.locator('.ld').textContent()));
  const html = await page.content();
  check('ladder: call tests 3 questions, audit does 40', /3 of your buyers/.test(html) && /40 questions/.test(html) && !/a few of your buyers/.test(html));
  check('ladder: audit is the secondary CTA in the header', (await page.locator('.page-hero a[href="/audit/"]').count()) === 1);
  await ctx.close();
  const home = await open('/');
  check('ladder: condensed ladder in the home closing band', (await home.page.locator('.cta-band .ld-short li').count()) === 3);
  await home.ctx.close();
}

{
  const { ctx, page } = await open('/');
  const html = await page.content();
  check('language: no ar_MA and no Arabic hreflang', !html.includes('ar_MA') && !/hreflang="ar"/.test(html));
  check('language: English and French switcher in header and footer', (await page.locator('.lang-switch a[hreflang=fr]').count()) === 1 && (await page.locator('.footer-lang a[hreflang=fr]').count()) === 1);
  check('language: counter reads 2 languages', /2[\s\S]{0,40}languages: English and French/.test(html.replace(/<[^>]+>/g, ' ')));
  await ctx.close();
  const fr = await open('/fr/');
  const fhtml = await fr.page.content();
  check('language: French page has og:locale fr_FR and reciprocal alternates', fhtml.includes('og:locale" content="fr_FR"') && /hreflang="en" href="https:\/\/www\.kortexlab\.me\/"/.test(fhtml) && /hreflang="x-default"/.test(fhtml));
  await fr.ctx.close();
}

{
  const sm = readFileSync(new URL('../sitemap.xml', import.meta.url), 'utf8');
  check('sitemap: no Arabic URLs while Arabic is off', !/kortexlab\.me\/ar\//.test(sm));
  const { ctx, page } = await open('/ar/');
  check('Arabic tree still answers but is noindex', /noindex/.test(await page.content()));
  await ctx.close();
}

{
  const { ctx, page } = await open('/glossary/');
  const first = page.locator('.gl-rail a').first();
  await first.scrollIntoViewIfNeeded();
  check('footer wordmark is within the viewport width', await page.evaluate(() => { const m = document.querySelector('.footer-mark svg'); return m.getBoundingClientRect().width <= document.documentElement.clientWidth + 1; }));
  await ctx.close();
}

if (videos) {
  for (const scheme of ['light', 'dark']) {
    for (const path of ['/', '/how-it-works/']) {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, colorScheme: scheme, recordVideo: { dir: videos, size: { width: 1024, height: 576 } } });
      const page = await ctx.newPage();
      await page.goto(base + path, { waitUntil: 'load' });
      await page.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ v: 'denied', t: Date.now() })); } catch (e) { } });
      await page.reload({ waitUntil: 'load' });
      await page.waitForTimeout(1600);
      for (let i = 0; i < 14; i++) { await page.mouse.move(500 + i * 20, 300 + (i % 3) * 40); await page.mouse.wheel(0, 700); await page.waitForTimeout(420); }
      const file = await page.video().path();
      await ctx.close();
      const { renameSync } = await import('node:fs');
      renameSync(file, `${videos}/${path === '/' ? 'home' : 'how-it-works'}-${scheme}.webm`);
    }
  }
}

await browser.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
