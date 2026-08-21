# 08 · The scripts

Everything in `scripts/`. All are run from `package.json`; none is a one-off.

---

## `sync-design.mjs` — the vendoring

```bash
yarn design:sync    # refresh the vendored copy
yarn design:check   # fail if it drifted (runs in pretest / CI)
```

Copies from `../../../../NS-Design-System` into the theme:

| from | to |
| --- | --- |
| `styles.css`, `tokens/`, `icons/`, `patterns/`, `components/css/` | `assets/css/nsds/` |
| `assets/js/*.js` | `assets/js/nsds/` |
| `fonts/*.woff2`, `icons/*.woff2` | `assets/fonts/` |
| `icons/namaste-icons.svg` | `assets/icons/` |
| `assets/js/theme-init.js` | **generated** into `partials/nsds/theme-init.hbs` |

**Design decisions worth keeping:**

- Copies **whole directories, discovered not hardcoded** — `styles.css` decides
  what it imports and that list grows upstream. A hardcoded subset breaks the
  build with an unresolved `@import` the next time a file is added.
- `--check` builds into a **temp directory, never in place**. A check that
  rebuilds over the working tree silently FIXES the drift it is meant to report
  and then passes on the next run.
- Only the CSS tree is fingerprinted. `assets/fonts/` and `assets/icons/` hold
  theme-owned files too, so hashing them would report drift on every addition.
- The ONE edit it makes to upstream bytes is rewriting `url()` values for this
  theme's nesting depth — see 04.
- **Fonts are copied, never pruned.** When upstream retires a face the stale
  woff2 lingers until removed by hand:
  `comm -23 <(ls assets/fonts) <(ls ../../../../NS-Design-System/fonts)`
- `theme-init.js`'s **leading banner comment is stripped** before inlining: it
  quotes `{{ghost_head}}`, and Ghost tries to parse that once it is inside a
  `.hbs`.

## `build-styleguide.py` — the living docs

Generates `styleguide/` — a static site rendered against the **real**
`assets/built/screen.css`, so it cannot drift from what ships. ~60 pages: one
per foundation topic, element family, component and module.

**Edit the generator, never the HTML.** Adding a component is adding one
`page(...)` call.

Two guardrails that have both caught real bugs:

- Specimens are written `<i class="ph ph-name">` because it is terser; the
  generator rewrites every one into the inline SVG from `partials/icons.hbs`
  and **fails the build on an unknown icon name**.
- **Fails on any inline CSS** in a specimen — a `style=` attribute hides what
  the component actually needs.

The styleguide DOCUMENTS the templates, so when markup moves onto a new
component the generator moves with it. It is not a separate source of truth.

⚠️ When bulk-editing this file with regex, do NOT run whitespace-normalising
substitutions over it — it is Python containing HTML strings, and a pattern
matching across a newline will corrupt the source. Token-only replacements,
then `python3 -c "import ast; ast.parse(open(...).read())"`.

## `fix-lexical-double-encoding.py`

A content repair for Ghost's Lexical format. Not part of the build.

## `demo.html`

A fragment to paste into a Ghost HTML card. Different thing from the
styleguide; it is for checking components inside the editor.
