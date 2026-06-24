# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A custom **Ghost** publishing-platform theme ("Namaste Salesforce"), forked from Ghost's Casper theme but heavily customized for a Salesforce learning site. Templates are Handlebars (`.hbs`); styling is a **custom, in-house SCSS framework** under `assets/scss/framework/` — **Bulma has been removed**. The framework reimplements only the utility/component classes the templates use (grid, buttons, navbar, forms, helpers, …), themed with the design tokens in `variables.scss`.

## Commands

```bash
yarn install        # install dependencies (Yarn, not npm — package-lock.json is gitignored)
yarn dev            # gulp default: build + livereload watch server (edit assets, auto-recompiles)
yarn zip            # build + package into dist/namaste-salesforce.zip for upload to Ghost
yarn test           # gscan . — validates the theme against Ghost's theme rules
yarn test:ci        # gscan --fatal --verbose . (used in CI)
```

There is no unit-test framework. "Testing" means **gscan** theme validation — run `yarn test` after template changes to catch Ghost compatibility errors. `pretest` runs `gulp build` first, so the committed `assets/built/` output is what gets validated.

## Build pipeline (gulpfile.js)

`gulp build` runs three steps in series, all output to `assets/built/` (committed to git — Ghost serves these directly):

- **css**: `assets/scss/screen.scss` → Sass → PostCSS (autoprefixer + cssnano) → `built/screen.css` + sourcemap. No external SCSS dependencies — the framework resolves via relative `@use`.
- **js**: `assets/js/lib/*.js` then `assets/js/*.js`, concatenated (lib first so app code can depend on it) → uglify → `built/casper.js`.
- **locales**: merges `locales-local/` overrides into `locales/` via `@tryghost/theme-translations`.

Because `assets/built/` is committed, **rebuild and commit the built output** when you change SCSS or JS, or Ghost will serve stale assets.

## Architecture

**Template resolution (Ghost conventions):**
- `default.hbs` is the shared HTML shell — `<head>`, `{{> header}}`, `{{{body}}}`, `{{> footer}}`, the theme-toggle script, and asset/`{{ghost_head}}`/`{{ghost_foot}}` injection. Every page template starts with `{{!< default}}` to inherit it.
- `index.hbs` (post list / home), `post.hbs`, `page.hbs`, `tag.hbs`, `author.hbs` are Ghost's reserved template names.
- `home.hbs`, `blog.hbs`, `courses.hbs`, `training.hbs`, `documentation.hbs` are **custom templates** — selectable per-page in the Ghost editor and/or routed via the site's `routes.yaml` (configured in Ghost admin, not in this repo). Each renders a distinct section of the site with its own hero/layout.

**Partials (`partials/`):** Reusable Handlebars fragments included with `{{> name}}`.
- `post-*.hbs` (`post-card`, `post-blog`, `post-course`, `post-training`, `post-documentation`, `post-default`, `post-lesson`) are the per-context post renderers — pick the one matching the section.
- `header/` holds composable header pieces (`brand`, `burger`, `search-icon`, `theme-toggle`, `portal-buttons`, etc.); `header.hbs` assembles them.
- `icons/` holds inline SVG icons — include via `{{> "icons/name"}}`. Note: most UI icons in templates use **Phosphor icons** (`<i class="ph-...">`), loaded from the unpkg CDN in `default.hbs`.

**Styling (`assets/scss/`):**
- `screen.scss` is the only compiled entry point. It loads the in-house framework (`framework/*`), then bespoke components, then utility helpers (helpers use `!important`, so load order between them and components doesn't matter), then content/TOC/animation styles, and finally the web-font `@import`.
- `framework/` is the custom CSS framework that replaced Bulma: `_base`, `_layout`, `_helpers`, `_buttons`, `_forms`, `_tags`, `_navbar`, `_menu`, `_card`, `_typography`. Each partial reimplements the Bulma-compatible class names the templates rely on (`.columns`/`.column`, `.button`, `.navbar`, `.tag`, `is-*`/`has-*` helpers, …).
- `variables.scss` defines the Salesforce brand palette and dark-mode tokens (`$sf-*`).
- `ghost.scss` styles Ghost's generated post/Koenig-card content; `toc.scss` styles the table of contents.

**Dark mode:** Driven by `data-theme="light|dark"` on `<html>`. An inline pre-paint script in `default.hbs` applies the saved theme from `localStorage` key `ns-theme` before first paint (avoids flash). A second script wires any `.ns-theme-toggle` button and swaps `.ns-theme-icon` (Phosphor `ph-moon`/`ph-sun`). Style dark mode via the `[data-theme="dark"]` selector using `$sf-dark-*` tokens.

**Translations:** Author overrides in `locales-local/`; `gulp locales` merges them into `locales/`. Don't hand-edit merged files in `locales/`.

## Conventions

- Layout uses Bulma utility classes (`columns`, `is-*`, `hero`, etc.) directly in templates rather than custom CSS where possible.
- `$salesforce-blue` / `#0176D3` is the brand primary, mapped to Bulma's `$primary` and `$link`.
- The `release`/`ship` gulp tasks target the upstream TryGhost/Casper repo and a `GST_TOKEN` env var — they are not used for this fork's workflow.
