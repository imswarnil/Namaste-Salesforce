# Training — authoring guide

How the `/training/` area is put together, and exactly what to click in Ghost to
add a section or a lesson.

There is **one training**. It has **sections**, each section has **lessons**.
Nothing about that hierarchy is a post — it is built out of *tags*:

| Concept | What it actually is | Where it lives |
| --- | --- | --- |
| The training | a route, no post at all | `routes.yaml` → `training.hbs` |
| A section | a **public tag** (`automation-basics`) | Ghost → Tags |
| A lesson | a **post**, primary tag = its section | Ghost → Posts |
| Section order | a hand-written list | `partials/training/sections.hbs` |

---

## 1. The tags that must match

This is the part that silently breaks things, so read it once.

### `#training-content` — the marker tag

Every lesson post **must** carry the internal tag `#training-content`.
It is what the collection filter, the router, and every count query key off:

- `routes.yaml` collection filter → `tag:hash-training-content`
- `post.hbs` → `{{#has tag="#training-content"}}` → renders `post-training.hbs`
- lesson counts on cards/rail → `tag:{section}+tag:hash-training-content`

In Ghost you type `#training-content` (with the hash — that's how Ghost marks a
tag internal/hidden). In Handlebars the same tag is written
`hash-training-content` inside `{{#get}}` filters and `#training-content` inside
`{{#has}}`. Both spellings refer to the one tag. Don't create both.

A post without this tag will render as a normal blog post at the wrong URL.

### The section tag must be the **primary tag**

Primary tag = the **first** tag in the post's tag list in Ghost. Drag it to
position 1. It matters twice:

1. **URL.** The permalink is `/training/{primary_tag}/{slug}/`. If
   `#training-content` is first, the URL becomes `/training/hash-training-content/…`
   and the lesson is orphaned.
2. **Navigation.** `post-training.hbs` passes `cur=primary_tag.slug` to the
   curriculum rail — that's what highlights the right section and shows the
   "back to section" pill.

So the tag list on a lesson is, in order:

```
1. automation-basics      ← the section (primary — MUST be first)
2. #training-content      ← the marker
3. #training-type-video   ← optional, see below
```

Ghost internal tags (`#…`) are never counted as the primary tag by Ghost itself
*only if* a public tag comes first — hence the ordering rule.

### Slugs that must line up

For a section called `Automation Basics`, this **one slug** appears in four
places and must be byte-identical everywhere:

| Place | Value |
| --- | --- |
| Ghost tag slug | `automation-basics` |
| `routes.yaml` route path | `/training/automation-basics/` |
| `routes.yaml` `data:` | `tag.automation-basics` |
| `sections.hbs` `slug=` | `slug="automation-basics"` |

**Keep section slugs clean — no numeric prefix.** `train-06-automation` would
leak into every lesson URL under it (`/training/train-06-automation/…`). Because
clean slugs can't encode order, the order lives in `sections.hbs` instead.

### Optional lesson type tags

Add **at most one** of these internal tags to change how the lesson renders:

| Tag | Effect |
| --- | --- |
| `#training-type-video` | full-width video hero; `training-video.js` lifts the first YouTube/Vimeo/`<video>` embed out of the body into the hero, and makes timestamps in a table seek the player |
| `#training-type-exercise` | barbell icon + "Exercise" badge |
| `#training-type-quiz` | exam icon + "Quiz" badge |
| *(none)* | reading lesson — file-text icon |

These also set `learningResourceType` in the JSON-LD.

---

## 2. Add a new section (3 steps)

### Step 1 — Ghost Admin → Tags → New tag

| Field | What to put | Used by |
| --- | --- | --- |
| **Name** | `Automation Basics` | card title, rail row, breadcrumb, JSON-LD `name` |
| **Slug** | `automation-basics` | URL + all three files below |
| **Description** | one or two sentences | card blurb (`ns-road__desc`), section-page intro, JSON-LD `description` — **fill it in**, the card looks empty without it |
| **Tag image** | optional | replaces the icon in the roadmap card thumb and on the section page |

Leave it a **public** tag (no `#`).

### Step 2 — Ghost Admin → Settings → Labs → Routes (`routes.yaml`)

Download the current YAML, add the block after the last existing section, upload
it back. Ghost Admin holds the live copy — the file in this repo is a reference
copy, keep it in sync.

```yaml
  /training/automation-basics/:
    data: tag.automation-basics
    template: training-section
```

### Step 3 — theme: `partials/training/sections.hbs`

Append one line:

```hbs
{{> "training/section-item" view=view cur=cur curId=curId n="6" slug="automation-basics" icon="ph-lightning"}}
```

- `n` — the step number shown on the roadmap. Sequential, no gaps.
- `slug` — must equal the Ghost tag slug.
- `icon` — any [Phosphor](https://phosphoricons.com/) name (`ph-…`); rendered
  filled where the design calls for it.
- `first="1"` — **only** on the very first entry. It suppresses the leading
  comma in the JSON-LD array; a second one produces invalid JSON-LD.

That single line feeds all five views: the `/training/` roadmap card, the lesson
rail, the search dropdown, and both JSON-LD shapes. Nothing else to edit.

Then rebuild and commit the built CSS — Tailwind scans templates for class
names:

```bash
yarn build && yarn test
```

### Also update the hardcoded counts

`training.hbs` says "five sections" in two places (the hero copy and the "The
path" intro). Grep for `Five sections` / `five sections` and update, or reword
to something count-free.

---

## 3. Add a lesson

Ghost Admin → Posts → New post.

1. **Title** — becomes the rail row and the hero heading.
2. **Tags**, in this order: `automation-basics`, `#training-content`, and
   optionally one `#training-type-*`.
3. **Excerpt** (Post settings → Excerpt) — shown under the title in the hero.
   Without it the hero is just a heading.
4. **Feature image** — the video poster on video lessons; a side illustration on
   others. Optional; the layout goes full-width without it.
5. **Access** — `Public` or `Members only`. The roadmap card and rail show a
   lock and a "N free" count derived from this.
6. **Publish date** — **this is the lesson order.** Lessons sort
   `published_at asc` within a section. To reorder, backdate.

The URL comes out as `/training/automation-basics/your-post-slug/`.

### Video lessons

Tag `#training-type-video` and paste the YouTube/Vimeo embed anywhere in the
body — the script moves it into the hero. To get chapter links, add a normal
table where one column holds timestamps (`0:00`, `12:34`, `1:02:03`); those
cells turn into seek buttons.

### Limits to know

- The rail and JSON-LD fetch **50 lessons per section** (`limit="50"`). More
  than that and the tail is silently dropped.
- Only **published** posts appear. Drafts and scheduled posts are invisible to
  `{{#get}}`.

---

## 4. Renaming or removing a section

Changing a tag's slug changes every lesson URL under it. If you must:

1. Rename the tag slug in Ghost.
2. Update `routes.yaml` (both the path and `data:`).
3. Update `sections.hbs`.
4. Add redirects in Ghost Admin → Settings → Labs → Redirects for the old
   lesson URLs.

To remove a section, delete its line from `sections.hbs` and its route block,
renumber the remaining `n` values, and re-home or unpublish its lessons first —
a lesson whose section has no route still resolves, but links back to a 404.

---

## 5. Checklist

- [ ] Tag slug is clean, no number prefix
- [ ] Same slug in Ghost, `routes.yaml` path, `routes.yaml` `data:`, `sections.hbs`
- [ ] Tag has a description
- [ ] `n` values sequential; `first="1"` on the first entry only
- [ ] Every lesson: section tag **first**, `#training-content` present
- [ ] Lesson publish dates give the order you want
- [ ] `yarn build` run, `assets/built/` committed
- [ ] `yarn test` (gscan) clean

---

## Quick reference — where things live

| File | Owns |
| --- | --- |
| `routes.yaml` (Ghost Admin) | `/training/` route, one route per section, the lesson collection + permalink |
| `training.hbs` | `/training/` landing: hero, roadmap, newsletter |
| `training-section.hbs` | `/training/{section}/` overview page |
| `partials/training/sections.hbs` | **section list + order** — the file you edit |
| `partials/training/section-item.hbs` | how one section renders in each of the 5 views |
| `partials/training/curriculum.hbs` | the left-hand lesson rail |
| `partials/post-training.hbs` | a lesson page |
| `assets/js/training-video.js` | hero video adoption + timestamp seeking |
| `assets/css/2-components/course.css` | `.ns-road*` roadmap styles, rail, lesson page |
