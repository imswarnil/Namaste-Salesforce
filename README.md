# Namaste Salesforce — Ghost theme

The theme behind [Namaste Salesforce](https://namastesalesforce.com): a
Salesforce learning platform built on Ghost — structured courses with a
lesson player, tag-driven training modules, a video library with chapter
navigation, a five-layout blog, newsletter, changelog and membership.
Designed on the NS Design System (Salesforce Lightning blue, navy grays,
Figtree — self-hosted).

## Why this project exists

**The goal.** Become a GTM Engineer, and use AI to get there — understand
how a company actually sells, end to end, and build the systems that make
it happen.

**The motive.** I started in Salesforce CRM Analytics, building dashboards.
At Twilio I met the term GTM for the first time — ToFu, opportunity
management, customer success, CPQ, quote-to-cash — whole teams I had been
reporting on without really understanding. I don't want to stay the CRM
Analytics person.

**The plan.** Learn Salesforce in depth, with the business metrics, process
and foundations underneath it. Then the stack around it — n8n, Clay, 6sense
and the AI layer on top. Then find out whether it lands the job. Every step
gets written down on the site as it happens.

**Why in public.** I went looking for a proper step-by-step GTM learning
path and found it scattered across a hundred places. If this works, it
becomes the one place — and it is open source so anyone can read the source
of every lesson, and fork the platform itself.

> AI will come. Selling, and doing business, will never stop — it will only
> change shape. I just want to be able to solve a business problem in any era.

This is why the site teaches *concepts*, not clicks: sales cycles, lead
capture, lead enrichment, routing, automation. Salesforce is the way in,
not the destination.

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

## Design system

The NS Design System — tokens, components, sections and learning templates
— lives in [`design-system/`](./design-system/) and is published to
**https://salesforce.imswarnil.com/** by GitHub Pages on every push that
touches it. Start with its [readme](./design-system/readme.md) and
[DESIGN.md](./design-system/DESIGN.md).

## Deploy

Pushes to `main` deploy automatically to Ghost via
`TryGhost/action-deploy-theme` (`GHOST_ADMIN_API_URL` /
`GHOST_ADMIN_API_KEY` repo secrets).
