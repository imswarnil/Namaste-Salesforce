# Publication banner — image-generation prompt

Prompts for generating the Namaste Salesforce publication cover / social banner
so it matches the site's design system: calm, flat, reading-first, one working
blue, hairline lines, generous whitespace. Use with Midjourney, DALL·E,
Ideogram, Recraft (best for flat vector), or similar.

  **Canvas:** Ghost publication cover `1200×630` (og:image) · optional wide hero
  `2400×800` · square `1024×1024` for avatars/cards.

  ---

  ## Main prompt

  > Flat vector illustration, clean minimal tech-education style. A young Indian
  > professional sitting at a tidy desk with a laptop, learning on an online
  > platform: the laptop screen shows a simple video-lesson UI (play button,
  > progress bar, lesson checklist). Around the scene, small floating UI cards
  > connected by thin hairline lines with small dots (HUD-pin style): a CRM
  > record card, a mini funnel bar chart, a flowchart node diagram, and a code
  > snippet card. A subtle curvy dotted learning path winds through the
  > background from a flag to a certificate badge.
  >
  > Color palette strictly limited: royal azure blue #0176D3 as the only accent,
  > with lighter tints #1B96FF and #B0D7FF, deep navy #032D60 for details, on a
  > white / very light gray #F6F7F9 background. Soft rounded corners, 1px
  > hairline outlines, small flat shadows, NO gradients on text, generous
  > negative space, geometric sans-serif feel. Modern SaaS landing-page
  > illustration, style of open-source documentation sites — friendly,
  > professional, uncluttered. Wide 1200×630 composition with clear empty space
  > on the left third for a title overlay.

  **Negative prompt (where supported):** photorealism, 3D render, glassmorphism,
  neon glow, purple/violet/orange/rainbow colors, gradients on text, clutter,
  skeuomorphism, stock-photo people, text, words, letters, watermark, logo.

  ---

  ## Variants

  **A — Platform only (no person):** replace the person/desk sentence with:
  "A large clean browser window in the center showing a lesson player UI, tilted
  slightly, surrounded by the floating concept cards."

  **B — Learning path hero:** "A winding curvy dotted road across a flat
  landscape of abstract UI shapes, with milestone nodes as rounded icon badges
  (flag → database → gear → chart → certificate), tiny flat clouds, one blue
  accent color."

  **C — Square avatar/icon:** "Minimal flat badge: an open book merged with a
  cloud shape, single azure blue #0176D3 on white, thick simple shapes, no
  outline text, centered, lots of padding."

  ---

  ## Style keywords (append/mix as needed)

  `flat vector` · `2D corporate illustration` · `SaaS hero illustration` ·
  `monochromatic blue palette` · `hairline stroke details` · `rounded geometric
  shapes` · `whitespace-heavy composition` · `documentation-site art style` ·
  `clean edtech branding`

## After generating

- Export/upscale to PNG ≥ 1200×630, keep under ~1 MB (compress via Squoosh).
- Upload in **Ghost Admin → Settings → Design & branding → Publication cover**.
- Check it in both themes — the white background should sit fine in dark mode
  cards since Ghost renders covers in their own frame.
