import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const results = [];
const check = (name, ok, detail = '') => { results.push(ok); console.log(`${ok ? 'pass' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`); };
const browser = await chromium.launch();
const IGNORE = /ERR_TUNNEL|cal\.com|googletagmanager|pageclip/i;

async function open(path, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, ...opts });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base + path, { waitUntil: 'load' });
  await page.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ analytics: false })); } catch (e) { } });
  await page.reload({ waitUntil: 'load' });
  await page.waitForTimeout(500);
  return { ctx, page, errors };
}

{
  const { ctx, page, errors } = await open('/blog/');
  await page.locator('.bx').scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  const total = await page.locator('.bx-card').count();
  check('blog index: chips become buttons and All is pressed', (await page.locator('button.bx-chip[aria-pressed=true]').count()) === 1);
  await page.locator('.bx-chip[data-cat=measurement]').focus();
  await page.keyboard.press('Enter');
  const shown = await page.locator('.bx-card:not([hidden])').count();
  check('blog index: category filter by keyboard', shown === 2, `shown ${shown} of ${total}`);
  await page.locator('.bx-chip[data-cat=""]').click();
  await page.locator('#bx-q').fill('hreflang');
  await page.waitForTimeout(600);
  const hits = await page.locator('.bx-card:not([hidden])').count();
  check('blog index: search over titles and descriptions', hits >= 1 && hits < total, `hits ${hits}`);
  check('blog index: search result count announced', /found|trouvé/i.test(await page.locator('.bx-status').textContent()));
  await page.locator('#bx-q').fill('zzzzqq');
  await page.waitForTimeout(500);
  check('blog index: empty state message', await page.locator('.bx-none').isVisible());
  check('blog index: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const idx = await (await fetch(base + '/assets/data/blog-index-en.json')).text();
  check('blog search index under 10 KB', idx.length < 10240, idx.length + ' bytes');
}
{
  const { ctx, page, errors } = await open('/glossary/');
  await page.locator('.gl').scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);
  check('glossary: A to Z rail rendered', (await page.locator('.gl-rail a').count()) >= 8);
  const flip = page.locator('.gt-flip').first();
  await flip.focus();
  await page.keyboard.press('Enter');
  check('glossary: card flips from the keyboard', (await page.locator('.gt.is-flipped').count()) === 1 && (await flip.getAttribute('aria-pressed')) === 'true');
  await page.locator('.gl-rail a').nth(3).click();
  await page.waitForTimeout(900);
  check('glossary: rail marks the letter in view', (await page.locator('.gl-rail a[aria-current=true]').count()) === 1);
  check('glossary: at least 18 terms', (await page.locator('.gt').count()) >= 18, String(await page.locator('.gt').count()));
  check('glossary: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/glossary/entity/');
  check('glossary term: related-terms map with links', (await page.locator('.rg a.rg-n').count()) >= 3);
  check('glossary term: DefinedTerm markup present', (await page.content()).includes('"DefinedTerm"'));
  check('glossary term: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/compare/kortex-vs-freelance-writer/');
  await page.locator('.vs').scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  const input = page.locator('.vd-bar input');
  await input.focus();
  await page.keyboard.press('ArrowRight');
  check('compare: verdict slider moves toward KORTEX by keyboard', (await page.locator('.vs').getAttribute('data-lean')) === 'right');
  await page.keyboard.press('Home');
  check('compare: slider reaches the other option', (await page.locator('.vs').getAttribute('data-lean')) === 'left');
  check('compare: verdict text announced', (await page.locator('.vd-out').textContent()).length > 20);
  check('compare: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/solutions/');
  await page.locator('.mix').scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  await page.locator('.mix-chips label').nth(1).click();
  await page.waitForTimeout(300);
  check('solutions: source toggle swaps the panel', (await page.locator('.mix-panel:not([hidden])').count()) === 1 && /video|vidéo/i.test(await page.locator('.mix-panel:not([hidden]) .mix-h').textContent()));
  await page.locator('input[name=mix-source]').nth(1).focus();
  await page.keyboard.press('ArrowRight');
  check('solutions: arrow keys move through sources', await page.locator('input[name=mix-source]').nth(2).isChecked());
  check('solutions: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/checklist/');
  await page.locator('.ck').scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  const boxes = page.locator('.ck-row input');
  check('checklist: 27 checks are tickable', (await boxes.count()) === 27);
  await boxes.nth(0).focus();
  await page.keyboard.press('Space');
  check('checklist: space ticks a check and the count updates', /^1 of 27|^1 vérification/.test((await page.locator('.ck-count').textContent()).trim()));
  for (let i = 1; i < 20; i++) await boxes.nth(i).check();
  check('checklist: 20 ticks suggest the audit', /audit/i.test(await page.locator('.ck-cta a').textContent()));
  await page.locator('.ck-reset').click();
  check('checklist: reset clears the ticks', (await page.locator('.ck-row input:checked').count()) === 0);
  check('checklist: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/contact/');
  const form = page.locator('form[data-module=fields]');
  await form.scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  let posted = false;
  await page.route(/pageclip/i, (route) => { posted = true; route.fulfill({ status: 200, body: '{}' }); });
  await page.locator('#c-email').fill('abc');
  await page.locator('#c-name').focus();
  check('contact: invalid email message in voice', /incomplete/.test(await form.locator('.ff-msg:not([hidden])').first().textContent()));
  await form.locator('button[type=submit]').click();
  await page.waitForTimeout(400);
  check('contact: empty required fields block the send', !posted && (await form.locator('.ff-msg:not([hidden])').count()) >= 2);
  check('contact: invalid fields flagged with aria-invalid', (await form.locator('[aria-invalid=true]').count()) >= 2);
  await page.locator('#c-name').fill('Test Person');
  await page.locator('#c-email').fill('test@example.com');
  await page.locator('#c-site').fill('https://example.com');
  await form.locator('button[type=submit]').click();
  await page.waitForTimeout(900);
  check('contact: valid form is sent', posted);
  check('contact: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/');
  await page.mouse.wheel(0, 2600);
  await page.waitForTimeout(900);
  check('home: section nav appears after the hero', (await page.locator('.homenav.is-on').count()) === 1 && (await page.locator('.homenav li').count()) >= 5);
  await page.locator('.homenav a').nth(2).click();
  await page.waitForTimeout(1200);
  check('home: section nav scrolls and marks the active section', (await page.locator('.homenav a[aria-current=true]').count()) === 1);
  check('home: lab notes list the latest three pieces', (await page.locator('.labnotes .card').count()) === 3);
  check('home: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/pricing/');
  const btn = page.locator('.pr-diff');
  await btn.scrollIntoViewIfNeeded();
  await btn.focus();
  await page.keyboard.press('Enter');
  check('pricing: compare toggle highlights differing rows', (await btn.getAttribute('aria-pressed')) === 'true' && (await page.locator('.tbl.is-diff tr[data-same]').count()) >= 3);
  check('pricing: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
  const m = await open('/pricing/', { viewport: { width: 390, height: 800 } });
  await m.page.locator('#finder').scrollIntoViewIfNeeded();
  await m.page.locator('input[name=fcomp][value=own]').check({ force: true });
  await m.page.waitForTimeout(500);
  check('pricing mobile: sticky bar shows the selected plan', /TITAN/.test(await m.page.locator('[data-bookbar] span').textContent()), await m.page.locator('[data-bookbar] span').textContent());
  await m.ctx.close();
}
{
  const { ctx, page, errors } = await open('/how-it-works/');
  const fill = page.locator('.hl-fill i').first();
  await page.locator('.hl').scrollIntoViewIfNeeded();
  const read = () => page.evaluate(() => getComputedStyle(document.querySelector('.hl')).getPropertyValue('--p'));
  const a = await read();
  await page.mouse.wheel(0, 900);
  await page.waitForTimeout(700);
  const b = await read();
  check('how it works: pipeline progress follows the scroll', a !== b, `${a} to ${b}`);
  check('how it works: five stages', (await page.locator('.hl-station').count()) === 5);
  check('how it works: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
  const r = await open('/how-it-works/', { reducedMotion: 'reduce' });
  check('how it works reduced motion: stages not pinned', (await r.page.evaluate(() => getComputedStyle(document.querySelector('.hl-sticky')).position)) === 'static');
  await r.ctx.close();
}
{
  const { ctx, page, errors } = await open('/blog/entity-seo-for-founders/');
  await page.mouse.wheel(0, 1500);
  await page.waitForTimeout(700);
  check('article: progress bar and contents rail', (await page.locator('.read-progress').count()) === 1 && (await page.locator('.toc a').count()) >= 5);
  check('article: pull quote and aside present', (await page.locator('blockquote.pull').count()) === 1 && (await page.locator('details.aside').count()) === 1);
  await page.locator('details.aside summary').focus();
  await page.keyboard.press('Enter');
  check('article: aside opens by keyboard', await page.locator('details.aside').evaluate((d) => d.open));
  check('article: next and previous tiles', (await page.locator('.post-nav .pn').count()) >= 1);
  check('article: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page, errors } = await open('/404.html');
  check('404: canvas and three links', (await page.locator('canvas.kx-field').count()) === 1 && (await page.locator('.notfound .hero-actions a').count()) === 3);
  check('404: no console errors', errors.length === 0, errors.join(' | '));
  await ctx.close();
}
{
  const { ctx, page } = await open('/glossary/', { javaScriptEnabled: false });
  check('no JS glossary: all terms and both faces in the HTML', (await page.locator('.gt').count()) >= 18 && (await page.locator('.gt-back p').count()) >= 18);
  await ctx.close();
}
{
  const { ctx, page } = await open('/blog/', { javaScriptEnabled: false });
  check('no JS blog: every article card and category link present', (await page.locator('.bx-card').count()) >= 19 && (await page.locator('a.bx-chip').count()) === 4);
  await ctx.close();
}
{
  const { ctx, page } = await open('/solutions/', { javaScriptEnabled: false });
  check('no JS solutions: all four source panels visible', (await page.locator('.mix-panel:visible').count()) === 4);
  await ctx.close();
}
{
  const { ctx, page } = await open('/checklist/', { javaScriptEnabled: false });
  check('no JS checklist: 27 checks listed', (await page.locator('.ck-list li').count()) === 27);
  await ctx.close();
}
{
  const { ctx, page } = await open('/glossary/entity/', { javaScriptEnabled: false });
  check('no JS term: related terms reachable', (await page.locator('.rg a, .rg-list a').count()) >= 3);
  await ctx.close();
}
{
  const { ctx, page } = await open('/', { reducedMotion: 'reduce' });
  await page.mouse.wheel(0, 2600);
  await page.waitForTimeout(600);
  check('reduced motion: no animations running on the home page', (await page.evaluate(() => document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.getTiming().iterations === Infinity).length)) === 0);
  await ctx.close();
}
for (const path of ['/fr/blog/', '/fr/glossary/', '/fr/glossary/entity/', '/fr/compare/kortex-vs-in-house-writer/', '/fr/solutions/', '/fr/checklist/', '/fr/contact/', '/fr/blog/human-qa-layer/', '/fr/teardowns/', '/teardowns/', '/audit/', '/about/', '/proof/', '/blog/podcast-to-authority/', '/glossary/share-of-model/']) {
  const { ctx, page, errors } = await open(path);
  await page.waitForTimeout(600);
  await page.mouse.wheel(0, 1800);
  await page.waitForTimeout(500);
  check(`console clean: ${path}`, errors.length === 0, errors.join(' | '));
  await ctx.close();
}
await browser.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
