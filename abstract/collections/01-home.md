# 01 · Home

> **STATUS: unspecified.** Nothing is built for this yet, and nothing should
> be until this file says what it is. Write in the blanks; delete the prompts
> as you answer them. `README.md` in this folder explains why the file comes
> first.

---

## 1 · What it is, in one paragraph

*What is this surface for, and who arrives at it? If you cannot say it without
naming another collection, the two may be one thing.*

**→**

## 2 · Who it is for, and what they do next

*The reader arrives from where — search, the nav, a link in a lesson? What is
the single action this page exists to make easy?*

**→**

## 3 · The URL model

*This is the expensive part. Changing it after publishing means 301-ing every
page under it. `01-content-model.md` has the mechanism; the tag names are
canonical in the root abstract's `05-content/tag-registry.md`.*

| | proposed | decided |
|---|---|---|
| mount path | `/` | **→** |
| permalink | `— (a page, not a collection)` | **→** |
| internal tag | `—` | **→** |
| routes.yaml filter | `—` | **→** |

**Is this collection paginated?** *(and at what page size — `posts_per_page`
is currently 12)*  **→**

**Does it get an RSS feed?**  **→**

## 4 · The listing page

*What does someone see at `/`? A grid of cards, a dense table, a
roadmap, a rail with filters? What is the sort order, and is it the same for a
signed-in member?*

**→**

**What does one item look like in the listing** — which fields are visible?
*(title, excerpt, cover, tag, date, reading time, duration, level, index
number, progress, price…)*

**→**

**What does it look like with nothing in it?**  **→**

## 5 · The single page

*What furniture does one of these carry? Table of contents, breadcrumb,
previous/next, a rail, an author box, related items, a share row, a CTA?*

**→**

**What is at the bottom** — what should the reader do when they finish?

**→**

## 6 · The NSDS archetype it ports

*Which file in `NS-Design-System/templates/` is this page? If none fits, say
which components it composes. **Do not design a new one here** —
`03-design-system.md` is why.*

| | |
|---|---|
| listing archetype | `homepage.html` + `sections-home.html` |
| single archetype | — |
| components it needs | **→** |
| behaviour script | `nav.js` |

## 7 · Members and access

*Free, members-only, paid, or mixed? If mixed, what does a signed-out reader
see — a preview, a locked card, nothing at all? Ghost's `{{#unless @member}}`
and `visibility` are the mechanism; the tier names live in the root abstract's
`06-growth/subscriptions-and-growth.md`.*

**→**

## 8 · What it is NOT

*The most useful section here. Name the neighbouring collection this one keeps
being confused with, and the line between them. Two collections that cannot be
told apart in one sentence should be one collection.*

**→**

## 9 · Open questions

*Anything you want to decide later. Something written here is a decision
deferred; something not written is a decision nobody knows is pending.*

- **→**

---

## Build checklist — do not start until §1–§8 are answered

- [ ] `routes.yaml` — collection block added, permalink and filter as decided above
- [ ] the tag exists in Ghost Admin and is in the root abstract's tag registry
- [ ] listing template ``home.hbs`` exists and is named in `routes.yaml`
- [ ] the dispatch branch in `post.hbs` (single pages) or none if this is pages-only
- [ ] the chrome dispatch in `default.hbs` — does this surface get the site bar?
- [ ] `npm run build` clean: classes defined, icons present, layers hold
- [ ] looked at, in both themes, at 360px, with JavaScript off
