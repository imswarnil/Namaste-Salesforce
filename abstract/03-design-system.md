# 03 · NSDS — the Namaste Salesforce Design System

**NSDS owns how everything looks. The theme must not have a second opinion.**

It lives OUTSIDE the theme, beside the Ghost install, at
`../../../../NS-Design-System`, and is **vendored** in by `yarn design:sync`.
The same system is vendored into the Next.js LMS at app.namastesalesforce.com,
which is the entire point: one system, two products, no drift.

| Path | Contents | Rule |
| --- | --- | --- |
| `assets/css/nsds/` | tokens + the `.ns-*` component layer | **generated — never edit** |
| `assets/js/nsds/` | the system's runtime | **generated — never edit** |
| `partials/nsds/` | generated partials (the inlined theme bootstrap) | **generated — never edit** |

Editing any of it works until the next sync silently reverts you. Change
`NS-Design-System` and re-sync.

## Why vendor instead of importing across the filesystem

A Ghost theme ships as a self-contained zip. Anything reaching outside the
theme root resolves on your machine and 404s on the server. So: copy, and
commit the copy. `yarn design:check` fails the build if the copy has drifted.

## Class names stay `.ns-*`

NSDS is the NAME of the system; `.ns-` is its namespace. The theme does not
invent a second prefix — a second namespace is how two products stop looking
like one.

## THE BEHAVIOUR IS PART OF THE CONTRACT

Several components are inert markup without their script. Vendoring the CSS and
hand-rolling the behaviour is how the two products drift in the half nobody
diffs.

| script | drives |
| --- | --- |
| `nav.js` | topnav menus, mobile sheet, theme switch, scrolled state |
| `toc.js` | builds the outline from headings, scroll-spy |
| `tabs.js` | the ARIA tab contract (roving tabindex, arrow keys) |
| `lms.js` | lesson rail, curriculum, reading progress |
| `training.js` | opens the current curriculum module |
| `rail.js` | opens the docs sidebar group |
| `code.js` | copy button on code blocks |
| `theme-init.js` | **inlined, blocking, in `<head>`** — see 07 |

## Before writing ANY component, check NSDS first

Its variant sets are larger than they look — `.ns-btn` has 19, `.ns-table` 17.
This was skipped repeatedly and the cost was:

- ~100 classes reimplementing the training layer under different names
  (`.ns-reader` was `.ns-training`, `.ns-sidenav` was `.ns-trainingnav`,
  `.ns-track-card` was `.ns-trackcard`, `.ns-lock` was `.ns-gate`)
- three copies of a lesson row, two tables of contents, two share components,
  two post cards, two pagers, two section headers

## A shared class name is not always a shared component

`.ns-mark` was NSDS's `<mark>` text highlight **and** the theme's animated SVG
logo. The theme's `width: 100%` was landing on highlighted text inside blog
posts. Check what a colliding name MEANS before assuming it is a duplicate.

## Where the theme legitimately differs, write down why

Two live examples, both documented in the files themselves:

- **`.ns-progress`** — NSDS styles a native `<progress>` through
  `::-webkit-progress-value`. The theme's is a `<div>` + `__bar`. Deleting the
  theme's makes every bar silently blank.
- **Icons** — NSDS was written against an icon FONT and styles glyphs by
  element (`.ns-buybox__list i`). This theme draws inline SVG, so every one of
  those rules misses. `icon-bridge.css` restates them for `.ns-icon`, with the
  upstream `file:line` on each. **The real fix is `i, .ns-icon` upstream.**
