# 12 · The content system — one idea, many formats

The mistake most technical-education sites make is treating a blog post, a
video, a course lesson, a LinkedIn post and a slide deck as **five pieces of
work**. They are one piece of work and five *renderings* of it.

Build the pipeline that way and output roughly quadruples for the same effort.
Build it the other way and you burn out in a month.

---

> `19-teaching-method.md` is the companion to this file: this one decides what
> gets made and in what order, `19` decides what a lesson is made **of**. Read
> `19` before writing one.

## The unit is a CONCEPT, not a post

One concept = one thing a reader can now do that they could not before.
"Governor limits", "why your trigger fails at 200 records", "the difference
between a profile and a permission set."

A concept is worth doing when you can write its **outcome sentence** first:

> *After this, you can take a governor-limit exception and find the line that
> caused it, first time.*

If you cannot write that sentence, you do not have a concept yet — you have a
topic. Topics produce content nobody finishes.

## The cascade — always in this order

```
CONCEPT
  └─ 1. the LESSON        canonical, longest, on the site        (owns the URL)
       ├─ 2. the VIDEO    the same lesson, performed             (5–12 min)
       ├─ 3. the BLOG     the lesson's argument, standalone      (opinion + link)
       ├─ 4. the SLIDES   the lesson's skeleton                  (10–15 slides)
       └─ 5. the SOCIAL   the lesson's single sharpest claim     (LinkedIn/X)
```

**Never write these in parallel and never start at 5.** Every downstream format
is a *reduction* of the lesson, and reductions are fast. Writing the LinkedIn
post first produces a lesson that is a stretched tweet.

### Why the lesson owns the URL
It is the only one that is indexable, linkable, updatable and yours. YouTube
owns the video. LinkedIn owns the post. SlideShare owns the deck. **The lesson
is the asset; everything else is distribution.** Every downstream format links
back to it — that is the entire point of making them.

## What each format is actually for

| Format | Job | Length | Success looks like |
| --- | --- | --- | --- |
| **Lesson** | teach it properly, once | 800–1,500 words | someone finishes and can do the thing |
| **Video** | show the thing happening in a real org | 5–12 min | watch-through > 50% |
| **Blog** | the argument, with a point of view | 600–1,200 words | it gets linked to |
| **Slides** | teach it to a room, or hand it over | 10–15 slides | someone else can present it |
| **LinkedIn** | one claim, sharp enough to disagree with | 150–300 words | comments, not likes |

### The video is not a screencast of the lesson
Video is for what text is bad at: **watching something happen.** Building the
flow, hitting the error, reading the debug log. If the video can be a
screenshot, it should be a screenshot in the lesson.

Practical: script from the lesson's headings, record in one take per section,
never edit for polish. Chapters = the lesson's h2s, which also gives you the
timestamps for deep links.

### The blog post is NOT the lesson republished
The lesson teaches. The blog post **argues** — it has a position, names a
mistake, disagrees with common practice. It ends by linking to the lesson for
people who now want to learn it properly.

This distinction is what makes the blog worth reading for people who are not
your students.

### Slides are the skeleton, not the transcript
One claim per slide, the lesson's h2s as section breaks, a code block or a
screenshot per point. If a slide needs a paragraph, it is a lesson page.

### LinkedIn: one claim, no thread
The best-performing technical post is a **specific correction of a common
belief**, in plain language, with the reasoning visible:

> "Most Apex tutorials show you a trigger that works. Almost none show you one
> that survives a 200-record data load — which is every real data load.
> Here is the difference, and why the naive version fails. [link]"

That is the lesson's outcome sentence, sharpened. It is not a summary.

## The weekly rhythm that makes this sustainable

Pick a cadence you can hold on a bad week, not a good one.

```
Mon   write the LESSON            (the only hard day)
Tue   record + publish the VIDEO
Wed   cut the BLOG post from it
Thu   build the SLIDES
Fri   post the CLAIM to LinkedIn, linking the lesson
```

One concept per week is 50 concepts a year — a complete curriculum in two
years, with 250 pieces of distribution behind it. Two concepts a week is not
twice as good; it is how the whole thing stops.

## Repurposing OLD content is cheaper than new content

An existing lesson can be re-cut at any time. Every quarter:

1. Find the five lessons with the most traffic.
2. Ask what is now wrong or missing (the platform ships three times a year).
3. Update the lesson, then re-run the cascade from step 2.

Updated content ranks better than new content and costs a fraction as much.
`{{date updated_at}}` is already in the templates — use it honestly.

## What to measure, and what to ignore

**Measure:** lesson completion, search terms with no good result, which lessons
get linked to, which get updated most.

**Ignore:** pageviews, likes, follower count. A lesson read by 40 people who
finish it is worth more than 4,000 bounces, and only one of those numbers tells
you what to write next.

> The single most useful signal on the whole site is **what people search for
> and do not find.** Build search first (`abstract/11`), log the empty results,
> and let that pick your next concept.
