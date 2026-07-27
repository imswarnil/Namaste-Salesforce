# Namaste Salesforce Design

A design system for **Namaste Salesforce**, an open-source Ghost theme (`imswarnil/Namaste-Salesforce`) for Salesforce learning communities: courses, a training roadmap, developer documentation, and a blog, all in one calm, fast, accessible package.

*Why "Console" styling?* Apex is Salesforce's own programming language — and the whole visual language here (mono indices, code-comment kickers, hairline borders, terminal-row lists) is built to feel like a developer console, not a marketing site. See **Design Principles** below.

**Sources used to build this system** (not attached to this project — explore them yourself for deeper context or to extend this system):
- GitHub repo: [imswarnil/Namaste-Salesforce](https://github.com/imswarnil/Namaste-Salesforce) — the Ghost theme itself. Read `assets/css/screen.css` (Tailwind v4 `@theme` tokens), `assets/css/theme/*.css` (the LMS component layer: `tokens.css`, `base.css`, `components.css`, `navbar.css`, `course.css`), `training-docs.md` (how the training roadmap's tags/routes fit together), `dummy-content/*.json` (real sample course & lesson copy), and `prompt.md` (the brand's own image-generation style guide — useful for commissioning matching illustrations).

**Important caveat:** the repository as attached contains no `.hbs` template files — only the compiled design tokens, CSS, self-hosted fonts/icons, and dummy content JSON. The theme's actual page layouts (`home.hbs`, `courses.hbs`, `training.hbs`, partials, etc.) described in its own README were not present to read. Everything here — the components and the LMS UI kit — was reconstructed from the CSS component classes (`.ns-ccard`, `.ns-curriculum`, `.ns-road__*`, `.ns-course-hero`, etc.), their extensive inline comments, and the dummy content copy. If you have the missing `.hbs`/`partials/` files, attach them and this system can be tightened to match exactly.

## Design Principles

This system is not "brand blue on white Tailwind cards." It follows **five explicit rules**, borrowed from developer-tool product design (Mux, Vercel, Linear) rather than marketing-site conventions — every component in `components/` inherits them, and any new component should be checked against this list before it ships.

1. **The hairline is the structure, not the shadow.** Cards, inputs, and tags are built from a single `1px` border (`--color-border`). Soft drop-shadows are almost entirely retired (`--shadow-card` is nearly flat) — elevation comes from a border brightening to brand-blue on hover, never a floating lift.
2. **Monospace is a structural material, not a code-block accessory.** JetBrains Mono renders every index, duration, timestamp, status tag and section kicker — Inter is reserved for prose and headings. This is what makes a list of lessons read as *data* and a paragraph read as *writing*, without touching color.
3. **One signal color.** Brand blue (`#0176D3`) is the only color that means "interactive" or "active." Status (success/warning/error) shows as a small dot + mono text, never a background wash — so a screen with a solid blue button on it has exactly one obvious next action.
4. **Sharp, specific geometry.** `--radius-card` (6px) and `--radius-btn` (4px) replace the generic "12px + pill-everywhere" look; `--radius-pill` is reserved for true pills (tags). Nothing is rounded just because rounding is the default.
5. **Motion is instant, not springy.** State changes (hover, press, active) resolve in 120–180ms with a plain ease-out — no bounce, no scale-pop, no translateY lift on hover. The one exception is the small float loop on decorative illustrations. This is what makes the UI feel like a precise tool, not a marketing page.

Two supporting motifs worth naming: **the code-comment kicker** (`// Getting started`, borrowed from the theme's own Apex/SOQL comment voice) replaces a pastel eyebrow pill everywhere a section label is needed, and **the mono index** (`01`, `02`…) appears on every list/card/roadmap item as a first-class visual element, not a hidden a11y label.

## Product

One product: **Namaste Salesforce**, a Ghost LMS theme with five page families — a marketing home, a course catalog + course/lesson pages, a training roadmap, a documentation hub, and a blog. The identity: *calm, flat, reading-first* — one working blue, hairline borders, small shadows, generous white space, flash-free dark mode. Explicitly no gradients, glassmorphism, glow, or neon.

## Content fundamentals

- **Voice:** plain-English, encouraging, practical. Explains *why*, not just *what* — e.g. lesson copy walks from "an org is..." to a concrete next action ("try creating a custom object called Project…").
- **Person:** second person for instruction ("You'll learn to navigate Lightning Experience…"), third person for the product/ecosystem itself.
- **Structure:** every lesson follows the same shape — a plain-English concept, a concrete example or code block, then a bridge to the next lesson ("Next, we'll turn this data into insight…").
- **Casing:** sentence case everywhere (headings, buttons, nav) except short uppercase kickers/eyebrows and lesson-type badges, which are intentionally all-caps with wide letter-spacing.
- **No emoji** in product copy or UI (the source repo's own README uses a few emoji as bullet markers, but this is a maintainer-doc convention, not a UI pattern — the app itself carries none).
- **Numbers used sparingly and only when concrete**: "75%+ coverage", "200-record data load", "five sections" — never decorative stats.

## Visual foundations

Governed by the five Design Principles above. In short:

- **Color:** one working blue (`#0176D3`) carries every interactive/active signal. Status colors show as a dot + mono text, never a tinted background fill.
- **Dark mode:** semantic role tokens (`--color-surface`, `--color-ink`, `--color-muted`, `--color-border`) flip under `[data-theme="dark"]` on `<html>`, resolving to the brand navy scale (`--color-brand-800`/`900`) rather than a generic slate — dark mode is *this brand's* console, not a GitHub reskin.
- **Type:** Inter for headings/prose (800 heading weight, 400 body); JetBrains Mono for every index, label, timestamp and status tag, uppercase and letter-spaced (`--tracking-label`).
- **Geometry:** `--radius-card` 6px, `--radius-btn` 4px — sharp and specific, not "rounded because rounded." `--radius-pill` only for true pill tags.
- **Elevation:** a `1px` hairline border is the primary structuring device; hover brightens the border to brand-blue (or draws a left/top accent line), it never lifts on a shadow.
- **Spacing:** Tailwind's default 4px scale; no custom spacing tokens layered on top.
- **Backgrounds:** a faint hairline grid dissolving via a radial mask, used behind dark hero sections only. No photography, no gradients, no hand-drawn illustration.
- **Motion:** fade-up entrance + one gentle float loop (illustrations only); everything else is a 120–180ms plain ease-out. No springs, no bounce, no hover-lift.
- **Hover/press:** hover = border brightens to brand-blue + an accent line (top on cards, left on rows); press = instant opacity dim. No color-lightening, no scale-pop except the video-poster play ring and card-media zoom (1.03–1.05x).
- **Cards:** `1px` hairline border + `6px` radius, no shadow at rest; brand-blue border + top accent line on hover.

## Iconography

- **Phosphor icons**, self-hosted and **subsetted** to the ~130 glyphs the theme actually uses (`assets/fonts/phosphor-subset.woff2` + `phosphor-fill-subset.woff2`, generated by the source repo's `scripts/subset-icons.py`). Use via `<i class="ph ph-name">`; filled variants use `ph-fill`. See `guidelines/icons.card.html` for the glyphs copied into this project and `assets/css/theme/icons.css` for the full generated class list.
- No PNG/SVG icon library, no unicode-symbol icons, no emoji as icons.
- A handful of inline-SVG *chrome* icons (nav, theme toggle) exist in the original theme's `partials/icons/` — not present in the attached repo, so this system uses Phosphor for those spots too (a reasonable substitution: same stroke weight, same visual family).

## What's in this project

- `styles.css` — the single stylesheet entry point; imports everything below.
- `tokens/` — `colors.css` (brand/accent scale, status colors, semantic light/dark roles), `fonts.css` (`@font-face` for Inter, JetBrains Mono, metric-matched fallback), `typography.css` (font stacks + type scale), `effects.css` (radius, shadow, motion tokens + keyframes), `base.css` (element resets, focus ring, selection, link colors).
- `assets/` — `logo/favicon.svg` (brand mark), `fonts/` (self-hosted woff2s), `img/` (the two source illustrations: `publication-cover.svg`, `training-trail.svg`), `css/theme/icons.css` (generated Phosphor subset), `screenshot-desktop.jpg`/`screenshot-mobile.jpg` (the source repo's own repo-preview screenshots — these show the *upstream Casper fork's* default Ghost content, not this theme's LMS screens, so treat them as a rough visual-tone reference only).
- `components/core/` — **Button**, **Kicker**, **Chip**, **Badge**, **Input**, **AvatarRing**, **Logo**, **Navbar**, **Footer**, **Hero**, **TableOfContents**, **TimelineStepper**, **CodeBlock**, **CodePanel** (SLDS syntax highlighter with light/dark toggle).
- `components/course/` — **CourseCard**, **LevelBadge**, **CurriculumList** (list/cards/detailed/timeline), **VideoPoster**, **CourseStats**, **RoadmapCard**, **AuthorBox**, **AdSlot**, **BlogCard**, **TrainingCard**, **ResourceCard**.
- `guidelines/` — 17 foundation specimen cards (colors, type, radii/shadows, motion, logo lockups, favicon, 9 background patterns, icons) shown in the Design System tab.
- `learn/` — 4 educational cards ("1. Learn Design System" group): what a design system is, how to use this one, how real companies use design systems, and the 9-step process to build one successfully.
- `ui_kits/lms/` — an interactive click-through of the LMS product: Home, Courses catalog, Course detail, Course/Training **Player** (video + TOC + stepper + code block), Training roadmap, **Blog**, **Resources**, Documentation hub — with a working dark-mode toggle.
- `SKILL.md` — Claude Code / Agent Skills-compatible packaging of this system.

### Intentional additions
No component inventory was defined by an attached codebase's actual component library (no `.jsx`/`.tsx`/Figma component set) — only CSS classes and their usage comments. The component list above was authored to cover every distinct visual pattern documented in `assets/css/theme/{components,course}.css`; nothing beyond that was invented.

## Caveats & how to help

- No `.hbs` templates were available, so exact page structure (header/footer chrome, homepage sections beyond the hero, the docs sidebar's real content) is a reconstruction from CSS + dummy content, not a byte-for-byte recreation. **Attach the theme's `partials/` and top-level `.hbs` files** if you have them, and this system can be corrected against the real markup.
- The two `screenshot-*.jpg` assets in this repo are the *generic Ghost Casper* preview images, not this theme's actual screens — don't use them as ground truth for the LMS layouts.
- No real logo mark exists beyond `assets/logo/favicon.svg` (a generic Ghost-style icon) — if Namaste Salesforce has since designed a proper wordmark/logo, please attach it.
- Icons inside Ghost post *content* (vs. template chrome) are icon-font glyphs from a `CONTENT_SAFELIST` we don't have visibility into — if specific lesson pages use icons not in the subset shipped here, re-run `scripts/subset-icons.py` upstream and re-copy the woff2s.
