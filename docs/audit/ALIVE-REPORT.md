# Alive report

Run on 15 November 2026 against a local gzip server, Chromium via Playwright. Suites: `scripts/test-alive.mjs` (36 checks), `scripts/test-depth.mjs` (73), `scripts/test-interactive.mjs` (47), all passing. Accessibility and overflow: `scripts/audit-depth.mjs`. The effect list is in `docs/audit/motion-inventory.md`.

## 1. Video and keyboard

- Scripted scroll-through with pointer movement, recorded as video: `docs/audit/screens/home-light.webm`, `home-dark.webm`, `how-it-works-light.webm`, `how-it-works-dark.webm`.
- Reduced-motion run of the same scroll on home, how it works and pricing: zero running transform, translate, scale, rotate or clip-path animations (peak 0 on all three), the inverted band is not animated, no console errors.
- Keyboard-only: slider, radios, chips, flip cards, rail, checklist, contact form, accordions, theme toggle and the blog search (Enter focuses the first result) are covered in `test-depth.mjs`.
- Console errors: none on 17 templates.
- Contact form POST intercept: the test fills the form, intercepts the Pageclip request, asserts that empty or invalid fields block the send with inline messages, that a valid submit posts once, and that the inline success state names the next step and offers the checklist, with no redirect and no alert.

## 2. Screenshots

All 17 templates at 375, 768 and 1440 px in light and dark (102 images): `docs/audit/screens-alive/`. I looked at them: no horizontal overflow at any width, no clipped display type, the inverted band is legible in both themes (navy on light pages, a darker navy on dark pages), and the footer wordmark fits the viewport width.

Before and after, full page, 1440 px light, in `docs/audit/screens/`: `before-` and `after-` for home, pricing, how-it-works, article, about and audit.

## 3. JSON-LD

`scripts/validate-jsonld.mjs` runs in `scripts/build.sh` and fails on parse errors, empty required fields, FAQ text drift against the visible FAQ, and missing per-template types. Result: 199 pages, 192 blocks, 0 errors.

| Template | Types |
|---|---|
| Every page | Organization (name, url, logo, sameAs LinkedIn), WebSite, WebPage, BreadcrumbList |
| Home | Person (founder), Service with three Offers (2,500, 5,500, 12,000 EUR), FAQPage |
| Pricing | Service with three Offers, FAQPage |
| Audit | Service with an Offer at 490 EUR, FAQPage |
| About | Person (jobTitle Founder, sameAs LinkedIn) |
| How it works | FAQPage |
| Articles, teardowns | BlogPosting (author Person with jobTitle), BreadcrumbList, FAQPage where a FAQ is visible |
| Glossary hub | CollectionPage, DefinedTermSet |
| Term pages | DefinedTerm |
| Blog, compare, solutions, teardowns, resources hubs | CollectionPage (with an ItemList where the hub lists pages) |

The only profile found in the repository is the founder's LinkedIn page, so it is the only `sameAs` entry.

## 4. Bundles and Lighthouse

Total JavaScript per page is `site.js` (8.5 KB gzip) plus the modules that page loads. Largest page: home at 11.9 KB. Everything on the site combined: 21.4 KB. Budget: 60 KB. Compiled stylesheet: 12.0 KB gzip.

| Page | Modules | JS gzip | HTML gzip |
|---|---|---|---|
| `/` | demo, field, homenav | 11.9 KB | 36.3 KB |
| `/pricing/` | calc, homenav, pricing | 11.5 KB | 27.8 KB |
| `/checklist/` | checks, homenav | 10.1 KB | 18.3 KB |
| `/404.html` | field | 9.7 KB | 14.5 KB |
| Article, teardown | article | 9.6 KB | 23.6 to 28.4 KB |
| Compare page | verdict | 9.4 KB | 20.6 KB |
| `/blog/` | blogidx | 9.4 KB | 40.0 KB |
| `/glossary/` | glossary | 9.2 KB | 26.6 KB |
| `/contact/` | fields | 9.1 KB | 18.2 KB |
| How it works, audit, about, proof | homenav | 9.1 KB | 17.2 to 24.8 KB |
| `/solutions/` | mix | 8.6 KB | 22.5 KB |
| Glossary term | none | 8.3 KB | 22.0 KB |

Lighthouse mobile, Performance, Accessibility, Best practices, SEO, then LCP, TBT, CLS. Before is `main` at the start of this work.

| Page | Before | After |
|---|---|---|
| `/` | 92 100 100 100, 2.2 s, 220 ms, 0 | 100 100 100 100, 1.5 s, 30 ms, 0 |
| `/pricing/` | 100 100 100 100, 1.5 s, 20 ms, 0 | 100 100 100 100, 1.5 s, 10 ms, 0 |
| Article | 100 100 100 100, 1.5 s, 0 ms, 0 | 100 100 100 100, 1.5 s, 0 ms, 0 |
| `/how-it-works/` | 100 100 100 100, 1.5 s, 0 ms, 0 | 100 100 100 100, 1.5 s, 0 ms, 0 |

The layout CSS is inlined in the document head, so the redesign adds no layout shift: CLS is 0 on all four. Axe (WCAG 2 A and AA, best practice): 0 violations on 17 templates in both themes.

## 5. Curl matrix

Full table: `docs/audit/curl-matrix-alive-2026-11-15.md`. 284 requests.

| Check | Result |
|---|---|
| Apex `https://kortexlab.me/`, `/pricing/`, `/login/` | 301 to the www URL (live) |
| www slashed routes | 200, self canonical, no mismatches |
| `/login/`, `/fr/login/` | `noindex, nofollow` meta; `X-Robots-Tag` is set in `deploy/nginx-kortexlab.conf` (GitHub Pages cannot send headers) |
| `robots.txt`, `sitemap.xml` | 200, no Arabic URLs in the sitemap |
| Public pages with noindex | none |
| hreflang, EN and FR | 139 URLs checked, 0 errors, every cluster reciprocal with `x-default` on the English page |

The local server does not emulate GitHub Pages redirects for unslashed URLs, which production answers with a 301. Rerun `scripts/curl-matrix.sh` against production after the merge.

## 6. Greps

No TODO, FIXME, lorem, `href="#"`, unresolved macro or bracket placeholder in the built pages. No `ar_MA` alternate on any indexable page. No `gean` or `Ricordati` outside the deindex checklist and the earlier report.

## 7. What changed

Language: the French tree is complete and current (every English page has a French page, apart from the podcast article), so it is surfaced: switcher in the header and footer, reciprocal hreflang with `x-default`, `og:locale fr_FR`. The `/ar/` tree turned out to be live, an older subset of 26 pages. It is now behind `"arabic": false` in `data/site.json`: its URLs still answer, but the pages are `noindex`, out of the sitemap, out of hreflang and out of the switcher, and the "3 languages" counter reads 2. Set the flag to true and rebuild to bring it back.

Per template, in one line each:

- Home: full-width display headline, asymmetric 12-column sections, navy inverted band for the SEO against GEO shift, five-figure fact row at display size, section dots, stack strip, giant footer wordmark.
- How it works: left section rail with mono indexes, inverted band for the human-review rules, typed stage logs, pinned stages unchanged.
- Pricing: offer ladder in an inverted band before the FAQ, audit as the secondary header CTA, call copy rewritten (3 questions live, 40 in the audit), sticky plan bar.
- Audit, about, proof, checklist: left rail, one inverted band each, mono section indexes.
- Blog index, glossary, compare index, resources, solutions hub: asymmetric hero, tools and filters on the new grid, inverted band on the closing call to action or the source toggle.
- Article, teardown: left contents rail in mono with a sliding indicator, progress bar, inverted closing band.
- Glossary term, compare page, audience pages: same grid, related-terms map and verdict slider kept.
- Contact: floating labels, inline success and error states.
- 404: canvas, one line, three links, Arabic card removed.
- Footer, every page: language switcher, four mono-labeled columns, newsletter, wordmark at 6 percent, "Built in Fès. Runs on n8n, Whisper, Gemini, Odoo."

## 8. Needs a human

1. Bing Webmaster and Search Console: run the removal and re-crawl in `docs/deindex-gean.md`. Owner only.
2. Confirm the Arabic decision. The `/ar/` pages existed and were live, so hiding them is a change from the current state. If any of them is meant to stay indexed, set `"arabic": true`.
3. First real 40-question run for `/proof/`.
4. Verify the citation-teaser entries, then set `citationTeaser: true`.
5. Send a real contact-form submission and confirm receipt. The Pageclip endpoint cannot be reached from the build environment, so the live receipt is unverified. The action URL and the honeypot are in the markup.
6. Confirm that Whisper and Gemini belong in the footer stack line. It follows your brief. Gemini appears elsewhere only as an engine we test, and Whisper appears nowhere else on the site.

## 9. Deploy and rollback

Deploy: merge the pull request. GitHub Pages serves the committed output, so there is no host-side build. Then run `scripts/curl-matrix.sh` against production and resubmit the sitemap in both webmaster tools.

Rollback: revert the merge commit on `main` and push. To bring Arabic back without a revert, set `"arabic": true` in `data/site.json` and rebuild.
