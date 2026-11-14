import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';

const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const teaser = process.argv.includes('--teaser');
const shots = process.argv.find((a) => a.startsWith('--shots='))?.slice(8);
if (shots) mkdirSync(shots, { recursive: true });
const results = [];
const check = (name, ok, detail = '') => {
  results.push(ok);
  console.log(`${ok ? 'pass' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
};
const eur = (n) => '€' + n.toLocaleString('en-US');

const cases = [
  { assets: 12, rate: 250, hours: 4, value: 60 },
  { assets: 4, rate: 50, hours: 0, value: 30 },
  { assets: 10, rate: 300, hours: 2, value: 100 },
  { assets: 11, rate: 600, hours: 10, value: 100 },
  { assets: 24, rate: 400, hours: 20, value: 100 },
  { assets: 25, rate: 300, hours: 8, value: 60 },
].map((c) => {
  const production = c.assets * c.rate;
  const time = Math.round((c.hours * 52 / 12) * c.value);
  const current = production + time;
  const plan = c.assets <= 10 ? 'GHOST' : c.assets <= 24 ? 'SWARM' : 'TITAN';
  const price = { GHOST: 2500, SWARM: 5500, TITAN: 12000 }[plan];
  return { ...c, production, time, current, plan, price };
});

const browser = await chromium.launch();

async function open(path, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, ...opts });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base + path, { waitUntil: 'load' });
  await page.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ analytics: false })); } catch (e) { } });
  return { ctx, page, errors };
}

{
  const { ctx, page, errors } = await open('/');
  const demo = page.locator('.demo');
  await demo.scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  check('demo: enhanced idle state with a Run button', (await demo.getAttribute('data-state')) === 'idle' && await page.locator('[data-demo-run]').isVisible());
  const chip = page.locator('input[name=demo-source]').first();
  await chip.focus();
  await page.keyboard.press('ArrowRight');
  check('demo: arrow key moves the source radio', await page.locator('input[name=demo-source][value=video]').isChecked());
  await page.keyboard.press('Tab');
  const focusedRun = await page.evaluate(() => document.activeElement?.matches('[data-demo-run]'));
  check('demo: Tab reaches the Run button', focusedRun);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
  check('demo: Enter starts the run', (await demo.getAttribute('data-state')) === 'running');
  await page.waitForTimeout(5200);
  check('demo: run completes', (await demo.getAttribute('data-state')) === 'done');
  check('demo: 8 asset cards present, all dealt after the run', (await page.locator('.demo-cards li').count()) === 8 && (await page.locator('.demo-cards li.is-dealt').count()) === 8);
  check('demo: 5 stages present', (await page.locator('.ds').count()) === 5);
  const card = page.locator('details.dc').nth(1);
  await card.locator('summary').focus();
  await page.keyboard.press('Enter');
  check('demo: card flips open from the keyboard', await card.evaluate((d) => d.open));
  check('demo: status is announced', (await page.locator('[data-demo-status]').textContent()).includes('10 assets'));
  check('demo: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

{
  const { ctx, page, errors } = await open('/', { reducedMotion: 'reduce' });
  const demo = page.locator('.demo');
  await demo.scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  await page.locator('[data-demo-run]').click();
  await page.waitForTimeout(150);
  check('demo reduced motion: final state at once', (await demo.getAttribute('data-state')) === 'done' && (await page.locator('.demo-cards li.is-dealt').count()) === 8);
  const frozen = await page.evaluate(() => new Promise((r) => { const c = document.querySelector('canvas.kx-field'); const a = c.toDataURL(); setTimeout(() => r(a === c.toDataURL()), 700); }));
  check('canvas reduced motion: frozen', frozen);
  check('hero reduced motion: no split words', (await page.locator('.hero h1 .hw').count()) === 0);
  check('reduced motion: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

{
  const { ctx, page, errors } = await open('/pricing/');
  const calc = page.locator('.calc2');
  await calc.scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  for (const [i, c] of cases.entries()) {
    await page.evaluate((c) => {
      const set = (id, v) => { const el = document.getElementById(id); el.value = String(v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
      set('cx-assets', c.assets); set('cx-rate', c.rate); set('cx-hours', c.hours); set('cx-value', c.value);
    }, c);
    await page.waitForTimeout(650);
    const got = {
      current: await page.locator('[data-current]').textContent(),
      plan: (await page.locator('[data-plan-name]').textContent()).trim(),
      price: await page.locator('[data-plan-price]').textContent(),
    };
    const ok = got.current === eur(c.current) && got.plan === c.plan && got.price === eur(c.price);
    check(`calc case ${i + 1}: ${c.assets} assets, ${eur(c.rate)}, ${c.hours} h, ${eur(c.value)}/h`, ok, `expected ${eur(c.current)} / ${c.plan} ${eur(c.price)}, got ${got.current} / ${got.plan} ${got.price}`);
    const verdict = await page.locator('[data-verdict]').textContent();
    const expectMore = c.plan !== 'TITAN' && c.price > c.current;
    const expectLess = c.plan !== 'TITAN' && c.price <= c.current;
    check(`calc case ${i + 1}: verdict`, c.plan === 'TITAN' ? /starts at/.test(verdict) : expectMore ? /costs more/.test(verdict) : expectLess ? /less/.test(verdict) : false, verdict.slice(0, 70));
  }
  const cta = await page.locator('[data-cta=calc]').getAttribute('href');
  check('calc: CTA carries the plan', /TITAN/.test(decodeURIComponent(cta)), decodeURIComponent(cta).slice(0, 90));
  check('calc: single ember CTA', (await page.locator('.calc2 .btn-primary').count()) === 1);
  await page.locator('#cx-assets').focus();
  await page.keyboard.press('Home');
  check('calc: slider operable by keyboard', (await page.locator('#cx-assets').inputValue()) === '4');
  check('calc: output is a live region', (await page.locator('.calc2-out').getAttribute('aria-live')) === 'polite');
  check('calc: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

{
  const { ctx, page } = await open('/pricing/', { javaScriptEnabled: false });
  const text = await page.locator('.calc2').innerText();
  check('calc without JS: defaults and verdict in the page', text.includes('€4,040') && text.includes('€5,500') && /costs more/.test(text));
  await ctx.close();
}

{
  const { ctx, page } = await open('/', { javaScriptEnabled: false });
  const text = await page.locator('.demo').innerText();
  check('demo without JS: stages and cards in the page', /Extract/i.test(text) && (await page.locator('.demo-cards li').count()) === 8 && (await page.locator('details.dc').count()) === 8);
  check('demo without JS: run button hidden', !(await page.locator('[data-demo-run]').isVisible()));
  await ctx.close();
}

{
  const { ctx, page, errors } = await open('/fr/');
  const demo = page.locator('.demo');
  await demo.scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  await page.locator('[data-demo-run]').click();
  await page.waitForTimeout(5800);
  check('demo FR: runs and reports in French', /prêts|terminé/i.test(await page.locator('[data-demo-status]').textContent()), await page.locator('[data-demo-status]').textContent());
  check('demo FR: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

{
  const { ctx, page, errors } = await open('/fr/pricing/');
  await page.locator('.calc2').scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  const t = await page.locator('[data-current]').textContent();
  check('calc FR: French number format', /4\s?040\s?€/.test(t.replace(/ | /g, ' ')), t);
  check('calc FR: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}

if (teaser) {
  for (const [path, lang] of [['/audit/', 'en'], ['/', 'en'], ['/fr/audit/', 'fr']]) {
    const { ctx, page, errors } = await open(path);
    const tz = page.locator('.tz');
    await tz.scrollIntoViewIfNeeded();
    await page.waitForTimeout(700);
    const select = page.locator('[data-tz-select]');
    await select.focus();
    await select.selectOption({ index: 2 });
    await page.waitForTimeout(300);
    check(`teaser ${path}: select shows an answer`, (await page.locator('.tz-ai').count()) === 1);
    await page.waitForTimeout(2200);
    check(`teaser ${path}: punchline shown within 2.2 s`, (await page.locator('.tz-punch').textContent()).includes(lang === 'en' ? 'None of these citations' : 'Aucune de ces citations'));
    await page.locator('.tz-skip').click();
    check(`teaser ${path}: skip works`, await page.locator('[data-tz-pane].is-skipped').count() === 1);
    let posted = null;
    await page.route(/pageclip|forms|contact|leads/i, (route) => { posted = route.request().url(); route.fulfill({ status: 200, contentType: 'application/json', body: '{}' }); });
    const form = tz.locator('form[data-lead-form]');
    if (await form.count()) {
      await form.locator('input[type=email]').fill('test@example.com');
      await form.locator('input[type=url]').fill('https://example.com');
      await form.locator('button[type=submit]').click();
      await page.waitForTimeout(900);
      check(`teaser ${path}: form submit intercepted`, posted !== null, posted || '');
    }
    check(`teaser ${path}: no console errors`, errors.length === 0, errors.join(' | '));
    await ctx.close();
  }
}

for (const path of ['/', '/pricing/', '/audit/', '/teardowns/', '/teardowns/our-pricing-page/', '/blog/measure-ai-citations/', '/fr/', '/fr/pricing/', '/fr/teardowns/our-pricing-page/']) {
  const { ctx, page, errors } = await open(path);
  await page.waitForTimeout(900);
  await page.mouse.wheel(0, 1600);
  await page.waitForTimeout(600);
  check(`console clean: ${path}`, errors.length === 0, errors.join(' | '));
  await ctx.close();
}

if (shots) {
  const sets = [
    { name: 'home', path: '/' }, { name: 'pricing', path: '/pricing/' }, { name: 'audit', path: '/audit/' }, { name: 'teardown', path: '/teardowns/our-pricing-page/' },
  ];
  for (const { name, path } of sets) {
    for (const scheme of ['light', 'dark']) {
      for (const w of [375, 768, 1440]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: w === 1440 ? 900 : 800 }, colorScheme: scheme });
        const page = await ctx.newPage();
        await page.goto(base + path, { waitUntil: 'load' });
        await page.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ analytics: false })); } catch (e) { } });
        await page.waitForTimeout(1200);
        const sel = name === 'pricing' ? '.calc2' : name === 'home' ? '.demo' : null;
        if (sel) { await page.locator(sel).first().scrollIntoViewIfNeeded(); await page.waitForTimeout(900); }
        await page.screenshot({ path: `${shots}/${name}-${scheme}-${w}.png` });
        await ctx.close();
      }
    }
    for (const [tag, opts] of [['reduced', { reducedMotion: 'reduce' }], ['nojs', { javaScriptEnabled: false }]]) {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'light', ...opts });
      const page = await ctx.newPage();
      await page.goto(base + path, { waitUntil: 'load' });
      await page.waitForTimeout(900);
      const sel = name === 'pricing' ? '.calc2' : name === 'home' ? '.demo' : null;
      if (sel) { await page.locator(sel).first().scrollIntoViewIfNeeded(); await page.waitForTimeout(600); }
      await page.screenshot({ path: `${shots}/${name}-${tag}-1440.png` });
      await ctx.close();
    }
  }
}

await browser.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
