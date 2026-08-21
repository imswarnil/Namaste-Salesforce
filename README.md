<div align="center">

# Namaste Salesforce

**An open-source [Ghost](https://ghost.org) theme for Salesforce learning communities.**

Courses with nested lessons · structured training paths · documentation · a blog —
built on a shared design system, with dark mode, self-hosted fonts and no third-party
requests in the render path.

[![CI](https://github.com/imswarnil/Namaste-Salesforce/actions/workflows/ci.yml/badge.svg)](https://github.com/imswarnil/Namaste-Salesforce/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ghost](https://img.shields.io/badge/Ghost-%3E%3D5.0-738a94)](https://ghost.org)

</div>

> **Status: `0.1.0`, rebuilding.** The theme is being rewritten from scratch on
> the Namaste Salesforce Design System. Pre-1.0 means the structure is still
> moving — see [CHANGELOG.md](CHANGELOG.md) and [`abstract/`](abstract/).

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
- **A design system, not a stylesheet.** Every visual decision comes from
  [NS-Design-System](https://github.com/imswarnil/NS-Design-System), vendored
  in and shared with the Next.js LMS, so the two products cannot drift.
- **Adding a training section is Ghost-Admin-only.** Make the tag, write the
  post, publish. No route edit, no theme edit, no deploy.

## Install

1. Download `namaste-salesforce.zip` from the
   [latest release](https://github.com/imswarnil/Namaste-Salesforce/releases).
2. Ghost Admin → **Design → Change theme → Upload a theme**.
3. Ghost Admin → **Settings → Labs → Routes** → upload
   [`routes.yaml`](routes.yaml).

> ⚠️ **Step 3 is not optional.** `routes.yaml` defines every collection and URL
> on the site. Without it, courses, training, docs and the blog have no URLs
> and the theme will look broken through no fault of its own.

To see it with content before writing your own: Ghost Admin → **Settings → Labs
→ Import** [`dummy-content/import.json`](dummy-content/import.json), which
seeds every collection and every tag the templates branch on.

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
yarn install
yarn dev          # build + watch, livereload
yarn build        # one-off build into assets/built/ (committed)
yarn test         # gscan — Ghost's own theme validator
yarn design:sync  # re-vendor the design system
yarn zip          # package for upload
```

`assets/built/` is committed because Ghost serves it directly. Run `yarn build`
and commit the result; CI fails if it is stale.

## Documentation

[`abstract/`](abstract/) is the documentation, ordered by **what breaks the
site if you get it wrong** rather than by what is interesting.

| | |
| --- | --- |
| [01 content model](abstract/01-content-model.md) | `routes.yaml`, tags, the URL rules |
| [02 post dispatcher](abstract/02-post-dispatcher.md) | one `post.hbs`, seven page types |
| [03 design system](abstract/03-design-system.md) | NSDS, vendoring, what the theme may not own |
| [04](abstract/04-build-pipeline.md) · [05](abstract/05-css-architecture.md) | build pipeline · CSS architecture |
| [06 Ghost glue](abstract/06-ghost-glue.md) | members, Koenig, JSON-LD, helper traps |
| [07 performance](abstract/07-performance.md) | fonts, images, the pre-paint script |
| [10 postmortem](abstract/10-how-this-went-wrong.md) | the mistakes already made here |
| [11 roadmap](abstract/11-theme-roadmap.md) | what to build next, ranked |
| [12 content system](abstract/12-content-system.md) | one concept → lesson, video, blog, slides, social |
| [13 collections](abstract/13-collections.md) | Ghost collections and the learning graph |

## Contributing

Contributions welcome at any size — see [CONTRIBUTING.md](CONTRIBUTING.md).

The first question is always **which repo**: how a component *looks* belongs to
[NS-Design-System](https://github.com/imswarnil/NS-Design-System); which Ghost
data appears and where belongs here.

## Licence

[MIT](LICENSE). Originally forked from [Casper](https://github.com/TryGhost/Casper),
Ghost's default theme, whose copyright is retained alongside this project's.
