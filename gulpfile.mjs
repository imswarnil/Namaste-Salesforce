/* ════════════════════════════════════════════════════════════════════════════
   gulpfile.mjs — the theme's build.
   ----------------------------------------------------------------------------
       npm run dev      watch and rebuild
       npm run build    one production build
       npm test         build, then gscan

   CSS   assets/css/screen.css → assets/built/screen.css
         Tailwind v4 through @tailwindcss/postcss, then cssnano in production.

   JS    assets/js/*.js → assets/built/main.js
         Concatenated in a fixed order, not bundled — these are NSDS's own
         plain IIFEs with no imports, and a bundler would add a dependency for
         no benefit. theme-init is NOT in it: that one must be inlined in
         <head> or it paints too late.

   ⚠ assets/built/ IS COMMITTED, because Ghost serves the theme as uploaded
   and there is no build step on the server. The risk that creates is a stale
   build, so CI rebuilds and fails if the output moved.
   ═══════════════════════════════════════════════════════════════════════ */

import { src, dest, watch, series, parallel } from 'gulp';
import postcss from 'gulp-postcss';
import concat from 'gulp-concat';
import tailwind from '@tailwindcss/postcss';
import cssnano from 'cssnano';
import { deleteAsync } from 'del';
import { execFileSync } from 'node:child_process';

const PROD = process.env.NODE_ENV === 'production';

/* Listed explicitly rather than globbed, so a new file in assets/js does not
   silently join the bundle — and so theme-init.js stays out of it. */
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
                discardComments: { removeAll: true },
                /* OFF: cssnano's default merges longhands into shorthands and
                   silently drops a custom property a longhand was holding —
                   and this sheet is almost entirely custom properties. */
                mergeLonghand: false,
            }],
        }));
    }
    return src('assets/css/screen.css').pipe(postcss(plugins)).pipe(dest('assets/built'));
}

export function js() {
    /* NOT allowEmpty. It was on once and silently produced a bundle of one
       file because the other six had never been copied in — a missing script
       does not fail, it just does not run. Let it throw. */
    return src(SCRIPTS).pipe(concat('main.js')).pipe(dest('assets/built'));
}

/* Runs on the OUTPUT — see scripts/check-layers.mjs for why the source would
   prove nothing. */
export function checkLayers(cb) {
    execFileSync('node', ['scripts/check-layers.mjs'], { stdio: 'inherit' });
    cb();
}

export const build = series(clean, parallel(css, js), checkLayers);

export function dev() {
    /* The .hbs glob matters as much as the .css one: Tailwind emits utilities
       from the class names it finds in templates, so editing a template
       changes the CSS. Miss this and a new utility does nothing until the
       next full build. */
    watch(['assets/css/**/*.css', '**/*.hbs', '!node_modules/**'], css);
    watch(SCRIPTS, js);
}

export default series(build, dev);
