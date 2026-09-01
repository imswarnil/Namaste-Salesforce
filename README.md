# Namaste Salesforce — Ghost theme

The theme behind [Namaste Salesforce](https://namastesalesforce.com): a
Salesforce learning platform built on Ghost — structured courses with a
lesson player, tag-driven training modules, a video library with chapter
navigation, a five-layout blog, newsletter, changelog and membership.
Designed on the NS Design System (Salesforce Lightning blue, navy grays,
Figtree — self-hosted).

## Quick start

```bash
pnpm install --frozen-lockfile
pnpm build      # compile CSS/JS into assets/built/
pnpm test       # gscan
```

Upload `routes.yaml` in Ghost Admin → Settings → Labs → Routes.
`dummy-content/import.json` seeds a complete demo site (Settings →
Import), then `python3 dummy-content/build-thumbnails.py` draws branded
SVG thumbnails for every post.

## How it works

**A post is a post.** One internal tag decides everything — its URL, its
layout, its queries: `#course-col`, `#lesson-col`, `#training-col`,
`#video-col`, `#blog-col`, `#newsletter-col`, `#changelog-col`. A course's
slug equals its public tag's slug; every lesson's primary tag is that tag.
A training module *is* a public tag.

Read `NAMASTE-SALESFORCE.md` for the full architecture — URL model, the
duration-tag ramp, video chapters, the sidebar/TOC rule, and the
Handlebars traps already hit once so you don't hit them twice.

## Deploy

Pushes to `main` deploy automatically to Ghost via
`TryGhost/action-deploy-theme` (`GHOST_ADMIN_API_URL` /
`GHOST_ADMIN_API_KEY` repo secrets).
