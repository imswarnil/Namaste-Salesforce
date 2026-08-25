# 0002 · How the theme gets its CSS

**Status:** **Accepted** — option A
**Date raised:** 2026-08-21
**Date decided:** 2026-08-25

## Context

The theme was a stack-free starter ([0001](0001-reset-to-a-starter.md)) with
~30 lines of CSS and no opinion about how anything looked. Building the site
chrome forced the question, because a navbar cannot be written without one.

The question is usually framed as *"Tailwind, or CSS variables?"* — and
measuring NSDS shows that framing is wrong. The full measurement is in
[`../17-consuming-the-design-system.md`](../17-consuming-the-design-system.md);
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
roughly 200 KB of source. `abstract/17` §4 is explicit that cherry-picking
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
