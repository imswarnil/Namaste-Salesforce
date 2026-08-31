# Namaste Salesforce — Ghost theme

A Ghost theme for a Salesforce learning site, built as a **port of
[NS Design System](../../../../NS-Design-System)** — not a likeness of it.

Ghost owns the content model through `routes.yaml` and tags. NSDS owns how
everything looks. The theme is the wiring between them, and stays thin.

## Status: skeleton

The foundation is built and green — build, checks, CI/CD, chrome, reading
surface, icons, fonts. **The collections are not built, deliberately:** each
page family gets a spec in [`abstract/collections.md`](abstract/collections.md)
before any template is written for it. None is answered yet.

## Quick start

```bash
npm install
npm run dev      # gulp: build, then watch and rebuild
npm run build    # NODE_ENV=production — one production build
npm test         # build, then gscan
```

Then point a local Ghost at `content/themes/`, and upload `routes.yaml` in
**Admin → Settings → Labs → Routes** — Ghost does not read it from the theme.

## Layout

```
assets/
  built/     screen.min.css + main.min.js. Committed — no build on the server
  css/       screen.css → nsds/ (vendored) + theme/0-foundation…9-generated
  fonts/     Figtree, self-hosted, licensed — one face, four unicode-range cuts
  icons/     NSDS's icon font and sprite, vendored
  js/        0-vendor/ (NSDS) + 1-theme/ + theme-init.js (inlined)
partials/
  icons/     THIS theme's icons — one inline-SVG partial each, no comments
  navbar/    brand, links, search, github-star, theme-toggle, auth, burger,
             the mobile sheet, and the navigation JSON-LD
  footer/    link columns, the social row, the newsletter form
  home/      one partial per band of the homepage
  post/      one partial per kind of reading surface
  navigation.hbs   what Ghost's {{navigation}} helper renders — read it first
scripts/     the build and the checks — plain node, each runs standalone
abstract/    the documentation. Start at abstract/README.md.
```

## Documentation

**[`abstract/`](abstract/)** is the documentation, ordered by what breaks the
site if you get it wrong — and its README carries the **add-a-page-family
playbook** plus the surface checklist for a complete NSDS theme.
**[`CLAUDE.md`](CLAUDE.md)** is the same material compressed for Claude Code,
including the full NSDS reference.

Content strategy, the tag vocabulary, the teaching method and pricing are
**not** here — they live in the root knowledge base at
`Namaste Salesforce/abstract/`, because they are shared with the Next.js LMS.

## The rule

> Before writing a rule, a component or a script: check whether **Ghost**
> already supplies it, then whether **NSDS** already supplies it. The theme's
> job is only what neither can know about.

[`abstract/09-lessons.md`](abstract/09-lessons.md) is
what happens when that check is skipped.

## Licence

MIT.
