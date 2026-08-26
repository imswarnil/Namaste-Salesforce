# partials/icons/ — the theme draws its icons

One partial per icon, each an **inline SVG**. Use it with a partial parameter
for the class:

```hbs
{{> "icons/home"}}
{{> "icons/arrow-right" class="ns-router__go-icon"}}
```

## Why inline SVG, when NSDS ships an icon font

NSDS's own answer is `<i class="ph ph-home">` against a subsetted Phosphor
woff2. That is a good answer for the React LMS and a worse one for a Ghost
theme, for three reasons:

1. **A missing glyph renders as empty space, not a box.** An icon font fails
   invisibly, and the failure ships. A missing partial fails the build.
2. **The font is a blocking request before the first icon paints.** Inline SVG
   is already in the HTML.
3. **`currentColor` and `1em` sizing behave the same either way**, so nothing
   is lost visually.

The cost is real and is paid in one file — see *the bridge* below.

## The grid

24px viewBox · **1.7 stroke** · round caps and joins · `fill="none"` ·
`stroke="currentColor"` · `aria-hidden="true" focusable="false"`.

That is the same grid and stroke as NSDS's bespoke sprite
(`icons/namaste-icons.svg`), so these mix in one row with anything drawn
there. Phosphor's own regular weight is 256/16, which is 1.5 at 24 — close
enough to sit beside, which is what NSDS's readme already assumes.

**Names match Phosphor's.** `ph-caret-right` → `icons/caret-right`. Keeping
the vocabulary identical is what lets an archetype be ported by swapping
`<i class="ph ph-x">` for `{{> "icons/x"}}` with no decision to make.

**Brand marks are the exception.** `github-logo.hbs` is filled and drawn to
its owner's outline, because redrawing a company's mark on our grid
misrepresents it. Marked as such in the file.

## The bridge — the one real cost

NSDS styles some icons **by element**: `.ns-buybox__list i`, `.ns-code__btn i`,
`.ns-fit__list i` — 59 selectors across 12 stylesheets. An inline `<svg>` is
not an `<i>`, so every one of those rules misses, and the icon renders
unstyled rather than not at all: right glyph, wrong size, wrong colour, wrong
alignment. That is harder to notice than a missing icon.

`assets/css/theme/icon-bridge.css` restates those rules for `.ns-icon`. It is
**generated** by `scripts/build-icon-bridge.mjs` from the vendored bundle, so
it cannot drift from upstream, and CI diffs it the same way it diffs
`assets/built/`.

```bash
node scripts/build-icon-bridge.mjs          # regenerate after a sync-nsds
node scripts/build-icon-bridge.mjs --check  # what CI runs
```

> **The real fix is upstream.** One selector change in NSDS —
> `.ns-buybox__list i` → `.ns-buybox__list :is(i, .ns-icon)` — deletes this
> whole file and helps the LMS too. Until then the bridge is a translation,
> not a design decision, and belongs in `@layer components` with everything
> else the theme translates.

## Adding an icon

1. Check Phosphor for the name and the shape; keep their name.
2. Draw it on the 24 grid at 1.7. Do not paste a 256-viewBox path and hope.
3. `{{> "icons/<name>"}}`. There is no registration step.

`scripts/check-icons.mjs` fails the build on a `{{> "icons/…"}}` that has no
partial — the inline-SVG equivalent of NSDS's missing-glyph check.
