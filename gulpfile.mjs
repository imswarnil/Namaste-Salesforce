/* ════════════════════════════════════════════════════════════════════════════
   gulpfile.mjs — the theme's build.
   ----------------------------------------------------------------------------
       gulp            watch and rebuild (development)
       gulp build      one production build
       gulp zip        build, validate, package for upload

   WHAT IT DOES, AND WHY EACH STEP IS HERE

   CSS   assets/css/screen.css → assets/built/screen.css
         Tailwind v4 through @tailwindcss/postcss, then cssnano in production.
         postcss-import runs FIRST because Tailwind needs to see the whole
         sheet — including the design system's `@layer ns-components` — before
         it decides which utilities to emit and where to put them.

   JS    assets/js/*.js → assets/built/main.js
         Concatenated in a fixed order, not bundled: these are NSDS's own
         scripts, they are plain IIFEs with no imports, and a bundler here
         would add a build dependency for no benefit. theme-init is NOT in
         this file — it must be inlined in <head> or it paints too late.

   ⚠ assets/built/ IS COMMITTED. Ghost serves the theme as uploaded; there is
   no build step on the server. The cost is that a stale build ships CSS the
   source does not describe — so CI rebuilds and fails if the output changed,
   which is the guard that makes committing it safe.
   ═══════════════════════════════════════════════════════════════════════ */

import { src, dest, watch, series, parallel } from 'gulp';
import postcss from 'gulp-postcss';
import concat from 'gulp-concat';
import tailwind from '@tailwindcss/postcss';
import cssnano from 'cssnano';
import { deleteAsync } from 'del';
import { execFileSync } from 'node:child_process';

const PROD = process.env.NODE_ENV === 'production';

/* Order matters only in that theme-init is excluded — everything else is an
   independent IIFE. Listed explicitly rather than globbed so a new file in
   assets/js does not silently join the bundle. */
const SCRIPTS = [
    'assets/js/nav.js',
    'assets/js/toc.js',
    'assets/js/type-fx.js',
    'assets/js/lms.js',
    'assets/js/training.js',
    'assets/js/rail.js',
    'assets/js/tabs.js',
    'assets/js/code.js',
];

export function clean() {
    return deleteAsync(['assets/built']);
}

export function css() {
    const plugins = [tailwind()];
    if (PROD) {
        plugins.push(cssnano({
            preset: ['default', {
                /* Comments in the design system carry its reasoning, but they
                   are for the repo, not for every reader on every page. */
                discardComments: { removeAll: true },
                /* OFF: cssnano's default merges longhands into shorthands,
                   which silently drops a custom property that a longhand was
                   holding — and this stylesheet is almost entirely custom
                   properties. */
                mergeLonghand: false,
            }],
        }));
    }
    return src('assets/css/screen.css')
        .pipe(postcss(plugins))
        .pipe(dest('assets/built'));
}

export function js() {
    /* NOT allowEmpty. It was on, and it silently produced a bundle containing
       one of the seven listed files because the other six had never been
       copied into this theme — a missing script does not fail, it just does
       not run, and the feature it drives quietly does nothing. Let it throw. */
    return src(SCRIPTS)
        .pipe(concat('main.js'))
        .pipe(dest('assets/built'));
}

/* The layer check runs on the OUTPUT, so it has to come after css. See
   scripts/check-layers.mjs for why checking the source would prove nothing. */
export function checkLayers(cb) {
    execFileSync('node', ['scripts/check-layers.mjs'], { stdio: 'inherit' });
    cb();
}

export const build = series(clean, parallel(css, js), checkLayers);

export function dev() {
    /* The .hbs glob matters as much as the .css one: Tailwind emits utilities
       based on the class names it finds in the templates, so editing a
       template changes the CSS. Miss this and a new utility silently does
       nothing until the next full build. */
    watch(['assets/css/**/*.css', '**/*.hbs', '!node_modules/**'], css);
    watch(SCRIPTS, js);
}

export default series(build, dev);
