import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { createRequire } from 'node:module';

const { chromium } = createRequire(import.meta.url)('playwright');

const root = new URL('..', import.meta.url).pathname;
const origin = 'https://www.kortexlab.me';
const fonts = `
@font-face{font-family:"Archivo Wide";src:url(file://${root}assets/fonts/archivo-display.woff2) format("woff2");font-weight:600 850}
@font-face{font-family:"Inter";src:url(file://${root}assets/fonts/inter.woff2) format("woff2");font-weight:400 650}
@font-face{font-family:"Alexandria";src:url(file://${root}assets/fonts/alexandria-arabic.woff2) format("woff2");font-weight:400 800}`;

const decode = (value) => value.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/\s+/g, ' ').trim();
const escape = (value) => value.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const sitemap = readFileSync(join(root, 'sitemap.xml'), 'utf8');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(origin, ''));

const jobs = locs.map((path) => {
  const lang = path.startsWith('/fr/') ? 'fr' : path.startsWith('/ar/') ? 'ar' : 'en';
  const rest = path.replace(/^\/(fr|ar)\//, '/').replace(/^\/|\/$/g, '');
  const pid = rest || 'home';
  const html = readFileSync(join(root, path.replace(/^\//, ''), 'index.html'), 'utf8');
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
  const title = decode(h1 ? h1[1] : html.match(/<title>([\s\S]*?)<\/title>/)[1]);
  const section = pid.includes('/') ? pid.split('/')[0] : pid;
  return { lang, pid, title, section, path };
});

const labels = {
  en: { blog: 'Blog', glossary: 'Glossary', compare: 'Comparison', pricing: 'Pricing', 'how-it-works': 'How it works' },
  fr: { blog: 'Blog', glossary: 'Glossaire', compare: 'Comparatif', pricing: 'Tarifs', 'how-it-works': 'Comment ça marche' },
  ar: { blog: 'المدونة', glossary: 'المصطلحات', compare: 'مقارنة', pricing: 'الأسعار', 'how-it-works': 'كيف نعمل' },
};

const card = ({ lang, title, section, path }) => {
  const rtl = lang === 'ar';
  const family = rtl ? '"Alexandria","Inter"' : '"Archivo Wide","Inter"';
  const size = title.length > 70 ? 54 : title.length > 46 ? 64 : 76;
  const label = labels[lang][section] || '';
  return `<!doctype html><html lang="${lang}" dir="${rtl ? 'rtl' : 'ltr'}"><meta charset="utf-8"><style>${fonts}
*{box-sizing:border-box;margin:0}
html{width:1200px;height:630px;overflow:hidden}
body{width:1200px;height:630px;background:#0B1327;color:#F4EDE3;font-family:"Inter",sans-serif;position:relative;overflow:hidden}
.glow{position:absolute;inset-inline-end:-160px;top:-200px;width:760px;height:760px;border-radius:50%;background:radial-gradient(closest-side,rgb(255 107 91/.30),transparent)}
.frame{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between}
.top{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px;font:800 30px "Archivo Wide",sans-serif;letter-spacing:.06em}
.mark{width:44px;height:44px;border-radius:13px;background:#FF6B5B;display:grid;place-items:center}
.pill{padding:10px 20px;border:2px solid rgb(244 237 227/.24);border-radius:999px;font-size:22px;font-weight:600;color:#A3ACC2}
h1{font-family:${family},sans-serif;font-weight:800;font-size:${size}px;line-height:${rtl ? 1.4 : 1.08};max-width:1000px;text-wrap:balance}
.foot{display:flex;align-items:center;justify-content:space-between;font-size:24px;color:#A3ACC2}
.cta{padding:14px 26px;border-radius:999px;background:#FF6B5B;color:#0B1327;font-weight:700;font-size:24px}
</style><body><div class="glow"></div><div class="frame">
<div class="top"><div class="brand"><span class="mark"><svg width="26" height="26" viewBox="0 0 32 32"><path d="M11 8.5v15M11 16l9-7.5M13.8 13.6l7.2 9.9" stroke="#0B1327" stroke-width="3" stroke-linecap="round" fill="none"/></svg></span>KORTEX</div>${label ? `<span class="pill">${escape(label)}</span>` : ''}</div>
<h1>${escape(title)}</h1>
<div class="foot"><span dir="ltr">kortexlab.me${escape(path === '/' ? '' : path.replace(/\/$/, ''))}</span><span class="cta">${rtl ? 'احجز مكالمة استراتيجية' : lang === 'fr' ? 'Réserver un appel stratégique' : 'Book a strategy call'}</span></div>
</div></body></html>`;
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
let written = 0;
for (const job of jobs) {
  const file = join(tmpdir(), 'kortex-og-card.html');
  writeFileSync(file, card(job));
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const out = join(root, 'assets/og', `${job.pid}-${job.lang}.jpg`);
  if (!existsSync(dirname(out))) mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, await page.screenshot({ type: 'jpeg', quality: 84 }));
  written += 1;
}
await browser.close();
console.log(`${written} images written`);
