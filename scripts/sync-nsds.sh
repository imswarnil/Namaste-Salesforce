#!/usr/bin/env bash
# ============================================================================
# sync-nsds.sh — vendor NS-Design-System into the theme.
# ----------------------------------------------------------------------------
# A Ghost theme ships as a self-contained zip: anything reaching outside the
# theme root resolves on your machine and 404s on the server. So everything
# NSDS provides is COPIED in, and this script is the copy. It also makes CI
# hermetic — the build does not need NS-Design-System checked out beside it.
#
#     ./scripts/sync-nsds.sh [path-to-NS-Design-System]
#
# WHAT LANDS WHERE, and why the two CSS files sit in assets/css/:
# the bundle's font and icon urls are `../fonts/…` and `../icons/…`. From
# assets/css/ that resolves to assets/fonts and assets/icons; from the
# COMPILED assets/built/ it resolves to the same two places. So the paths are
# right whether or not postcss rebases them during the inline — the sort of
# thing that otherwise only shows up as a 404 on a font nobody notices.
# ============================================================================
set -euo pipefail

DS="${1:-../../../../NS-Design-System}"
[ -d "$DS" ] || { echo "NS-Design-System not found at: $DS" >&2; exit 1; }

cp "$DS/dist/namaste-ui.css"  assets/css/namaste-ui.css
cp "$DS/tokens/tailwind.css"  assets/css/ns-tailwind.css
cp "$DS/fonts/"*.woff2        assets/fonts/
cp "$DS/fonts/FONTSHARE-EULA.txt" assets/fonts/
cp "$DS/fonts/licences/"*     assets/fonts/licences/
cp "$DS/icons/"*.woff2        assets/icons/
cp "$DS/icons/namaste-icons.svg" assets/icons/
for f in nav toc type-fx lms training rail tabs code theme-init; do
    cp "$DS/assets/js/$f.js" "assets/js/$f.js"
done

REV=$(cd "$DS" && git rev-parse --short HEAD)
DATE=$(cd "$DS" && git log -1 --format=%cs)
echo "vendored NS-Design-System @ $REV ($DATE)"
echo "→ npm run build, then LOOK AT A PAGE. gscan cannot see a visual regression."
