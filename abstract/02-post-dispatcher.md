# 02 · `post.hbs` is a dispatcher, not a template

Ghost gives you **exactly one** `post.hbs` for every post on the site. This
site has seven kinds of post and they are genuinely different *pages* — a
lesson is a reading player, a course is a sales page, a doc is a reference.

So `post.hbs` renders nothing itself. It reads tags and dispatches:

```hbs
{{!< default}}
{{#post}}
  {{#has tag="documentation"}}          {{> "post-documentation"}}
  {{else has tag="#training-section"}}  {{> "post-training-section"}}
  {{else has tag="#training-content"}}  {{> "post-training"}}
  {{else has tag="#course"}}            {{> "post-course"}}
  {{else has tag="#lesson"}}            {{> "post-lesson"}}
  {{else has tag="#resource"}}          {{> "post-resource"}}
  {{else has tag="#blog"}}              {{> "post-blog"}}
  {{else}}                              {{> "post-default"}}
  {{/has}}
{{/post}}
```

## ⚠️ BRANCH ORDER IS LOAD-BEARING

`#training-section` is tested **before** `#training-content`. A section
overview is not a lesson, and matching the lesson branch would render it
inside the lesson player.

A new branch goes where its **specificity** demands, not at the end. Ask: is
there any post that carries both this tag and a tag already in the list? If
so, the more specific one goes first.

## The fallback is not optional

A post with none of these tags still has to render. `post-default` exists for
that, and it is deliberately the *same reading surface a blog post gets* — an
untyped post is still a post, and giving it a lesser layout is how a page ends
up looking broken rather than plain.

## `default.hbs` dispatches too, on the same tags

The chrome swaps, so a reading surface does not get a marketing bar:

| | reading post | everything else |
| --- | --- | --- |
| header | `components/course-player-header` | `partials/header` |
| footer | `partials/footer-lesson` | `partials/footer` |

Reading posts are `#lesson, #training, #training-content, #training-section`.

Per-page scripts are gated the same way — only a course page loads `tabs.js`,
only a training page loads `training.js`.

## Art direction is an internal tag, resolved in ONE partial

A course hero and a blog header each have several versions. Which one a post
gets is an internal tag, and the `{{#has}}` chain that maps tag → class lives
in exactly one partial per surface, because each is needed in three places on
its page (the element, the background layer, the media slot) and copied three
times it will drift.

- `partials/courses/hero-variant.hbs` → `.ns-chero--*`
- `partials/blog/head-variant.hbs` → `.ns-posthead--*`

Keep numeric aliases (`#hero-1`…`#hero-5`) working when you rename to semantic
tags. Ghost content is not in this repo, so a hard cutover silently drops every
already-published post back to the default.

## Metadata rides on internal tags, in the tag's DESCRIPTION

The convention: the tag's **description** field carries the text, so an author
writes it in Ghost Admin without touching the theme.

```
#duration-6h20m   description = "6h 20m"
#learn-triggers   description = "Write a trigger that survives 200 records"
#prereq-apex      description = "You can read a class and a method"
#cert-pd1         description = "Platform Developer I"
```

Read with:

```hbs
{{#foreach tags visibility="internal"}}
  {{#match slug "~^" "hash-duration-"}}{{description}}{{/match}}
{{/foreach}}
```

Other structural internal tags: `#level-*`, `#free` / `#paid`, `#preview`,
`#hide-image`, `#lesson-type-video|quiz|lab`, `#training-video|exercise|quiz`.
