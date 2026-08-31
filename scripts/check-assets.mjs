/* ════════════════════════════════════════════════════════════════════════════
   check-assets.mjs — every url() in the SHIPPED css must resolve to a file.
   ----------------------------------------------------------------------------
   This exists because moving the vendored bundle one directory deeper broke
   every font and icon on the site, and NOTHING caught it: gulp was green,
   gscan was green, the cascade check passed, the class and icon checks passed.
   The only symptom was four 404s in a network panel nobody had open, and text
   silently falling back to a system face.

   The cause is that postcss REBASES url() while inlining @import — it resolves
   each url against the file it came from and rewrites it relative to the entry
   point. So the correctness of a font path depends on how deep its stylesheet
   sits, which is not a property anyone thinks about when reorganising folders.

   So: parse the OUTPUT, resolve every url() the way a browser would — relative
   to assets/built/, where the stylesheet is served from — and require the file
   to exist. data: and remote urls are skipped; a remote one would be a
   different bug, and abstract/05 is why there are none.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

const FILE = 'assets/built/screen.min.css';
const BASE = dirname(FILE);

let css;
try {
    css = readFileSync(FILE, 'utf8');
} catch {
    console.error(`✗ ${FILE} not found — run \`npm run build\` first.`);
    process.exit(1);
}

const seen = new Map();
for (const m of css.matchAll(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g)) {
    const raw = m[2].trim();
    if (/^(data:|https?:|\/\/|#)/.test(raw)) continue;
    const clean = raw.split(/[?#]/)[0];
    if (!clean) continue;
    seen.set(clean, resolve(BASE, clean));
}

const missing = [...seen].filter(([, abs]) => !existsSync(abs));

if (missing.length) {
    console.error(`✗ ${missing.length} url() in ${FILE} do not resolve:\n`);
    for (const [raw, abs] of missing) {
        console.error(`  url(${raw})`);
        console.error(`      → ${abs}`);
    }
    console.error('\n  These 404 in the browser and nowhere else. If the vendored bundle');
    console.error('  moved, fix the rebase in scripts/sync-nsds.sh rather than here.');
    process.exit(1);
}

console.log(`✓ all ${seen.size} url() in the built css resolve`);
