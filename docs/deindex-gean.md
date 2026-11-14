# Removing the stale "Gean | Log in" result

## What it is

Bing shows the home result for the domain as "Gean | Log in: Login per cominciare la tua sessione Ricordati". Those Italian strings come from a login page of an admin-style app. Nothing in this repository contains it: a search of the source, data and built pages for `gean`, `Ricordati`, `cominciare` and `AdminLTE` returns nothing.

## What is live today

`kortexlab.me` is served by GitHub Pages, not by a server with its own configuration. Checked on 14 November 2026:

```
$ curl -sI https://kortexlab.me/
HTTP/2 301
server: GitHub.com
location: https://www.kortexlab.me/
```

So the apex already redirects to `https://www.kortexlab.me/` and the live site does not serve the login app. What Bing shows is an old snapshot taken when the apex pointed at a different host. The fix left is in the index, and in DNS if a stray record still points elsewhere.

## Owner checklist

1. DNS. At your registrar, confirm the apex `kortexlab.me` has only the four GitHub Pages A records (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) and, if you use IPv6, the matching AAAA records. Delete any A or AAAA record pointing at an old server, and any other hostname that still points there. If a server still answers on that old address, either shut the app down or apply `deploy/nginx-kortexlab.conf`, which answers every unknown host and IP request with a 301 to `https://www.kortexlab.me`.
2. Bing Webmaster Tools. Add and verify `https://kortexlab.me/` if it is not there. Run URL Inspection on `https://kortexlab.me/` and on `https://www.kortexlab.me/`, then request indexing for the www home page. Under Block URLs (the removal tool), submit `https://kortexlab.me/` for removal of the cached page.
3. Google Search Console. In the URL Inspection tool, inspect `https://kortexlab.me/` and `https://www.kortexlab.me/`, then request indexing for the second. If a Domain property exists, the Removals tool can clear a stale snapshot.
4. Wait 7 to 14 days, then search `site:kortexlab.me` in both engines. Only `www.kortexlab.me` results should remain.

## Commands that prove the fix

```
curl -sI https://kortexlab.me/ | grep -iE "^(HTTP|location)"
curl -sI https://kortexlab.me/login/ | grep -iE "^(HTTP|location)"
curl -s https://www.kortexlab.me/login/ | grep -o '<meta name="robots"[^>]*>'
curl -s https://www.kortexlab.me/robots.txt
```

The first two must show a 301 with `location: https://www.kortexlab.me/` (and `/login/`). The third must show `noindex, nofollow`. The robots.txt must not disallow the login paths: a crawler that is blocked from a page cannot read its noindex tag.

## In the repository

- `/login/`, `/fr/login/` and `/ar/login/` carry `noindex, nofollow` and are not in `sitemap.xml`.
- `deploy/nginx-kortexlab.conf` is for a server only. GitHub Pages cannot send `X-Robots-Tag`, so on GitHub Pages the login pages rely on the meta tag.
- If the app is still needed, move it to a separate hostname behind HTTP basic auth with `X-Robots-Tag: noindex, nofollow`, and never to the apex.
