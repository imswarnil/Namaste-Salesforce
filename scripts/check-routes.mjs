/* ════════════════════════════════════════════════════════════════════════════
   check-routes.mjs — every template routes.yaml names must exist.
   ----------------------------------------------------------------------------
   THE CHECK THAT WOULD HAVE CAUGHT THE /courses/ AND /docs/ REGRESSION.

   Ghost does not validate a `template:` key. Name a template that is not in
   the theme and Ghost does not warn, does not log and does not 404 — it falls
   back to index.hbs and serves the page. So the failure is not an error, it
   is a WRONG PAGE: /courses/ and /docs/ were served as the blog grid, with
   .ns-bcard covers and reading times, for as long as the templates were
   missing. Nothing in the build, in gscan, or in a green CI run saw it,
   because every one of them was in fact green.

   That is the same silent-failure shape as check-classes and check-icons:
   the page RENDERS, so only a check that knows what it should have been can
   tell. routes.yaml says this rule in its own header — this is the rule
   being enforced rather than merely written down.

   ── WHY THIS PARSES BY HAND ─────────────────────────────────────────────────
   `yaml` is present in the tree but only as a transitive dependency, and a
   check that silently stops running when someone prunes the lockfile is
   worse than no check. routes.yaml is a file this repo fully controls and
   whose shape is fixed by Ghost, so a line scanner for the two forms Ghost
   accepts is enough:

       /blog/:                  |   /:  home
         template: blog         |   (the one-line shorthand)

   ⚠ routes.yaml is NOT in the theme zip — Ghost stores it separately. This
   check therefore proves the COMMITTED file is self-consistent, which is not
   the same as proving the file uploaded to Ghost Admin is. Those two drifted
   apart once already; see the header of routes.yaml.
   ═══════════════════════════════════════════════════════════════════════ */

import { readFileSync, existsSync } from 'node:fs';

const lines = readFileSync('routes.yaml', 'utf8').split('\n');

/* path → template, in source order, so an error can name the line. */
const named = [];
let currentPath = null;

lines.forEach((raw, i) => {
    const line = raw.replace(/#.*$/, '').trimEnd();
    if (!line.trim()) return;

    /* `  /blog/:` — opens a block. Also `  /: home`, the shorthand. */
    const block = line.match(/^\s{2}(\/[^\s:]*):\s*(\S+)?\s*$/);
    if (block) {
        currentPath = block[1];
        if (block[2]) named.push({ path: currentPath, template: block[2], line: i + 1 });
        return;
    }

    const tpl = line.match(/^\s{4,}template:\s*(\S+)\s*$/);
    if (tpl && currentPath) named.push({ path: currentPath, template: tpl[1], line: i + 1 });
});

if (!named.length) {
    console.error('::error::check-routes parsed no templates out of routes.yaml — the parser and the file have diverged.');
    process.exit(1);
}

const missing = named.filter(n => !existsSync(`${n.template}.hbs`));

for (const m of missing) {
    console.error(
        `::error file=routes.yaml,line=${m.line}::${m.path} names template "${m.template}", ` +
        `but ${m.template}.hbs does not exist. Ghost will serve index.hbs instead — the page will ` +
        `render, and render wrong.`
    );
}

if (missing.length) process.exit(1);

console.log(`✓ every template routes.yaml names exists  (${named.length} routes)`);
for (const n of named) console.log(`    ${n.path.padEnd(20)} → ${n.template}.hbs`);
