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
