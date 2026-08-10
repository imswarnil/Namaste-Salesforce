# Prompt — a RESOURCE

> Paste `00-house-style.md` above this, then your brief.

You are producing a **library entry** at `/resources/{slug}/` — a pointer to
something that lives elsewhere: a book, a tool, a site, a repo, a podcast. The
value of the page is the **judgement**: who it is for, when it is the right thing
to reach for, and when it is not.

Rendered by `partials/post-resource.hbs`.

---

## What a resource page is not

It is not a summary of the thing, and it is not a press release for it. A reader
arrives already able to find the official description. What they cannot get
elsewhere is an honest read: *is this worth my weekend?* Write that.

Never claim a resource is free, current or maintained unless you know it is.

## Where it lands and what the theme builds around you

| Region | Comes from |
| --- | --- |
| Type glyph in a chip + type badge | the `#resource-type-*` tag |
| `<h1>` | Title |
| Lede | **Excerpt** |
| Cover image | Feature image + its alt |
| The review | **your body** |
| "All resources" button | theme |
| Sidebar: "More like this" | other resources, newest first |
| Left/right ad rails | theme |

The `/resources/` index filters by type using these same tags, so the type tag is
what makes an entry findable.

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | The resource's real name, as its authors write it. "Salesforce CLI", "Advanced Apex Programming", "Salesforce Developer Docs". Do not editorialise the title — that is what the excerpt is for. |
| **Slug** | The name, lowercased and hyphenated: `salesforce-cli`, `advanced-apex-programming`. |
| **Excerpt** | The lede, and where your judgement goes. 15–30 words. *"The book to read after you can already write a trigger — it is about design, not syntax."* |
| **Feature image** | Book cover, tool screenshot, or site home page. Renders full width in a hairline frame. Optional. |
| **Feature image alt** | Required when there is an image. |
| **Publish date** | When you added it. The index and the "More like this" list are newest-first. |
| **Visibility** | `public`. |

## Tags — exact

```
TAGS: #resource, #resource-type-…
```

1. `#resource` — required, routes it to `/resources/`.
2. **Exactly one type tag.** These drive the glyph, the badge and the index
   filter:

| Tag | Badge | Glyph | Exists in Ghost? |
| --- | --- | --- | --- |
| `#resource-type-book` | Book | book | ✅ |
| `#resource-type-tool` | Tool | wrench | ✅ |
| `#resource-type-website` | Website | globe | ✅ |
| `#resource-type-video` | Video | video camera | create it |
| `#resource-type-cheatsheet` | Cheat sheet | file | create it |
| `#resource-type-podcast` | Podcast | microphone | create it |
| `#resource-type-repo` | Repo | git fork | create it |
| `#resource-type-community` | Community | users | create it |

The last five are fully supported by the templates but the tags are not in the
content bundle yet. If you use one, declare it:

```
NEW TAGS TO CREATE:
  name: #resource-type-podcast   slug: hash-resource-type-podcast
  description: Resource type: podcast.
```

With no type tag the page falls back to a generic cube glyph and the badge reads
"Resource" — always set one.

A public topic tag is optional here and unused by the layout; skip it unless you
want the resource showing on a tag archive.

---

## Body — the review

**200–450 words.** Short. This is a recommendation, not an article.

**Required shape:**

```html
<h2>What it is</h2>
<p>{Two or three sentences. What the thing actually is and who made it. Include
   the outbound link here — the first link in the body is treated as the
   resource itself.}</p>

<h2>Who it's for</h2>
<p>{Be specific about the level. "After your first trigger, before your first
   integration." Name who should not bother, and what they should use instead.}</p>

<h2>What it's good at</h2>
<ul>
  <li>{2–4 concrete strengths. Not "comprehensive" — say what it covers that
      others do not.}</li>
</ul>

<h2>What to know before you start</h2>
<p>{Cost, currency, effort, prerequisites. If it is a paid book, say so. If it
   was last updated four years ago, say so and say whether that matters — for
   Apex design it often does not, for UI screenshots it always does.}</p>
```

### The outbound link

Put the real link in the first paragraph, as an ordinary `<a href="…">` around
the resource's name. Use the canonical URL, not a redirect or an affiliate link.

```html
<p><a href="https://developer.salesforce.com/docs">The Salesforce Developer
  Docs</a> are the official reference for every API, object and metadata type
  on the platform.</p>
```

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Advanced Apex Programming
SLUG:         advanced-apex-programming
EXCERPT:      The book to read once you can already write a trigger — it is about
              design and limits, not syntax.
TAGS:         #resource, #resource-type-book
VISIBILITY:   public
PUBLISH:      2026-08-14 09:00
FEATURE IMAGE: The book cover, straight on, on a plain light ground.
IMAGE ALT:    Cover of Advanced Apex Programming by Dan Appleman
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>What it is</h2>
<p><a href="https://advancedapex.com/">Advanced Apex Programming</a> by Dan
  Appleman is a book about designing Apex under the platform's constraints —
  governor limits, bulk execution, and the architectural decisions that follow
  from both. It assumes you can already write the code and asks whether you
  should have.</p>

<h2>Who it's for</h2>
<p>Developers who have shipped a trigger and been surprised by production. If you
  are still learning Apex syntax, this will be frustrating — work through the
  Apex course here first, then come back. If you have been writing Apex for five
  years without reading it, you are the intended reader more than anyone.</p>

<h2>What it's good at</h2>
<ul>
  <li>Trigger design patterns explained as trade-offs, not as one right answer</li>
  <li>Governor limits treated as an architectural input rather than an obstacle</li>
  <li>Asynchronous Apex — when each mechanism is the correct one</li>
  <li>Testing as a design tool, not a coverage target</li>
</ul>

<h2>What to know before you start</h2>
<p>It is a paid book and it is not a reference — it reads front to back and
  rewards that. The platform specifics age, but the reasoning does not, which is
  why it is still the recommendation several releases after publication. Budget a
  couple of evenings and read it near an org you can experiment in.</p>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] `#resource` present, plus **exactly one** `#resource-type-*`
- [ ] Any type tag outside the three shipped ones declared under
      `NEW TAGS TO CREATE`
- [ ] The real canonical outbound link is the first link in the body
- [ ] Excerpt carries a judgement, not a description
- [ ] "Who it's for" names who should skip it
- [ ] Cost, currency and effort stated honestly
- [ ] No claim about being free, current or maintained that you cannot support
- [ ] Under ~450 words
