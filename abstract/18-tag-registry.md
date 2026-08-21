# 18 · The tag registry — the canonical vocabulary

**Every tag this site uses, what it means, and who may create one.**

`01` owns the URL model and `13` owns how collections work. This file owns the
*names*. When they disagree, this file wins and the other two get fixed.

Fix the vocabulary **now**, while there is no content. Renaming a tag later
means re-tagging every post and 301-ing every URL underneath it — this is the
second-most expensive thing to change here, after `routes.yaml` itself.

---

## ⚠️ Read this before designing any hierarchy

> **A Ghost permalink has exactly one `{primary_tag}` placeholder. You get two
> URL levels. There is no third.**

The placeholders are `{slug}`, `{id}`, `{year}`, `{month}`, `{day}`,
`{primary_tag}`, `{primary_author}`, `{author}`. A post has exactly one primary
tag, so a permalink can express *parent → child* and nothing deeper:

```yaml
permalink: /courses/{slug}/                    # parent — see the slug==tag rule in 01
permalink: /courses/{primary_tag}/{slug}/      # child  — nests automatically
permalink: /training/{track}/{module}/{slug}/  # ✗ IMPOSSIBLE. No second tag placeholder.
```

This directly constrains the three-level shapes: `#training` →
`#training-module` → `#training-module-content`, and `#docs` → `#docs-section`
→ `#docs-content`. **Neither can exist as three URL levels.**

That is not a problem, because the top level of each was never a *content*
level. `/training/` and `/docs/` are landing pages that list what is below
them. A landing page needs a route or a Ghost page — **it does not need a
tag**. Dropping `#training` and `#docs` costs nothing and buys a hierarchy that
Ghost can actually express.

> **Rule: tag a thing only if something must FIND it by filter.** Nothing
> filters for "the training landing page" — there is one, and it is at a known
> URL.

If you genuinely need multiple training *tracks* later, they become a facet
(`#track-admin`) that the landing page filters on, not a URL segment. The URL
stays `/training/{module}/{lesson}/`.

---

## The registry

### Structural tags — what a post IS

Exactly one per post. This tag decides which template renders it (`02`).

| Tag | The post is | Primary tag | URL |
| --- | --- | --- | --- |
| `#blog` | a blog post | — | `/blog/{slug}/` |
| `#course` | a course overview | **its own course tag** | `/courses/{slug}/` |
| `#lesson` | a lesson in a course | **its course's tag** | `/courses/{course}/{slug}/` |
| `#training-module` | a module overview | **its own module tag** | `/training/{slug}/` |
| `#training-lesson` | a lesson in a module | **its module's tag** | `/training/{module}/{slug}/` |
| `#docs-section` | a docs section overview | **its own section tag** | `/docs/{slug}/` |
| `#docs-page` | a page in a section | **its section's tag** | `/docs/{section}/{slug}/` |
| `#resource` | one resource | — | `/resources/{slug}/` |
| `#product` | something for sale | — | `/toolkit/{slug}/` |

**The slug==tag rule from `01` applies to all four parents** — `#course`,
`#training-module`, `#docs-section`, and any future one. The parent post's slug
must equal its own tag's slug, or its children 301 to the wrong parent.

### Facet tags — what a post is ABOUT or FOR

Any number per post. These never decide a template; they feed `{{#get}}`
filters, badges and generated landing pages.

| Pattern | Example | What it powers |
| --- | --- | --- |
| `#level-*` | `#level-beginner` | "everything for a beginner, in order" |
| `#cert-*` | `#cert-pd1` | a page per certification, assembled from existing lessons |
| `#prereq-*` | `#prereq-apex-basics` | "before you start" blocks, soft gating |
| `#series-*` | `#series-apex-perf` | "part 3 of 6" — see `13` |
| `#format-*` | `#format-video` | filtering a mixed list by medium |

`#cert-*` is the highest-leverage one and the most neglected. A
`/certifications/pd1/` page that gathers every `#cert-pd1` lesson across every
course is **a top-of-funnel landing page you never write** — it is generated
from content that already exists, and it targets exactly what people search.

### Public tags — TOPICS a reader browses

No `#`. These get archive pages at `/tag/{slug}/` and appear on the site:
`apex`, `flow`, `lwc`, `security`, `data-modelling`, `integration`.

**Keep this list under 20.** Past that they stop meaning anything and you have
folders, not a taxonomy. If you want a public tag that is really a content
type, it is an internal tag.

---

## The naming rules

**1 · Structural tags are singular.** The tag names what the post *is*: one
post is one `#resource`. The *collection* is plural because it is a list:
`#resource` → `/resources/`, `#product` → `/toolkit/`.

**2 · A child tag says what the child is**, not that it is "content".
`#training-lesson`, not `#training-module-content`. Everything on the site is
content; the word carries no information, and it makes the tag longer than the
thing it describes. Parallel structure is the point:

```
#course           → #lesson
#training-module  → #training-lesson
#docs-section     → #docs-page
```

**3 · Facets are `#prefix-value`.** The prefix is the axis, the value is the
position on it. This is what makes `filter="tag:hash-cert-pd1"` and a wildcard
sweep of the whole axis both work.

**4 · In a filter string an internal tag is `hash-`, not `#`.**
`filter="tag:hash-lesson"`. In `{{#has}}` it is `#lesson`. Getting this wrong
fails silently — the filter matches nothing and you get an empty list, not an
error.

**5 · Never rename a public tag after publishing.** It is a URL.

---

## Changes from earlier drafts, and why

If you find the old names in `01`, `13` or an old commit, these supersede them.

| Was | Now | Why |
| --- | --- | --- |
| `#training-section` | `#training-module` | "module" is what learners call it; "section" collides with docs |
| `#training-content` | `#training-lesson` | parallel with `#lesson`; says what it is |
| `documentation` (public!) | `#docs-page` | it was a public tag doing a structural job — it would have got an archive page competing with `/docs/` in search |
| docs sections as bare TAGS | `#docs-section` **posts** | see below — this is the real upgrade |
| `#resources` (plural) | `#resource` | rule 1 |
| `#digital-downloads` + `#products` | `#product` | one collection; see below |
| `#training`, `#docs` | *dropped* | landing pages, not filterable things |

### Docs become a collection, and this is the biggest win here

`01` records that the ten docs sections are hand-routed, each needing a
`routes.yaml` entry **and** a partial edit — and notes that this is why nobody
ever added an eleventh. `13` states the rule that condemns it:

> **If adding a new one should be possible without touching this repo, it must
> be a collection.**

Giving each section a backing post tagged `#docs-section` makes docs work
exactly like training: make the tag, write the post, publish. No route edit, no
theme edit, no deploy. It also gives every section a real overview page with an
intro, which the `data: tag.x` version could never have.

The cost is that each section now needs a post to exist before its children
resolve. That is one post, and it is a page you wanted anyway.

---

## `#product` and the Ghost constraint that shapes it

One tag, one collection. `#digital-downloads` and `#products` are the same
thing wearing two names — a template, a checklist pack, an ebook and a
recorded workshop are all *a thing someone buys*. Splitting them at the tag
level would mean two collections, two templates and two index pages for one
catalogue of maybe fifteen items. If you need the distinction, it is a facet:
`#format-template`, `#format-ebook`, `#format-workshop`.

**Collection name: `/toolkit/`.** `/store/` and `/shop/` are clearer about
commercial intent and would probably convert marginally better cold; `/toolkit/`
says what the buyer gets rather than what you are doing to them, and it fits a
site whose whole proposition is "the things that save you time." Either is
defensible — this is a genuine coin-flip and it is recorded in
[`decisions/0004`](decisions/0004-tag-vocabulary.md) so it can be reopened
without re-arguing.

> ### ⚠️ Ghost cannot take a one-time payment
>
> Ghost Members is **subscriptions only**. There is no native one-off checkout,
> so `/toolkit/` cannot sell a ₹499 template on its own. Your options:
>
> 1. **Make the toolkit a tier benefit** — everything in it unlocks with a paid
>    subscription. Best for recurring revenue, and it makes `/toolkit/` a
>    *reason to subscribe* rather than a competing transaction.
> 2. **External checkout** — Gumroad / Lemon Squeezy / Razorpay, with `#product`
>    posts as the landing pages. Ghost still gets the SEO and the email capture;
>    the payment happens elsewhere.
>
> **Verify this before building either.** It is the kind of platform limit that
> changes between versions — check current Ghost docs rather than trusting this
> line. See `20` for how this interacts with pricing.

---

## Adding a tag

Facets and public tags: just add them, they cost nothing.

**A new structural tag is a different matter** — it needs a collection, a
template, a `routes.yaml` entry and a branch in the `post.hbs` dispatcher, and
branch order there is load-bearing (`02`). Nine structural tags is already a
lot. Before adding a tenth, check whether it is really a facet on an existing
one.

## Verify

```bash
# Does Ghost still allow only one {primary_tag}? (check the docs, not this file)
open https://ghost.org/docs/themes/routing/#permalinks

# Every structural tag has a template and a route:
grep -oE 'template: [a-z-]+' routes.yaml | sed 's/template: //' | sort -u \
  | while read t; do [ -f "$t.hbs" ] || echo "MISSING $t.hbs"; done
```
