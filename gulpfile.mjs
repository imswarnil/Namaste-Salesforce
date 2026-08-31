/* ════════════════════════════════════════════════════════════════════════════
   gulpfile.mjs — the theme's build.
   ----------------------------------------------------------------------------
       npm run dev      build, watch, and serve with live reload
       npm run build    one production build
       npm test         build, then gscan

   CSS   assets/css/screen.css      → assets/built/screen.min.css
   JS    assets/js/0-vendor/*.js    → assets/built/main.min.js

   ── WHY THE OUTPUT IS ALWAYS CALLED .min ─────────────────────────────────
   Handlebars cannot see NODE_ENV, so default.hbs has to name ONE file. Two
   names would mean either a runtime switch the platform does not offer, or a
   template edit between dev and deploy — and a template edit that only
   happens at deploy time is a template edit that gets forgotten.

   So the name is constant and the CONTENTS change: readable in development,
   minified in production. `.min` is a promise about the shipped file, and
   the shipped file is always built with NODE_ENV=production.

   ⚠ assets/built/ IS COMMITTED, because Ghost serves the theme as uploaded
   and there is no build step on the server. The risk that creates is a stale
   build, so CI rebuilds and fails if the output moved.
   ═══════════════════════════════════════════════════════════════════════ */

import { src, dest, watch, series, parallel } from 'gulp';
import postcss from 'gulp-postcss';
import concat from 'gulp-concat';
import terser from 'gulp-terser';
import tailwind from '@tailwindcss/postcss';
import cssnano from 'cssnano';
import { deleteAsync } from 'del';
import { execFileSync } from 'node:child_process';
import browserSync from 'browser-sync';

const PROD = process.env.NODE_ENV === 'production';
const GHOST = process.env.GHOST_URL || 'http://localhost:2369';
const bs = browserSync.create();

/* Listed explicitly rather than globbed, so a new file in 0-vendor does not
   silently join the bundle — and so theme-init.js stays OUT of it. That one
   must be inlined in <head>; in a deferred bundle it paints too late, which
   is the white-flash-on-every-navigation bug it exists to prevent.

   Order is load order. nav first because it owns the chrome. */
const SCRIPTS = [
    'assets/js/0-vendor/nav.js',
    'assets/js/0-vendor/toc.js',
    'assets/js/0-vendor/type-fx.js',
    'assets/js/0-vendor/lms.js',
    'assets/js/0-vendor/training.js',
    'assets/js/0-vendor/rail.js',
    'assets/js/0-vendor/tabs.js',
    'assets/js/0-vendor/code.js',
    /* The theme's own scripts load after the design system's, so they can
       assume its behaviour is already wired. Empty today. */
    'assets/js/1-theme/*.js',
];

export function clean() {
    return deleteAsync(['assets/built']);
}

/* ── The generated icon bridge ─────────────────────────────────────────────
   NSDS styles 85 icon rules by ELEMENT (`.ns-code__btn i`) because it was
   written against an icon font; this theme draws inline SVG, so each of those
   rules misses and the icon renders unstyled rather than not at all. */
export function iconBridge(cb) {
    execFileSync('node', ['scripts/build-icon-bridge.mjs'], { stdio: 'inherit' });
    cb();
}

export function css() {
    const plugins = [tailwind()];
    if (PROD) {
        plugins.push(cssnano({
            preset: ['default', {
                discardComments: { removeAll: true },
                /* OFF: cssnano's default merges longhands into shorthands and
                   silently drops a custom property a longhand was holding —
                   and this sheet is almost entirely custom properties. */
                mergeLonghand: false,
            }],
        }));
    }
    return src('assets/css/screen.css')
        .pipe(postcss(plugins))
        .pipe(concat('screen.min.css'))
        .pipe(dest('assets/built'))
        .pipe(bs.stream());
}

export function js() {
    /* NOT allowEmpty on the vendored files. It was on once and silently
       produced a bundle of one file because the other six had never been
       copied in — a missing script does not fail, it just does not run. */
    let stream = src(SCRIPTS).pipe(concat('main.min.js'));
    if (PROD) stream = stream.pipe(terser({ format: { comments: false } }));
    return stream.pipe(dest('assets/built'));
}

/* Runs on the OUTPUT — see scripts/check-layers.mjs for why the source would
   prove nothing. */
export function checkLayers(cb) {
    execFileSync('node', ['scripts/check-layers.mjs'], { stdio: 'inherit' });
    cb();
}

/* All three catch failures that RENDER — an undefined class renders as bare
   markup, a missing icon partial renders as nothing, and a template
   routes.yaml names but the theme lacks renders as index.hbs — which is why
   neither gscan nor a green build sees them. */
export function checkMarkup(cb) {
    execFileSync('node', ['scripts/check-classes.mjs'], { stdio: 'inherit' });
    execFileSync('node', ['scripts/check-icons.mjs'], { stdio: 'inherit' });
    execFileSync('node', ['scripts/check-routes.mjs'], { stdio: 'inherit' });
    cb();
}

/* Fonts and icons 404 in the browser and nowhere else. Runs on the OUTPUT,
   because postcss rewrites the paths on the way there. */
export function checkAssets(cb) {
    execFileSync('node', ['scripts/check-assets.mjs'], { stdio: 'inherit' });
    cb();
}

export const build = series(
    clean, iconBridge, parallel(css, js), checkLayers, checkMarkup, checkAssets,
);

/* ── The dev server ────────────────────────────────────────────────────────
   Ghost renders the site; browser-sync PROXIES it. It is not serving files
   itself — a static server would have no Handlebars, no Members and no
   {{ghost_head}}, which is most of what there is to look at.

   CSS is injected without a reload (bs.stream in the css task), so a style
   change does not lose your scroll position or close an open menu. Templates
   and scripts cannot be injected, so those reload the page. */
export function serve(cb) {
    bs.init({
        proxy: GHOST,
        port: 4000,
        open: false,
        notify: false,
        ghostMode: false,
        /* Ghost fingerprints assets with ?v=; without this browser-sync
           serves the previous file from cache and the change looks lost. */
        rewriteRules: [{ match: /\?v=[a-f0-9]+/g, fn: () => '?v=' + Date.now() }],
    }, cb);
}

export function dev() {
    /* The .hbs glob matters as much as the .css one: Tailwind emits utilities
       from the class names it finds in templates, so editing a template
       changes the CSS. Miss this and a new utility does nothing until the
       next full build. */
    watch(['assets/css/**/*.css', '**/*.hbs', '!node_modules/**', '!assets/built/**'], css);
    watch(['assets/js/**/*.js', '!assets/js/theme-init.js'], series(js, reload));
    watch(['**/*.hbs', 'routes.yaml', '!node_modules/**'], series(checkMarkup, reload));
}

function reload(cb) { bs.reload(); cb(); }

export default series(build, serve, dev);
