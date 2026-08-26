# collections/ — one file per surface, written before it is built

Each file here specifies **one page family**: what it is, what its URLs are,
what the listing shows, what the single page carries, and which NSDS archetype
it ports. Eight of them, all currently **unspecified**.

> **The rule: no collection gets built before its file is answered.**

That is not process for its own sake. The last version of this theme had its
content model assembled one reasonable commit at a time, and the result —
recorded in [`../10-how-this-went-wrong.md`](../10-how-this-went-wrong.md) —
was ~100 duplicated classes, three copies of a lesson row, two tables of
contents, and a set of URLs nobody had decided. Every one of those started as
a template written before anyone had said what the page was.

## What a collection is, mechanically

A filter, a permalink, and a template. Those three things buy you a stable URL
shape, an index page, an RSS feed, pagination, and `{{#prev_post}}` /
`{{#next_post}}` scoped to the collection — which is what turns a pile of posts
into a sequence. [`../07-collections.md`](../07-collections.md) is the full
mechanics; [`../01-content-model.md`](../01-content-model.md) is the URL rules
and the one that is unrecoverable if wrong.

## The eight

| file | surface | mounts at |
|---|---|---|
| [`01-home.md`](01-home.md) | the homepage | `/` |
| [`02-blog.md`](02-blog.md) | writing | `/blog/` |
| [`03-courses.md`](03-courses.md) | courses and their lessons | `/courses/` |
| [`04-training.md`](04-training.md) | the training roadmap and its lessons | `/training/` |
| [`05-docs.md`](05-docs.md) | the documentation hub | `/docs/` |
| [`06-resources.md`](06-resources.md) | downloads, snippets, references | `/resources/` |
| [`07-toolkit.md`](07-toolkit.md) | products | `/toolkit/` |
| [`08-archive.md`](08-archive.md) | the catch-all | `/archive/` |

The **proposed** column in each file's §3 is carried over from the previous
content model. It is a starting point with no authority — overwrite it. The
**decided** column is the one `routes.yaml` gets built from.

## Answer them in this order

1. **§8, "What it is NOT", first.** It is the fastest way to find out that two
   of these are one collection. Courses and training are the pair most likely
   to collapse into each other, and finding that out now costs nothing.
2. **§3, the URL model.** The only genuinely expensive part. Everything else
   here can be rebuilt in an afternoon; a published URL cannot be moved without
   301s and lost ranking.
3. **§1, §2, §4, §5** — the shape of the thing.
4. **§6, the archetype.** If nothing in `NS-Design-System/templates/` fits, that
   is worth knowing *before* the build starts, because the answer is usually
   that the archetype belongs upstream rather than here.
5. **§7, access.** Last, because it is the cheapest to change.

## Then, and only then

The checklist at the foot of each file is the build order. It ends with *look
at the page* — in both themes, at 360px, with JavaScript off — because a green
build has been green on a visually broken site more than once here.

## Tag names are not decided here

They are canonical in the root abstract, at
`Namaste Salesforce/abstract/05-content/tag-registry.md`. This folder decides
what a surface *does*; that file decides what things are *called*, because the
names are shared with the LMS and the content pipeline and cannot be a
theme-local choice.
