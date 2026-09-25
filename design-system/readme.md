# NS Design System

The design system behind [Namaste Salesforce](https://namastesalesforce.com) — a Salesforce learning publication on Ghost. Token-first, dependency-free CSS: one accent blue, a navy gray ramp, Figtree, light and dark built in, and the components a learning site actually needs (lesson player rail, quiz, progress, trail, lesson pagination).

**Live:** https://salesforce.imswarnil.com/ · published from this folder by GitHub Pages.

```html
<link rel="stylesheet" href="https://salesforce.imswarnil.com/dist/css/screen.min.css" />
<script src="https://salesforce.imswarnil.com/dist/js/nsds.js" defer></script> <!-- optional -->
```

## What is here

| Path | What |
| --- | --- |
| `index.html` | landing |
| `docs.html` | foundations — install, architecture, every token, breakpoints, theming, accessibility |
| `components.html` | the component gallery, live with copy-paste markup |
| `sections.html` | page bands — heroes, props, split, trail, pricing, FAQ, CTA |
| `templates/site.html` | a complete single-page learning publication |
| `templates/courses.html` · `course.html` · `lesson.html` · `training.html` | catalogue, course landing, lesson player, training trail |
| `DESIGN.md` · `design-guidelines.md` · `design-components.md` | the AI-readable spec (tokens · rules · components) |
| `llms.txt` | machine index |
| `src/scss/` | 53 plain-CSS partials in six layers; `screen.scss` is the manifest |
| `src/js/nsds.js` | the optional runtime: theme toggle, TOC + scroll-spy, copy buttons, quiz tally, toast, rail toggle |
| `dist/` | compiled output — committed on purpose |

## Commands

```bash
npm ci
npm run build     # sass → dist/css/screen.css + .min.css, copies fonts + js
npm run watch     # recompile on save
npm run serve     # static server at :4322
npm run stage     # what CI publishes: _site/ with CNAME
```

## Layers

```
0-abstracts   tokens + @font-face — no selectors that paint
1-base        reset, element typography, .gh-content article styles
2-layout      .outer/.inner containers, header (CSS drawer + dropdowns), footer
3-components  buttons, chips, badges, cards, avatars, forms, search, widgets, toc,
              filters, pagination, pager, alerts, tabs, accordion, tables, lists,
              progress, quiz, media, code, stats, pricing, testimonial, tooltip, empty
4-templates   sections, home, blog, post, courses, course, lesson, training, trail,
              trainer, videos, newsletter, changelog, page, docs, archive, error
5-utilities   background patterns + helpers, allowed to win
```

The `@use` order in `src/scss/screen.scss` is the cascade. Later layers may override earlier ones, never the reverse.

## Theming

```html
<html data-theme="dark">   <!-- force dark -->
<html data-theme="light">  <!-- force light -->
<html>                     <!-- follow the OS -->
```

Retheme by overriding tokens after the stylesheet loads — start with `--accent`, `--accent-strong`, `--accent-soft`, the radii and the `--brand-*` ramp. Full list in [DESIGN.md](./DESIGN.md).

## Deploy

Pushes to `main` that touch `design-system/` run `.github/workflows/design-system.yml`: build, drift check (`git diff --exit-code`), then `npm run stage` and GitHub Pages deploy with `_site/CNAME = salesforce.imswarnil.com`. The Ghost theme deploy excludes this folder from the theme zip.

MIT.
