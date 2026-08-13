# House style — read this first

Shared contract for every piece of content on Namaste Salesforce. Paste this
above whichever type prompt you are using.

Namaste Salesforce is an open-source Salesforce learning site built on Ghost.
Its design language is the **"Developer Console"** system. You are writing
content that will be rendered by that system — so most of the visual work is
already done for you, and your job is to supply *correctly structured* prose and
*correctly tagged* metadata, and then get out of the way.

---

## 1. The five design rules (and why they constrain your writing)

| Rule | What it means for you |
| --- | --- |
| **The hairline is the structure, not the shadow** | Borders separate things. Do not describe or request boxes, cards, shadows or panels in body copy — the theme decides those. |
| **Monospace is structural** | Every index (`01`), duration, timestamp, status and kicker is set in N&M Mono *by the theme*. Never type a fake kicker like `// Getting started` into the body. |
| **One signal color** | Brand blue `#0176D3` means "interactive". Nothing you write should imply another accent colour, and nothing should be coloured by hand. |
| **Sharp, specific geometry** | 6px cards, 4px buttons, pills only for true tags. Not your concern — but do not add your own radii or classes. |
| **Motion is instant** | 120–180ms ease-out. Do not write copy that promises animation. |

The practical consequence: **the body of a post is plain semantic HTML.** The
theme's prose layer styles it. Every time you add a class, an inline style or a
hand-built "component" into body copy, you are fighting a system that was
already going to render it correctly.

---

## 2. Voice

Write the way this repo's own comments are written: direct, specific, and
willing to say what something is *not*.

- **Lead with the useful sentence.** No "In today's fast-paced world". No "Let's
  dive in". No throat-clearing before the first idea.
- **Second person, present tense.** "You create the object, then add the
  fields." Not "The user should then proceed to create".
- **Name the trade-off.** The most valuable line in a Salesforce lesson is
  usually the one that says when *not* to do the thing. Include it.
- **Concrete over abstract.** Object names, field names, real limits, real error
  messages. "SOQL 101 error" beats "performance issues".
- **British-neutral spelling**, matching the existing content ("behaviour",
  "organisation") — except Salesforce's own product names and API terms, which
  keep their official spelling (`Organization-Wide Defaults`, `Authorize`).
- **Short paragraphs.** Two to four sentences. This renders on phones.
- **No emoji.** No exclamation marks in body copy.
- **Never invent Salesforce facts.** Limits, API names and UI paths must be
  real. If you are unsure of a number, describe the behaviour without the
  number rather than guessing one.

Anti-patterns that read as filler here: "Introduction" / "Conclusion" headings,
"In this article we will learn", bulleted lists that restate the heading, and
summaries that repeat what was just said.

---

## 3. Body markup — what to emit

Bodies are authored as HTML (in Ghost, an **HTML card**, or normal Koenig
blocks). Emit only this vocabulary:

```html
<h2>   <h3>   <p>   <ul><li>   <ol><li>   <strong>   <em>   <code>
<a href="…">   <blockquote>   <table><thead><tbody><tr><th><td>
<pre><code class="language-apex">…</code></pre>
<figure><img src="…" alt="…"><figcaption>…</figcaption></figure>
```

**Rules:**

- **Start at `<h2>`.** The post title is the page's `<h1>`. A second `<h1>` in
  the body breaks the document outline.
- **`<h2>` and `<h3>` only.** The table of contents is built from exactly those
  two levels, `<h3>` indented under `<h2>`. `<h4>` and deeper are invisible to
  it. If you need a fourth level, you need a different structure.
- **Two headings minimum for a TOC.** The contents rail hides itself on posts
  with fewer than two headings. Any post long enough to want one needs at least
  two `<h2>`s.
- **Headings are statements, not labels.** "Governor limits are per-transaction,
  not per-record" is a heading. "Governor limits" is a filing category.
- **No classes, no inline styles, no `<div>`s, no `<span>`s** in body copy. No
  Tailwind utilities. No `ns-*` classes — those are the theme's, and hand-typing
  them into content couples your article to CSS it does not own. **One
  exception: the callout** (`.ns-note`), below.
- **Every image needs real `alt` text.** Describe what it shows, not "screenshot".
- **Tables need a `<thead>`.** They are styled as data tables and read badly
  without a header row.

## 4. Code blocks

Set the language, always. The theme wraps every `<pre><code>` in
`.gh-content` in a Developer-Console window — navy bar, language tab, copy
button — and highlights it with a built-in tokeniser. **The language string you
give is printed verbatim on the window's tab**, so `apex` shows "apex".

Languages the highlighter actually knows:

| Write | Highlights as |
| --- | --- |
| `apex`, `cls`, `trigger` | Apex |
| `soql`, `sql` | SOQL / SQL (`--` comments) |
| `javascript`, `js`, `ts`, `typescript`, `lwc` | JavaScript / TypeScript |
| `json` | JSON |
| `bash`, `sh`, `shell`, `console` | Shell (`#` comments) |
| `css` | CSS |
| `html`, `xml`, `markup`, `svg`, `hbs`, `handlebars`, `vue` | Markup (tag-aware) |

Anything else falls back to a generic keyword set — it still renders, still gets
a tab and a copy button, just with duller highlighting. Prefer a name from the
table.

```html
<pre><code class="language-apex">trigger AccountTrigger on Account (before insert) {
    AccountService.applyDefaults(Trigger.new);
}</code></pre>
```

**Code should be runnable and bulk-safe.** No `…` placeholders mid-statement, no
single-record assumptions in trigger examples, no `SELECT` inside a `for` loop
unless the point of the snippet is that it is wrong (say so if it is).

## 4a. The callout — the one component you may hand-write

`.ns-note` is the system's inline callout, and the only place the design system
permits a colour tint (held at 4–6%, with the colour carried by the border and
the icon). Use it for the thing a reader must not miss — a governor limit, a
destructive step, a prerequisite. Exact markup:

```html
<div class="ns-note ns-note--warning">
  <i class="ph ph-warning ns-note__icon" aria-hidden="true"></i>
  <div class="ns-note__body">
    <p class="ns-note__title">This deletes data</p>
    <p>Removing a field removes its values. There is no undo in production.</p>
  </div>
</div>
```

Three classes on the icon, all three required: `ph` (the font family — see §5),
`ph-warning` (the glyph), and `ns-note__icon` (which is what picks up the tone
colour; without it the icon stays brand blue inside a red callout).

Tones: default (brand), `--info`, `--success`, `--warning`, `--danger`,
`--neutral`. Sizes: `--sm`, `--lg`. Pair the tone with a sensible safelisted
glyph — `ph-info`, `ph-lightbulb`, `ph-check-circle`, `ph-warning`,
`ph-warning-circle`, `ph-x-circle`.

**At most two per article.** A page of callouts is a page with no emphasis. If
the whole lesson is a warning, that belongs in the excerpt.

## 5. Icons inside body copy

Phosphor is **self-hosted and subsetted** — only glyphs the theme already uses
are shipped. An icon you invent renders as a blank box.

Safe inside post content — these sixteen only:

```
ph-info            ph-warning        ph-warning-circle   ph-check-circle
ph-x-circle        ph-lightbulb      ph-note             ph-bookmark-simple
ph-code            ph-terminal-window ph-database        ph-cloud
ph-lightning       ph-rocket-launch  ph-star             ph-question
```

**Two classes, always:** a weight class *and* a glyph class. The CSS rules are
written `.ph.ph-info` and `.ph-fill.ph-info`, so a glyph class on its own renders
nothing at all:

```html
<i class="ph ph-info" aria-hidden="true"></i>        <!-- outline -->
<i class="ph-fill ph-info" aria-hidden="true"></i>   <!-- filled -->
<i class="ph-info" aria-hidden="true"></i>           <!-- ✗ renders nothing -->
```

All sixteen are shipped in both weights. That list exists for
exactly one purpose: the callout above. Anything else requires adding the glyph
to `CONTENT_SAFELIST` in `scripts/subset-icons.py` and re-running it — a code
change, not a content change. **Outside a callout, use no icons.** The theme
supplies its own everywhere it wants them.

## 6. Fields, and what they actually do

| Ghost field | Where it surfaces | Rules |
| --- | --- | --- |
| **Title** | the `<h1>` | 4–9 words. No trailing punctuation. Sentence case with product names capitalised. |
| **Slug** | the URL | lowercase, hyphens, no stop-words padding. Type prompts give the per-type convention. |
| **Excerpt** (`custom_excerpt`) | the lede paragraph under the `<h1>`, plus cards and search results | **Always write one.** 15–30 words, one sentence, no full stop needed if it reads as a standfirst. It is not a summary of the article — it is the reason to read it. |
| **Feature image** | hero / poster / card art | 16:9 or 4:3, ≥1600px wide. Optional everywhere. |
| **Feature image alt** | accessibility, and the `alt` on blog/docs/resource images | Write it whenever you set a feature image. |
| **Publish date** | **ordering**, everywhere | See below. |
| **Visibility** | the members gate | `public`, `members`, `paid`, or specific tiers. Drives the lock panel. |
| **Featured** | a "Featured" badge on courses | Use sparingly. |
| **Tags** | routing, layout, badges, filters | Order matters. See each type prompt. |

### Publish date is the sort key

There is no manual ordering UI. `published_at` ascending decides:

- lesson order within a course,
- lesson order within a training section,
- article order within a docs section,
- **the number rendered on a training section's hero** (it counts sections
  published on or before that one),
- prev/next links on every one of the above.

So when you produce a set — a course and its lessons, a section and its lessons
— **also state the intended publish order**, and space the dates (an hour apart
is plenty). Two posts with identical timestamps have undefined order.

### Internal tags carry data in their *description*

Ghost tags starting `#` are internal (they never appear as a public tag). The
theme reads several of them by slug prefix and **prints the tag's `description`
field directly into the UI**:

- `#duration-*` → the course's "Duration" stat and its "N of content" line
- `#video-duration-*` → the duration chip on a video lesson

So the description must be **only the display value** — `9h`, `45m`, `12m`. The
demo content ships descriptions written as sentences ("Total length: 9h.") and
consequently renders a chip reading *"Total length: 9h."* When you introduce a
new duration tag, set its description to the bare value.

---

## 7. Things that silently break a page

| Do this | Or else |
| --- | --- |
| Course post slug **==** course tag slug | Ghost 301s to the wrong course |
| Section post slug **==** section tag slug | `/training/{section}/` resolves to the wrong post |
| Put the **public** tag first, the `#internal` ones after | `primary_tag` is wrong → wrong URL, empty badges, dead "related" queries |
| Give a blog post a public topic tag | the topic badge renders empty and *related posts return nothing* — the query filters on `primary_tag.slug` |
| Write a `custom_excerpt` on a course lesson | the lede falls back to the literal words "Article lesson" |
| Use only the docs section slugs that are registered | an unregistered docs section has no route and no sidebar entry |
| Exactly one type tag per item | two `#level-*` or two `#training-*` type tags → the first branch wins, unpredictably |
| Real, existing Salesforce facts | the site's credibility is the product |

---

## 8. Output format

Unless the type prompt says otherwise, return **one block per item** in exactly
this shape, ready to enter in Ghost Admin. No commentary before or after.

```
─────────────────────────────────────────
TITLE:        …
SLUG:         …
EXCERPT:      …
TAGS:         Public Tag, #internal-one, #internal-two      ← in this order
VISIBILITY:   public | members | paid
PUBLISH:      2026-08-01 09:00   (relative order: 1 of 4)
FEATURE IMAGE: <describe the image to source/generate, or "none">
IMAGE ALT:    …
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>…</h2>
<p>…</p>
```

If a tag in `TAGS:` does not exist in Ghost yet, add a line
`NEW TAGS TO CREATE:` listing each one with the exact `name`, `slug` and
`description` to give it.

## 9. Self-check before you hand anything over

- [ ] Public tag first; exactly one of each internal type tag
- [ ] Slug follows the type's convention (and equals the tag slug, for courses
      and training sections)
- [ ] `EXCERPT` written, 15–30 words, not a summary
- [ ] Body starts at `<h2>`; at least two `<h2>`s; no `<h4>`+
- [ ] No classes, inline styles, `<div>`s or `ns-*` anywhere in the body
- [ ] Every `<pre><code>` has a `language-*` from the supported list
- [ ] No icons in the body, or only safelisted ones
- [ ] Every image has real alt text
- [ ] Publish order stated for multi-item output
- [ ] Every Salesforce claim is one you are confident is true
