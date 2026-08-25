# partials/icons

One partial per icon. Each is a **one-line wrapper** over the Phosphor icon
font that ships in `assets/icons/`:

```hbs
{{!-- partials/icons/search.hbs --}}
<i class="ph ph-magnifying-glass" aria-hidden="true"></i>
```

Used from any template as:

```hbs
{{> "icons/search"}}
```

## Why wrappers rather than writing the class inline

Three reasons, and only the third is about tidiness.

1. **The icon set is swappable in one place.** Every icon in the theme is
   named by ROLE (`search`, `menu`, `close`, `next`) rather than by whatever
   the icon library happens to call it (`magnifying-glass`, `list`, `x`,
   `caret-right`). Swapping Phosphor for inline SVG, or for a different set,
   is then an edit to this directory — not a grep across every template for a
   class name that also appears in prose and comments.

2. **A missing glyph is invisible, not broken.** An icon font renders an
   absent glyph as empty space: no error, no box, nothing in the console. A
   named partial at least fails loudly — Ghost 500s on a partial that does not
   exist — which turns a silent gap into a stack trace.

3. `aria-hidden` is on every single one. Icons here are always decorative:
   the control they sit in carries the accessible name. Writing the `<i>` by
   hand is how one of them ends up without it and a screen reader starts
   announcing a private-use codepoint.

## Adding one

Check the glyph exists in the subset first — `assets/icons/phosphor.css` is
the list, and it is generated from the icons the design system actually uses:

```bash
grep 'ph-your-icon' assets/icons/phosphor.css
```

If it is not there the icon will render as blank space. Re-subset upstream in
NS-Design-System rather than reaching for a CDN; nothing in this theme is
allowed to fetch from a third party at run time.
