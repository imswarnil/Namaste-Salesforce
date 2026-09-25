# NS Design System — DESIGN.md

> **Always read this file first.** It is the token reference for the design system behind Namaste Salesforce (https://salesforce.imswarnil.com). Rules and accessibility live in [design-guidelines.md](./design-guidelines.md); component specs live in [design-components.md](./design-components.md). Machine index: [llms.txt](./llms.txt).

NS Design System is a token-first, dependency-free CSS system for a Salesforce learning publication: one accent blue, a navy gray ramp, Figtree, a 10px rem base, light and dark themes flipped entirely through custom properties. It is compiled from 53 plain-CSS SCSS partials into one stylesheet and consumed by the Namaste Salesforce Ghost theme (Handlebars) and any static page.

- Stylesheet: `https://salesforce.imswarnil.com/dist/css/screen.min.css`
- Optional runtime (5 KB): `https://salesforce.imswarnil.com/dist/js/nsds.js`
- Source: `design-system/` inside https://github.com/imswarnil/Namaste-Salesforce

---

## Colors

Raw ramps live on `:root` and never change. Everything a component paints with is a **semantic token**, defined once for light and once for dark. Components never use raw hex.

### Brand — Salesforce Lightning blue

| Token | Hex | Usage |
| --- | --- | --- |
| `--brand-50` | `#eef6ff` | tints, `--accent-soft` (light) |
| `--brand-100` | `#d8edff` | tints |
| `--brand-200` | `#b0d7ff` | breakpoint bar, decorative |
| `--brand-300` | `#7cbeff` | `--accent-strong` (dark), on-dark kickers |
| `--brand-400` | `#1b96ff` | `--accent` (dark), gradient end |
| `--brand-500` | `#0176d3` | `--accent` (light) — **the one blue** |
| `--brand-600` | `#0b5cab` | `--accent-strong` (light), `--info-ink` |
| `--brand-700` | `#03386b` | deep tints |
| `--brand-800` | `#032d60` | `--gray-800` alias, navy |
| `--brand-900` | `#001a3e` | `--gray-900` alias, headings (light) |

### Grays — the navy ramp

| Token | Hex | Usage |
| --- | --- | --- |
| `--gray-50` | `#f4f6f8` | `--bg-alt`, `--surface-alt`, `--code-bg` (light) |
| `--gray-100` | `#eaeef3` | inverse-button hover |
| `--gray-200` | `#dddbda` | `--border` (light) |
| `--gray-300` | `#c6ccd4` | ghost-button hover ring, footer headings |
| `--gray-400` | `#98a6b8` | `--text-faint` (light), `--text` (dark) |
| `--gray-500` | `#5c5a57` | `--text-muted` (light) |
| `--gray-600` | `#45566b` | `--text-faint` (dark) |
| `--gray-700` | `#2c3e56` | reserved |
| `--gray-800` | `#032d60` | brand navy |
| `--gray-900` | `#001a3e` | `--heading` (light), tooltips, toasts |
| `--gray-950` | `#051222` | `--bg` (dark), footer, cinema bands |

### Semantic tokens

| Token | Light | Dark | Role |
| --- | --- | --- | --- |
| `--bg` | `#ffffff` | `#051222` | page |
| `--bg-alt` | `#f4f6f8` | `#081a33` | alternating band |
| `--surface` | `#ffffff` | `#0a1f3c` | cards, widgets, panels |
| `--surface-alt` | `#f4f6f8` | `#081a33` | raised-on-raised |
| `--border` | `#dddbda` | `rgba(152,166,184,.18)` | hairlines |
| `--border-soft` | `rgba(221,219,218,.55)` | `rgba(152,166,184,.1)` | dividers that whisper |
| `--text` | `#1a2b45` | `#98a6b8` | body |
| `--text-muted` | `#5c5a57` | `#7d8fa6` | secondary |
| `--text-faint` | `#98a6b8` | `#45566b` | meta, counters |
| `--heading` | `#001a3e` | `#f4f6f8` | headings, strong |
| `--accent` | `#0176d3` | `#1b96ff` | the signal |
| `--accent-strong` | `#0b5cab` | `#7cbeff` | hover |
| `--accent-soft` | `#eef6ff` | `rgba(27,150,255,.12)` | tint, current state |
| `--accent-contrast` | `#ffffff` | `#051222` | ink on accent |
| `--header-bg` | `rgba(255,255,255,.85)` | `rgba(5,18,34,.8)` | translucent bars |
| `--code-bg` | `#f4f6f8` | `#08192f` | inline code |
| `--scrim` | `rgba(5,18,34,.45)` | `rgba(0,0,0,.6)` | modal backdrop |

### Status

Fills and strokes take the base hue; **text takes the ink** (`#fe9339` on white is 2.2:1 and fails AA).

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--success` / `--success-ink` | `#2e844a` / `#1a6b34` | — / `#4fbf72` | done, correct, positive delta |
| `--warning` / `--warning-ink` | `#fe9339` / `#8a4b00` | — / `#f2a341` | caution |
| `--error` / `--error-ink` | `#ea001e` / `#ba0017` | — / `#ff6b7a` | wrong answer, destructive, live dot |
| `--info` / `--info-ink` | `#0176d3` / `#0b5cab` | — / `#7cbeff` | informational alerts |
| `--level-ink` | `#8a5a00` | `#d9a03f` | course level chips (intermediate+) |
| `--featured-ink` | `#7c4a03` | `#f2b661` (chip) | featured chip |

---

## Typography

Face: **Figtree** (variable 300–900, normal + italic, latin + latin-ext, self-hosted woff2). Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif`. Mono: `"SF Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace`.

Base: `html { font-size: 62.5% }` so **1rem = 10px**. Body 1.6rem / 1.6.

| Style | Size | Weight | Line height | Tracking |
| --- | --- | --- | --- | --- |
| Hero display (`.hero h1`) | clamp(3.6rem, 6.5vw, 6.4rem) | 700 | 1.05 | -0.03em |
| h1 | clamp(3.2rem, 5vw, 4.6rem) | 700 | 1.2 | -0.025em |
| h2 | clamp(2.4rem, 3.5vw, 3.2rem) | 700 | 1.2 | -0.015em |
| h3 | 2.1rem | 700 | 1.2 | -0.015em |
| h4 | 1.8rem | 700 | 1.2 | -0.015em |
| h5 | 1.6rem | 700 | 1.2 | — |
| h6 | 1.4rem uppercase | 700 | 1.2 | 0.05em |
| Lead (`.hero-lead`, `.docs-lead`) | 1.8–2rem | 400 | 1.6 | — |
| Body | 1.6rem | 400 | 1.6 | — |
| Article (`.gh-content`) | 1.75rem | 400 | 1.7 | — |
| Small / meta | 1.3–1.45rem | 400–600 | 1.5 | — |
| Kicker (`.kicker`) | 1.2rem uppercase | 700 | 1 | 0.1em |
| Label (`.card-eyebrow`, `.widget-title`) | 1.2–1.25rem uppercase | 700 | 1 | 0.07–0.08em |
| Code | 1.35rem mono | 400 | 1.6 | — |

Headings use `text-wrap: balance`. Stat and counter numbers use `font-variant-numeric: tabular-nums`.

---

## Shape

| Token | Radius | Components |
| --- | --- | --- |
| `--radius-sm` | 6px | buttons, inputs, chips (rect), kbd, small controls |
| `--radius` | 10px | alerts, callouts, tables, code, tab panels, widgets inside rails |
| `--radius-lg` | 16px | cards, widgets, tiers, modals, quiz questions, frames |
| `--radius-full` | 999px | pills: chips, badges, progress, marquee chips |

---

## Elevation

| Level | Token | Shadow (light) | Usage |
| --- | --- | --- | --- |
| 0 | — | none, `1px solid var(--border)` | resting cards, inputs |
| 1 | `--shadow-sm` | `0 1px 2px rgba(5,18,34,.06)` | pill tab, kbd |
| 2 | `--shadow` | `0 0 0 1px rgba(5,18,34,.03), 0 4px 16px rgba(5,18,34,.07)` | hover on buttons, lesson-nav |
| 3 | `--shadow-lg` | `0 0 0 1px rgba(5,18,34,.04), 0 12px 40px rgba(5,18,34,.12)` | card hover, dropdowns, browser frames, modals |

Dark theme swaps all three for black-based shadows with a faint gray ring.

---

## Interaction states

| State | Treatment |
| --- | --- |
| Enabled | token colours, `1px` border |
| Hover | colour → `--accent-strong` / `--heading`; cards and buttons lift `translateY(-1…-3px)` + shadow |
| Focus | `:focus-visible` → `2px solid var(--accent)`, `outline-offset: 2px` |
| Active / pressed | no lift (transform reset) |
| Current | `--accent` ink on `--accent-soft` fill (nav, rails, tabs, pager) |
| Done | green check disc (`--success`) in rails, trail, steps |
| Locked | `opacity: .55`, lock icon, "Members" chip |
| Disabled | `aria-disabled="true"` + `opacity: .5; pointer-events: none` (inline) |

---

## Layout

| Class | Width | Panes | Navigation |
| --- | --- | --- | --- |
| Compact | < 600px | 1 | drawer (burger), sticky `.lesson-bar` |
| Medium | 600–899px | 1 | drawer (burger) |
| Expanded | 900–1279px | 1–2 (sidebar folds ≤1023) | inline nav + dropdowns; reader rail ≥1024 |
| Wide | ≥ 1280px | 2–3 (TOC column appears) | inline nav; rail + article + TOC |

Grammar: `.outer` (page gutter `max(4vmin, 20px)`) → `.inner` (`max-width: 1200px`) → `.section` band rhythm `clamp(4.8rem, 8vmin, 8rem)`. Prose measure `--measure: 720px`; wide `--measure-wide: 1120px`; reader rail `--rail-w: 320px`; header `--header-height: 64px`.

---

## Motion

| Token | Value | Use |
| --- | --- | --- |
| `--ease` | `cubic-bezier(0.2, 0, 0, 1)` | everything by default |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | entrances, pulses |
| `--dur-fast` | 150ms | colour, border, opacity |
| `--dur` | 220ms | transforms, chevrons, drawers |
| `--dur-slow` | 400ms | progress bars, trail line |

Only `transform`, `opacity` and colours animate. `prefers-reduced-motion: reduce` zeroes every duration in the reset and stops the marquee.

---

## Stacking

| Token | Value | What sits there |
| --- | --- | --- |
| `--z-raised` | 10 | tooltips, hover cards |
| `--z-sticky` | 100 | sticky rails, `.lesson-bar`, rail toggle |
| `--z-drawer` | 290 | mobile navigation drawer |
| `--z-header` | 300 | `.site-head` |
| `--z-modal` | 400 | `<dialog>` |
| `--z-toast` | 500 | toasts, skip link |

---

## Icons

24×24 viewBox, 1.8 stroke (2 for chevrons), round caps and joins, `currentColor`, `aria-hidden="true"`. Sizes: 1.3–1.4rem in chips and meta, 1.6rem in nav and buttons, 2rem in icon buttons, 2.2rem in prop tiles, 2.8rem in empty states.

---

## Design tokens — naming

`--{family}-{step}` for ramps (`--brand-500`), `--{role}` for semantics (`--surface`), `--{role}-{modifier}` for variants (`--accent-soft`, `--success-ink`), `--{measure}` for rhythm (`--gap-lg`), `--z-{layer}`, `--dur-{speed}`. New values become tokens in `src/scss/0-abstracts/_tokens.scss` before any component uses them.
