#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/build.py
node scripts/build-checklist-pdf.mjs
node scripts/build-og-images.mjs
python3 src/build.py
node scripts/validate-jsonld.mjs
node scripts/check-hreflang.mjs
node scripts/check-contrast.mjs
