# KORTEX — site bilingue (FR principal, EN sous /en/)

## Déployer sur GitHub Pages
1. Dans votre repo GitHub Pages, supprimez les anciens fichiers du site (gardez .git).
2. Copiez TOUT le contenu de ce dossier à la racine du repo (y compris `CNAME`, `.nojekyll`, `en/`).
3. Commit + push. Settings → Pages → Custom domain = `www.kortexlab.me` → cochez **Enforce HTTPS**.
4. Namecheap DNS : 4 enregistrements A `@` → 185.199.108.153 / 109.153 / 110.153 / 111.153 ; CNAME `www` → `<votre-user>.github.io`.
5. Google Search Console : ajoutez la propriété `https://www.kortexlab.me/`, soumettez `sitemap.xml`, demandez l'indexation de `/` puis `/en/`.

## Structure des URL
| Page | Français (indexé en premier, x-default) | English |
|---|---|---|
| Accueil | / | /en/ |
| Solutions | /solutions.html | /en/solutions.html |
| Tarifs | /tarifs.html | /en/pricing.html |
| Blog | /blog.html | /en/blog.html |
| Contact | /contact.html | /en/contact.html |
| 8 articles | /blog-<slug-fr>.html | /en/blog-<slug-en>.html |

Les anciennes URL anglaises à la racine (`/pricing.html`, `/blog-stop-ranking-start-dominating.html`, …) redirigent vers `/en/…`.
Chaque page a canonical, hreflang fr/en/x-default, Open Graph, JSON-LD (Organization, WebSite, WebPage, Breadcrumb + Article/FAQPage/Service/Offer selon la page). robots.txt autorise explicitement GPTBot, PerplexityBot, ClaudeBot, Google-Extended.

## Voir le site en local
Double-cliquez sur `index.html` : tous les chemins sont relatifs, CSS et JS se chargent. Dans un Codespace : `python3 -m http.server 8000` puis ouvrez le port 8000.

## Formulaire de contact
Web3Forms (clé existante). Après envoi, retour sur `contact.html?sent=1` avec message de confirmation. Testez un envoi après déploiement.
