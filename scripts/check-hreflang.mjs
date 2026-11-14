import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const origin = 'https://www.kortexlab.me';
const sitemap = readFileSync(join(root, 'sitemap.xml'), 'utf8');
const urls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(origin, ''));

const read = (path) => {
  const file = join(root, path.replace(/^\//, ''), 'index.html');
  return existsSync(file) ? readFileSync(file, 'utf8') : null;
};
const cluster = (html) => Object.fromEntries([...html.matchAll(/<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"/g)].map((m) => [m[1], m[2].replace(origin, '')]));
const localeAlternates = (html) => [...html.matchAll(/<meta property="og:locale:alternate" content="([^"]+)"/g)].map((m) => m[1]);
const localeFor = { en: 'en_US', fr: 'fr_FR', ar: 'ar_MA' };

let errors = 0;
const fail = (url, message) => {
  errors += 1;
  console.error(`${url}: ${message}`);
};

for (const url of urls) {
  const html = read(url);
  if (!html) { fail(url, 'page missing'); continue; }
  const set = cluster(html);
  const langs = Object.keys(set).filter((l) => l !== 'x-default');
  const own = langs.find((l) => set[l] === url);
  if (!own) fail(url, 'no self-referencing hreflang');
  if (langs.includes('en') && set['x-default'] !== set.en) fail(url, 'x-default does not point to English');
  for (const lang of langs) {
    const other = read(set[lang]);
    if (!other) { fail(url, `alternate ${lang} does not exist`); continue; }
    const back = cluster(other);
    if (back[own] !== url) fail(url, `alternate ${lang} does not link back`);
  }
  const alt = localeAlternates(html);
  const expected = langs.filter((l) => l !== own).map((l) => localeFor[l]).sort();
  if (JSON.stringify([...alt].sort()) !== JSON.stringify(expected)) fail(url, `og:locale:alternate ${alt} does not match real alternates ${expected}`);
  if (own && !html.includes(`og:locale" content="${localeFor[own]}"`)) fail(url, 'og:locale does not match page language');
}

console.log(`${urls.length} URLs checked, ${errors} errors`);
if (errors) process.exit(1);
