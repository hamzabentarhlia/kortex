#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
BASE="${1:-https://www.kortexlab.me}"
APEX="${2:-https://kortexlab.me}"
probe() {
  local u="$1"
  local head body status loc xr robots canon
  head=$(curl -sS -m 20 -I "$u" 2>/dev/null | tr -d '\r')
  status=$(printf '%s\n' "$head" | awk '/^HTTP/{s=$2} END{print s}')
  loc=$(printf '%s\n' "$head" | awk -F': ' 'tolower($1)=="location"{print $2}' | tail -1)
  xr=$(printf '%s\n' "$head" | awk -F': ' 'tolower($1)=="x-robots-tag"{print $2}' | tail -1)
  robots="-"; canon="-"
  if [ "$status" = "200" ]; then
    body=$(curl -sS -m 20 "$u" 2>/dev/null)
    robots=$(printf '%s' "$body" | grep -o '<meta name="robots" content="[^"]*"' | head -1 | sed 's/.*content="//; s/"$//')
    canon=$(printf '%s' "$body" | grep -o '<link rel="canonical" href="[^"]*"' | head -1 | sed 's/.*href="//; s/"$//')
    [ -z "$robots" ] && robots="index, follow (default)"
    [ -z "$canon" ] && canon="-"
  fi
  printf '| %s | %s | %s | %s | %s | %s |\n' "$u" "$status" "${loc:--}" "${robots}" "${xr:--}" "${canon}"
}
export -f probe
echo "| URL | Status | Location | Robots meta | X-Robots-Tag | Canonical |"
echo "|---|---|---|---|---|---|"
probe "$APEX/"
probe "$APEX/pricing/"
probe "$APEX/login/"
grep -o '<loc>[^<]*</loc>' sitemap.xml | sed 's#<loc>https://www.kortexlab.me##; s#</loc>##' | while read -r path; do
  probe "$BASE$path"
  [ "$path" != "/" ] && probe "$BASE${path%/}"
done
probe "$BASE/login/"
probe "$BASE/fr/login/"
probe "$BASE/robots.txt"
probe "$BASE/sitemap.xml"
