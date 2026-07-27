# prompt.md — image prompts for Namaste Salesforce

Copy-paste prompts for generating thumbnails, feature images and OG cards that
match this theme. Any image model works (Midjourney, Imagen, DALL·E, Ideogram,
Firefly); the wording is model-agnostic.

**How to use:** paste the [Base style block](#the-base-style-block) verbatim,
then append one [recipe](#recipes). Replace `{{…}}` placeholders. Check the
result against the [rejection list](#reject-the-image-if).

---

## The design language, in one paragraph

The theme is **calm, flat and reading-first**: one working blue, hairline
borders, small shadows, generous white space. Explicitly **no gradients, no
glassmorphism, no glow, no neon, no 3D render sheen**. Salesforce-adjacent
(SLDS-inspired) without copying Salesforce branding. Images are supporting
illustration, never the loudest thing on the page — the text is.

### Palette (exact hex — do not substitute)

| Role | Hex | Use in images |
| --- | --- | --- |
| Primary blue | `#0176D3` | the one saturated colour — lines, key shapes, accents |
| Bright blue | `#1B96FF` | second blue, for a lighter plane |
| Sky | `#7CBEFF` | tints, fills |
| Pale blue | `#D8EDFF` | large soft fills |
| Blue wash | `#EEF6FF` | background tint on light images |
| Deep navy | `#032D60` | dark ink, the dark-image background |
| Darkest navy | `#001A3E` | dark-image background alternative |
| Ink | `#181818` | text / strong lines on light |
| Muted | `#706E6B` | secondary lines |
| Border | `#DDDBDA` | hairlines, 1px rules |
| Surface | `#FFFFFF` | light background |
| Sunken | `#F3F3F3` | panel fill |
| Success green | `#2E844A` | **only** for a checkmark / "done" state |
| Warning amber | `#FE9339` | sparingly, one accent max |

Rule of thumb: **white/near-white ground + blues + one ink** — that is the whole
palette for most images. Green and amber appear at most once, as a single mark.

### Recurring motifs

Reuse these so images read as one family:

- **48px faint grid** dissolving toward one side (the site's `bg-grid-corner`)
- **dashed trail / path** with dots as stops — the training roadmap metaphor
- **rounded rectangles, radius ≈ 12px**, with **1px hairline borders**
- **pill shapes** for chips and buttons
- **abstract UI panes** — a toolbar bar, three list rows, a small chart — with
  no legible text, only grey placeholder bars
- geometry over realism: circles, arrows, nodes, stacked cards

### Typography inside images

Prefer **no text at all** — headings live in HTML, not baked into the picture.
If a word is unavoidable, use **Inter, semi-bold, one or two words maximum**.
Never render paragraphs; use grey placeholder bars instead.

---

## The base style block

Paste this first, every time:

```
Flat vector illustration, minimal and calm, generous negative space.
Strict palette: white #FFFFFF background, primary blue #0176D3, bright blue
#1B96FF, sky #7CBEFF, pale blue #D8EDFF, deep navy #032D60, ink #181818,
grey hairlines #DDDBDA. No other colours.
Style: clean geometric shapes, rounded rectangles with 12px corner radius and
1px hairline borders, thin consistent stroke weight, subtle 48px faint grid
dissolving toward one edge, soft flat shadow at most.
Strictly avoid: gradients, glassmorphism, glow, neon, drop shadows with blur,
3D renders, gloss, photorealism, stock-photo people, clutter, lens flare,
text and lettering, watermarks, logos, Salesforce trademarks or the Salesforce
cloud mark.
Composition: centred subject, wide margins, flat front-on or light isometric
view. Feels like a modern documentation site illustration.
```

Append aspect + subject from the recipes below.

---

## Sizes

| Where | Ratio | Pixels | Notes |
| --- | --- | --- | --- |
| Post / lesson feature image | 16:9 | 1600×900 | Ghost resizes; upload large |
| Open Graph / Twitter card | 1.91:1 | 1200×630 | keep the subject centred — edges get cropped |
| Training section tag image | 16:9 | 1200×675 | shown small in the roadmap card thumb — **must read at 96px** |
| Course card | 16:9 | 1200×675 | |
| Author avatar | 1:1 | 512×512 | |
| Inline in-content figure | 16:9 or 4:3 | 1200×675 | |

**The small-size test:** section and course thumbnails render tiny. One idea,
big, centred. If it needs squinting at 96px, it's wrong.

---

## Recipes

### Training section thumbnail

```
{{BASE}}
Aspect ratio 16:9.
Subject: a single bold abstract icon representing {{TOPIC}}, drawn as flat
geometry in #0176D3 on a white ground, sitting on a short dashed path with two
small filled dots either side of it — one stop on a longer journey. The dashed
path is #7CBEFF. A faint 48px grid fades in from the right edge. One idea only,
very large, centred, readable at thumbnail size.
```

Topic shapes that have worked:

| Section | `{{TOPIC}}` |
| --- | --- |
| Foundations / getting started | a flag planted on a small rise |
| Org setup | interlocking gear and a toggle switch |
| Navigation | a compass rose beside a simplified app window |
| Data model | three linked rounded rectangles as database tables joined by lines |
| Security | a shield with a keyhole, beside a permission grid of dots |
| Automation | a branching flow diagram, three nodes and a decision diamond |
| Reports & dashboards | a bar chart and a donut chart in one panel |
| Apex / code | an editor window with grey placeholder code bars |

### Lesson feature image (video)

```
{{BASE}}
Aspect ratio 16:9.
Subject: an abstract video player frame — a rounded rectangle with a 1px
#DDDBDA border, a solid #0176D3 play triangle in a white circle at centre, and
a thin progress bar along the bottom in #7CBEFF with one #0176D3 filled
segment. Behind it, a faint grid dissolving to the left. Small floating
rounded chips suggesting {{TOPIC}} around the frame. No text.
```

### Lesson feature image (reading / exercise)

```
{{BASE}}
Aspect ratio 16:9.
Subject: a light isometric arrangement of two or three abstract UI panels —
one with a toolbar and three grey placeholder rows, one with a small chart —
connected by thin #0176D3 lines with small circular nodes. Panels are white
with 1px #DDDBDA borders and 12px radius. The concept is {{TOPIC}}. Grey
placeholder bars only, no legible text. Faint grid behind, wide margins.
```

### Course card

```
{{BASE}}
Aspect ratio 16:9.
Subject: a stack of three offset rounded cards in white with 1px #DDDBDA
borders, the front card carrying a large flat #0176D3 icon of {{TOPIC}}. A
small pale-blue #D8EDFF pill sits in the upper corner. Light isometric view,
faint grid dissolving toward the right. Calm, uncluttered.
```

### Blog post feature image

```
{{BASE}}
Aspect ratio 16:9.
Subject: a single flat conceptual illustration of {{IDEA}}, built from simple
geometry — circles, arrows, rounded rectangles — in #0176D3 and #1B96FF on
white, with #181818 used only for thin detail lines. One clear focal shape,
lots of negative space, faint grid in one corner. Editorial and quiet, not
busy.
```

### Open Graph / social card

```
{{BASE}}
Aspect ratio 1.91:1, 1200x630.
Subject: {{SUBJECT}}, placed slightly left of centre with the right third left
as empty white space. Large simple shapes only — this is viewed small in a
social feed. A #0176D3 accent bar runs along the bottom edge. No text.
```

### Dark-mode variant

The site has a dark theme; if you want a matching dark image, swap the ground:

```
…as above, but on a deep navy #032D60 background. Shapes in #1B96FF and
#7CBEFF, hairlines in #30363D, panel fills in #161B22. Keep it flat — no glow,
no neon, no light bloom. Same composition.
```

### Author avatar / illustration

```
{{BASE}}
Aspect ratio 1:1.
Subject: a simple flat geometric mark — {{SHAPE}} — in #0176D3 on a #EEF6FF
circle. Extremely minimal, no face, no gradients, centred with even margins.
```

---

## Reject the image if

- there is any **gradient, glow, glass or neon** — the single most common failure
- it has **baked-in text**, especially gibberish lettering
- it uses colours outside the palette (purple, teal, pink, orange floods)
- it renders **realistic people or stock-photo faces**
- it includes a **Salesforce cloud logo or trademark**
- it's **cluttered** — more than one idea, or busy background detail
- it's **3D-rendered / glossy / plasticky** rather than flat vector
- the **subject touches the edges** (needs margin; OG cards get cropped)
- it **doesn't read at 96px** — the real test for section and course thumbs

Negative-prompt string, for models that take one:

```
gradient, glow, neon, glassmorphism, 3d render, glossy, photorealistic,
photograph, people, faces, hands, text, letters, words, watermark, logo,
Salesforce logo, cloud logo, clutter, busy, noisy texture, lens flare,
drop shadow, bevel, emboss, dark vignette
```

---

## Workflow notes

- Generate **larger than needed**, then downscale — small text-free shapes
  survive downscaling well.
- Export **WebP** where possible; Ghost serves responsive sizes itself, so a
  single large upload is enough.
- **Alt text is not optional.** Describe the concept, not the artwork
  ("a branching flow with a decision point", not "blue illustration").
- Purely decorative images inside content should get empty alt (`alt=""`).
- Keep one image per section/course consistent over time — the roadmap reads as
  a set, and a mismatched thumbnail is obvious in the grid.
- Sources of truth if you ever need to re-derive the palette:
  `assets/css/0-foundation/colors.css` and the rest of `assets/css/0-foundation/`.
