# NS Design System — design-guidelines.md

> Read [DESIGN.md](./DESIGN.md) first for every token. Component specs are in [design-components.md](./design-components.md). This file is the rulebook: accessibility, interaction, content and the do/don't list an agent or a human should check against before shipping a page.

---

## Accessibility

### Contrast requirements

| Requirement | Ratio |
| --- | --- |
| Body and heading text on `--bg`, `--bg-alt`, `--surface` | ≥ 4.5:1 (all semantic ink/surface pairs pass) |
| Large text (≥ 2.4rem bold) | ≥ 3:1 |
| Status text | always the `*-ink` token, never the base hue |
| `--accent-contrast` on `--accent` | ≥ 4.5:1 in both themes |

| Component | 3:1 against |
| --- | --- |
| Button borders, input borders, focus ring | adjacent surface |
| Chips and badges | their fill |
| Progress fill, ring track | `--bg-alt` |
| Icons that carry meaning | their background |

### Touch targets

- Minimum 44×44px for anything tappable: `.btn` (44px), `.icon-btn` (40px + 4px gap), `.pager a` (40px), drawer rows (full width), `.quiz-opt` (≥ 44px).
- 8px minimum between adjacent targets; the drawer uses 4px gaps between full-width rows, which is fine because the rows are the targets.
- Never shrink targets below 36px (`.btn-sm`) on touch surfaces.

### Keyboard navigation

| Key | Action |
| --- | --- |
| Tab / Shift+Tab | move through links, buttons, inputs, `<summary>`, radios |
| Enter / Space | activate buttons and summaries; Space checks a radio |
| Arrow keys | move within a radio group (tabs, quiz options) |
| Escape | closes the mobile drawer (nsds.js), closes `<dialog>` |
| Skip link | first Tab on every page reveals "Skip to content" |

Dropdowns open on `:focus-within`, so tabbing into a child opens the menu without a mouse.

### Assistive technology

- One `<h1>` per page; headings descend without skipping levels.
- Landmarks: `<header>`, `<nav aria-label>`, `<main id="main">`, `<aside aria-label>`, `<footer>`.
- Decorative SVG gets `aria-hidden="true"`; icon-only controls get `aria-label`.
- Current item: `aria-current="page"` on the nav link or `.nav-current` on the `<li>`.
- Progress: give `.progress` a `role="progressbar"` with `aria-valuenow` when it carries meaning.
- Reduced motion is honoured globally; nothing depends on an animation to be understood.

---

## Gestures

| Gesture | Use |
| --- | --- |
| Tap | activate; whole cards are targets (`.card-link::after`) |
| Scroll | vertical page; horizontal only on `.path` and `.marquee` |
| Swipe | scroll-snap on `.path` steps |
| Long press / double tap / pinch | not used |
| Drag | not used |

---

## Content design

- Sentence case everywhere; kickers and labels are uppercase by CSS, not by typing.
- Chip text comes from a tag's **description**, never parsed from a slug.
- Buttons start with a verb: "Start lesson 1", "Mark complete", "Join free".
- Measure ≤ 60ch for prose, ≤ 42ch for lead paragraphs in tiles.
- Numbers use tabular figures; durations read "18 min", "3 h 10 min".
- No exclamation marks, no "click here", no lorem ipsum in shipped pages.
- Empty states say what to do next, not only that nothing is here.

---

## Do's and Don'ts

### Color
- Do paint with semantic tokens only; raw ramps appear in `_tokens.scss` alone.
- Do keep the two dark blocks (`html[data-theme="dark"]` and the `prefers-color-scheme` copy) identical.
- Don't introduce a second accent; amber is for level chips, not for CTAs.
- Don't put text in `--warning` or `--error`; use the ink token.

### Shape
- Do use `--radius-lg` for containers, `--radius-sm` for controls, pills for facts.
- Don't mix radii inside one component.

### Elevation
- Do reserve `--shadow-lg` for things that float (dropdowns, browser frames, modals, hover).
- Don't shadow resting cards; a hairline is enough.

### Interaction
- Do lift on hover and ring on focus; both are already in the components.
- Do use `.is-current`, `.is-done`, `.is-locked` on list items, not on links.
- Don't rely on hover for anything essential; the drawer and dropdowns work by focus and tap too.

### Layout
- Do build every page as `.outer > .inner` bands and alternate `.section-alt`.
- Do keep tables inside `.table-wrap`.
- Don't set widths on `.inner`; change the measure with `.inner-narrow` or a token.
- Don't let anything scroll horizontally except `.path` and `.marquee`.

### Typography
- Do write sizes in rem against the 10px base (`1.6rem` = 16px).
- Don't load Google Fonts; Figtree ships in `dist/fonts/`.

### Motion
- Do use `--dur` and `--ease`; never write a raw `0.3s ease`.
- Don't animate layout properties (width, height, top) except the reader rail's grid track.

### Components
- Do compose from existing pieces (a `.widget` holding a `.ring`) before adding a partial.
- Do add a new partial in the right layer and `@use` it in `screen.scss` in cascade order.
- Don't nest SCSS, write mixins or functions; the API is class names and custom properties.
- Don't ship without `npm run build`; `dist/` is committed and CI fails on drift.

---

## Quality gates

1. `python3 checkclasses.py page.html` reports zero unknown classes.
2. Page renders at 360px with no horizontal scroll.
3. Both themes checked (toggle in the header).
4. Keyboard walk: Tab reaches every control; Escape closes the drawer.
5. One h1; landmarks present; icons hidden from AT.
6. `git diff --exit-code` after `npm run build` is clean.
