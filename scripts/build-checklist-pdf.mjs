import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createRequire } from 'node:module';

const { chromium } = createRequire(import.meta.url)('playwright');
const root = new URL('..', import.meta.url).pathname;
const data = JSON.parse(readFileSync(join(root, 'data/checklist.json'), 'utf8'));

const copy = {
  en: {
    kicker: 'KORTEX',
    title: 'The GEO Audit Checklist',
    sub: 'The 27 checks we run before any engagement',
    intro: 'Give each check a pass, a partial or a fail. Fix the Access group first, then Pages. A pass on every check does not guarantee citations: no engine publishes a full recipe. A fail in Access means the rest cannot work.',
    check: 'Check',
    how: 'How to check',
    good: 'What good looks like',
    score: 'Score',
    pass: 'Pass',
    partial: 'Partial',
    fail: 'Fail',
    sheet: 'Score sheet',
    group: 'Group',
    total: 'Passes',
    of: 'of',
    ctaTitle: 'Want it done for you?',
    ctaText: 'The AI Citation Audit runs these checks on your site and tests 40 buyer questions in ChatGPT, Perplexity, Gemini and Google AI Overviews. 490 euros, delivered in 5 business days, credited in full against your first month.',
    ctaLink: 'kortexlab.me/audit',
    footer: 'KORTEX, Fès, Morocco. Hamza Bentarhlia.',
  },
  fr: {
    kicker: 'KORTEX',
    title: "La checklist d'audit GEO",
    sub: 'Les 27 contrôles que nous faisons avant toute mission',
    intro: "Donnez à chaque contrôle un résultat : réussi, partiel ou échoué. Corrigez d'abord le groupe Accès, puis les Pages. Tout réussir ne garantit pas d'être cité : aucun moteur ne publie de recette complète. Un échec dans Accès signifie que le reste ne peut pas fonctionner.",
    check: 'Contrôle',
    how: 'Comment vérifier',
    good: 'Un bon résultat',
    score: 'Score',
    pass: 'Réussi',
    partial: 'Partiel',
    fail: 'Échoué',
    sheet: 'Grille de score',
    group: 'Groupe',
    total: 'Réussis',
    of: 'sur',
    ctaTitle: 'Vous préférez le faire faire ?',
    ctaText: "L'audit de citations IA applique ces contrôles à votre site et teste 40 questions d'acheteurs dans ChatGPT, Perplexity, Gemini et Google AI Overviews. 490 euros, livré en 5 jours ouvrés, déduit en totalité de votre premier mois.",
    ctaLink: 'kortexlab.me/fr/audit',
    footer: 'KORTEX, Fès, Maroc. Hamza Bentarhlia.',
  },
};

const esc = (v) => v.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const build = (lang) => {
  const c = copy[lang];
  let n = 0;
  const groups = data.groups.map((g) => {
    const rows = data.checks.filter((k) => k.group === g.id).map((k) => {
      n += 1;
      return `<tr><td class="n">${n}</td><td class="t">${esc(k[lang].title)}</td><td>${esc(k[lang].how)}</td><td>${esc(k[lang].good)}</td><td class="s"><span>${c.pass}</span><span>${c.partial}</span><span>${c.fail}</span></td></tr>`;
    }).join('');
    return `<section><h2>${esc(g[lang])}</h2><table><thead><tr><th>#</th><th>${c.check}</th><th>${c.how}</th><th>${c.good}</th><th>${c.score}</th></tr></thead><tbody>${rows}</tbody></table></section>`;
  }).join('');
  const sheet = data.groups.map((g) => {
    const count = data.checks.filter((k) => k.group === g.id).length;
    return `<tr><td>${esc(g[lang])}</td><td class="line">&nbsp;</td><td>${c.of} ${count}</td></tr>`;
  }).join('');
  return `<!doctype html><html lang="${lang}"><meta charset="utf-8"><style>
@font-face{font-family:"Archivo Wide";src:url(file://${root}assets/fonts/archivo-display.woff2) format("woff2");font-weight:600 850}
@font-face{font-family:"Inter";src:url(file://${root}assets/fonts/inter.woff2) format("woff2");font-weight:400 650}
@page{size:A4;margin:16mm 14mm}
*{box-sizing:border-box}
body{margin:0;font:10pt/1.45 "Inter",sans-serif;color:#14213D}
.cover{min-height:255mm;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always}
.brand{font:800 14pt "Archivo Wide",sans-serif;letter-spacing:.08em}
.brand b{display:inline-block;width:9mm;height:9mm;border-radius:2.5mm;background:#FF6B5B;vertical-align:middle;margin-inline-end:3mm}
h1{font:800 34pt/1.05 "Archivo Wide",sans-serif;margin:0 0 6mm}
.sub{font-size:15pt;color:#4A5570;margin:0 0 10mm}
.intro{max-width:140mm;font-size:11pt}
.bar{height:3mm;width:40mm;background:#FF6B5B;border-radius:2mm;margin:8mm 0}
h2{font:800 15pt "Archivo Wide",sans-serif;margin:0 0 4mm;color:#14213D;break-after:avoid}
section{margin-bottom:9mm}
table{width:100%;border-collapse:collapse;font-size:8.6pt}
th{text-align:start;font-weight:600;font-size:7.6pt;letter-spacing:.06em;text-transform:uppercase;color:#4A5570;border-bottom:1.4pt solid #14213D;padding:2mm 2mm}
td{vertical-align:top;border-bottom:.6pt solid #cfc7b9;padding:2.4mm 2mm}
tr{break-inside:avoid}
td.n{width:7mm;font-weight:700;color:#B3331F}
td.t{width:44mm;font-weight:600}
td.s{width:22mm}
td.s span{display:block;font-size:7.6pt;color:#4A5570}
td.s span::before{content:"";display:inline-block;width:2.6mm;height:2.6mm;border:.8pt solid #14213D;margin-inline-end:1.6mm;vertical-align:-.3mm}
.sheet table td{font-size:10pt;padding:3.2mm 2mm}
.line{width:40mm;border-bottom:.8pt solid #14213D}
.cta{border:1.4pt solid #FF6B5B;border-radius:3mm;padding:7mm;margin-top:8mm}
.cta h2{margin-bottom:2mm}
.foot{margin-top:6mm;font-size:8pt;color:#4A5570}
</style><body>
<div class="cover"><div class="brand"><b></b>${c.kicker}</div><div><h1>${esc(c.title)}</h1><p class="sub">${esc(c.sub)}</p><div class="bar"></div><p class="intro">${esc(c.intro)}</p></div><div class="foot">${esc(c.footer)}</div></div>
${groups}
<section class="sheet"><h2>${c.sheet}</h2><table><thead><tr><th>${c.group}</th><th>${c.total}</th><th></th></tr></thead><tbody>${sheet}</tbody></table>
<div class="cta"><h2>${esc(c.ctaTitle)}</h2><p>${esc(c.ctaText)}</p><p><strong>${c.ctaLink}</strong></p></div></section>
</body></html>`;
};

const browser = await chromium.launch();
const page = await browser.newPage();
mkdirSync(join(root, 'assets/downloads'), { recursive: true });
for (const lang of ['en', 'fr']) {
  const file = join(tmpdir(), `kortex-checklist-${lang}.html`);
  writeFileSync(file, build(lang));
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: join(root, `assets/downloads/kortex-geo-audit-checklist-${lang}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
}
await browser.close();
console.log('checklist PDFs written');
