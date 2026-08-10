# Prompt — a BLOG POST

> Paste `00-house-style.md` above this, then your brief.

You are producing a **blog article** at `/blog/{slug}/`. Blog is where the site
argues, explains and takes positions. It is not a lesson: nobody arrives at a
blog post partway through a curriculum, and nothing depends on it. So a blog post
can have an opinion, and the good ones do.

Rendered by `partials/post-blog.hbs` — article plus a sidebar carrying the
contents rail and blog widgets.

---

## Blog vs. lesson

| | Lesson | Blog post |
| --- | --- | --- |
| Reader arrives | in sequence, mid-course | cold, from search or a link |
| Job | teach one mechanic | change how someone thinks about a decision |
| Voice | instructional | argumentative, first person acceptable |
| Ends with | a checked outcome | a position |

If your draft could be dropped into a course as lesson four, it is a lesson, not
a blog post. Rewrite it around the *judgement* rather than the procedure.

## Where it lands and what the theme builds around you

| Region | Comes from |
| --- | --- |
| Breadcrumb | theme |
| **Topic badge above the title** | **`primary_tag`** — the first public tag |
| `<h1>` | Title |
| Lede | **Excerpt** |
| Byline: author, date, reading time | Ghost author + publish date |
| Feature image with a caption | Feature image, its **alt**, and its **caption** — all three render |
| The article | **your body** |
| Tag pills in the footer | your public tags |
| Share buttons | theme |
| Discussion | Ghost comments, when enabled |
| Sidebar: on-this-page + blog widgets | your `<h2>`/`<h3>`s |
| **"Related posts" strip** | **posts sharing `primary_tag`** |

### The one rule people get wrong: give it a public topic tag

Two things on this page are driven by `primary_tag`, which is *the first public
tag* — internal `#` tags do not count:

- the topic badge above the title, and
- the related-posts query, which filters on `primary_tag.slug`.

The demo content ships blog posts tagged **only** `#blog`. Those posts have no
`primary_tag`, so the badge renders empty and the related-posts strip silently
finds nothing. **Always give a blog post a real public topic tag, first.**

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | Take a position or name a mental model. Existing: "Why Flow before Apex", "A mental model for governor limits", "Your first 90 days as an admin". Avoid listicles and avoid "The ultimate guide to". No clickbait questions. |
| **Slug** | The title, condensed, no stop-words: `why-flow-before-apex`, `governor-limits-mental-model`. |
| **Excerpt** | The lede under the title. 15–30 words. State the *claim*, not the topic. "Reach for code and you inherit a test class, a deployment and a reviewer" beats "An overview of Flow and Apex". |
| **Feature image** | Optional but wanted — it renders wide with a caption. 16:9, ≥1600px. |
| **Feature image alt** | Required whenever there is an image. |
| **Feature image caption** | Optional and genuinely rendered — use it for attribution or a real aside, not to repeat the alt text. |
| **Publish date** | The actual date. Blog order is reverse-chronological. |
| **Visibility** | `public`. Gate lessons, not opinions. |

## Tags — exact, and in this order

```
TAGS: <Topic>, #blog
```

1. **A public topic tag, first.** Reuse an existing one where it fits — the
   course tags (`Apex`, `LWC`, `Admin Foundations`) double as topic tags and
   give the related strip somewhere to point. Otherwise create a broad one
   (`Careers`, `Automation`, `Architecture`) — broad enough that a third and
   fourth post will share it, or related-posts stays empty.
2. `#blog` — required; this is what routes it to `/blog/`.

A second public tag is fine and shows as a pill in the footer, but the **first**
one is the one that matters.

---

## Body — the article

**700–1,400 words.** Long enough to earn a position, short enough to finish.

**Required shape — an argument, not a survey:**

```html
<h2>{The claim, stated flatly}</h2>
<p>{Open on the actual situation, not on context. The first sentence should be
   the one a reader would quote. No "In the Salesforce ecosystem…".}</p>

<h2>{The case for it}</h2>
<p>{The strongest version of your position, with a concrete example — a real
   requirement, a real limit, a real number.}</p>

<h2>{When it's wrong}</h2>
<p>{The honest counter-case. This section is why the post is worth reading
   rather than agreeing with. Name the conditions under which you would do the
   opposite.}</p>

<h2>{What to do about it}</h2>
<p>{The practical residue. What the reader should do differently on Monday.}</p>
```

Optional: a short comparison `<table>` when the post genuinely compares two
options — one table, with a `<thead>`, no more than four columns.

### Notes

- **Two `<h2>`s minimum** or the contents rail hides.
- Headings are claims: "Flow upgrades with the platform; your Apex does not"
  beats "Advantages of Flow".
- Code blocks are allowed and welcome, but a blog post is not a tutorial — if
  you are writing step five, you are writing a lesson.
- No "Conclusion" or "Introduction" headings. No "In this article we'll look
  at…". No summary that restates the piece.
- First person is fine here ("I've watched three teams do this"). It is not fine
  in lessons or docs.
- At most one `.ns-note` callout.

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Why Flow before Apex
SLUG:         why-flow-before-apex
EXCERPT:      Reaching for code is the instinct developers bring with them, and
              on this platform it is wrong more often than it is right.
TAGS:         Automation, #blog
VISIBILITY:   public
PUBLISH:      2026-08-12 09:00
FEATURE IMAGE: A Flow canvas, wide, shot at a shallow angle so the nodes read as
               texture rather than a readable diagram. 16:9.
IMAGE ALT:    A Salesforce Flow canvas with several connected elements
IMAGE CAPTION: A flow any admin on the team can read six months from now
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>The least powerful tool that works is the right one</h2>
<p>There is a habit among developers moving into the Salesforce ecosystem: reach
  for code, because code is what we know. It is the wrong instinct here more
  often than it is right, and the reason has nothing to do with how good the
  code is.</p>

<h2>What Flow actually buys you</h2>
<p>Every admin on the team can read it. It upgrades with the platform, which
  means a release note is Salesforce's problem rather than yours. It needs no
  test class, no deployment, and no second person to review a pull request. That
  is not a small list, and none of it is about capability — it is about who can
  maintain the thing after you have moved on.</p>

<h2>When Apex genuinely wins</h2>
<p>Complex bulk logic, callouts that need real error handling, and anything you
  need to unit test properly. Those are real reasons and they are not rare. If
  your requirement involves a hundred thousand records or an external system that
  fails in interesting ways, write the class. "I am faster in code" is not on the
  list — you are faster today, and slower for everyone who touches it later.</p>

<h2>What to do about it</h2>
<p>Start every requirement in Flow and stop when it stops fitting. The point at
  which Flow becomes awkward is real information: it usually means the
  requirement is more complicated than it was described as, and that is worth
  discovering before you have written a test class for it.</p>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] **A public topic tag is first**, before `#blog` — otherwise the badge is
      empty and related posts return nothing
- [ ] The topic tag is broad enough that other posts will share it
- [ ] Excerpt states the claim, not the topic
- [ ] There is a "when it's wrong" section
- [ ] No Introduction / Conclusion headings, no "In this article"
- [ ] Two or more `<h2>`s
- [ ] Feature image has alt text; caption used only if it says something new
- [ ] It is an argument, not a procedure — if it teaches steps, it is a lesson
