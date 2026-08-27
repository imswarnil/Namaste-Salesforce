# abstract/ — how to build and grow this theme

Nine documents and a folder of surface specs. Ordered by **what breaks the
site if you get it wrong**, not by what is interesting.

> **Ghost owns the content model. NSDS owns how everything looks. The theme is
> the wiring, and stays thin.**
>
> Before writing a rule, a component or a script: check whether **Ghost**
> supplies it, then whether **NSDS** supplies it. The theme's job is only what
> neither can know about.

That check was skipped repeatedly and cost ~100 duplicated classes, three
copies of a lesson row, two tables of contents and two post cards
([`09`](09-lessons.md)). It was skipped again recently in one line of CSS,
which flattened every control in the navbar to the wrong height.

---

## The documents

| # | | If you get it wrong |
|---|---|---|
| [01](01-content-model.md) | **Content model** — tags, `routes.yaml`, URLs, collections | Every URL 404s or 301s to the wrong page |
| [02](02-templates.md) | **Templates** — the post dispatcher, the partial tree | Every post renders as the wrong kind of page |
| [03](03-design-system.md) | **NSDS** — what it is, how to port an archetype | The theme reimplements it and the two products drift |
| [04](04-css.md) | **CSS** — the cascade contract, how to write a rule | Overrides stop working, silently |
| [05](05-assets.md) | **Assets** — fonts, icons, images | Fonts flash, icons render as empty space |
| [06](06-discoverability.md) | **Structured data, feeds, LLM-readability** | The site is invisible to search and to models |
| [07](07-build-and-ci.md) | **Build and CI** — gulp, the checks, deploy | You ship the CSS from before the fix |
| [08](08-ghost.md) | **Ghost** — helpers, Members, Koenig, performance | Things break in ways tests miss |
| [09](09-lessons.md) | **What went wrong last time** | You repeat it |

## [`collections.md`](collections.md) — **the next thing to do**

One file per page family, six questions each. **All eight are unanswered**,
and no collection gets built before its file is. That folder is where the
remaining work is defined; everything else here is the foundation it sits on.

---

## Adding a page family — the whole procedure

This is the loop the site scales through. It has not changed since the theme
was rebuilt, and every step exists because skipping it cost something.

**1 · Decide the surface.** Answer the six questions in
`collections.md`. Question 1 first — "what is it NOT" — because that is
what catches two collections that are really one.

**2 · Settle the URL.** Question 3. The only irreversible part: a published
permalink cannot move without 301s and lost ranking. Nothing below matters if
this is wrong.

**3 · Find the archetype.** `ls ../../../../NS-Design-System/templates/` — 57
of them. If one fits, the page is a **port**, not a design. If none fits,
compose from existing `.ns-*` components; if that fails too, the component
probably belongs upstream in NSDS rather than here ([`03`](03-design-system.md)).

**4 · Port it.** Copy into `partials/`, rename to `.hbs`, swap the marked
slots for Ghost helpers, replace inline `style` with utilities, swap
`<i class="ph ph-x">` for `{{> "icons/x"}}`. **Do not rename a class on the
way through.**

**5 · Wire the routing.** A collection block in `routes.yaml`, a branch in
`post.hbs` delegating to one partial, and a decision in `default.hbs` about
whether the surface gets the site bar.

**6 · Say what it is.** Structured data for the kind — [`06`](06-discoverability.md)
§2. `Article` is Ghost's default and is rarely the right answer for a learning
site.

**7 · Build.** `npm run build` runs six checks. Undefined classes, missing
icons, a stale icon bridge, an inverted cascade and unresolvable asset urls
are all things that otherwise ship green.

**8 · Look at it.** In both themes, at 360px, with JavaScript off. gscan and a
green build have both been green on a visually broken site more than once.

---

## Toward a complete NSDS theme

NSDS ships **57 archetypes**; this theme currently renders a handful. A
"complete" theme is not all 57 — the LMS surfaces (player, admin, AI, decks)
belong to the Next.js app and a Ghost page never renders them. What is left is
roughly this, in the order that compounds fastest:

| Surface | Archetype | Blocked on |
|---|---|---|
| Blog listing + post | `blog-listing`, `blog-post` | `collections.md` §02 |
| Tag index + tag page | `tag-index`, `tag-page` | nothing — could be built now |
| Course listing + detail | `course-listing`, `course-detail` | `collections.md` §03 |
| Lesson reading surface | `course-player-article` | `collections.md` §03 |
| Training index + module | `training-index`, `training-module` | `collections.md` §04 |
| Docs tree + page | compose `.ns-sidenav` + `.ns-tree` | `collections.md` §05 |
| Sign-in / sign-up | `signin-form`, `signup-form` | nothing |
| Account / membership | `account` | nothing |
| Search results | Ghost's Sodo Search owns this | nothing to build |
| Error pages | `error-page` | **done** |
| Homepage bands | `homepage`, `sections-home` | **done** (two bands dummy) |
| Navbar + sheet + footer | `navbar`, `footer` | **done** |

**The two unblocked ones are the cheapest real progress available**: the tag
pages and the members surfaces need no collection decision, and both are
straight ports.

Weight is the other half of "complete". The bundle still ships every LMS
surface — `player.css`, `ai.css`, `deck.css`, `admin.css`, `auth.css`,
`helpdesk.css` are ~200 KB a Ghost page never renders. `components/css/` is a
flat list of imports, so cherry-picking is already supported — **after** the
theme renders correctly, never before ([`03`](03-design-system.md)).

---

## What exists right now

| | |
|---|---|
| Build | gulp + Tailwind v4 + cssnano → `assets/built/`, committed |
| Checks | layers, classes, icons, icon bridge, asset urls, inline styles, comments, gscan |
| CI/CD | CI on every PR, deploy on `main`, release on a `v*` tag |
| NSDS | vendored at `f0dd883` — 1,822 selectors, 278 tokens |
| Templates | `default`, `home`, `index`, `post`, `page`, `tag`, `author`, `error`, `error-404` |
| Partials | `navbar/`, `footer/`, `home/`, `post/`, `icons/`, `components/` |
| Structured data | `SiteNavigationElement`, plus everything `{{ghost_head}}` emits |
| Collections | **none** — eight specs waiting |

## Where the rest of the knowledge lives

Content strategy, the tag registry, the teaching method and pricing are **not
here**. They live in the root knowledge base at `Namaste Salesforce/abstract/`,
because they are shared with the Next.js LMS and the content pipeline. The tag
registry is canonical for every tag name this theme's URL model depends on.

`CLAUDE.md` at the theme root is this same material compressed for Claude Code,
plus the full NSDS reference.
