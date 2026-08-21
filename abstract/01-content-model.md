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
| Training section | `#training-section` | its own section tag | `/training/{slug}/` |
| Training lesson | `#training-content` | its **section's** tag | `/training/{section}/{slug}/` |
| Doc | `documentation` | its docs section tag | `/docs/{section}/{slug}/` |
| Resource | `#resource` | — | `/resources/{slug}/` |
| Blog post | `#blog` | — | `/blog/{slug}/` |
| anything else | — | — | `/archive/{slug}/` |

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

Make the tag → write a post tagged `#training-section` with a matching slug →
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

## Docs sections are routed one-by-one, and that is deliberate

Ten `/docs/{section}/` routes with `data: tag.{slug}`. Unlike training, a docs
section is a TAG with no backing post, so there is nothing for a collection to
discover. Adding one means a `routes.yaml` entry AND an entry in
`partials/docs/sections.hbs`. Keep them in sync.

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
#   Section      = POST tagged #training-section, PRIMARY tag = the section tag,
#                  and post slug == that tag's slug (e.g. slug "start", primary
#                  tag "start"). The post BODY is the section overview.
#                  → /training/start/
#   Lesson       = post tagged #training-content, PRIMARY tag = its section tag.
#                  → /training/start/{lesson-slug}/
#   Section ORDER = published_at asc. Backdate a section post to move it earlier.
#
#   Adding a section is therefore Ghost-Admin-only: make the tag, write the
#   section post with a matching slug, publish. No routes.yaml edit, no theme
#   edit. (This replaced a hardcoded route-per-section list plus an ordered
#   partial that both had to be kept in sync by hand.)
#   Doc          = post tagged `documentation`, primary tag = docs-NN-* section tag
#   Resource     = post tagged #resource
#   Blog post    = post tagged #blog
#   Pages: /about/, /products/, /contact/ use page-{slug}.hbs automatically.
#
# TAG pages redirect in tag.hbs rather than serving a duplicate archive:
#   /tag/{course-tag}/   -> the course
#   /tag/{section-tag}/  -> /training/{section}/  (detected by the #training-section
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
  # (tagged #training-section) and is served by the /training-sections/
  # collection below, so adding a section is pure Ghost Admin work — no route
  # edit, no theme edit. See the collection for the slug rule.

  # Docs section pages — /docs/{section}/ (clean slugs, no numbering).
  # Each renders docs-section.hbs with its tag as {{tag}}. Section tag slugs
  # in Ghost Admin must match (rename docs-01-getting-started → getting-started
  # etc.). Keep this list in sync with partials/docs/sections.hbs.
  /docs/getting-started/:
    data: tag.getting-started
    template: docs-section
  /docs/account-profile/:
    data: tag.account-profile
    template: docs-section
  /docs/courses-lessons/:
    data: tag.courses-lessons
    template: docs-section
  /docs/roadmaps/:
    data: tag.roadmaps
    template: docs-section
  /docs/membership-billing/:
    data: tag.membership-billing
    template: docs-section
  /docs/certificates-progress/:
    data: tag.certificates-progress
    template: docs-section
  /docs/become-an-author/:
    data: tag.become-an-author
    template: docs-section
  /docs/community-support/:
    data: tag.community-support
    template: docs-section
  /docs/troubleshooting/:
    data: tag.troubleshooting
    template: docs-section
  /docs/design-system/:
    data: tag.design-system
    template: docs-section

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

  # ── Training SECTIONS — /training/{section}/ ─────────────────────────────
  # A section is a POST tagged #training-section whose PRIMARY tag is the
  # section tag. Its body is the section overview.
  #
  # THE ONE RULE: the section post's SLUG must equal its primary TAG's slug.
  # The permalink uses {slug} (unique per post) rather than {primary_tag},
  # because the section post and every one of its lessons share that tag —
  # {primary_tag} would be ambiguous and Ghost would 301 to the wrong place.
  # Keeping slug == tag slug is what makes /training/start/ (the section) and
  # /training/start/{lesson}/ (its lessons) line up. Same trick as /courses/.
  #
  # This replaces the old hand-maintained route-per-section list: sections are
  # now discovered from content, and their ORDER is published_at asc.
  /training-sections/:
    permalink: /training/{slug}/
    template: training-section
    filter: tag:hash-training-section

  # Training LESSONS nest under their section: /training/{section}/{lesson}/
  # A lesson's primary tag IS its section tag, so {primary_tag} nests it
  # automatically. Different path depth from the section above, so no clash.
  /training-lessons/:
    permalink: /training/{primary_tag}/{slug}/
    template: index
    filter: tag:hash-training-content

  # Docs hub + section-nested articles: /docs/{section-tag}/{doc-slug}/
  # (doc primary tag = its docs-NN-* section tag).
  /docs/:
    permalink: /docs/{primary_tag}/{slug}/
    template: documentation
    filter: tag:documentation

  /resources/:
    permalink: /resources/{slug}/
    template: resources
    filter: tag:hash-resource

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
