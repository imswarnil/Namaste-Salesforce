# AGENTS.md — Namaste Salesforce theme

This repository is **the Namaste Salesforce Ghost theme** — a Salesforce
learning platform (courses with a lesson player, tag-driven training
modules, a video library with chapter navigation, a five-layout blog,
newsletter, changelog, GitHub-styled projects, membership). Built from scratch on the NS Design
System. It is NOT Casper, whatever the git history says.

**Read `NAMASTE-SALESFORCE.md` before changing anything** — it is the
architecture document: URL model, tag vocabulary, CSS layers, the
Handlebars traps that have already been hit once.

## Commands

```bash
pnpm install --frozen-lockfile
pnpm build        # gulp: CSS (postcss) + JS (concat/uglify) → assets/built/
pnpm test         # gscan
pnpm test:ci      # gscan --fatal, builds a zip first
```

Run `pnpm build` after touching `assets/css/**` or `assets/js/**`;
templates need no build. Run `pnpm test` before a PR.

## The one idea

A post is a post; ONE internal tag decides its URL (routes.yaml), its
layout (post.hbs dispatches on `post_class`) and its queries:
`#course` `#lesson` `#training` `#video` `#slides` `#blog`
`#newsletter` `#changelog` `#project` (plus `#resource` `#shop`
`#snippet` `#prompt`).
A course's slug equals its public
tag's slug and every lesson's primary tag is that tag — that equality is
the entire parent/child mechanism. Training mirrors it: a module IS a
public tag, its `#module` landing post's slug equals that tag's slug
(URL /training/{slug}/), and `#training` sections nest under it.

## Conventions that must survive edits

- **Durations**: one site-wide ramp — `#duration-5m` … `#duration-55m`
  (fives), `#duration-1h`, `#duration-1h-15m` … The chip text is the tag
  DESCRIPTION; `partials/duration-chip.hbs` is the only renderer. Never
  parse slugs.
- **Video chapters**: a table in the post whose first column is
  timestamps becomes the seeking sidebar (`assets/js/video.js`). It
  looks for the player DOCUMENT-wide, because on a reader page
  `reader-video.js` has already lifted the body's first embed into the
  hero stage (`partials/video-stage.hbs`). That script must keep
  sorting before video.js in the concatenated bundle.
- **Reader heroes**: `#lesson-type-video` pages open with the player
  and move their title block into the reading column; article pages
  keep the cover hero. Both render `partials/trainer-head.hbs`, which
  exists precisely so the breadcrumb/title/chips have one definition
  and two homes.
- **Slide decks**: a `#slides` post's content splits into slides on
  every divider card. `assets/js/deck.js` renders the full-viewport
  player (NS Slides grammar: fixed 1280×720 canvas scaled by
  transform, cinema letterbox, filmstrip rail of cloned minis).
  Ghost's own post access gates a deck; post-slides.hbs shows the
  locked cover when `access` is false.
- **TOC rule**: page has a sidebar → TOC widget lives in it; no sidebar →
  `partials/toc-inline.hbs` right after the hero. toc.js self-removes
  when a page has no headings.
- **Nav dropdowns**: `+Parent` / `-Child` label prefixes in Ghost's
  navigation settings; icons are matched per slug in
  `partials/nav-icon.hbs` (static `{{#match}}` chain — the dynamic
  `{{#> (concat …)}}` partial trick is banned, it fails silently).
- **Internal tag slugs carry Ghost's `hash-` prefix** in the DB and in
  import files; templates match `tag-hash-*` via `post_class`.
- **Feature-image URLs written directly to the DB need the
  `__GHOST_URL__` token** or Ghost's normalisation job nulls them.
- **gscan reads Handlebars comments.** A `{{!-- --}}` that mentions the
  translation helper by its bare mustache form fails the build with "Add
  a string to translate". Describe it in words instead.
- **Reader frames share one rail.** `.player-list` rows, the
  content-coloured active row (bleeds by `--rail-pad`), the edge
  collapse handle and `.rail-home` all live in `4-templates/_lesson.css`
  and serve the lesson player AND the training reader; `_trainer.css`
  only owns grid tracks and the hero. The rail is `position: fixed`
  above its breakpoint — which takes it OUT of the grid flow, so the
  reading region needs an explicit `grid-column`, or it slides into the
  rail's track. `--rail-w` drives the track and the fixed width
  together.
- **/about tells its story ONCE.** The page's own body wins when the
  editor has written one; the theme's built-in version is the fallback
  for an empty page. Both used to render, one under the other. The
  `<main id="site-main">` sits on that section, so `#the-plan` (the
  hero button's target) lives on the inner wrapper: one element, one
  id.
- **Reader frames get `partials/footer-strip.hbs`**, not the navy
  footer; `partials/footer.hbs` matches the collection tag to choose.
- `{{#get}}` switches context to the API response: hash params carried in
  via `partials/with-this.hbs` need `../` per intervening block; filter
  strings compile in the CALLING frame. `{{#if emptyArray}}` is truthy.

## design-system/ — the NS Design System lives here now

`design-system/` is the NS Design System (moved in from the standalone
NSDS-Design-System repo on 24 Sep 2026): SCSS source, committed `dist/`, the
styleguide site (index, docs, components, sections, five `templates/`) and
the AI-readable spec (`DESIGN.md`, `design-guidelines.md`,
`design-components.md`, `llms.txt`). It has its own `CLAUDE.md`, `npm`
lockfile and CI: `.github/workflows/design-system.yml` publishes it to
GitHub Pages at **https://salesforce.imswarnil.com/**. It is NOT part of the
theme — `gulpfile.js` `zipper` and `deploy-theme.yml` `exclude` both leave
it out of the theme zip, and the theme deploy ignores pushes that only touch
it. The theme's `assets/css/` is a hand-kept sibling of `design-system/src/scss/`.

## Layout of the repo

- `routes.yaml` — the URL model; mirror to Ghost's
  `content/settings/routes.yaml` + restart after edits.
- `assets/css/` — layered: `0-abstracts` (tokens/fonts) → `1-base` →
  `2-layout` → `3-components` → `4-templates` → `5-utilities`;
  `screen.css` is the manifest. Paint with semantic tokens only.
- `assets/js/` — theme.js, toc.js, filters.js, video.js, deck.js, plus the
  reader scripts: rail.js (collapsible reader rail, state on
  `html[data-rail]`, restored before paint by the inline script in
  default.hbs) and quote-fill.js (word-by-word scroll fill). Keep JS
  last resort;
  Handlebars/CSS first (`prev_post in="primary_tag"`, `<details>`
  collapse, checkbox drawer).
- `partials/icons/` — one drawing style: 24-box, 1.8 stroke, currentColor.
- `dummy-content/` — `build-import.py` → `import.json` (full demo data,
  navigation included), `build-thumbnails.py` → branded SVG thumbs.
- `design-system/` — the NS Design System + styleguide site (see above).
- Fonts are self-hosted in `assets/fonts/`.

## Boundaries

- Commit generated `assets/built/` — the GitHub deploy ships the repo
  as-is.
- Do not commit `node_modules/`, `dist/`, or secrets.
- Commits: no AI co-author trailers (owner's standing instruction).
