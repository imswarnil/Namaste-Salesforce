# 0003 · `routes.yaml` names only templates that exist

**Status:** Accepted
**Date:** 2026-08-21

## Context

`routes.yaml` is the most valuable file in the project — it defines every
collection, permalink and URL, and `../01-content-model.md` calls it the only
part that is expensive to change later. So it was deliberately preserved
untouched through the reset ([0001](0001-reset-to-a-starter.md)).

That was a mistake, and an instructive one. It still named **eleven** templates.
Ten had just been deleted:

```
MISSING blog · courses · docs-section · documentation · page-about
        page-become-author · page-sponsor · resources · training · training-section
OK      index
```

**A route pointing at a missing template is a 400, not a fallback.** Ghost
answers `Missing template courses.hbs for route /courses/` and the page is dead;
there is no degradation to `index`. Uploading the preserved file to the emptied
Ghost would have broken every URL on the site — and this failure had already
been hit once in this project, reported as `400 Missing template home.hbs`.

The file did not change. Everything it pointed at did.

## Options

1. **Ship it whole** — it is the canonical model. (400s on ten routes.)
2. **Delete it** — regenerate when templates exist. (Loses the model, which is
   the expensive part; the templates are the cheap part.)
3. **Trim to servable routes, preserve the full model in prose.**

## Decision

**Option 3.** `routes.yaml` carries `/` → `home` plus one catch-all collection.
The full model is preserved verbatim in a fenced block at the bottom of
`../01-content-model.md`.

**Restore one entry in the same commit that adds the template that serves it.**
Never ahead of it.

## Consequences

- The shipped file no longer documents the intended URL structure — a reader
  must follow the pointer to `../01`. Accepted: a file that 400s the site is
  worse than one that under-describes it.
- Two files must now stay in step. `../01` says so explicitly, and the release
  checklist in `../15` carries the one-line check:
  `grep -oE 'template: [a-z-]+' routes.yaml`
- The single collection means all posts currently share one flat permalink
  space. Correct for a starter; it is superseded the moment courses land, and
  that is a URL change, which is a **MAJOR** version bump (`CHANGELOG.md`).

## The general lesson

> **A file is only "unchanged" relative to what it points at.**

Preservation reasoning ("this file is valuable, don't touch it") is about the
file's *contents*. Correctness is about its *referents*. Anything naming things
outside itself — routes, config, CI paths, docs with file links — needs
re-validating after a deletion, precisely *because* it was not edited. A diff
will never show it.

## Revisit if

The theme reaches a point where most page types exist. At that stage the
minimal file is the liability rather than the safeguard, and `../01`'s block
should be restored wholesale and this record superseded.
