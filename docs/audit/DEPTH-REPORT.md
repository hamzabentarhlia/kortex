# Depth report

Run on 14 November 2026. Browser checks with Playwright (Chromium) against a local gzip server. Suites: `scripts/test-depth.mjs` (71 checks) and `scripts/test-interactive.mjs` (47 checks), both passing. Accessibility and overflow: `scripts/audit-depth.mjs`.

## 1. Index hygiene and the "Gean" result

What it was: nothing in this repository contains it. A search of source, data and built pages for `gean`, `Ricordati`, `cominciare` and `AdminLTE` finds nothing. The Italian strings are those of an admin-style login page, so it is almost certainly an app that was once served from a different host at the apex. The live apex is served by GitHub Pages, not by a server with its own configuration (`server: GitHub.com`), so there was no vhost in this repository to remove.

What was done:

- Live check of the apex: `curl -sI https://kortexlab.me/` returns `301` with `location: https://www.kortexlab.me/`, and the same for `/pricing/` and `/login/`.
- `deploy/nginx-kortexlab.conf` written as the authoritative config for any server that still answers a request for this domain or its IP: a `default_server` catch-all on 80 and 443 that 301s to `https://www.kortexlab.me$request_uri` with `X-Robots-Tag: noindex, nofollow`, the apex redirect, HSTS and the security headers, and `X-Robots-Tag` on `/login/`. It is a contingency: GitHub Pages cannot send response headers.
- Login pages now carry `noindex, nofollow` (was `noindex, follow`), stay out of the sitemap, and `robots.txt` no longer disallows them, because a crawler that is blocked from a page cannot read its noindex tag.
- `docs/deindex-gean.md`: the owner checklist (DNS records, Bing URL Inspection and Block URLs, Search Console URL Inspection and Removals, the 7 to 14 day check) and the curl commands that prove the fix.

The remaining fix is in the index and possibly in DNS, and only the owner can do it.

## 2. Curl matrix

Full tables: `docs/audit/curl-matrix-live-2026-11-14.md` (production, before this branch) and `docs/audit/curl-matrix-build-2026-11-14.md` (this build on the local server).

| Check | Production, 154 sitemap URLs | This build, 183 sitemap URLs |
|---|---|---|
| Apex `https://kortexlab.me/`, `/pricing/`, `/login/` | 301 to the www URL | not applicable locally |
| Slashed URL | 200, self canonical, index and follow (default) | 200, self canonical |
| Unslashed URL | 301 to the slashed URL, all 154 | the local server does not emulate GitHub Pages redirects, recheck live after merge |
| Public pages with noindex | none | none |
| Login pages | `noindex, follow` | `noindex, nofollow` |
| `robots.txt`, `sitemap.xml` | 200 | 200 |
| Canonical mismatches | 0 | 0 |

HTTP (not HTTPS) probes cannot be made from this environment. Run `scripts/curl-matrix.sh` against production after the merge.

## 3. Interactive elements per page

| Page | What the visitor can do |
|---|---|
| Home | Pipeline demo, citation teaser (flag), section dots that appear after the hero with active state, lab notes strip with the latest three pieces, stack strip, hero word reveal and field canvas |
| How it works | Existing pinned scroll pipeline checked: progress follows the scroll, five stages, static and unpinned under reduced motion. Typing log lines were not added |
| Pricing | Calculator, compare toggle that dims identical rows, sticky mobile bar that shows the selected plan, animated FAQ |
| Blog index | Category filter chips (anchors without JS), search over titles and descriptions from a 5.7 KB JSON index, freshness and reading-time badges, featured latest post |
| Blog posts | Progress bar, sticky contents rail, pull quotes, expandable asides, newer and older tiles with cover reveal |
| Glossary | Sticky A to Z rail with active letter, flip cards for why a term matters for citations |
| Glossary terms | Related-terms map in inline SVG with hover highlight, plain list on small screens |
| Compare pages | Verdict slider between the other option and KORTEX, sticky table header |
| Solutions | Source toggle (blog, video, podcast, webinar) that swaps what we pull out and what it becomes, from the real service pages. Worked examples added for creators and e-commerce |
| About | Photo in ink, full colour on hover or focus. The existing scroll-driven path is kept (vertical, not horizontal) |
| Proof | Changelog rows stagger in, methodology steps draw their number rings |
| Checklist | 27 checks tickable in memory, live count, score bands pointing to the call or the audit |
| Contact | Floating labels, inline validation in voice, success page that names the next step and offers the checklist |
| 404 | Field canvas, one line in voice and three links |

Left out: the giant footer wordmark, removed at your request after it rendered at full opacity. The audit page has no tickable list, since the 27 checks live on the checklist page.

## 4. Bundle sizes, gzip

Total JavaScript loaded per page is `site.js` (8,281 B) plus the modules that page uses. Largest page: home at 11.3 KB. Everything on the site combined is about 24 KB. Budget: 45 KB.

| Page | Modules | Total |
|---|---|---|
| `/` | demo, field, homenav | 11.3 KB |
| `/pricing/` | calc, pricing | 10.4 KB |
| `/404.html` | field | 9.4 KB |
| `/blog/` | blogidx | 9.1 KB |
| Blog post, teardown | article | 9.3 KB |
| `/glossary/` | glossary | 8.9 KB |
| Compare page | verdict | 9.2 KB |
| `/solutions/` | mix | 8.4 KB |
| `/checklist/` | checks | 9.0 KB |
| `/contact/` | fields | 8.8 KB |
| How it works, about, proof, audit, term pages | none | 8.1 KB |

## 5. Lighthouse, mobile

Performance, Accessibility, Best practices, SEO, then LCP, TBT and CLS. Before is the build on `main` at the start of this work.

| Page | Before | After |
|---|---|---|
| `/` | 98 100 100 100, 1.5 s, 170 ms, 0 | 99 100 100 100, 1.7 s, 60 ms, 0 |
| `/how-it-works/` | 100 100 100 100, 1.5 s, 0 ms, 0 | 100 100 100 100, 1.5 s, 20 ms, 0.005 |
| `/pricing/` | 100 100 100 100, 1.7 s, 20 ms, 0 | 100 100 100 100, 1.5 s, 0 ms, 0 |
| `/blog/` | 100 100 100 100, 1.5 s, 50 ms, 0 | 100 100 100 100, 1.5 s, 40 ms, 0 |
| Blog post (entity-first) | 99 100 100 100, 1.7 s, 110 ms, 0 | 99 100 100 100, 1.7 s, 110 ms, 0 |
| `/glossary/entity/` | 100 100 100 100, 1.5 s, 0 ms, 0 | 100 100 100 100, 1.7 s, 0 ms, 0 |
| Compare page | 100 100 100 100, 1.5 s, 0 ms, 0 | 100 100 100 100, 1.5 s, 0 ms, 0 |

One run of `/glossary/entity/` read CLS 0.112 on the in-short box. Four reruns across term pages, including that one, read 0. The first reading was not reproduced and is reported here for completeness.

Axe (WCAG 2 A and AA, best practice) on 17 templates at 1440 px in light and dark: 0 violations. Horizontal overflow at 375, 768 and 1440 px in both schemes: none.

## 6. Structured data

`scripts/validate-jsonld.mjs`: 199 pages, 192 JSON-LD blocks, 0 errors. FAQ markup is extracted from the visible FAQ on each page and compared with it. Each glossary entry carries `DefinedTerm` markup. `scripts/check-hreflang.mjs`: 183 URLs, 0 errors.

## 7. Links

- Internal: 14,721 links across the sitemap resolve to a built page, 0 broken.
- External sources in articles and glossary: 18 of 19 distinct links answer 200. LinkedIn does not answer from this environment. The Cal.com booking links cannot be reached from this environment either, so they are unchecked here.
- Link map: `docs/audit/link-map.md`. English and French content pages all have at least three inbound and three outbound links. 17 Arabic content pages, which were not part of this work, sit at one or two inbound links. `/resources/`, `/contact/` and the cookies page are reached from the navigation and footer only.

## 8. Greps

No TODO, FIXME, lorem, `href="#"`, unresolved macro or bracket placeholder in the built pages or the source. No `gean` or `Ricordati` outside the deindex checklist. No code comments in the new scripts or styles. None of the banned words and no exclamation marks in the new articles, terms or teardowns.

## 9. Content shipped

Articles (English): `entity-seo-for-founders`, `agency-vs-in-house-vs-ai-studio`, `repurposing-mistakes-that-kill-authority`, `human-qa-layer`, `podcast-to-authority`, `geo-in-french-and-arabic`, 1,400 to 1,550 words each. French versions of five of them (all except the podcast piece), 1,500 to 1,650 words. Four queue articles were already published and are unchanged: `get-cited-by-chatgpt-perplexity-gemini`, `schema-markup-ai-engines-read`, `measure-ai-citations`, `llms-txt-what-to-do`.

Glossary: nine new terms in both languages, 22 in total: citation, zero-click search, knowledge graph, hreflang, content decay, information gain, grounding, prompt-level demand, share of model.

Compare: all four comparison cards link to full pages. The brief's `kortex-vs-hiring-an-agency` is covered by the existing `kortex-vs-seo-agency`, and `kortex-vs-in-house-writer` already existed. A second agency page would compete with the first for the same query, so none was added.

Teardown 1 is live in production with its screenshots, now annotated with numbered pins. Teardown 2 is outlined in `docs/teardown-2-outline.md`. The `/resources/` hub lists every new piece.

Sources for the articles were fetched directly (curl), because the page-fetch tool could not resolve developers.google.com in this session. Each claim attributed to Google appears in the page text that was read.

## 10. Needs a human

1. Run the steps in `docs/deindex-gean.md` in Bing Webmaster Tools and Search Console. Only the owner can request removal and re-crawl.
2. Check DNS for the apex and every hostname. If any record still points at an old server, remove it or apply `deploy/nginx-kortexlab.conf` there, and say whether the Gean app is still needed anywhere. If so, give it a separate hostname behind basic auth.
3. Approve the teardown 2 subject in `docs/teardown-2-outline.md`.
4. Provide the first real citation-log data for `/proof/`.
5. Confirm the VAT position of the plan prices before the pricing page is changed.

## 11. Deploy and rollback

Deploy: merge the pull request. GitHub Pages serves the committed output, so there is no host-side build. To rebuild locally: `scripts/build.sh`. After the merge, run `scripts/curl-matrix.sh` against production and resubmit the sitemap in both webmaster tools.

Rollback: revert the merge commit on `main` and push.
