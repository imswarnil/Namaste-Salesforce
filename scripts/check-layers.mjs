/* ════════════════════════════════════════════════════════════════════════════
   check-layers.mjs — re-prove the cascade contract on the COMPILED css.
   ----------------------------------------------------------------------------
       node scripts/check-layers.mjs

   WHY THIS EXISTS. `assets/css/screen.css` declares

       @layer theme, base, ns-components, components, utilities;

   before its imports. That statement is then MINIFIED AWAY — once the layer
   blocks are emitted in the right order the statement is redundant, so
   cssnano drops it. Which means the only remaining record of the contract in
   the shipped file is THE ORDER THE BLOCKS APPEAR IN, and nothing in the
   pipeline guarantees that stays right.

   It has already been wrong once here. Without the bare statement the order
   came out

       theme → base → components → utilities → ns-components

   with the design system LAST — beating this theme's own layer and every
   Tailwind utility. No error, no warning; overrides just stop working, and
   `abstract/05` records that the project shipped exactly that bug before.

   So the check runs on the OUTPUT, not the source. Checking the source would
   only prove the statement was written, which was never the failing part.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync } from 'node:fs';

const FILE = 'assets/built/screen.css';
const WANT = ['theme', 'base', 'ns-components', 'components', 'utilities'];

let css;
try {
    css = readFileSync(FILE, 'utf8');
} catch {
    console.error(`✗ ${FILE} not found — run \`gulp build\` first.`);
    process.exit(1);
}

/* Order of FIRST APPEARANCE is what CSS uses to order layers when there is no
   bare statement, so that is what gets measured. */
const seen = [];
for (const m of css.matchAll(/@layer\s+([a-zA-Z-]+)\s*\{/g)) {
    if (!seen.includes(m[1])) seen.push(m[1]);
}

const actual = seen.filter(n => WANT.includes(n));
const ok = WANT.every((n, i) => actual[i] === n);

if (!ok) {
    console.error('✗ CASCADE CONTRACT BROKEN in ' + FILE);
    console.error('  expected: ' + WANT.join(' → '));
    console.error('  actual  : ' + (actual.join(' → ') || '(no layers found)'));
    console.error('');
    console.error('  Check that assets/css/screen.css still opens with the bare');
    console.error('  @layer statement BEFORE any @import. See abstract/05.');
    process.exit(1);
}

/* An unlayered rule beats every layered rule at any specificity, so one stray
   rule silently revokes the order above. Everything before the first @layer
   block should be at-rules only — charset, imports, font-face, properties. */
const firstLayer = css.indexOf('@layer');
const preamble = css.slice(0, firstLayer < 0 ? css.length : firstLayer).trim();
const strays = preamble.replace(/@[a-z-]+[^;{]*(;|\{[^}]*\})/g, '').trim();

if (strays.length > 0) {
    console.error('✗ UNLAYERED CSS before the first @layer block in ' + FILE);
    console.error('  ' + strays.slice(0, 200));
    process.exit(1);
}

console.log(`✓ cascade contract holds — ${actual.join(' → ')}`);
