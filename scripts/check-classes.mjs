/* ════════════════════════════════════════════════════════════════════════════
   check-classes.mjs — every .ns-* a template uses must actually be defined.
   ----------------------------------------------------------------------------
   This is NSDS's own check-markup.mjs, pointed at Handlebars.

   The failure it catches is the quietest one in the project: a class name
   invented while porting an archetype — `.ns-trackcard` for `.ns-track-card`,
   `.ns-trainingnav` for `.ns-sidenav` — renders as unstyled markup. No error,
   no warning, and gscan passes because it is valid HTML. abstract/10 is the
   record of ~100 classes that got in this way.

   The vendored bundle is the authority: if a name is not in it, the theme
   either mistyped an NSDS class or is inventing one. Both are defects, and
   the second is the one this project exists to avoid.

   Genuinely new theme classes belong in assets/css/theme/*.css and are
   allowed — the check reads those too. It is the UNDEFINED name that fails.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

/* The vendored bundle plus EVERY file in the theme's own layer, discovered
   rather than listed — a hardcoded list means a new theme/*.css file is
   invisible to this check until somebody remembers to add it here, and the
   symptom is a false failure on a class that is in fact defined. */
const CSS = ['assets/css/namaste-ui.css',
    ...readdirSync('assets/css/theme').filter(f => f.endsWith('.css'))
        .map(f => join('assets/css/theme', f))];

function walk(dir, out = []) {
    for (const name of readdirSync(dir)) {
        if (name === 'node_modules' || name === '.git' || name === 'dist') continue;
        const p = join(dir, name);
        if (statSync(p).isDirectory()) walk(p, out);
        else if (p.endsWith('.hbs')) out.push(p);
    }
    return out;
}

const defined = new Set();
for (const f of CSS) {
    for (const m of readFileSync(f, 'utf8').matchAll(/\.(ns-[a-zA-Z0-9_-]+)/g)) defined.add(m[1]);
}

const missing = new Map();
for (const file of walk('.')) {
    const src = readFileSync(file, 'utf8');
    /* class="…" only. A bare ns- token in a comment or a data attribute is
       not a class and must not fail the build. */
    for (const attr of src.matchAll(/class="([^"]*)"/g)) {
        for (const cls of attr[1].split(/\s+/)) {
            /* Handlebars interpolation inside the attribute — {{#if}}…{{/if}}
               fragments — is not a class name. */
            if (!cls.startsWith('ns-') || cls.includes('{')) continue;
            if (defined.has(cls)) continue;
            if (!missing.has(cls)) missing.set(cls, new Set());
            missing.get(cls).add(file);
        }
    }
}

if (missing.size) {
    console.error('✗ UNDEFINED .ns-* classes — these render as bare markup:\n');
    for (const [cls, files] of [...missing].sort()) {
        console.error(`  .${cls}`);
        for (const f of files) console.error(`      ${f}`);
    }
    console.error('\n  Either it is a typo for an NSDS class — grep assets/css/namaste-ui.css —');
    console.error('  or the theme is inventing a name NSDS already has. See abstract/10.');
    process.exit(1);
}

console.log(`✓ every .ns-* class in the templates is defined  (${defined.size} available)`);
