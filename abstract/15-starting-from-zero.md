# 15 · Starting from zero — what was removed, and what to decide

The theme was stripped to a **stack-free Ghost starter**. Nothing about the
build, the CSS approach or the component library has been decided yet. That is
deliberate: those decisions were previously made implicitly, one commit at a
time, and the result is `abstract/10`.

Everything below is recoverable from git — the last full implementation is at
tag-able commit `f8ec6d8` and its parents.

---

## What the theme is now

```
default.hbs          the shell — <head>, header, {{{body}}}, footer
home.hbs             `/` (routes.yaml maps it; Ghost 400s without this file)
index.hbs            the default collection listing
post.hbs             a post — and the future DISPATCHER (abstract/02)
page.hbs             a Ghost page
partials/
  navigation.hbs     reserved name, rendered by {{navigation}}
  post-card.hbs      one post in a listing
assets/css/screen.css  hand-written, ~30 lines, no build
routes.yaml          the URL model — unchanged, and the most valuable file here
```

No build step. No dependencies except `gscan`, which is a validator rather than
a stack choice — it is what Ghost itself runs on upload.

## What was removed

| Removed | Why | How to get it back |
| --- | --- | --- |
| Tailwind CSS v4, PostCSS, cssnano | a stack decision, unmade | choose it, then re-add |
| gulp + `gulpfile.js` | ditto — there is nothing to build yet | ditto |
| Alpine.js | ditto | ditto |
| `assets/css/nsds/`, `assets/js/nsds/`, `partials/nsds/` | **generated**, never hand-written | `yarn design:sync` regenerates all three |
| `scripts/sync-design.mjs` | the NSDS vendoring tool | documented in full in `abstract/08` |
| `scripts/build-styleguide.py` | generated the styleguide | `abstract/08` |
| `partials/icons.hbs` | 125 hand-drawn SVG icons | **not regenerable — recover from git** |
| `assets/fonts/*`, `assets/icons/*` | vendored by the sync | `yarn design:sync` |
| `dummy-content/import.json` | a fixture, cheap to remake | `abstract/14` |
| every other template and partial | the old implementation | git |

> ⚠️ `partials/icons.hbs` is the one deletion with no cheap recovery path.
> 125 icons drawn to a single contract. If icons are wanted, take that file out
> of git history rather than redrawing them.

## What survived, and why

- **`routes.yaml`** — the URL model. The only part of this project that is
  expensive to get wrong (`abstract/01`).
- **`abstract/`** — this documentation.
- **`prompt/`** — the content briefs (`abstract/09`).
- **`assets/logo/`** — brand identity, not a stack footprint.
- **`locales/`** — translations, still valid.
- **`.github/`** — CI, release workflow, issue and PR templates.
- **`LICENSE` · `README` · `CONTRIBUTING` · `CHANGELOG`** — the OSS surface.

## The decisions to make, in the order they constrain each other

### 1 · Does the theme use NSDS at all?
This is the biggest fork in the road and everything else follows from it.

- **Yes** → the theme owns almost no CSS; it vendors NSDS and writes markup
  against `.ns-*`. The Ghost site and the Next.js app cannot drift. This is
  what the last implementation did, and `abstract/03`, `04`, `05` and `08`
  describe it.
- **No** → the theme owns its styling. Simpler to reason about alone, and it
  guarantees the two products diverge.

Decide this before writing a single rule.

### 2 · What generates the CSS?
Only ask once (1) is answered.

| | Good when | Cost |
| --- | --- | --- |
| Hand-written CSS | small theme, no build, easiest to contribute to | you write the system yourself |
| Tailwind v4 | fast composition, tiny output | a build step; utilities in markup |
| Vendored NSDS + a thin layer | one system across two products | the vendoring must be maintained |

### 3 · Is there any JavaScript?
The last implementation ended with **almost none** — native `<details>`,
`<dialog>` and `popover` replaced an Alpine store, a scrim and two dropdowns.
That is worth repeating deliberately rather than by accident.

### 4 · Which page types exist on day one?
`abstract/01` lists seven. You do not need all seven to ship. A blog and a
course is a coherent v0.2.0; training and docs can follow.

## The order to build in

1. **`routes.yaml` into a local Ghost, and seed content in** (`abstract/14`).
   Nothing else is verifiable until a page can render.
2. **`post.hbs` as a dispatcher** (`abstract/02`) — get the branch order right
   while there are two branches instead of seven.
3. **Decide 1–3 above, and write the decision down here.**
4. Then styling.

Steps 1 and 2 are cheap now and expensive later. Step 4 is cheap at any time —
which is exactly why it should not come first.

## Record decisions here as they are made

> **Decision log** — append, never rewrite. A decision with its reasoning is
> worth ten times one without.
>
> - *(none yet)*
