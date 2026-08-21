# Contributing

Thanks for wanting to help. Typo fixes, accessibility improvements, new
sections, docs — all welcome, at any size.

> ### ⚠️ Read this before opening a styling PR
>
> The theme is currently a **stack-free starter**. There is no build step, no
> CSS framework and no component library, because those decisions have not been
> made yet — see [`abstract/15`](abstract/15-starting-from-zero.md), which lists
> the four open ones and the order they constrain each other in.
>
> That makes styling PRs **premature right now**: the first decision is whether
> the theme owns its CSS at all, and until it is settled, anything written
> against one answer is thrown away by the other. Structure, templates,
> accessibility, docs and the URL model are all fair game today.

---

## Getting set up

```bash
git clone https://github.com/imswarnil/Namaste-Salesforce.git
cd Namaste-Salesforce
npm install       # gscan only — there is no build step
npm test          # gscan, Ghost's own theme validator
```

You need a [local Ghost install](https://ghost.org/docs/install/local/) to see
the theme against real content. **Do this before you write anything** — it is
the single check that catches what the build cannot:

1. Point Ghost at the theme (symlink it into `content/themes/`).
2. Ghost Admin → Settings → Labs → **Routes** → upload `routes.yaml`.
3. Add a few posts, or build a seed fixture — [`abstract/14`](abstract/14-seed-content.md)
   describes how the old one was generated and which rules it had to encode.

> `routes.yaml` here is deliberately **minimal**. A route pointing at a template
> that does not exist is a **400**, not a fallback — Ghost answers
> `Missing template x.hbs` and the page is dead. So add a route back in the same
> commit that adds its template, never before. The full target model is at the
> bottom of [`abstract/01`](abstract/01-content-model.md).

## Where does my change go?

This project is three repositories with a strict division. Putting a change in
the wrong one is the most common way a PR gets sent back. (The design-system
row is how the previous implementation worked and the direction being resumed —
but see the note at the top: it is a decision to re-make, not a settled one.)

| If you are changing… | It belongs in |
| --- | --- |
| a colour, spacing, a component's shape or its variants | **[NS-Design-System](https://github.com/imswarnil/NS-Design-System)** |
| how a component *behaves* (menus, tabs, the outline) | **NS-Design-System** |
| which Ghost data appears, and where | **this repo** |
| URL shapes, tags, collections | **this repo** (`routes.yaml`) |
| quizzes, grading, certificates, anything with real user state | the Next.js app |

> **The theme's job is only what neither Ghost nor NSDS can know about.**

Before writing a rule or a component, check whether Ghost already supplies it,
then whether the design system does. NSDS's variant sets are larger than they
look — `.ns-btn` has 19, `.ns-table` has 17. Skipping this check is how the
theme previously grew ~100 classes that were NSDS components under different
names: **disjoint by name, identical in substance.** Compare what things *are*.

## The rules that CI enforces

- **`npm test` must pass** (gscan, Ghost's own validator).
- **No `style="…"` and no `<style>` in any `.hbs`.** An inline style cannot be
  themed, cannot flip in dark mode, cannot be overridden by a later layer and
  cannot be found by grep.

## The rules CI cannot enforce, and which matter more

- **When markup moves onto a new class, grep the JS for the old one in the same
  change.** A script whose selectors no longer match fails silently: the build
  is green, gscan is green, and the feature is simply dead. This has happened
  here more than once.
- **Look at it in a browser, light and dark.** Everything static can pass while
  every page is wrong. This is not a hypothetical here — it is the single
  failure that cost this project the most time.
- **State is an attribute, not a class** — `aria-current`, `data-state`,
  `[open]` — so the CSS and the screen reader read one source.
- **Do not invent data.** NSDS has a star rating and a "was" price; Ghost has
  neither a review model nor a discount. Omitting them is correct. Rendering
  five hard-coded stars is decoration pretending to be data.

## Ghost traps that will cost you an afternoon

- Never call a Ghost **helper** across `../` (`{{../url}}`) — Ghost throws and
  500s the page. Dotted **property** access (`{{primary_tag.slug}}`) is fine.
- `limit="all"` is not supported in `{{#get}}`. Use `limit="100"`.
- Internal tags are `hash-lesson` inside a filter string, `#lesson` in `{{#has}}`.
- `{{#get}}` swaps the context — values from outside need a `../` path, which
  is why several partials take the current id as a parameter instead.
- Nested quotes break attributes:
  `data-x="{{^has visibility="public"}}…"` closes at `"public"`.

## Commits and branches

Work on a branch off `main`. Write commit messages that say **why**, not just
what — the reasoning is the part nobody can reconstruct later.

## Releasing (maintainers)

Semver, with a theme-specific reading of what "breaking" means — see
[CHANGELOG.md](CHANGELOG.md). In short: **if upgrading could change a live
site's URLs or lose an editor's Admin settings, it is a MAJOR.**

```bash
# 1. update CHANGELOG.md, move Unreleased → the new version
# 2. bump package.json (the release workflow fails if the tag disagrees)
git tag -a v0.2.0 -m "0.2.0 — …"
git push origin v0.2.0
```

That builds the zip, runs gscan and publishes a GitHub release with the zip
attached, which is what a site owner uploads in Ghost Admin.

## Understanding the codebase

`abstract/` is the documentation, ordered by what breaks the site if you get it
wrong. `abstract/00-README.md` is the map. If you read two files, read
`01-content-model.md` (the URL model — the only part that is expensive to
change later) and `10-how-this-went-wrong.md` (the mistakes already made here,
so you do not repeat them).

## Code of conduct

Be decent. Assume good faith, review the change and not the person, and
remember that most contributors are doing this on their own time.
