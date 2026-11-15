# Motion inventory

Every effect that ships. Easing `out` is `cubic-bezier(.22,1,.36,1)`, `ease` is `cubic-bezier(.2,.7,.2,1)`. Under `prefers-reduced-motion: reduce` every row marked "removed" renders its final state at once, and `scripts/test-alive.mjs` asserts that no transform, translate, scale, rotate or clip-path animation runs while scrolling the home page, how it works and pricing.

## Entry

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| Home and every page with a display headline | Mono eyebrow | Load, first page of the session | opacity | 500 ms, out | Removed |
| Same | Headline words (split at build time) | Load, first page of the session | opacity, transform (rise 24 px) | 620 ms each, 60 ms stagger, first 10 words | Removed |
| Same | Ember phrase (`chip-word`) | Load, after the last word | opacity, transform | 620 ms, starts at 780 ms | Removed |
| Same | Lead paragraph | Load | opacity, transform (14 px) | 600 ms, delay 560 ms, out | Removed |
| Same | Buttons and note | Load | opacity, transform (14 px) | 600 ms, delay 700 ms, out | Removed |
| Every page | Header | Load | opacity, transform (14 px) | 700 ms, delay 300 ms, out | Removed |
| Home, 404 | Field canvas | Load | opacity | 1,100 ms, delay 600 ms, out | Removed, one frozen frame |
| Every page after the first | None of the above | Navigation | `html.no-entry` skips the sequence | - | - |
| Every page | Page cross-fade | Navigation | View Transitions, UA cross-fade | 280 ms | Browser default, removed by the OS setting |

## Scroll

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| All | Section heads, tables, FAQs, answer blocks | Enters viewport (observer) | opacity, transform (rise 16 px) | 380 ms, ease, once | Removed |
| All | Visual blocks (`.vx`) | Enters viewport | opacity, transform (40 px), 80 ms after the text | 380 ms, ease, once | Removed |
| All | Visual blocks (`.vx`) | Scroll position (CSS `view()`, where supported) | translate, 8 px drift each way | linear | Removed |
| Every page with an inverted band, including closing bands | Inverted band | Scroll position (CSS `view()`, where supported) | clip-path inset wipe from the bottom | linear, entry 0 to 60% | Removed |
| All | Section rule | Scroll position (CSS `view()`, where supported) | transform scaleX, left to right (right to left in RTL) | linear, entry 0 to 45% | Removed |
| All with section numbers | Mono section index | Enters viewport | text ticks from 00 to the number | about 400 ms, 45 ms steps, once | Removed |
| Home | Fact counters | Enters viewport | text counts from 0 to the number, tabular numerals, plus a pop (opacity, transform 6 px) | 700 ms, ease-out cubic, once | Final number at once |
| All with card groups | Card stagger | Enters viewport | opacity, transform (10 px) | 380 ms, 40 ms stagger | Removed |
| Proof | Changelog and log rows | Enters viewport | opacity, transform | 380 ms, 40 ms stagger | Removed |
| Proof | Methodology number rings | Enters viewport | stroke-dashoffset | 900 ms, out, 120 ms stagger | Removed |
| Articles, teardowns | Reading progress bar | Scroll | transform scaleX | scroll-linked | Removed |
| Articles, teardowns | Contents rail indicator | Active heading changes | transform translateY | 360 ms, out | Instant |
| How it works, about, pricing, proof, audit, checklist | Left section rail | Active section changes | border and number colour change, no movement | none | None |
| Home | Section dots | Active section changes | dot transform scale, label opacity | 180 ms to 360 ms | Instant |
| Blog posts | Newer and older tiles | Enters viewport | clip-path (cover reveal) | 700 ms, out | Removed |
| Footer | KORTEX wordmark | Enters viewport | opacity, transform (10 px) | 380 ms, ease, once | Removed |

## Pipeline

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| Home | Pipeline demo run | In view at 55% once, or the Run button | stage nodes light in sequence, connecting line draws (stroke-dashoffset), eight cards deal | 600 ms per stage, 700 ms line, 80 ms per card | Final state at once |
| Home | Demo log lines | Each stage as it lights | text types in, height reserved | 16 ms per two characters | Final text at once |
| How it works | Five stages | Scroll | existing sticky pin, native scroll speed, rail fills with scroll position | scroll-linked | Unpinned, all stages open |
| How it works | Stage log lines | Enters viewport | text types in, height reserved | 18 ms per two characters | Final text at once |

## Rest

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| Home, 404 | Field canvas nodes | Always, with pointer gravity within 170 px on a fine pointer | canvas pixels, redrawn with requestAnimationFrame | continuous, stops off screen and when the tab is hidden | One frozen frame |
| All | Hero glow drift | Always | transform | 20 s, ease-in-out, alternate | Removed |
| Home | Stack strip marquee | Always, pauses on hover | transform translateX | continuous | Static row of chips |
| Hero and portal visuals | Live status dots | Always | transform, opacity | 2.4 s, ease-in-out | Removed |
| All | Every animation | Tab hidden | `animation-play-state: paused` | - | - |

## Interaction

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| All | Primary buttons | Pointer move, press | transform translate, capped at 8 px, scale .98 on press | per pointer event | Removed |
| All | Plan and card tilt | Pointer move | transform rotate, 4 degrees on plan cards, 3 on others | per pointer event | Removed |
| All | Card hover | Hover | transform translateY(-3 px), background step | 360 ms, out | Removed |
| All | Text links | Hover, focus | underline draws (background-size) | 360 ms, out | Instant |
| All | Navigation indicator | Hover, route | transform | 350 ms | Instant |
| All | Accordions | Click | height (details content), plus sign rotates 45 degrees | 360 ms, out | Instant |
| Contact | Floating labels | Focus, input | transform, scale .78 | 180 ms, out | Instant |
| Contact | Validation messages | Blur, submit | appear in place, no movement | - | - |
| All | Theme toggle | Click | icon opacity, rotate and scale, 240 ms; page colours cross-fade with View Transitions | 240 ms | Instant |
| Pricing | Compare toggle | Click | row opacity | 360 ms | Instant |
| Pricing | Calculator figures | Input | text count-up | 300 ms | Instant |
| Glossary | Flip cards | Click, Enter | transform rotateY | 700 ms, out | Instant |
| Compare pages | Verdict slider | Input | opacity, transform scale .985 on the other column | 360 ms | Instant |
| Solutions | Source toggle | Change | opacity, transform (8 px) on the panel | 360 ms, out | Removed |
| Checklist | Score bar | Tick | transform scaleX | 360 ms, out | Instant |

## Not on transform, opacity or clip-path

These are small, paint-only state changes, listed here so nothing is hidden: border and background colour on chip and button hover (180 ms), the label width of the home section dots (a fixed element, no layout effect), the canvas (pixels), and the text changes for counters, index ticks, typed log lines and calculator figures. None of them changes layout.

## Added in the layout fix

| Page | Element | Trigger | Properties | Duration, easing | Reduced motion |
|---|---|---|---|---|---|
| All card grids | Card glow | Pointer over a card | soft ember radial glow follows the cursor, translate (transform only) and opacity | 300 ms fade, follows the pointer | Removed |
| All card grids | Card entry stagger | Enters viewport | opacity, transform, 60 ms stagger (was 40 ms) | 380 ms, ease | Removed |
| Home | Asset row ("What you actually receive") | Drag with the mouse, touch swipe, arrow keys | scrollLeft with inertia (rAF decay), scroll-snap; cards lift on grab (translate -6 px, shadow) | inertia decays at 0.94 per frame; lift 360 ms, out | Instant scroll, no inertia, no lift animation |
| Home | Audience cards | Pointer move | tilt toward the pointer, 3 degrees (existing) | per pointer event | Removed |
| Home | Audience icons | Enters viewport, first time | stroke-dashoffset draws each icon | 800 ms, out, 60 ms stagger | Drawn at once |
| Home, resources, solutions | Card link underline | Hover on the card, not only the link | background-size draws the underline | 360 ms, out | Instant |
| Every page with section heads | Highlighter on the last word of each section heading | Enters viewport, once | clip-path inset sweep behind the word | 500 ms, out, 240 ms delay | Static highlight |
| Home | Fact counters | Enters viewport | odometer: each digit column rolls (transform translateY) | 900 ms, out, 90 ms per digit | Final number at once |
| Home | Fact captions | After the last digit lands | opacity, transform (8 px) | 500 ms, out | Visible |
| Comparison tables | Row hover | Hover | row background step; the winning cell turns ember text with a hairline stroke (no weight change, so no layout shift) | 180 ms | Instant |
| Comparison tables | Winning-cell check | Table enters viewport | clip-path draws the check | 500 ms, out, 300 ms delay | Static check |
| Home | Hero diagram depth (signature moment) | Pointer anywhere over the page while the hero is in view | the tabs, source column and asset column each translate by up to 4, 8 and 10 px against the pointer, a layered diagram that floats | 160 ms linear | Removed |
