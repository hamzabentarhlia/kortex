# Changelog

| Area | URL | Before | After |
|---|---|---|---|
| Indexation (P0) | /blog, /contact, /solutions, /login, /pricing without slash | Served root files blog.html, contact.html, solutions.html, login.html and pricing.html: noindex stubs, three of them with a canonical to a French URL | Stubs removed. GitHub Pages now answers with a 301 to the slashed English page. Legacy .html addresses redirect from the 404 page script |
| Sitemap | /sitemap.xml | lastmod from a fixed build date | lastmod from git history of each source file. Login and drafts excluded |
| Design | all pages | Orange and near-black palette, separate amber and crimson accents | Ink and Ember tokens in src/styles/tokens.css for dark and light. Amber and crimson are aliases of the coral tones. One hero glow. Flat primary buttons with navy text |
| Theme | all pages | theme-color fixed | theme-color follows the toggle and the system setting. Body cross-fade 360 ms, off under reduced motion |
| Contact form | /contact/, /fr/contact/, /ar/contact/ | Web3Forms redirect flow | Pageclip endpoint, pageclip-form classes, honeypot, inline success and error states, generate_lead event |
| Analytics | all pages | One generic CTA event | cta_click, book_call_click, generate_lead, theme_toggle, language_switch |
| Feeds | /blog/feed.xml, /fr/blog/feed.xml, /ar/blog/feed.xml | none | RSS 2.0 per language, linked with rel="alternate" |
| Metadata | 121 pages | 58 titles over 60 characters, 92 descriptions outside 130 to 155 | All within limits in English, French and Arabic |
| Structured data | legal pages | Article without datePublished | WebPage only. scripts/validate-jsonld.mjs passes 127 pages and 120 blocks |
| Social images | 117 indexable URLs | 37 hand-made images, the rest fell back to the home image | One 1200x630 image per URL from scripts/build-og-images.mjs, plus twitter:image |
| Accessibility | compare pages, home, how-it-works | landmark-unique and colour-contrast findings | axe-core: 0 violations on 15 pages in both themes |
| Placeholders | home, how-it-works visuals | Sample brand text "yourbrand.com" | Sample brand "acme.com" |
| Articles | /blog/llms-txt-what-to-do/, /geo-vs-seo-for-b2b/, /get-cited-by-chatgpt-perplexity-gemini/, /measure-ai-citations/, /schema-markup-ai-engines-read/, /webinar-to-content-system/ (and /fr/ versions) | none | Six sourced articles in English and French, each with a sources list of pages opened and read, a visible update date, FAQ and its own cover |
| Glossary | /glossary/retrieval-augmented-generation/, /query-fan-out/, /e-e-a-t/ | 10 entries | 13 entries in English, French and Arabic, each citing Google documentation |
| Compare | /compare/kortex-vs-in-house-writer/ | 3 comparisons under a heading that says four | 4 comparisons in three languages, each with a section on when the other option is better |
| Hub | /resources/, /fr/resources/, /ar/resources/ | Menu led nowhere for resources | Hub page linking articles, glossary and comparisons, added to the menu, footer, sitemap and llms.txt |
| Layout | all pages | Grid and card base rules in the async stylesheet caused a layout shift on two pages | Base layout rules moved into the inlined critical CSS. CLS 0 on the re-tested pages |
| Tables | article pages | Three-column tables scrolled sideways on phones | Narrow tables fit at 390 px, captions styled |

