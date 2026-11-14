# Interactive layer report

Run against the built site on a local gzip-enabled server, Chromium via Playwright, 14 November 2026. Test suite: `scripts/test-interactive.mjs` (run `node scripts/test-interactive.mjs`, add `--teaser` with the teaser flag on, `--shots=<dir>` for screenshots). Result of the last run: 47 passed, 0 failed. With the teaser flag temporarily on and test entries marked verified: 62 passed, 0 failed. The flag and the entries were then restored to off and unverified.

## New interactive blocks

| Block | Where | Without JavaScript |
|---|---|---|
| Pipeline demo, four sample sources, five stages, eight asset cards | `/`, `/fr/` | Final state is in the HTML: five stages with logs, eight native `details` cards, labelled "Example". Run button is hidden. |
| Cost calculator, three sliders and one select, live result | `/pricing/`, `/fr/pricing/` | Default result is computed at build time with the same formula and rounding: EUR 4,040 against SWARM EUR 5,500, with the verdict line. |
| Citation teaser | `/`, `/audit/` and French equivalents, behind the `citationTeaser` flag | Static definition list of the questions and the sources by type. Hidden entirely while the flag is off. |
| Neural field canvas | home hero | Decorative, absent without JavaScript. Frozen single frame under reduced motion. |
| Article progress bar and contents rail | every blog article and teardown | Article reads normally. Rail shows at 1320 px and wider, after at least three section headings. |
| Hero headline word reveal | home | Headline is plain text. No split under reduced motion. |
| Stack strip (marquee) | home | Static row of chips. |
| Lab notes strip | home | Static cards, built from the three latest dated articles and teardowns. |

Motion items already shipped before this mission and left as they were: scroll reveals, counters, link underline draw, nav indicator, magnetic buttons, cursor glow, view transitions. Changed in this mission: plan-card tilt to 4 degrees, dividers to ink at 14 percent, theme toggle morph at 240 ms with a 240 ms colour cross-fade, FAQ open and close animation.

## Calculator test cases

Expected values were computed by hand from the formula: production = assets x rate, time = round(hours x 52 / 12 x value), plan by assets (up to 10 GHOST, 11 to 24 SWARM, 25 or more TITAN).

| # | Assets | EUR per asset | Hours per week | EUR per hour | Expected current cost | Expected plan | Result |
|---|---|---|---|---|---|---|---|
| 1 | 12 | 250 | 4 | 60 | 4,040 | SWARM 5,500, costs more | pass |
| 2 | 4 | 50 | 0 | 30 | 200 | GHOST 2,500, costs more | pass |
| 3 | 10 | 300 | 2 | 100 | 3,867 | GHOST 2,500, about 1,367 less | pass |
| 4 | 11 | 600 | 10 | 100 | 10,933 | SWARM 5,500, about 5,433 less | pass |
| 5 | 24 | 400 | 20 | 100 | 18,267 | SWARM 5,500, about 12,767 less | pass |
| 6 | 25 | 300 | 8 | 60 | 9,580 | TITAN from 12,000, scope set on a call | pass |

The booking link carries the plan in the notes field (case 6 gives TITAN). French render checked: `4 040 €`.

## Bundle sizes, gzip

| File | Loaded | Gzip |
|---|---|---|
| `site.js` (was 7,874 B) | every page | 8,275 B (+401 B) |
| `demo.js` | home, when the block nears the viewport | 1,185 B |
| `calc.js` | pricing, when the block nears the viewport | 1,301 B |
| `teaser.js` | only when the flag is on | 718 B |
| `field.js` | home hero | 1,403 B |
| `article.js` | articles and teardowns | 1,282 B |
| **New JavaScript in total** | | **6,290 B, about 6.1 KB** |

Budget was 30 KB. Added per-block CSS (inlined only on the pages that use it): demo 1,628 B, calculator 776 B, teaser 879 B gzip.

## Lighthouse, mobile

Scores are Performance, Accessibility, Best practices, SEO. "Before" is the build on `main` before this mission, "after" is this branch.

| Page | Before | After | LCP | TBT | CLS |
|---|---|---|---|---|---|
| `/` | 98 100 100 100 | 98 100 100 100 | 1.5 s to 1.5 s | 140 ms to 140 ms | 0 to 0.003 |
| `/pricing/` | 100 100 100 100 | 100 100 100 100 | 1.5 s to 1.5 s | 0 ms to 10 ms | 0 to 0 |
| `/audit/` | not measured | 100 100 100 100 | 1.4 s | 0 ms | 0 |
| `/teardowns/our-pricing-page/` | new page | 100 100 100 100 | 1.5 s | 30 ms | 0 |
| `/fr/` | not measured | 100 100 100 100 | 1.5 s | 30 ms | 0 |

One regression caught and fixed on the way: the footer wordmark first failed the colour contrast check on both pages (accessibility 97 and 96). It is now drawn from a pseudo-element on an `aria-hidden` element, and accessibility is back at 100.

## Checks

- Keyboard only: source radios move with the arrow keys, Tab reaches Run, Enter starts it, a card opens with Enter, sliders move with Home and the arrow keys, the result is an `aria-live="polite"` region, the teaser select and skip button work from the keyboard.
- Reduced motion: demo jumps to the final state at once, canvas frame does not change over 700 ms, no headline split, no animation on the accordions or the theme morph.
- JavaScript disabled: calculator defaults and verdict present, demo stages and eight cards present, run button hidden.
- Console errors: none on `/`, `/pricing/`, `/audit/`, `/teardowns/`, the teardown, a blog article, and the French home, pricing and teardown.
- Teaser (flag temporarily on): select shows the answer, the punchline arrives within 2.2 s, skip works, the form submit was intercepted and posted to the Pageclip endpoint, on `/`, `/audit/` and `/fr/audit/`. Build gate verified: with the flag on and any entry unverified the build exits with the list of entries.
- Greps over source, data and the key built pages: no TODO, FIXME or lorem, no unresolved macros or bracket placeholders, no `href="#"`, no code comments in the new scripts or styles.
- Content in the raw HTML (curl, no rendering): "Your current monthly cost", "EUR 4,040" and the verdict on `/pricing/`; "Extract", "Human review", eight `dc` cards and "Lab notes" on `/`.

## Screenshots

`docs/audit/screens-interactive/`: home, pricing, audit and the teardown at 375, 768 and 1440 px in light and dark, plus reduced-motion and JavaScript-disabled sets at 1440 px. Home and pricing are scrolled to the demo and the calculator.

## New content

- `/teardowns/` and `/fr/teardowns/` (hub)
- `/teardowns/our-pricing-page/` and `/fr/teardowns/our-pricing-page/` (teardown 1, with real screenshots and counts from the built page)
- Lab notes strip on the home page, newest first from the dated articles and teardowns
- Changelog on `/proof/`, one new dated entry
- Articles `geo-vs-seo-for-b2b` and `webinar-to-content-system` were already published and are unchanged

## Needs a human

1. Verify all 16 teaser entries in ChatGPT and Perplexity, enter the engine and date for each, set `verified` to true in `data/citation-teaser.json`, then set `citationTeaser` to true in `data/site.json`. The build refuses to publish the teaser until this is done.
2. The teaser form promises a free single-question run in 3 business days. The brief asked for that wording, but it sits next to the paid audit. Decide whether to keep it.
3. Approve teardown 1. It is about our own page, because no third-party page was captured. Replace or add a third-party teardown only with the owner's agreement.
4. Confirm the calculator defaults: EUR 250 per asset and EUR 60 per hour.
5. The teardown lists three changes we have not made yet: a VAT line on pricing, a link from pricing to the proof page, and a price summary at the top. Confirm the VAT facts before the first.

## Deploy and rollback

Deploy: merge the pull request into `main`. GitHub Pages serves the committed output at the repository root, so there is no separate build step on the host. To rebuild locally: `scripts/build.sh`.

Rollback: revert the merge commit on `main` and push. Switching the teaser off at any time needs only `citationTeaser: false` in `data/site.json` and a rebuild.
