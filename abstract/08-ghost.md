# 06 · The Ghost glue — what NEITHER Ghost nor NSDS can supply

This is the theme's real job. None of it is styling; none of it has an NSDS
equivalent. **If you are deleting theme code, these are not candidates.**

---

## 1 · The members form is a state machine Ghost does not provide

`assets/css/2-components/subscribe.css` + `partials/members/subscribe.hbs`.

Ghost's members script does exactly one thing to a `data-members-form`: it puts
`loading`, then `success` or `error`, on the FORM element. It does not reveal a
message, spin a spinner, or disable a button.

> ⚠️ **The two message elements must stay SIBLINGS of the form** — they are
> revealed with `~`. Nest them inside it and they are hidden permanently.

That was a real bug: five hand-rolled copies each carried messages marked
`hidden` that nothing ever un-hid, so subscribing appeared to do nothing at all.

**ONE signup form in the theme.** `{{> "members/subscribe"}}` — home hero,
footer, blog sidebar, the CTA band. It is member-aware: a signed-in reader gets
"you're subscribed as …" instead of a field asking for an address Ghost already
has. `ask=true` forces the form anyway.

`{{> "members/tiers"}}` pulls plans from Ghost via `{{#get "tiers"}}` and the
`{{price}}` helper. **No price is written in the theme** — a hard-coded price
is one that will eventually disagree with the one that charges the card.

## 2 · Koenig editor cards

Ghost's editor emits `.kg-*` markup this repo does not write. Restyling it is
glue by definition:

- toggle card → FAQ accordion
- product card → testimonial
- `<pre><code class="language-x">` → upgraded to NSDS's `.ns-code` figure by
  `assets/js/code.js` (bar, gutter, `ns-tok-*` spans). That script builds the
  structure; NSDS's own `code.js` wires the copy button via `[data-code="copy"]`.

## 3 · JSON-LD assembled as ONE `@graph`

`partials/jsonld/graph.hbs` emits a single
`<script type="application/ld+json">` holding a `@graph` array — the pattern
Google prefers and Yoast/RankMath use.

- Site-wide base nodes (owner · website · navigation) always emit.
- Per-page nodes append after them, and **each per-page partial starts with a
  comma** because it is concatenated into an array.
- Live: `Course` (+ `CourseInstance`, `hasPart` → lessons) and
  `LearningResource` (+ `VideoObject` for video lessons).

> ⚠️ **Double-stache only.** `{{title}}` HTML-escapes quotes, which is what
> keeps the JSON parseable. `{{{title}}}` emits a raw `"` and breaks the block.

Included in `<head>` BEFORE `{{ghost_head}}`. Additive to Ghost's own JSON-LD;
the duplication is harmless and deliberate.

## 4 · Icons are inline SVG

`partials/icons.hbs` — 125 hand-drawn 24×24 icons dispatched by name. No font
request before the first icon paints, no empty boxes for missing glyphs, no
re-subsetting step to add one. Adding an icon is adding a `{{#match name}}`
line: 24×24 viewBox, `stroke-width: 1.7`, round caps, `currentColor`.

Every `<svg>` carries `.ns-icon` — NSDS's icon primitive, the same contract the
app's sprite icons use.

**Nothing else in this theme should contain a raw `<path>`.** A second copy of
artwork is invisible to the styleguide's icon check, which fails the build on
an unknown icon name.

## 5 · Ghost helper traps

- **Never call a HELPER across `../`** (`{{../url}}`) — Ghost throws and 500s
  the page. Dotted PROPERTY access (`{{primary_tag.slug}}`, `{{../../id}}`) is
  fine.
- `limit="all"` is **not supported** in `{{#get}}`. Use `limit="100"`.
- Internal tags are `hash-lesson` inside a filter string, `#lesson` in `{{#has}}`.
- `{{#get}}` **swaps the context**. Values from outside it need a `../` path,
  which is why several partials take the current id as a PARAM instead.
- Nested quotes break attributes:
  `data-state="{{^has visibility="public"}}locked{{/has}}"` closes the attribute
  at `"public"`. Put the whole attribute inside the block instead.

## The navigation trap — read before touching a menu

**`{{#foreach navigation}}` works in exactly one place, and fails silently
everywhere else.**

`navigation` is not a page variable. It is built by the `{{navigation}}`
*helper*, which resolves `current`, adds a `slug`, and then renders
`partials/navigation.hbs` with the result:

```js
this.navigation = output;          // core/frontend/helpers/navigation.js
_.merge(this, options.hash);       // …plus any hash you passed
templates.execute('navigation', …)
```

Outside that partial and the partials it calls, `navigation` is undefined —
`{{#foreach}}` over it emits an empty string. No error, no warning, and gscan
passes because it is valid Handlebars. **This theme shipped exactly that bug:
a fully written navbar that rendered no items at all.**

`@site.navigation` *is* available everywhere, but it is the raw setting — no
`slug`, no `current`.

So: one helper call per rendering, and the hash is how one partial serves
three of them.

```hbs
{{navigation variant="bar"}}
{{navigation variant="sheet"}}
{{navigation type="secondary" variant="footer"}}
```

`type` is Ghost's own switch between the primary and secondary menus.
`variant` is ours, and it works only because the helper merges its hash into
the context.

## Dropdowns come from Ghost Admin, with a `-`

Ghost's navigation is a **flat list** with no nesting of its own. The
convention this theme uses — and the one most Ghost themes use — is a leading
hyphen in the label:

```
Courses            top-level
-Administrator     a child of Courses
-Developer         a child of Courses
Blog               top-level again
```

Detected with `{{#match label "~^" "-"}}` — `~^` is Ghost's **startsWith**
operator. No JavaScript, so the structure is in the HTML and survives with
scripting off.

Two consequences worth knowing:

- **The marker is stripped with `{{split}}`, not by hand.** Ghost's `split`
  drops empty segments, so `-Courses` becomes `["Courses"]`; the segments are
  rejoined with `-` so `-Data Cloud - Advanced` keeps its internal dash.
  `partials/navbar/label.hbs`.
- **`slug` is `slugify(label)`, and slugify strips the hyphen.** `-Data Cloud`
  arrives as `data-cloud`, which is why `partials/navbar/icon.hbs` can map
  parents and children with the same table — and also why `slug` cannot be
  used to detect a child.

Handlebars cannot look ahead, so `navbar/links.hbs` closes the previous
parent's `<li>` at the start of the next one and closes the loop once at the
end. **The tags look unbalanced read top to bottom; they balance across
iterations.** The `{{~ ~}}` whitespace control in that file is load-bearing:
a parent with no children must emit a literally empty `.ns-navmenu` so
`:empty` matches and `theme/navbar.css` can hide its caret.

---

# Performance

*Merged from what was `09-performance.md`. It lives here because every
item on it is a consequence of how Ghost serves a theme.*

> ### ⚠️ Status: describes the removed implementation
>
> The fonts, preloads and inline theme script below shipped with the previous
> theme and are gone. The *reasoning* is still correct and is what to rebuild
> toward; the file paths and build hooks are not current.

## Fonts — one, self-hosted, one file preloaded

**Figtree**, and only Figtree: interface, reading layer, headings and the label
voice, separated by weight and size rather than by cut. It ships as four
woff2s — upright/italic × latin/latin-ext — and only `figtree-var-latin.woff2`
is preloaded, because the other three are gated behind `unicode-range` and
`font-style` and most routes never fetch them.

**No shipped serif** — `--font-serif` resolves to the platform's own (Georgia
where it exists), so a pull-quote still reads as a quotation and costs nothing.
**No shipped mono either**, now: `--font-code` borrows `ui-monospace` for code
blocks, on the same trade.

Three earlier states are stale, and each was true once: `N&M` / `nmtext` /
weight 450 is pre-Switzer. **Sentient**, or a claim that mono is *not* shipped,
is pre-Roboto-Mono. **Switzer + Roboto Mono, both preloaded** is pre-NSDS-3.0 —
and note that the third of these looks exactly like the second read backwards,
which is why the version is what to check, not the claim.

## The pre-paint theme script

`{{> "nsds/theme-init"}}`, generated by the sync, **inlined and blocking, first
thing in `<head>` before any stylesheet**. It sets `data-theme` on `<html>`
before first paint.

A `<script src>` is fetched async and paints too late — that is the
white-flash-on-every-navigation bug every design system with dark mode ships
once. It shares the `ns-theme` storage key with the Next.js app, so a reader
crossing between products keeps their theme.

## Images — one partial, `components/img.hbs`

Ghost generates the widths in `package.json → config.image_sizes`
(xxs 30 · xs 100 · s 300 · m 600 · l 1000 · xl 2000) at upload time. They cost
nothing extra to serve, and the theme was asking for exactly one — so a phone
downloaded a 1000px cover to paint it 340px wide.

```hbs
{{> "components/img" src=feature_image alt=feature_image_alt
    sizes="(min-width: 64rem) 24rem, 92vw" eager=true}}
```

- `sizes` matters: a wrong one is worse than none, because the browser picks
  confidently from it.
- `eager=true` on the **ONE** above-the-fold image per route; it also sets
  `fetchpriority="high"`. Everything else stays lazy. Above the fold,
  `loading="lazy"` is a pessimisation.

> ⚠️ **A plain `<img>`, deliberately not `<picture>`.** NSDS styles media with
> DIRECT-CHILD selectors (`.ns-chero__media > img`,
> `.ns-card__media > :where(img, video)`). A `<picture>` wrapper silently drops
> every one of them. The gain would be a format; the cost would be the
> object-fit and aspect ratio on every card on the site.

## Deferred rendering

`.ns-defer` (`content-visibility: auto` + `contain-intrinsic-size`) on
below-fold grids and bands. The size hint is **not optional** — without it the
skipped subtree measures 0, the scrollbar is wrong, and it jumps as each band
renders. Never use it above the fold, or on anything a fragment link or in-page
search must find.

## Scripts

All `defer`, never `async` — they run after parse, in order, and none blocks
first paint. Per-page: only a course page loads `tabs.js`, only a post loads
`toc.js`. Preconnect ONLY to origins the page actually hits, and only when
enabled; a speculative preconnect evicts a real one.

## Weight, measured rather than assumed

Numbers from the running site, not estimates:

| | uncompressed | **transferred** |
|---|---|---|
| `screen.min.css` | 481 KB | **67.6 KB** gzip |
| `main.min.js` | 23.9 KB | ~8 KB gzip |
| homepage HTML | 61 KB | ~12 KB gzip |

**The 481 KB figure is the one everyone reacts to, and it is not the one that
travels.** Ghost gzips on the wire; the browser downloads 67.6 KB of CSS in
one round trip. That is the number to argue with.

### Why cherry-picking the bundle is still deferred

`components/css/index.css` is a flat list of imports, so dropping the LMS
surfaces is mechanically easy. The measured sizes:

| never rendered by a Ghost page | source |
|---|---|
| `deck.css` — slides | 46.5 KB |
| `ai.css` | 47.2 KB |
| `admin.css` | 23.8 KB |
| `helpdesk.css` | 9.0 KB |

That is ~127 KB of source, against a 945 KB component layer — call it **single
digit KB once gzipped**, because CSS this repetitive compresses extremely
well.

Two files that look trimmable and are not:

- **`player.css` (60 KB)** — the lesson reading surface ports from
  `course-player-article.html`, which uses it. Dropping it now is a silent
  missing-style bug waiting for the courses collection.
- **`auth.css` (6.4 KB)** — the sign-in and account surfaces are on the
  roadmap and unblocked.

So the honest trade today is *single-digit KB saved* against *a whole class of
invisible breakage*, on surfaces that are about to be built. It is the wrong
side of the trade, and it stays deferred until the collections exist. When it
is done, `scripts/check-classes.mjs` is what makes it safe — a class that
vanishes from the bundle stops being "defined" and fails the build.

### What actually governs LCP here

Not the stylesheet. The largest paint element on the homepage is the `h1`,
which is text in the HTML — so LCP is bounded by the font and the
render-blocking CSS, both of which are one warm round trip. The levers already
pulled: both above-the-fold faces preloaded with `crossorigin`, `theme-init`
inlined so there is no white flash, analytics deferred to end-of-body and not
loaded at all without a key, and preconnect limited to the one origin the page
genuinely fetches from.
