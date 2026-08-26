# 04 · CSS — the cascade, and how to write it here

**Read this before writing a single rule.** Almost every visual bug in this
project's history was a cascade problem wearing a styling problem's clothes.

---

## 1. The file that decides everything

`assets/css/screen.css` is the SOURCE. The browser never loads it —
`assets/built/screen.css` is what `default.hbs` links, and gulp compiles one
into the other. **Edit the source; never the output.**

```
assets/css/
├── screen.css              ← the only entry point. Layer statement, imports.
├── namaste-ui.css          ← VENDORED from NSDS. Never edit.
├── ns-tailwind.css         ← VENDORED token bridge. Never edit.
└── theme/                  ← everything the theme itself owns
    ├── reset.css           ← what NSDS assumes but does not ship
    ├── ghost.css           ← Koenig's .kg-* vocabulary, translated
    ├── shell.css           ← the page shell: footer pinned to the bottom
    ├── navbar.css          ← Ghost's flat nav, in NSDS's nested chrome
    ├── icon-bridge.css     ← GENERATED. Never edit. See 05.
    └── logo-sting.css      ← the brand mark. The one exception — see below.
```

Six files, and **five of them are translations rather than design**: they
exist because Ghost or the browser imposes something NSDS has no opinion
about. That ratio is the health metric for this layer. When it stops being
true, the theme has started being a design system again.

**`logo-sting.css` is the one place the theme draws rather than composes**,
and it is allowed for a single reason: NSDS has no Namaste Salesforce mark in
it, because NSDS is shared with the LMS and the mark is *brand*, not system.
Even then the geometry is not invented here — the cloud, the 307 India dots
and the namaste hands are lifted verbatim from `logo-sting/intro.html`, the
4-second broadcast sting, which is the source of truth for the mark's shape.
A second exception on those terms needs the same paragraph written for it.

## 2. The layer statement, and why it comes first

```css
@layer theme, base, ns-components, components, utilities;
```

Declared **before any `@import`** — a bare `@layer` statement is one of only
two things allowed to precede one. Read it as a precedence list, lowest first:

| layer | holds |
|---|---|
| `theme` | Tailwind's `@theme` variables |
| `base` | preflight + NSDS's `tokens/base.css` — bare element defaults |
| `ns-components` | **the design system** |
| `components` | **this theme's** classes — they beat NSDS |
| `utilities` | Tailwind utilities — they beat everything |

Two consequences worth knowing by heart:

- **A utility always wins.** `<a class="ns-btn ns-btn--primary p-8">` has 2rem
  of padding with no `!important` anywhere. Specificity inside NSDS only ever
  decides DS-vs-DS conflicts; a `:has()` chain still loses to `.p-4`.
- **Nothing may sit outside a layer.** An unlayered rule beats every layered
  rule at any specificity, so one stray rule silently revokes the whole thing.

### This has already broken once, and it broke silently

Built without the bare statement, the compiled order came out

```
theme → base → components → utilities → ns-components
```

— the design system **last**, beating both the theme's own layer and every
utility. Nothing errored. Overrides simply stopped working.

So it is not a matter of discipline any more. `scripts/check-layers.mjs`
re-proves the contract on **the compiled output**, on every build and in CI.
It runs on the output because checking the source would only prove the
statement was written, which was never the failing part.

### The one sanctioned exception

At the tail of `theme/ghost.css`. Ghost injects its own `cards.min.css`
**unlayered** through `{{ghost_head}}`, and an unlayered rule beats every
layered rule at any specificity — so the rules that override it cannot be
layered either. That block is fenced and explains itself.

**Do not add anything to it that works from inside the layer.**

## 3. Where a change belongs — the decision, in order

Ask these three questions in this order. The rule that would have prevented
most of the rework in [`10`](10-how-this-went-wrong.md) is just this list.

### Q1 · Does Ghost already do this?

Members, search, RSS, sitemaps, image resizing, the `{{navigation}}` helper,
`{{reading_time}}`, `{{excerpt}}`, related posts through `{{#get}}`. If Ghost
supplies it, the theme's version is a second copy that will drift and a
setting in Admin that stops working.

### Q2 · Does NSDS already do this?

**Search the vendored bundle before writing anything.** 1,779 selectors is
more than anyone remembers.

```bash
grep -oE '\.ns-[a-zA-Z0-9_-]+' assets/css/namaste-ui.css | sort -u | grep card
grep -n -A20 '\.ns-bcard\b' assets/css/namaste-ui.css
ls ../../../../NS-Design-System/templates/     # is there an archetype?
```

If there is an archetype, **port it** — do not rebuild it. If there is a
component but no archetype, compose it and check the class names.

### Q3 · Only now: write it. Where?

| What it is | Where it goes |
|---|---|
| A one-off layout only this page has | **a utility in the markup** |
| Translating Ghost's vocabulary (`.kg-*`, `.gh-*`) | `theme/ghost.css` |
| Something NSDS assumes but does not ship | `theme/reset.css` |
| A genuine, reusable component both products need | **upstream, in NSDS** |
| A genuine component only the Ghost site needs | `theme/` + a note saying why |

The fourth row is the one people skip. A component the LMS will also need
belongs in NSDS even though that is a slower change — putting it here is how
the two products stop matching.

## 4. Writing a rule

Everything in `theme/` obeys the same rules NSDS enforces on itself, because a
theme layer with looser standards is where the drift starts.

```css
@layer components {
  .kg-callout-card {
    gap: var(--space-3);
    padding: var(--pad-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface-2);
    transition: border-color var(--duration-fast) var(--ease-out);
  }
}
```

- **`@layer components`, always.** A rule outside a layer breaks §2 for the
  whole site.
- **No raw values.** No hex, no `px` radius, no `240ms`, no `font-family`, no
  bare padding or gap number. There is a token for it — 278 of them.
- **Not even inside a `var()` fallback.** `var(--duration-slow, 240ms)` is a
  raw value with extra steps. Use the token with no fallback; if it is missing,
  that is a bug to fix upstream, not to paper over.
- **If a value genuinely cannot be a token**, append
  `/* lint-ok: <reason> */` on that line, so the exception is argued for in
  the diff rather than buried.
- **State is an attribute** — `aria-current`, `aria-expanded`, `data-state`,
  `open` — never a class. The CSS and the screen reader then read one source,
  and there is no second state to keep in sync.
- **Never `!important`.** If a rule is not winning, the layer is wrong, and
  `!important` hides that rather than fixing it.

## 5. Adding a component — the whole procedure

1. **Q1, Q2, Q3 above.** Most of the time you stop at Q2.
2. **Find the archetype**: `ls ../../../../NS-Design-System/templates/`. If one
   exists, copy it into `partials/`, rename to `.hbs`, and swap the marked
   slots for Ghost helpers. `data-members-*` attributes work as-is.
3. **Replace the archetype's inline `style="…"` with utilities.** Never carry
   an inline style across — CI fails on it, and correctly.
4. **Do not rename a class on the way through.** Not even to make it read
   better. §3 of [`03`](03-design-system.md) is the price list.
5. **Swap `<i class="ph ph-x">` for `{{> "icons/x"}}`.** The names match
   deliberately, so this is mechanical. [`05`](05-assets.md).
6. **Check the behaviour.** If the archetype's comment names a script, the
   component is inert without it — that script is already vendored in
   `assets/js/`, but it has to be in the gulp bundle list.
7. **`npm run build`.** `check-classes` and `check-icons` will tell you about
   a name you invented or an icon you have not drawn.
8. **Then look at the page.** In both themes, at 360px, and with JavaScript
   off. §7.

## 6. Utilities: what they are for, and what they are not

Tailwind is here to compose **layout this theme has and NSDS does not** —
the gap between two bands, a one-off grid on the homepage, the margin under a
ported archetype's inline style.

It is **not** here to build components.

```hbs
{{!-- NO. This is .ns-card, rebuilt badly, and it will not follow a token
     change or dark mode. --}}
<div class="rounded-md border border-neutral-200 bg-white p-5 shadow-sm">

{{!-- YES. --}}
<div class="ns-card">
```

The signal that this has gone wrong: a `class` attribute with more than about
six utilities in it, or the same six repeated on three pages. Both mean a
component exists and has not been found.

## 7. Verifying — and why green is not enough

`gscan` and a green build are **necessary and not sufficient**. Both were green
while the site was visually broken, more than once — an unstyled class is valid
HTML, and a missing style is not a build error.

After any CSS change:

```bash
npm run build
```

then **look at a page**, and specifically:

- **Both themes.** The switch is in the top bar; dark is where a raw colour
  shows up as a light-mode value on a dark surface.
- **360px wide.** 89 rules in the bundle declare a width alongside padding —
  under the wrong box model each overflows by exactly its own padding, which
  reads as a mysterious horizontal scrollbar.
- **With JavaScript off.** The nav, the outline, the theme controls and the
  code copy button are all progressive enhancement and must degrade.
- **`/blog/styleguide/`** once it exists — it carries every Koenig card, which
  is the only way to see the whole `theme/ghost.css` surface at once.

## 8. The trigger that reopens this decision

> The theme's own `@layer components` block grows past **~15 rules** that are
> not Ghost-vocabulary translation.

That is the signal it has started being a design system again. Count it, do not
estimate it — the last one reached ~100 without anyone noticing, one reasonable
commit at a time.
