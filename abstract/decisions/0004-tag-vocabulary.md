# 0004 · The tag vocabulary

**Status:** Proposed — adopt or amend before the first real post is published
**Date:** 2026-08-21

## Context

The registry is [`../18-tag-registry.md`](../18-tag-registry.md). This records
the choices inside it that were genuine forks rather than obvious calls.

Two facts force most of the decision:

1. **A Ghost permalink has exactly one `{primary_tag}` placeholder.** Two URL
   levels, parent and child. There is no third. A proposed three-level shape —
   `#training` → `#training-module` → `#training-module-content`, and the same
   for docs — cannot be expressed as URLs.
2. **The theme has no content yet.** Renaming a tag after publishing means
   re-tagging every post and 301-ing every URL beneath it. This is the last
   moment it is free.

## Options

**On the third level:** invent a nesting scheme outside the permalink (a facet
tag plus theme logic that fakes the depth), or accept two levels.

Accepted two levels. The top level of each proposed hierarchy — `#training`,
`#docs` — was never a content level; it is a landing page listing what is below
it, and a landing page needs a route, not a tag. Faking a third level means
hand-built URLs that Ghost's own `{{#prev_post}}`, collection index, RSS and
pagination know nothing about, which discards most of what `13` says
collections are for. Multiple training *tracks*, if they ever exist, become a
facet the landing page filters on.

**On `#docs-section` as a post rather than a bare tag:** keep the ten
hand-routed `data: tag.x` entries, or give each section a backing post.

Changed to posts. `13`'s own rule decides it — *if adding a new one should be
possible without touching this repo, it must be a collection* — and the old
model is self-evidently the failure case: it needed a `routes.yaml` edit plus a
partial edit per section, and in practice nobody ever added an eleventh. The
cost is one post per section, which is a page you wanted anyway.

**On `#digital-downloads` + `#products`:** two tags or one.

One, `#product`. They are the same thing wearing two names — a template pack,
an ebook and a recorded workshop are all *a thing someone buys*. Two tags means
two collections, two templates and two index pages for one catalogue of maybe
fifteen items. Format becomes a facet (`#format-template`).

**On the collection name:** `/store/`, `/shop/`, `/downloads/` or `/toolkit/`.

`/toolkit/`, and this one is close to a coin-flip. `/store/` is clearer about
commercial intent and would likely convert marginally better on cold traffic.
`/toolkit/` names what the buyer gets rather than what you are doing to them,
and fits a site whose proposition is "the things that save you time". Recorded
here precisely because it is arguable, so it can be reopened without
re-deriving the argument.

**On `-content` vs `-lesson` / `-page`:** the proposed `#training-module-content`
and `#docs-content` became `#training-lesson` and `#docs-page`. Everything on
the site is content, so the word carries no information and makes the tag longer
than the thing it names. `#course`→`#lesson` already existed; the parallel is
worth more than the literal accuracy.

## Decision

Nine structural tags, singular, two levels maximum:

```
#blog
#course           → #lesson
#training-module  → #training-lesson
#docs-section     → #docs-page
#resource
#product
```

Plus facets (`#level-*`, `#cert-*`, `#prereq-*`, `#series-*`, `#format-*`) and
under 20 public topic tags. `#training` and `#docs` are dropped.

## Consequences

- **`01` was rewritten to match** — its kinds table and its target
  `routes.yaml` both. There is now one vocabulary, and `18` is where it lives;
  `01` carries a pointer saying so. Two documents describing the same names in
  their own words is how they drift.
- **Docs gained a template requirement.** `docs-section` needs a real overview
  template, and each section needs a post before its children resolve.
- **`/toolkit/` cannot transact.** Ghost is subscriptions-only, so those pages
  are either a tier benefit or a link to an external checkout. See
  [`../20`](../20-subscriptions-and-growth.md) — this shapes pricing, not just
  routing.
- **Nine structural tags is a lot**, and each one costs a collection, a
  template, a route and a dispatcher branch whose order is load-bearing (`02`).
  A tenth should have to argue for itself against being a facet.
- **Everything above is free to change today and expensive after the first
  publish.** That asymmetry is the entire reason this is being decided now
  rather than when it comes up.

## Revisit if

- Multiple training tracks become real — the answer is a facet on the landing
  page, not a URL segment, and that is worth re-confirming against Ghost's
  permalink placeholders rather than assumed.
- `/toolkit/` conversion is measurably poor on cold traffic — try `/store/`.
  It is a 301 and a template rename, cheap while the catalogue is small.
- Ghost adds a second permalink tag placeholder, or one-time payments. Both
  would reopen real choices here.
