# `prompt/` — content-generation prompts for Namaste Salesforce

Ready-to-paste prompts for producing publishable content for this Ghost site.
One file per content type. Every prompt is written against the **actual**
templates, tag model and `routes.yaml` in this repo, not against a generic idea
of a blog — so content produced from them drops into Ghost Admin and renders
correctly the first time.

## How to use

Paste **two** files into the model, in this order:

1. `00-house-style.md` — the shared contract: voice, markup rules, the code
   languages the highlighter knows, the icon safelist, and the mistakes that
   silently break a page. Every type prompt assumes it.
2. the type prompt you want, from the table below.

Then add your brief ("a course on Apex triggers for admins moving into code").

If you can only paste one file, paste the type prompt — each one repeats the
handful of rules that would break *that* type.

**For anything that is not one of the seven content types** — a question about
the site, a change to the theme, an image to generate, a model that needs to
know what it is looking at — paste [`SITE-CONTEXT.md`](SITE-CONTEXT.md)
instead. It is the full briefing: the product, the two domains, the routing
model, the build, the design system, the palette, the image rules, and the list
of things that fail silently. It also supersedes the old `prompt.md` and
`prompt-banner.md`, which were image-only and are gone.

## Two websites, one brand

Before writing anything, be sure which surface it is for:

- **www.namastesalesforce.com** — this Ghost site. Public, indexable, free to
  read: marketing, blog, docs, the free training track, the course catalog.
- **app.namastesalesforce.com** — the Next.js LMS. Anything gated, enrolled in,
  tracked or graded: the course player, progress, accounts.

Everything in *this* folder produces content for the Ghost site. Both products
share the same design system, so the writing rules below hold on either — but
the tag model, the routes and the templates described here are Ghost's.

## The prompts

| File | Produces | Lands at |
| --- | --- | --- |
| [`01-course.md`](01-course.md) | a course (`#course`) | `/courses/{course-tag}/` |
| [`02-course-lesson.md`](02-course-lesson.md) | a lesson inside a course (`#lesson`) | `/courses/{course-tag}/{lesson}/` |
| [`03-training-section.md`](03-training-section.md) | a training section (`#training-section`) | `/training/{section}/` |
| [`04-training-lesson.md`](04-training-lesson.md) | a training lesson (`#training-content`) | `/training/{section}/{lesson}/` |
| [`05-blog-post.md`](05-blog-post.md) | a blog article (`#blog`) | `/blog/{slug}/` |
| [`06-resource.md`](06-resource.md) | a library entry (`#resource`) | `/resources/{slug}/` |
| [`07-documentation.md`](07-documentation.md) | a docs article (`documentation`) | `/docs/{section}/{slug}/` |

## The two content models, in one place

Everything in this folder rests on these rules from `routes.yaml`. They are the
part people get wrong.

**Courses** — a course and its lessons *share one public tag*:

```
Course post   slug = "apex"     tags: [Apex, #course, …]        → /courses/apex/
Lesson post   slug = "apex-01-…" tags: [Apex, #lesson, …]       → /courses/apex/apex-01-…/
                                        ↑ primary tag = the course tag
```

The course post's **slug must equal its course tag's slug**. The permalink uses
`{slug}`, and lessons nest by `{primary_tag}` — that is the whole mechanism.

**Training** — one training, many sections, same trick one level down:

```
Section post  slug = "start"     tags: [Start Here, #training-section]  → /training/start/
Lesson post   slug = "start-01-…" tags: [Start Here, #training-content, …] → /training/start/start-01-…/
```

The section post's **slug must equal its section tag's slug**. There is no
`/training/` post — that route is the landing page listing the sections.

**Order is `published_at`, ascending, everywhere.** Lesson order inside a
course, lesson order inside a section, article order inside a docs section, and
the *section numbers* on the training hero are all derived from publish date.
To move something earlier, backdate it. Nothing else controls sequence.

## Adding content vs. changing the theme

Almost everything is Ghost-Admin-only. Two things are not:

- **A new docs section** needs a theme change — the ten sections are registered
  in `partials/docs/sections.hbs`, `partials/docs/next-section-for.hbs` *and*
  `routes.yaml`. See `07-documentation.md`.
- **A Phosphor icon in post body copy** that isn't already shipped renders as a
  blank box. Only the sixteen glyphs in `00-house-style.md` are safe. Anything
  else needs `CONTENT_SAFELIST` in `scripts/subset-icons.py` updated and the
  script re-run.

New courses, lessons, training sections, training lessons, blog posts and
resources need no theme edit and no `routes.yaml` edit.

## Where these came from

The tag vocabulary is the one in `dummy-content/import.json`; the page anatomy
is read from `partials/post-*.hbs`; the content-body behaviours (code windows,
video adoption, timestamp seeking, table-of-contents) are read from
`assets/js/`. The design language is the **NS Design System**, which lives in
its own repository beside the Ghost install and is vendored into this theme at
`assets/css/ds/` — see `NS-Design-System/readme.md` and its
`docs/INTEGRATION.md`.
