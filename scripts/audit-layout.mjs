import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const shots = process.argv.find((a) => a.startsWith('--shots='))?.slice(8);
if (shots) mkdirSync(shots, { recursive: true });
const templates = {
  home: '/', 'how-it-works': '/how-it-works/', pricing: '/pricing/', 'blog-index': '/blog/', 'blog-post': '/blog/entity-seo-for-founders/', 'glossary-index': '/glossary/', 'glossary-term': '/glossary/entity/',
  compare: '/compare/kortex-vs-freelance-writer/', 'compare-index': '/compare/', solutions: '/solutions/', audience: '/solutions/b2b/', source: '/solutions/from-a-blog/', about: '/about/', proof: '/proof/', audit: '/audit/', checklist: '/checklist/',
  contact: '/contact/', teardown: '/teardowns/our-pricing-page/', resources: '/resources/', '404': '/404.html', fr: '/fr/', 'fr-pricing': '/fr/pricing/',
};
const widths = [375, 768, 1024, 1440, 1920];
const b = await chromium.launch();
let bleed = 0, overflow = 0, n = 0;
for (const [name, path] of Object.entries(templates)) {
  for (const scheme of ['light', 'dark']) {
    for (const w of widths) {
      const ctx = await b.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme, reducedMotion: 'reduce' });
      const p = await ctx.newPage();
      await p.goto(base + path, { waitUntil: 'load' });
      await p.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ v: 'denied', t: Date.now() })); } catch (e) { } });
      await p.reload({ waitUntil: 'load' });
      await p.waitForTimeout(500);
      const r = await p.evaluate((scheme) => {
        const lum = (c) => { const m = c.match(/[\d.]+/g).map(Number); const [r, g, b, a = 1] = m; return { l: (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255, a }; };
        const stray = [];
        document.querySelectorAll('main *').forEach((el) => {
          if (el.closest('.band-invert, svg, canvas, picture, video, .vx, .demo, .hpipe, [data-v], .portal, .pt-profile, .hero-visual')) return;
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') return;
          const bb = el.getBoundingClientRect();
          if (bb.width * bb.height < 2500) return;
          const { l, a } = lum(cs.backgroundColor);
          if (a < 0.85) return;
          if (scheme === 'light' && l < 0.25) stray.push((el.className || el.tagName).toString().slice(0, 40));
          if (scheme === 'dark' && l > 0.7) stray.push((el.className || el.tagName).toString().slice(0, 40));
        });
        return { sw: document.documentElement.scrollWidth, iw: innerWidth, stray: [...new Set(stray)].slice(0, 5) };
      }, scheme);
      n++;
      if (r.sw > r.iw + 1) { overflow++; console.log('OVERFLOW', name, scheme, w, r.sw); }
      if (r.stray.length) { bleed++; console.log('BLEED', name, scheme, w, r.stray.join(' | ')); }
      if (shots) await p.screenshot({ path: `${shots}/${name}-${scheme}-${w}.png`, fullPage: true });
      await ctx.close();
    }
  }
}
console.log(`captures ${n}, overflow ${overflow}, bleed hits ${bleed}`);
await b.close();
