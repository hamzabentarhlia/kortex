# Layout report

Run on 15 November 2026 on the built output. Test suites: `scripts/test-layout.mjs` (23 checks, new), `test-alive.mjs` 46, `test-depth.mjs` 73, `test-interactive.mjs` 47, all passing.

## Diagnosis, confirmed

The split layout (heading left, content right) was applied by a CSS `:has()` rule to every section that had a heading, so card grids were squeezed into seven of twelve columns: audience cards near 200 px, "E-commerce" breaking mid-word, a wall of empty space under the heading. Before and after of the worst case, taken from production and from this build at 1440 px: `docs/audit/layout/before-home-who-title.webp` and `after-home-who-title.webp`.

## 1. The layout rule, rewritten

The build now decides per section and writes `data-layout="stack"` or `data-layout="split"` on it.

- **Stack (the default).** Index, heading and a standfirst of at most 60 characters across the top, content on the full width below. Applies to every section holding a card grid, tiers, facts, lab notes, the ladder, a strip, or the pinned pipeline.
- **Split.** Only a section with one visual or one block: the dashboard mockup, the demo, the source toggle, a comparison table, a FAQ, a heading with one card. It applies from 1200 px up, and alternates sides. Below 1200 px everything stacks, because seven of twelve columns is too narrow for a table at 1024.
- **Cards.** `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` on every grid and on the audience row. The wrapper is 1280 px wide, so four audience cards fit one row at 1440 px. `test-layout.mjs` measures every grid card on 25 templates at 375, 768, 1024, 1440 and 1920 px: none is narrower than 280 px, and none of the 125 page captures scrolls sideways.

Reflowed sections per template (split before, stack now):

| Template | Reflowed to heading on top, cards on the full width | Kept side by side (single visual or one block) |
|---|---|---|
| / | stack, geo, how, samples, trust, who, measure, plans, labnotes | demo, portal, faq |
| /how-it-works/ | steps, never, month, who-for | offsite, how-faq |
| /pricing/ | risk, stacks, calc2, ladder, every, calc, call | bars, pricing-faq, table, ways |
| /audit/ | audit-problem, audit-price, audit-flow | audit-included, audit-sample, audit-faq, audit-request |
| /about/ | - | - |
| /proof/ | proof-method, proof-log, proof-changes | - |
| /checklist/ | ck-list | ck-how, ck-bottom |
| /contact/ | - | form |
| /solutions/ | - | mix |
| /solutions/b2b/ | b2b-build | b2b-problem, mix, b2b-faq |
| /solutions/creators/ | cr-problem, cr-build | mix, cr-faq |
| /solutions/ecommerce/ | ec-build | ec-problem, mix, ec-faq |
| /solutions/from-a-blog/ | from-blog-assets, keep-exploring | from-blog-pull, from-blog-good, from-blog-faq |
| /solutions/from-youtube/ | from-youtube-assets, keep-exploring | from-youtube-pull, from-youtube-good, from-youtube-faq |
| /solutions/from-a-podcast/ | from-podcast-assets, keep-exploring | from-podcast-pull, from-podcast-good, from-podcast-faq |
| /solutions/from-a-webinar/ | from-webinar-assets, keep-exploring | from-webinar-pull, from-webinar-good, from-webinar-faq |
| /resources/ | res-blog, res-gloss, res-compare, res-td, res-method | - |
| /compare/ | - | - |

## 2. Type wrapping

`text-wrap: balance`, `hyphens: none` and `overflow-wrap: normal` on every heading and display number; card body text is at least 14 px at 1.5 line height (the asset cards use 14.4 px). The asset-card excerpts no longer wrap one word per line: the cards are 320 px wide, and the video script keeps its type size. The test asserts that no heading overflows its box on any template at any width.

## 3. Section rail

Rebuilt from scratch: no pill, no background, no border. Dots and mono numbers only, fixed to the right at 24 px, transparent. The active item shows its label to the left of the dot, right-aligned, from 1720 px up, where the margin has room. Between 1440 and 1719 px the label is the dot's tooltip and its accessible name, because the margin is 80 px wide and a label there would sit on the cards. Below 1440 px it is not rendered. It is hidden whenever the footer, an inverted band or a closing band is at the rail's height. `test-layout.mjs` scrolls home, how it works, pricing and audit at 1440 and 1920 px to four positions each, 19 visible states, and finds 0 overlaps with cards, tiers, figures or tables.

Screenshots at three scroll positions: `docs/audit/layout/rail-1440.webp` and `rail-1920.webp`.

## 4. Theme bleed

- Exactly one inverted band on each of the 139 indexed pages (counted in the built HTML), and the pricing test asserts it in both themes.
- The only hard-coded dark values in the stylesheets are inside the band rule itself; `grep` for the navy hex values outside `tokens.css` returns that one rule and nothing else. `color-scheme: dark` appears only in that rule and in the dark token set.
- `scripts/audit-layout.mjs` visits 22 templates at five widths in both themes (220 captures) and flags any opaque surface larger than 2,500 px² outside the band that is dark in a light page or light in a dark page, skipping images, SVG and canvas. Result: 0 flags and 0 horizontal overflows.
- I also looked at the contact sheets for both themes: no stray inverted card, input or strip.

## 5. More life

All additions are in `docs/audit/motion-inventory.md` (section "Added in the layout fix"), reduced-motion safe and readable without JavaScript.

- Card glow follows the cursor on every card, audience card and asset card (translate and opacity only); card entry stagger is 60 ms.
- "What you actually receive" is a row of five 320 px cards: drag with the mouse with inertia, native swipe on touch, scroll-snap, arrow keys, cards lift on grab. No library, 0.8 KB.
- Audience cards tilt, their icons draw themselves on first reveal, and the "For B2B" link underlines when the card is hovered.
- Every section heading highlights its last word with a 500 ms clip-path sweep.
- Fact counters roll like an odometer, captions fade up after the last digit lands.
- Comparison tables highlight the row on hover, the winning value turns ember with a hairline stroke (no weight change, so no layout shift), and the winning cell gets a check that draws on reveal.
- Signature moment, under 5 KB (0.4 KB of script, a few lines of CSS): the hero diagram floats in three layers that drift against the pointer, up to 4, 8 and 10 px, so the diagram feels like a mobile hanging in the page. A visitor would say "the hero reacts to my mouse". No proposal was needed.

## 6. Full screenshot pass

All 22 templates at 375, 768, 1024, 1440 and 1920 px in light and dark (220 captures), reviewed as contact sheets at 1024 and 1440 and spot-checked at 375. Found and fixed:

| Found | Fixed |
|---|---|
| Card grids squeezed into half the viewport | Stack layout, section 1 |
| Rail pill overflow and overlap with cards | Rail rebuilt, section 3 |
| Comparison table cramped in seven columns at 1024 px | Split applies from 1200 px only |
| Highlighter class collided with the pipeline's existing `.hl` class, which would have styled the headings as pipeline tracks | Renamed to `hl-mark` before shipping |
| A heading reported as overflowing | It was the visually hidden founder heading, excluded from the check |
| No other squeezed cards, clipped or overflowing text, rail collisions, theme bleed or horizontal scroll | None needed |

## 7. Checks

- Zero horizontal scroll: `document.documentElement.scrollWidth <= innerWidth` asserted on 25 templates at five widths, and on all 220 captures.
- Axe: 0 violations on 17 templates in both themes.
- Lighthouse mobile after: home 99, pricing 100, how it works 100; accessibility, best practices and SEO 100; CLS 0. Home was 99 to 100 across the previous runs, so this is unchanged.
- JavaScript on the home page: 8.8 KB `site.js` plus 1.4 KB `demo`, 1.4 KB `field`, 1.0 KB `homenav` and 0.8 KB `rowdrag`, 13.4 KB gzip against the 60 KB budget. The compiled stylesheet is 13.0 KB gzip.

## 8. Deploy

Merge the pull request, then check the home page at 1440 and 1920 px on production: the audience row, the asset row and the rail.
