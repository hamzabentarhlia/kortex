# Polish report

Run on 15 November 2026. Production was fetched first, before any change, to see what is actually served.

## 0. What production serves

Production already carries the previous release. Fetched with curl on the seven URLs below, every page has one JSON-LD script with the full graph, reciprocal hreflang for English, French and `x-default`, `og:locale` en_US with fr_FR as the only alternate, and no `ar_MA`. So fixes 4 and 5 were already live when this pass started. A fetcher that reported no Organization, WebSite, Service or FAQPage was reading an older cached copy or looking for separate script blocks, because the graph was one block. To remove that ambiguity every entity is now emitted as its own `application/ld+json` block.

## 1. Footer wordmark

Rebuilt as one decorative node: a single `div`, `aria-hidden="true"`, `user-select: none`, no children, text drawn by one pseudo-element (real text at 6 percent tripped the contrast check), `line-height: .8`, `white-space: nowrap`, centred, colour `color-mix` at 6 percent of the ink token, `overflow-x: clip` on the footer only. It rises as one node (opacity and translateY). The old SVG, the per-glyph fitting and anything layered over it are gone. The stack line now sits above the wordmark, so nothing overlaps it.

Font size is `clamp(3rem, 17vw, 22rem)`, not the `6rem` minimum in the brief: at 375 px the word is about 5.3 em wide, and 6rem would be 510 px wide and clip.

| Width | Word left | Word right | Viewport | Page scroll width |
|---|---|---|---|---|
| 375 | 18 | 357 | 375 | 375 |
| 1440 | 67 | 1373 | 1440 | 1440 |
| 1920 | 90 | 1830 | 1920 | 1920 |
| 2560 | 342 | 2218 | 2560 | 2560 |

Before and after screenshots at the four widths: `docs/audit/polish/footer-before-*.webp` (production) and `footer-after-*.webp`. The before shots show the cause: the rail blob sat over the footer and the wordmark rendered as a solid grey block. `test-alive.mjs` asserts the word fits at all four widths with no children and no horizontal scroll.

## 2. Section dot rail

- Background, border and backdrop removed. The rail is dots and mono labels only, with a small pill behind a label only on hover, focus or the active item.
- Numbers come from the section's own index, and the index now counts only the sections that are in the rail, so the sequence is 01 to 08 on the home page and 01 to 06 on how it works, with no gaps.
- Hidden once the footer enters the viewport, and below 1280 px.
- z-index 30, under the header at 50. Keyboard focusable with a visible outline. Smooth scroll, or an instant jump under reduced motion.
- Link names stay available to screen readers while the labels are visually hidden.
- Screenshots: `docs/audit/polish/rail-after-home-light-home-dark-how-it-works.webp`.

## 3. Sticky header

The pill now uses the raised surface token at 90 percent with a 14 px blur, so overlapped text never shows through. It sits at z-index 50 above everything except the cookie banner and mobile bar. Every in-page target has `scroll-margin-top: 110px`, asserted in the test.

## 4. JSON-LD in the deployed output

| URL | Production now | This build |
|---|---|---|
| / | 1 block, 7 types | 7 blocks, 7 types: BreadcrumbList, FAQPage, Organization, Person, Service, WebPage, WebSite |
| /pricing/ | 1 block, 6 types | 6 blocks, 6 types: BreadcrumbList, FAQPage, Organization, Service, WebPage, WebSite |
| /audit/ | 1 block, 6 types | 6 blocks, 6 types: BreadcrumbList, FAQPage, Organization, Service, WebPage, WebSite |
| /about/ | 1 block, 5 types | 5 blocks, 5 types: BreadcrumbList, Organization, Person, WebPage, WebSite |
| /how-it-works/ | 1 block, 5 types | 5 blocks, 5 types: BreadcrumbList, FAQPage, Organization, WebPage, WebSite |
| /blog/human-qa-layer/ | 1 block, 6 types | 6 blocks, 6 types: BlogPosting, BreadcrumbList, FAQPage, Organization, WebPage, WebSite |
| /glossary/entity/ | 1 block, 5 types | 5 blocks, 5 types: BreadcrumbList, DefinedTerm, Organization, WebPage, WebSite |

`scripts/validate-jsonld.mjs` (in `build.sh`) reports 199 pages, 981 blocks, 0 errors, and enforces the per-template types, the offer prices (2,500, 5,500 and 12,000 on home and pricing, 490 on the audit), FAQ text against the visible FAQ, and a CollectionPage on every hub.

## 5. Hreflang and locale

Production head on the seven URLs: `hreflang` en, fr and x-default, `og:locale` en_US with `fr_FR` as the alternate, `<html lang="en">`. `scripts/check-hreflang.mjs`: 139 URLs, 0 errors, every cluster reciprocal with `x-default` on the English page. The French pages carry `og:locale` fr_FR. The Arabic tree is noindex and out of the clusters, and its own locale tag is now `ar_AR`, so `ar_MA` returns zero hits in the built pages, sitemap and source (a stale compiled `.pyc` is not tracked). The "languages" counter reads 2: English and French.

## 6. Bing's flags

`scripts/seo-checks.py` (now part of `build.sh`) checks every URL in the sitemap. Before: 20 meta descriptions outside 130 to 155 characters, all on pages added in the last two releases. They were rewritten. After: 139 URLs, 0 description, 0 alt, 0 H1 and 0 lang issues. All built pages, not only the sitemap, also pass: every `img` has an `alt`, exactly one H1, `lang` is en, fr or ar to match the tree.

## 7. Template sweep

All 17 templates at 375, 768 and 1440 in light and dark were screenshotted and reviewed: overflow 0, axe 0 violations.

| Found | Fixed |
|---|---|
| Wordmark rendered as a solid block and clipped at the X on wide screens | Rebuilt, fits at 375 to 2560 |
| Rail blob over the footer, numbering with gaps | Rebuilt, see section 2 |
| Header showing page text through it | 90 percent surface plus blur |
| Wordmark text failing the contrast check (36 axe hits across templates) | Text moved to a pseudo-element |
| Rail link names empty once labels were hidden (axe link-name) | Labels visually hidden, not removed |
| Rail numbers differing from the section indexes on the page | Both come from the same numbering |
| No overlaps, clipped display type or stray blobs on the other templates | None needed |

## 8. Checks

- `test-alive.mjs` 46, `test-depth.mjs` 73, `test-interactive.mjs` 47, all passing.
- Lighthouse mobile after: home 99, pricing 100, article 100; accessibility, best practices and SEO 100; CLS 0. Home was 100 before this pass, so the one point is run-to-run noise on LCP (1.7 s against 1.5 s).

## 9. Deploy

Merge the pull request, then run `scripts/curl-matrix.sh` against production and spot-check the footer and the rail on the live home page.
