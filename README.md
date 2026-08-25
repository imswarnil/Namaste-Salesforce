# Namaste Salesforce — Ghost theme

Built on [NS-Design-System](https://nsds.imswarnil.com/). Every page is a port
of an archetype in `NS-Design-System/templates/`, with the marked slots swapped
for Ghost helpers — the procedure that system's own `docs/INTEGRATION.md` §5
specifies. The theme adds no design opinions of its own.

## Develop

```bash
npm install
npm run dev      # watch and rebuild
npm run build    # one production build
npm test         # build, then gscan
```

`assets/css/screen.css` is the source; `assets/built/` is what Ghost serves.
It is committed, because Ghost serves the theme as uploaded and there is no
build step on the server — and CI rebuilds and diffs it, which is what makes
committing generated files safe.

## Set up a local Ghost

```bash
# 1. Admin → Settings → Labs → Routes  → upload routes.yaml      ← FIRST
# 2. Admin → Settings → Labs → Import  → dummy-content/import.json
```

Step 1 before step 2. Without `routes.yaml` the collections do not exist, the
posts import with no URLs, and every page looks broken for reasons that have
nothing to do with the theme.

Regenerate the fixture with `python3 scripts/build-import.py`.

## The pages

| URL | Template | NSDS archetype |
|---|---|---|
| `/` | `home.hbs` | `homepage` |
| `/blog/` | `blog.hbs` | `blog-listing` |
| `/blog/{post}/` | `post/blog` | `blog-post` |
| `/courses/` | `courses.hbs` | `course-listing` |
| `/courses/{course}/` | `post/course` | `course-detail` |
| `/courses/{course}/{lesson}/` | `post/lesson` | `course-player-article` |
| `/training/` | `training.hbs` | `training-index` |
| `/training/{section}/` | `post/section` | `training-module` |
| `/training/{section}/{post}/` | `post/training-post` | `training-post` |
| `/docs/…` | as training | — |
| `/tag/{slug}/` | `tag.hbs` | `tag-page` |

A course is a **destination** — its card leads with a glyph and its lessons
carry an index and an access state. A training section is a **step** — its
card leads with a numeral and its posts carry a type and a time. NSDS ships
both pairs; the difference is the information, not decoration.

## Documentation

`abstract/` — start at `abstract/00-README.md`. `CLAUDE.md` has the rules that
are easy to break silently.
