# 14 · The seed content — how to rebuild `import.json`

The bundle itself has been deleted; **this file is how you make another one.**
It is a fixture, not source material — regenerating it is cheap, and a stale
fixture that no longer matches the templates is worse than none.

You need it before you can look at a single page. Ghost with no content renders
every template as an empty state.

---

## What it is

ONE file, importable at **Ghost Admin → Settings → Labs → Import**:

```
dummy-content/import.json
```

```jsonc
{
  "meta": { "exported_on": 1753600000000, "version": "5.0.0" },
  "data": {
    "tags":       [ … ],   // every tag the templates branch on
    "posts":      [ … ],   // 2–3 per collection
    "posts_tags": [ … ]    // the join — SORT ORDER MATTERS, see below
  }
}
```

Field sets, which is all Ghost needs:

| table | fields |
| --- | --- |
| `posts` | `id · title · slug · lexical · status · type · visibility · featured · feature_image · custom_excerpt · created_at · published_at · updated_at` |
| `tags` | `id · name · slug · description · visibility` |
| `posts_tags` | `post_id · tag_id · sort_order` |

## ⚠️ The three things that make or break it

### 1 · `sort_order: 0` IS the primary tag
Ghost has no `primary_tag` column. **The tag with `sort_order: 0` is the
primary tag**, and the whole URL model depends on it (`abstract/01`). Get this
wrong and every nested URL collapses.

For a lesson, `sort_order: 0` must be its **course's** tag — not a tag of its
own. That inheritance is what makes `/courses/{primary_tag}/{slug}/` nest.

### 2 · Internal tags are written `hash-*`
In the import file an internal tag is `hash-course`, never `#course`. Its
`visibility` is `"internal"`. (In a template you write `#course`; in a *filter
string* and in this file you write `hash-`.)

### 3 · slug == tag slug, for parents
A course post's `slug` must equal its course tag's slug; same for a section.
Verify before importing:

```python
# every course/section post's slug must equal its sort_order:0 public tag
```

The last bundle passed this for all six parents — `admin-foundations`, `apex`,
`lwc` (courses) and `start`, `build`, `automate` (sections).

## What was in it, as a target to hit again

**52 posts · 49 tags · 138 joins**

| Kind | Count | Notes |
| --- | --- | --- |
| Courses (`hash-course`) | 3 | apex · lwc · admin-foundations |
| Course lessons (`hash-lesson`) | 9 | 3 per course, primary tag = the course |
| Training sections (`hash-training-section`) | 3 | start · build · automate |
| Training lessons (`hash-training-content`) | 9 | 3 per section |
| Blog posts (`hash-blog`) | 3 | |
| Resources (`hash-resource`) | 3 | |
| Docs + pages | 22 | 10 docs sections × ~2 articles, plus `about` / `training` |

**Every tag the templates branch on must exist**, or those branches are never
exercised and you will not see the bug until production:

```
structure  hash-course hash-lesson hash-training-section hash-training-content
           hash-blog hash-resource
access     hash-free hash-paid hash-preview
level      hash-level-beginner|intermediate|advanced
duration   hash-duration-45m|1h30m|3h|6h|9h        (description = "1h 30m")
art        hash-hero-1|2|3
lesson kind hash-lesson-type-video · hash-video-duration-6m|9m|12m|18m
training   hash-training-article|video|exercise|quiz
resource   hash-resource-type-book|tool|website
```

> The metadata convention: **the tag's `description` field carries the text.**
> `hash-duration-1h30m` has `description: "1h 30m"`. That is what lets an author
> add a duration in Ghost Admin without touching the theme (`abstract/02`).

## Coverage rules — what "enough" means

Two of a thing proves it renders. Three proves the LIST renders. So:

- **≥3 per collection** — a one-item grid hides every gap alignment bug.
- **At least one of each STATE**, because the empty and locked paths are where
  bugs hide: one `visibility: "members"` lesson, one `hash-preview`, one
  `featured: true`, one post with **no** `feature_image`, one course with no
  lessons at all.
- **One long title and one long excerpt** — truncation and text-wrap bugs only
  appear at length.
- **Every art-direction variant used at least once** (`hash-hero-1|2|3`), or
  you are shipping variants nobody has ever seen.

## Writing the bodies

`lexical` is Ghost's editor format (a JSON string, not HTML). Two ways:

1. **Easiest and most reliable:** write the posts in a real Ghost, then
   **Settings → Labs → Export** and trim the export down. The export is already
   in exactly this shape.
2. Hand-write minimal lexical. A single paragraph is enough for a fixture:

```json
"lexical": "{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Body copy.\",\"type\":\"extended-text\",\"version\":1}],\"direction\":\"ltr\",\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1}],\"direction\":\"ltr\",\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}"
```

Option 1 is strongly preferred — hand-written lexical is easy to get subtly
wrong and Ghost fails the import without saying which post.

`scripts/fix-lexical-double-encoding.py` exists because that JSON string gets
double-escaped when passed through tooling. If an import fails on lexical, that
is the first thing to check.

## Ordering

Sections and lessons order by `published_at asc`. Backdate to reorder. Give the
fixture spaced-out dates rather than identical ones, or the order is arbitrary
and prev/next behaves differently on each import.

## The workflow this fixture is for

```bash
# 1. Ghost Admin → Settings → Labs → Routes  → upload routes.yaml   ← FIRST
# 2. Ghost Admin → Settings → Labs → Import  → import.json
# 3. open every route in abstract/01 and look at it
```

Step 1 before step 2. Without `routes.yaml` the collections do not exist, the
posts import with no URLs, and every page looks broken for reasons that have
nothing to do with the theme.
