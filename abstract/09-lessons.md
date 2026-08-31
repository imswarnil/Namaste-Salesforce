# 10 · How this went wrong — read before rebuilding

Written honestly so the rebuild does not repeat it. Every item below actually
happened.

---

## The root cause

**The theme grew a third opinion.** Ghost owns the content model, NSDS owns how
things look, and the theme should be the thin wiring between them. Instead it
accumulated its own component library, its own tokens, its own drawer, its own
table of contents — each a reasonable local decision, and collectively a second
design system that silently beat the vendored one.

The mechanism was the cascade: **layer 2 sits after NSDS, so anything the theme
declares wins — silently.** 130 class names existed in both. NSDS was
maintained, synced, compiled, shipped, and then overridden.

## The single most expensive mistake

I concluded the training module's namespace was "fully disjoint from NSDS,
nothing to migrate." It was disjoint by **name only**:

```
.ns-reader → .ns-training      .ns-track-card → .ns-trackcard
.ns-sidenav → .ns-trainingnav  .ns-track-list → .ns-roadmap
.ns-lock   → .ns-gate          .ns-subbar     → .ns-panelbar
```

~100 classes and six stylesheets reimplementing a layer that was already
vendored. **Comparing class NAMES is not comparing components.** Compare what
the thing IS.

## The failure mode that hides from every check

`gulp build` passed. `gscan` passed. Zero undefined classes. All JS parsed.
**And the pages still looked wrong.**

Static checks verify that code compiles, not that a page is right. Two specific
kinds of breakage passed every gate:

1. **Scripts whose selectors no longer match.** After markup moved onto NSDS,
   `training-nav.js` and `training-progress.js` still queried `.ns-sidenav__link`
   and `.ns-reader__foot`. They matched nothing. The features simply stopped
   working, and nothing reported it.
2. **Structural mismatches inside a component.** `.ns-callout` is a two-column
   grid; markup with three children put the button in the icon column.
   `.ns-card` pads `__body` and leaves the base unpadded, so `__header` rendered
   flush against the hairline. Both compiled perfectly.

> **RULE: when markup moves onto a new class, grep the JS for the old one in the
> same commit.**

## Other traps, each of which cost real time

| Trap | Symptom |
| --- | --- |
| `.ns-band` + `.ns-section` nested | `padding-block` applied **twice**; every band double height |
| `.ns-mark` name clash | NSDS's `<mark>` highlight vs the theme's SVG logo; `width:100%` on highlighted text in posts |
| `.ns-avatar` contract inverted | NSDS WRAPS the `<img>`; the theme put the class ON it — mono letter-spacing meant for initials, no object-fit |
| `theme-init.js` banner | its comment quotes `{{ghost_head}}`; Ghost parsed it and gscan failed |
| Nested quotes in an attribute | `data-x="{{^has visibility="public"}}"` closes at `"public"` |
| Regex over `build-styleguide.py` | whitespace substitution matched across a newline and corrupted the Python |
| `limit="all"` | not supported by `{{#get}}` |

## What to do differently

1. **Check Ghost, then NSDS, then write.** In that order, every time.
2. **Measure, do not reason.** Diff the markup's classes against NSDS's own
   reference templates in `NS-Design-System/templates/`. Coverage went 51% → 77%
   only once it was measured rather than argued about.
3. **Count two things, not one.** *Coverage* (does an NSDS class appear?) and
   *utility ratio* (is the markup around it still hand-rolled?). They read 77%
   and 59% at the same moment; both were true.
4. **Open the browser.** Nothing above substitutes for it. The one check never
   run here was rendering a real page against real Ghost data — which is
   precisely where the remaining breakage is.
5. **Do not fabricate data.** NSDS has `.ns-rating` and `.ns-price__was`; Ghost
   has no review model and no "was" price. Omitting them is right. Rendering
   five hard-coded stars is decoration pretending to be data.
6. **Delete only what you can prove is dead**, and say so in the commit. "Delete
   all" is not a plan; every deletion here needed a grep first, and the ones
   that skipped it broke something.

## The order to rebuild in

`01` → `02` → `03` before writing a line of CSS. Get the URL model and the
dispatcher right first: they are the only parts that are expensive to change
later. Styling is cheap to redo; content URLs are not.
