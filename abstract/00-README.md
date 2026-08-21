# abstract/ — everything you need to rebuild this theme from nothing

These files are ordered by **what breaks the site if you get it wrong**, not by
what is interesting. Read them in order. `01` is unrecoverable if wrong; `09`
is a preference.

| # | File | If you get this wrong |
| --- | --- | --- |
| 01 | `01-content-model.md` | Every URL on the site 404s or 301s to the wrong page |
| 02 | `02-post-dispatcher.md` | Every post renders as the wrong kind of page |
| 03 | `03-design-system.md` | The theme reimplements NSDS and the two products drift |
| 04 | `04-build-pipeline.md` | Nothing compiles, or compiles wrong and silently |
| 05 | `05-css-architecture.md` | The cascade inverts and NSDS stops applying |
| 06 | `06-ghost-glue.md` | Members, prose and editor cards break in ways tests miss |
| 07 | `07-performance.md` | Slow pages, layout shift, a white flash on every nav |
| 08 | `08-scripts.md` | The vendoring and the styleguide rot |
| 09 | `09-content-prompts.md` | Content stops matching the templates that render it |
| 10 | `10-how-this-went-wrong.md` | You repeat the mistakes this rebuild was needed for |

### Then — what to build, rather than how not to break it

| # | File | Answers |
| --- | --- | --- |
| 11 | `11-theme-roadmap.md` | What actually makes this a better Ghost theme, ranked by return per hour |
| 12 | `12-content-system.md` | One concept → lesson, video, blog, slides, LinkedIn — and the weekly rhythm |
| 13 | `13-collections.md` | Ghost collections, the learning graph, taxonomy hygiene |
| 14 | `14-seed-content.md` | How to rebuild the importable fixture you need before anything renders |

### And two about the work itself

| # | File | Answers |
| --- | --- | --- |
| 15 | `15-starting-from-zero.md` | What the theme is now, what was removed, and the decisions still open |
| 16 | `16-how-to-claude.md` | Working effectively with Claude Code — grounded in what happened here |

---

## The one-paragraph version

A Ghost theme for a Salesforce learning site. **Ghost owns the content model
through `routes.yaml` and tags; NSDS owns how everything looks; the theme is
the wiring between them and should be as thin as possible.** Almost every
mistake made building this came from the theme growing a third opinion — its
own components, its own tokens, its own drawer — that duplicated one of the
other two.

## The rule that would have prevented most of the rework

> Before writing a rule, a component or a script: check whether **Ghost**
> already supplies it, then whether **NSDS** already supplies it. The theme's
> job is only what neither can know about.

That check was skipped repeatedly, and the result was ~100 classes
reimplementing NSDS's training layer under different names, three copies of a
lesson row, two tables of contents, two share components and two post cards.
