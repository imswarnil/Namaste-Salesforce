# partials/internal — reading control off internal tags

Ghost gives an author no per-post switches beyond the editor's own. This theme
gives them some, using **internal tags** — the `#`-prefixed ones that never
appear on the site.

| Tag | Effect |
|---|---|
| `#hero-1` … `#hero-5` | which header treatment the post gets |
| `#toc` / `#no-toc` | force the table of contents on or off |
| `#duration-*` | reading/watching time — the tag's **description** is shown |
| `#level-*` | difficulty badge — likewise |
| `#format-*` | article / video / exercise / quiz |

## Two rules, both of which have bitten this codebase

**1 · A tag→class chain is resolved in exactly ONE partial.** Art direction is
needed in more than one place on a page, and copied it drifts. `abstract/10`
is a record of what that costs.

**2 · Metadata rides in the tag's DESCRIPTION, not its name.**
`#duration-1h-5m` has `description: "1h 5m"`. The theme prints the
description, so an author writes the display text in Ghost Admin and the theme
never parses `1h-5m` into `1h 5m`. Parsing would mean the theme owns the
format, and adding `#duration-90m` would need a code change.

## Reading them

Internal tags are excluded from `{{tags}}` by default, so they need
`visibility="internal"` explicitly — and note `hash-`, not `#`. In
`{{#has tag="#x"}}` you write the hash; in a **slug comparison** you write
`hash-`.

```hbs
{{#foreach tags visibility="internal"}}
    {{#match slug "~^" "hash-duration-"}}{{description}}{{/match}}
{{/foreach}}
```

## Every glyph must be in the subset

`assets/css/namaste-ui.css` carries a Phosphor subset generated from the
glyphs the design system itself uses. **A `ph-` class outside it renders as
empty space** — no error, no fallback box. Check before adding one:

```bash
grep 'ph-your-icon' assets/css/namaste-ui.css
```
