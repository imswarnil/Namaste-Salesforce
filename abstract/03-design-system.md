# 03 · NSDS — the design system this theme is a port of

**NSDS owns how everything looks. The theme must not have a second opinion.**

It lives OUTSIDE the theme, beside the Ghost install, at
`../../../../NS-Design-System`. The same system is consumed by the Next.js LMS
at app.namastesalesforce.com, which is the entire point: one system, two
products, no drift.

The requirement is not "in the spirit of NSDS." It is that the site look
**exactly** like it. Every page is a **port of an archetype** in
`NS-Design-System/templates/` — the same `.ns-*` markup with the marked slots
swapped for Ghost helpers, which is the procedure NSDS's own
`docs/INTEGRATION.md` §5 specifies. Approximating an archetype from memory is
the failure recorded in [`10`](09-lessons.md), twice.

---

## What NSDS actually is, measured

Measured against the repo at `f0dd883` (2026-08-24), not inferred from its
README. The commands to re-check every number are at the foot of this file.

| | |
|---|---|
| custom properties | **278** across 8 token files |
| `.ns-*` selectors | **1,779**, resolving to **323 distinct component blocks** |
| component stylesheets | **34** in `components/css/` |
| framework-agnostic archetypes | **57** in `templates/` |
| `@apply` / `theme()` / `tw-` in the component layer | **0** |

That last row is the load-bearing one. **NSDS is already a CSS-variables
system.** Tailwind is not underneath it. `tokens/tailwind.css` is *generated*
from the same token files and only re-declares each token inside `@theme`, so
`--space-5` also answers to `p-card`. It is a projection of the tokens into a
second syntax — delete it and no component loses a declaration; you lose only
the ability to compose new *layout* in markup.

Two entry points, and the difference is the whole consumption question:

| Entry | Contains | Build? |
|---|---|---|
| `styles.css` | tokens → base → icons → patterns → 323 components, plain CSS | no |
| `tailwind.entry.css` | `@import "tailwindcss"` + the token bridge + `styles.css` | yes |

## What this theme takes, and why

**Tailwind v4 + NSDS, with a gulp build.** Decided as the plain bundle with no
build step, then reversed the same day when the first real templates showed
what was missing. [`04`](04-css.md) is the file to read before touching the
CSS setup.

The short version: NSDS's archetypes express layout that is not in the `.ns-*`
class layer at all —

```html
<div class="ns-blog-listing" style="max-inline-size:var(--container-page);…">
```

— and a theme has four ways to reproduce that. Inline styles are banned (they
cannot be overridden by a stylesheet, so they break dark mode and the
publisher's accent silently). A named theme class per instance is the
~100-duplicate mechanism from `10`. Approximating is what went wrong. Utilities
are the fourth, and they are the one NSDS itself assumes.

**The temptation moves rather than disappears.** Under a no-build setup it was
to write a theme class; under this one it is to build a component out of twelve
utilities that NSDS already ships as one class. A utility is for composing a
**layout that only this theme has** — not for rebuilding a card.

## Vendored, not imported

A Ghost theme ships as a self-contained zip: anything reaching outside the
theme root resolves on your machine and 404s on the server. So NSDS is
**copied in** and the copy is committed.

```bash
./scripts/sync-nsds.sh              # re-vendor from ../../../../NS-Design-System
npm run build                       # then rebuild — the icon bridge regenerates
```

| Path | What | Rule |
|---|---|---|
| `assets/css/namaste-ui.css` | the whole component layer, flattened | **generated — never edit** |
| `assets/css/ns-tailwind.css` | the `@theme` token bridge | **generated — never edit** |
| `assets/js/*.js` | NSDS's own behaviour layer | **generated — never edit** |
| `assets/fonts/`, `assets/icons/` | the self-hosted faces | **generated — never edit** |

Editing any of it works until the next sync silently reverts you. Change
`NS-Design-System` and re-sync. [`05`](05-assets.md) covers what lands where
and why the paths resolve.

## Class names stay `.ns-*`

NSDS is the name of the system; `.ns-` is its namespace. The theme does not
invent a second prefix — **a second namespace is how two products stop looking
like one**.

`scripts/check-classes.mjs` fails the build on any `.ns-*` in a template that
is not defined in the vendored bundle or the theme's own layer. That check
exists because the failure is silent: an invented name renders as unstyled
markup, and gscan passes, because it is valid HTML.

## Check NSDS before writing ANY component

Its variant sets are larger than they look — `.ns-btn` has 19, `.ns-table` 17.
Skipping this check cost, last time:

- ~100 classes reimplementing the training layer under different names
  (`.ns-reader` was `.ns-training`, `.ns-sidenav` was `.ns-trainingnav`,
  `.ns-track-card` was `.ns-trackcard`, `.ns-lock` was `.ns-gate`)
- three copies of a lesson row, two tables of contents, two share components,
  two post cards, two pagers, two section headers

**A shared class name is not always a shared component.** `.ns-mark` was NSDS's
`<mark>` text highlight **and** the theme's animated SVG logo, and the theme's
`width: 100%` was landing on highlighted text inside blog posts. Check what a
colliding name *means* before assuming it is a duplicate.

## The behaviour is part of the contract

Several components are inert markup without their script. Vendoring the CSS and
hand-rolling the behaviour is how the two products drift in the half nobody
diffs.

| script | drives |
|---|---|
| `theme-init.js` | **inlined, blocking, in `<head>`** — see [`08`](08-ghost.md) |
| `nav.js` | topnav menus, mobile sheet, theme switch, scrolled state |
| `toc.js` | builds the outline from headings, scroll-spy |
| `tabs.js` | the ARIA tab contract — roving tabindex, arrow keys |
| `lms.js` | lesson rail, curriculum, reading progress |
| `training.js` | opens the current curriculum module |
| `rail.js` | opens the docs sidebar group |
| `code.js` | copy button on code blocks |

## Where the theme legitimately differs, write down why

Two live examples, both documented in the files themselves:

- **Icons.** NSDS was written against an icon FONT and styles glyphs by element
  (`.ns-buybox__list i`). This theme draws inline SVG, so 85 of those rules
  miss. `assets/css/theme/icon-bridge.css` restates them for `.ns-icon` — and
  it is *generated*, so it cannot drift. [`05`](05-assets.md) has the argument.
- **`.ns-progress`.** NSDS styles a native `<progress>` through
  `::-webkit-progress-value`; a theme reimplementation as a `div` + `__bar` is
  a legitimate difference, and deleting it makes every bar silently blank.

## The three values that MUST match across both products

From `docs/INTEGRATION.md`. If the theme and the LMS ever disagree visually,
the cause is almost always one of these:

| | Value |
|---|---|
| spacing base | `--spacing: 0.25rem` in Tailwind, `--space-*` in CSS |
| theme attribute | `data-theme="dark"` on `<html>` |
| theme storage key | `ns-theme` in `localStorage` |
| layer order | `@layer theme, base, ns-components, components, utilities;` |

The last two are set in one shared file, `assets/js/theme-init.js`, which both
products inline **verbatim**.

## Weight, and the lever that is not Tailwind

~467 KB compiled. **Tailwind does not shrink it** — purging only removes
generated utilities; `@layer ns-components` is hand-written CSS included
verbatim either way.

The real lever is that `components/css/index.css` is a flat list of `@import`s,
so cherry-picking is already supported. `player.css`, `ai.css`, `deck.css`,
`admin.css`, `auth.css` and `helpdesk.css` are LMS surfaces a Ghost page never
renders — roughly 200 KB of source.

> **Do this after the theme renders correctly, never before.** Trimming while
> you are still discovering which components you need produces the
> silent-missing-style bug, and you will blame the wrong thing.

## Facts to re-check if NSDS moves

```bash
DS=../../../../NS-Design-System

# Still no Tailwind in the component layer? (expect: nothing)
grep -rl '@apply\|theme(' $DS/components/css/ $DS/tokens/*.css | grep -v tailwind.css

# The inventory
grep -rhoE '\.ns-[a-zA-Z0-9_-]+' $DS/components/css/ | sed 's/__.*//; s/--.*//' | sort -u | wc -l
ls $DS/templates/*.html | wc -l
ls -la $DS/dist/

# What we are vendored against
git -C $DS log --oneline -1
```
