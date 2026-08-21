# 05 · CSS architecture

`assets/css/screen.css` is the final stylesheet and stays tiny: Tailwind,
`@source` globs, `@custom-variant dark`, and the imports.

```
nsds/           THE DESIGN SYSTEM — tokens, base elements, the .ns-* layer
0-foundation/   only what NSDS does not own: the bridge, mixins, helpers
1-elements/     bare HTML, one file per element family
2-components/   what remains of the theme's own layer
```

Order is dependency order: a later layer spends what earlier ones declare.
Each layer has an `index.css` listing its files, so adding one means adding a
file and ONE line — `screen.css` never changes.

---

## ⚠️⚠️ THE LINE THAT MUST COME FIRST

```css
@layer theme, base, ns-components, components, utilities;
@import "tailwindcss";
```

That bare `@layer` statement must precede the Tailwind import. **Delete it and
a large amount of styling silently stops applying.**

Cascade-layer order is fixed by the FIRST statement naming each layer, and a
later statement can only APPEND names it introduces. Tailwind emits
`@layer theme, base, components, utilities;` first. So when NSDS then asks for
`ns-components` to sit between `base` and `components`, the name is appended to
the END:

```
theme · base · components · utilities · ns-components     ← WRONG
```

Layer order beats specificity, so in that arrangement **every NSDS rule wins
over the theme's layer 2 and over Tailwind utilities** — the exact inverse of
the contract. The symptom is silent: `.ns-subscribe--dark .ns-field__label`
(two classes) loses to `.ns-field__label` (one class), and `hidden` / `p-4`
cannot override an NSDS default without `!important`.

Naming the full order up front makes both later statements no-ops.

Verify: the first non-`properties` statement must be the five-name one.

```bash
grep -o '@layer[^;{]*;' assets/built/screen.css | head -3
```

## The layer-2 rule: NSDS wins

Layer 2 sits AFTER NSDS in the cascade, so anything declared there beats it —
**silently**. That is how a vendored system gets shipped and then overridden by
a local copy nobody remembers writing.

Before adding to layer 2:

1. Check NSDS first.
2. If NSDS has the class, **do not redeclare it** — change the MARKUP to NSDS's
   contract instead.
3. If you genuinely need an addition, add the **variant only, never the base**,
   and say in the file header what NSDS owns.

## Two scoping rules in layer 1

- Reading-context styling uses `:where(.gh-content, .ns-prose)` — **zero
  specificity**, so utilities and NSDS always win.
- Global element rules guard with `:not([class])` so utility-styled markup is
  never touched.

## No inline styles. Ever.

Zero `style="…"` attributes and zero `<style>` blocks in any `.hbs`. An inline
style cannot be themed, cannot flip in dark mode, cannot be overridden by a
later layer and cannot be found by grep.

Spacing comes from NSDS's `.ns-stack` utilities. The handful of *placements*
NSDS does not name (where a component SITS, which is a page decision) live in
one small `2-components/layout-bridge.css`. Keep it small: it is the pressure
valve, not a second component layer.

## State is an ATTRIBUTE, not a class

NSDS expresses state with `aria-current="page"`, `data-state`, `[open]`,
`aria-expanded` — so the thing the CSS styles and the thing a screen reader
announces are one source and cannot drift. Follow that. The few genuine state
classes a script must toggle live in `2-components/state.css`.
