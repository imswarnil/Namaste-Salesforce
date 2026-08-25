# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

A **Ghost theme** for Namaste Salesforce, built on **NS-Design-System**. Every
page is a port of an archetype in `NS-Design-System/templates/` — the same
`.ns-*` markup, with the marked slots swapped for Ghost helpers, which is the
procedure NSDS's own `docs/INTEGRATION.md` §5 specifies.

The theme adds no design opinions. Ghost owns the content model, NSDS owns how
everything looks, and the theme is the wiring.

## Read this before doing anything

**`abstract/` is the documentation**, ordered by what breaks the site if you
get it wrong. `abstract/00-README.md` is the map.

If you read three files, read:

- **`abstract/01-content-model.md`** — `routes.yaml`, tags and the URL rules.
  The only part of this project expensive to change later.
- **`abstract/18-tag-registry.md`** — the canonical tag vocabulary. It OWNS
  the names, and supersedes the older list `abstract/02` was written against.
- **`abstract/10-how-this-went-wrong.md`** — the mistakes already made here.

## Commands

```bash
npm install
npm run dev      # watch and rebuild
npm run build    # one production build
npm test         # build, then gscan
npm run zip      # package for upload
./scripts/sync-nsds.sh   # re-vendor the design system
```

There IS a build. `assets/css/screen.css` is the source; `assets/built/` is
what Ghost serves, and it is committed because there is no build step on the
server. CI rebuilds and diffs it.

## The rules

- **No inline styles.** No `style="…"`, no `<style>` in any `.hbs`. CI fails
  on it: a style attribute cannot be overridden by a stylesheet, so it breaks
  dark mode and the publisher's accent silently.
- **Check Ghost first, then the design system, then write.** The theme's job
  is only what neither can know about.
- **Never call a Ghost helper across `../`** (`{{../content}}`) — it renders
  nothing. Dotted property access is fine.
- **`{{#get}}` switches the block context even with `as |x|`**, so a partial's
  own parameters need `../` inside it — and its `filter` cannot contain `../`
  at all (`unsupported path segment`).
- **`limit="all"` is not supported** in `{{#get}}` — Ghost returns 15 silently.
- **A comment-close sequence inside a Handlebars comment** ends the comment
  there and leaks the rest into the page. CI greps for it.
- **A `ph-` class outside the Phosphor subset renders as empty space.** Grep
  `assets/css/namaste-ui.css` before adding one.
- **State is an attribute** (`aria-current`, `aria-expanded`, `data-state`,
  `open`), not a class, so the CSS and the screen reader read one source.

## Verifying

`gscan` and a green build are necessary and **not sufficient** — both were
green while the site was visually broken, more than once. Get Ghost running,
upload `routes.yaml`, import `dummy-content/import.json`, and look at the
page. `/blog/styleguide/` carries every Koenig card; open it after any CSS
change.
