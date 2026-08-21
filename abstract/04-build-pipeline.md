# 04 · The build pipeline

```bash
yarn install       # Yarn; package-lock.json is gitignored
yarn dev           # gulp default: build + livereload watch
yarn build         # one-off build into assets/built/
yarn design:sync   # re-vendor NS-Design-System → assets/css/nsds + js/nsds
yarn design:check  # fail if the vendored copy drifted (runs in pretest)
yarn preview       # build + styleguide + serve at 127.0.0.1:4321
yarn styleguide    # regenerate styleguide/ only
yarn test          # gscan . — validate against Ghost's theme rules
yarn zip           # build + package into dist/
```

`gulp build` runs three steps, all output to **`assets/built/`, which is
COMMITTED** — Ghost serves it directly. **Rebuild and commit the built output
after changing CSS, JS or any `.hbs`** (Tailwind scans templates for classes).

| step | in | out |
| --- | --- | --- |
| css | `assets/css/screen.css` → `@tailwindcss/postcss` → cssnano | `built/screen.css` |
| js | `assets/js/*.js` concatenated → uglify | `built/casper.js` |
| locales | merges `locales-local/` into `locales/` | |

**`assets/js/nsds/*` is NOT bundled.** Those are independent modules on their
own `<script defer>` so a page pays only for what it uses and load order stays
explicit. Ditto `assets/js/vendor/alpine.js`.

There is **no `tailwind.config.js`** — tokens and `@source` globs live in
`screen.css`. Tailwind v4 emits its own vendor prefixes; autoprefixer is not
used.

## ⚠️ The `url()` gotcha

The pipeline rebases relative urls and **consumes exactly one `../`**. A font
referenced as `../../../fonts/x.woff2` in a vendored stylesheet emits
`../../fonts/x.woff2` in `built/screen.css`, which is what resolves.
`sync-design.mjs` rewrites upstream's font urls for this, controlled by one
constant, `FONT_URL_DEPTH`.

Check after touching font paths:

```bash
yarn build && grep -o 'url([^)]*)' assets/built/screen.css
```

## Testing means gscan, and gscan is not enough

`yarn test` runs `gscan`, which validates Handlebars and Ghost's theme rules.
`pretest` runs `gulp build` first, so the committed output is what gets
validated.

**What gscan does NOT catch, and what actually broke this theme:**

- a script whose selectors no longer match the markup — the feature silently
  stops working and every check still passes
- a class in the markup with no rule behind it
- anything about how the page LOOKS

Two greps worth running, which caught real bugs here:

```bash
# markup classes with no CSS behind them
grep -rhoE 'ns-[a-z0-9-]+' --include='*.hbs' partials *.hbs | sort -u \
  | while read c; do grep -qF "$c" assets/built/screen.css || echo "MISSING $c"; done

# the cascade-layer invariant (see 05)
grep -o '@layer[^;{]*;' assets/built/screen.css | head -3
```

**None of it replaces opening the site in a browser.** Everything static can
pass while every page looks wrong. That is what happened.
