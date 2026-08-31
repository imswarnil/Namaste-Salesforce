# theme/ — the only CSS this theme owns

Numbered so the folder order **is** the import order, and the import order
**is** the cascade within `@layer components`. If two rules in here fight, the
higher number wins. That is the whole reason for the digits.

```
0-foundation/   theme-owned custom properties.        ⚠ NOT design tokens.
1-base/         document-level: reset, page shell.
2-layouts/      page-level structures the theme owns.
3-components/   things the theme draws or deviates on.
4-ghost/        Ghost's vocabulary (.kg-*, .gh-content), translated.
5-utilities/    theme utilities. Last, so they win.
9-generated/    machine-written. Never edit by hand.
```

The numbering mirrors NS-Design-System's own `0-foundation / 1-base / …`
layout, deliberately: someone who has read one should be able to navigate the
other without a map.

---

## ⚠ 0-foundation does NOT hold tokens

This is the one place the structure diverges from NSDS's, and the divergence
is the point.

**NSDS owns every design token.** Colour, spacing, radius, type scale,
duration — all 278 of them arrive vendored in `assets/css/nsds/nsds.css` and
are consumed by both this theme and the Next.js LMS. A `--color-brand-500`
declared here would be a *second* source of truth for a value the two products
must agree on, and the drift would be invisible until someone diffed two
running sites.

So `0-foundation/` is for custom properties that are **theme-local by
nature** — a value scoped to one theme component, or a knob NSDS has no
opinion about. If you are about to declare a colour, a spacing step or a font
size here, the answer is upstream in NSDS.

That rule has already been broken once. `theme/3-components/navbar.css` sets
no `--_control-h`, and its comment explains at length why: overriding one
NSDS-owned variable flattened every control in the navbar to the wrong height
on desktop. Read it before adding a variable anywhere in this tree.

## What belongs here at all

Three questions, in order — the same ones in `abstract/04-css.md`:

1. **Does Ghost already do it?** Members, search, RSS, sitemaps, image sizing,
   `{{navigation}}`. If yes, stop.
2. **Does NSDS already do it?** 1,822 selectors. Grep before writing:
   `grep -oE '\.ns-[a-zA-Z0-9_-]+' ../nsds/nsds.css | sort -u | grep <thing>`
3. **Only then**, and it goes in the numbered folder that matches what it is.

Everything currently in this tree is a **translation** — Ghost's vocabulary,
the browser's defaults, or a seam between NSDS's assumptions and Ghost's
reality — with exactly one exception, `3-components/logo-sting.css`, which
draws the brand mark because NSDS has no Namaste Salesforce mark in it and
says why in its own header.

**The budget: ~15 rules that are not translation.** Past that, the theme has
started being a design system again, which is what `abstract/09-lessons.md` is
a record of. Count them; do not estimate.

## Adding a file

1. Pick the folder by what the file IS, not by what feels tidy.
2. Add the `@import` to `assets/css/screen.css` in numeric order.
3. Everything goes inside `@layer components`. A rule outside a layer beats
   every layered rule at any specificity and silently revokes the cascade
   contract — `scripts/check-layers.mjs` fails the build on it.
4. No raw values. There is a token for it, and `var(--x, 12px)` is a raw value
   with extra steps.
