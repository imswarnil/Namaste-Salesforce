# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A custom **Ghost** publishing-platform theme ("Namaste Salesforce"), originally forked from Casper but rebuilt for a Salesforce learning site. Templates are Handlebars (`.hbs`); styling is **Tailwind CSS v4** (no Bulma, no SCSS framework). Light interactivity uses **Alpine.js** (self-hosted). The design language is **SLDS-inspired** (Salesforce-blue palette, clean cards, dark mode).

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
- `icons/` — inline-SVG icons; include via `{{> "icons/name" class="h-4 w-4 …"}}`. They use `currentColor` + a `class` param, so Tailwind utilities theme them. (Content/cards still use **Phosphor** `<i class="ph-…">` from the unpkg CDN.)
- `home/`, `about/`, `courses/`, `blog/`, `docs/`, `training/` — section-specific partials.
- `ads/` — `slot` resolves to AdSense → sponsor → dummy placeholder.

**Styling (`assets/css/screen.css`, Tailwind v4):**
- `@theme` holds SLDS tokens: the `brand-*` blue scale, status colours, fonts, radii, shadows, motion. **Semantic role tokens** (`surface`, `surface-raised/sunken`, `ink`, `muted`, `border`) map to `--ns-*` CSS vars that flip under `[data-theme="dark"]`, so `bg-surface`/`text-ink` auto-adapt — avoid hard-coding `dark:` for those.
- `@layer components` holds the few reusable classes: `.nav-link`, `.icon-btn`/`.nav-tip`, `.subnav-bar`/`.subnav-panel`, `.toc-link`, `.js-spotlight`, `.ns-timeline`/`.ns-steps`, `.bg-grid`/`.bg-dots`, and `.prose` overrides.
- `@custom-variant dark` wires the `dark:` variant to `data-theme="dark"`.

**Dark mode:** `data-theme="light|dark"` on `<html>`. A pre-paint inline script in `default.hbs` applies the saved theme (`localStorage` key `ns-theme`) before first paint; `theme-toggle.js` flips it on `.ns-theme-toggle` clicks. The sun/moon glyph swap is pure CSS (`dark:` variant).

**JS (`assets/js/`):** `theme-toggle`, `toc` (builds TOC + scroll-spy from `.gh-content`), `effects` (pointer spotlight), `reveal` (scroll reveal) → `casper.js`. Alpine (`vendor/alpine.js`) powers menus, the mobile sub-nav panels, and client-side search filters.

**Translations:** author overrides in `locales-local/`; `gulp locales` merges into `locales/` (don't hand-edit merged files).

## Conventions & gotchas

- Prefer Tailwind utilities in markup; promote to `@layer components` only when a pattern repeats or is awkward as utilities.
- Use the **role tokens** (`surface`/`ink`/`muted`/`border`) and `brand-*` scale; `#0176D3` is `brand-500`.
- **Never call a Ghost helper across `../`** inside a partial (e.g. `{{../url absolute="true"}}`) — Ghost throws and 500s the page. Use dotted property access (`{{primary_tag.url}}`) instead.
- Ad slots and per-section sidebars/TOC are shown by default; ads only become "real" once `@custom.enable_ads` + `adsense_publisher_id` (or `sponsor_*`) are set in Ghost Admin → Design.
- `routes.yaml` (collections / permalinks) lives in Ghost Admin, **not** in this repo.
