import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const skip = new Set(['src', 'scripts', 'node_modules', '.git', 'assets', 'docs']);

const pages = [];
const walk = (dir) => {
  for (const name of readdirSync(dir)) {
    if (skip.has(name)) continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path);
    else if (name === 'index.html') pages.push(path);
  }
};
walk(root);

const required = {
  Organization: ['name', 'url'],
  WebSite: ['name', 'url'],
  Person: ['name'],
  BlogPosting: ['headline', 'datePublished', 'author', 'publisher', 'mainEntityOfPage', 'inLanguage'],
  Article: ['headline', 'datePublished', 'author', 'publisher'],
  FAQPage: ['mainEntity'],
  BreadcrumbList: ['itemListElement'],
  Service: ['name', 'provider'],
  Offer: ['priceCurrency'],
  DefinedTerm: ['name', 'description'],
  DefinedTermSet: ['name', 'hasDefinedTerm'],
  SoftwareApplication: ['name'],
};

const plain = (value) => value.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();

const flatten = (node, out = []) => {
  if (Array.isArray(node)) node.forEach((n) => flatten(n, out));
  else if (node && typeof node === 'object') {
    if (node['@type']) out.push(node);
    Object.values(node).forEach((v) => flatten(v, out));
  }
  return out;
};

let errors = 0;
let blocks = 0;
const fail = (page, message) => {
  errors += 1;
  console.error(`${relative(root, page)}: ${message}`);
};

for (const page of pages) {
  const html = readFileSync(page, 'utf8');
  if (/http-equiv="refresh"/.test(html)) continue;
  const scripts = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  const visibleQuestions = [...html.matchAll(/<details class="faq-item"[^>]*>\s*<summary>([\s\S]*?)<\/summary>/g)].map((m) => plain(m[1]));
  let hasFaqSchema = false;
  for (const match of scripts) {
    blocks += 1;
    let data;
    try {
      data = JSON.parse(match[1]);
    } catch (error) {
      fail(page, `invalid JSON: ${error.message}`);
      continue;
    }
    for (const node of flatten(data)) {
      const types = [].concat(node['@type']);
      for (const type of types) {
        for (const key of required[type] || []) {
          if (node[key] === undefined || node[key] === '') fail(page, `${type} is missing ${key}`);
        }
        if (type === 'Offer' && node.price === undefined && !node.priceSpecification) fail(page, 'Offer needs price or priceSpecification');
        if (type === 'FAQPage') {
          hasFaqSchema = true;
          const schemaQuestions = node.mainEntity.map((q) => q.name);
          if (JSON.stringify(schemaQuestions) !== JSON.stringify(visibleQuestions)) fail(page, 'FAQPage questions differ from the visible FAQ');
          for (const q of node.mainEntity) {
            if (!q.acceptedAnswer || !q.acceptedAnswer.text) fail(page, `FAQ answer missing for "${q.name}"`);
          }
        }
      }
    }
  }
  if (visibleQuestions.length && !hasFaqSchema) fail(page, 'visible FAQ without FAQPage schema');
}

console.log(`${pages.length} pages, ${blocks} JSON-LD blocks, ${errors} errors`);
if (errors) process.exit(1);
