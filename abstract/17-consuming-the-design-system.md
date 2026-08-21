# 17 · Consuming NSDS — and the CSS-variables question

> **The short answer: NSDS is already a CSS-variables design system.** Tailwind
> is not underneath it, it sits *beside* it as an optional utility bridge, and
> the framework-neutral build already exists and already ships. You do not have
> to convert anything. You have to choose which of two files to import.

Everything below was measured against the repo at
`../../../../NS-Design-System`, not inferred from its README.

---

## 1. What NSDS actually is

Two entry points, and the difference is the whole answer:

| Entry | Contains | Needs a build? |
| --- | --- | --- |
| `styles.css` | tokens → base → icons → **300 components**, all plain CSS | no |
| `tailwind.entry.css` | `@import "tailwindcss"` + the token bridge + `styles.css` | yes |

And two matching prebuilt bundles, both committed in `dist/`:

| File | Size | Min | What it is |
| --- | --- | --- | --- |
| `dist/namaste-ui.css` | 819 KB | **420 KB** | `styles.css` flattened. **No Tailwind.** |
| `dist/namaste-ui.tailwind.css` | 610 KB | 489 KB | the above + Tailwind v4 utilities |

NSDS's own build script says it in its header, and it is worth quoting because
it is the design intent rather than my reading of it:

> `dist/namaste-ui.css` — *"Framework-neutral plain CSS with no Tailwind, so it
> can be dropped into a page with no build step at all."*

**This is verified, not assumed.** Across all 33 component stylesheets and all
7 token files there is not one `@apply`, not one `theme()` call, and not one
`tw-` prefix. The component layer is hand-written CSS whose only dependency is
`var(--…)`:

```css
.ns-btn {
  gap: var(--gap-inline);
  min-block-size: var(--target-comfy);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-btn);
  font-family: var(--font-sans);
  transition: background-color var(--duration-fast) var(--ease-out);
}
```

Nothing in that rule knows Tailwind exists.

### The inventory

```
407  custom properties        colors 115 · typography 49 · dataviz 45 · spacing 39
                              effects 28 · layout 23  (+108 in the Tailwind bridge)
663  .ns-* class names
300  distinct component blocks
 33  component stylesheets
```

### So what is Tailwind doing there at all?

`tokens/tailwind.css` is **generated** from the same token files by
`scripts/build-tokens.mjs`, and it does exactly one thing: re-declare each token
inside `@theme` so a utility name exists for it. `--space-5` becomes `p-card`;
`--ns-brand-500` becomes `bg-brand-500`.

It is a **projection of the tokens into a second syntax**. Delete it and no
component loses a single declaration — you lose the ability to write `p-card`
in markup, and nothing else.

> Tailwind here is a *convenience for composing new markup*, not the material
> the system is made of. That is the opposite of the usual arrangement, and it
> is why the question "can I have a CSS-variables version?" already has a yes.

---

## 2. The cascade contract, which matters more than either choice

```css
@layer theme, base, ns-components, components, utilities;
```

Declared **before** any `@import`, and this ordering is the entire override
model:

- `ns-components` is its own layer, deliberately *not* the generic `components`
  one, so a consuming app's own components beat NSDS **by layer** rather than
  by import order or specificity.
- `utilities` is last, so a Tailwind utility always wins over a component
  default with no `!important`.
- **Nothing may sit outside a layer.** An unlayered rule beats every layered
  rule at any specificity, so one stray rule silently inverts the whole
  contract. NSDS enforces this with `scripts/lint-principles.mjs`.

`abstract/05` records that this project already broke this once, by importing
Tailwind before declaring the layers. The layer statement must come first.

**If you take the framework-neutral bundle, you inherit this contract and you
must keep honouring it.** Theme CSS goes in `@layer components` — after
`ns-components`, so you can override — and never outside a layer.

---

## 3. ⚠️ The gap in the framework-neutral bundle

This is the one real finding, and it is not written down anywhere in NSDS.

**`dist/namaste-ui.css` contains no CSS reset**, because the reset it relies on
is Tailwind's Preflight — which by definition is only in the *other* bundle.
Measured across every rule in both files:

| Preflight behaviour | in `namaste-ui.tailwind.css` | in `namaste-ui.css` |
| --- | --- | --- |
| `*, ::before, ::after { box-sizing: border-box }` | yes | **missing** |
| `img, video { display: block }` | yes | **missing** |
| `img, video { max-width: 100% }` | yes | **missing** |
| `ul, ol { list-style: none }` | yes | **missing** |
| `table { border-collapse: collapse }` | yes | **missing** |
| `button, input { font: inherit }` | yes | **missing** |

`tokens/base.css` is 50 lines and sets `body`, headings, links, focus rings and
selection — genuine base styling, but not a reset.

**`box-sizing` is the one that hurts.** Every component in the system is
authored assuming border-box: **89 rules declare a width *and* padding or a
border in the same block.** Under the browser default of `content-box` each of
those is padding *added to* the declared width, so a `100%`-wide element
overflows its parent by exactly its own padding. That is a subtle, everywhere,
"why is there a horizontal scrollbar" bug — the exact failure mode
`abstract/10` is about.

There is corroboration inside NSDS that this has already been hit once:

```css
.ns-input, .ns-select, .ns-textarea {
  inline-size: 100%;
  box-sizing: border-box;   /* ← the only box-sizing in the whole neutral bundle */
```

Someone patched the one place it visibly broke and did not generalise it.

**The fix is three lines**, and it belongs in the consuming theme (or upstream
in `tokens/base.css`, which would be better for everyone):

```css
@layer base {
  *, *::before, *::after { box-sizing: border-box; }
  img, svg, video { display: block; max-inline-size: 100%; height: auto; }
  table { border-collapse: collapse; }
}
```

> Worth raising as an NSDS issue: a bundle advertised as "drop it in with no
> build step" should not have an unstated dependency on a reset it does not
> ship.

---

## 4. Weight, and the one thing Tailwind does *not* buy you

420 KB minified is a lot of CSS for a Ghost theme.

The instinct is that Tailwind would tree-shake it. **It would not.** Tailwind
only purges *utilities* it generates by scanning your markup; `@layer
ns-components` is hand-written CSS that is included verbatim either way. Both
bundles carry all 300 components.

The real lever is that `components/css/index.css` is a flat list of `@import`s,
so **cherry-picking is already supported**. A Ghost marketing-and-blog site does
not need the LMS surfaces:

| Never rendered by Ghost | Size |
| --- | --- |
| `player.css` — the course player | 60 KB |
| `ai.css` | 45 KB |
| `deck.css` — slides | 46 KB |
| `admin.css` | 23 KB |
| `auth.css`, `helpdesk.css` | ~30 KB |

That is roughly **200 KB of source** the theme can simply not import. Write a
theme-local entry that imports the tokens plus only the component files this
site actually renders, rather than taking `dist/` wholesale.

> Do this **after** the theme renders correctly, never before. Trimming imports
> while you are still discovering which components you need produces the
> silent-missing-style bug, and you will blame the wrong thing.

---

## 5. The three options, honestly

Assume in all three that NSDS stays the source of truth — `abstract/03` covers
why the theme must not grow a third opinion.

### A · Framework-neutral CSS, no build (`dist/namaste-ui.css`)

- **Cost:** none. Copy one file into `assets/css/`, add the reset from §3.
  Assets resolve for free: the bundle's only real `url()`s are
  `../fonts/*.woff2` and `../icons/*.woff2`, so `assets/css/namaste-ui.css`
  finds `assets/fonts/` and `assets/icons/` with no rewriting.
- **Gives:** all 407 tokens, all 300 components, dark mode, the icon font.
- **Costs:** no utilities — every one-off spacing tweak is a named theme class
  in `@layer components`. Whole-system weight until you cherry-pick.
- **Best when:** the theme stays thin and mostly composes existing components,
  which is exactly what `abstract/00` says it should do.

### B · Tailwind + NSDS (what the previous implementation did)

- **Cost:** a build step, a content glob, and `assets/built/` committed.
- **Gives:** A, plus `p-card` / `bg-brand-500` for composition.
- **Costs:** the layer trap in `abstract/05` is live; a stale build ships CSS
  the source does not describe; every `.hbs` edit needs a rebuild.
- **Best when:** the theme writes a lot of novel layout.

### C · Neutral CSS + a tiny hand-written utility set

- The ~15 utilities a Ghost theme actually repeats (stack, cluster, visually
  hidden, measure), written once against the tokens.
- Keeps the no-build property; avoids one-class-per-tweak sprawl.
- Costs: you maintain it, and it is the seed of a third opinion. Cap it and
  write the cap down.

**My reading:** start at **A**. It is the only option that is reversible for
free — A → B is an afternoon, and you will know by then whether the utilities
are actually missed. Nothing about A forecloses B.

The decision itself lives in
[`decisions/0002-css-strategy.md`](decisions/0002-css-strategy.md), not here.

---

## 6. Facts to re-check before trusting this file

Written against NSDS as of **2026-08-21**. These are the claims that would
change if NSDS moves; each is one command:

```bash
DS=../../../../NS-Design-System

# Still no Tailwind in the component layer?
grep -rl '@apply\|theme(' $DS/components/css/ $DS/tokens/*.css | grep -v tailwind.css

# Does the neutral bundle still lack a universal box-sizing? (expect: 1 = .ns-input)
grep -c 'box-sizing' $DS/dist/namaste-ui.css

# Current weights
ls -la $DS/dist/
```
