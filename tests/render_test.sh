#!/usr/bin/env bash
# Type-check and server-render every tab of a tracker Page file.
#   tests/render_test.sh                      # the empty kit Page
#   tests/render_test.sh path/to/page.tsx     # e.g. a Page with your injected payload
#   tests/render_test.sh --fixture            # build from tests/fixtures/demo (fictional) and test
# Needs node + npm. Installs typescript/esbuild/react into tests/.node (git-ignored).
set -euo pipefail
cd "$(dirname "$0")"
ROOT=..
if [ "${1:-}" = "--fixture" ]; then
  python3 $ROOT/scripts/build_page_payload.py --data-dir fixtures/demo --page $ROOT/page/tracker.canvas.tsx --out _page.tsx --as-of 2030-03-05
else
  cp "${1:-$ROOT/page/tracker.canvas.tsx}" _page.tsx
fi
if [ ! -d .node/node_modules ]; then
  mkdir -p .node && (cd .node && echo "{\"name\":\"kit-tests\",\"private\":true}" > package.json && npm i -s typescript@5 esbuild react@18 react-dom@18 @types/react@18 @types/react-dom@18 >/dev/null)
fi
export NODE_PATH="$PWD/.node/node_modules"
ln -sfn .node/node_modules node_modules
./node_modules/.bin/tsc -p . && echo "tsc: OK (strict)"
for TAB in "Picks" "Calendar" "Save for later" "History" "Budget"; do
  sed "s/useState<string>(\"Picks\")/useState<string>(\"$TAB\")/" _page.tsx > _tab.tsx
  ./node_modules/.bin/esbuild _tab.tsx --bundle --format=esm --platform=node --alias:grok/canvas=./shim/grok-canvas.ts \
    --jsx=automatic --external:react --external:react-dom --external:react/jsx-runtime --outfile=_tab.mjs --log-level=error
  node -e "import('./_tab.mjs').then(async m=>{const R=await import('react');const S=await import('react-dom/server');const h=S.renderToString(R.createElement(m.default));const t=h.replace(/<style>[\s\S]*?<\/style>/,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ');console.log('render [$TAB]: OK ::',t.slice(0,240));})"
done
rm -f _tab.tsx _tab.mjs
