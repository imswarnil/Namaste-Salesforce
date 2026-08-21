# 0001 · Reset the theme to a stack-free starter

**Status:** Accepted
**Date:** 2026-08-19

## Context

The theme had grown into a large implementation: Tailwind v4, PostCSS, gulp,
Alpine.js, a vendored copy of NSDS, a generated styleguide, 125 hand-drawn
icons, and templates and partials for seven page types.

None of that was ever *decided*. Each piece arrived in a commit that was
reasonable on its own, and the compound result is `../10-how-this-went-wrong.md`:
~100 theme classes that were NSDS components under different names, three copies
of a lesson row, two tables of contents, two share components, two post cards.
Coverage against NSDS's own reference templates measured **51%** at its worst,
and the site was visually broken while the build, gscan and every static check
were green.

The diagnosis was not "the code is bad." It was that **no layer of the stack had
an owner or a stated reason**, so nothing could be argued with — a duplicate
component was indistinguishable from an intentional one.

## Options

1. **Refactor in place** — migrate the duplicated classes onto NSDS one
   component at a time. Preserves working pages throughout.
2. **Reset to a starter** — delete the implementation, keep the knowledge, make
   each stack decision explicitly before rebuilding.
3. **Leave it** — accept the drift; it renders.

## Decision

**Option 2.** Reduced to five templates, two partials, ~30 lines of CSS, and one
dev dependency (`gscan`, a validator rather than a stack choice).

The reasoning is timing, not aesthetics: the cost of re-deciding scales with
what has been built on top of the undecided thing. Doing it at ~10k lines was
already expensive; doing it later would be worse. Refactoring in place would
have preserved the pages but preserved the ambiguity too — the duplication was a
*symptom*, and migrating it would have treated the symptom.

## Consequences

- **The site does not render its real page types.** That is the accepted price,
  and it is why `../15-starting-from-zero.md` exists.
- **Everything is recoverable from git.** The last full implementation is at
  `f8ec6d8` and its parents. One exception: `partials/icons.hbs`, 125 icons
  drawn to a single contract, has **no cheap regeneration path**. Recover it
  from history rather than redrawing.
- **The knowledge was kept deliberately.** `abstract/` was written *before* the
  deletion, not after. The 17 documents are the actual deliverable of the reset;
  the deletion was the cheap part.
- **`routes.yaml` survived and became a hazard** — see
  [0003](0003-routes-yaml-minimal.md).
- **A reset does not itself prevent recurrence.** It only creates the moment
  where decisions can be made explicitly. If [0002](0002-css-strategy.md) is
  answered by drift rather than by choice, this was wasted.

## Revisit if

Nothing reopens this — it has happened. What can go wrong is the *follow-through*:
if the open decisions are still open once real templates exist, the same failure
is repeating with a cleaner starting point.
