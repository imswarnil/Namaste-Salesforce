# 0002 · How the theme gets its CSS

**Status:** **Open** — this is the decision that gates all styling work
**Date raised:** 2026-08-21

## Context

The theme is a stack-free starter ([0001](0001-reset-to-a-starter.md)).
`assets/css/screen.css` is ~30 lines of what Ghost itself requires and is
explicitly disposable.

The question is usually framed as *"Tailwind, or CSS variables?"* — and
measuring NSDS shows that framing is wrong. The full measurement is in
[`../17-consuming-the-design-system.md`](../17-consuming-the-design-system.md);
the load-bearing facts:

- **NSDS is already a CSS-variables system.** 407 custom properties, 663 `.ns-*`
  classes, 300 component blocks — and across all 33 component stylesheets there
  is **no `@apply`, no `theme()`, no `tw-` prefix**. The component layer is
  plain CSS whose only dependency is `var(--…)`.
- **Tailwind is a projection, not a foundation.** `tokens/tailwind.css` is
  *generated* from the same token files and only re-declares each token inside
  `@theme` so a utility name exists. Removing it costs zero declarations.
- **The framework-neutral build already ships**: `dist/namaste-ui.css`,
  420 KB minified, described by NSDS's own build script as droppable into a page
  "with no build step at all."
- **Tailwind would not shrink it.** Purging only removes generated utilities;
  `@layer ns-components` is hand-written and included verbatim either way.
  Cherry-picking `components/css/*.css` is the actual lever (~200 KB of LMS-only
  surfaces a Ghost site never renders).
- **The neutral bundle has no reset.** It depends on Tailwind's Preflight for
  `box-sizing: border-box`, `img` sizing, list and table normalisation — none of
  which are in the neutral build. 89 rules declare a width alongside padding,
  so under `content-box` they overflow by their own padding. Fixable in three
  lines, but it must not be discovered in production.

So this is not a question about what NSDS is made of. It is a question about
**whether the theme wants utilities for composing its own markup.**

## Options

### A · Framework-neutral CSS, no build step
Import `dist/namaste-ui.css` (or a cherry-picked entry), add the missing reset,
write theme-specific rules as named classes in `@layer components`.

- **Cost to adopt:** one file copied into `assets/css/`. The bundle's only real
  `url()`s are `../fonts/` and `../icons/`, which resolve correctly from
  `assets/css/` with no rewriting.
- **Gains:** no build, no `assets/built/` to keep in sync, no stale-output
  class of bug, a contributor needs nothing but a text editor.
- **Costs:** every one-off tweak is a named class. Full weight until trimmed.

### B · Tailwind v4 + NSDS
What the previous implementation did.

- **Gains:** A, plus `p-card` / `bg-brand-500` composition, and NSDS's own
  styleguide is authored this way so its examples paste in directly.
- **Costs:** a build step and a committed `assets/built/`; the layer-order trap
  in `../05-css-architecture.md` becomes live again; every `.hbs` edit needs a
  rebuild because the content scan reads class names out of templates. **This
  is the configuration that produced `abstract/10`** — which is an argument for
  care, not an argument against it.

### C · Neutral CSS + ~15 hand-written utilities
Stack, cluster, visually-hidden, measure — the handful a Ghost theme genuinely
repeats, written once against the tokens.

- **Gains:** keeps the no-build property, avoids one-class-per-tweak sprawl.
- **Costs:** you maintain it, and it is the seed of the "third opinion" that
  `abstract/00` identifies as the root cause of most rework here. Viable only
  with a hard cap written into the file itself.

## Decision

**Not yet made.** Recorded so it is made deliberately rather than by the first
commit that needs a margin.

**Recommendation: start at A.** Not because utilities are wrong, but because A
is the only option that is reversible for free. A → B is an afternoon of adding
a build; by then you will know from real templates whether the utilities are
actually missed, instead of guessing now. Nothing in A forecloses B, and B's
failure mode is already documented in this repo.

## Consequences

**If A:** the theme owns a small named-class layer, and there will be a
recurring temptation to grow it into a system. That temptation is the exact
mechanism behind the ~100 duplicated classes in `abstract/10`. Guard it with the
`abstract/00` rule — *check Ghost, then NSDS, then write* — and treat any new
theme class as a defect until proven otherwise.

**Whichever wins:** the layer contract is inherited and non-negotiable —
`@layer theme, base, ns-components, components, utilities`, declared before any
`@import`, nothing outside a layer. One unlayered rule beats every layered rule
at any specificity.

**And regardless:** the missing reset from §3 of `../17` must be added in the
same commit that first imports NSDS. Not afterwards.

## Revisit if

- The theme's own class layer passes ~40 classes — utilities are being
  hand-rolled and B or C is now cheaper than A.
- CSS weight shows up in a real measurement on a real page (not a guess), and
  cherry-picking `components/css/` has already been tried.
- NSDS changes its distribution model — e.g. drops the neutral bundle, or moves
  the component layer to `@apply`. Re-check with the commands at the end of
  `../17`.
