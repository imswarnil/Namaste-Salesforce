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
