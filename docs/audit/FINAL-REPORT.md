# Final report

## Stack and hosting found in the repo

- Static generator: src/build.py, page sources in src/pages/{en,fr,ar}, output committed at the repo root.
- Hosting: GitHub Pages (CNAME file, workflow in .github). No nginx, Dockerfile or Procfile exists. Response headers cannot be set on this host, so no nginx snippet was written.
- Not done from this sandbox: crawl of the live www.kortexlab.me and a diff against the repo. The sandbox cannot reach the live site.

## Verification results

| Check | Result |
|---|---|
| Build | 121 pages, no warnings |
| Internal links | 9,032 links checked on the built site, 0 broken |
| JSON-LD | 127 pages, 120 blocks, 0 errors. FAQ schema equals the visible FAQ |
| Slashless URLs | /blog, /pricing, /contact, /solutions, /login, /about, /fr/blog, /ar/pricing resolve with a 301 to the slashed URL |
| Contrast | scripts/check-contrast.mjs passes for both themes |
| axe-core | 0 violations on 15 pages in dark and light, reduced motion on |
| Contact form | success, error and honeypot states tested in all three languages with the endpoint mocked |
| Titles and descriptions | 0 pages outside 60 characters and 130 to 155 |

## Lighthouse mobile, 24 pages

Accessibility, best practices and SEO are 100 on all 24 pages (home, pricing, contact, about, B2B solution, article, blog index, glossary term, in three languages). Performance is 99 or 100, with one run of 97 on an article that scored 100 on the rerun.

| Page (EN) | Accessibility before | after | Performance before | after |
|---|---|---|---|---|
| / | 97 | 100 | 100 | 99 |
| /pricing/ | 96 | 100 | 100 | 100 |
| /contact/ | 96 | 100 | 100 | 100 |
| /about/ | 96 | 100 | 100 | 100 |
| /solutions/b2b/ | 96 | 100 | 100 | 100 |
| /blog/stop-ranking-start-dominating/ | 96 | 100 | 100 | 100 |

## Needs human

- Real client results, testimonials, logos or permission to publish citation-test numbers. No proof section was invented.
- Founder bio facts, photos beyond the existing portrait, and real social profile URLs for sameAs.
- Native review of the Arabic copy, including the rewritten titles and descriptions.
- Facts for Terms and Security: hosting region, AI providers, retention, deletion process, ownership, payment terms, governing law, legal entity.
- Confirmation that the Pageclip form key is active and that submissions reach your inbox.
- Cal.com account settings: Google Meet as the only location, 30-minute duration, account language.

## Second batch

- Sources were read by hand from Google Search Central (AI features, the generative AI optimization guide, spam policies, helpful content, generative AI content, structured data policies, documentation updates), llmstxt.org, Perplexity's crawler documentation and schema.org. OpenAI's crawler documentation could not be opened from this environment, so no OpenAI statement is made anywhere.
- Six articles in English and French, three glossary terms in three languages, one comparison in three languages, and the /resources/ hub in three languages.
- Findings that affect existing copy, from Google's own guide: llms.txt, special markup and chunking are not needed for Google Search; the FAQ rich result is no longer shown; separate pages for every query variation can breach the scaled content abuse policy. Older articles and some page copy still describe these as levers. They were not rewritten.

## Not done

- Articles 5 to 12 of the queue (entity SEO for founders, agency vs in-house vs studio, repurposing mistakes, human QA layer, podcast to authority, GEO in French and Arabic) and Arabic versions of all new articles.
- The extra comparison "kortex-vs-hiring-an-agency": it would repeat the existing SEO agency comparison.
- The neural-network canvas: kortex_core.js does not exist in this repo.
- Reading progress bar, table of contents, cursor glow, View Transitions and the pipeline diagram on how it works.
- Blog category filter and pagination.

## Deploy on GitHub Pages

1. Build: python3 src/build.py
2. Commit the changed files at the repo root and push to the branch behind the Pages site.
3. Pages publishes within a few minutes. No cache purge is needed on this host.
4. Submit the sitemap again in Search Console and ping IndexNow with src/indexnow.py.
5. Rollback: git revert the merge commit and push.
