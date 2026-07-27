# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A custom **Ghost** publishing-platform theme ("Namaste Salesforce"), originally forked from Casper but rebuilt for a Salesforce learning site. Templates are Handlebars (`.hbs`); styling is **Tailwind CSS v4** (no Bulma, no SCSS framework). Light interactivity uses **Alpine.js** (self-hosted). The design language is the **"Developer Console" design system**, built as numbered layers: `assets/css/0-foundation/` (tokens/vars/mixins only), `assets/css/1-elements/` (bare HTML, one file per element family), `assets/css/2-components/` (the UI library, one file per component with its full variant set), `assets/css/3-modules/` (per-feature styling). Each layer has an `index.css` listing its files; `screen.css` imports the four indexes and nothing else. **Living docs at `/docs/design-system/`** — a regular docs section: 17 posts (Introduction, Colors, Typography, …, per-element and per-component pages) shipped as `dummy-content/design-system.json` (import via Ghost Admin → Labs → Import). Registered in `partials/docs/sections.hbs` + `next-section-for.hbs` + a `/docs/design-system/` route. To extend the docs, add/edit posts in Ghost Admin (or regenerate the JSON) — no theme changes needed. Five rules (see `assets/css/0-foundation/README.md`): hairline borders are the structure (not shadows); Fira Code renders every index/label/kicker/status; one signal color (brand blue `#0176D3`); sharp geometry (6px cards, 4px buttons, pills only for true tags); instant 120–180ms motion (no spring/lift). Dark mode is brand navy, not slate. `design-system/` at the repo root is the exported reference system (guidelines, component specs, content-creation templates) this was built to match — read-only inspiration, not part of the build.

## Commands

```bash
yarn install     # install dependencies (Yarn; package-lock.json is gitignored)
yarn dev         # gulp default: build + livereload watch
yarn build       # one-off build into assets/built/
yarn zip         # build + package into dist/namaste-salesforce.zip
yarn test        # gscan . — validate against Ghost's theme rules
yarn test:ci     # gscan --fatal --verbose .
```

"Testing" means **gscan** validation — run `yarn test` after template changes. `pretest` runs `gulp build` first, so the committed `assets/built/` output is what gets validated.

## Build pipeline (gulpfile.js)

`gulp build` runs three steps, all output to `assets/built/` (committed — Ghost serves these directly):

- **css**: `assets/css/screen.css` → PostCSS with **`@tailwindcss/postcss`** (Tailwind v4) → cssnano → `built/screen.css`. There is **no `tailwind.config.js`**; tokens and `@source` globs live in `screen.css`. Tailwind v4 emits its own vendor prefixes, so autoprefixer is not used.
  **`url()` gotcha:** the pipeline rebases relative urls and consumes exactly one `../`, so a font referenced as `../../fonts/x.woff2` in source emits `../fonts/x.woff2` in `built/screen.css` (which is what resolves). Check `grep -o 'url([^)]*)' assets/built/screen.css` after touching font paths.
- **js**: `assets/js/*.js` concatenated → uglify → `built/casper.js`. (`assets/js/vendor/*` — Alpine — is **not** bundled; it's loaded separately.)
- **locales**: merges `locales-local/` into `locales/`.

Because `assets/built/` is committed, **rebuild and commit the built output** after changing CSS or JS. Editing a `.hbs` requires a rebuild too (Tailwind scans templates for class names).

## Architecture

**Templates (Ghost conventions):**
- `default.hbs` — shared shell: `<head>`, `{{> header}}`, `{{{body}}}`, `{{> footer}}`, the pre-paint theme script, Alpine + `casper.js` includes, `{{ghost_head}}`/`{{ghost_foot}}`. Page templates start with `{{!< default}}`.
- Reserved names: `index`, `post`, `page`, `tag`, `author`, `error`.
- Custom templates: `home`, `courses`, `documentation`, `blog`, `training`, `page-about` (routed/selected in Ghost Admin).
- `post.hbs` is a **router** — `{{#has tag="…"}}` picks a `post-*` partial: `post-course`, `post-lesson`, `post-training`, `post-documentation`, `post-blog`, `post-default`.

**Partials (`partials/`, organised in folders):**
- `components/` — chrome & shared bits: `theme-toggle`, `nav-icon`, `page-header`, `hero-bg`, `breadcrumb`, `toc`, `cta`, `author-byline`, `tag-pills`, `social-icons`.
- `icons/` — inline-SVG icons; include via `{{> "icons/name" class="h-4 w-4 …"}}`. They use `currentColor` + a `class` param, so Tailwind utilities theme them. (Content/cards still use **Phosphor** `<i class="ph-…">`.)

**Icon font (important):** Phosphor is **self-hosted and subsetted** — `assets/fonts/phosphor*.woff2` plus the generated `assets/css/0-foundation/icons.css`, built by `scripts/subset-icons.py`. Only the ~131 glyphs the theme references are shipped. **Adding a new `ph-*` class means re-running the script**, otherwise the icon renders as a blank box:

```bash
pip3 install fonttools brotli   # once
python3 scripts/subset-icons.py
yarn build
```

Icons used *inside Ghost post content* can't be found by scanning templates — add those to `CONTENT_SAFELIST` in that script.
- `home/`, `about/`, `courses/`, `blog/`, `docs/`, `training/` — section-specific partials.
- `ads/` — `slot` resolves to AdSense → sponsor → dummy placeholder.

**Styling (Tailwind v4, CSS-first):** `assets/css/screen.css` is the final stylesheet and stays tiny — Tailwind + `@source` globs + `@custom-variant dark` + four `@import`s. Each layer owns an `index.css` that lists its own files, so adding a token/element/component means adding a file and ONE line in that layer's index; `screen.css` never changes. Full contract in `assets/css/0-foundation/README.md` ("Adding to the system").
- **`0-foundation/` — layer 0, tokens/vars/mixins only** (no selectors that paint UI). `colors.css` (brand/accent scales, status, semantic roles `surface`/`ink`/`muted`/`border`/`label`/`grid` → `--ns-*` vars that flip under `[data-theme="dark"]` to a brand-navy console — avoid hard-coding `dark:` for those), `typography.css` (Inter prose scale + **Fira Code** label scale: `--size-label`, `--tracking-label`), `spacing.css`, `borders.css` (radii 6px/4px + `--border-hairline/strong`), `elevation.css` (near-flat shadows + `--z-*`), `motion.css` (`--duration-fast/base`, `--ease-out`, keyframes incl. `ns-spin`), `mixins.css` (`@utility` recipes: `ns-label`, `ns-index`, `ns-hairline`, `ns-dot-marker`, `ns-transition` — usable in markup AND via `@apply`), `backgrounds.css`, `fonts.css`, `icons.css` (generated). These same variables drive off-site brand assets.
- **`1-elements/` — layer 1, one file per element family:** `base` (html/body/scrollbar/selection/focus) · `typography` · `links` · `lists` · `quotes` · `tables` · `code` · `media` · `forms` · `interactive` (details/dialog/progress) · `separators` · `prose` (the `.prose` token bridge + required Koenig classes). **Two scoping rules:** reading-context styling uses `:where(.gh-content, .ns-prose)` (zero specificity, so utilities always win) and global rules guard with `:not([class])` so utility-styled markup is never touched.
- **`2-components/` — layer 2, the UI library, one file per component:** `button` · `badge` · `chip` · `tag` · `kicker` · `avatar` · `card` · `input` · `code-window` · `video-poster` · `steps` · `timeline` · `nav-link` · `icon-button` · `tooltip` · `toc` · `sidebar` · `subnav` · `share` · `ad` · `marquee` · `effects`. Naming contract: `.ns-thing` base, `.ns-thing--variant` (one axis at a time — SIZE / SHAPE / TONE / STATE), `.ns-thing__part`, `.is-state` for script-toggled runtime state. Variants compose, so reach for `.ns-card .ns-card--lg .ns-card--interactive .ns-card--grid` before writing a new class.
- **`3-modules/` — layer 3, features:** `navbar` (header scroll behaviours, lesson drawer) · `curriculum` (`.ns-curriculum`, 4 `data-style`s, visibility badges) · `course` (level/price tags, hero stats, hero variants) · `catalog` · `lesson` · `training`. Nothing in layers 0–2 may depend on this layer; when a module piece proves reusable, promote it into `2-components/` with a proper variant set.
- House styling rules: status = dot + mono text, never a tinted wash; hover = border brightens to brand + an accent line (top on cards via `::after`, left on rows via inset box-shadow), never a translateY lift; indices/durations/labels always `--font-mono` with `--color-label`.

**Dark mode:** `data-theme="light|dark"` on `<html>`. A pre-paint inline script in `default.hbs` applies the saved theme (`localStorage` key `ns-theme`) before first paint; `theme-toggle.js` flips it on `.ns-theme-toggle` clicks. The sun/moon glyph swap is pure CSS (`dark:` variant).

**JS (`assets/js/`):** `theme-toggle`, `toc` (builds TOC + scroll-spy from `.gh-content`), `effects` (pointer spotlight), `reveal` (scroll reveal) → `casper.js`. Alpine (`vendor/alpine.js`) powers menus, the mobile sub-nav panels, and client-side search filters.

**Translations:** author overrides in `locales-local/`; `gulp locales` merges into `locales/` (don't hand-edit merged files).

## Conventions & gotchas

- Prefer Tailwind utilities in markup; promote to `@layer components` only when a pattern repeats or is awkward as utilities.
- Use the **role tokens** (`surface`/`ink`/`muted`/`border`) and `brand-*` scale; `#0176D3` is `brand-500`.
- **Never call a Ghost helper across `../`** inside a partial (e.g. `{{../url absolute="true"}}`) — Ghost throws and 500s the page. Use dotted property access (`{{primary_tag.url}}`) instead.
- Ad slots and per-section sidebars/TOC are shown by default; ads only become "real" once `@custom.enable_ads` + `adsense_publisher_id` (or `sponsor_*`) are set in Ghost Admin → Design.
- `routes.yaml` (collections / permalinks) lives in Ghost Admin, **not** in this repo.
