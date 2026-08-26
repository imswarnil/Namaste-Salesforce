# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

A **Ghost theme** for Namaste Salesforce, built on **NS-Design-System (NSDS)**.

The requirement is not "in the spirit of NSDS." It is that the site look
**exactly** like NSDS. Every page is a **port of an archetype** in
`NS-Design-System/templates/` — the same `.ns-*` markup, with the marked slots
swapped for Ghost helpers, which is the procedure NSDS's own
`docs/INTEGRATION.md` §5 specifies. Approximating an archetype from memory is
the failure this project has already paid for twice; see
`abstract/10-how-this-went-wrong.md`.

> **Ghost owns the content model. NSDS owns how everything looks. The theme is
> the wiring between them, and should be as thin as possible.**
>
> Before writing a rule, a component or a script: check whether **Ghost**
> already supplies it, then whether **NSDS** already supplies it. The theme's
> job is only what neither can know about.

Almost every mistake made here came from the theme growing a *third opinion* —
its own components, its own tokens, its own drawer — duplicating one of the
other two.

## Current state — a skeleton, and what that means

The foundation is built and green. The **collections are not**, deliberately.

| | |
|---|---|
| **Build** | gulp + Tailwind v4 + cssnano → `assets/built/`, committed |
| **Checks** | layers, classes, icons, icon bridge, inline styles, Handlebars comments, gscan |
| **CI/CD** | CI on every PR; deploy on `main`; release on a `v*` tag |
| **NSDS** | vendored at `f0dd883` — 1,779 selectors, 278 tokens available |
| **Icons** | 47 inline-SVG partials in `partials/icons/` + a generated 85-rule bridge |
| **Fonts** | Switzer + Roboto Mono, self-hosted, preloaded |
| **Templates** | `default`, `home`, `index`, `post`, `page`, `tag`, `author`, `error`, `error-404` |
| **Navbar** | `partials/navbar/` — bar, sheet, per-item icons, `-Label` dropdowns |
| **Footer** | `partials/footer/` — link columns, social row, newsletter, pinned to the bottom |
| **Homepage** | `home.hbs` — split hero with inline subscribe form + the looping brand mark, what shipped, latest, follow, subscribe |
| **Brand mark** | `partials/logo-sting.hbs` — geometry lifted from `logo-sting/intro.html`, looped in CSS |
| **Reading surface** | `partials/post/article.hbs`, ported from `blog-post.html` |
| **Collections** | **none.** Eight specs waiting in `abstract/collections/` |

`npm run build` is green, `gscan` reports no issues, and the cascade contract
holds in both the development and production builds.

**Do not build a collection before its file in `abstract/collections/` is
answered.** All eight are currently unanswered, and the previous version of
this theme was assembled the other way round — one reasonable commit at a time,
with the content model emerging afterwards. That is what `abstract/10` is a
record of.

`post.hbs` and `default.hbs` both carry placeholder tag lists marked ⚠ SKELETON
for exactly this reason: they are wired, not decided.

The full previous port is still in git at `206a211` if a page needs to be read
rather than reinvented:

```bash
git show 206a211:partials/post/training-post.hbs
git log --oneline 206a211
```

---

# NS-Design-System

## Where it is

`../../../../NS-Design-System` — **outside** the theme, beside the Ghost
install, at `/Users/swarnil/Namaste Salesforce/NS-Design-System`. Measured
here at `f0dd883`, which is also the commit the vendored bundle was taken from.

The same system is consumed by the Next.js LMS at `app.namastesalesforce.com`.
That is the entire point: one system, two products, no drift.

**NSDS is the source of truth and is not edited from this repo.** A value that
needs to change changes there, and comes back through a re-vendor.

## What it actually is, measured

| | |
|---|---|
| custom properties | **278** across 8 token files (colors, dataviz, spacing, layout, fonts, typography, effects, base) |
| `.ns-*` selectors | **1,779**, resolving to **323 distinct component blocks** |
| component stylesheets | **34** in `components/css/` |
| framework-agnostic HTML archetypes | **57** in `templates/` |
| `@apply` / `theme()` / `tw-` in the component layer | **0** |

That last row is load-bearing: **NSDS is already a CSS-variables system.**
Tailwind is not underneath it. `tokens/tailwind.css` is *generated* from the
same token files and only re-declares each token inside `@theme`, so
`--space-5` also answers to `p-card`. It is a **projection of the tokens into a
second syntax** — delete it and no component loses a declaration; you lose only
the ability to compose new layout in markup.

Two entry points, and the difference is the whole consumption question:

| Entry | Contains | Build? |
|---|---|---|
| `styles.css` | tokens → base → icons → patterns → 323 components, plain CSS | no |
| `tailwind.entry.css` | `@import "tailwindcss"` + the token bridge + `styles.css` | yes |

with two prebuilt bundles committed in `dist/`: `namaste-ui.css` (947 KB / 451
KB min, **no Tailwind**) and `namaste-ui.tailwind.css` (654 KB / 521 KB min).

## The five design principles

Not "brand blue on white Tailwind cards." Borrowed from developer-tool product
design (Mux, Vercel, Linear), not marketing-site convention. Check any new
component against all five before it ships.

1. **The hairline is the structure, not the shadow.** Cards, inputs and tags
   are a single `1px` border (`--color-border`). `--shadow-card` is nearly
   flat. Elevation comes from a border brightening to brand blue on hover —
   never a floating lift.
2. **Monospace is a structural material, not a code-block accessory.** Roboto
   Mono renders every index, duration, timestamp, status tag and section
   kicker; Switzer is reserved for prose, headings and quotations. This is what
   makes a list of lessons read as *data* and a paragraph read as *writing*,
   without touching color.
3. **One signal color.** Brand blue `#0176D3` is the only color meaning
   "interactive" or "active." Status shows as a small dot + mono text, never a
   background wash — so a screen has exactly one obvious next action.
4. **Sharp, specific geometry.** `--radius-card` 6px, `--radius-btn` 4px.
   `--radius-pill` is for true pills (tags) only. Nothing is rounded because
   rounding is the default.
5. **Motion is instant, not springy.** 120–180ms plain ease-out. No bounce, no
   scale-pop, no hover translateY. The one exception is the float loop on
   decorative illustrations.

Two supporting motifs: **the code-comment kicker** (`// Getting started`,
in the Apex/SOQL comment voice) replaces a pastel eyebrow pill wherever a
section label is needed, and **the mono index** (`01`, `02`…) appears on every
list, card and roadmap item as a first-class visual element — not a hidden a11y
label.

Identity: *calm, flat, reading-first*. Explicitly **no** gradients, no
glassmorphism, no glow, no neon, no photography, no emoji in UI copy.

## The type scale forks — and the fork is the point

The UI base is **14px**, not 16, because this is a product with an app inside
it. But 14 is the wrong base for an *article*, so `.ns-prose` and everything
built on it take a separate reading scale at **17px / 68ch (`--measure-prose`)
/ 1.7**.

| scale | token | size | for |
|---|---|---|---|
| UI | `--size-body` | 14px | the base — rails, tables, cards, chrome |
| UI | `--size-small` | 13px | dense UI, meta |
| UI | `--size-label` | 11px | mono kickers, all-caps, `--tracking-label` |
| reading | `--size-prose` | 17px | reading copy |
| reading | `--size-prose-lead` | 20px | standfirsts, pull quotes, `.ns-lead` |
| reading | `--size-prose-small` | 15px | tables, code, captions *inside* prose |

Leading forks with it: `--leading-prose` 1.7 for prose paragraphs only,
`--leading-body` 1.6 the UI standard, `--leading-snug` 1.45 for multi-line
scanned text (card excerpts, TOC entries, 20px ledes). **Leading grows with
the measure and shrinks with the size** — never 1.7 on a table row, never 1.3
on a wrapping sentence.

The axis is **scanned versus read**. Do not set an article at `--size-body` or
a table row at `--size-prose`. Weights are `400 / 500 / 600 / 700` — only
weights Switzer's designer actually drew.

`text-label` is the kicker (11px, 700, `0.09em`) arriving whole so it cannot be
half-applied; `text-data` is the same 11px **without** weight and tracking, for
mono data, which is quiet by definition and reads wrong bold.

## Color, dark mode, spacing

- One working blue `#0176D3` carries every interactive and active signal.
  Status colors are a dot + mono text, never a tinted fill.
- Dark mode flips the semantic role tokens — `--color-surface`, `--color-ink`,
  `--color-muted`, `--color-border` — under `[data-theme="dark"]` on `<html>`,
  resolving to the brand navy scale (`--color-brand-800`/`900`). It is *this
  brand's console*, not a GitHub reskin.
- Spacing is a 4px `--space-*` scale whose index matches Tailwind's **1:1**, so
  `p-4` in a `.hbs` and `var(--space-4)` in a React component are the same
  16px. Semantic aliases — `--pad-card`, `--gap-grid`, `--stack-lg` — carry the
  repeated structural relationships.
- Hover brightens the border to brand blue and draws an accent line (top on
  cards, left on rows); press is an instant opacity dim.
- Buttons default to a `--size-small` label at a 40px target. Height is the
  accessibility property, type size the typographic one, set independently.
  Sections never define their own action — they leave `.ns-band__actions` and
  the page puts a button in it.

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

## The cascade contract — non-negotiable

```css
@layer theme, base, ns-components, components, utilities;
```

Declared **before any `@import`** (a bare `@layer` statement is one of the two
things allowed to precede one). Lowest precedence first:

| layer | holds |
|---|---|
| `theme` | Tailwind's `@theme` variables |
| `base` | Preflight + `tokens/base.css` — bare element defaults |
| `ns-components` | **NSDS**, deliberately its own layer, not the generic one |
| `components` | **this theme's** classes — they beat NSDS by layer, not by specificity |
| `utilities` | Tailwind utilities — they beat everything |

Consequences:

- A utility always wins. `<button class="ns-btn ns-btn--primary p-8 bg-error">`
  is red with 2rem padding and no `!important`. Specificity inside NSDS only
  ever decides DS-vs-DS conflicts; a `:has()` chain still loses to `.p-4`.
- **Nothing may sit outside a layer.** An unlayered rule beats every layered
  rule at any specificity, so one stray rule silently revokes the whole
  contract. `scripts/check-layers.mjs` re-proves the order **on the compiled
  output** on every build and in CI — because when this broke, nothing errored;
  overrides simply stopped working.

There is **one sanctioned exception**, fenced and self-explaining at the tail
of `assets/css/theme/ghost.css`: Ghost injects its own `cards.min.css`
unlayered via `{{ghost_head}}`, so the rules overriding it cannot be layered
either. Do not add anything to that block that works from inside the layer.

## How this theme consumes NSDS — decision 0002, option B

`abstract/decisions/0002-css-strategy.md` was decided as A (neutral bundle, no
build) on 2026-08-25 and **reversed to B the same day**: **Tailwind v4 + NSDS,
with a gulp build.** Read that file before touching the CSS setup; the reversal
is at the foot of it.

Why B: NSDS's `templates/*.html` — the canonical markup for every archetype —
express layout that is not in the `.ns-*` class layer at all.

```html
<div class="ns-blog-listing" style="max-inline-size:var(--container-page);…">
<article class="ns-card ns-bcard ns-bcard--wide" style="margin-block-end:var(--space-8)">
```

Under A the theme has three ways to reproduce those and all three are bad:
inline styles (banned), a named theme class per instance (the ~100-duplicate
mechanism), or approximating (what happened). **Utilities are the fourth way,
and it is the one NSDS itself assumes** — `tokens/tailwind.css` exists
precisely so `p-card` is `var(--space-5)` in both products.

So: `assets/css/screen.css` opens with the bare `@layer` statement, imports
Tailwind, the vendored NSDS bundle and the token bridge, then the theme's own
small layer. `assets/built/` is **committed**, because Ghost serves the theme
as uploaded and there is no build step on the server; CI rebuilds and fails if
the output differs from what is checked in.

**The temptation moves rather than disappears.** Under A it was to write a
theme class; under B it is to build a component out of twelve utilities that
NSDS already ships as one class. A utility is for composing a **layout that
only this theme has** — not for rebuilding a card.

Revisit if the theme's own `@layer components` block grows past ~15 rules that
are not Ghost-vocabulary translation. That is the signal it has started being a
design system again.

## Weight

~467 KB compiled, and **Tailwind does not shrink it** — purging only removes
generated utilities; `@layer ns-components` is hand-written CSS included
verbatim. The real lever is that `components/css/index.css` is a flat list of
`@import`s, so cherry-picking is already supported: `player.css`, `ai.css`,
`deck.css`, `admin.css`, `auth.css`, `helpdesk.css` are LMS surfaces a Ghost
page never renders — roughly 200 KB of source.

**Do this after the theme renders correctly, never before.** Trimming while
still discovering which components are needed produces the silent-missing-style
bug, and you will blame the wrong thing.

## Behaviour is part of the contract

Several components are inert markup without their script. Vendoring the CSS and
hand-rolling the behaviour is how the two products drift in the half nobody
diffs.

| script | drives |
|---|---|
| `theme-init.js` | **inlined, blocking, in `<head>`** — before `{{ghost_head}}` and before the stylesheet. A `<script src>` paints too late; that is the white-flash-on-every-navigation bug it exists to prevent. |
| `nav.js` | topnav menus, mobile sheet, theme switch, scrolled state |
| `toc.js` | builds the outline from headings, scroll-spy |
| `tabs.js` | the ARIA tab contract — roving tabindex, arrow keys |
| `lms.js` | lesson rail, curriculum, reading progress |
| `training.js` | opens the current curriculum module |
| `rail.js` | opens the docs sidebar group |
| `code.js` | copy button on code blocks |

Immediately inside `<body>`: `{{> "ns/skip-link"}}`, with
`<main id="main" tabindex="-1">`. The `tabindex="-1"` is **not optional** —
without it Safari and Chrome move the viewport but leave focus at the top of
the document, and the skip link accomplishes nothing.

## Icons — the theme draws its own

**`partials/icons/`, one inline-SVG partial per icon.** `{{> "icons/home"}}`,
or `{{> "icons/arrow-right" class="…"}}`. 24px viewBox, 1.7 stroke, round
caps, `currentColor`, `aria-hidden`.

NSDS's own answer is `<i class="ph ph-home">` against a subsetted Phosphor
woff2, and that is the right answer for the React LMS. Here it is not: a
missing glyph in an icon font renders as **empty space, not a box** — an
invisible control that ships — and the font is a blocking request before the
first icon paints. A missing partial fails the build instead.

**Names match Phosphor's**, so porting an archetype is mechanical: swap
`<i class="ph ph-x">` for `{{> "icons/x"}}` and there is no decision to make.
Brand marks (`github-logo`) are filled and drawn to their owner's outline —
redrawing a company's mark on our grid misrepresents it.

**The cost, and it is generated.** NSDS styles **85 rules** by element
(`.ns-buybox__list i`), and an inline `<svg>` is not an `<i>`, so all 85 miss —
the icon renders *unstyled* rather than missing, which is far harder to notice.
`assets/css/theme/icon-bridge.css` restates them for `.ns-icon`, generated from
the vendored bundle by `scripts/build-icon-bridge.mjs` and diffed in CI, so it
cannot drift. The real fix is `i` → `:is(i, .ns-icon)` upstream, which deletes
the file.

NSDS's icon font is still vendored in `assets/icons/`, because the bundle's
`@font-face` rules reference it and a 404 in a stylesheet is a console error on
every page. A `ph-` class outside the subset still renders as empty space —
grep before adding one.

`partials/icons/README.md` and `abstract/05-assets.md` carry the full argument.

## Porting an archetype — the procedure

1. Find the archetype in `NS-Design-System/templates/` (57 of them —
   `blog-post.html`, `course-detail.html`, `homepage.html`, `navbar-blog.html`,
   `tag-page.html`, `error-page.html`, `signin-form.html`…).
2. Copy it into `partials/` and rename to `.hbs`.
3. Swap the marked slots for Ghost helpers — `{{@site.url}}`, `{{title}}`,
   `{{@site.title}}`. `data-members-*` attributes are Ghost Members hooks and
   work as-is.
4. Replace the archetype's inline `style="…"` layout with the matching Tailwind
   utilities. Never carry an inline style across.
5. Do not rename a class on the way through. `.ns-` is NSDS's namespace and the
   theme does not invent a second one — a second namespace is how two products
   stop looking like one.

**Check NSDS before writing any component.** Its variant sets are larger than
they look: `.ns-btn` has 19, `.ns-table` 17. Skipping this check cost ~100
classes reimplementing the training layer under different names, three copies
of a lesson row, two tables of contents, two share components and two pagers.

**A shared class name is not always a shared component.** `.ns-mark` was NSDS's
`<mark>` highlight *and* the theme's animated SVG logo, and the theme's
`width: 100%` was landing on highlighted text inside blog posts. Check what a
colliding name *means* before assuming it is a duplicate.

**Where the theme legitimately differs, write down why, in the file.** Two live
examples: `.ns-progress` (NSDS styles a native `<progress>`; the theme's is a
`div` + `__bar`, and deleting the theme's makes every bar silently blank), and
the icon bridge (NSDS styles glyphs by element, `.ns-buybox__list i`; inline
SVG misses every one of those rules).

---

# Ghost

## Commands

```bash
npm install
npm run dev      # gulp: build, then watch and rebuild
npm run build    # NODE_ENV=production — one production build
npm test         # build, then gscan
npm run test:ci  # build, then gscan --fatal (warnings fail too)
npm run zip      # package dist/namaste-salesforce.zip for upload

./scripts/sync-nsds.sh   # re-vendor NSDS, then npm run build
```

Every check is a plain node script and runs on its own with no gulp:

```bash
node scripts/build-icon-bridge.mjs --check   # bridge matches the bundle
node scripts/check-layers.mjs                # the cascade contract, on the OUTPUT
node scripts/check-classes.mjs               # every .ns-* used is defined
node scripts/check-icons.mjs                 # every {{> "icons/…"}} exists
```

**Check by exit code, not by grepping output.** These print human-readable
findings with no `FAIL` prefix, so `npm run build | grep -i error` reports
success on a failing build.

There **is** a build. `assets/css/screen.css` is the source; `assets/built/` is
what Ghost serves and is committed. Every `.hbs` edit needs a rebuild, because
Tailwind emits utilities from the class names it finds in the templates. Gulp
watches both.

## The rules

- **No inline styles.** No `style="…"`, no `<style>` in any `.hbs`. CI fails on
  it: a style attribute cannot be overridden by a stylesheet, so it breaks dark
  mode and the publisher's accent colour silently.
- **State is an attribute** — `aria-current`, `aria-expanded`, `data-state`,
  `open` — not a class, so the CSS and the screen reader read one source.
- **`{{#foreach navigation}}` only works inside `partials/navigation.hbs`.**
  `navigation` is created by the `{{navigation}}` helper and exists nowhere
  else; iterating it in any other file emits an empty string, with no error
  and a passing gscan. This theme shipped that bug once. Call
  `{{navigation variant="bar"}}` and let `partials/navigation.hbs` dispatch.
  `abstract/08` has the whole trap, including the `-Label` dropdown
  convention and `{{#match label "~^" "-"}}`.
- **Never call a Ghost helper across `../`** (`{{../content}}`) — it renders
  nothing. Dotted property access is fine.
- **`{{#get}}` switches the block context even with `as |x|`**, so a partial's
  own parameters need `../` inside it — and its `filter` cannot contain `../`
  at all (`unsupported path segment`).
- **`limit="all"` is not supported** in `{{#get}}` — Ghost returns 15 silently.
- **A comment-close sequence inside a Handlebars comment** ends the comment
  there and leaks the rest into the page. CI greps for it.

## Verifying

`gscan` and a green build are **necessary and not sufficient** — both were
green while the site was visually broken, more than once. Get Ghost running,
upload `routes.yaml`, import `dummy-content/import.json`, and look at the page.
`/blog/styleguide/` carries every Koenig card; open it after any CSS change.

For a side-by-side against the source of truth:

```bash
cd "../../../../NS-Design-System" && npm run dev   # styleguide at :4322/preview/
```

---

# Read before doing anything

**`abstract/` is the documentation**, ordered by what breaks the site if you
get it wrong. `abstract/00-README.md` is the map, and its status column matters
— some files describe an implementation that no longer exists and carry a
banner saying so.

If you read four:

- **`abstract/01-content-model.md`** — `routes.yaml`, tags, URL rules. The only
  part of this project that is expensive to change later.
- **`abstract/03-design-system.md`** — what NSDS is, measured, and the rules
  for consuming it without growing a second opinion.
- **`abstract/04-css-architecture.md`** — the cascade contract, and how to
  write a rule or add a component here.
- **`abstract/10-how-this-went-wrong.md`** — the mistakes already made here.

And before building any page family: **`abstract/collections/`** — one spec
per surface, all eight currently unanswered. No collection gets built before
its file is.

Tag names are **not** decided in this repo. They are canonical in the root
knowledge base at `Namaste Salesforce/abstract/05-content/tag-registry.md`,
because the vocabulary is shared with the LMS and the content pipeline.

`abstract/decisions/` is one file per choice expensive to reverse, with its
reasoning, its downside and the trigger that should reopen it. That folder
exists because the last stack was never actually decided — it accumulated one
reasonable commit at a time, which is why `10` had to be written.

## Facts to re-check if NSDS moves

Written against NSDS at **f0dd883, 2026-08-24**.

```bash
DS=../../../../NS-Design-System
grep -rl '@apply\|theme(' $DS/components/css/ $DS/tokens/*.css | grep -v tailwind.css   # expect none
grep -rhoE '\.ns-[a-zA-Z0-9_-]+' $DS/components/css/ | sed 's/__.*//; s/--.*//' | sort -u | wc -l
ls -la $DS/dist/
git -C $DS log --oneline -1
```
