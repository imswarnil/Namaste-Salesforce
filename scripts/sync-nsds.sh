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
#
# ── THE FONT AND ICON DIRECTORIES ARE WIPED, NOT MERGED. ───────────────────
# A plain `cp` only ever ADDS. When NSDS 3.0 replaced Switzer + Roboto Mono
# with a single Figtree, a merging sync would have left both old woff2s and
# the Fontshare EULA sitting in assets/fonts/ — unreferenced by any
# @font-face, invisible to every check in the build (check-assets.mjs proves
# that referenced files EXIST, not that existing files are REFERENCED), and
# shipped in the zip forever. Upstream owns what faces the system has; this
# directory is a mirror of that, so it is replaced wholesale each sync.
# ============================================================================
set -euo pipefail

DS="${1:-../../../../NS-Design-System}"
[ -d "$DS" ] || { echo "NS-Design-System not found at: $DS" >&2; exit 1; }

# ── CSS ─────────────────────────────────────────────────────────────────────
# dist/nsds.css is the flat bundle (imports already inlined); src/tokens/
# tailwind.css is the @theme bridge that maps the tokens onto Tailwind's
# names. NOT dist/nsds.tailwind.css — that is Tailwind PLUS the system, built
# for NSDS's own styleguide, and this theme already runs Tailwind itself.
# See docs/INTEGRATION.md in the design system.
cp "$DS/dist/nsds.css"           assets/css/nsds/nsds.css
cp "$DS/src/tokens/tailwind.css" assets/css/nsds/tailwind.css

# ── REBASE THE ASSET URLS. Do not remove. ───────────────────────────────────
# The bundle ships `url("../fonts/…")`, which is correct when it sits directly
# in assets/css/. It lives one level deeper, in assets/css/nsds/, so the same
# string points at assets/css/fonts/ — which does not exist.
#
# It matters because POSTCSS REBASES these during the @import inline: it
# resolves the url against the file it came from, then rewrites it relative to
# the entry point. Feed it a path that is already wrong and it faithfully
# emits a wrong path into assets/built/screen.min.css — with a green build, a
# green gscan, and a 404 on every font that only shows up in a browser.
# scripts/check-assets.mjs is the guard; this sed is the fix.
sed -i '' 's|url("\.\./fonts/|url("../../fonts/|g; s|url("\.\./icons/|url("../../icons/|g' \
    assets/css/nsds/nsds.css

# ── Fonts and icons — mirrored, see the header note ─────────────────────────
rm -rf assets/fonts assets/icons
mkdir -p assets/fonts/licences assets/icons
cp "$DS/fonts/"*.woff2        assets/fonts/
cp "$DS/fonts/licences/"*     assets/fonts/licences/
cp "$DS/icons/"*.woff2        assets/icons/
cp "$DS/icons/namaste-icons.svg" assets/icons/

# ── Scripts — MIRRORED, like the fonts and icons above ──────────────────────
# This used to be a hardcoded list of eight. That is the same shape of bug the
# font directory note describes, pointing the other way: a plain list only
# ever copies what someone REMEMBERED, so a module upstream adds is missing
# here until somebody notices — and "notices" means a control that renders and
# does nothing, which is the failure this repo keeps paying for.
#
# So the directory is mirrored. Upstream owns which behaviours the system has.
#
# ⚠ VENDORED IS NOT THE SAME AS BUNDLED. Everything upstream ships lands in
# assets/js/0-vendor/, but gulpfile.mjs's SCRIPTS list decides what is
# CONCATENATED into main.min.js, and it is deliberately shorter: a script that
# binds to markup no template emits is dead weight on every page load. Adding
# the markup means adding the script to SCRIPTS in the same commit, and
# scripts/check-behaviour.mjs fails the build if you forget.
#
# theme-init stays at the top level: it is INLINED into <head> rather than
# bundled, so it is not part of the vendored script layer.
rm -rf assets/js/0-vendor
mkdir -p assets/js/0-vendor
for f in "$DS/assets/js/"*.js; do
    base=$(basename "$f")
    [ "$base" = "theme-init.js" ] && continue
    cp "$f" "assets/js/0-vendor/$base"
done
cp "$DS/assets/js/theme-init.js" assets/js/theme-init.js
echo "vendored $(ls assets/js/0-vendor | wc -l | tr -d ' ') behaviour modules"

# ── The preload check ───────────────────────────────────────────────────────
# default.hbs names the above-the-fold font by filename, and a preload for a
# file that no longer exists is a silent console warning plus a wasted
# request. The build's check-assets.mjs cannot see it: it parses url() in the
# stylesheet, and a preload is markup.
for f in $(grep -o 'fonts/[a-z0-9.-]*\.woff2' default.hbs | sort -u); do
    [ -f "assets/$f" ] || echo "⚠ default.hbs preloads assets/$f, which upstream no longer ships" >&2
done

REV=$(cd "$DS" && git rev-parse --short HEAD)
DATE=$(cd "$DS" && git log -1 --format=%cs)
echo "vendored NS-Design-System @ $REV ($DATE)"
echo "→ npm run build, then LOOK AT A PAGE. gscan cannot see a visual regression."
