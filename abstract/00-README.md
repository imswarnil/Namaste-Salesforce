# abstract/ — everything you need to rebuild this theme from nothing

These files are ordered by **what breaks the site if you get it wrong**, not by
what is interesting. Read them in order. `01` is unrecoverable if wrong; `09`
is a preference.

**Read the status column first.** The theme was reset to a starter
([`decisions/0001`](decisions/0001-reset-to-a-starter.md)), and some of these
documents describe an implementation that no longer exists. They were kept
because they are accurate records of something that worked — but following one
as instructions will rebuild a stack nobody has chosen yet. Each carries a
banner saying so.

| # | File | Status | If you get this wrong |
| --- | --- | --- | --- |
| 01 | `01-content-model.md` | **current** | Every URL on the site 404s or 301s to the wrong page |
| 02 | `02-post-dispatcher.md` | **current** | Every post renders as the wrong kind of page |
| 03 | `03-design-system.md` | principle current, mechanism open | The theme reimplements NSDS and the two products drift |
| 04 | `04-build-pipeline.md` | *history* | Nothing compiles, or compiles wrong and silently |
| 05 | `05-css-architecture.md` | *layout history, layer contract current* | The cascade inverts and NSDS stops applying |
| 06 | `06-ghost-glue.md` | **current** | Members, prose and editor cards break in ways tests miss |
| 07 | `07-performance.md` | *history; reasoning current* | Slow pages, layout shift, a white flash on every nav |
| 08 | `08-scripts.md` | *history* | The vendoring and the styleguide rot |
| 09 | `09-content-prompts.md` | **current** | Content stops matching the templates that render it |
| 10 | `10-how-this-went-wrong.md` | **current** | You repeat the mistakes this rebuild was needed for |

### Then — what to build, rather than how not to break it

| # | File | Answers |
| --- | --- | --- |
| 11 | `11-theme-roadmap.md` | What actually makes this a better Ghost theme, ranked by return per hour |
| 12 | `12-content-system.md` | One concept → lesson, video, blog, slides, LinkedIn — and the weekly rhythm |
| 13 | `13-collections.md` | Ghost collections, the learning graph, taxonomy hygiene |
| 14 | `14-seed-content.md` | How to rebuild the importable fixture you need before anything renders |
| 17 | `17-consuming-the-design-system.md` | What NSDS actually is, measured — and whether you need Tailwind to use it (**you do not**) |

### And two about the work itself

| # | File | Answers |
| --- | --- | --- |
| 15 | `15-starting-from-zero.md` | What the theme is now, what was removed, and the decisions still open |
| 16 | `16-how-to-claude.md` | Working effectively with Claude Code — grounded in what happened here |

### [`decisions/`](decisions/) — the decision record

One file per choice that is expensive to reverse, with its reasoning, its
downside and the trigger that should reopen it. **This folder exists because the
last stack was never actually decided** — it accumulated one reasonable commit
at a time, which is why `10` had to be written.

| # | Decision | Status |
| --- | --- | --- |
| [0001](decisions/0001-reset-to-a-starter.md) | Reset the theme to a stack-free starter | Accepted |
| [0002](decisions/0002-css-strategy.md) | How the theme gets its CSS | **Open — gates all styling work** |
| [0003](decisions/0003-routes-yaml-minimal.md) | `routes.yaml` names only servable templates | Accepted |

---

## The one-paragraph version

A Ghost theme for a Salesforce learning site. **Ghost owns the content model
through `routes.yaml` and tags; NSDS owns how everything looks; the theme is
the wiring between them and should be as thin as possible.** It is currently a
stack-free starter — the wiring exists, the pages do not yet. Almost every
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
