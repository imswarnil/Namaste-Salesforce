# 01 · The content model and `routes.yaml`

**This is the most important file here. Everything else is recoverable; this
is not — get it wrong and every URL on the site changes.**

`routes.yaml` is NOT read from the theme folder. It is uploaded in
**Ghost Admin → Settings → Labs → Routes**. It lives in the repo so it is
versioned next to the templates that depend on it, and the two must agree.

---

## The kinds of content, and the tag that makes each one

Everything is a Ghost POST. What it *is* comes from its tags.

| Kind | Tag | Primary tag | URL |
| --- | --- | --- | --- |
| Course | `#course` | its own course tag | `/courses/{slug}/` |
| Course lesson | `#lesson` | its **course's** tag | `/courses/{course-tag}/{slug}/` |
| Training module | `#training-module` | its own module tag | `/training/{slug}/` |
| Training lesson | `#training-lesson` | its **module's** tag | `/training/{module}/{slug}/` |
| Docs section | `#docs-section` | its own section tag | `/docs/{slug}/` |
| Docs page | `#docs-page` | its **section's** tag | `/docs/{section}/{slug}/` |
| Resource | `#resource` | — | `/resources/{slug}/` |
| Product | `#product` | — | `/toolkit/{slug}/` |
| Blog post | `#blog` | — | `/blog/{slug}/` |
| anything else | — | — | `/archive/{slug}/` |

> **the root abstract's [`05-content/tag-registry.md`](../../../../../abstract/05-content/tag-registry.md) is canonical for these names**,
> and explains why a three-level hierarchy is impossible in Ghost. This table is
> a summary of it — if the two ever disagree, 18 wins and this gets fixed.

Tags starting `#` are Ghost **internal** tags: they never appear on the site,
which is exactly why they carry structure and metadata.

---

## THE ONE RULE THAT BREAKS EVERYTHING IF BROKEN

> **A course post's slug must equal its course tag's slug.**
> **A section post's slug must equal its section tag's slug.**

Why: the permalink uses `{slug}`, not `{primary_tag}`.

A course and *all of its lessons* share the same primary tag. If the course
permalink used `{primary_tag}`, Ghost could not tell the course from its
lessons and would **301 to the wrong course**. Using `{slug}` is unambiguous
because a slug is unique per post.

And because `course-slug == course-tag`, the lesson permalink
`/courses/{primary_tag}/{slug}/` still nests every lesson under its course
automatically. The two rules are one mechanism.

The same trick, for the same reason, makes `/training/start/` (the section)
and `/training/start/{lesson}/` (its lessons) line up.

## Nesting works because primary tag is inherited

A lesson's PRIMARY tag *is* its parent's tag. That single fact is what makes
`{primary_tag}` in a permalink produce the nesting, and it is also what
`{{#get}}` filters rely on everywhere in the templates:

```hbs
{{#get "posts" filter="primary_tag:{{primary_tag.slug}}+tag:hash-lesson"}}
```

Note `hash-lesson`, not `#lesson` — in a **filter string** Ghost writes an
internal tag as `hash-`.

## Adding a training section is Ghost-Admin-only

Make the tag → write a post tagged `#training-module` with a matching slug →
publish. **No `routes.yaml` edit, no theme edit.** Order is `published_at asc`,
so backdate a post to move it earlier.

This replaced a hand-maintained route-per-section list plus an ordered partial
that both had to be kept in sync by hand. Do not reintroduce either.

## Tag pages redirect rather than duplicate

`tag.hbs` is not an archive for course and section tags — it redirects:

- `/tag/{course-tag}/` → the course
- `/tag/{section-tag}/` → `/training/{section}/`

detected by the backing POST whose primary tag it is, so a brand-new empty
section still redirects. Serving an archive there would be a worse duplicate
of a page that already exists, competing with it in search.

⚠️ The `../` depths inside `tag.hbs` are load-bearing. **Never call a Ghost
HELPER across `../`** (`{{../url}}`) — Ghost throws and 500s the page. Dotted
PROPERTY access (`{{primary_tag.slug}}`, `{{../../id}}`) is fine.

## Docs sections were routed one-by-one — and that is now reversed

The old model gave docs ten `/docs/{section}/` routes with `data: tag.{slug}`,
because a docs section was a TAG with no backing post and a collection had
nothing to discover. Adding one meant a `routes.yaml` edit **and** a partial
edit, which is precisely why there were exactly ten and nobody ever added an
eleventh.

**Docs now use the same two-level shape as training**: a section is a POST
tagged `#docs-section`, so adding one is Ghost-Admin-only work and the section
gets a real overview page. The reasoning is in
the root abstract's `05-content/tag-registry.md`;
`13`'s rule is what forced it — *if adding a new one should be possible without
touching this repo, it must be a collection.*

## Content-less routes

`/`, `/training/`, `/about/`, `/become-author/`, `/sponsor/` render a template
standalone. Each also works if a Ghost PAGE with the matching slug exists —
the templates fork on `{{#page}}` to pick up a title and excerpt from Admin.


---

## The full `routes.yaml`, as a target

The shipped `routes.yaml` is deliberately minimal — a route pointing at a
template that does not exist is a **400**, not a fallback, so it only ever
carries routes the theme can serve.

This is the model to grow back into. **Move one entry at a time, in the same
commit that adds its template.**

```yaml
# routes.yaml — Namaste Salesforce
# Upload in Ghost Admin → Settings → Labs → Routes (this file is NOT read from
# the theme folder; it lives here so it's versioned alongside the theme).
#
# URL model (nested course → lesson):
#   /courses/                      list of courses (courses template)
#   /courses/{course-tag}/         a single course  (post #course, primary tag = course tag)
#   /courses/{course-tag}/{slug}/  a lesson of that course (post #lesson, primary tag = course tag)
# Because a lesson's primary tag == its course's tag, the {primary_tag} segment
# nests every lesson under its course automatically.
#
# Content model (matches the templates' tag conventions + dummy-content/*.json):
#   Course       = post tagged #course,  primary tag = course tag (e.g. apex)
#   Lesson       = post tagged #lesson,  primary tag = its course's tag
#   Training     = /training/ itself. There is ONE training, so it has no post
#                  of its own — the landing lists its sections.
#   Module       = POST tagged #training-module, PRIMARY tag = the module tag,
#                  and post slug == that tag's slug (e.g. slug "start", primary
#                  tag "start"). The post BODY is the section overview.
#                  → /training/start/
#   Lesson       = post tagged #training-lesson, PRIMARY tag = its module tag.
#                  → /training/start/{lesson-slug}/
#   Section ORDER = published_at asc. Backdate a section post to move it earlier.
#
#   Adding a section is therefore Ghost-Admin-only: make the tag, write the
#   section post with a matching slug, publish. No routes.yaml edit, no theme
#   edit. (This replaced a hardcoded route-per-section list plus an ordered
#   partial that both had to be kept in sync by hand.)
#   Doc page     = post tagged `#docs-page`, primary tag = its #docs-section tag
#   Resource     = post tagged #resource
#   Blog post    = post tagged #blog
#   Pages: /about/, /products/, /contact/ use page-{slug}.hbs automatically.
#
# TAG pages redirect in tag.hbs rather than serving a duplicate archive:
#   /tag/{course-tag}/   -> the course
#   /tag/{module-tag}/   -> /training/{module}/   (detected by the #training-module
#                           POST whose primary tag it is — the section's backing post)

routes:
  /: home
  # Content-less routes → these templates render standalone (also work if a
  # Ghost page with the matching slug exists).
  /become-author/:
    template: page-become-author
  /about/:
    template: page-about
  /sponsor/:
    template: page-sponsor

  # ── Training ──────────────────────────────────────────────────────────
  # /training/ is the single training's landing (no #training post backs it;
  # a Ghost PAGE with slug `training` will supply the title/excerpt if one
  # exists — training.hbs forks on {{#page}}).
  /training/:
    template: training

  # NOTE: sections are NO LONGER routed one-by-one here. A section is a POST
  # (tagged #training-module) and is served by the /training-modules/
  # collection below, so adding a section is pure Ghost Admin work — no route
  # edit, no theme edit. See the collection for the slug rule.

  # Docs section pages — /docs/{section}/ (clean slugs, no numbering).
  # Each renders docs-section.hbs with its tag as {{tag}}. Section tag slugs
  # in Ghost Admin must match (rename docs-01-getting-started → getting-started
  # etc.). Keep this list in sync with partials/docs/sections.hbs.

collections:
  # Courses list + single course at /courses/{course-slug}/.
  # IMPORTANT: give each course POST a slug equal to its course TAG (e.g. course
  # "Apex Masterclass" → slug "apex", primary tag "apex"). The course URL uses
  # {slug} (unique) — using {primary_tag} is ambiguous because the course and
  # all its lessons share that tag, which makes Ghost 301 to the wrong course.
  # Because course-slug == course-tag, lessons still nest under /courses/{tag}/.
  /courses/:
    permalink: /courses/{slug}/
    template: courses
    filter: tag:hash-course

  # Lessons nest under their course: /courses/{course-tag}/{lesson-slug}/
  # (the /lessons/ path is just this collection's archive index.)
  /lessons/:
    permalink: /courses/{primary_tag}/{slug}/
    template: index
    filter: tag:hash-lesson

  # ── Training MODULES — /training/{module}/ ───────────────────────────────
  # A module is a POST tagged #training-module whose PRIMARY tag is the module
  # tag. Its body is the module overview.
  #
  # THE ONE RULE: the module post's SLUG must equal its primary TAG's slug.
  # The permalink uses {slug} (unique per post) rather than {primary_tag},
  # because the module post and every one of its lessons share that tag —
  # {primary_tag} would be ambiguous and Ghost would 301 to the wrong place.
  # Keeping slug == tag slug is what makes /training/start/ (the module) and
  # /training/start/{lesson}/ (its lessons) line up. Same trick as /courses/.
  #
  # This replaces the old hand-maintained route-per-module list: modules are
  # now discovered from content, and their ORDER is published_at asc.
  /training-modules/:
    permalink: /training/{slug}/
    template: training-module
    filter: tag:hash-training-module

  # Training LESSONS nest under their module: /training/{module}/{lesson}/
  # A lesson's primary tag IS its module tag, so {primary_tag} nests it
  # automatically. Different path depth from the module above, so no clash.
  /training-lessons/:
    permalink: /training/{primary_tag}/{slug}/
    template: index
    filter: tag:hash-training-lesson

  # ── Docs — the SAME two-level shape as training, and that is the point ────
  # Docs sections used to be ten hand-written routes with `data: tag.x`, each
  # needing a routes.yaml edit AND a partial edit to add one. Nobody ever added
  # an eleventh. Giving each section a backing POST tagged #docs-section makes
  # it Ghost-Admin-only work, and gives the section a real overview page that
  # `data: tag.x` could never have. See the root abstract's 05-content/tag-registry.md.
  /docs-sections/:
    permalink: /docs/{slug}/
    template: docs-section
    filter: tag:hash-docs-section

  /docs-pages/:
    permalink: /docs/{primary_tag}/{slug}/
    template: index
    filter: tag:hash-docs-page

  /resources/:
    permalink: /resources/{slug}/
    template: resources
    filter: tag:hash-resource

  # Things for sale. Ghost takes no one-time payment — see the root abstract's 05-content/tag-registry.md and 06-growth/subscriptions-and-growth.md.
  /toolkit/:
    permalink: /toolkit/{slug}/
    template: toolkit
    filter: tag:hash-product

  /blog/:
    permalink: /blog/{slug}/
    template: blog
    filter: tag:hash-blog

  # Catch-all so untagged posts still get a URL.
  /archive/:
    permalink: /archive/{slug}/
    template: index

taxonomies:
  tag: /tag/{slug}/
  author: /author/{slug}/
```

---

# Collections, mechanically

*Merged from what was `07-collections.md`. What each collection IS gets
decided in [`collections.md`](collections.md); this is how the machinery works.*

Ghost's `collections` in `routes.yaml` are the most under-used feature in the
platform, and on a learning site they are the difference between "a blog with
categories" and "a curriculum".

Read `01` first — this builds on the URL model — and
the root abstract's `05-content/tag-registry.md` for the tag *names*, which are
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
share that tag — and Ghost will 301 to the wrong one. See the URL rules above.

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
the same shape as training (the tag registry,
the root knowledge base's tag registry). Apply the rule to every
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
