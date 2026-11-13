# Monetization report

## Needs human, in priority order

1. **Stripe Payment Link for the 490 euro audit.** Create a product "AI Citation Audit" in Stripe, create a Payment Link, set its success URL to `https://www.kortexlab.me/thanks-audit/`, and paste the URL into `data/site.json` as `stripeAuditUrl`. Run `scripts/build.sh`. The audit page then shows a pay button instead of the request form. Until then the page collects name, company, website and email and says payment follows a fit check.
2. **Second Pageclip form for email capture.** Create a form called "leads" in Pageclip, paste its key into `data/site.json` as `leadsFormKey`, and rebuild. Until then newsletter and checklist submissions go to the existing contact form key, so nothing is lost, but they arrive mixed with contact messages. Each submission carries `form` (newsletter, checklist or audit), `source` (page) and `language` fields.
3. **First citation-log run for /proof/.** Run the 40 questions in four engines and add the rows to `data/citations.json` under `runs` (fields: date, engine, question, named, cited, others, optional screenshot). Until then the page shows the method, the changelog and a line saying the first dated run is not published yet.
4. **GA4.** Mark the five key events listed in `docs/ga4-setup.md` and confirm Search Console is linked. Events only appear in GA4 after they have fired once, so trigger each yourself first.
5. **A real testimonial or permission to name a collaboration.** None is shown anywhere. The case study template at `/case-studies/_template/` renders from `data/case-studies.json` and stays noindex and out of the sitemap until an entry exists.
6. **Decisions I made that you should confirm or change:**
   - The 490 euro price and "credited in full against your first month". Both are used on the audit, pricing, checklist, emails and blog pages.
   - The call promise "30 minutes, no deck, you leave with three fixes whether we work together or not" is now on every booking button. Use it only if you will honor it on every call.
   - The newsletter says "twice a month". That is a commitment to publish.
   - The brief mentioned "the first month includes the pilot review". I do not know what that refers to, so it is not on the site.
   - The pricing comparison with a content marketer and an agency is qualitative, with no euro ranges, because I have no source for ranges. Give me quotes you trust and I will add labeled estimates.
   - Cal.com: I could not confirm that your Cal.com booking page and webhook keep `utm_*` parameters. The links carry them. Check one booking.
   - Pageclip: I could not confirm your plan offers webhooks. `docs/n8n-lead-flow.md` gives a Gmail Trigger fallback.
   - The nurture emails are English only. Add French versions before using the French branch.

## Where this brief did not match the repo

- **The stub bug was already fixed.** PR 7 deleted the five root files that served noindex stubs. The live site was checked on 2026-11-13: `/pricing/`, `/blog/` and `/contact/` return 200 with no robots meta and a self canonical, and the slashless forms return 301. Before and after matrices are in `docs/audit/stub-matrix.md`.
- **Arabic is live, so I did not remove it.** The brief asked to remove every Arabic reference. `/ar/` ships 35 pages with correct hreflang, so removing it would delete real pages. `scripts/check-hreflang.mjs` verifies every cluster is reciprocal, has a self reference and an English x-default, and that `og:locale:alternate` only lists languages that exist.
- **JSON-LD was already shipped** on every page. The gaps I found and fixed: `DefinedTermSet` on the glossary, `FAQPage` on blog post FAQs, and `Service` and `Offer` for the audit.
- **Branch:** work is on `claude/practical-euler-czw19j`, the branch this session was assigned, not `kortex-monetize`.
- **The new pages exist in English and French.** Arabic readers see the call to action but not the audit, checklist or proof pages.

## What was built

| URL | What it is |
|---|---|
| `/audit/`, `/fr/audit/` | The AI Citation Audit: problem, what is included, a sample section labeled illustrative, price, credit, three steps, FAQ, request form or Stripe button |
| `/checklist/`, `/fr/checklist/` | The 27 checks in five groups, email form, PDF in `assets/downloads/` in both languages |
| `/proof/`, `/fr/proof/` | Method, results table read from `data/citations.json`, changelog |
| `/thanks/`, `/fr/thanks/`, `/thanks-audit/`, `/fr/thanks-audit/` | Conversion pages, noindex |
| `/case-studies/_template/`, `/fr/case-studies/_template/` | Case study layout from `data/case-studies.json`, noindex, not in the sitemap |
| Pricing page | Four-question plan chooser with a deep link, per-asset math, audit card, risk section, comparison table |
| Everywhere | Newsletter block in the footer, on the blog index and on every post; a slide-in on blog posts (desktop only, after 60 percent scroll, once per session, dismissible); an audit link as the secondary CTA in the final CTA band; topic-matched end-of-post CTAs |

## Funnel map

1. Stranger finds a post, the glossary or the citation log through search or an AI answer.
2. The post offers the checklist PDF and the twice-monthly teardown; the slide-in and footer capture the email.
3. n8n sends four emails over 14 days (`content/emails/`, flow in `docs/n8n-lead-flow.md`) and stops on reply or booking.
4. The audit page or email 4 offers the 490 euro AI Citation Audit, credited against the first month.
5. The walkthrough call and the audit report lead to a SWARM-first plan conversation; every booking link carries `utm_source`, `utm_medium` and `utm_campaign`.

## Verification

### 1. Stub matrix

Result: 153 routes, each tested slashed and unslashed, 0 rows needing attention (no noindex on a public page, no cross-language canonical, no redirect stub). The before state found 5 bad addresses. Full tables: `docs/audit/stub-matrix.md`.

### 2. Built output and live checks

```

/pricing/ status=200 bytes=120829 robots=none canonical="https://www.kortexlab.me/pricing/"
/blog/ status=200 bytes=208829 robots=none canonical="https://www.kortexlab.me/blog/"
/contact/ status=200 bytes=63710 robots=none canonical="https://www.kortexlab.me/contact/"
/audit/ status=200 bytes=58091 robots=none canonical="https://www.kortexlab.me/audit/"
/checklist/ status=200 bytes=49611 robots=none canonical="https://www.kortexlab.me/checklist/"
/proof/ status=200 bytes=45054 robots=none canonical="https://www.kortexlab.me/proof/"
/fr/audit/ status=200 bytes=60275 robots=none canonical="https://www.kortexlab.me/fr/audit/"
/fr/checklist/ status=200 bytes=51198 robots=none canonical="https://www.kortexlab.me/fr/checklist/"
/fr/proof/ status=200 bytes=46456 robots=none canonical="https://www.kortexlab.me/fr/proof/"

```

Local server results for the same URLs: all 200. Live site, checked after the PR 7 merge: see `docs/audit/stub-matrix.md`.

### 3. JSON-LD

`scripts/validate-jsonld.mjs`: 166 pages, 159 JSON-LD blocks, 0 errors

Types per template: home Organization, WebSite, Person, Service, Offer, FAQPage, BreadcrumbList; pricing adds Service and Offer per plan with the real prices; audit adds Service and Offer at 490 EUR and FAQPage; blog posts BlogPosting, BreadcrumbList and FAQPage; glossary DefinedTermSet and DefinedTerm; about Person with sameAs LinkedIn.

### 4. Forms and tracking, tested end to end in Playwright with the Pageclip POST intercepted

```
pass  newsletter posts to Pageclip
pass  newsletter success message shown
pass  newsletter_signup and generate_lead fired
pass  checklist posts and redirects to /thanks/
pass  thanks page shows the PDF download
pass  PDF link returns a PDF  /assets/downloads/kortex-geo-audit-checklist-en.pdf
pass  audit request posts all fields
pass  contact form posts and redirects to /thanks/
pass  audit shows an inline error when the endpoint fails
pass  honeypot blocks the submission
pass  every booking link carries UTM parameters  9 links
pass  every button has a data-cta id  0 missing
pass  plan finder recommends TITAN for two sources and deep-links the plan
pass  plan finder recommends GHOST for a quiet niche and a test
pass  pricing_plan_view fires for visible plans  ghost,swarm,titan
pass  book_call_click and outbound_calcom fire
pass  slide-in appears after 60 percent scroll on desktop
pass  slide-in is dismissible
pass  tactical post ends with the audit CTA  /audit/
pass  slide-in never shows on mobile
pass  strategy post ends with the call CTA  https://cal.com/hamza-bentarhlia?lng=en&utm_source=site&utm_medium=blog-geo-vs-seo-for-b2b&utm_campaign=post-book
pass  Solutions is a real link  /solutions/
22 of 22 passed
```

### 5. Screenshots

36 images at 375, 768 and 1440 pixels in light and dark for home, pricing, audit, checklist, proof and one post: `docs/audit/screens-monetize/`. No horizontal overflow at any width. Contrast and keyboard checks: axe-core reports 0 violations on 18 funnel pages in both themes.

### 6. Leftovers

Zero `lorem`, `TODO`, `yourbrand` or dead `href="#"` in shipped files. The bracket templates ("[your product]") on the B2B and e-commerce pages were replaced with concrete example questions. Remaining brackets are inside article text that teaches a fill-in template. Hard-coded hex values outside `tokens.css` are limited to the two theme-color metas, the theme script, the Cal.com brand color and the logo, which cannot read CSS variables.

### 7. Lighthouse, mobile

| Page | Performance before | after | Accessibility, best practices, SEO |
|---|---|---|---|
| / | 100 | 100 | 100, 100, 100 |
| /pricing/ | 100 | 100 | 100, 100, 100 |
| /contact/ | 100 | 100 | 100, 100, 100 |
| /blog/measure-ai-citations/ | 100 | 100 | 100, 100, 100 |
| /audit/ | new | 100 | 100, 100, 100 |
| /checklist/ | new | 100 | 100, 100, 100 |
| /proof/ | new | 100 | 100, 100, 100 |
| /fr/ | 100 | 100 | 100, 100, 100 |
| /fr/pricing/ | 100 | 99 | 100, 100, 100 |
| /fr/audit/ | new | 100 | 100, 100, 100 |

One run of the home page scored 96 because of a 220 ms blocking-time spike. The rerun scored 100.

## Deploy on GitHub Pages

The host is GitHub Pages (CNAME file, no server config). There is no nginx to touch.

1. `scripts/build.sh` rebuilds pages, the checklist PDFs and social images, then runs the three validators.
2. Review the pull request and merge it into `main`. Pages publishes from the root of `main`.
3. After a few minutes, open `/audit/`, `/checklist/`, `/proof/` and `/pricing/`, and submit the audit form once.
4. In Search Console, resubmit `sitemap.xml` and request indexing for `/audit/`, `/checklist/` and `/proof/`.

Rollback: revert the merge commit on `main` with `git revert -m 1 <merge commit>` and push. To undo only the offer, set nothing in `data/site.json` and remove the audit links; the rest keeps working.

## The one metric to watch weekly

Audit requests per week: `generate_lead` events where `form_name` is `audit`, split by `utm_medium` of the page that sent the visitor. It is the first step that earns revenue. Read it with the number of strategy calls booked, but do not judge a week on fewer than a few requests; read the trend over the four weeks.
