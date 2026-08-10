# Prompt — a COURSE LESSON

> Paste `00-house-style.md` above this, then your brief.

You are producing a **lesson inside a course**, at
`/courses/{course-tag}/{lesson-slug}/`. This is the teaching. It is the page a
learner works through, so it has to be complete enough to act on and short
enough to finish.

Rendered by `partials/post-lesson.hbs` — the three-column lesson player: course
navigation with a progress bar on the left, the lesson in the middle, contents
rail on the right.

---

## Where it lands and what the theme builds around you

```
/courses/{course-tag}/{lesson-slug}/
```

| Region | Comes from |
| --- | --- |
| Left rail: course nav + % complete | generated from the course's lessons |
| Breadcrumb | theme |
| Type badge — "Video" or "Article" | `#lesson-type-video`, or its absence |
| Duration chip | `#video-duration-*`'s **description** for video lessons; **`reading_time`** (automatic) for articles |
| Access badge — "Free preview" / "Members" / "Free" | `#preview`, `#paid`, `#free` |
| `<h1>` | Title |
| Lede | **Excerpt** — if you omit it the page prints the literal words *"Article lesson"* |
| Video poster or feature image | Feature image |
| Members gate | post **Visibility** (+ `#preview` to let it through) |
| The lesson | **your body** |
| Prev / Next buttons | the sibling lessons, by publish date |
| "Finish course" on the last lesson | theme |
| Right rail: on-this-page | your `<h2>`/`<h3>`s |
| Discussion | Ghost comments |

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | The thing being taught, as a phrase. "Your first trigger", "Governor limits and bulk patterns", "Objects, fields and relationships". Not "Lesson 3" and not a question. |
| **Slug** | `{course-tag}-NN-{title-words}` — `apex-01-your-first-trigger`, `lwc-02-reactivity-and-the-wire-service`. The `NN` keeps the admin list readable and matches existing content; it does **not** control order. |
| **Excerpt** | **Mandatory.** One sentence, 15–30 words, saying what the reader will have done by the end. *"A tour of the platform: the clouds, the org, and where configuration ends and code begins."* |
| **Feature image** | For a video lesson this becomes the player poster — use a real frame. For an article, optional. |
| **Publish date** | **This is the lesson's position in the course.** Ascending. Space lessons an hour apart. |
| **Visibility** | `public` for free lessons. `members` or `paid` for gated ones. |

## Tags — exact, and in this order

```
TAGS: <Course Tag>, #lesson, [#lesson-type-video, #video-duration-…], [#free|#paid|#preview]
```

1. **The course tag** — public, first, identical to the parent course's tag.
   This is what nests the lesson under its course; get it wrong and the URL is
   wrong.
2. `#lesson` — required.
3. If it is a video: `#lesson-type-video` **and** one `#video-duration-*`
   (existing: `6m`, `9m`, `12m`, `18m`). Omit both for an article lesson —
   reading time is then computed automatically, so do not add a duration tag.
4. Access, at most one:
   - `#free` — badged "Free"
   - `#paid` — badged "Members"
   - `#preview` — badged "Free preview": a locked lesson deliberately left
     readable. Use on the second or third lesson of a paid course so a visitor
     can judge the teaching before paying.

`#video-duration-*` prints **its description** into the chip, so a new one must
be created with the bare value:

```
NEW TAGS TO CREATE:
  name: #video-duration-14m   slug: hash-video-duration-14m   description: 14m
```

### Gate and badge are two separate switches

The badge comes from the tag; the actual paywall comes from the post's
**Visibility**. They must agree:

| Intent | Visibility | Tag |
| --- | --- | --- |
| Anyone can read | `public` | `#free` |
| Members only | `members` | `#paid` |
| Paying members only | `paid` | `#paid` |
| Locked lesson, readable as a sample | `public` | `#preview` |

A `#paid` tag with `public` visibility badges a lock that does not exist. A
`paid` visibility with no tag gates the lesson with no explanation.

---

## Body — the lesson

Aim for **600–1,200 words** for an article lesson, or **250–500 words** of
supporting notes for a video lesson. One lesson teaches one thing.

**Required shape:**

```html
<h2>{The idea, stated}</h2>
<p>{Why this exists. 2–4 sentences. What problem it solves, in the org, in
   plain terms. No history lesson.}</p>

<h2>{The mechanics}</h2>
<p>{How it actually works. This is where a code block or a table belongs.}</p>
<pre><code class="language-apex">…</code></pre>
<p>{Read the snippet back in one or two sentences — what the important line
   does and why it is written that way.}</p>

<h2>{Doing it}</h2>
<ol>
  <li>{Numbered steps with real UI paths: "Setup → Object Manager → Account →
      Fields & Relationships → New".}</li>
</ol>

<h2>{Where it goes wrong}</h2>
<p>{The failure mode. The error message they will actually see. The limit they
   will actually hit. This section is why the lesson is worth more than the
   documentation.}</p>
```

Optional closer, one short paragraph — what the next lesson builds on this. Do
**not** write "Next up: …" with a link; the Next button is rendered for you.

### For a video lesson

The video is not embedded by you into the hero — put **one** embed in the body
and the theme moves it up into the player frame automatically (`training-video.js`
adopts the first YouTube, Vimeo or `<video>` it finds in `.gh-content`). Then
write the notes *underneath* it: the summary, the code shown on screen, and the
links. A video lesson with no text below it is a page with nothing to scan.

### Structure rules that matter here

- **Two `<h2>`s minimum** or the contents rail hides itself.
- Headings are statements: "Triggers fire once per batch, not once per record"
  beats "Trigger context".
- Every code block gets `class="language-…"` — `apex`, `soql`, `javascript`,
  `lwc`, `bash`, `json`, `html`. Snippets must be bulk-safe unless the point is
  that they are not, in which case say so in the sentence before.
- At most two `.ns-note` callouts, for the destructive step or the hard limit.

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Your first trigger
SLUG:         apex-01-your-first-trigger
EXCERPT:      Write a before-insert trigger, then find out why the platform runs
              it once for two hundred records instead of two hundred times.
TAGS:         Apex, #lesson, #lesson-type-video, #video-duration-9m, #free
VISIBILITY:   public
PUBLISH:      2026-08-05 09:00   (relative order: 1 of 3)
FEATURE IMAGE: The Developer Console with a trigger file open, navy chrome.
IMAGE ALT:    A trigger open in the Developer Console
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>A trigger is a hook, not a program</h2>
<p>A trigger runs when the platform saves a record, and it runs for the whole
  batch the platform happens to be saving — not once per record. Almost every
  Apex mistake in a first year comes from forgetting that second half.</p>

<h2>The smallest useful trigger</h2>
<pre><code class="language-apex">trigger AccountTrigger on Account (before insert) {
    for (Account a : Trigger.new) {
        if (String.isBlank(a.Industry)) {
            a.Industry = 'Unknown';
        }
    }
}</code></pre>
<p>No DML and no <code>update</code> call: in a <code>before</code> trigger the
  records in <code>Trigger.new</code> are still in memory, so assigning to a
  field is the save. Adding <code>update a;</code> here would be an error, not a
  belt-and-braces measure.</p>

<h2>Create it in your org</h2>
<ol>
  <li>Open the Developer Console: the gear menu, then Developer Console.</li>
  <li>File → New → Apex Trigger. Name it <code>AccountTrigger</code> and choose
    Account as the sObject.</li>
  <li>Paste the code above and save. Saving compiles it.</li>
  <li>Create an Account with no Industry and confirm it saves as Unknown.</li>
</ol>

<h2>Where it goes wrong</h2>
<p>Write the same logic with a query inside the loop and it works perfectly on
  one record and fails on a data load — <em>System.LimitException: Too many SOQL
  queries: 101</em>. The loop is fine. The query inside it is not, and the next
  lesson is about why.</p>

<div class="ns-note ns-note--warning">
  <i class="ph ph-warning ns-note__icon" aria-hidden="true"></i>
  <div class="ns-note__body">
    <p class="ns-note__title">One trigger per object</p>
    <p>A second trigger on Account will also fire, in an order you cannot
      control. Keep one per object and branch inside it.</p>
  </div>
</div>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] Course tag first, identical to the parent course's tag
- [ ] `#lesson` present
- [ ] Excerpt written — otherwise the lede reads "Article lesson"
- [ ] Video lesson → `#lesson-type-video` **and** a `#video-duration-*`;
      article lesson → **neither**
- [ ] Visibility and access tag agree (see the table)
- [ ] Publish date set to the intended position, spaced from its siblings
- [ ] Two or more `<h2>`s
- [ ] A "where it goes wrong" section exists
- [ ] Code is bulk-safe, and every block has a `language-*`
- [ ] No "Next up" link and no lesson-number heading in the body
