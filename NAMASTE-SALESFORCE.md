# Namaste Salesforce — the theme

A Ghost theme for a Salesforce learning platform, built from the foundation
up on the NS Design System: the Salesforce Lightning blue ramp, the navy
gray ramp, Figtree. No Tailwind, no framework — layered CSS, Handlebars
first, and three small scripts for the jobs Handlebars genuinely cannot do.

Live model: **courses** with a lesson player, **training** modules discovered
from tags, and a **blog** whose every post can choose its own layout.

---

## The one idea

**A post is a post.** A course, a lesson, a training page and an article are
all Ghost posts. One internal tag decides everything at once:

| Tag | What the post becomes | URL |
| --- | --- | --- |
| `#course-col` | a course landing page | `/courses/{slug}/` |
| `#lesson-col` | a lesson in the player | `/courses/{course}/{slug}/` |
| `#training-col` | a page in a training module | `/training/{module}/{slug}/` |
| `#blog-col` | an article | `/blog/{slug}/` |
| `#video-col` | a library video (the embed is the page) | `/videos/{slug}/` |
| `#newsletter-col` | a newsletter issue | `/newsletter/{slug}/` |
| `#changelog-col` (or `#feed-col`) | a changelog entry | `/changelog/{slug}/` |
| *(none of these)* | a standalone post | `/{slug}/` |

The bright vocabulary already on imported content is accepted everywhere:
`#courses-col`, `#lessons-col`, `#docs-col`.

`routes.yaml` claims the URL, `post.hbs` dispatches the layout, and the same
tags drive every query. `post.hbs` renders no markup of its own — it reads
the tag out of `{{post_class}}` and hands off to `partials/post-course`,
`post-lesson`, `post-training` or `post-blog`.

### Courses ⇄ lessons: one equality

A course's **slug equals its public tag's slug**, and every lesson's
**primary tag is that tag**. That single equality nests lesson URLs, finds
the course from a lesson, lists the curriculum, and keeps
`{{prev_post}}/{{next_post}} in="primary_tag"` walking inside the course —
all pure Handlebars. Visiting `/tag/{course-slug}/` meta-refreshes to the
course page (tag.hbs).

### Training: the module IS the tag, and the rail shows them all

The reader's sidebar lists EVERY module as a native `<details>` group —
only the module that owns the current page starts open, so any other
section is one click away without leaving the page. On screens ≥1280px the
article grows a second column: the page's own table of contents
(`data-toc`, filled by toc.js).

There is no parent post. A module is a **public tag**: its name and
description come from the tag, its pages are the `#training-col` posts
carrying it as **primary tag**, ordered oldest-first.
`partials/module-grid.hbs` discovers modules by walking public tags and
keeping only those with training posts — publish a post with a new primary
tag and a module card appears; retire the last one and it goes.

### Facet tags (chip/filter vocabulary)

The chip text is always the tag's **description** — templates never parse
slugs into words.

| Prefix | Where it shows |
| --- | --- |
| `#course-level-*` | level chip on cards + course hero, /courses filter |
| `#course-duration-*` | duration chip, /courses filter |
| `#lesson-duration-*` | chip in curriculum + player |
| `#lesson-type-video/-quiz/-audio` | player icon + chip (default: article) |

### Course & lesson per-post layouts

Same convention as the blog: an internal tag stamps a class on the
shell; only the hero/header restyles, the body never changes.

| Tag | Effect |
| --- | --- |
| `#course-layout-cinema` | dark full-bleed hero, image as backdrop |
| `#course-layout-minimal` | centered type, no image |
| `#course-layout-billboard` | wide image banner on top |
| `#course-layout-boxed` | hero framed in a floating card |
| *(none)* | classic — text left, image right |
| `#course-curriculum-cards` | curriculum as a two-column tile grid |
| `#course-curriculum-timeline` | curriculum as a vertical timeline |
| `#course-curriculum-compact` | dense curriculum rows, no excerpts |
| `#course-curriculum-checklist` | check-marked curriculum rows |
| *(none)* | classic — numbered rows |
| `#lesson-layout-right` | curriculum rail on the right |
| `#lesson-layout-focus` | no rail — collapsible contents, centered article |
| `#lesson-layout-cinema` | dark hero card on the lesson header |
| `#lesson-layout-wide` | narrow rail, article grows to the wide measure |
| *(none)* | classic — rail left, measured article |

Static pages take two options the same way (pages carry tags too):
`#page-hero-cover` (feature image becomes a full-width cover behind the
title) and `#page-sidebar` (widget rail right; the TOC moves into it).

`/style-guide/` is a page exercising every Koenig card the editor can
produce — all of them themed in `1-base/_content.css`. When a card
renders oddly, fix the theme, never the content.

### Blog per-post options

| Tag | Effect |
| --- | --- |
| `#blog-layout-magazine` | full-bleed image hero, overlaid title |
| `#blog-layout-minimal` | centered type, no feature image |
| `#blog-layout-split` | text left, image right |
| `#blog-layout-wide` | image breaks out of the column |
| *(none)* | classic |
| `#blog-sidebar-left` / `#blog-sidebar-none` | sidebar position (default right) |
| `#blog-toc-hide` | drop the table of contents |

Layouts restyle only the header, so any layout composes with any sidebar.
Sidebar widgets live in `partials/widgets/` (toc, author, recent-posts,
newsletter, share); `partials/blog-sidebar.hbs` sets the order.

---

### The training reader (v5 — current)

Outer split: content region left, **training navigation right** as a
full-height sticky rail (every module a `<details>`, only the active one
open, per-page type icons). Inside the left region: a full-width hero on
the canvas grid (thumbnail; `#lesson-type-video` flips it to the dark
cinematic variant), then small sticky sidebar (TOC, sponsor skyscraper,
share) + fluid content. Below 1280px the rail folds into a `<details>`
above the content.

### Videos, newsletter, guestbook, welcome

- Video singles are wide two-column; a timestamp table in the post
  becomes the seeking **chapters** sidebar (video.js); cards show only
  thumb + play + duration.
- **`#video-preview`** (any post with a video first): the card plays the
  post's video as a muted autoplaying loop over its thumbnail — the
  content rides into the card in a `<template>`
  (partials/video-preview.hbs) and video-preview.js rewrites the first
  YouTube/Vimeo/video embed into background mode. Ported from the
  aspect theme's featured-video-preview.
- `/newsletter/` frames the latest issue as a mac-window email; issues
  get a sent-date rail + subscribe CTA (post-issue.hbs).
- `/guestbook/` (page-guestbook.hbs): sticky pitch left, Ghost comments
  right — comments are the entries. Requires commenting enabled.
- `/welcome/` (page-welcome.hbs) is every tier's welcome_page_url —
  members land there after signup with three live first-step cards.
- `/signin/`, `/signup/`, `/membership/` wrap Portal; tiers render live.

### The training reader (v3 — superseded)

Three fluid columns: a small widget rail (sponsor skyscraper + share) on
the left, the article — full width, TOC inline after the hero — in the
middle, and the module navigation on the right: every module a native
`<details>`, only the active one open, lesson-type icons per page. Below
1280px the widget rail goes; below 1024px the module nav collapses into a
`<details>` above the content.

### Sponsorship, sitemap, socials

`partials/widgets/sponsor.hbs` renders the sponsor card (skyscraper=true
for the tall slot); every instance routes to the `/sponsor` Ghost page —
edit the pitch there. `/sitemap/` is the visual sitemap, queried live.
Footer socials: Ghost's own facebook/twitter settings plus the
`social_youtube/linkedin/github/instagram` custom settings.

### Thumbnails

`dummy-content/build-thumbnails.py` draws a branded SVG per post (navy
gradient, grid, collection icon, wrapped title) into
`assets/images/thumbs/` and repoints feature_image at it — stored with
Ghost's `__GHOST_URL__` token, because a bare relative path gets nulled
by Ghost's URL-normalisation job (learned live). Cards without any image
fall back to `partials/thumb-placeholder.hbs`.

Figtree is self-hosted (`assets/fonts/`, declared in
`0-abstracts/_fonts.css`) — no Google Fonts request.

## CSS architecture

`assets/css/screen.css` is a manifest; each folder is a cascade layer:

```
0-abstracts/   design tokens only — NSDS ramps + semantic tokens, dark mode
1-base/        reset, typography, the article body (.gh-content)
2-layout/      containers, header (CSS-only drawer), footer
3-components/  buttons, chips, cards, forms, widgets, toc, filters, pagination
4-templates/   one file per template's own layout
5-utilities/   background patterns, helpers
```

Rules: components paint only with semantic tokens (`--bg`, `--text`,
`--accent`…); raw ramp values appear only in `0-abstracts`. Dark mode is the
same tokens redefined — `html[data-theme="dark"]` plus a `prefers-color-scheme`
copy for the no-choice state. `pnpm build` compiles.

## Handlebars-first inventory

- **Navbar** — `partials/navigation.hbs`, rendered by `{{navigation}}` (the
  helper supplies each item's computed `slug` and `current`). Icons resolve
  dynamically: `icons/nav-{slug}` (`nav-home`, `nav-courses`…); items without
  a matching partial render as text. Mobile drawer is the `#nav-open`
  checkbox + label — zero JS.

  **Dropdowns are a label convention** in Admin → Settings → Navigation:
  `+Learn` opens a dropdown (shown as "Learn"), the `-Courses` / `-Training`
  run after it are its children, and the first unprefixed label ends the run.
  The dropdown itself is pure CSS (`:hover` / `:focus-within`); in the mobile
  drawer children render inline, indented. A parent whose child is current
  reads as current.
- **Icons** — `partials/icons/*.hbs`, one drawing style (24-box, 1.8 stroke,
  currentColor). Add an icon by adding a file.
- **JSON-LD** — `partials/json-ld.hbs` (WebSite + Organization +
  SiteNavigationElement from live navigation) on every page; `Course` on
  course pages; `BreadcrumbList` on lessons and training pages.
- **/llms/** — theme-curated machine-readable site map in Markdown, built
  from live queries (nav, courses with lessons, modules, writing, pages).
  Ghost 6's native handler owns `/llms.txt` itself (`llms_enabled` is on).
- **prev/next** — `{{prev_post in="primary_tag"}}`, no script.

The three scripts (`assets/js/`): `theme.js` (toggle + storage; the inline
head script in default.hbs applies it pre-paint), `toc.js` (heading ids,
outline, scroll-spy; removes itself without headings), `filters.js` (the
/courses toolbar — built from the cards' data attributes, because
`{{#get "tags"}}` is served by Ghost's TagPublic model and can never see
internal tags).

## Custom settings

`dark_logo` (image for dark mode; without one the logo is auto-inverted to
white), `footer_tagline`, `newsletter_heading`, `newsletter_text`.

## Gotchas learned the hard way

- `{{#get}}` switches context to the API response: values carried in via
  `partials/with-this.hbs` need `../` inside the get, `../../` inside a
  nested foreach. Filter strings are the exception — they compile in the
  CALLING frame.
- `{{#if emptyArray}}` is truthy. Gate on `{{#if items}}` only after a
  foreach proves something rendered, or check a known-scalar.
- Helpers shadow properties: on navigation items `{{url}}` is the URL
  *helper* (site root). `{{this.url}}` reads the property.
- `updated_at` is not a helper — `{{date updated_at format="…"}}`.

## Files

```
routes.yaml            the URL model — mirror to content/settings/ + restart
home.hbs               the designed homepage (data: page.home)
courses.hbs / training.hbs / blog.hbs / llms.hbs
post.hbs               the dispatcher
index.hbs              catch-all archive (mounted at /archive/)
partials/              header, footer, navigation, json-ld, cards, player,
                       module-grid, blog single + widgets/, icons/
```

## Dummy content

`dummy-content/import.json` is a Ghost import (Admin → Settings →
Import/Export) that exercises everything: a course with all four lesson
types, two training modules, one blog post per layout, every facet tag WITH
its chip description, and the navigation settings including the dropdown
convention. Regenerate it with `python3 dummy-content/build-import.py` —
internal tag slugs get Ghost's `hash-` prefix automatically (an internal tag
whose slug lacks it is invisible to `post_class` matching; learned the hard
way).

`pnpm build` after touching assets; `pnpm test` runs gscan.
