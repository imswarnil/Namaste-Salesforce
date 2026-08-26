/* ════════════════════════════════════════════════════════════════════════════
   check-icons.mjs — every {{> "icons/…"}} must have a partial.
   ----------------------------------------------------------------------------
   The inline-SVG equivalent of NSDS's check-icons.mjs, and it exists for the
   same reason: a missing icon does not render a box, it renders nothing —
   an invisible control that ships.

   Ghost is quieter about this than the icon font is. A missing partial throws
   at RENDER time, on one page, in production — not at build time on every
   page. So it gets caught here instead.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

function walk(dir, out = []) {
    for (const name of readdirSync(dir)) {
        if (name === 'node_modules' || name === '.git' || name === 'dist') continue;
        const p = join(dir, name);
        if (statSync(p).isDirectory()) walk(p, out);
        else if (p.endsWith('.hbs')) out.push(p);
    }
    return out;
}

const files = walk('.');
const used = new Map();
for (const file of files) {
    for (const m of readFileSync(file, 'utf8').matchAll(/\{\{>\s*"icons\/([a-z0-9-]+)"/g)) {
        if (!used.has(m[1])) used.set(m[1], new Set());
        used.get(m[1]).add(file);
    }
}

const missing = [...used].filter(([name]) => !existsSync(`partials/icons/${name}.hbs`));
if (missing.length) {
    console.error('✗ MISSING icon partials — these render as nothing at all:\n');
    for (const [name, where] of missing) {
        console.error(`  partials/icons/${name}.hbs`);
        for (const f of where) console.error(`      ${f}`);
    }
    console.error('\n  Draw it on the 24 grid at 1.7 stroke. partials/icons/README.md.');
    process.exit(1);
}

const all = readdirSync('partials/icons').filter(f => f.endsWith('.hbs')).map(f => f.slice(0, -4));
const unused = all.filter(n => !used.has(n));
console.log(`✓ ${used.size} icons used, all present`
    + (unused.length ? `  (${unused.length} drawn but unused: ${unused.join(', ')})` : ''));
