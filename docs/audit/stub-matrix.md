# Stub matrix

Mechanism of the bug: GitHub Pages serves a root file named blog.html, contact.html, solutions.html, login.html or pricing.html at the slashless URL before it redirects to the directory. Those files were language-detection redirect stubs with noindex and, for four of them, a canonical pointing at the French page. Search engines that fetched /blog or /contact saw a near-empty noindex document. The slashed URLs used by navigation always served the full page.

Fix: the five stub files were deleted, so every slashless URL now gets a real 301 from GitHub Pages to the slashed page. Legacy .html addresses redirect through the 404 page script. No language detection runs on any shell page.

Live confirmation on https://www.kortexlab.me after the merge of PR 7:

| URL | Status | Robots meta | Canonical |
|---|---|---|---|
| /pricing/ | 200 | none (indexable) | "/pricing/" |
| /blog/ | 200 | none (indexable) | "/blog/" |
| /contact/ | 200 | none (indexable) | "/contact/" |
| /solutions/ | 200 | none (indexable) | "/solutions/" |
| /pricing | 301 | none | none |
| /blog | 301 | none | none |
| /contact | 301 | none | none |
| /fr/pricing/ | 200 | none (indexable) | "/fr/pricing/" |
| /fr/blog/ | 200 | none (indexable) | "/fr/blog/" |
| /fr/contact/ | 200 | none (indexable) | "/fr/contact/" |

## Before: state of the site at commit 674ceb3, the version published until PR 7

120 routes, each tested slashed and unslashed. Rows needing attention: 5.

| URL | Status | Robots | Canonical | Result |
|---|---|---|---|---|
| / | 200 | default | / | ok |
| /fr/ | 200 | default | /fr/ | ok |
| /fr | 301 to /fr/ | default | /fr/ | ok |
| /ar/ | 200 | default | /ar/ | ok |
| /ar | 301 to /ar/ | default | /ar/ | ok |
| /how-it-works/ | 200 | default | /how-it-works/ | ok |
| /how-it-works | 301 to /how-it-works/ | default | /how-it-works/ | ok |
| /fr/how-it-works/ | 200 | default | /fr/how-it-works/ | ok |
| /fr/how-it-works | 301 to /fr/how-it-works/ | default | /fr/how-it-works/ | ok |
| /ar/how-it-works/ | 200 | default | /ar/how-it-works/ | ok |
| /ar/how-it-works | 301 to /ar/how-it-works/ | default | /ar/how-it-works/ | ok |
| /solutions/ | 200 | default | /solutions/ | ok |
| /solutions | 200 | noindex, follow | /fr/how-it-works/ | redirect stub, near-empty |
| /fr/solutions/ | 200 | default | /fr/solutions/ | ok |
| /fr/solutions | 301 to /fr/solutions/ | default | /fr/solutions/ | ok |
| /ar/solutions/ | 200 | default | /ar/solutions/ | ok |
| /ar/solutions | 301 to /ar/solutions/ | default | /ar/solutions/ | ok |
| /solutions/b2b/ | 200 | default | /solutions/b2b/ | ok |
| /solutions/b2b | 301 to /solutions/b2b/ | default | /solutions/b2b/ | ok |
| /fr/solutions/b2b/ | 200 | default | /fr/solutions/b2b/ | ok |
| /fr/solutions/b2b | 301 to /fr/solutions/b2b/ | default | /fr/solutions/b2b/ | ok |
| /ar/solutions/b2b/ | 200 | default | /ar/solutions/b2b/ | ok |
| /ar/solutions/b2b | 301 to /ar/solutions/b2b/ | default | /ar/solutions/b2b/ | ok |
| /solutions/creators/ | 200 | default | /solutions/creators/ | ok |
| /solutions/creators | 301 to /solutions/creators/ | default | /solutions/creators/ | ok |
| /fr/solutions/creators/ | 200 | default | /fr/solutions/creators/ | ok |
| /fr/solutions/creators | 301 to /fr/solutions/creators/ | default | /fr/solutions/creators/ | ok |
| /ar/solutions/creators/ | 200 | default | /ar/solutions/creators/ | ok |
| /ar/solutions/creators | 301 to /ar/solutions/creators/ | default | /ar/solutions/creators/ | ok |
| /solutions/ecommerce/ | 200 | default | /solutions/ecommerce/ | ok |
| /solutions/ecommerce | 301 to /solutions/ecommerce/ | default | /solutions/ecommerce/ | ok |
| /fr/solutions/ecommerce/ | 200 | default | /fr/solutions/ecommerce/ | ok |
| /fr/solutions/ecommerce | 301 to /fr/solutions/ecommerce/ | default | /fr/solutions/ecommerce/ | ok |
| /ar/solutions/ecommerce/ | 200 | default | /ar/solutions/ecommerce/ | ok |
| /ar/solutions/ecommerce | 301 to /ar/solutions/ecommerce/ | default | /ar/solutions/ecommerce/ | ok |
| /solutions/from-a-blog/ | 200 | default | /solutions/from-a-blog/ | ok |
| /solutions/from-a-blog | 301 to /solutions/from-a-blog/ | default | /solutions/from-a-blog/ | ok |
| /fr/solutions/from-a-blog/ | 200 | default | /fr/solutions/from-a-blog/ | ok |
| /fr/solutions/from-a-blog | 301 to /fr/solutions/from-a-blog/ | default | /fr/solutions/from-a-blog/ | ok |
| /ar/solutions/from-a-blog/ | 200 | default | /ar/solutions/from-a-blog/ | ok |
| /ar/solutions/from-a-blog | 301 to /ar/solutions/from-a-blog/ | default | /ar/solutions/from-a-blog/ | ok |
| /solutions/from-youtube/ | 200 | default | /solutions/from-youtube/ | ok |
| /solutions/from-youtube | 301 to /solutions/from-youtube/ | default | /solutions/from-youtube/ | ok |
| /fr/solutions/from-youtube/ | 200 | default | /fr/solutions/from-youtube/ | ok |
| /fr/solutions/from-youtube | 301 to /fr/solutions/from-youtube/ | default | /fr/solutions/from-youtube/ | ok |
| /ar/solutions/from-youtube/ | 200 | default | /ar/solutions/from-youtube/ | ok |
| /ar/solutions/from-youtube | 301 to /ar/solutions/from-youtube/ | default | /ar/solutions/from-youtube/ | ok |
| /solutions/from-a-podcast/ | 200 | default | /solutions/from-a-podcast/ | ok |
| /solutions/from-a-podcast | 301 to /solutions/from-a-podcast/ | default | /solutions/from-a-podcast/ | ok |
| /fr/solutions/from-a-podcast/ | 200 | default | /fr/solutions/from-a-podcast/ | ok |
| /fr/solutions/from-a-podcast | 301 to /fr/solutions/from-a-podcast/ | default | /fr/solutions/from-a-podcast/ | ok |
| /ar/solutions/from-a-podcast/ | 200 | default | /ar/solutions/from-a-podcast/ | ok |
| /ar/solutions/from-a-podcast | 301 to /ar/solutions/from-a-podcast/ | default | /ar/solutions/from-a-podcast/ | ok |
| /solutions/from-a-webinar/ | 200 | default | /solutions/from-a-webinar/ | ok |
| /solutions/from-a-webinar | 301 to /solutions/from-a-webinar/ | default | /solutions/from-a-webinar/ | ok |
| /fr/solutions/from-a-webinar/ | 200 | default | /fr/solutions/from-a-webinar/ | ok |
| /fr/solutions/from-a-webinar | 301 to /fr/solutions/from-a-webinar/ | default | /fr/solutions/from-a-webinar/ | ok |
| /ar/solutions/from-a-webinar/ | 200 | default | /ar/solutions/from-a-webinar/ | ok |
| /ar/solutions/from-a-webinar | 301 to /ar/solutions/from-a-webinar/ | default | /ar/solutions/from-a-webinar/ | ok |
| /pricing/ | 200 | default | /pricing/ | ok |
| /pricing | 200 | noindex, follow | /pricing/ | redirect stub, near-empty |
| /fr/pricing/ | 200 | default | /fr/pricing/ | ok |
| /fr/pricing | 301 to /fr/pricing/ | default | /fr/pricing/ | ok |
| /ar/pricing/ | 200 | default | /ar/pricing/ | ok |
| /ar/pricing | 301 to /ar/pricing/ | default | /ar/pricing/ | ok |
| /about/ | 200 | default | /about/ | ok |
| /about | 301 to /about/ | default | /about/ | ok |
| /fr/about/ | 200 | default | /fr/about/ | ok |
| /fr/about | 301 to /fr/about/ | default | /fr/about/ | ok |
| /ar/about/ | 200 | default | /ar/about/ | ok |
| /ar/about | 301 to /ar/about/ | default | /ar/about/ | ok |
| /compare/ | 200 | default | /compare/ | ok |
| /compare | 301 to /compare/ | default | /compare/ | ok |
| /fr/compare/ | 200 | default | /fr/compare/ | ok |
| /fr/compare | 301 to /fr/compare/ | default | /fr/compare/ | ok |
| /ar/compare/ | 200 | default | /ar/compare/ | ok |
| /ar/compare | 301 to /ar/compare/ | default | /ar/compare/ | ok |
| /glossary/ | 200 | default | /glossary/ | ok |
| /glossary | 301 to /glossary/ | default | /glossary/ | ok |
| /fr/glossary/ | 200 | default | /fr/glossary/ | ok |
| /fr/glossary | 301 to /fr/glossary/ | default | /fr/glossary/ | ok |
| /ar/glossary/ | 200 | default | /ar/glossary/ | ok |
| /ar/glossary | 301 to /ar/glossary/ | default | /ar/glossary/ | ok |
| /blog/ | 200 | default | /blog/ | ok |
| /blog | 200 | noindex, follow | /fr/blog/ | redirect stub, near-empty |
| /fr/blog/ | 200 | default | /fr/blog/ | ok |
| /fr/blog | 301 to /fr/blog/ | default | /fr/blog/ | ok |
| /ar/blog/ | 200 | default | /ar/blog/ | ok |
| /ar/blog | 301 to /ar/blog/ | default | /ar/blog/ | ok |
| /contact/ | 200 | default | /contact/ | ok |
| /contact | 200 | noindex, follow | /fr/contact/ | redirect stub, near-empty |
| /fr/contact/ | 200 | default | /fr/contact/ | ok |
| /fr/contact | 301 to /fr/contact/ | default | /fr/contact/ | ok |
| /ar/contact/ | 200 | default | /ar/contact/ | ok |
| /ar/contact | 301 to /ar/contact/ | default | /ar/contact/ | ok |
| /legal/privacy/ | 200 | default | /legal/privacy/ | ok |
| /legal/privacy | 301 to /legal/privacy/ | default | /legal/privacy/ | ok |
| /fr/legal/privacy/ | 200 | default | /fr/legal/privacy/ | ok |
| /fr/legal/privacy | 301 to /fr/legal/privacy/ | default | /fr/legal/privacy/ | ok |
| /ar/legal/privacy/ | 200 | default | /ar/legal/privacy/ | ok |
| /ar/legal/privacy | 301 to /ar/legal/privacy/ | default | /ar/legal/privacy/ | ok |
| /legal/cookies/ | 200 | default | /legal/cookies/ | ok |
| /legal/cookies | 301 to /legal/cookies/ | default | /legal/cookies/ | ok |
| /fr/legal/cookies/ | 200 | default | /fr/legal/cookies/ | ok |
| /fr/legal/cookies | 301 to /fr/legal/cookies/ | default | /fr/legal/cookies/ | ok |
| /ar/legal/cookies/ | 200 | default | /ar/legal/cookies/ | ok |
| /ar/legal/cookies | 301 to /ar/legal/cookies/ | default | /ar/legal/cookies/ | ok |
| /blog/answer-engine-visibility-guide/ | 200 | default | /blog/answer-engine-visibility-guide/ | ok |
| /blog/answer-engine-visibility-guide | 301 to /blog/answer-engine-visibility-guide/ | default | /blog/answer-engine-visibility-guide/ | ok |
| /fr/blog/answer-engine-visibility-guide/ | 200 | default | /fr/blog/answer-engine-visibility-guide/ | ok |
| /fr/blog/answer-engine-visibility-guide | 301 to /fr/blog/answer-engine-visibility-guide/ | default | /fr/blog/answer-engine-visibility-guide/ | ok |
| /ar/blog/answer-engine-visibility-guide/ | 200 | default | /ar/blog/answer-engine-visibility-guide/ | ok |
| /ar/blog/answer-engine-visibility-guide | 301 to /ar/blog/answer-engine-visibility-guide/ | default | /ar/blog/answer-engine-visibility-guide/ | ok |
| /blog/b2b-linkedin-content-dies/ | 200 | default | /blog/b2b-linkedin-content-dies/ | ok |
| /blog/b2b-linkedin-content-dies | 301 to /blog/b2b-linkedin-content-dies/ | default | /blog/b2b-linkedin-content-dies/ | ok |
| /fr/blog/b2b-linkedin-content-dies/ | 200 | default | /fr/blog/b2b-linkedin-content-dies/ | ok |
| /fr/blog/b2b-linkedin-content-dies | 301 to /fr/blog/b2b-linkedin-content-dies/ | default | /fr/blog/b2b-linkedin-content-dies/ | ok |
| /ar/blog/b2b-linkedin-content-dies/ | 200 | default | /ar/blog/b2b-linkedin-content-dies/ | ok |
| /ar/blog/b2b-linkedin-content-dies | 301 to /ar/blog/b2b-linkedin-content-dies/ | default | /ar/blog/b2b-linkedin-content-dies/ | ok |
| /blog/category-creation-ai-search/ | 200 | default | /blog/category-creation-ai-search/ | ok |
| /blog/category-creation-ai-search | 301 to /blog/category-creation-ai-search/ | default | /blog/category-creation-ai-search/ | ok |
| /fr/blog/category-creation-ai-search/ | 200 | default | /fr/blog/category-creation-ai-search/ | ok |
| /fr/blog/category-creation-ai-search | 301 to /fr/blog/category-creation-ai-search/ | default | /fr/blog/category-creation-ai-search/ | ok |
| /ar/blog/category-creation-ai-search/ | 200 | default | /ar/blog/category-creation-ai-search/ | ok |
| /ar/blog/category-creation-ai-search | 301 to /ar/blog/category-creation-ai-search/ | default | /ar/blog/category-creation-ai-search/ | ok |
| /blog/content-audit-ai-retrieval/ | 200 | default | /blog/content-audit-ai-retrieval/ | ok |
| /blog/content-audit-ai-retrieval | 301 to /blog/content-audit-ai-retrieval/ | default | /blog/content-audit-ai-retrieval/ | ok |
| /fr/blog/content-audit-ai-retrieval/ | 200 | default | /fr/blog/content-audit-ai-retrieval/ | ok |
| /fr/blog/content-audit-ai-retrieval | 301 to /fr/blog/content-audit-ai-retrieval/ | default | /fr/blog/content-audit-ai-retrieval/ | ok |
| /ar/blog/content-audit-ai-retrieval/ | 200 | default | /ar/blog/content-audit-ai-retrieval/ | ok |
| /ar/blog/content-audit-ai-retrieval | 301 to /ar/blog/content-audit-ai-retrieval/ | default | /ar/blog/content-audit-ai-retrieval/ | ok |
| /blog/entity-first-content-architecture/ | 200 | default | /blog/entity-first-content-architecture/ | ok |
| /blog/entity-first-content-architecture | 301 to /blog/entity-first-content-architecture/ | default | /blog/entity-first-content-architecture/ | ok |
| /fr/blog/entity-first-content-architecture/ | 200 | default | /fr/blog/entity-first-content-architecture/ | ok |
| /fr/blog/entity-first-content-architecture | 301 to /fr/blog/entity-first-content-architecture/ | default | /fr/blog/entity-first-content-architecture/ | ok |
| /ar/blog/entity-first-content-architecture/ | 200 | default | /ar/blog/entity-first-content-architecture/ | ok |
| /ar/blog/entity-first-content-architecture | 301 to /ar/blog/entity-first-content-architecture/ | default | /ar/blog/entity-first-content-architecture/ | ok |
| /blog/new-b2b-content-stack/ | 200 | default | /blog/new-b2b-content-stack/ | ok |
| /blog/new-b2b-content-stack | 301 to /blog/new-b2b-content-stack/ | default | /blog/new-b2b-content-stack/ | ok |
| /fr/blog/new-b2b-content-stack/ | 200 | default | /fr/blog/new-b2b-content-stack/ | ok |
| /fr/blog/new-b2b-content-stack | 301 to /fr/blog/new-b2b-content-stack/ | default | /fr/blog/new-b2b-content-stack/ | ok |
| /ar/blog/new-b2b-content-stack/ | 200 | default | /ar/blog/new-b2b-content-stack/ | ok |
| /ar/blog/new-b2b-content-stack | 301 to /ar/blog/new-b2b-content-stack/ | default | /ar/blog/new-b2b-content-stack/ | ok |
| /blog/one-video-authority-system/ | 200 | default | /blog/one-video-authority-system/ | ok |
| /blog/one-video-authority-system | 301 to /blog/one-video-authority-system/ | default | /blog/one-video-authority-system/ | ok |
| /fr/blog/one-video-authority-system/ | 200 | default | /fr/blog/one-video-authority-system/ | ok |
| /fr/blog/one-video-authority-system | 301 to /fr/blog/one-video-authority-system/ | default | /fr/blog/one-video-authority-system/ | ok |
| /ar/blog/one-video-authority-system/ | 200 | default | /ar/blog/one-video-authority-system/ | ok |
| /ar/blog/one-video-authority-system | 301 to /ar/blog/one-video-authority-system/ | default | /ar/blog/one-video-authority-system/ | ok |
| /blog/stop-ranking-start-dominating/ | 200 | default | /blog/stop-ranking-start-dominating/ | ok |
| /blog/stop-ranking-start-dominating | 301 to /blog/stop-ranking-start-dominating/ | default | /blog/stop-ranking-start-dominating/ | ok |
| /fr/blog/stop-ranking-start-dominating/ | 200 | default | /fr/blog/stop-ranking-start-dominating/ | ok |
| /fr/blog/stop-ranking-start-dominating | 301 to /fr/blog/stop-ranking-start-dominating/ | default | /fr/blog/stop-ranking-start-dominating/ | ok |
| /ar/blog/stop-ranking-start-dominating/ | 200 | default | /ar/blog/stop-ranking-start-dominating/ | ok |
| /ar/blog/stop-ranking-start-dominating | 301 to /ar/blog/stop-ranking-start-dominating/ | default | /ar/blog/stop-ranking-start-dominating/ | ok |
| /compare/kortex-vs-chatgpt/ | 200 | default | /compare/kortex-vs-chatgpt/ | ok |
| /compare/kortex-vs-chatgpt | 301 to /compare/kortex-vs-chatgpt/ | default | /compare/kortex-vs-chatgpt/ | ok |
| /fr/compare/kortex-vs-chatgpt/ | 200 | default | /fr/compare/kortex-vs-chatgpt/ | ok |
| /fr/compare/kortex-vs-chatgpt | 301 to /fr/compare/kortex-vs-chatgpt/ | default | /fr/compare/kortex-vs-chatgpt/ | ok |
| /ar/compare/kortex-vs-chatgpt/ | 200 | default | /ar/compare/kortex-vs-chatgpt/ | ok |
| /ar/compare/kortex-vs-chatgpt | 301 to /ar/compare/kortex-vs-chatgpt/ | default | /ar/compare/kortex-vs-chatgpt/ | ok |
| /compare/kortex-vs-freelance-writer/ | 200 | default | /compare/kortex-vs-freelance-writer/ | ok |
| /compare/kortex-vs-freelance-writer | 301 to /compare/kortex-vs-freelance-writer/ | default | /compare/kortex-vs-freelance-writer/ | ok |
| /fr/compare/kortex-vs-freelance-writer/ | 200 | default | /fr/compare/kortex-vs-freelance-writer/ | ok |
| /fr/compare/kortex-vs-freelance-writer | 301 to /fr/compare/kortex-vs-freelance-writer/ | default | /fr/compare/kortex-vs-freelance-writer/ | ok |
| /ar/compare/kortex-vs-freelance-writer/ | 200 | default | /ar/compare/kortex-vs-freelance-writer/ | ok |
| /ar/compare/kortex-vs-freelance-writer | 301 to /ar/compare/kortex-vs-freelance-writer/ | default | /ar/compare/kortex-vs-freelance-writer/ | ok |
| /compare/kortex-vs-seo-agency/ | 200 | default | /compare/kortex-vs-seo-agency/ | ok |
| /compare/kortex-vs-seo-agency | 301 to /compare/kortex-vs-seo-agency/ | default | /compare/kortex-vs-seo-agency/ | ok |
| /fr/compare/kortex-vs-seo-agency/ | 200 | default | /fr/compare/kortex-vs-seo-agency/ | ok |
| /fr/compare/kortex-vs-seo-agency | 301 to /fr/compare/kortex-vs-seo-agency/ | default | /fr/compare/kortex-vs-seo-agency/ | ok |
| /ar/compare/kortex-vs-seo-agency/ | 200 | default | /ar/compare/kortex-vs-seo-agency/ | ok |
| /ar/compare/kortex-vs-seo-agency | 301 to /ar/compare/kortex-vs-seo-agency/ | default | /ar/compare/kortex-vs-seo-agency/ | ok |
| /glossary/ai-overviews/ | 200 | default | /glossary/ai-overviews/ | ok |
| /glossary/ai-overviews | 301 to /glossary/ai-overviews/ | default | /glossary/ai-overviews/ | ok |
| /fr/glossary/ai-overviews/ | 200 | default | /fr/glossary/ai-overviews/ | ok |
| /fr/glossary/ai-overviews | 301 to /fr/glossary/ai-overviews/ | default | /fr/glossary/ai-overviews/ | ok |
| /ar/glossary/ai-overviews/ | 200 | default | /ar/glossary/ai-overviews/ | ok |
| /ar/glossary/ai-overviews | 301 to /ar/glossary/ai-overviews/ | default | /ar/glossary/ai-overviews/ | ok |
| /glossary/answer-engine-optimization/ | 200 | default | /glossary/answer-engine-optimization/ | ok |
| /glossary/answer-engine-optimization | 301 to /glossary/answer-engine-optimization/ | default | /glossary/answer-engine-optimization/ | ok |
| /fr/glossary/answer-engine-optimization/ | 200 | default | /fr/glossary/answer-engine-optimization/ | ok |
| /fr/glossary/answer-engine-optimization | 301 to /fr/glossary/answer-engine-optimization/ | default | /fr/glossary/answer-engine-optimization/ | ok |
| /ar/glossary/answer-engine-optimization/ | 200 | default | /ar/glossary/answer-engine-optimization/ | ok |
| /ar/glossary/answer-engine-optimization | 301 to /ar/glossary/answer-engine-optimization/ | default | /ar/glossary/answer-engine-optimization/ | ok |
| /glossary/answer-first-content/ | 200 | default | /glossary/answer-first-content/ | ok |
| /glossary/answer-first-content | 301 to /glossary/answer-first-content/ | default | /glossary/answer-first-content/ | ok |
| /fr/glossary/answer-first-content/ | 200 | default | /fr/glossary/answer-first-content/ | ok |
| /fr/glossary/answer-first-content | 301 to /fr/glossary/answer-first-content/ | default | /fr/glossary/answer-first-content/ | ok |
| /ar/glossary/answer-first-content/ | 200 | default | /ar/glossary/answer-first-content/ | ok |
| /ar/glossary/answer-first-content | 301 to /ar/glossary/answer-first-content/ | default | /ar/glossary/answer-first-content/ | ok |
| /glossary/citation-rate/ | 200 | default | /glossary/citation-rate/ | ok |
| /glossary/citation-rate | 301 to /glossary/citation-rate/ | default | /glossary/citation-rate/ | ok |
| /fr/glossary/citation-rate/ | 200 | default | /fr/glossary/citation-rate/ | ok |
| /fr/glossary/citation-rate | 301 to /fr/glossary/citation-rate/ | default | /fr/glossary/citation-rate/ | ok |
| /ar/glossary/citation-rate/ | 200 | default | /ar/glossary/citation-rate/ | ok |
| /ar/glossary/citation-rate | 301 to /ar/glossary/citation-rate/ | default | /ar/glossary/citation-rate/ | ok |
| /glossary/entity/ | 200 | default | /glossary/entity/ | ok |
| /glossary/entity | 301 to /glossary/entity/ | default | /glossary/entity/ | ok |
| /fr/glossary/entity/ | 200 | default | /fr/glossary/entity/ | ok |
| /fr/glossary/entity | 301 to /fr/glossary/entity/ | default | /fr/glossary/entity/ | ok |
| /ar/glossary/entity/ | 200 | default | /ar/glossary/entity/ | ok |
| /ar/glossary/entity | 301 to /ar/glossary/entity/ | default | /ar/glossary/entity/ | ok |
| /glossary/generative-engine-optimization/ | 200 | default | /glossary/generative-engine-optimization/ | ok |
| /glossary/generative-engine-optimization | 301 to /glossary/generative-engine-optimization/ | default | /glossary/generative-engine-optimization/ | ok |
| /fr/glossary/generative-engine-optimization/ | 200 | default | /fr/glossary/generative-engine-optimization/ | ok |
| /fr/glossary/generative-engine-optimization | 301 to /fr/glossary/generative-engine-optimization/ | default | /fr/glossary/generative-engine-optimization/ | ok |
| /ar/glossary/generative-engine-optimization/ | 200 | default | /ar/glossary/generative-engine-optimization/ | ok |
| /ar/glossary/generative-engine-optimization | 301 to /ar/glossary/generative-engine-optimization/ | default | /ar/glossary/generative-engine-optimization/ | ok |
| /glossary/llms-txt/ | 200 | default | /glossary/llms-txt/ | ok |
| /glossary/llms-txt | 301 to /glossary/llms-txt/ | default | /glossary/llms-txt/ | ok |
| /fr/glossary/llms-txt/ | 200 | default | /fr/glossary/llms-txt/ | ok |
| /fr/glossary/llms-txt | 301 to /fr/glossary/llms-txt/ | default | /fr/glossary/llms-txt/ | ok |
| /ar/glossary/llms-txt/ | 200 | default | /ar/glossary/llms-txt/ | ok |
| /ar/glossary/llms-txt | 301 to /ar/glossary/llms-txt/ | default | /ar/glossary/llms-txt/ | ok |
| /glossary/schema-markup/ | 200 | default | /glossary/schema-markup/ | ok |
| /glossary/schema-markup | 301 to /glossary/schema-markup/ | default | /glossary/schema-markup/ | ok |
| /fr/glossary/schema-markup/ | 200 | default | /fr/glossary/schema-markup/ | ok |
| /fr/glossary/schema-markup | 301 to /fr/glossary/schema-markup/ | default | /fr/glossary/schema-markup/ | ok |
| /ar/glossary/schema-markup/ | 200 | default | /ar/glossary/schema-markup/ | ok |
| /ar/glossary/schema-markup | 301 to /ar/glossary/schema-markup/ | default | /ar/glossary/schema-markup/ | ok |
| /glossary/search-engine-optimization/ | 200 | default | /glossary/search-engine-optimization/ | ok |
| /glossary/search-engine-optimization | 301 to /glossary/search-engine-optimization/ | default | /glossary/search-engine-optimization/ | ok |
| /fr/glossary/search-engine-optimization/ | 200 | default | /fr/glossary/search-engine-optimization/ | ok |
| /fr/glossary/search-engine-optimization | 301 to /fr/glossary/search-engine-optimization/ | default | /fr/glossary/search-engine-optimization/ | ok |
| /ar/glossary/search-engine-optimization/ | 200 | default | /ar/glossary/search-engine-optimization/ | ok |
| /ar/glossary/search-engine-optimization | 301 to /ar/glossary/search-engine-optimization/ | default | /ar/glossary/search-engine-optimization/ | ok |
| /glossary/topical-authority/ | 200 | default | /glossary/topical-authority/ | ok |
| /glossary/topical-authority | 301 to /glossary/topical-authority/ | default | /glossary/topical-authority/ | ok |
| /fr/glossary/topical-authority/ | 200 | default | /fr/glossary/topical-authority/ | ok |
| /fr/glossary/topical-authority | 301 to /fr/glossary/topical-authority/ | default | /fr/glossary/topical-authority/ | ok |
| /ar/glossary/topical-authority/ | 200 | default | /ar/glossary/topical-authority/ | ok |
| /ar/glossary/topical-authority | 301 to /ar/glossary/topical-authority/ | default | /ar/glossary/topical-authority/ | ok |
| /login/ | 200 | noindex, follow | /login/ | ok |
| /login | 200 | noindex, follow | /fr/login/ | redirect stub, near-empty |
| /fr/login/ | 200 | noindex, follow | /fr/login/ | ok |
| /fr/login | 301 to /fr/login/ | noindex, follow | /fr/login/ | ok |
| /ar/login/ | 200 | noindex, follow | /ar/login/ | ok |
| /ar/login | 301 to /ar/login/ | noindex, follow | /ar/login/ | ok |

## After: current branch

147 routes, each tested slashed and unslashed. Rows needing attention: 0.

| URL | Status | Robots | Canonical | Result |
|---|---|---|---|---|
| / | 200 | default | / | ok |
| /fr/ | 200 | default | /fr/ | ok |
| /fr | 301 to /fr/ | default | /fr/ | ok |
| /ar/ | 200 | default | /ar/ | ok |
| /ar | 301 to /ar/ | default | /ar/ | ok |
| /how-it-works/ | 200 | default | /how-it-works/ | ok |
| /how-it-works | 301 to /how-it-works/ | default | /how-it-works/ | ok |
| /fr/how-it-works/ | 200 | default | /fr/how-it-works/ | ok |
| /fr/how-it-works | 301 to /fr/how-it-works/ | default | /fr/how-it-works/ | ok |
| /ar/how-it-works/ | 200 | default | /ar/how-it-works/ | ok |
| /ar/how-it-works | 301 to /ar/how-it-works/ | default | /ar/how-it-works/ | ok |
| /solutions/ | 200 | default | /solutions/ | ok |
| /solutions | 301 to /solutions/ | default | /solutions/ | ok |
| /fr/solutions/ | 200 | default | /fr/solutions/ | ok |
| /fr/solutions | 301 to /fr/solutions/ | default | /fr/solutions/ | ok |
| /ar/solutions/ | 200 | default | /ar/solutions/ | ok |
| /ar/solutions | 301 to /ar/solutions/ | default | /ar/solutions/ | ok |
| /solutions/b2b/ | 200 | default | /solutions/b2b/ | ok |
| /solutions/b2b | 301 to /solutions/b2b/ | default | /solutions/b2b/ | ok |
| /fr/solutions/b2b/ | 200 | default | /fr/solutions/b2b/ | ok |
| /fr/solutions/b2b | 301 to /fr/solutions/b2b/ | default | /fr/solutions/b2b/ | ok |
| /ar/solutions/b2b/ | 200 | default | /ar/solutions/b2b/ | ok |
| /ar/solutions/b2b | 301 to /ar/solutions/b2b/ | default | /ar/solutions/b2b/ | ok |
| /solutions/creators/ | 200 | default | /solutions/creators/ | ok |
| /solutions/creators | 301 to /solutions/creators/ | default | /solutions/creators/ | ok |
| /fr/solutions/creators/ | 200 | default | /fr/solutions/creators/ | ok |
| /fr/solutions/creators | 301 to /fr/solutions/creators/ | default | /fr/solutions/creators/ | ok |
| /ar/solutions/creators/ | 200 | default | /ar/solutions/creators/ | ok |
| /ar/solutions/creators | 301 to /ar/solutions/creators/ | default | /ar/solutions/creators/ | ok |
| /solutions/ecommerce/ | 200 | default | /solutions/ecommerce/ | ok |
| /solutions/ecommerce | 301 to /solutions/ecommerce/ | default | /solutions/ecommerce/ | ok |
| /fr/solutions/ecommerce/ | 200 | default | /fr/solutions/ecommerce/ | ok |
| /fr/solutions/ecommerce | 301 to /fr/solutions/ecommerce/ | default | /fr/solutions/ecommerce/ | ok |
| /ar/solutions/ecommerce/ | 200 | default | /ar/solutions/ecommerce/ | ok |
| /ar/solutions/ecommerce | 301 to /ar/solutions/ecommerce/ | default | /ar/solutions/ecommerce/ | ok |
| /solutions/from-a-blog/ | 200 | default | /solutions/from-a-blog/ | ok |
| /solutions/from-a-blog | 301 to /solutions/from-a-blog/ | default | /solutions/from-a-blog/ | ok |
| /fr/solutions/from-a-blog/ | 200 | default | /fr/solutions/from-a-blog/ | ok |
| /fr/solutions/from-a-blog | 301 to /fr/solutions/from-a-blog/ | default | /fr/solutions/from-a-blog/ | ok |
| /ar/solutions/from-a-blog/ | 200 | default | /ar/solutions/from-a-blog/ | ok |
| /ar/solutions/from-a-blog | 301 to /ar/solutions/from-a-blog/ | default | /ar/solutions/from-a-blog/ | ok |
| /solutions/from-youtube/ | 200 | default | /solutions/from-youtube/ | ok |
| /solutions/from-youtube | 301 to /solutions/from-youtube/ | default | /solutions/from-youtube/ | ok |
| /fr/solutions/from-youtube/ | 200 | default | /fr/solutions/from-youtube/ | ok |
| /fr/solutions/from-youtube | 301 to /fr/solutions/from-youtube/ | default | /fr/solutions/from-youtube/ | ok |
| /ar/solutions/from-youtube/ | 200 | default | /ar/solutions/from-youtube/ | ok |
| /ar/solutions/from-youtube | 301 to /ar/solutions/from-youtube/ | default | /ar/solutions/from-youtube/ | ok |
| /solutions/from-a-podcast/ | 200 | default | /solutions/from-a-podcast/ | ok |
| /solutions/from-a-podcast | 301 to /solutions/from-a-podcast/ | default | /solutions/from-a-podcast/ | ok |
| /fr/solutions/from-a-podcast/ | 200 | default | /fr/solutions/from-a-podcast/ | ok |
| /fr/solutions/from-a-podcast | 301 to /fr/solutions/from-a-podcast/ | default | /fr/solutions/from-a-podcast/ | ok |
| /ar/solutions/from-a-podcast/ | 200 | default | /ar/solutions/from-a-podcast/ | ok |
| /ar/solutions/from-a-podcast | 301 to /ar/solutions/from-a-podcast/ | default | /ar/solutions/from-a-podcast/ | ok |
| /solutions/from-a-webinar/ | 200 | default | /solutions/from-a-webinar/ | ok |
| /solutions/from-a-webinar | 301 to /solutions/from-a-webinar/ | default | /solutions/from-a-webinar/ | ok |
| /fr/solutions/from-a-webinar/ | 200 | default | /fr/solutions/from-a-webinar/ | ok |
| /fr/solutions/from-a-webinar | 301 to /fr/solutions/from-a-webinar/ | default | /fr/solutions/from-a-webinar/ | ok |
| /ar/solutions/from-a-webinar/ | 200 | default | /ar/solutions/from-a-webinar/ | ok |
| /ar/solutions/from-a-webinar | 301 to /ar/solutions/from-a-webinar/ | default | /ar/solutions/from-a-webinar/ | ok |
| /pricing/ | 200 | default | /pricing/ | ok |
| /pricing | 301 to /pricing/ | default | /pricing/ | ok |
| /fr/pricing/ | 200 | default | /fr/pricing/ | ok |
| /fr/pricing | 301 to /fr/pricing/ | default | /fr/pricing/ | ok |
| /ar/pricing/ | 200 | default | /ar/pricing/ | ok |
| /ar/pricing | 301 to /ar/pricing/ | default | /ar/pricing/ | ok |
| /about/ | 200 | default | /about/ | ok |
| /about | 301 to /about/ | default | /about/ | ok |
| /fr/about/ | 200 | default | /fr/about/ | ok |
| /fr/about | 301 to /fr/about/ | default | /fr/about/ | ok |
| /ar/about/ | 200 | default | /ar/about/ | ok |
| /ar/about | 301 to /ar/about/ | default | /ar/about/ | ok |
| /compare/ | 200 | default | /compare/ | ok |
| /compare | 301 to /compare/ | default | /compare/ | ok |
| /fr/compare/ | 200 | default | /fr/compare/ | ok |
| /fr/compare | 301 to /fr/compare/ | default | /fr/compare/ | ok |
| /ar/compare/ | 200 | default | /ar/compare/ | ok |
| /ar/compare | 301 to /ar/compare/ | default | /ar/compare/ | ok |
| /glossary/ | 200 | default | /glossary/ | ok |
| /glossary | 301 to /glossary/ | default | /glossary/ | ok |
| /fr/glossary/ | 200 | default | /fr/glossary/ | ok |
| /fr/glossary | 301 to /fr/glossary/ | default | /fr/glossary/ | ok |
| /ar/glossary/ | 200 | default | /ar/glossary/ | ok |
| /ar/glossary | 301 to /ar/glossary/ | default | /ar/glossary/ | ok |
| /resources/ | 200 | default | /resources/ | ok |
| /resources | 301 to /resources/ | default | /resources/ | ok |
| /fr/resources/ | 200 | default | /fr/resources/ | ok |
| /fr/resources | 301 to /fr/resources/ | default | /fr/resources/ | ok |
| /ar/resources/ | 200 | default | /ar/resources/ | ok |
| /ar/resources | 301 to /ar/resources/ | default | /ar/resources/ | ok |
| /blog/ | 200 | default | /blog/ | ok |
| /blog | 301 to /blog/ | default | /blog/ | ok |
| /fr/blog/ | 200 | default | /fr/blog/ | ok |
| /fr/blog | 301 to /fr/blog/ | default | /fr/blog/ | ok |
| /ar/blog/ | 200 | default | /ar/blog/ | ok |
| /ar/blog | 301 to /ar/blog/ | default | /ar/blog/ | ok |
| /contact/ | 200 | default | /contact/ | ok |
| /contact | 301 to /contact/ | default | /contact/ | ok |
| /fr/contact/ | 200 | default | /fr/contact/ | ok |
| /fr/contact | 301 to /fr/contact/ | default | /fr/contact/ | ok |
| /ar/contact/ | 200 | default | /ar/contact/ | ok |
| /ar/contact | 301 to /ar/contact/ | default | /ar/contact/ | ok |
| /legal/privacy/ | 200 | default | /legal/privacy/ | ok |
| /legal/privacy | 301 to /legal/privacy/ | default | /legal/privacy/ | ok |
| /fr/legal/privacy/ | 200 | default | /fr/legal/privacy/ | ok |
| /fr/legal/privacy | 301 to /fr/legal/privacy/ | default | /fr/legal/privacy/ | ok |
| /ar/legal/privacy/ | 200 | default | /ar/legal/privacy/ | ok |
| /ar/legal/privacy | 301 to /ar/legal/privacy/ | default | /ar/legal/privacy/ | ok |
| /legal/cookies/ | 200 | default | /legal/cookies/ | ok |
| /legal/cookies | 301 to /legal/cookies/ | default | /legal/cookies/ | ok |
| /fr/legal/cookies/ | 200 | default | /fr/legal/cookies/ | ok |
| /fr/legal/cookies | 301 to /fr/legal/cookies/ | default | /fr/legal/cookies/ | ok |
| /ar/legal/cookies/ | 200 | default | /ar/legal/cookies/ | ok |
| /ar/legal/cookies | 301 to /ar/legal/cookies/ | default | /ar/legal/cookies/ | ok |
| /blog/answer-engine-visibility-guide/ | 200 | default | /blog/answer-engine-visibility-guide/ | ok |
| /blog/answer-engine-visibility-guide | 301 to /blog/answer-engine-visibility-guide/ | default | /blog/answer-engine-visibility-guide/ | ok |
| /fr/blog/answer-engine-visibility-guide/ | 200 | default | /fr/blog/answer-engine-visibility-guide/ | ok |
| /fr/blog/answer-engine-visibility-guide | 301 to /fr/blog/answer-engine-visibility-guide/ | default | /fr/blog/answer-engine-visibility-guide/ | ok |
| /ar/blog/answer-engine-visibility-guide/ | 200 | default | /ar/blog/answer-engine-visibility-guide/ | ok |
| /ar/blog/answer-engine-visibility-guide | 301 to /ar/blog/answer-engine-visibility-guide/ | default | /ar/blog/answer-engine-visibility-guide/ | ok |
| /blog/b2b-linkedin-content-dies/ | 200 | default | /blog/b2b-linkedin-content-dies/ | ok |
| /blog/b2b-linkedin-content-dies | 301 to /blog/b2b-linkedin-content-dies/ | default | /blog/b2b-linkedin-content-dies/ | ok |
| /fr/blog/b2b-linkedin-content-dies/ | 200 | default | /fr/blog/b2b-linkedin-content-dies/ | ok |
| /fr/blog/b2b-linkedin-content-dies | 301 to /fr/blog/b2b-linkedin-content-dies/ | default | /fr/blog/b2b-linkedin-content-dies/ | ok |
| /ar/blog/b2b-linkedin-content-dies/ | 200 | default | /ar/blog/b2b-linkedin-content-dies/ | ok |
| /ar/blog/b2b-linkedin-content-dies | 301 to /ar/blog/b2b-linkedin-content-dies/ | default | /ar/blog/b2b-linkedin-content-dies/ | ok |
| /blog/category-creation-ai-search/ | 200 | default | /blog/category-creation-ai-search/ | ok |
| /blog/category-creation-ai-search | 301 to /blog/category-creation-ai-search/ | default | /blog/category-creation-ai-search/ | ok |
| /fr/blog/category-creation-ai-search/ | 200 | default | /fr/blog/category-creation-ai-search/ | ok |
| /fr/blog/category-creation-ai-search | 301 to /fr/blog/category-creation-ai-search/ | default | /fr/blog/category-creation-ai-search/ | ok |
| /ar/blog/category-creation-ai-search/ | 200 | default | /ar/blog/category-creation-ai-search/ | ok |
| /ar/blog/category-creation-ai-search | 301 to /ar/blog/category-creation-ai-search/ | default | /ar/blog/category-creation-ai-search/ | ok |
| /blog/content-audit-ai-retrieval/ | 200 | default | /blog/content-audit-ai-retrieval/ | ok |
| /blog/content-audit-ai-retrieval | 301 to /blog/content-audit-ai-retrieval/ | default | /blog/content-audit-ai-retrieval/ | ok |
| /fr/blog/content-audit-ai-retrieval/ | 200 | default | /fr/blog/content-audit-ai-retrieval/ | ok |
| /fr/blog/content-audit-ai-retrieval | 301 to /fr/blog/content-audit-ai-retrieval/ | default | /fr/blog/content-audit-ai-retrieval/ | ok |
| /ar/blog/content-audit-ai-retrieval/ | 200 | default | /ar/blog/content-audit-ai-retrieval/ | ok |
| /ar/blog/content-audit-ai-retrieval | 301 to /ar/blog/content-audit-ai-retrieval/ | default | /ar/blog/content-audit-ai-retrieval/ | ok |
| /blog/entity-first-content-architecture/ | 200 | default | /blog/entity-first-content-architecture/ | ok |
| /blog/entity-first-content-architecture | 301 to /blog/entity-first-content-architecture/ | default | /blog/entity-first-content-architecture/ | ok |
| /fr/blog/entity-first-content-architecture/ | 200 | default | /fr/blog/entity-first-content-architecture/ | ok |
| /fr/blog/entity-first-content-architecture | 301 to /fr/blog/entity-first-content-architecture/ | default | /fr/blog/entity-first-content-architecture/ | ok |
| /ar/blog/entity-first-content-architecture/ | 200 | default | /ar/blog/entity-first-content-architecture/ | ok |
| /ar/blog/entity-first-content-architecture | 301 to /ar/blog/entity-first-content-architecture/ | default | /ar/blog/entity-first-content-architecture/ | ok |
| /blog/new-b2b-content-stack/ | 200 | default | /blog/new-b2b-content-stack/ | ok |
| /blog/new-b2b-content-stack | 301 to /blog/new-b2b-content-stack/ | default | /blog/new-b2b-content-stack/ | ok |
| /fr/blog/new-b2b-content-stack/ | 200 | default | /fr/blog/new-b2b-content-stack/ | ok |
| /fr/blog/new-b2b-content-stack | 301 to /fr/blog/new-b2b-content-stack/ | default | /fr/blog/new-b2b-content-stack/ | ok |
| /ar/blog/new-b2b-content-stack/ | 200 | default | /ar/blog/new-b2b-content-stack/ | ok |
| /ar/blog/new-b2b-content-stack | 301 to /ar/blog/new-b2b-content-stack/ | default | /ar/blog/new-b2b-content-stack/ | ok |
| /blog/one-video-authority-system/ | 200 | default | /blog/one-video-authority-system/ | ok |
| /blog/one-video-authority-system | 301 to /blog/one-video-authority-system/ | default | /blog/one-video-authority-system/ | ok |
| /fr/blog/one-video-authority-system/ | 200 | default | /fr/blog/one-video-authority-system/ | ok |
| /fr/blog/one-video-authority-system | 301 to /fr/blog/one-video-authority-system/ | default | /fr/blog/one-video-authority-system/ | ok |
| /ar/blog/one-video-authority-system/ | 200 | default | /ar/blog/one-video-authority-system/ | ok |
| /ar/blog/one-video-authority-system | 301 to /ar/blog/one-video-authority-system/ | default | /ar/blog/one-video-authority-system/ | ok |
| /blog/stop-ranking-start-dominating/ | 200 | default | /blog/stop-ranking-start-dominating/ | ok |
| /blog/stop-ranking-start-dominating | 301 to /blog/stop-ranking-start-dominating/ | default | /blog/stop-ranking-start-dominating/ | ok |
| /fr/blog/stop-ranking-start-dominating/ | 200 | default | /fr/blog/stop-ranking-start-dominating/ | ok |
| /fr/blog/stop-ranking-start-dominating | 301 to /fr/blog/stop-ranking-start-dominating/ | default | /fr/blog/stop-ranking-start-dominating/ | ok |
| /ar/blog/stop-ranking-start-dominating/ | 200 | default | /ar/blog/stop-ranking-start-dominating/ | ok |
| /ar/blog/stop-ranking-start-dominating | 301 to /ar/blog/stop-ranking-start-dominating/ | default | /ar/blog/stop-ranking-start-dominating/ | ok |
| /compare/kortex-vs-chatgpt/ | 200 | default | /compare/kortex-vs-chatgpt/ | ok |
| /compare/kortex-vs-chatgpt | 301 to /compare/kortex-vs-chatgpt/ | default | /compare/kortex-vs-chatgpt/ | ok |
| /fr/compare/kortex-vs-chatgpt/ | 200 | default | /fr/compare/kortex-vs-chatgpt/ | ok |
| /fr/compare/kortex-vs-chatgpt | 301 to /fr/compare/kortex-vs-chatgpt/ | default | /fr/compare/kortex-vs-chatgpt/ | ok |
| /ar/compare/kortex-vs-chatgpt/ | 200 | default | /ar/compare/kortex-vs-chatgpt/ | ok |
| /ar/compare/kortex-vs-chatgpt | 301 to /ar/compare/kortex-vs-chatgpt/ | default | /ar/compare/kortex-vs-chatgpt/ | ok |
| /compare/kortex-vs-freelance-writer/ | 200 | default | /compare/kortex-vs-freelance-writer/ | ok |
| /compare/kortex-vs-freelance-writer | 301 to /compare/kortex-vs-freelance-writer/ | default | /compare/kortex-vs-freelance-writer/ | ok |
| /fr/compare/kortex-vs-freelance-writer/ | 200 | default | /fr/compare/kortex-vs-freelance-writer/ | ok |
| /fr/compare/kortex-vs-freelance-writer | 301 to /fr/compare/kortex-vs-freelance-writer/ | default | /fr/compare/kortex-vs-freelance-writer/ | ok |
| /ar/compare/kortex-vs-freelance-writer/ | 200 | default | /ar/compare/kortex-vs-freelance-writer/ | ok |
| /ar/compare/kortex-vs-freelance-writer | 301 to /ar/compare/kortex-vs-freelance-writer/ | default | /ar/compare/kortex-vs-freelance-writer/ | ok |
| /compare/kortex-vs-in-house-writer/ | 200 | default | /compare/kortex-vs-in-house-writer/ | ok |
| /compare/kortex-vs-in-house-writer | 301 to /compare/kortex-vs-in-house-writer/ | default | /compare/kortex-vs-in-house-writer/ | ok |
| /fr/compare/kortex-vs-in-house-writer/ | 200 | default | /fr/compare/kortex-vs-in-house-writer/ | ok |
| /fr/compare/kortex-vs-in-house-writer | 301 to /fr/compare/kortex-vs-in-house-writer/ | default | /fr/compare/kortex-vs-in-house-writer/ | ok |
| /ar/compare/kortex-vs-in-house-writer/ | 200 | default | /ar/compare/kortex-vs-in-house-writer/ | ok |
| /ar/compare/kortex-vs-in-house-writer | 301 to /ar/compare/kortex-vs-in-house-writer/ | default | /ar/compare/kortex-vs-in-house-writer/ | ok |
| /compare/kortex-vs-seo-agency/ | 200 | default | /compare/kortex-vs-seo-agency/ | ok |
| /compare/kortex-vs-seo-agency | 301 to /compare/kortex-vs-seo-agency/ | default | /compare/kortex-vs-seo-agency/ | ok |
| /fr/compare/kortex-vs-seo-agency/ | 200 | default | /fr/compare/kortex-vs-seo-agency/ | ok |
| /fr/compare/kortex-vs-seo-agency | 301 to /fr/compare/kortex-vs-seo-agency/ | default | /fr/compare/kortex-vs-seo-agency/ | ok |
| /ar/compare/kortex-vs-seo-agency/ | 200 | default | /ar/compare/kortex-vs-seo-agency/ | ok |
| /ar/compare/kortex-vs-seo-agency | 301 to /ar/compare/kortex-vs-seo-agency/ | default | /ar/compare/kortex-vs-seo-agency/ | ok |
| /glossary/ai-overviews/ | 200 | default | /glossary/ai-overviews/ | ok |
| /glossary/ai-overviews | 301 to /glossary/ai-overviews/ | default | /glossary/ai-overviews/ | ok |
| /fr/glossary/ai-overviews/ | 200 | default | /fr/glossary/ai-overviews/ | ok |
| /fr/glossary/ai-overviews | 301 to /fr/glossary/ai-overviews/ | default | /fr/glossary/ai-overviews/ | ok |
| /ar/glossary/ai-overviews/ | 200 | default | /ar/glossary/ai-overviews/ | ok |
| /ar/glossary/ai-overviews | 301 to /ar/glossary/ai-overviews/ | default | /ar/glossary/ai-overviews/ | ok |
| /glossary/answer-engine-optimization/ | 200 | default | /glossary/answer-engine-optimization/ | ok |
| /glossary/answer-engine-optimization | 301 to /glossary/answer-engine-optimization/ | default | /glossary/answer-engine-optimization/ | ok |
| /fr/glossary/answer-engine-optimization/ | 200 | default | /fr/glossary/answer-engine-optimization/ | ok |
| /fr/glossary/answer-engine-optimization | 301 to /fr/glossary/answer-engine-optimization/ | default | /fr/glossary/answer-engine-optimization/ | ok |
| /ar/glossary/answer-engine-optimization/ | 200 | default | /ar/glossary/answer-engine-optimization/ | ok |
| /ar/glossary/answer-engine-optimization | 301 to /ar/glossary/answer-engine-optimization/ | default | /ar/glossary/answer-engine-optimization/ | ok |
| /glossary/answer-first-content/ | 200 | default | /glossary/answer-first-content/ | ok |
| /glossary/answer-first-content | 301 to /glossary/answer-first-content/ | default | /glossary/answer-first-content/ | ok |
| /fr/glossary/answer-first-content/ | 200 | default | /fr/glossary/answer-first-content/ | ok |
| /fr/glossary/answer-first-content | 301 to /fr/glossary/answer-first-content/ | default | /fr/glossary/answer-first-content/ | ok |
| /ar/glossary/answer-first-content/ | 200 | default | /ar/glossary/answer-first-content/ | ok |
| /ar/glossary/answer-first-content | 301 to /ar/glossary/answer-first-content/ | default | /ar/glossary/answer-first-content/ | ok |
| /glossary/citation-rate/ | 200 | default | /glossary/citation-rate/ | ok |
| /glossary/citation-rate | 301 to /glossary/citation-rate/ | default | /glossary/citation-rate/ | ok |
| /fr/glossary/citation-rate/ | 200 | default | /fr/glossary/citation-rate/ | ok |
| /fr/glossary/citation-rate | 301 to /fr/glossary/citation-rate/ | default | /fr/glossary/citation-rate/ | ok |
| /ar/glossary/citation-rate/ | 200 | default | /ar/glossary/citation-rate/ | ok |
| /ar/glossary/citation-rate | 301 to /ar/glossary/citation-rate/ | default | /ar/glossary/citation-rate/ | ok |
| /glossary/e-e-a-t/ | 200 | default | /glossary/e-e-a-t/ | ok |
| /glossary/e-e-a-t | 301 to /glossary/e-e-a-t/ | default | /glossary/e-e-a-t/ | ok |
| /fr/glossary/e-e-a-t/ | 200 | default | /fr/glossary/e-e-a-t/ | ok |
| /fr/glossary/e-e-a-t | 301 to /fr/glossary/e-e-a-t/ | default | /fr/glossary/e-e-a-t/ | ok |
| /ar/glossary/e-e-a-t/ | 200 | default | /ar/glossary/e-e-a-t/ | ok |
| /ar/glossary/e-e-a-t | 301 to /ar/glossary/e-e-a-t/ | default | /ar/glossary/e-e-a-t/ | ok |
| /glossary/entity/ | 200 | default | /glossary/entity/ | ok |
| /glossary/entity | 301 to /glossary/entity/ | default | /glossary/entity/ | ok |
| /fr/glossary/entity/ | 200 | default | /fr/glossary/entity/ | ok |
| /fr/glossary/entity | 301 to /fr/glossary/entity/ | default | /fr/glossary/entity/ | ok |
| /ar/glossary/entity/ | 200 | default | /ar/glossary/entity/ | ok |
| /ar/glossary/entity | 301 to /ar/glossary/entity/ | default | /ar/glossary/entity/ | ok |
| /glossary/generative-engine-optimization/ | 200 | default | /glossary/generative-engine-optimization/ | ok |
| /glossary/generative-engine-optimization | 301 to /glossary/generative-engine-optimization/ | default | /glossary/generative-engine-optimization/ | ok |
| /fr/glossary/generative-engine-optimization/ | 200 | default | /fr/glossary/generative-engine-optimization/ | ok |
| /fr/glossary/generative-engine-optimization | 301 to /fr/glossary/generative-engine-optimization/ | default | /fr/glossary/generative-engine-optimization/ | ok |
| /ar/glossary/generative-engine-optimization/ | 200 | default | /ar/glossary/generative-engine-optimization/ | ok |
| /ar/glossary/generative-engine-optimization | 301 to /ar/glossary/generative-engine-optimization/ | default | /ar/glossary/generative-engine-optimization/ | ok |
| /glossary/llms-txt/ | 200 | default | /glossary/llms-txt/ | ok |
| /glossary/llms-txt | 301 to /glossary/llms-txt/ | default | /glossary/llms-txt/ | ok |
| /fr/glossary/llms-txt/ | 200 | default | /fr/glossary/llms-txt/ | ok |
| /fr/glossary/llms-txt | 301 to /fr/glossary/llms-txt/ | default | /fr/glossary/llms-txt/ | ok |
| /ar/glossary/llms-txt/ | 200 | default | /ar/glossary/llms-txt/ | ok |
| /ar/glossary/llms-txt | 301 to /ar/glossary/llms-txt/ | default | /ar/glossary/llms-txt/ | ok |
| /glossary/query-fan-out/ | 200 | default | /glossary/query-fan-out/ | ok |
| /glossary/query-fan-out | 301 to /glossary/query-fan-out/ | default | /glossary/query-fan-out/ | ok |
| /fr/glossary/query-fan-out/ | 200 | default | /fr/glossary/query-fan-out/ | ok |
| /fr/glossary/query-fan-out | 301 to /fr/glossary/query-fan-out/ | default | /fr/glossary/query-fan-out/ | ok |
| /ar/glossary/query-fan-out/ | 200 | default | /ar/glossary/query-fan-out/ | ok |
| /ar/glossary/query-fan-out | 301 to /ar/glossary/query-fan-out/ | default | /ar/glossary/query-fan-out/ | ok |
| /glossary/retrieval-augmented-generation/ | 200 | default | /glossary/retrieval-augmented-generation/ | ok |
| /glossary/retrieval-augmented-generation | 301 to /glossary/retrieval-augmented-generation/ | default | /glossary/retrieval-augmented-generation/ | ok |
| /fr/glossary/retrieval-augmented-generation/ | 200 | default | /fr/glossary/retrieval-augmented-generation/ | ok |
| /fr/glossary/retrieval-augmented-generation | 301 to /fr/glossary/retrieval-augmented-generation/ | default | /fr/glossary/retrieval-augmented-generation/ | ok |
| /ar/glossary/retrieval-augmented-generation/ | 200 | default | /ar/glossary/retrieval-augmented-generation/ | ok |
| /ar/glossary/retrieval-augmented-generation | 301 to /ar/glossary/retrieval-augmented-generation/ | default | /ar/glossary/retrieval-augmented-generation/ | ok |
| /glossary/schema-markup/ | 200 | default | /glossary/schema-markup/ | ok |
| /glossary/schema-markup | 301 to /glossary/schema-markup/ | default | /glossary/schema-markup/ | ok |
| /fr/glossary/schema-markup/ | 200 | default | /fr/glossary/schema-markup/ | ok |
| /fr/glossary/schema-markup | 301 to /fr/glossary/schema-markup/ | default | /fr/glossary/schema-markup/ | ok |
| /ar/glossary/schema-markup/ | 200 | default | /ar/glossary/schema-markup/ | ok |
| /ar/glossary/schema-markup | 301 to /ar/glossary/schema-markup/ | default | /ar/glossary/schema-markup/ | ok |
| /glossary/search-engine-optimization/ | 200 | default | /glossary/search-engine-optimization/ | ok |
| /glossary/search-engine-optimization | 301 to /glossary/search-engine-optimization/ | default | /glossary/search-engine-optimization/ | ok |
| /fr/glossary/search-engine-optimization/ | 200 | default | /fr/glossary/search-engine-optimization/ | ok |
| /fr/glossary/search-engine-optimization | 301 to /fr/glossary/search-engine-optimization/ | default | /fr/glossary/search-engine-optimization/ | ok |
| /ar/glossary/search-engine-optimization/ | 200 | default | /ar/glossary/search-engine-optimization/ | ok |
| /ar/glossary/search-engine-optimization | 301 to /ar/glossary/search-engine-optimization/ | default | /ar/glossary/search-engine-optimization/ | ok |
| /glossary/topical-authority/ | 200 | default | /glossary/topical-authority/ | ok |
| /glossary/topical-authority | 301 to /glossary/topical-authority/ | default | /glossary/topical-authority/ | ok |
| /fr/glossary/topical-authority/ | 200 | default | /fr/glossary/topical-authority/ | ok |
| /fr/glossary/topical-authority | 301 to /fr/glossary/topical-authority/ | default | /fr/glossary/topical-authority/ | ok |
| /ar/glossary/topical-authority/ | 200 | default | /ar/glossary/topical-authority/ | ok |
| /ar/glossary/topical-authority | 301 to /ar/glossary/topical-authority/ | default | /ar/glossary/topical-authority/ | ok |
| /blog/geo-vs-seo-for-b2b/ | 200 | default | /blog/geo-vs-seo-for-b2b/ | ok |
| /blog/geo-vs-seo-for-b2b | 301 to /blog/geo-vs-seo-for-b2b/ | default | /blog/geo-vs-seo-for-b2b/ | ok |
| /fr/blog/geo-vs-seo-for-b2b/ | 200 | default | /fr/blog/geo-vs-seo-for-b2b/ | ok |
| /fr/blog/geo-vs-seo-for-b2b | 301 to /fr/blog/geo-vs-seo-for-b2b/ | default | /fr/blog/geo-vs-seo-for-b2b/ | ok |
| /blog/get-cited-by-chatgpt-perplexity-gemini/ | 200 | default | /blog/get-cited-by-chatgpt-perplexity-gemini/ | ok |
| /blog/get-cited-by-chatgpt-perplexity-gemini | 301 to /blog/get-cited-by-chatgpt-perplexity-gemini/ | default | /blog/get-cited-by-chatgpt-perplexity-gemini/ | ok |
| /fr/blog/get-cited-by-chatgpt-perplexity-gemini/ | 200 | default | /fr/blog/get-cited-by-chatgpt-perplexity-gemini/ | ok |
| /fr/blog/get-cited-by-chatgpt-perplexity-gemini | 301 to /fr/blog/get-cited-by-chatgpt-perplexity-gemini/ | default | /fr/blog/get-cited-by-chatgpt-perplexity-gemini/ | ok |
| /blog/llms-txt-what-to-do/ | 200 | default | /blog/llms-txt-what-to-do/ | ok |
| /blog/llms-txt-what-to-do | 301 to /blog/llms-txt-what-to-do/ | default | /blog/llms-txt-what-to-do/ | ok |
| /fr/blog/llms-txt-what-to-do/ | 200 | default | /fr/blog/llms-txt-what-to-do/ | ok |
| /fr/blog/llms-txt-what-to-do | 301 to /fr/blog/llms-txt-what-to-do/ | default | /fr/blog/llms-txt-what-to-do/ | ok |
| /blog/measure-ai-citations/ | 200 | default | /blog/measure-ai-citations/ | ok |
| /blog/measure-ai-citations | 301 to /blog/measure-ai-citations/ | default | /blog/measure-ai-citations/ | ok |
| /fr/blog/measure-ai-citations/ | 200 | default | /fr/blog/measure-ai-citations/ | ok |
| /fr/blog/measure-ai-citations | 301 to /fr/blog/measure-ai-citations/ | default | /fr/blog/measure-ai-citations/ | ok |
| /blog/schema-markup-ai-engines-read/ | 200 | default | /blog/schema-markup-ai-engines-read/ | ok |
| /blog/schema-markup-ai-engines-read | 301 to /blog/schema-markup-ai-engines-read/ | default | /blog/schema-markup-ai-engines-read/ | ok |
| /fr/blog/schema-markup-ai-engines-read/ | 200 | default | /fr/blog/schema-markup-ai-engines-read/ | ok |
| /fr/blog/schema-markup-ai-engines-read | 301 to /fr/blog/schema-markup-ai-engines-read/ | default | /fr/blog/schema-markup-ai-engines-read/ | ok |
| /blog/webinar-to-content-system/ | 200 | default | /blog/webinar-to-content-system/ | ok |
| /blog/webinar-to-content-system | 301 to /blog/webinar-to-content-system/ | default | /blog/webinar-to-content-system/ | ok |
| /fr/blog/webinar-to-content-system/ | 200 | default | /fr/blog/webinar-to-content-system/ | ok |
| /fr/blog/webinar-to-content-system | 301 to /fr/blog/webinar-to-content-system/ | default | /fr/blog/webinar-to-content-system/ | ok |
| /login/ | 200 | noindex, follow | /login/ | ok |
| /login | 301 to /login/ | noindex, follow | /login/ | ok |
| /fr/login/ | 200 | noindex, follow | /fr/login/ | ok |
| /fr/login | 301 to /fr/login/ | noindex, follow | /fr/login/ | ok |
| /ar/login/ | 200 | noindex, follow | /ar/login/ | ok |
| /ar/login | 301 to /ar/login/ | noindex, follow | /ar/login/ | ok |

