# 13 · Collections, taxonomy and the learning graph

Ghost's `collections` in `routes.yaml` are the most under-used feature in the
platform, and on a learning site they are the difference between "a blog with
categories" and "a curriculum".

Read `01` first — this builds on the URL model — and
[`18-tag-registry.md`](18-tag-registry.md) for the tag *names*, which are
canonical there. This file is about how collections work, not what things are
called.

---

## What a collection actually is

A collection is **a filter + a permalink + a template**. That is it. But those
three things together give you:

- a stable URL shape (`/courses/{course}/{lesson}/`)
- an index page for free
- an RSS feed for free
- pagination for free
- `{{#prev_post}}` / `{{#next_post}}` scoped to the collection

That last one is the important one. **`in="primary_tag"` on prev/next is what
turns a pile of posts into a sequence** — it is the entire mechanism behind
"next lesson", and it costs nothing.

## The four levers, in order of power

### 1. `filter` — what belongs
```yaml
/courses/:
  permalink: /courses/{slug}/
  filter: tag:hash-course
```
Ghost's filter syntax is more capable than most themes use:
`tag:hash-lesson+tag:-hash-draft`, `authors:swarnil`, `published_at:>2026-01-01`,
`visibility:public`. A collection can be as narrow as you like.

### 2. `permalink` — the shape, and the nesting
`{primary_tag}` is what nests a child under its parent. This is the single
cleverest thing in the current setup and it is worth preserving exactly:

```yaml
permalink: /courses/{primary_tag}/{slug}/   # lesson nests under its course
```

⚠️ Use `{slug}` for the PARENT and `{primary_tag}` for the CHILD. Using
`{primary_tag}` for the parent is ambiguous — the parent and all its children
share that tag — and Ghost will 301 to the wrong one. See `abstract/01`.

### 3. `template` — the rendering
A collection index gets its own template. `/courses/` → `courses.hbs`.

### 4. `data` — binding a route to a specific record
```yaml
/docs/getting-started/:
  data: tag.getting-started
  template: docs-section
```
Use this when a section is a TAG with no backing post. If it *can* have a
backing post, prefer a collection — then adding one is Ghost-Admin-only work.

## The rule that decides collection vs route

> **If adding a new one should be possible without touching this repo, it must
> be a collection.**

Training modules are a collection, so adding one is: make the tag, write the
post, publish. Docs sections *were* hand-routed — a `routes.yaml` edit AND a
partial edit each — which is why there were exactly ten and nobody ever added
an eleventh.

**That asymmetry was the bug, and this rule is what caught it.** Docs now use
the same shape as training ([`18`](18-tag-registry.md),
[`decisions/0004`](decisions/0004-tag-vocabulary.md)). Apply the rule to every
new content type before building it, not after.

## The learning graph — what to build on top

Collections give you sequence. A curriculum needs three more relationships,
and all three are expressible with tags today:

| Relationship | Mechanism | Gives you |
| --- | --- | --- |
| **belongs to** | primary tag | nesting, prev/next, "12 lessons" |
| **comes after** | `published_at` order | "next lesson", roadmaps |
| **requires** | `#prereq-*` internal tags | "before you start", gating |
| **counts towards** | `#cert-*` internal tag | "counts towards PD1", cert pages |

The fourth is the one that is barely used and is the most valuable: a page per
**certification** that assembles every lesson tagged `#cert-pd1` across every
course into one path. That is a top-of-funnel landing page you do not have to
write — it is generated from content that already exists.

Same trick for **`#level-*`**: "everything for a beginner, in order" is a
`{{#get}}` away.

## Series — the missing collection

A blog SERIES ("Apex performance, part 3 of 6") is a collection Ghost does not
give you, but a tag plus `{{#get}}` does. NSDS already ships `.ns-series` for
it. Worth adding because series are the format that converts casual readers
into course students.

## Taxonomy hygiene

Two kinds of tag, and never mix them:

- **Public tags** are TOPICS a reader browses (`apex`, `flow`, `security`).
  They get archive pages. Keep the list short — under 20 — or they stop
  meaning anything.
- **Internal tags** (`#`) are STRUCTURE and METADATA. They never appear on the
  site. Unlimited, because nobody browses them.

If you find yourself wanting a public tag that is really a content type, it is
an internal tag. If you find yourself with 60 public tags, you have folders,
not a taxonomy.

## Collections to add next

| Collection | Filter | Why |
| --- | --- | --- |
| `/certifications/{cert}/` | `tag:hash-cert-*` | assembles a path from existing lessons; strong SEO |
| `/series/{series}/` | a series tag | converts readers into students |
| `/toolkit/{slug}/` | `tag:hash-product` | the catalogue — but read `20` first, Ghost takes no one-time payment |
| `/authors/{author}/` | exists as a taxonomy | make it a real page, not an archive |
| `/updated/` | `updated_at` desc | "what changed" — the platform ships 3× a year |
