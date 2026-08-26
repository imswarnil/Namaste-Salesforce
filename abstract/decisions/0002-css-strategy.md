# 0002 · How the theme gets its CSS

**Status:** **Superseded by option B** — see the reversal at the foot of this file
**Date raised:** 2026-08-21
**Date decided:** 2026-08-25

## Context

The theme was a stack-free starter ([0001](0001-reset-to-a-starter.md)) with
~30 lines of CSS and no opinion about how anything looked. Building the site
chrome forced the question, because a navbar cannot be written without one.

The question is usually framed as *"Tailwind, or CSS variables?"* — and
measuring NSDS shows that framing is wrong. The full measurement is in
[`../03-design-system.md`](../03-design-system.md);
the load-bearing facts:

- **NSDS is already a CSS-variables system.** 407 custom properties, 663 `.ns-*`
  classes, 300 component blocks — and across all 33 component stylesheets there
  is **no `@apply`, no `theme()`, no `tw-` prefix**.
- **Tailwind is a projection, not a foundation.** `tokens/tailwind.css` is
  *generated* from the same token files and only re-declares each token inside
  `@theme`. Removing it costs zero declarations.
- **The framework-neutral build already ships** and is described by NSDS's own
  build script as droppable into a page "with no build step at all."
- **Tailwind would not shrink it.** Purging only removes generated utilities.
- **The neutral bundle has no reset.** It depends on Tailwind's Preflight for
  `box-sizing: border-box` and friends. 89 rules declare a width alongside
  padding, so under `content-box` they overflow by their own padding.

## Decision

**Option A. The framework-neutral bundle, no build step.**

`assets/css/namaste-ui.css` is NSDS's `dist/namaste-ui.css` vendored at
**f0dd883 (2026-08-24)**. `assets/css/screen.css` declares the layer contract, imports
it, and then imports this theme's own small layer.

**The reset landed in the same commit**, as this decision required — see
`assets/css/theme/reset.css`, which explains what it fixes and why the absence
is not obvious.

### Why A rather than B or C

Not because utilities are wrong, but because **A is the only option that is
reversible for free.** A → B is an afternoon of adding a build; by then the
templates will say whether the utilities are actually missed, rather than the
decision resting on a guess made before any of them existed. Nothing in A
forecloses B, and B's failure mode is already documented in `abstract/10`.

The chrome built on top of it (`partials/chrome/`) has needed **zero** theme
CSS so far — every class in the navbar, the sheet and the footer is NSDS's.
That is the strongest evidence available that A is sufficient.

## Consequences

**The theme owns a small named-class layer, and there will be a recurring
temptation to grow it into a system.** That temptation is the exact mechanism
behind the ~100 duplicated classes in `abstract/10`. Guard it with the
`abstract/00` rule — *check Ghost, then NSDS, then write* — and treat any new
theme class as a defect until proven otherwise.

Right now the theme layer is two files and both are translations rather than
design: `theme/reset.css` (what NSDS assumes but does not ship) and
`theme/ghost.css` (Koenig's `.kg-*` vocabulary, which NSDS has never heard of).

**The layer contract is inherited and non-negotiable** —
`@layer theme, base, ns-components, components, utilities`, declared before any
`@import`, nothing outside a layer. There is **one sanctioned exception**, at
the tail of `theme/ghost.css`: Ghost injects its own `cards.min.css` unlayered
via `{{ghost_head}}`, and an unlayered rule beats every layered rule at any
specificity, so the rules that override it cannot be layered either. That block
is fenced and explains itself. Do not add to it anything that works from inside
the layer.

**Weight is currently untrimmed.** The whole bundle ships, including LMS
surfaces (player, deck, admin, ai, helpdesk) that a Ghost page never renders —
roughly 200 KB of source. `abstract/03` §"Weight" is explicit that cherry-picking
`components/css/` comes **after** the theme renders correctly, never before:
trimming while you are still discovering which components you need produces the
silent-missing-style bug, and you will blame the wrong thing.

## Revisit if

- The theme's own class layer passes ~40 classes — utilities are being
  hand-rolled and B or C is now cheaper than A.
- CSS weight shows up in a real measurement on a real page (not a guess), and
  cherry-picking `components/css/` has already been tried.
- NSDS changes its distribution model — e.g. drops the neutral bundle, or moves
  the component layer to `@apply`. Re-check with the commands at the end of
  `../17`.


---

# ⚠ REVERSED — option B, 2026-08-25

**Status:** **Accepted — option B.** Tailwind v4 + NSDS, with a gulp build.

## What changed

Option A was chosen because it was the only choice that was **reversible for
free**, and the reasoning explicitly said "A → B is an afternoon of adding a
build; by then you will know from real templates whether the utilities are
actually missed."

The templates now exist, and the answer is yes.

The requirement is that the site look **exactly** like NS-Design-System — not
in the same spirit, the same. And NSDS's `templates/*.html`, which are the
canonical markup for every page archetype, express layout that is not in the
`.ns-*` class layer at all:

```html
<div class="ns-blog-listing" style="max-inline-size:var(--container-page);…">
<article class="ns-card ns-bcard ns-bcard--wide" style="margin-block-end:var(--space-8)">
<nav class="ns-pagination" style="margin-block-start:var(--space-10)">
```

Under option A a theme has three ways to reproduce those, and all three are
bad:

1. **Inline styles** — banned here, and rightly: a `style` attribute cannot be
   overridden by a stylesheet, so it breaks dark mode and the publisher's
   accent colour silently (`abstract/04`).
2. **Named theme classes** — one per instance. That is the ~40-class trigger
   this decision already named as the signal to move to B, and it is the exact
   mechanism behind the ~100 duplicated classes in `abstract/10`.
3. **Approximating** — which is what happened, and it is why this is being
   revisited rather than debated.

Utilities are the fourth way, and it is the one NSDS itself assumes: the
design system ships `tokens/tailwind.css` precisely so `p-card` is
`var(--space-5)` and `bg-brand-500` is the brand blue in both products.
`docs/INTEGRATION.md` documents the Ghost setup as a supported path.

## The trigger fired

This decision's own **Revisit if** listed:

> The theme's own class layer passes ~40 classes — utilities are being
> hand-rolled and B or C is now cheaper than A.

It was heading there. Reversing now is the outcome the decision was written to
produce, not a failure of it.

## What is different this time

`abstract/10` is a record of Tailwind + NSDS going wrong here once. The two
things that actually went wrong are both now checked by machine:

**1 · The layer order.** The original break was importing Tailwind before
declaring the layers. That is not a matter of discipline any more:
`assets/css/screen.css` opens with the bare `@layer` statement, and
`scripts/check-layers.mjs` re-proves the order **on the compiled output** on
every build and in CI.

That check earned itself immediately. Built without the statement, the order
came out

```
theme → base → components → utilities → ns-components
```

— the design system last, beating both the theme's own layer and every
utility. Nothing errored. Overrides simply stopped working.

**2 · A stale `assets/built/`.** It is committed, because Ghost serves the
theme as uploaded and there is no build step on the server. CI rebuilds and
fails if the output differs from what is checked in, so the committed bytes
always describe the source.

## Consequences

**Every `.hbs` edit needs a rebuild**, because Tailwind emits utilities from
the class names it finds in the templates. `gulp` watches both.

**The temptation moves rather than disappears.** Under A it was to write a
theme class; under B it is to build a component out of twelve utilities that
NSDS already ships as one class. The rule is unchanged and is the one in
`abstract/00`: check Ghost, then check NSDS, then write. A utility is for
composing a LAYOUT that only this theme has — not for rebuilding a card.

**Weight.** The compiled sheet is ~467 KB unminified-comments-stripped, and
Tailwind does not shrink the `@layer ns-components` half — purging only ever
removes generated utilities. Cherry-picking `components/css/` remains the
real lever and remains deferred until a measurement on a real page asks for
it.

## Revisit if

- The theme's own `@layer components` block grows past ~15 rules that are not
  Ghost-vocabulary translation. That is the signal it has started being a
  design system again.
- A build failure ever ships. The whole justification for committing
  `assets/built/` is that CI proves it is current.
