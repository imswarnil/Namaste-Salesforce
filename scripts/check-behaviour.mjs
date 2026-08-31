/* ════════════════════════════════════════════════════════════════════════════
   check-behaviour.mjs — markup that needs a script must ship that script.
   ----------------------------------------------------------------------------
   THE BUG THIS EXISTS FOR, which this project has now paid for twice:

     · A control renders and does nothing. The training rail shipped for weeks
       with every collapse hook in main.min.js and no markup emitting them —
       and the mirror image is one line of a template away: paste NSDS's
       search palette or video player into a partial, forget to add search.js
       or video.js to SCRIPTS, and the page renders a perfect dead control.
       No error, no console warning, green build, green gscan.

   NSDS is VENDORED WHOLE — all 13 behaviour modules land in assets/js/0-vendor/
   so nothing is missing when a surface needs it. But only the modules in
   gulpfile.mjs's SCRIPTS list are CONCATENATED into main.min.js, because a
   script bound to markup no template emits is dead weight on every page load.

   That split is the right one and it needs exactly this guard: the moment a
   template starts emitting a module's hooks, that module has to be bundled.

   ── HOW A MODULE IS MATCHED TO ITS MARKUP ───────────────────────────────────
   By its data-ns-* attributes, which are behaviour hooks and nothing else. A
   .ns-* class is a STYLING decision and several modules touch generic ones
   (search.js reads .ns-btn--ghost), so matching on classes would fire on any
   page with a button. Five modules bind by class rather than attribute; those
   carry an explicit root selector below, chosen to be distinctive.

   Reported both ways round: a MISSING module fails the build, an UNUSED one
   is only noted. Unused costs bytes; missing costs a broken control.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

/* Modules that bind by class, not attribute. Distinctive roots only. */
const CLASS_HOOKS = {
    'ai':      ['ns-aisuggest', 'ns-aiwelcome', 'ns-aithinking'],
    'code':    ['ns-code__tab'],
    'tabs':    ['ns-tabs'],
    'toc':     ['ns-toc'],
    'type-fx': ['ns-scramble', 'ns-curve', 'ns-circle'],
};

function walk(dir, out = []) {
    for (const name of readdirSync(dir)) {
        if (['node_modules', '.git', 'dist', 'assets'].includes(name)) continue;
        const p = join(dir, name);
        if (statSync(p).isDirectory()) walk(p, out);
        else if (p.endsWith('.hbs')) out.push(p);
    }
    return out;
}

const markup = walk('.').map(f => readFileSync(f, 'utf8')).join('\n');

/* What gulp actually bundles. Parsed rather than duplicated — a second list
   would be one more thing to keep in sync, which is the bug above again. */
const gulpfile = readFileSync('gulpfile.mjs', 'utf8');
const scriptsBlock = gulpfile.slice(gulpfile.indexOf('const SCRIPTS'));
const bundled = new Set(
    [...scriptsBlock.slice(0, scriptsBlock.indexOf(']')).matchAll(/0-vendor\/([a-z-]+)\.js/g)]
        .map(m => m[1])
);

const vendored = readdirSync('assets/js/0-vendor').filter(f => f.endsWith('.js'))
    .map(f => f.replace(/\.js$/, ''));

const missing = [], unused = [];

for (const mod of vendored) {
    const src = readFileSync(`assets/js/0-vendor/${mod}.js`, 'utf8');
    const attrs = [...new Set([...src.matchAll(/data-ns-[a-z-]+/g)].map(m => m[0]))];
    const hooks = attrs.length ? attrs : (CLASS_HOOKS[mod] ?? []);
    if (!hooks.length) continue;                       // nothing to match on

    const hit = hooks.find(h => markup.includes(h));
    if (hit && !bundled.has(mod)) missing.push({ mod, hit });
    if (!hit && bundled.has(mod)) unused.push(mod);
}

for (const { mod, hit } of missing) {
    console.error(
        `::error::A template emits "${hit}", which ${mod}.js binds — but ${mod}.js is not in ` +
        `SCRIPTS in gulpfile.mjs, so it is not in main.min.js. The control will render and do ` +
        `nothing. Add 'assets/js/0-vendor/${mod}.js' to SCRIPTS.`
    );
}

if (missing.length) process.exit(1);

console.log(`✓ every behaviour the markup asks for is bundled  (${bundled.size} of ${vendored.length} vendored modules in main.min.js)`);
if (unused.length) console.log(`    bundled but no markup uses them yet: ${unused.join(', ')}`);
