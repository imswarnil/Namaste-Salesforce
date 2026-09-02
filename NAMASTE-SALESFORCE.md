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

There is no parent post. A module is a **public tag**: its name,
description and image come from the tag, its pages are the `#training-col`
posts carrying it as **primary tag**, ordered oldest-first.
`partials/module-grid.hbs` discovers modules by walking public tags and
keeping only those with training posts — publish a post with a new primary
tag and a module card appears; retire the last one and it goes.

`/training/` is the **trail** (`partials/training-trail.hbs`): a
two-column hero (pitch + live "up next" panel) over `.training-layout` —
the trail left, a sticky widget sidebar right. On the trail, modules AND
their sections hang off ONE rail: a numbered waypoint per module (CSS
counter in `.trail-node`, tag image as the module badge), each section a
timeline stop with its lesson-type icon and duration chip, then the next
module. The rail itself is an SVG line (`.trail-line`) whose accent path
draws down with scroll (`data-draw`, animate.js); waypoints light as
they reveal (`.is-in`). The homepage repeats the sequence as
**`partials/training-path.hbs`** — compact numbered steps on a
horizontal scroll-snap track (`.home-path`), closing with a terminus
step to /training.

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
- `/newsletter/` frames the latest issue as a mac-window email; below,
  issues (thumbnails + sent dates) beside a sticky sidebar whose **sent
  calendar** (widgets/sent-calendar.hbs + calendar.js) renders the
  current month, marks every day an issue went out, tooltips the title
  on hover (CSS `attr(data-tip)`) and walks months back to the first
  issue. Issue singles keep the sent-date rail + subscribe CTA
  (post-issue.hbs).
- **Changelog types**: `#changelog-type-feature/-improvement/-fix/
  -content` — the badge text is the tag DESCRIPTION, the slug suffix
  picks colour + icon (partials/changelog-badge.hbs); renders on the
  /changelog timeline/board and the entry header.
- `/sponsor/` (page-sponsor.hbs) and `/contact/` (page-contact.hbs) are
  homepage-grade: hero + live-counted stats/prop cards/social row, with
  the page's own content still rendered in a section.
- `/sitemap/` is a TREE: root node, trunk, one branch per collection
  (its icon on the head), every entry a leaf on dashed connectors —
  pure CSS, queried live. `/guestbook/` locks to the viewport ≥901px:
  the pitch stays put, only the comments column scrolls.
- `/changelog/` has two CSS-only views: two radio inputs before
  `.changelog-layout` restyle the SAME entry markup as a timeline
  (default) or a kanban-style board — the toolbar labels are the switch,
  zero JS. Entries carry their feature image (placeholder fallback) and
  their primary tag as a chip with the TAG's image as icon; a sticky
  sidebar (subscribe, RSS, sponsor) rides right and folds under on
  mobile. Changelog singles use post-simple.hbs `withSidebar=true`: the
  entry reader — sticky sidebar left (TOC, share, sponsor), sectioned
  article right (each h2 opens a bordered section). On small screens the
  sidebar folds above the content, TOC first, share/sponsor hidden.
  Newsletter issues keep the narrow variant with the inline TOC.
- Post cards always carry media (feature image or the branded thumb
  placeholder), and the eyebrow shows the primary tag with the tag's
  feature image as a round icon (`.card-tag-icon`, tag glyph fallback).
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

The same script draws a **badge per PUBLIC tag** (monogram tile) into
`assets/images/tags/{slug}.svg` and repoints the tag's feature_image;
build-import.py stamps the same URLs into import.json. Templates use
the tag image as the tag's icon everywhere — card eyebrows
(`.card-tag-icon`), module badges on the trail and home path, the
training reader rail (`.rail-module-ico`), sitemap topic leaves — each
with a glyph fallback when a tag has no image. The lesson player rail
heads with the course's own thumb the same way.

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

  The bar is **full-bleed** — `.site-head-inner` has its own padding, no
  `.inner` max-width. The mobile drawer blooms open from the burger's
  corner (a `clip-path: circle()` reveal, disabled under reduced
  motion) with the items cascading in on staggered delays.

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

The scripts (`assets/js/`, all concatenated into built/main.js) also
include `calendar.js` (the newsletter sent calendar — reads the hidden
issue list the widget renders, builds the month grid with Intl names,
removes itself without data) alongside `theme.js` (toggle + storage; the inline
head script in default.hbs applies it pre-paint), `toc.js` (heading ids,
outline, scroll-spy; removes itself without headings), `filters.js` (the
/courses toolbar — built from the cards' data attributes, because
`{{#get "tags"}}` is served by Ghost's TagPublic model and can never see
internal tags).

## Custom settings

`hero_style` (select — the homepage hero: **Showcase split** (default,
copy + featured-course card), **Centered**, **Cinematic dark** (navy
band, literal colours), **Illustrated** (copy + the platform drawn as
inline SVG — partials/illustrations/hero-platform.hbs, riding CSS vars
so it follows dark mode), **Product window** (the LMS mocked in a
browser frame, filled with the featured course's real curriculum).
Every style shares partials/hero-copy.hbs + hero-stats.hbs; home.hbs
dispatches on the setting), `dark_logo` (image for dark mode; without
one the logo is auto-inverted to white), `footer_tagline`,
`newsletter_heading`, `newsletter_text`.

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
