import { createRequire } from 'node:module';

const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv[2] || 'http://localhost:8765';
const results = [];
const check = (name, ok, detail = '') => {
  results.push({ name, ok });
  console.log(`${ok ? 'pass' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
};

const browser = await chromium.launch();

const open = async (path, { status = 200, width = 1280, pointer = true } = {}) => {
  const ctx = await browser.newContext({ viewport: { width, height: 900 } });
  const page = await ctx.newPage();
  const posts = [];
  await page.addInitScript(() => {
    window.kxGA = true;
    try { localStorage.setItem('kx-consent', JSON.stringify({ v: 'granted', t: Date.now() })); } catch (e) { }
  });
  await page.route('**/send.pageclip.co/**', (r) => { posts.push({ url: r.request().url(), body: r.request().postData() || '' }); r.fulfill({ status, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: '{}' }); });
  await page.route(/googletagmanager|google-analytics|cal\.com/, (r) => r.fulfill({ status: 200, contentType: 'text/javascript', body: '' }));
  await page.goto(base + path, { waitUntil: 'networkidle' });
  return { ctx, page, posts };
};

const events = (page) => page.evaluate(() => [...(window.dataLayer || [])].filter((a) => a[0] === 'event').map((a) => ({ name: a[1], params: a[2] })));

{
  const { ctx, page, posts } = await open('/blog/');
  await page.fill('.footer-nl input[type=email]', 'lead@example.org');
  await page.click('.footer-nl button[type=submit]');
  await page.waitForTimeout(600);
  const ev = await events(page);
  check('newsletter posts to Pageclip', posts.length === 1 && posts[0].body.includes('newsletter'));
  check('newsletter success message shown', await page.isVisible('.footer-nl [data-form-ok]'));
  check('newsletter_signup and generate_lead fired', ev.some((e) => e.name === 'newsletter_signup') && ev.some((e) => e.name === 'generate_lead' && e.params.form_name === 'newsletter'));
  await ctx.close();
}

{
  const { ctx, page, posts } = await open('/checklist/');
  await page.fill('.ck-hero-form input[type=email]', 'lead@example.org');
  await page.click('.ck-hero-form button[type=submit]');
  await page.waitForURL('**/thanks/?f=checklist', { timeout: 5000 });
  check('checklist posts and redirects to /thanks/', posts.length === 1 && posts[0].body.includes('checklist'));
  check('thanks page shows the PDF download', await page.isVisible('[data-thanks-block=checklist]'));
  const href = await page.getAttribute('[data-checklist-download]', 'href');
  const pdf = await page.request.get(base + href);
  check('PDF link returns a PDF', pdf.status() === 200 && (pdf.headers()['content-type'] || '').includes('pdf'), href);
  await ctx.close();
}

{
  const { ctx, page, posts } = await open('/audit/');
  await page.fill('#a-name', 'Test Person');
  await page.fill('#a-company', 'Acme');
  await page.fill('#a-site', 'https://example.org');
  await page.fill('#a-email', 'lead@example.org');
  await page.click('#request button[type=submit]');
  await page.waitForURL('**/thanks-audit/', { timeout: 5000 });
  check('audit request posts all fields', posts.length === 1 && ['Acme', 'example.org', 'audit'].every((v) => posts[0].body.includes(v)));
  await ctx.close();
}

{
  const { ctx, page, posts } = await open('/contact/');
  await page.fill('#c-name', 'Test');
  await page.fill('#c-email', 'lead@example.org');
  await page.fill('#c-site', 'https://example.org');
  await page.click('.pageclip-form__submit');
  await page.waitForURL('**/thanks/', { timeout: 5000 });
  check('contact form posts and redirects to /thanks/', posts.length === 1);
  await ctx.close();
}

{
  const { ctx, page, posts } = await open('/audit/', { status: 500 });
  await page.fill('#a-name', 'Test');
  await page.fill('#a-company', 'Acme');
  await page.fill('#a-site', 'https://example.org');
  await page.fill('#a-email', 'lead@example.org');
  await page.click('#request button[type=submit]');
  await page.waitForTimeout(600);
  check('audit shows an inline error when the endpoint fails', await page.isVisible('#request [data-form-error]') && page.url().endsWith('/audit/'));
  await ctx.close();
}

{
  const { ctx, page, posts } = await open('/audit/');
  await page.evaluate(() => { document.querySelector('.hp').checked = true; });
  await page.fill('#a-name', 'Bot');
  await page.fill('#a-company', 'Bot');
  await page.fill('#a-site', 'https://example.org');
  await page.fill('#a-email', 'bot@example.org');
  await page.click('#request button[type=submit]');
  await page.waitForTimeout(400);
  check('honeypot blocks the submission', posts.length === 0);
  await ctx.close();
}

{
  const { ctx, page } = await open('/pricing/');
  const hrefs = await page.$$eval('a[data-cal]', (a) => a.map((x) => x.href));
  check('every booking link carries UTM parameters', hrefs.length > 5 && hrefs.every((h) => /utm_source=site&utm_medium=pricing&utm_campaign=[a-z0-9-]+/.test(h)), `${hrefs.length} links`);
  const withoutCta = await page.$$eval('a.btn', (a) => a.filter((x) => !x.dataset.cta).length);
  check('every button has a data-cta id', withoutCta === 0, `${withoutCta} missing`);
  await page.click('.finder input[name=fsrc][value=many]');
  const rec = await page.$eval('[data-why=titan]', (e) => !e.hidden);
  const link = await page.$eval('[data-finder-book]', (e) => e.href);
  check('plan finder recommends TITAN for two sources and deep-links the plan', rec && /notes=Plan\+I\+am\+considering%3A\+TITAN/.test(link) && link.includes('plan_titan'));
  await page.click('.finder input[name=fsrc][value=one]');
  await page.click('.finder input[name=fcomp][value=quiet]');
  await page.click('.finder input[name=fgoal][value=test]');
  check('plan finder recommends GHOST for a quiet niche and a test', await page.$eval('[data-why=ghost]', (e) => !e.hidden));
  await page.evaluate(() => window.scrollTo({ top: 1300, behavior: 'instant' }));
  await page.waitForTimeout(800);
  const ev = await events(page);
  check('pricing_plan_view fires for visible plans', ev.some((e) => e.name === 'pricing_plan_view'), ev.filter((e) => e.name === 'pricing_plan_view').map((e) => e.params.plan).join(','));
  await page.click('a[data-cal][data-cta="pricing-swarm"]');
  await page.waitForTimeout(500);
  const ev2 = await events(page);
  check('book_call_click and outbound_calcom fire', ev2.some((e) => e.name === 'book_call_click') && ev2.some((e) => e.name === 'outbound_calcom'));
  await ctx.close();
}

{
  const { ctx, page } = await open('/blog/measure-ai-citations/');
  await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight * 0.7, behavior: 'instant' }));
  await page.waitForTimeout(700);
  check('slide-in appears after 60 percent scroll on desktop', await page.isVisible('[data-slide]'));
  await page.click('[data-slide-close]');
  check('slide-in is dismissible', !(await page.isVisible('[data-slide]')));
  const cta = await page.$eval('#cta a[data-cta]', (a) => a.getAttribute('href'));
  check('tactical post ends with the audit CTA', cta === '/audit/', cta);
  await ctx.close();
}

{
  const { ctx, page } = await open('/blog/measure-ai-citations/', { width: 390 });
  await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight * 0.7, behavior: 'instant' }));
  await page.waitForTimeout(500);
  check('slide-in never shows on mobile', !(await page.isVisible('[data-slide]')));
  await ctx.close();
}

{
  const { ctx, page } = await open('/blog/geo-vs-seo-for-b2b/');
  const cta = await page.$eval('#cta a[data-cta]', (a) => a.getAttribute('href'));
  check('strategy post ends with the call CTA', cta.startsWith('https://cal.com/') && cta.includes('utm_campaign=post-book'), cta);
  await ctx.close();
}

{
  const { ctx, page } = await open('/');
  const solutions = await page.$eval('.nav-split .nav-link', (a) => a.getAttribute('href'));
  check('Solutions is a real link', solutions === '/solutions/', solutions);
  await ctx.close();
}

await browser.close();
const failed = results.filter((r) => !r.ok).length;
console.log(`${results.length - failed} of ${results.length} passed`);
if (failed) process.exit(1);
