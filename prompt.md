# Image prompt — the Namaste Salesforce style

Copy the master prompt, fill the `[SUBJECT]` and `[TYPE]` blanks, and
paste it into any image model (Midjourney, DALL·E, Ideogram, Firefly,
Recraft…). It encodes the same design system the theme's generated
thumbnails use (`build-thumbnails.py`), so hand-made art and generated
art sit side by side without clashing.

---

## Master prompt

> Flat vector illustration for a Salesforce learning platform, in a
> clean engineering-blueprint style. Deep navy canvas (#032d60, shading
> toward #051222 at the edges), with a single soft radial glow of
> electric blue (rgba 27,150,255 at 35%) behind the focal point.
> Accent color is Salesforce electric blue #1b96ff with a deeper blue
> #0176d3 for secondary strokes; white (#ffffff) reserved for the main
> subject's linework and text. Decorative geometry, used sparingly: a
> faint blueprint grid (thin lines, blue at ~15% opacity), one thin
> dashed circle with round dash caps, a small grid of dots at ~12%
> white, one small solid blue dot. The focal subject sits inside or
> beside a rounded-square tile (large corner radius, translucent blue
> fill at ~16%, 2px blue stroke at ~55%). All linework in a single
> consistent stroke weight — rounded caps, rounded joins, like icons
> drawn on a 24px grid at 1.8px stroke. No gradients except the one
> glow, no textures, no photorealism, no 3D, no drop shadows, no
> people's faces, generous negative space. Composition: subject
> weighted to the right two-thirds, left third kept calm for a title.
> Aspect ratio 16:9, 1200×675.
>
> Subject: **[SUBJECT]** — e.g. "a branching flowchart with decision
> diamonds and a lightning bolt", "a database cylinder connected to
> three record cards", "a rocket launching from a cloud console".
>
> This is a **[TYPE]** (see the type notes below).

---

## Type notes — swap in one of these

**Blog illustration** — looser and more editorial: the subject can be
a metaphor (a compass over a map of nodes, a ladder into a cloud).
Keep the left-third calm; the theme overlays no text on blog art, so
the drawing may breathe more.

**Course thumbnail** — most structured: one clear hero object centered
in the rounded tile, right of center, reading at card size (~300px).
Think "one icon promoted to a poster". No fine detail smaller than a
stroke width.

**Video thumbnail** — calmest of all: solid navy, the subject small
and centered or a faint tiled icon pattern at ~7% white; the theme
overlays its own play badge and duration chip, so leave the corners
empty and add no play button.

**Tag / topic badge** — square 1:1, 600×600: the tile fills most of
the frame, one bold monogram or single glyph inside, dashed ring
around it. Must read at 20px.

**Hero / section art** — wide 21:9 allowed: several small subjects
drifting on the grid (cloud, bolt, database, code brackets) as
floating tiles, connected by one thin dashed path — the site's
"trail" motif.

---

## Palette (exact)

| Role | Hex |
| --- | --- |
| Canvas navy | `#032d60` |
| Canvas edge / near-black | `#051222` |
| Accent (primary strokes, glow) | `#1b96ff` |
| Accent deep (secondary strokes) | `#0176d3` |
| Subject linework / text | `#ffffff` |
| Success green (rare, one element max) | `#2e844a` |

Type, if any text is drawn: Figtree (or a close geometric sans),
kicker lines uppercase with wide letter-spacing in `#1b96ff`, titles
white and heavy (800).

## Negative prompt

> photorealistic, 3D render, glossy, skeuomorphic, stock-photo people,
> faces, hands, Salesforce logo, official trademarks, neon rainbow,
> purple/pink gradients, texture noise, paper grain, drop shadows,
> busy background, text watermarks

## Ratios cheat-sheet

- Post / course / video thumbnail: **16:9** (1200×675)
- Tag badge: **1:1** (600×600)
- Hero band: **21:9**

Feature images go into Ghost as usual; anything written straight to
the DB needs the `__GHOST_URL__` token (see NAMASTE-SALESFORCE.md).
