# Prompt — a TRAINING SECTION

> Paste `00-house-style.md` above this, then your brief.

You are producing a **training section** — one stage of the site's single
guided training, at `/training/{section}/`. The training is one ordered path
from nothing to competent; a section is a leg of it. Its post body is the
section's **overview**: what this leg covers, what it assumes, and what you can
do when you finish it.

Rendered by `partials/post-training-section.hbs`.

---

## How training differs from courses

Courses are a catalog — a learner picks one. **Training is a single ordered
path** and a section's whole meaning is its position in that path. So a section
overview must be written as a leg of a journey, not as a standalone topic page:
it should say what came before and what this unlocks.

```
/training/            the landing page listing every section   (no post backs it)
/training/start/      section post, slug "start", tag "Start Here"
/training/start/…/    its lessons
```

## Where it lands and what the theme builds around you

| Region | Comes from |
| --- | --- |
| Hero band, dot pattern | theme |
| **A giant section number set as the hero's ground** | **counted from publish dates** — see below |
| Atmospheric bleed image behind the hero | the **section tag's** feature image, else the post's |
| Breadcrumb: Home › Training › {section} | theme |
| `<h1>` | Title |
| Hero sub-line | **Excerpt** |
| "N lessons" stat | counted from the section's lessons |
| "Start this section" button | auto-links the earliest-published lesson |
| Section rail (all sections + their lessons) | generated |
| **Overview prose** | **your body** |
| The lesson list, with type icons and lock state | generated — do not write it |
| "On to the next section" | generated |

### The section number is derived, not authored

The hero's number is a count of `#training-section` posts published **on or
before** this one. So `published_at` alone decides both the order of the
sections and the digit drawn on the hero. There is no numbering field, and
putting "Section 2" in the title would double it.

**Always state the intended position** in your output, and set the date to
match. To insert a section between two existing ones, backdate it between them.

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | The stage, as a place you arrive at. Existing: "Start Here", "Build Your First App", "Automate the Work". Imperative or noun-phrase, 2–4 words. Never a number. |
| **Slug** | **Must equal the section tag's slug.** One short word where possible: `start`, `build`, `automate`. This is a URL segment every lesson nests under. |
| **Excerpt** | The hero sub-line. 15–30 words. Say what this leg does *to the reader*, in sequence. *"Your first object, its fields, and a report that proves the data is really there."* |
| **Feature image** | Prefer setting it on the **tag** instead — the theme looks at `primary_tag.feature_image` first, and uses it as an atmospheric bleed, blended into the trailing edge. It must survive being tinted and cropped: texture, not information. Never a diagram, never text. |
| **Publish date** | **The section's position and its hero number.** |
| **Visibility** | `public`. A section overview is a signpost; gating it hides the path. |

## Tags — exact, and in this order

```
TAGS: <Section Name>, #training-section
```

That is the whole set. Two tags.

1. **The section tag** — public, first. Its slug **must** equal the post slug.
2. `#training-section` — required, and it is what makes the router treat this as
   an overview rather than a lesson. (`post.hbs` tests it *before*
   `#training-content`, so never put both on one post.)

Do not add level, duration or access tags — the section hero has no slots for
them.

```
NEW TAGS TO CREATE:
  name: Automate the Work   slug: automate   description: Automate the Work — training
    section tag. The section post and all its lessons carry this tag.
  (set a feature image on this tag if you have one)
```

---

## Body — the section overview

**250–450 words.** Short. The reader is standing at a signpost, not reading a
chapter.

**Required shape:**

```html
<h2>{What this leg of the training actually does}</h2>
<p>{2–4 sentences. The premise of the section. Where the reader is standing now
   and where they will be standing at the end of it. Reference the previous
   section by name if there is one.}</p>

<h3>What you'll build</h3>
<p>{The concrete artefact. Training sections should produce something that
   exists in the reader's org — an object, a flow, a report. Name it.}</p>

<h3>What this assumes</h3>
<p>{Either the previous section by name, or "nothing" said plainly. A guided
   path earns trust by being explicit about its own prerequisites.}</p>

<h3>When you're done</h3>
<ul>
  <li>{2–4 capabilities, each a thing they can do unaided}</li>
</ul>
```

**Do not** list the lessons. The lesson list is rendered directly below your
prose, with type icons, durations and lock states. Writing it again is the single
most common mistake on this page type.

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Build Your First App
SLUG:         build
EXCERPT:      Your first custom object, the fields that earn their place on it,
              and a report that proves the data is really there.
TAGS:         Build, #training-section
VISIBILITY:   public
PUBLISH:      2026-08-08 09:00   (section 2 of 3 — after "Start Here",
                                  before "Automate the Work")
FEATURE IMAGE: Set on the TAG. Abstract navy field with a faint schema-line
               texture. No text, no diagram — it gets tinted and cropped.
IMAGE ALT:    (decorative — the theme renders it aria-hidden)
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>Configuration is the platform, not a shortcut around it</h2>
<p>Start Here got you an org and a vocabulary. This section spends it: you build
  a small application out of nothing but configuration, and you finish with
  something a real user could open. No code appears in this section, and that is
  not a simplification — most of what ships on Salesforce is built exactly this
  way.</p>

<h3>What you'll build</h3>
<p>A <strong>Project</strong> object with the handful of fields a project
  actually needs, a page layout that puts them in a sensible order, a list view
  your future self can scan, and a report that counts them. Roughly ninety
  minutes of work in your Developer org.</p>

<h3>What this assumes</h3>
<p>Start Here, and nothing else. You need a Developer org you can log into and a
  rough idea of what an object is. If either of those is shaky, that section is
  twenty minutes and it will save you an hour here.</p>

<h3>When you're done</h3>
<ul>
  <li>Create a custom object and explain why each of its fields exists</li>
  <li>Choose between a formula field and a stored value</li>
  <li>Lay out a record page so the important field is the first one read</li>
  <li>Build a report that answers a question someone actually asked</li>
</ul>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] **Post slug equals the section tag's slug**
- [ ] Exactly two tags: the public section tag first, then `#training-section`
- [ ] `#training-content` is **not** also present
- [ ] Publish date set to the section's intended position, and the position
      stated in the output
- [ ] Title carries no number
- [ ] Body does **not** list the lessons
- [ ] "What this assumes" names the previous section, or says "nothing"
- [ ] Visibility is `public`
- [ ] Feature image is texture, not a diagram — and ideally set on the tag
