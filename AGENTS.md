# AGENTS.md — Namaste Salesforce theme

This repository is **the Namaste Salesforce Ghost theme** — a Salesforce
learning platform (courses with a lesson player, tag-driven training
modules, a video library with chapter navigation, a five-layout blog,
newsletter, changelog, membership). Built from scratch on the NS Design
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
`#course-col` `#lesson-col` `#training-col` `#video-col` `#blog-col`
`#newsletter-col` `#changelog-col`. A course's slug equals its public
tag's slug and every lesson's primary tag is that tag — that equality is
the entire parent/child mechanism. A training module IS a public tag.

## Conventions that must survive edits

- **Durations**: one site-wide ramp — `#duration-5m` … `#duration-55m`
  (fives), `#duration-1h`, `#duration-1h-15m` … The chip text is the tag
  DESCRIPTION; `partials/duration-chip.hbs` is the only renderer. Never
  parse slugs.
- **Video chapters**: a table in the post whose first column is
  timestamps becomes the seeking sidebar (`assets/js/video.js`).
- **TOC rule**: page has a sidebar → TOC widget lives in it; no sidebar →
  `partials/toc-inline.hbs` right after the hero. toc.js self-removes
  when a page has no headings.
- **Nav dropdowns**: `+Parent` / `-Child` label prefixes in Ghost's
  navigation settings; icons resolve as `partials/icons/nav-{slug}`.
- **Internal tag slugs carry Ghost's `hash-` prefix** in the DB and in
  import files; templates match `tag-hash-*` via `post_class`.
- **Feature-image URLs written directly to the DB need the
  `__GHOST_URL__` token** or Ghost's normalisation job nulls them.
- `{{#get}}` switches context to the API response: hash params carried in
  via `partials/with-this.hbs` need `../` per intervening block; filter
  strings compile in the CALLING frame. `{{#if emptyArray}}` is truthy.

## Layout of the repo

- `routes.yaml` — the URL model; mirror to Ghost's
  `content/settings/routes.yaml` + restart after edits.
- `assets/css/` — layered: `0-abstracts` (tokens/fonts) → `1-base` →
  `2-layout` → `3-components` → `4-templates` → `5-utilities`;
  `screen.css` is the manifest. Paint with semantic tokens only.
- `assets/js/` — theme.js, toc.js, filters.js, video.js. Keep JS last
  resort; Handlebars/CSS first (`prev_post in="primary_tag"`, `<details>`
  collapse, checkbox drawer).
- `partials/icons/` — one drawing style: 24-box, 1.8 stroke, currentColor.
- `dummy-content/` — `build-import.py` → `import.json` (full demo data,
  navigation included), `build-thumbnails.py` → branded SVG thumbs.
- Fonts are self-hosted in `assets/fonts/`.

## Boundaries

- Commit generated `assets/built/` — the GitHub deploy ships the repo
  as-is.
- Do not commit `node_modules/`, `dist/`, or secrets.
- Commits: no AI co-author trailers (owner's standing instruction).
