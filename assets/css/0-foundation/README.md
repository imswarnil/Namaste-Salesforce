# 0-foundation — the SFUI foundation layer

Everything above this layer (`1-elements/` components, templates, off-site
brand assets) is built from the variables defined here. Change a token here
and the site, the course pages, and the YouTube/blog covers all follow.

## Files (imported in this order by `assets/css/screen.css`)

| File | What it owns |
| --- | --- |
| `fonts.css` | Self-hosted Inter + Fira Code variable fonts, metric-matched fallback |
| `icons.css` | **Generated** Phosphor subset — never edit; re-run `scripts/subset-icons.py` |
| `colors.css` | Brand/accent blue scales, status colors, semantic roles (`surface` / `ink` / `muted` / `border` / `label` / `grid`) and their light/dark values |
| `typography.css` | Font stacks, the prose scale (`--size-display` … `--size-small`) and the mono/label scale (`--size-label`, `--tracking-label`) |
| `spacing.css` | Semantic rhythm (`--space-card/gap/row/section/gutter`), navbar height, containers, cover safe-area |
| `borders.css` | Border widths (`--border-hairline/strong`) + corner radii (`--radius-card/btn/sm/pill`) |
| `elevation.css` | Shadows (`--shadow-card/raised/brand/focus`) + the z-index ladder (`--z-*`) |
| `motion.css` | Easing (`--ease-out`), durations (`--duration-fast/base`), keyframes + `animate-*` tokens |
| `mixins.css` | `@utility` recipes — `ns-label`, `ns-index`, `ns-hairline`, `ns-dot-marker`, `ns-transition` (markup classes AND `@apply`-able) |
| `backgrounds.css` | Brand patterns (`.bg-grid`, `.bg-dots`, `.bg-lines`, …) and the `.ns-cover-*` canvases for content assets |

Element defaults (body, headings, scrollbar, focus ring) now live in
`../1-elements/base.css` — this layer holds no selectors that paint UI.

## Design principles (the "Developer Console" rules)

1. **The hairline is the structure, not the shadow.** One 1px border
   (`--color-border`); shadows near-flat. Elevation = border brightens to
   brand blue on hover, never a floating lift.
2. **Monospace is a structural material.** Fira Code renders every
   index, duration, timestamp, status tag and kicker — Inter is for prose
   and headings only.
3. **One signal color.** Brand blue `#0176D3` is the only color that means
   "interactive". Status shows as a dot + mono text, never a background wash.
4. **Sharp, specific geometry.** Cards 6px, buttons/inputs 4px;
   `--radius-pill` only for true pills (tags).
5. **Motion is instant.** 120–180ms plain ease-out; no spring, no bounce,
   no hover-lift. The one exception: the float loop on illustrations.

Supporting motifs: the **code-comment kicker** (`// Getting started`) instead
of pastel eyebrow pills, and the **mono index** (`01`, `02`, …) as a
first-class visual element on lists, cards and roadmap items.

## Using the foundation for content assets

Build covers on a `.ns-cover ns-cover--video` (16:9 YouTube), `--square`
(Instagram), `--story` (9:16) or `--banner` canvas: navy ground, a
`.bg-grid-corner` layer, headline in `--font-heading` at `--size-display`,
kicker in `--font-mono` uppercase with `--tracking-label`, one brand-blue
accent. See `design-system/brand-content-creation/` for full specs.
