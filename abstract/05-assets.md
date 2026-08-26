# 05 · Assets — fonts, icons, images, and why all of it is local

**Nothing this theme needs comes from a CDN.** No Google Fonts, no icon CDN,
no jQuery, no analytics script the theme installs on its own. Every byte is
served from the site's own origin.

That is not a preference. A Ghost theme ships as a zip and runs on somebody
else's server: a third-party host is a dependency the site owner did not agree
to, a second DNS lookup and TLS handshake before the first paragraph paints,
and a privacy disclosure they now have to make.

```
assets/
├── built/        ← COMPILED. Committed. Never edited by hand.
├── css/          ← the stylesheet source + the vendored bundle (see 04)
├── fonts/        ← two variable woff2 + their licences
├── icons/        ← NSDS's icon font + sprite, vendored
└── js/           ← NSDS's behaviour layer, vendored
partials/
└── icons/        ← THIS THEME'S icons: one inline-SVG partial each
```

---

## 1. Fonts

Two faces, both variable, both subset to latin, both self-hosted:

| file | face | carries |
|---|---|---|
| `switzer-var-latin.woff2` | **Switzer** | headings, prose, quotations |
| `roboto-mono-var-latin.woff2` | **Roboto Mono** | every index, label, duration, timestamp, status tag and kicker |

The split is NSDS design principle 2 and it is structural, not decorative:
**monospace is what makes a list of lessons read as *data* and a paragraph read
as *writing*, without touching colour.** A lesson row set in the sans is a
different design, not a smaller change.

Licences ship beside them — `FONTSHARE-EULA.txt` and `licences/roboto-mono-OFL.txt`.
They are not optional and they are not clutter: the theme is distributed.

### Both are preloaded, and only these two

In `default.hbs`, before the stylesheet:

```hbs
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="{{asset "fonts/switzer-var-latin.woff2"}}">
```

The `@font-face` rules live *inside* the compiled stylesheet, so the browser
only discovers them after fetching and parsing it — one round trip later than
it could start. Preloading closes that gap, which is what keeps the fallback
swap invisible on a cold load.

- **Only the two that draw above the fold.** A preload for something that is
  not immediately used is a warning in the console and bandwidth taken from
  something that was.
- **`crossorigin` is required even though these are same-origin.** Fonts are
  always fetched in CORS mode; a preload without it produces a second, unused
  download instead of a warm cache hit. This is the single most commonly
  broken line in any theme's `<head>`.

## 2. Icons — the theme draws its own

**`partials/icons/`, one inline-SVG partial per icon.**

```hbs
{{> "icons/home"}}
{{> "icons/arrow-right" class="ns-router__go-icon"}}
```

### Why not NSDS's icon font

NSDS's own answer is `<i class="ph ph-home">` against a subsetted Phosphor
woff2. That is the right answer for the React LMS and the wrong one here:

1. **A missing glyph renders as empty space, not a box.** An icon font fails
   *invisibly*, and the failure ships as a control nobody can see. A missing
   partial fails the build.
2. **The font is a blocking request before the first icon paints.** Inline SVG
   is already in the HTML.
3. `currentColor` and `1em` sizing behave identically either way, so nothing is
   lost visually.

### The grid

24px viewBox · **1.7 stroke** · round caps and joins · `fill="none"` ·
`stroke="currentColor"` · `aria-hidden="true" focusable="false"`.

Same grid and stroke as NSDS's bespoke sprite (`icons/namaste-icons.svg`), so
these mix in one row with anything drawn there. Phosphor's regular weight is
256/16 — 1.5 at 24 — close enough to sit beside, which NSDS's own readme
already assumes.

**Names match Phosphor's.** `ph-caret-right` → `icons/caret-right`. Keeping the
vocabulary identical is what makes porting an archetype mechanical: swap
`<i class="ph ph-x">` for `{{> "icons/x"}}` and there is no decision to make.

**Brand marks live in their own namespace** — `brand-x`, `brand-linkedin`,
`brand-youtube`, `brand-github` — because they are a different kind of thing:
filled, and drawn to their owner's outline rather than to our grid. The split
also keeps `icons/x` free for Phosphor's `x`, which is the close glyph and is
needed far more often than the logo.

**The partials carry no comments.** A `{{!-- … --}}` header on a file that is
one line of SVG is longer than the file, and it is inlined into the page on
every use. The grid, the naming and the reasoning are here and in
`partials/icons/README.md` instead. (The first version of these files shipped
`{!--` rather than `{{!--`, which is not a Handlebars comment at all — it is
literal text, and it rendered into every page that used an icon. Nothing
caught it: valid HTML, valid Handlebars, green gscan.)

### The bridge — the one real cost, and it is generated

NSDS styles some icons **by element**: `.ns-buybox__list i`, `.ns-code__btn i`,
`.ns-fit__list i` — **85 rules** across the bundle. An inline `<svg>` is not an
`<i>`, so every one of them misses, and the icon renders **unstyled rather than
missing**: right glyph, wrong size, wrong colour, wrong alignment. That is
much harder to notice than nothing at all.

`assets/css/theme/icon-bridge.css` restates those rules for `.ns-icon`. It is
**generated** from the vendored bundle by `scripts/build-icon-bridge.mjs`, runs
as the first step of every build, and CI diffs it — so it cannot drift from
upstream and nobody has to remember it.

```bash
node scripts/build-icon-bridge.mjs           # regenerate (gulp does this)
node scripts/build-icon-bridge.mjs --check   # what CI runs
```

> **The real fix is upstream.** One change in NSDS — `.ns-buybox__list i` →
> `.ns-buybox__list :is(i, .ns-icon)` — deletes this whole file and helps the
> LMS too. Until then the bridge is a translation, not a design decision, and
> lives in `@layer components` with everything else the theme translates.

### Adding one

1. Check Phosphor for the name and the shape. **Keep their name.**
2. Draw it on the 24 grid at 1.7. Do not paste a 256-viewBox path and hope.
3. Use it. There is no registration step.

`scripts/check-icons.mjs` fails the build on a `{{> "icons/…"}}` with no
partial — the inline-SVG equivalent of NSDS's missing-glyph check. It also
reports icons drawn but never used, which is how the set stays honest.

### NSDS's icon font is still vendored

`assets/icons/` carries `phosphor-subset.woff2`, `phosphor-fill-subset.woff2`
and `namaste-icons.svg`, because the vendored bundle's `@font-face` and
`<use href>` rules reference them and a 404 in a stylesheet is a console error
on every page. If a ported archetype keeps an `<i class="ph …">`, it still
works — but prefer the partial, and grep the subset before adding a `ph-`
class, because a glyph outside it renders as empty space.

## 3. Images

Ghost resizes; the theme does not. `package.json` declares the sizes:

```json
"image_sizes": { "xxs": 30, "xs": 100, "s": 300, "m": 600, "l": 1000, "xl": 2000 }
```

and every image comes through `{{img_url … size="m"}}` with a `srcset` and a
`sizes`. A raw `{{feature_image}}` ships a 3000px original to a phone.

- **`loading="lazy"` on everything below the fold**, `eager` on a feature image
  that is the first thing on the page — lazy-loading the LCP element delays it
  by one round trip.
- **`alt` comes from `feature_image_alt`**, and an empty `alt` is correct for a
  decorative image. Never invent alt text in a template.

## 4. What is vendored, and how to refresh it

`assets/css/namaste-ui.css`, `assets/css/ns-tailwind.css`, `assets/fonts/*`,
`assets/icons/*` and `assets/js/*.js` are all **copies of NSDS**. They are
committed because a Ghost theme has to be self-contained, and because CI must
build without NS-Design-System checked out beside it.

```bash
./scripts/sync-nsds.sh              # copies from ../../../../NS-Design-System
npm run build                       # regenerates the icon bridge, recompiles
```

Then **look at a page**. `gscan` cannot see a visual regression, and a sync is
exactly when one arrives.

The font and icon `url()`s in the bundle are `../fonts/…` and `../icons/…`.
From `assets/css/` that resolves to `assets/fonts/` and `assets/icons/`; from
the compiled `assets/built/` it resolves to the same two places. So the paths
are correct whether or not postcss rebases them during the inline — the sort of
thing that otherwise shows up only as a 404 on a font nobody notices.

## 5. What ships, and what does not

`assets/css/` is **not** in the theme zip — only `assets/built/` is served.
Shipping both invites someone to edit the wrong one. The prune list lives in
`package.json`'s `zip` script and in `.github/workflows/deploy-theme.yml`, and
the two must agree; see [`06`](06-build-and-ci.md).
