# Namaste Salesforce — Changes & TODO

A running log of what's been built on the theme and what's left.

---

## ✅ Done

### Design system — "Developer Console"
- **Four layers, one file per thing**, each with its own `index.css`; `screen.css` is just Tailwind + four imports. `0-foundation/` (tokens) → `1-elements/` (one file per element family) → `2-components/` (one file per component) → `3-modules/` (per-feature). The old `namaste-ui/` and `theme/` folders are gone.
- **Components** (`.ns-thing` / `.ns-thing--variant` / `.ns-thing__part` / `.is-state`, variants compose): button · badge · chip · tag · kicker · avatar · card · feature · quote · widget · note · empty-state · stat · progress · input · code-window · video-poster · steps · timeline · page-header · section-head · breadcrumb · pagination · nav-link · icon-button · menu · tooltip · toc · sidebar · subnav · share · ad · marquee · effects.
- Foundation mixins: `ns-label` / `ns-index` / `ns-hairline` / `ns-dot-marker` / `ns-transition`.
- Five rules (`0-foundation/README.md`): hairline borders are the structure, one signal blue, mono for every label/index, sharp geometry (6px card / 4px button, pills only for true tags), instant 120–180ms motion. No gradients, glass, glow, or hover lifts.
- Fira Code is the mono face; dark mode is brand navy. Live docs at `/docs/design-system/`; specimen sheet in `demo.html`.

### Navigation & headers
- **Full-width navbar**, menu items **centered**; plain login icon that becomes an **avatar + dropdown** (with "Become Author") when signed in.
- **Custom settings** (Ghost Admin → Design): `navbar_behavior` (Sticky / Fixed on scroll / Island on scroll / Static), show search/github/sponsor toggles, become-author URL.
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

### Demo content (`dummy-content/import.json`)
- **One importable bundle**, not a file per collection. Import it in **Settings → Labs → Import**.
- Contains 2–3 posts for every collection and section: 3 courses × 3 lessons · 3 training sections × 3 lessons · 10 docs sections × 2 articles · 3 blog posts · 3 resources · the `about` and `training` pages · every tag the templates branch on.
- Encodes the `routes.yaml` rules: course slug == course tag, section slug == section tag, lesson primary tag == its parent course/section tag.


### Routes updated (2 changes)
- **Docs moved to `/docs/`** (was `/documentation/`) and now **section-nested**: `/docs/{section}/{doc}/`. All in-theme links repointed.
- **Training split into two collections** like courses: tracks at `/training/{track}/`, content at `/training/{track}/{lesson}/`.
- Internal tags: `#course #lesson`, `#free #paid`, `#level-*`, `#hero-1..5`, `#show-image/#hide-image`, `#lesson-type-video`, `#preview`, `#duration-*` (15m→12h30m), `#video-duration-*` (1m→45m).

---

## 📋 To do on your Ghost site
1. **Routes** — already synced to `content/settings/routes.yaml`; if you move hosts, upload `routes.yaml` in **Settings → Labs → Routes**.
2. **Navigation** — set the primary + secondary menus in **Settings → Navigation** (Home · Courses · Training · Docs · Blog · Resources · About).
3. **Custom settings** — pick a navbar style in **Settings → Design → Site-wide**.
4. **Pages** — `/about/` and `/become-author/` work via routes; create real Ghost pages with those slugs only if you want editable bodies.
5. **Course images** — cards/heroes look fuller with feature images; upload one per course (tag `#show-image`).
6. **Zip & deploy** — `yarn zip` → `dist/namaste-salesforce.zip`.

---

### Templates wired to the section model (done)
- **Homepage** (`home.hbs`) — plain Tailwind, grid-line background patterns, no gradients.
- **Docs home** (`documentation.hbs`) — grouped by **section** (`docs-NN-*` primary tag), search filters within groups.
- **Docs sidebar** (`docs/sidebar.hbs`) — section-grouped; single doc breadcrumb shows the section; prev/next stays **within the section** (`in="primary_tag"`).
- **Training curriculum** (`training/curriculum.hbs`) — THIS track's modules grouped by **section** (`train-{track}-NN-*`); `training-nav.js` flows Prev/Next across sections → Finish.

## 🔜 Pending (next up — requested, not yet built)
- **Import** `dummy-content/import.json` (Settings → Labs → Import) — the live site still shows older content until you do.
- **Hero variants** — flesh out all 5 distinct course-hero layouts (2 = centered, 5 = video already differ).
- **JSON-LD** — add branches for blog, docs, training, collection pages.

---
_Last updated by the current build session. Local dev: `/Users/swarnil/Namaste Salesforce` (port 2369)._
