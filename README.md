<div align="center">

# Namaste Salesforce

**An open-source [Ghost](https://ghost.org) theme for Salesforce learning communities.**

Courses with nested lessons · structured training paths · documentation · a blog.

**Currently a stack-free starter** — five templates, two partials, ~30 lines of CSS,
no build step. The architecture and the decisions still open are in [`abstract/`](abstract/).

[![CI](https://github.com/imswarnil/Namaste-Salesforce/actions/workflows/ci.yml/badge.svg)](https://github.com/imswarnil/Namaste-Salesforce/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ghost](https://img.shields.io/badge/Ghost-%3E%3D5.0-738a94)](https://ghost.org)

</div>

> **Status: `0.1.0` — a starter, being rebuilt.** The previous implementation was
> deliberately reset; no build tool, CSS framework or component library has been
> chosen yet. See [`abstract/15`](abstract/15-starting-from-zero.md) for what was
> removed and the decisions still open, and [CHANGELOG.md](CHANGELOG.md).

---

## What makes it different from a blog theme

Ghost is a publishing platform, not an LMS. This theme is the set of
conventions that make it behave like one **without giving up what Ghost is good
at** — being fast, indexable and editable by a writer.

- **Courses with nested lessons.** `/courses/apex/` and
  `/courses/apex/triggers/` — a lesson nests under its course automatically,
  because its primary tag *is* the course's tag.
- **Structured training.** A sequence of sections, each with its own lessons,
  a reading rail and prev/next that crosses section boundaries.
- **One dispatcher, seven page types.** Ghost gives a theme one `post.hbs`;
  this one reads tags and dispatches to a real page per kind of content.
- **Adding a training section is Ghost-Admin-only.** Make the tag, write the
  post, publish. No route edit, no theme edit, no deploy.

These are the conventions the theme is being rebuilt to serve; the starter
implements the URL model and the dispatcher shape, not yet the pages.

## Install

1. Download `namaste-salesforce.zip` from the
   [latest release](https://github.com/imswarnil/Namaste-Salesforce/releases).
2. Ghost Admin → **Design → Change theme → Upload a theme**.
3. Ghost Admin → **Settings → Labs → Routes** → upload
   [`routes.yaml`](routes.yaml).

> ⚠️ **Step 3 is not optional.** `routes.yaml` defines every collection and URL
> on the site. Without it the collections do not exist and posts import with no
> URLs. Note that the shipped file is deliberately minimal — a route pointing at
> a template that does not exist is a **400**, not a fallback — so entries are
> added back as their templates land. The full model is in
> [`abstract/01`](abstract/01-content-model.md).

To see it with content, you need a seed fixture —
[`abstract/14`](abstract/14-seed-content.md) is how to build one, and why the
`sort_order: 0` rule in it is what makes the whole URL model work.

## The content model in one table

Everything is a Ghost post. What it *is* comes from its tags.

| Kind | Tag | Primary tag | URL |
| --- | --- | --- | --- |
| Course | `#course` | its own course tag | `/courses/{slug}/` |
| Course lesson | `#lesson` | its **course's** tag | `/courses/{course}/{slug}/` |
| Training section | `#training-section` | its own section tag | `/training/{slug}/` |
| Training lesson | `#training-content` | its **section's** tag | `/training/{section}/{slug}/` |
| Doc | `documentation` | its docs section tag | `/docs/{section}/{slug}/` |
| Resource | `#resource` | — | `/resources/{slug}/` |
| Blog post | `#blog` | — | `/blog/{slug}/` |

**The one rule:** a course post's slug must equal its course tag's slug (and
the same for sections). Full reasoning in
[`abstract/01-content-model.md`](abstract/01-content-model.md) — it is the only
part of this theme that is expensive to get wrong.

## Develop

```bash
npm install
npm test          # gscan — Ghost's own theme validator
npm run zip       # package for upload
```

There is no build step. `assets/css/screen.css` is served directly.

## Documentation

[`abstract/`](abstract/) is the documentation, ordered by **what breaks the
site if you get it wrong** rather than by what is interesting.

| | |
| --- | --- |
| [01 content model](abstract/01-content-model.md) | `routes.yaml`, tags, the URL rules |
| [02 post dispatcher](abstract/02-post-dispatcher.md) | one `post.hbs`, seven page types |
| [03 design system](abstract/03-design-system.md) | NSDS, vendoring, what the theme may not own |
| [04](abstract/04-build-pipeline.md) · [05](abstract/05-css-architecture.md) | build pipeline · CSS architecture (**both describe the removed stack — reference, not current**) |
| [06 Ghost glue](abstract/06-ghost-glue.md) | members, Koenig, JSON-LD, helper traps |
| [07 performance](abstract/07-performance.md) | fonts, images, the pre-paint script |
| [10 postmortem](abstract/10-how-this-went-wrong.md) | the mistakes already made here |
| [11 roadmap](abstract/11-theme-roadmap.md) | what to build next, ranked |
| [12 content system](abstract/12-content-system.md) | one concept → lesson, video, blog, slides, social |
| [13 collections](abstract/13-collections.md) | Ghost collections and the learning graph |
| [17 design system](abstract/17-consuming-the-design-system.md) | what NSDS is, measured — and why Tailwind is optional |
| [decisions/](abstract/decisions/) | the decision record, with reasoning and downsides |
| [14 seed content](abstract/14-seed-content.md) | how to rebuild the fixture you need before anything renders |
| [15 starting from zero](abstract/15-starting-from-zero.md) | what was removed, and the decisions still open |
| [16 how to Claude](abstract/16-how-to-claude.md) | working effectively with Claude Code |

## Contributing

Contributions welcome at any size — see [CONTRIBUTING.md](CONTRIBUTING.md).

The first question is always **which repo**: how a component *looks* belongs to
[NS-Design-System](https://github.com/imswarnil/NS-Design-System); which Ghost
data appears and where belongs here.

## Licence

[MIT](LICENSE). Originally forked from [Casper](https://github.com/TryGhost/Casper),
Ghost's default theme, whose copyright is retained alongside this project's.
