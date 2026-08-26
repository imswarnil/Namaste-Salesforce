/* ════════════════════════════════════════════════════════════════════════════
   check-layers.mjs — re-prove the cascade contract on the COMPILED css.
   ----------------------------------------------------------------------------
   assets/css/screen.css declares

       @layer theme, base, ns-components, components, utilities;

   before its imports. That statement is then MINIFIED AWAY — once the blocks
   are emitted in the right order it is redundant, so cssnano drops it. Which
   means the only remaining record of the contract in the shipped file is THE
   ORDER THE BLOCKS APPEAR IN, and nothing in the pipeline guarantees that.

   It has already been wrong once here. Without the bare statement the order
   came out

       theme → base → components → utilities → ns-components

   with the design system LAST — beating this theme's own layer and every
   Tailwind utility. No error, no warning; overrides just stop working, and
   abstract/04 records that the project shipped exactly that bug before.

   So the check runs on the OUTPUT. Checking the source would only prove the
   statement was written, which was never the failing part.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync } from 'node:fs';

const FILE = 'assets/built/screen.css';
const WANT = ['theme', 'base', 'ns-components', 'components', 'utilities'];

let css;
try {
    css = readFileSync(FILE, 'utf8');
} catch {
    console.error(`✗ ${FILE} not found — run \`npm run build\` first.`);
    process.exit(1);
}

/* ── Declared order beats emitted order ───────────────────────────────────
   A bare `@layer a, b, c;` statement fixes the precedence outright: where the
   BLOCKS then appear is irrelevant, and the browser honours the statement.

   In a development build the statement survives, and the blocks legitimately
   come out in a different order — Tailwind emits its utilities early, so the
   raw file reads theme → base → utilities → ns-components → components while
   behaving as theme → base → ns-components → components → utilities.

   cssnano DROPS the statement in production, once the blocks have been
   reordered to match it. That is the build where block order becomes the only
   surviving evidence, and it is the build this check exists for.

   Checking block order unconditionally fails every dev build — and a check
   that cries wolf in the edit loop is a check someone deletes. So: look for
   the statement first, and only fall through to the blocks when it is gone. */
const statement = new RegExp('@layer\\s+' + WANT.join('\\s*,\\s*') + '\\s*;');
if (statement.test(css)) {
    console.log(`✓ cascade contract holds — declared: ${WANT.join(' → ')}`);
    process.exit(0);
}

const seen = [];
for (const m of css.matchAll(/@layer\s+([a-zA-Z-]+)\s*\{/g)) {
    if (!seen.includes(m[1])) seen.push(m[1]);
}

/* A SUBSEQUENCE check, not an equality one. A layer that emits nothing emits
   no block: with no templates yet Tailwind produces no utilities, so
   `utilities` is legitimately absent. What must never happen is two present
   layers appearing in the WRONG ORDER relative to each other — that is the
   failure this file exists to catch, and requiring all five would have made
   the check cry wolf on an empty theme and get switched off. */
const actual = seen.filter(n => WANT.includes(n));
const ordered = actual.every((n, i) =>
    i === 0 || WANT.indexOf(actual[i - 1]) < WANT.indexOf(n));

if (!ordered) {
    console.error('✗ CASCADE CONTRACT BROKEN in ' + FILE);
    console.error('  expected order: ' + WANT.join(' → '));
    console.error('  actual         : ' + (actual.join(' → ') || '(no layers found)'));
    console.error('  Check that screen.css still opens with the bare @layer');
    console.error('  statement BEFORE any @import. See abstract/04.');
    process.exit(1);
}

const missing = WANT.filter(n => !actual.includes(n));

/* An unlayered rule beats every layered rule at any specificity, so one stray
   rule silently revokes the order above. Everything before the first @layer
   block should be at-rules only. */
const firstLayer = css.indexOf('@layer');
const preamble = css.slice(0, firstLayer < 0 ? css.length : firstLayer).trim();
const strays = preamble.replace(/@[a-z-]+[^;{]*(;|\{[^}]*\})/g, '').trim();
if (strays) {
    console.error('✗ UNLAYERED CSS before the first @layer block:');
    console.error('  ' + strays.slice(0, 200));
    process.exit(1);
}

console.log(`✓ cascade contract holds — ${actual.join(' → ')}`
    + (missing.length ? `  (not emitted: ${missing.join(', ')})` : ''));
