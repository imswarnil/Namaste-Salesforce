# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

An open-source **Ghost theme** for a Salesforce learning site, currently a
**stack-free starter**: five templates, two partials, ~30 lines of CSS, no
build step, no dependencies except `gscan`.

It was previously a large implementation and was deliberately reset. Do not
reintroduce a build, a CSS framework or a component library without an explicit
decision — see `abstract/15`, which lists what was removed and the questions
still open.

## Read this before doing anything

**`abstract/` is the documentation**, ordered by what breaks the site if you
get it wrong. `abstract/00-README.md` is the map.

If you read three files, read:

- **`abstract/01-content-model.md`** — `routes.yaml`, tags and the URL rules.
  The only part of this project that is expensive to change later.
- **`abstract/02-post-dispatcher.md`** — one `post.hbs`, several page types,
  and why branch order is load-bearing.
- **`abstract/10-how-this-went-wrong.md`** — the mistakes already made here.

Before any styling work, read **`abstract/17-consuming-the-design-system.md`**
(what NSDS actually is — it is already CSS-variables-based, no Tailwind in its
component layer) and **`abstract/decisions/0002-css-strategy.md`**, which is
**open** and gates that work.

**`abstract/decisions/`** is the decision record. If a choice would take more
than a day to reverse, it gets a file there — with its downside and the trigger
that reopens it. Decisions made by drift are what `abstract/10` is about.

## Commands

```bash
npm install
npm test        # gscan — Ghost's own theme validator
npm run zip     # package for upload
```

There is no build. `assets/css/screen.css` is served directly.

## The rules

- **No inline styles.** No `style="…"`, no `<style>` in any `.hbs`. CI fails on
  it. Reasoning in `abstract/05`.
- **Check Ghost first, then the design system, then write.** The theme's job is
  only what neither can know about.
- **Never call a Ghost helper across `../`** (`{{../url}}`) — Ghost throws and
  500s the page. Dotted property access is fine.
- **`limit="all"` is not supported** in `{{#get}}`. Use `limit="100"`.
- **When markup moves onto a new class, grep the JS for the old one in the same
  change.** A script whose selectors no longer match fails silently — build
  green, validator green, feature dead. This has happened here.
- **State is an attribute** (`aria-current`, `data-state`, `[open]`), not a
  class, so the CSS and the screen reader read one source.

## Verifying

`gscan` and a green build are necessary and **not sufficient** — both were
green while the site was visually broken. Get Ghost running locally, upload
`routes.yaml`, import a fixture (`abstract/14`), and look at the page.
