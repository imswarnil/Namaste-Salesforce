# NS Design System — design-components.md

> 42 components, grouped by workflow. Tokens: [DESIGN.md](./DESIGN.md). Rules: [design-guidelines.md](./design-guidelines.md). Live specimens with copy-paste markup: [components.html](./components.html) · page-level bands: [sections.html](./sections.html).

Measurements assume the 10px rem base (`1.6rem` = 16px).

---

## Actions

### Button — `.btn`
Faces: solid (default), `.btn-ghost`, `.btn-soft`, `.btn-inverse` (on dark). Sizes: default 44px, `.btn-sm` 36px, `.btn-lg` 52px. Leading icon 1.7rem.

| Contrast | States | Touch target |
| --- | --- | --- |
| `--accent-contrast` on `--accent` ≥ 4.5:1 | hover lift + `--accent-strong`; focus ring; `aria-disabled` | 44×44 |

- Do start labels with a verb. Don't put two solid buttons side by side.

### Icon button — `.icon-btn`
40×40, 2rem icon, needs `aria-label`. Used in headers, share rows, the lesson bar.

### Chip — `.chip`
Pill, 1.25rem, 600. Faces: default, `.chip-accent`, `.chip-level` (+ `.chip-level-beginner`), `.chip-featured`, `.chip-type`. Wrap in `.chips`. Text is a tag description.

### Badge — `.badge`
22px pill for counts. Faces: default, `.badge-soft`, `.badge-muted`, `.badge-success`, `.badge-warning`, `.badge-error`, `.badge-dark`.

### Status — `.status` + `.badge-dot`
Dot + word. Dot variants `-success -warning -error -accent -live` (pulsing).

### Kbd — `.kbd`
Keyboard key, mono 1.15rem.

### Tooltip — `[data-tip]`
CSS-only, appears on hover and `:focus-visible`; `data-tip-pos="bottom"` flips it.

---

## Input

### Input — `.input`
46px, 1.5rem, focus ring `0 0 0 3px var(--accent-soft)`. Textarea: same class with `height:auto`.

### Search — `.search`
Icon + `.input` + `.kbd` hint; `.search-results` list with title/meta.

### Subscribe row — `.subscribe-row`
Input + button sharing a baseline; stacks below 520px. `.fake-input` when a portal owns the real form.

### Filter bar — `.filter-bar`
Groups of `.filter-btn` pills with `.is-active`; `.filter-clear` appears when `.has-active`.

### Quiz — `.quiz`
`<form>` of `.quiz-q` fieldsets; `.quiz-opt` radio labels, one input carries `data-correct`. `:has()` paints right/wrong and reveals `.quiz-explain`; `.quiz-score` tallied by nsds.js.

| Contrast | States | Touch target |
| --- | --- | --- |
| verdict colours are borders + 6–8% fills, text stays `--text` | hover, checked-correct, checked-wrong, revealed | ≥ 44px rows |

### Tabs — `.tabs`
Radio-driven; n-th radio shows n-th `.tab-panel` (≤ 8). `.tabs-pill` for the segmented face.

---

## Navigation

### Header — `.site-head`
64px sticky translucent bar: brand, `.site-nav` with icons, `.site-head-cta`, actions, burger. Drawer ≤ 900px via `#nav-open` checkbox, full-height, scroll-locked. Dropdowns: `.nav-has-dropdown > .nav-dropdown`, hover and `:focus-within`.

### Breadcrumbs — `.crumbs`
1.35rem, chevron SVGs between, `aria-current` on the last.

### Table of contents — `.toc-list`
Left-rule links with `.is-active`; `.toc-h3` indents. `[data-toc]` is filled by nsds.js; `.toc-inline` is the collapsed mobile form.

### Pagination — `.pagination` / `.pager` / `.post-nav`
Newer/older row; numbered pager with `.is-current` and `.pager-gap`; prev/next post links.

### Lesson navigation — `.lesson-nav` / `.lesson-bar`
Prev/next lesson cards under an article (stack ≤ 600px). `.lesson-bar` is the sticky bottom bar ≤ 1023px: progress, "4 / 12", arrows.

### Player rail — `.player-rail`
320px course sidebar: `.player-rail-course`, `.player-rail-progress`, `.rail-module` `<details>` groups, `.player-list` rows with counters and `.is-done / .is-current / .is-locked`. Folds to `.player-rail-toggle` `<details>` ≤ 1023px; `.rail-toggle` collapses it ≥ 1024px via `html[data-rail]`.

### Trail — `.trail` / Path — `.path`
Vertical numbered rail of `.trail-node` modules with `.trail-stops`; `.trail-end` terminus. `.path` is the horizontal scroll-snap version with `.path-step` and `.path-terminus`.

### Steps — `.steps`
Horizontal stepper with counters, `.is-done` check discs, `.is-current` ring; `.steps-v` vertical with headings.

### Accordion — `.acc` / `.faq`
Native `<details>`; `.acc-group` shares hairlines; `.faq` is flush.

---

## Containment

### Card — `.card`
Surface, hairline, `--radius-lg`, hover lift; `.card-media` 16:9; `.card-body`; `.card-eyebrow`, `.card-title`, `.card-excerpt` (3-line clamp), `.card-meta`. Variants `.course-card`, `.video-card`, `.card-feature`, `.template-card`. Whole card is one target via `.card-link::after`.

### Module card — `.module-card`
Tag identity head + `.module-list` of sections + foot.

### Widget — `.widget`
Sidebar box with `.widget-title`. Family: author, recent posts, newsletter, share, sponsor (`.widget-sponsor`, `.is-skyscraper`), tag cloud.

### Frame — `.frame`
16:9 media well (`.frame-4x3`, `.frame-square`, `.frame-cinema`), `.frame-play`, `.frame-badge`, `.frame-caption`.

### Browser — `.browser`
Window chrome with dots and URL; `.browser-dark` for code. Device — `.device` phone bezel.

### Code — `.code` / `.code-head`
Dark face, mono 1.35rem, `.copy-btn` (nsds.js), `.tk-*` token spans, `.ln-add / .ln-del` diff lines, `.code-inline`.

### Table — `.table`
Inside `.table-wrap`; `.table-striped`, `.table-hover`, `.table-compact`, `.table-compare`, `.num` cells.

### Modal — `dialog.modal`
Native `<dialog>` with `::backdrop` scrim; head/body/foot; sheet from the bottom ≤ 600px.

### Pricing tier — `.tier`
In `.tiers`; `.tier-featured` + `.tier-flag`; price, period, check-list, `.tier-cta` full-width button.

### Callout — `.callout`
Coloured left rail: default (note), `-tip`, `-warn`, `-danger`, `-key`; `.callout-label`.

---

## Data display

### Stats — `.stats` / `.stat`
Tiles with `.stat-value` (tabular, `em` accent), `.stat-label`, `.stat-delta`, `.stat-icon`; `.stats-inline` borderless; `.on-dark` variant.

### Progress — `.progress` / `.ring`
`--value` 0–100 drives both; `.progress-row` adds the label; ring sizes `-sm / -lg`.

### Avatar — `.avatar`
32px circle; sizes `-sm 24 / -md 40 / -lg 64 / -xl 96`; `.avatar-mono` monogram; `.avatar-ring`; `.avatar-stack` with `.avatar-stack-count`; `.person` row.

### Lists — `.check-list` / `.icon-list` / `.dl` / `.num-list`
Ticked, iconed, term/description grid, big-numbered.

### Curriculum — `.curriculum`
Numbered lesson rows in one bordered box; `.curriculum-side` holds type icon + duration chip.

### Timeline — `.timeline`
Dot, date, title, excerpt — the changelog list.

### Testimonial — `.quote-card` / `.pull-quote`
Mark, stars, words, `.person`; `.quote-grid` columns.

---

## Feedback

### Alert — `.alert`
Info default; `-success`, `-warning`, `-error`; icon, body, title, close. Ink tokens for text.

### Toast — `.toast`
Fixed bottom-centre; `nsds.toast("…")` shows it for 2.4 s.

### Empty state — `.empty`
Dashed box, icon tile, heading, one sentence, an action.

### Lesson recap — `.lesson-recap`
Accent-tinted takeaways box at the end of a lesson; `.lesson-resources` strip of downloadable links.

---

## Sections (page bands)

`.hero` (+ `.hero-split`, `.hero-center`, `.hero-cinema`), `.marquee`, `.logo-strip`, `.props` (+ `.props-flush`), `.split` (+ `.split-reverse`), `.spotlight`, `.cta-band` (+ `.cta-band-split`, `.cta-band-full`), `.band-newsletter`, `.band-dark.on-dark`, `.template-bar`. Each is documented live in [sections.html](./sections.html).
