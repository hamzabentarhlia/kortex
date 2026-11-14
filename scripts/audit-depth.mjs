import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const base = process.argv.slice(2).find((a) => a.startsWith('http')) || 'http://localhost:8765';
const axePath = process.env.AXE_PATH;
const axeSource = axePath ? readFileSync(axePath, 'utf8') : null;
const shots = process.argv.find((a) => a.startsWith('--shots='))?.slice(8);
if (shots) mkdirSync(shots, { recursive: true });
const templates = {
  home: '/', 'how-it-works': '/how-it-works/', pricing: '/pricing/', 'blog-index': '/blog/', 'blog-post': '/blog/entity-seo-for-founders/', 'glossary-index': '/glossary/', 'glossary-term': '/glossary/entity/',
  compare: '/compare/kortex-vs-freelance-writer/', solutions: '/solutions/', audience: '/solutions/b2b/', about: '/about/', proof: '/proof/', audit: '/audit/', checklist: '/checklist/', contact: '/contact/', teardown: '/teardowns/our-pricing-page/', '404': '/404.html',
};
const b = await chromium.launch();
let overflow = 0, violations = 0;
for (const [name, path] of Object.entries(templates)) {
  for (const scheme of ['light', 'dark']) {
    for (const w of [375, 768, 1440]) {
      const ctx = await b.newContext({ viewport: { width: w, height: w === 1440 ? 900 : 812 }, colorScheme: scheme, reducedMotion: 'reduce' });
      const p = await ctx.newPage();
      await p.goto(base + path, { waitUntil: 'load' });
      await p.evaluate(() => { try { localStorage.setItem('kx-consent', JSON.stringify({ v: 'denied', t: Date.now() })); } catch (e) { } });
      await p.reload({ waitUntil: 'load' });
      await p.waitForTimeout(900);
      const wide = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (wide > 1) { overflow++; console.log('OVERFLOW', name, scheme, w, wide); }
      if (axeSource && w === 1440) {
        await p.addScriptTag({ content: axeSource });
        const r = await p.evaluate(() => axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] }));
        for (const v of r.violations) { violations++; console.log('AXE', name, scheme, v.id, v.impact, v.nodes.length, v.nodes[0].target.join(' ').slice(0, 80)); }
      }
      if (shots) await p.screenshot({ path: `${shots}/${name}-${scheme}-${w}.png` });
      await ctx.close();
    }
  }
}
console.log(`templates ${Object.keys(templates).length}, overflow ${overflow}, axe violations ${violations}`);
await b.close();
