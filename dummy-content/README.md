# dummy-content/

`import.json` — a **Ghost import file**: 11 posts and 19 tags that exercise
every template and every internal tag this theme reads.

## How to load it

Ghost Admin → **Settings → Labs → Import content** → pick `import.json`.

It is additive. Ghost matches tags by slug, so importing twice does not
duplicate the tags — but it *will* duplicate the posts, because Ghost appends a
suffix to a clashing slug rather than replacing. Delete the previous set first
if you re-import.

> `routes.yaml` is **not** part of this. It is uploaded separately in
> **Settings → Labs → Routes**, and without it `/training/…` will not resolve —
> the module and lesson URLs come from the collections in that file.

## What is in it, and what each post is for

| Post | Tags | What it demonstrates |
|---|---|---|
| Foundations | `Foundations` `#training-module` | a module page at `/training/foundations/` |
| Standard vs custom objects | `Foundations` `#training-lesson` `#level-beginner` | a lesson, beginner chip |
| Field types… | `Foundations` `#training-lesson` `#level-beginner` | a lesson with a feature image in the stage |
| Lookup vs master-detail | `Foundations` `#training-lesson` `#level-intermediate` | the last lesson — pager has no "next" |
| Security and access | `Security` `#training-module` | the second module, so the rail has two sections |
| Profiles vs permission sets | `Security` `#training-lesson` `#level-beginner` | |
| The role hierarchy | `Security` `#training-lesson` `#level-intermediate` | |
| Org-wide defaults… | `Security` `#training-lesson` `#level-advanced` `#code` | advanced chip + "runnable code" row |
| Why your Flow is slower… | `Apex` `#blog` `#code` `#level-intermediate` `#updated` | blog post **with** the right-hand sidebar |
| A field-naming convention… | `Apex` `#blog` `#hide-sidebar` | blog post **without** it — full width |
| Sharing rules… | `Security` `#blog` `#level-advanced` | a third card so the listing grid fills a row |

## The one rule that will break it if you edit it

**A module post's slug must equal its primary tag's slug.** `Foundations` has
slug `foundations` and primary tag `foundations`; `/training/foundations/` is
the module and `/training/foundations/{lesson}/` are its lessons. Break that
and the module still renders — at a URL its own lessons do not sit under.

A lesson's **primary tag is its module's tag**. That inheritance is what makes
the nesting work; it is not a convention, it is the mechanism.

## The internal tags, and what reads each one

Internal tags start with `#`, are hidden from readers, and never appear at
`/tag/…`. In a **filter string** Ghost writes them `hash-` — `tag:hash-blog`,
never `tag:#blog`, which matches nothing silently.

| Tag | Read by | Effect |
|---|---|---|
| `#training-module` | `routes.yaml`, `training/modules`, `training/nav` | the post is a module |
| `#training-lesson` | `routes.yaml`, `post.hbs` | the post is a lesson; gets the course player |
| `#blog` | reserved for the filtered `/blog/` collection | not yet enforced — see below |
| `#hide-sidebar` | `post/article.hbs` | drops the right-hand column, full-width prose |
| `#code` | `post/sidebar.hbs` | adds the "Includes · Runnable code" row |
| `#updated` | `post/sidebar.hbs` | adds the "Updated" date row |
| `#level-beginner` / `-intermediate` / `-advanced` | `post/sidebar.hbs`, `post/training-lesson.hbs` | the level chip |
| `#lesson`, `#course`, `#docs-section`, `#docs-page`, `#resource`, `#product` | `post.hbs`, `abstract/01-content-model.md` | declared so the vocabulary exists; the templates for these are not built yet |

The last row matters: those six are in the file so the tags exist with the
right slugs and visibility when the collections that use them are added. They
are deliberately **not attached to any post** — an unused tag is free, a post
routed by a collection that has no template is a 404.

> `/blog/` is currently the **unfiltered catch-all**, so every post lands
> there regardless of `#blog`. `abstract/01-content-model.md` specifies
> `filter: tag:hash-blog` with `/archive/` as the catch-all instead. The tag is
> applied to the three blog posts already, so switching the collection over is
> a one-line change in `routes.yaml` with no content edits.
