# Namaste Salesforce — full site context for an AI

Paste this file into any model that is about to write content, generate an
image, answer a question or change code for Namaste Salesforce. It is the
single briefing: what the product is, what it is built from, how a URL comes to
exist, what the design language allows, and — the part most people get wrong —
**which of the two websites a given thing belongs to**.

Everything here is written against the real repository. Where a rule has a
mechanism behind it, the mechanism is named, so you can check rather than
trust.

---

## 1. What this is

**Namaste Salesforce** is an open-source Salesforce learning platform for an
Indian-and-global audience of admins, developers and consultants. It teaches
Salesforce through structured courses, a free guided training track, reference
documentation, a blog and a resource library.

It is two products on two domains, sharing one audience, one brand and one
design system:

| | **www.namastesalesforce.com** | **app.namastesalesforce.com** |
|---|---|---|
| What | The public site: marketing, blog, docs, free training, course catalog | The LMS: enrolment, the course player, progress, accounts, admin |
| Runs on | **Ghost** (self-hosted) + this custom theme | **Next.js 16** (App Router) + **Payload CMS 3** + **Supabase** |
| Language | Handlebars `.hbs` | React 19 + TypeScript |
| Content edited in | Ghost Admin | Payload admin |
| Deployed | Ghost host | Vercel |
| Audience state | Ghost Members | Supabase auth accounts |

**They are not one database.** The bridge is Ghost's own APIs, and every line
of code that crosses it lives in the app's `src/lib/ghost/` — nothing else may
talk to Ghost directly. A new app account becomes a Ghost member (label
`app-account`); Ghost's `member.added` webhook creates the Supabase account
going the other way.

**Which surface does my thing belong to?**

- Teaching an idea in public, indexable by Google, free to read → **Ghost**.
- Anything gated, tracked, graded, enrolled in, or tied to a specific learner's
  progress → **the app**.
- A blog post → Ghost (the app *renders* Ghost's blog at `/blog` through the
  Content API, but Ghost remains the source of truth, and the canonical URL
  stays on `www` so the two domains never compete for the same search terms).

---

## 2. The Ghost site, concretely

### 2.1 Routing — how a URL comes to exist

`routes.yaml` lives **in Ghost Admin, not in this repo**. It defines
collections and permalinks. The rules it encodes are the thing to internalise,
because they are what makes a correctly-tagged post land at the right URL:

**Courses — a course and its lessons share one public tag.**

```
Course post   slug = "apex"        tags: [Apex, #course]     → /courses/apex/
Lesson post   slug = "apex-01-…"   tags: [Apex, #lesson]     → /courses/apex/apex-01-…/
                                          ↑ PRIMARY tag = the course tag
```

The course post's **slug must equal its course tag's slug**. The permalink uses
`{slug}` and lessons nest by `{primary_tag}` — that is the entire mechanism. Get
the slug wrong and the lesson 404s.

**Training — same trick, one level down.**

```
Section post  slug = "start"       tags: [Start Here, #training-section]   → /training/start/
Lesson post   slug = "start-01-…"  tags: [Start Here, #training-content]   → /training/start/start-01-…/
```

The section post's **slug must equal its section tag's slug**. There is no
`/training/` *post* — that route is a landing page listing the sections.

**Everything else**

| Content | Internal tag | Lands at |
|---|---|---|
| Blog article | `#blog` | `/blog/{slug}/` |
| Resource | `#resource` | `/resources/{slug}/` |
| Docs article | `documentation` | `/docs/{section}/{slug}/` |

**Order is `published_at` ascending, everywhere.** Lesson order within a course,
lesson order within a section, article order within a docs section, and the
section numbers on the training hero are all derived from publish date. To move
something earlier, **backdate it**. Nothing else controls sequence — there is no
manual order field.

**Tags beginning with `#` are Ghost internal tags.** They drive template
selection and must never be displayed to a reader.

### 2.2 Templates

> ⚠️ **The theme is currently a stack-free starter.** The implementation this
> section used to describe was deliberately reset — no build step, no CSS
> framework, no component library, because those decisions are being re-made
> explicitly. See `abstract/15`. **§1, §2.1 and §4–5 are unaffected**: the
> product, the URL model and the content rules are what they always were, and
> they are what you actually need in order to write content.

Today: `default.hbs` (the shell), `home.hbs`, `index.hbs`, `post.hbs`,
`page.hbs`, and two partials — `navigation.hbs` and `post-card.hbs`.

Reserved Ghost names: `index`, `post`, `page`, `tag`, `author`, `error`.

**`post.hbs` is a dispatcher, not a layout** — that shape is being kept. It
reads `{{#has tag="…"}}` and hands off to a partial per content type
(`post-course`, `post-lesson`, `post-blog`, … falling through to
`post-default`). A post that renders as `post-default` when it should not is the
usual symptom of a wrong tag. Branch order is load-bearing; see `abstract/02`.

### 2.3 Build

There isn't one. `assets/css/screen.css` is served as written.

```bash
npm test            # gscan — validate against Ghost's theme rules
npm run zip         # package for upload
```

"Testing" here means **gscan**, nothing else. There is no unit-test suite.

---

## 3. The design system

The design language is the **"Developer Console"** system. It is no longer
defined inside this theme: it lives in **`NS-Design-System`**, a separate
repository beside the Ghost install, and is **vendored** into both products —
`assets/css/ds/` here, `src/styles/ds/` + `src/components/ds/` in the app. That
is what stops the marketing site and the LMS from drifting apart.

**`NS-Design-System` is read-only from the consuming side.** Never edit a
vendored copy — it is regenerated by the sync and your change disappears.
Change the system in its own repo and re-sync. (The theme's vendored copy and
its sync script were removed in the reset; the system itself is untouched, and
§3 describes it, not the theme.)

### 3.1 The five rules

| Rule | What it means when you are writing or generating |
|---|---|
| **The hairline is the structure, not the shadow** | 1px borders separate things. Never ask for boxes, cards, drop shadows, glass or glow. |
| **Mono is the structural material** | Every index (`01`), duration, timestamp, status and kicker is set in the **mono face** (the platform's own console font — no mono webfont ships), uppercase and tracked, *by the theme*. Never type a fake kicker like `// Getting started` into body copy. |
| **One signal colour** | Brand blue `#0176D3` is the only colour that means "interactive". Nothing you write or draw should imply a second accent. |
| **Sharp, specific geometry** | 6px cards, 4px buttons; pills only for true tags. Never introduce your own radii. |
| **Motion is instant** | 120–180ms ease-out. No spring, no bounce, no translateY lift. Do not write copy promising animation. |

Dark mode is **brand navy**, not slate — `data-theme="light|dark"` on `<html>`,
stored in `localStorage` under `ns-theme`, applied by a pre-paint inline script
so there is no white flash. The same key is used by the app, so a reader keeps
their theme when crossing between the two domains.

### 3.2 Type

Two self-hosted variable cuts, both latin-subset — and no serif at all:

- **Switzer** — headings AND body (Fontshare / Indian Type Foundry). One
  grotesque across the whole range, separated by WEIGHT and SIZE rather than by
  face. Reading copy sets at **14px / weight 400**; Switzer's Regular is
  properly fitted and does not render grey the way the previous cut did, so
  there is no "Book" 450 step. Inline `<strong>` is 600, not 700.
- **Roboto Mono** — the label material. Every index, timestamp, duration,
  kicker, tag, status and `<pre>` runs through it. It IS shipped, and it has to
  be: that voice is on screen far more often than a code block is, and
  borrowing it from the OS meant the most-repeated register in the interface
  was SF Mono on a Mac, Consolas on Windows and a lottery on Linux — three
  different products, none of them chosen. Both faces are preloaded, because
  both are first-viewport text on essentially every route.
- **No serif ships.** The editorial register — pull-quotes, drop caps, section
  quotations — resolves to the platform's own serif (Georgia where it exists,
  Iowan/Times otherwise). It still reads as a quotation everywhere and costs
  zero bytes.

⚠️ TWO EARLIER STATES ARE STALE. If you find **Sentient** described as the
editorial serif, or a claim that **mono is the platform's own / not shipped**
and that mono column widths therefore differ per platform — that was true and
is not now. (Roboto Mono plus `font-variant-numeric: tabular-nums` means digit
columns DO align.) Older still: any mention of `N&M`, `nmtext`, `nmdisplay` or
weight 450 is the pre-Switzer era.

Switzer is under the Fontshare Free Font EULA (free for personal and commercial
use, self-hosting explicitly permitted); Roboto Mono is under the SIL Open Font
Licence 1.1. Both licences travel with the faces in `NS-Design-System/fonts/`.

### 3.3 Colour, exactly

| Role | Hex |
|---|---|
| Brand blue (the one signal colour) | `#0176D3` |
| Bright blue | `#1B96FF` |
| Sky | `#7CBEFF` |
| Pale blue | `#D8EDFF` |
| Blue wash | `#EEF6FF` |
| Deep navy | `#032D60` |
| Darkest navy | `#001A3E` |
| Success green | `#2E844A` — only for a "done" mark |
| Warning amber | `#FE9339` — at most one, as a single mark |
| Error | `#EA001E` |

Rule of thumb for any generated image: **near-white ground + blues + one ink.**
Green and amber appear at most once, as a single mark.

### 3.4 Icons

**Phosphor**, self-hosted and subsetted to the ~131 glyphs the products
actually reference, plus an SVG sprite (`namaste-icons.svg`) for brand marks.

A `ph-*` class that is not in the subset renders as a **blank box**. Adding one
means re-running the subsetter in `NS-Design-System` and re-syncing. Icons used
*inside post body copy* cannot be found by scanning templates, so they must be
added to that script's `CONTENT_SAFELIST` — which is why content prompts
restrict body copy to a small safelist of glyphs.

### 3.5 This theme ships no inline CSS

No `style="…"` attributes and no `<style>` blocks in any `.hbs`. Anything that
looks like it needs one (a cover image chosen by an editor, an AdSense `<ins>`)
has a class instead. Preserve that when editing templates.

---

## 4. Writing content — the short version

The long version is `00-house-style.md` plus the type prompt you need; this is
the orientation.

- **Bodies are plain semantic HTML.** `<h2>`/`<h3>` only — the table of contents
  is built from exactly those two levels, and hides itself under two headings.
  Start at `<h2>`; the post title is the `<h1>`.
- **Never add classes, inline styles or hand-built components to body copy.**
  The prose layer already styles it correctly.
- **Voice**: direct, second person, present tense. Lead with the useful
  sentence. Name the trade-off — the most valuable line in a Salesforce lesson
  is usually the one saying when *not* to do the thing. Concrete object names,
  real limits, real error messages. Short paragraphs. No emoji. British-neutral
  spelling, except Salesforce's own product names.
- **Never invent Salesforce facts.** If unsure of a limit or an API name,
  describe the behaviour without the number rather than guessing.
- Anti-patterns: "In today's fast-paced world", "Let's dive in",
  "Introduction"/"Conclusion" headings, bullets that restate the heading.

---

## 5. Generating images

Images are supporting illustration; the text is always the loudest thing on the
page. Flat vector, calm, reading-first.

**Always:** near-white or navy ground, the blue scale above, 1px hairline
outlines, rounded rectangles at ~12px, generous negative space, geometry over
realism. Recurring motifs that make images read as one family: a faint 48px
grid dissolving toward one edge; a dashed trail with dots as stops (the
training-roadmap metaphor); abstract UI panes with **grey placeholder bars, no
legible text**; circles, arrows, nodes, stacked cards.

**Never:** gradients on text, glassmorphism, glow, neon, 3D render sheen,
stock-photo realism, Salesforce's own branding or Astro/mascot characters, or
more than one accent colour.

**Text inside images:** prefer none — headings live in HTML. If a word is
unavoidable, one or two words in a geometric sans, semi-bold.

Common canvases: publication cover / OG `1200×630`, wide hero `2400×800`,
square `1024×1024`, YouTube thumbnail `1280×720`.

---

## 6. Things that will silently break

- A course or section post whose **slug does not equal its tag's slug** — the
  children 404.
- A lesson whose **primary tag** is not its parent course/section tag — it
  falls out of the collection.
- A **route in `routes.yaml` whose template does not exist** — Ghost answers
  `400 Missing template x.hbs`, not a fallback. The shipped `routes.yaml` is
  minimal for exactly this reason; add a route back with its template.
- Editing a vendored design-system copy — overwritten on the next sync. Change
  it in `NS-Design-System` and re-sync.
- Calling a Ghost helper across `../` inside a partial (e.g.
  `{{../url absolute="true"}}`) — Ghost throws and 500s the page. Use dotted
  access (`{{primary_tag.url}}`).
- A **new docs section** — it needs a route in `routes.yaml` and registering in
  whatever partial lists the sections. New courses, lessons, training content,
  blog posts and resources need no theme edit, by design.

---

## 7. Where to look in the repo

| You want | Read |
|---|---|
| Conventions and gotchas | `CLAUDE.md` |
| **Everything, ordered by what breaks if wrong** | **`abstract/00-README.md`** |
| The URL model, and the full target `routes.yaml` | `abstract/01-content-model.md` |
| Why `post.hbs` dispatches, and the branch order | `abstract/02-post-dispatcher.md` |
| What was removed and which decisions are open | `abstract/15-starting-from-zero.md` |
| How to rebuild the seed fixture | `abstract/14-seed-content.md` |
| The design system itself | `NS-Design-System/readme.md`, `docs/INTEGRATION.md` |
| Ghost ↔ app integration | the app's `ghost.md` |
