import { readFileSync } from 'node:fs';

const css = readFileSync(new URL('../src/styles/tokens.css', import.meta.url), 'utf8');

const readBlock = (selector) => {
  const start = css.indexOf(selector + '{');
  const end = css.indexOf('}', start);
  const tokens = {};
  for (const match of css.slice(start, end).matchAll(/--([a-z0-9-]+):(#[0-9a-fA-F]{6})\b/g)) tokens[match[1]] = match[2];
  return tokens;
};

const themes = {
  dark: readBlock(':root'),
  light: readBlock(':root[data-theme=light]'),
};

const channel = (value) => {
  const v = value / 255;
  return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
};

const luminance = (hex) => {
  const n = parseInt(hex.slice(1), 16);
  return 0.2126 * channel((n >> 16) & 255) + 0.7152 * channel((n >> 8) & 255) + 0.0722 * channel(n & 255);
};

const ratio = (a, b) => {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

const pairs = [
  ['text', 'bg', 4.5],
  ['text', 'surface-solid', 4.5],
  ['text', 'surface-2', 4.5],
  ['text-2', 'bg', 4.5],
  ['text-2', 'surface-solid', 4.5],
  ['text-2', 'surface-2', 4.5],
  ['text-3', 'bg', 4.5],
  ['text-3', 'surface-solid', 4.5],
  ['text-3', 'surface-2', 4.5],
  ['accent-text', 'bg', 4.5],
  ['accent-text', 'surface-solid', 4.5],
  ['accent-text', 'surface-2', 4.5],
  ['on-ember', 'ember', 4.5],
  ['on-ember', 'ember-hover', 4.5],
  ['success', 'bg', 4.5],
  ['success', 'surface-solid', 4.5],
  ['accent-text', 'bg', 3],
];

let failures = 0;
for (const [theme, tokens] of Object.entries(themes)) {
  for (const [fg, bg, min] of pairs) {
    const value = ratio(tokens[fg], tokens[bg]);
    const ok = value >= min;
    if (!ok) failures += 1;
    console.log(`${ok ? 'pass' : 'FAIL'} ${theme} ${fg} on ${bg} ${value.toFixed(2)} (min ${min})`);
  }
}

if (failures) {
  console.error(`${failures} contrast failures`);
  process.exit(1);
}
console.log('contrast ok');
