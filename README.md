# Namaste Salesforce — Ghost theme

A Ghost theme for a Salesforce learning site, built as a **port of
[NS Design System](../../../../NS-Design-System)** — not a likeness of it.

Ghost owns the content model through `routes.yaml` and tags. NSDS owns how
everything looks. The theme is the wiring between them, and stays thin.

## Status: skeleton

The foundation is built and green — build, checks, CI/CD, chrome, reading
surface, icons, fonts. **The collections are not built, deliberately:** each
page family gets a spec in [`abstract/collections/`](abstract/collections/)
before any template is written for it. All eight are currently unanswered.

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
  built/     COMPILED and committed — Ghost has no build step on the server
  css/       screen.css (source) + the vendored NSDS bundle + theme/
  fonts/     Switzer + Roboto Mono, self-hosted, licensed
  icons/     NSDS's icon font and sprite, vendored
  js/        NSDS's behaviour layer, vendored
partials/
  icons/     THIS theme's icons — one inline-SVG partial each, no comments
  navbar/    the bar, the mobile sheet, and the pieces they share
  footer/    link columns, the social row, the newsletter form
  post/      one partial per kind of reading surface
  navigation.hbs   what Ghost's {{navigation}} helper renders — read it first
scripts/     the build and the checks — plain node, each runs standalone
abstract/    the documentation. Start at abstract/00-README.md.
```

## Documentation

**[`abstract/`](abstract/)** is the documentation, ordered by what breaks the
site if you get it wrong. **[`CLAUDE.md`](CLAUDE.md)** is the same material
compressed for Claude Code, including the full NSDS reference.

Content strategy, the tag vocabulary, the teaching method and pricing are
**not** here — they live in the root knowledge base at
`Namaste Salesforce/abstract/`, because they are shared with the Next.js LMS.

## The rule

> Before writing a rule, a component or a script: check whether **Ghost**
> already supplies it, then whether **NSDS** already supplies it. The theme's
> job is only what neither can know about.

[`abstract/10-how-this-went-wrong.md`](abstract/10-how-this-went-wrong.md) is
what happens when that check is skipped.

## Licence

MIT.
