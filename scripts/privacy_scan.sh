#!/usr/bin/env bash
# Scan a folder for personal data before sharing/pushing.
#   scripts/privacy_scan.sh [folder] [extra-term ...]
# Extra terms (names, home neighborhood, budget figures, calendar titles) are
# matched case-insensitively. Exit code 1 if anything matches.
set -uo pipefail
DIR="${1:-.}"; shift || true
hits=0
check() { local label="$1"; shift; if rg -n --hidden -g '!.git' -g '!tests/.node' -g '!tests/node_modules' "$@" "$DIR"; then echo ">> HIT: $label"; hits=1; fi; }
check "email address"   -e '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
check "uuid"            -i -e '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
check "store/canvas id" -i -e 'store-[0-9a-f]' -e 'cursor\.com/canvas'
check "calendar id"     -i -e 'group\.calendar\.google\.com'
check "tokens/secrets"  -e 'gh[pousr]_[A-Za-z0-9]{20,}' -e 'sk-[A-Za-z0-9]{20,}' -e 'AKIA[0-9A-Z]{16}' -i -e 'bearer [a-z0-9._-]{20,}'
for term in "$@"; do check "term: $term" -i -F -e "$term"; done
[ $hits -eq 0 ] && echo "privacy scan: clean" || echo "privacy scan: FOUND HITS (fix before sharing)"
exit $hits
