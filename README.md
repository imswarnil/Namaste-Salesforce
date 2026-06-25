# Namaste Salesforce — Ghost Theme

An open-source [Ghost](https://ghost.org/) theme for **Salesforce learning communities**:
courses, lessons, documentation, roadmaps, and a developer blog — all in one clean,
fast, accessible package.

- 🎨 **SLDS-inspired design** — a Salesforce-blue palette with a polished, modern feel
- 🌗 **Built-in dark mode** — instant, flash-free theme toggle (saved per visitor)
- 📱 **Fully responsive** — mobile-first layouts, collapsible navigation and sidebars
- 🧩 **Reusable components** — cards, heroes, stats, tracks, timelines, ads and more
- ⚡ **Tailwind CSS v4** — utility-first styling with a small SLDS token layer
- ✨ **Light interactivity** — [Alpine.js](https://alpinejs.dev/) (self-hosted) for menus & toggles
- ♿ **Accessible & SEO-ready** — semantic markup, focus rings, reduced-motion, JSON-LD

&nbsp;

## Quick start

You'll need [Node.js](https://nodejs.org/) and [Yarn](https://yarnpkg.com/).

```bash
yarn install     # install dependencies
yarn dev         # build + livereload watch server (for local development)
yarn build       # one-off build into assets/built/
yarn zip         # package into dist/namaste-salesforce.zip for upload to Ghost
yarn test        # validate the theme with gscan (Ghost's theme checker)
```

Upload the generated `dist/namaste-salesforce.zip` in **Ghost Admin → Settings → Design → Change theme → Upload theme**.

> **Note:** `assets/built/` is committed to git because Ghost serves it directly.
> Always rebuild (`yarn build`) and commit the output after changing CSS or JS.

&nbsp;

## Project structure

```
.
├── default.hbs            # HTML shell: <head>, header, body, footer, theme script
├── index.hbs              # Post list / fallback home
├── home.hbs               # Custom landing page
├── page-about.hbs         # Custom About page (auto-used for /about/)
├── courses.hbs            # Courses listing (search, stats, CTAs)
├── documentation.hbs      # Docs hub (hero search + sidebar)
├── blog.hbs               # Blog listing (+ sidebar)
├── training.hbs           # Roadmaps as an animated numbered timeline
├── post.hbs · page.hbs    # Single post (router) / page
├── tag.hbs · author.hbs   # Archive pages
├── error.hbs              # 404 / error page
│
├── partials/
│   ├── header.hbs · footer.hbs · navigation.hbs   # site chrome
│   ├── post-*.hbs                                  # single-post layouts (router targets)
│   ├── post-card.hbs · pagination.hbs · related-posts.hbs · social-share.hbs
│   ├── icons/        # inline-SVG icon set (currentColor + `class` param)
│   ├── components/   # theme-toggle, nav-icon, page-header, hero-bg, breadcrumb,
│   │                 #   toc, cta, author-byline, tag-pills, social-icons
│   ├── home/         # landing-page cards (track, feature, collection, step,
│   │                 #   timeline-item, testimonial, skills)
│   ├── about/        # founder card
│   ├── courses/      # course-card, lesson-nav, faq-item
│   ├── blog/         # featured-post, sidebar
│   ├── docs/         # sidebar
│   ├── training/     # curriculum, track-node
│   └── ads/          # slot (resolver), adsense, sponsored, placeholder
│
└── assets/
    ├── css/screen.css     # ⭐ Tailwind entry (tokens, base, components, patterns)
    ├── js/
    │   ├── theme-toggle.js · toc.js · effects.js · reveal.js   # → built/casper.js
    │   └── vendor/alpine.js                                    # self-hosted Alpine
    └── built/             # compiled, committed output (screen.css, casper.js)
```

&nbsp;

## Styling architecture (Tailwind v4)

Styling is **Tailwind CSS v4**, compiled through the existing gulp + PostCSS pipeline
(`@tailwindcss/postcss`) into `assets/built/screen.css`. There is no separate Tailwind
config file — everything lives in **`assets/css/screen.css`**:

- **Design tokens** in `@theme` — the SLDS brand-blue scale, status colours, fonts,
  radii, shadows and motion. Semantic role tokens (`surface`, `ink`, `muted`, `border`,
  …) are backed by CSS variables that **flip automatically in dark mode**, so
  `bg-surface` / `text-ink` adapt without `dark:` on every element.
- **Dark mode** is driven by `data-theme="light|dark"` on `<html>` (set before paint to
  avoid a flash); the Tailwind `dark:` variant is wired to that attribute.
- **`@layer components`** holds the small set of reusable classes that are awkward as
  pure utilities: `.nav-link`, `.icon-btn` + `.nav-tip`, `.subnav-bar` / `.subnav-panel`
  (mobile sub-nav), `.toc-link`, `.js-spotlight` (pointer spotlight), `.ns-timeline` /
  `.ns-steps` (timelines), `.bg-grid` / `.bg-dots` (faded background patterns), and the
  `.prose` overrides for post content.
- **`@source`** globs tell Tailwind to scan `*.hbs` and `partials/**/*.hbs` for classes.

JavaScript is intentionally tiny: `theme-toggle`, custom `toc` (scroll-spy), `effects`
(card spotlight) and `reveal` (scroll reveal) are concatenated into `built/casper.js`;
Alpine.js is self-hosted and loaded separately.

&nbsp;

## Custom templates, routing & settings

- `page-{slug}.hbs` → custom template for that page (e.g. `page-about.hbs` for `/about/`).
- `home.hbs`, `courses.hbs`, `documentation.hbs`, `blog.hbs`, `training.hbs` are selectable
  per page in the Ghost editor, or routed via `routes.yaml` (Ghost Admin → Settings).
- Post "sections" are driven by internal tags (`#course`, `#lesson`, `#blog`,
  `#training`, `#training-content`, `documentation`) which pick the single-post layout.
- **Theme settings** (Ghost Admin → Design) configure ads: `enable_ads`,
  `adsense_publisher_id`, and a self-hosted `sponsor_*` set. Ad slots show a dummy
  "Advertise with us" placeholder until configured.

&nbsp;

## Contributing

Contributions are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for setup,
coding conventions, and how to propose changes.

## License

Released under the [MIT license](LICENSE).
This theme began as a fork of Ghost's [Casper](https://github.com/TryGhost/Casper) theme.
