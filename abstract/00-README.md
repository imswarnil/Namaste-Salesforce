# abstract/ — everything you need to rebuild this theme from nothing

**This folder is Ghost-theme only.** Anything about what to write, who it is
for, how lessons are taught, what things are called or how subscriptions work
lives in the root knowledge base at `Namaste Salesforce/abstract/` — see
*Where the rest went* at the foot of this file. The split is deliberate: those
decisions are shared with the Next.js LMS and the content pipeline, and a theme
that owns them becomes the place the other two have to look, which is how a
theme turns into a third product.

Files are ordered by **what breaks the site if you get it wrong**, not by what
is interesting. `01` is unrecoverable if wrong; `12` is a working preference.

---

## The theme in one paragraph

A Ghost theme for a Salesforce learning site. **Ghost owns the content model
through `routes.yaml` and tags; NSDS owns how everything looks; the theme is
the wiring between them and should be as thin as possible.** Every page is a
*port* of an archetype in `NS-Design-System/templates/` — not a likeness of
one. It is currently a **skeleton**: the wiring, the build, the checks, the
navbar, footer, homepage and reading surface exist; the collections do not, because none of
them has been specified yet.

## The rule that would have prevented most of the rework

> Before writing a rule, a component or a script: check whether **Ghost**
> already supplies it, then whether **NSDS** already supplies it. The theme's
> job is only what neither can know about.

That check was skipped repeatedly, and the result was ~100 classes
reimplementing NSDS's training layer under different names, three copies of a
lesson row, two tables of contents, two share components and two post cards.

---

## Read in this order

| # | File | If you get this wrong |
| --- | --- | --- |
| 01 | [`01-content-model.md`](01-content-model.md) | Every URL on the site 404s or 301s to the wrong page |
| 02 | [`02-post-dispatcher.md`](02-post-dispatcher.md) | Every post renders as the wrong kind of page |
| 03 | [`03-design-system.md`](03-design-system.md) | The theme reimplements NSDS and the two products drift |
| 04 | [`04-css-architecture.md`](04-css-architecture.md) | The cascade inverts and NSDS silently stops applying |
| 05 | [`05-assets.md`](05-assets.md) | Fonts flash, icons render as empty space, images ship at 3000px |
| 06 | [`06-build-and-ci.md`](06-build-and-ci.md) | You ship the CSS from before the fix |
| 07 | [`07-collections.md`](07-collections.md) | A pile of posts instead of a curriculum |
| 08 | [`08-ghost-glue.md`](08-ghost-glue.md) | Members, prose and editor cards break in ways tests miss |
| 09 | [`09-performance.md`](09-performance.md) | Slow pages, layout shift, a white flash on every navigation |
| 10 | [`10-how-this-went-wrong.md`](10-how-this-went-wrong.md) | You repeat the mistakes this rebuild was needed for |

Then, for the work rather than the hazards:

| # | File | Answers |
| --- | --- | --- |
| 11 | [`11-roadmap.md`](11-roadmap.md) | What actually makes this a better Ghost theme, ranked by return per hour |
| 12 | [`12-how-to-claude.md`](12-how-to-claude.md) | Working effectively with Claude Code here, grounded in what happened |

## [`collections/`](collections/) — **the next thing to do**

One file per page family — home, blog, courses, training, docs, resources,
toolkit, archive — each specifying what the surface is, what its URLs are, what
the listing shows, what the single page carries, and which NSDS archetype it
ports.

**All eight are unanswered, and no collection gets built before its file is.**
That folder is where the theme's remaining work is defined; everything else
here is the foundation it will be built on.

## [`decisions/`](decisions/) — the decision record

One file per choice that is expensive to reverse, with its reasoning, its
downside and the trigger that should reopen it. **This folder exists because
the last stack was never actually decided** — it accumulated one reasonable
commit at a time, which is why `10` had to be written.

| # | Decision | Status |
| --- | --- | --- |
| [0001](decisions/0001-reset-to-a-starter.md) | Reset the theme to a stack-free starter | Accepted |
| [0002](decisions/0002-css-strategy.md) | How the theme gets its CSS | **Accepted — option B**, Tailwind v4 + NSDS + gulp |
| [0003](decisions/0003-routes-yaml-minimal.md) | `routes.yaml` names only servable templates | Accepted |

---

## What exists right now

| | |
|---|---|
| **Build** | gulp + Tailwind v4 + cssnano → `assets/built/`, committed |
| **Checks** | layers, classes, icons, icon bridge, inline styles, Handlebars comments, gscan |
| **CI/CD** | CI on every PR; deploy on `main`; release on a `v*` tag |
| **Design system** | NSDS vendored at `f0dd883`; 1,779 selectors, 278 tokens available |
| **Icons** | 47 inline-SVG partials in `partials/icons/`, plus a generated 85-rule bridge |
| **Fonts** | Switzer + Roboto Mono, self-hosted, preloaded |
| **Templates** | `default`, `home`, `index`, `post`, `page`, `tag`, `author`, `error`, `error-404` |
| **Navbar** | `partials/navbar/` — bar, sheet, per-item icons, `-Label` dropdowns from Ghost Admin |
| **Footer** | `partials/footer/` — link columns, social row, newsletter, pinned to the bottom |
| **Homepage** | `home.hbs` — hero, what shipped, latest, follow, subscribe |
| **Reading surface** | `partials/post/article.hbs` — ported from `blog-post.html` |
| **Collections** | **none.** Eight specs waiting in `collections/` |

`npm run build` is green, `gscan` reports no issues, and the cascade contract
holds in both the development and production builds.

## Where the rest went

Moved to the root knowledge base at `Namaste Salesforce/abstract/`, because
none of it is a theme decision:

| was | now |
|---|---|
| `09-content-prompts.md` | `abstract/05-content/content-prompts.md` |
| `12-content-system.md` | `abstract/05-content/content-system.md` |
| `14-seed-content.md` | `abstract/05-content/seed-content.md` |
| `18-tag-registry.md` | `abstract/05-content/tag-registry.md` |
| `19-teaching-method.md` | `abstract/05-content/teaching-method.md` |
| `20-subscriptions-and-growth.md` | `abstract/06-growth/subscriptions-and-growth.md` |
| `decisions/0004-tag-vocabulary.md` | `abstract/05-content/decision-tag-vocabulary.md` |

**`tag-registry.md` is still canonical for every tag name used here.** The
theme reads that vocabulary; it does not own it.

Two files were deleted rather than moved — `08-scripts.md` and
`15-starting-from-zero.md` — because they described a build and a state that no
longer exist. Their accurate parts are in `06` and in this file; git has the
rest. `13-collections.md` was kept and is now `07-collections.md`: the Ghost
collections mechanics are theme knowledge, even though what each collection
*is* now lives in `collections/`.
