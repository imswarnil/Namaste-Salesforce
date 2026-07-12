# Namaste Salesforce — Changes & TODO

A running log of what's been built on the theme and what's left. Nothing is
committed to git yet — review, then commit when you're happy.

---

## ✅ Done

### Design system — "Namaste UI" (SLDS blue)
- `assets/css/namaste-ui/` — `tokens · base · overrides · components · navbar · course` (imported by `screen.css`).
- SLDS-blue palette, primitives: `.ns-btn` (solid brand, **no gradient**), `.ns-kicker`, `.ns-chip`, `.ns-badge`, `.ns-input`, `.ns-aurora`, `.ns-level`, `.ns-price-tag`, etc.
- Dark mode, branded scrollbar, `overflow-x: clip` guard.

### Navigation & headers
- **Full-width navbar**, menu items **centered**; plain login icon that becomes an **avatar + dropdown** (with "Become Author") when signed in.
- **Custom settings** (Ghost Admin → Design): `navbar_behavior` (Sticky / Fixed on scroll / Island on scroll / Static), show search/github/sponsor toggles, become-author URL.
- **"# Topics" hover dropdown** next to the logo → tag cloud.
- **Course-player header** for lessons/modules (logo · centered nav · ✕ back-to-course); mobile **left hamburger** opens the lesson drawer below the navbar; **minimal lesson footer**.

### URLs (routes.yaml)
- `/courses/` list · `/courses/{course}/` course · `/courses/{course}/{lesson}/` lesson (nested).
- **Rule:** each course post's **slug must equal its course tag** (e.g. slug `apex`, tag `apex`).
- `/tag/{course-tag}/` **redirects to the course** (no duplicate tag page).
- Content-less routes: `/become-author/`, `/about/`.

### Course pages
- **Catalog** (`courses.hbs`): animated stats, filter sidebar (search · price · level with colour dots · **duration slider** · instructor), sponsored Udemy card, **ad after every 4 courses**, featured ribbons, animated become-author band. Level filters now **default OFF — tick a level to filter to it**.
- **Course page** (`post-course.hbs`): hero **variants** (`#hero-1..5`, `#hero-5` = video poster), level/price/featured badges, animated stats, description → curriculum → FAQ, sticky sidebar, share, members lock note. Course **body/overview now renders** (paid courses are public so the overview shows; lessons stay gated).
- **Lesson page** (`post-lesson.hbs`): video/article type + duration, members gate, **author box**, free-lesson **support CTA**, prev/next, comments.
- Cards simplified (icon price badge, compact, plain "View →").

### SEO — JSON-LD (`partials/jsonld/` + `structured-data.hbs`)
- `@graph` with Organization + WebSite + navigation ItemList (all pages).
- **Course** (+ CourseInstance, hasPart→lessons) on `#course`; **LearningResource** (+ VideoObject for `#lesson-type-video`) on `#lesson`.

### Dummy content (`dummy-content/`) — one importable per collection
- **`course.json`** — Ghost-importable courses + lessons (was `import.json`; **already imported**). `course-spec.json` keeps the readable outline.
- **`training.json`** — Ghost-importable tracks + section content (3 roadmaps → 12 sections → 37 lessons). Model: track slug == track tag; a training-content lesson's PRIMARY tag = the track tag (nests at `/training/{track}/{slug}/`), section = a secondary `train-{track}-NN-*` tag for grouping.
- **`docs.json`** — Ghost-importable docs (6 sections → 22 docs). Doc PRIMARY tag = its `docs-NN-*` section tag (nests at `/docs/{section}/{slug}/`).
- `taxonomy.json`, `navigation.json` — reference (not imports).
- Import each collection separately in **Settings → Labs → Import**.

### Routes updated (2 changes)
- **Docs moved to `/docs/`** (was `/documentation/`) and now **section-nested**: `/docs/{section}/{doc}/`. All in-theme links repointed.
- **Training split into two collections** like courses: tracks at `/training/{track}/`, content at `/training/{track}/{lesson}/`.
- Internal tags: `#course #lesson`, `#free #paid`, `#level-*`, `#hero-1..5`, `#show-image/#hide-image`, `#lesson-type-video`, `#preview`, `#duration-*` (15m→12h30m), `#video-duration-*` (1m→45m).

---

## 📋 To do on your Ghost site
1. **Routes** — already synced to `content/settings/routes.yaml`; if you move hosts, upload `routes.yaml` in **Settings → Labs → Routes**.
2. **Navigation** — set primary + secondary from `dummy-content/navigation.json` in **Settings → Navigation**.
3. **Custom settings** — pick a navbar style in **Settings → Design → Site-wide**.
4. **Pages** — `/about/` and `/become-author/` work via routes; create real Ghost pages with those slugs only if you want editable bodies.
5. **Course images** — cards/heroes look fuller with feature images; upload one per course (tag `#show-image`).
6. **Zip & deploy** — `yarn zip` → `dist/namaste-salesforce.zip`.

---

## 🔜 Pending (next up — requested, not yet built)
- **Training restructure** — mirror courses: `/training/` ordered list → training **sections** (a tag) → section lessons (`#training-content`), with end-to-end prev/next + switch (like the course player). Plus `dummy-content/training.json`.
- **Documentation restructure** — `/docs/` → docs **sections** → section posts; realistic docs (how to configure courses/lessons/site, end-to-end). Plus `dummy-content/docs.json`.
- **Homepage** — simplify to plain Tailwind: grids + line/grid background patterns, less "designed".
- **Hero variants** — flesh out all 5 distinct course-hero layouts (2 = centered, 5 = video already differ).
- **JSON-LD** — add branches for blog, docs, training, collection pages.

---
_Last updated by the current build session. Local dev: `/Users/swarnil/Namaste Salesforce` (port 2369)._
