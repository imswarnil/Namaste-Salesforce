# Prompt — a COURSE

> Paste `00-house-style.md` above this, then your brief.

You are producing a **course** for Namaste Salesforce: the landing page a
learner arrives at before starting, at `/courses/{course-tag}/`. A course post
is not a lesson and contains no teaching. It is the page that answers *should I
spend six hours on this?*

Rendered by `partials/post-course.hbs`.

---

## Where it lands and what the theme builds around you

```
/courses/{course-tag}/
```

The page is assembled from your fields and tags. You are not writing the layout:

| Region | Comes from |
| --- | --- |
| Navy hero, grid pattern, breadcrumb | theme |
| Level badge · "Featured" badge · Free/Members price tag | `#level-*`, the Featured flag, `#free`/`#paid` |
| `<h1>` | Title |
| Hero lede | **Excerpt** (falls back to the first 30 words of the body) |
| Three stats: Lessons · Duration · Access | lesson count is **counted automatically**; Duration is the `#duration-*` tag's *description*; Access is always "Self-paced" |
| Instructor name + avatar | the Ghost author |
| "Start course" button | auto-links the earliest-published lesson |
| Hero image (desktop) | Feature image, unless `#hide-image` |
| **"About this course"** | **your body** |
| Course curriculum list | generated from the lessons — you do not write it |
| Members lock notice | `#paid` |
| Sticky enrolment sidebar ("This course includes…") | lesson count, duration tag, level tag, updated date |
| Mobile sticky CTA bar | theme |

**Do not write** a lesson list, a "what you'll learn" duration table, a price, an
instructor bio, or a curriculum — every one of those is rendered for you and
duplicating it in the body produces the same information twice on one page.

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | The course's real name. 2–6 words. "Apex Programming", "Salesforce Admin Foundations". Not "The Complete Guide To…". |
| **Slug** | **Must equal the course tag's slug.** `apex`, `lwc`, `admin-foundations`. Short — it is a URL segment every lesson nests under. |
| **Excerpt** | The hero lede. 15–30 words, one sentence, states the ground covered and who it is for. *"Objects, fields, users and security — the groundwork every Salesforce career is built on."* |
| **Feature image** | 4:3 works best (the hero renders it at `aspect-[4/3]`). Optional. |
| **Publish date** | Any. Course order in the catalog is by date. |
| **Featured** | Only for the one or two courses you want badged on the catalog. |
| **Visibility** | `public` on the course page itself, even for a paid course — the *lessons* carry the gate, and a hidden course page cannot sell anything. |

## Tags — exact, and in this order

```
TAGS: <Course Name>, #course, #level-…, #free|#paid, #duration-…, [#hero-N], [#hide-image]
```

1. **The course tag** (public, first — this is `primary_tag`, and every lesson
   will carry it too). Name it as a title: `Apex`, `LWC`,
   `Admin Foundations`. Its slug must equal the course post's slug.
2. `#course` — required. This is what routes it.
3. Exactly one level: `#level-beginner` · `#level-intermediate` ·
   `#level-advanced`.
4. Exactly one access tag: `#free` or `#paid`.
5. One `#duration-*` — the total length of the course.
6. Optional hero variant: `#hero-1` (default, media right) · `#hero-2`
   (centred, no media) · `#hero-3` (image-forward) · `#hero-4` · `#hero-5`
   (turns the hero image into a play poster linking the first video lesson).
   Omit for `#hero-1`.
7. Optional `#hide-image` — suppresses the hero and sidebar image.

### Duration tags carry their value in the description

`#duration-*` renders **its description**, verbatim, into the "Duration" stat and
into "*N* of content" in the sidebar. If the tag you need does not exist, create
it with the description set to the bare display value:

```
NEW TAGS TO CREATE:
  name: #duration-4h   slug: hash-duration-4h   description: 4h
```

Not `Total length: 4h.` — that renders literally as *"Total length: 4h."* in the
stat. Existing tags: `#duration-45m`, `#duration-1h30m`, `#duration-3h`,
`#duration-6h`, `#duration-9h`. (`#hero-4`, `#hero-5` and `#hide-image` are
supported by the template but may not exist in Ghost yet — create them as
internal tags with a one-line description if you use them.)

---

## Body — "About this course"

Three to five short sections. This is a decision document, so every heading
should help someone decide.

**Required shape:**

```html
<h2>{A statement of what this course is actually about}</h2>
<p>{2–4 sentences. The premise. What ground it covers and in what order.
   Name the one thing that makes this course different from a docs page.}</p>

<h3>What you'll be able to do</h3>
<ul>
  <li>{An outcome, phrased as a capability — "Read an org's schema and explain
      how its objects relate"}</li>
  <li>{3–5 of these. Each one a thing they can DO, not a thing they will
      "understand" or "learn about".}</li>
</ul>

<h3>Who this is for</h3>
<p>{Name the reader. Also name who should skip it and what they should read
   instead — this is the most trusted paragraph on the page.}</p>

<h3>Before you start</h3>
<p>{Prerequisites, concretely: a free Developer org, a completed course,
   comfort with a concept. "None — this assumes no prior experience" is a
   perfectly good answer, and worth saying outright.}</p>
```

Optional, when the course warrants it:

```html
<h3>How the course is structured</h3>
<p>{The shape of the progression — not a lesson list. "Three passes over the
   same org: first the data model, then who can see it, then how to change it
   safely."}</p>
```

### Two Ghost cards behave specially on course pages

- A **toggle card** renders as an **FAQ accordion**. Use two to five at the end
  of the body for real objections: *"Do I need a paid org?"*, *"Is this current
  with the latest release?"*, *"How long will this actually take me?"*
- A **product card** renders as a **testimonial**. Use only with a real quote.

Both are styled in `2-components/site-course.css` and only look right inside a
course body. Insert them as Ghost cards, not hand-written HTML.

---

## Length

400–700 words in the body. A course page longer than that is competing with its
own curriculum list for attention.

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Apex Programming
SLUG:         apex
EXCERPT:      Triggers, governor limits and tests — writing Apex that survives
              contact with a real org and a real data volume.
TAGS:         Apex, #course, #level-intermediate, #paid, #hero-3, #duration-6h
VISIBILITY:   public
PUBLISH:      2026-08-04 09:00
FEATURE IMAGE: A Developer Console editor pane on navy, one Apex class open,
               shot at a slight angle. 4:3.
IMAGE ALT:    An Apex class open in the Salesforce Developer Console
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>Apex is the tool you reach for last, and it has to be right</h2>
<p>Most requirements on the platform should never become code. The ones that
  genuinely should are the ones where getting it wrong is expensive: bulk data
  loads, integrations, anything that has to be tested. This course covers those,
  in the order they bite — triggers first, then the limits that punish naive
  triggers, then the tests that stop the punishment reaching production.</p>

<h3>What you'll be able to do</h3>
<ul>
  <li>Write a trigger that behaves correctly on a 200-record batch</li>
  <li>Predict which governor limit a given piece of logic will hit first</li>
  <li>Move queries and DML out of loops without restructuring the whole class</li>
  <li>Write a test that fails for the right reason</li>
</ul>

<h3>Who this is for</h3>
<p>Admins who already build with Flow and have hit something Flow cannot do, and
  developers arriving from another language who need the platform's constraints
  rather than its syntax. If you have never configured an object, start with
  Admin Foundations — Apex assumes you can read a schema.</p>

<h3>Before you start</h3>
<p>A free Developer org, which takes about two minutes to create. Nothing is
  installed locally until the last section, and nothing here touches a
  production org.</p>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] **Slug equals the course tag's slug** — the single most common breakage
- [ ] Course tag is first in `TAGS`, before `#course`
- [ ] Exactly one `#level-*`, one of `#free`/`#paid`, one `#duration-*`
- [ ] Any new `#duration-*` tag's description is the bare value (`4h`)
- [ ] Body contains no lesson list, no price, no instructor bio, no duration table
- [ ] "Who this is for" names who should *skip* it
- [ ] Outcomes are capabilities, not "understand X"
- [ ] Course page visibility is `public` even when the course is `#paid`
