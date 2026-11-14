import { readFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const [root, label] = process.argv.slice(2);
const origin = 'https://www.kortexlab.me';

const sitemap = readFileSync(join(root, 'sitemap.xml'), 'utf8');
const urls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(origin, ''));
const extra = ['/login/', '/fr/login/', '/ar/login/'];
const routes = [...new Set([...urls, ...extra])];

const isFile = (p) => existsSync(p) && statSync(p).isFile();
const isDir = (p) => existsSync(p) && statSync(p).isDirectory();

const resolve = (path) => {
  const fs = join(root, path.replace(/^\//, ''));
  if (path.endsWith('/')) {
    const index = join(fs, 'index.html');
    return isFile(index) ? { status: 200, file: index } : { status: 404 };
  }
  if (isFile(fs)) return { status: 200, file: fs };
  if (isFile(fs + '.html')) return { status: 200, file: fs + '.html' };
  if (isDir(fs) && isFile(join(fs, 'index.html'))) return { status: 301, to: path + '/' };
  return { status: 404 };
};

const inspect = (file) => {
  const html = readFileSync(file, 'utf8');
  const robots = (html.match(/<meta name="robots" content="([^"]*)"/) || [])[1] || 'default';
  const canonical = ((html.match(/<link rel="canonical" href="([^"]*)"/) || [])[1] || 'none').replace(origin, '');
  const refresh = /http-equiv="refresh"/.test(html);
  return { robots, canonical, refresh, bytes: Buffer.byteLength(html) };
};

const rows = [];
let problems = 0;
for (const route of routes) {
  for (const form of [route, route.length > 1 ? route.replace(/\/$/, '') : null]) {
    if (!form) continue;
    const r = resolve(form);
    let cell = `${r.status}`;
    let robots = '-';
    let canonical = '-';
    let note = '';
    if (r.status === 301) {
      const target = resolve(r.to);
      cell = `301 to ${r.to}`;
      if (target.status === 200) {
        const i = inspect(target.file);
        robots = i.robots;
        canonical = i.canonical;
      }
    } else if (r.status === 200) {
      const i = inspect(r.file);
      robots = i.robots;
      canonical = i.canonical;
      if (i.refresh) note = 'redirect stub';
      if (i.bytes < 2000) note = (note ? note + ', ' : '') + 'near-empty';
    }
    const wanted = route.endsWith('/') ? route : route + '/';
    const isLogin = /\/login\/$/.test(route);
    const bad = r.status !== 200 && r.status !== 301
      || (r.status === 200 && !isLogin && (robots.includes('noindex') || canonical !== wanted || note))
      || (r.status === 200 && form !== route && form.length > 1);
    if (bad) problems += 1;
    rows.push(`| ${form} | ${cell} | ${robots} | ${canonical} | ${note || (bad ? 'check' : 'ok')} |`);
  }
}

console.log(`## ${label}\n`);
console.log(`${routes.length} routes, each tested slashed and unslashed. Rows needing attention: ${problems}.\n`);
console.log('| URL | Status | Robots | Canonical | Result |\n|---|---|---|---|---|');
console.log(rows.join('\n'));
console.log('');
