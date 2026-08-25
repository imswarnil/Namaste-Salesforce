# partials/internal — reading control off internal tags

Ghost gives an author no per-post switches beyond the editor's own. This theme
gives them some, using **internal tags** — the `#`-prefixed ones that never
appear on the site.

An author adds `#no-toc` to a post in Ghost Admin and that post loses its table
of contents. No theme edit, no custom field, no second system.

| Tag | Effect |
|---|---|
| `#hero-1` … `#hero-5` | which header treatment the post gets |
| `#toc` / `#no-toc` | force the table of contents on or off |
| `#no-sidebar` | full-width reading column, no aside |
| `#wide` | the article body takes the wide container |
| `#duration-*` | reading/watching time — the **tag's description** is shown |
| `#level-*` | difficulty badge — likewise the description |

## Two rules, and both have bitten this codebase before

**1 · A tag→class chain is resolved in exactly ONE partial.**
Art direction is needed in three places on a page — the element, the
background layer and the media slot — and copied three times it drifts.
`abstract/10` in the sibling project is a record of what that costs.

**2 · Metadata rides in the tag's DESCRIPTION, not its name.**
`#duration-1h-5m` has `description: "1h 5m"`. The theme prints the
description, so an author writes the display text in Ghost Admin and the theme
never has to parse `1h-5m` into `1h 5m`. Parsing it would mean the theme owns
the format, and then adding `#duration-90m` needs a code change.

## Reading them

Internal tags are excluded from `{{tags}}` by default, so they need
`visibility="internal"` explicitly:

```hbs
{{#foreach tags visibility="internal"}}
    {{#match slug "~^" "hash-duration-"}}{{description}}{{/match}}
{{/foreach}}
```

Note `hash-` and not `#`. In a template's `{{#has tag="#x"}}` you write the
hash; in a **slug comparison** and in an import file you write `hash-`.
