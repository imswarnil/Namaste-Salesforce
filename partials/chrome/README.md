# partials/chrome — the site's furniture

Three BARS will exist on this site, and they are genuinely different pages'
chrome rather than one bar with options:

| bar | where | what it says |
|---|---|---|
| `topnav.hbs` | marketing, blog, docs, listings | where you can go |
| `coursenav.hbs` | inside a lesson (`#lesson`, `#training-content`, …) | where you ARE, and how far in |
| `nav-sheet.hbs` | below `lg`, any page | the whole site map, as a dialog |

`default.hbs` picks between the first two on the same tags `post.hbs`
dispatches on — see `abstract/02`. A reading surface must not get a marketing
bar.

## Why the small partials exist

`brand`, `search`, `theme-switch`, `theme-toggle`, `members` and `burger` are
each used by **two or three** of those bars. They are partials for exactly
that reason, and not for any other.

That is a deliberate line. Ghost's own submission guidance says *"don't use
partials for every little snippet of code under the sun"*, and it is right:
a partial per snippet turns one readable template into forty files you have to
open in order. The test applied here is **used in more than one place, or
would drift if copied** — a brand lockup that appears in the bar, the sheet
and the course bar will drift; a `<h1>` will not.

`abstract/10` records what the drift actually costs: three copies of a lesson
row, two tables of contents, two share components, two post cards.

## Parameters

Partials take parameters rather than reading globals, so the same file can
serve a different bar:

```hbs
{{> "chrome/burger" sheet="site-nav"}}
{{> "chrome/brand" tagline="Learn"}}
{{> "chrome/members" size="sm"}}
```

Anything not passed falls back to a sensible default inside the partial.

## What is not here yet

- `coursenav.hbs` renders, but its progress value is hard-wired to 0 until
  there is somewhere real to read progress from. See the comment in the file.
- The training-section bar (`abstract/02`'s "training header") is not a third
  bar: it is `topnav.hbs` plus NSDS's `.ns-pathpick` control in the brand
  slot. Add it there, do not fork the file.
