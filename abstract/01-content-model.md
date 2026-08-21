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
