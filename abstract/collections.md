# Collections — decide the surface, then build it

Eight page families. **None is specified, and none gets built before its
section here is answered.**

That is not process for its own sake. The last version of this theme had its
content model assembled one reasonable commit at a time, and the result —
recorded in [`09-lessons.md`](09-lessons.md) — was ~100 duplicated classes,
three copies of a lesson row, two tables of contents, and a set of URLs nobody
had decided. Every one of those started as a template written before anyone
had said what the page was.

Fill in the `→` lines. The **proposed** values are carried over from the
previous content model and have no authority — overwrite them. The **decided**
column is what `routes.yaml` gets built from.

---

# Part 1 · What you are deciding

## A collection is a filter, a permalink and a template

Those three things buy you a stable URL shape, an index page, an RSS feed,
pagination, and `{{#prev_post}}` / `{{#next_post}}` scoped to the collection.

That last one is the important one. **`in="primary_tag"` on prev/next is what
turns a pile of posts into a sequence** — it is the entire mechanism behind
"next lesson", and it costs nothing.

[`01-content-model.md`](01-content-model.md) has the full mechanics.

## The six questions, explained

Each section below asks the same six. This is what they are really asking.

### 1 · What is it NOT?

Name the neighbouring collection this keeps being confused with, and the line
between them, in one sentence. **Answer this before anything else.**

Two collections that cannot be told apart in a sentence are one collection,
and finding that out now costs nothing — finding it out after both have URLs
and published posts costs a migration. **Courses and training are the pair
most likely to collapse into each other.**

### 2 · Who arrives, and what do they do next?

Where do they come from — search, the nav, a link inside a lesson? What is the
single action this page exists to make easy? If the answer is "several
things", the page does not have a job yet.

### 3 · The URL model

**The only genuinely expensive part.** Everything else here can be rebuilt in
an afternoon; a published URL cannot move without 301s and lost ranking.

- **mount** — where the index lives (`/courses/`).
- **permalink** — where the posts live. `{slug}` for a parent,
  `{primary_tag}/{slug}` for a child, which is what nests one under the other.
  **Never `{primary_tag}` for a parent**: it is shared with all its children,
  and Ghost will 301 to the wrong one.
- **internal tag** — the `#tag` that routes a post here. Names are canonical in
  the root knowledge base, not decided here.
- **filter** — Ghost's filter syntax. Internal tags are written
  `tag:hash-course`, never `tag:#course`.

Also decide: **paginated**, and at what size? **Its own RSS feed?**

> **The one rule that breaks everything if broken:** a parent post's slug must
> equal its own tag's slug. That is what lets the parent use `{slug}` while its
> children use `{primary_tag}/{slug}` and still nest correctly.

### 4 · The listing

Grid of cards, dense table, roadmap, rail with filters? What is the sort
order, and is it different for a signed-in member?

Then: which fields are visible on one item — title, excerpt, cover, tag, date,
reading time, duration, level, index number, progress, price?

And: **what does it look like with nothing in it?** Every band on the homepage
hides itself when empty; a listing cannot, so it needs a real empty state.

### 5 · The single page

Table of contents, breadcrumb, previous/next, a rail, an author box, related
items, a share row, a CTA? And what is at the bottom — what should the reader
do when they finish?

### 6 · Members

Free, members-only, paid, or mixed. If mixed, what does a signed-out reader
see: a preview, a locked card, or nothing at all? Ghost's `visibility` and
`{{#unless @member}}` are the mechanism.

## Tag names are not decided here

They are canonical in the root knowledge base at
`Namaste Salesforce/abstract/05-content/tag-registry.md`. This file decides
what a surface *does*; that file decides what things are *called*, because the
names are shared with the LMS and the content pipeline and cannot be a
theme-local choice.

---

# Part 2 · The build steps

Identical for every collection, which is why they are written once. Work down
the list; nothing here is optional.

- [ ] The tag exists in Ghost Admin, and its name matches the tag registry
- [ ] `routes.yaml` — collection block added, permalink and filter as decided
- [ ] Listing template exists and is named in `routes.yaml`. **Ghost does not
      validate a `template:` key** — a typo silently falls back to `index.hbs`,
      so the page renders, and renders wrong
- [ ] A branch in `post.hbs` for the single page, delegating to exactly one
      partial in `partials/post/` — no markup in the dispatcher itself
- [ ] The chrome dispatch in `default.hbs` — does this surface get the site
      bar, or does it carry its own?
- [ ] Structured data for the kind — [`06-discoverability.md`](06-discoverability.md)
      §2 says which type. `Article` is Ghost's default and is rarely right
- [ ] An empty state on the listing
- [ ] `npm run build` clean: classes defined, icons present, layers hold,
      asset urls resolve
- [ ] **Looked at** — in both themes, at 360px, with JavaScript off. gscan and
      a green build have both been green on a visually broken site

---

# Part 3 · The eight surfaces

## 01 · Home

Archetype: `homepage.html` + `sections-home.html` · Template: `home.hbs`
*Partly built — see `partials/home/`. Two bands are marked ⚠ DUMMY.*

| | proposed | decided |
|---|---|---|
| mount | `/` | → |
| permalink | — (a designed page, not a collection) | → |
| internal tag | — | → |
| filter | — | → |

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 02 · Blog

Archetype: `blog-listing.html` → `blog-post.html` · Template: `blog.hbs`

| | proposed | decided |
|---|---|---|
| mount | `/blog/` | → |
| permalink | `/blog/{slug}/` | → |
| internal tag | `#blog` | → |
| filter | `tag:hash-blog` | → |

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 03 · Courses

Archetype: `course-listing.html` → `course-detail.html` → `course-player-article.html`
Template: `courses.hbs`

| | proposed | decided |
|---|---|---|
| mount | `/courses/` | → |
| permalink | `/courses/{slug}/` | → |
| internal tag | `#course` | → |
| filter | `tag:hash-course` | → |
| child permalink | `/courses/{primary_tag}/{slug}/` | → |
| child tag | `#lesson` | → |

1. **Not:** *(start here — this is the one most likely to be the same thing as training)* →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 04 · Training

Archetype: `training-index.html` → `training-module.html` → `training-post.html`
Template: `training.hbs`

| | proposed | decided |
|---|---|---|
| mount | `/training/` | → |
| permalink | `/training/{slug}/` | → |
| internal tag | `#training-module` | → |
| filter | `tag:hash-training-module` | → |
| child permalink | `/training/{primary_tag}/{slug}/` | → |
| child tag | `#training-lesson` | → |

1. **Not:** *(and specifically: how is this not Courses?)* →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 05 · Docs

Archetype: none fits — compose `.ns-sidenav` + `.ns-tree` + `.ns-post__rail`
Template: `docs.hbs` · Behaviour: `rail.js`, `toc.js`, `code.js`

| | proposed | decided |
|---|---|---|
| mount | `/docs/` | → |
| permalink | `/docs/{slug}/` | → |
| internal tag | `#docs-section` | → |
| filter | `tag:hash-docs-section` | → |
| child permalink | `/docs/{primary_tag}/{slug}/` | → |
| child tag | `#docs-page` | → |

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 06 · Resources

Archetype: none — compose; `.ns-card` grid or `.ns-table` · Template: `resources.hbs`

| | proposed | decided |
|---|---|---|
| mount | `/resources/` | → |
| permalink | `/resources/{slug}/` | → |
| internal tag | `#resource` | → |
| filter | `tag:hash-resource` | → |

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 07 · Toolkit

Archetype: `.ns-buybox` + `.ns-product` · Template: `toolkit.hbs`

| | proposed | decided |
|---|---|---|
| mount | `/toolkit/` | → |
| permalink | `/toolkit/{slug}/` | → |
| internal tag | `#product` | → |
| filter | `tag:hash-product` | → |

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

## 08 · Archive — the catch-all

Archetype: `blog-listing.html` → `blog-post.html` · Template: `index.hbs`
*Built. Currently mounted at `/archive/` with a flat `/{slug}/` permalink.*

| | proposed | decided |
|---|---|---|
| mount | `/archive/` | → |
| permalink | `/{slug}/` | → |
| internal tag | — (none: whatever matches nothing else) | → |
| filter | — (unfiltered, and it must be LAST) | → |

> ⚠ **Unfiltered and last, always.** Every post lands here until a narrower
> collection claims it. A filter here makes any post matching nothing
> unroutable — a 404 on a published post, invisible until someone reports it.
>
> ⚠ **The feed lives at the mount**, so it is currently `/archive/rss/` and the
> templates link to it there. Change the mount and grep the theme for
> `archive/rss`.

1. **Not:** →
2. **Who / next action:** →
3. **Pagination · feed:** →
4. **Listing:** →
5. **Single page:** →
6. **Members:** →

---

## Starting a ninth

Copy any section above, and answer question 1 first. If the answer to "what is
it NOT" needs more than a sentence, the surface is probably two surfaces — or
it is one of the eight already here.
