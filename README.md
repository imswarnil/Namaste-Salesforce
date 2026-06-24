# Namaste Salesforce — Ghost Theme

An open-source [Ghost](https://ghost.org/) theme for **Salesforce learning communities**:
courses, lessons, documentation, roadmaps, and a developer blog — all in one clean,
fast, accessible package.

- 🎨 **SLDS-inspired design** — a Salesforce-blue palette with a polished, modern feel
- 🌗 **Built-in dark mode** — instant, flash-free theme toggle (saved per visitor)
- 📱 **Fully responsive** — mobile-first layouts, collapsible navigation and sidebars
- 🧩 **Reusable components** — cards, heroes, stats, tracks, badges, and more
- ⚡ **No CSS framework dependency** — a small, in-house SCSS framework (Bulma removed)
- ♿ **Accessible** — semantic markup, focus rings, reduced-motion support

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
> Always rebuild (`yarn build`) and commit the output after changing SCSS or JS.

&nbsp;

## Project structure

```
.
├── default.hbs            # HTML shell: <head>, header, body, footer, theme script
├── index.hbs              # Post list / fallback home
├── home.hbs               # Custom landing page
├── page-about.hbs         # Custom About page (auto-used for the /about/ page)
├── courses.hbs            # Courses listing
├── documentation.hbs      # Docs hub
├── blog.hbs               # Blog listing
├── training.hbs           # Roadmaps / training tracks
├── post.hbs · page.hbs    # Single post / page
├── tag.hbs · author.hbs   # Archive pages
│
├── partials/              # Reusable Handlebars fragments ({{> name}})
│   ├── header.hbs         # Context-aware navbar (course/lesson/blog/docs/…)
│   ├── footer.hbs
│   ├── navigation.hbs     # Ghost menu → navbar with dropdowns & icons
│   ├── doc-sidebar.hbs    # Documentation sidebar
│   ├── post-*.hbs         # Per-context post renderers (card, course, lesson, …)
│   └── toc.hbs            # Table of contents
│
└── assets/
    ├── scss/
    │   ├── screen.scss        # ⭐ The single compiled entry point
    │   ├── variables.scss     # Design tokens (colours, spacing, shadows, …)
    │   ├── mixins.scss        # Reusable SCSS mixins
    │   ├── framework/         # ⭐ In-house CSS framework (replaces Bulma)
    │   │   ├── _base.scss     #    reset + document theming
    │   │   ├── _layout.scss   #    container, 12-col grid, section, footer
    │   │   ├── _helpers.scss  #    spacing / flex / text / visibility utilities
    │   │   ├── _buttons.scss  #    buttons, button groups, icons
    │   │   ├── _forms.scss    #    inputs, fields, controls
    │   │   ├── _tags.scss     #    tags / badges
    │   │   ├── _navbar.scss   #    top navigation bar
    │   │   ├── _menu.scss     #    sidebar menu, breadcrumb, panel, tabs, progress
    │   │   ├── _card.scss     #    card, box, hero, image ratios
    │   │   └── _typography.scss#   title / subtitle / content
    │   ├── components.scss    # Bespoke ns-* components (hero, cards, stats, …)
    │   ├── ghost.scss         # Styling for Ghost/Koenig post content (.kg-* cards)
    │   ├── animations.scss    # Entrance / motion animations
    │   └── toc.scss           # Table-of-contents styling
    └── js/                    # Concatenated into built/casper.js
```

&nbsp;

## Styling architecture

This theme **does not use a CSS framework**. Instead it ships a small, purpose-built
SCSS framework under `assets/scss/framework/`. It reimplements just the utility and
component classes the templates need (grid, buttons, navbar, forms, helpers, …), themed
with the Salesforce design tokens in `variables.scss`.

- **Design tokens first.** Colours, spacing, radii, shadows and breakpoints all live in
  `variables.scss`. Change a token there and it propagates everywhere.
- **Dark mode** is driven by `data-theme="light|dark"` on `<html>`. Style dark variants
  with the `[data-theme="dark"] &` selector and the `$sf-dark-*` tokens.
- **Bespoke components** use an `ns-` prefix (e.g. `.ns-hero`, `.ns-card`,
  `.ns-feature-card`) and are documented inline in `components.scss`.

&nbsp;

## Custom templates & routing

Ghost picks templates by convention:

- `page-{slug}.hbs` → custom template for that page (e.g. `page-about.hbs` for `/about/`).
- `home.hbs`, `courses.hbs`, `documentation.hbs`, `blog.hbs`, `training.hbs` are selectable
  per page in the Ghost editor, or routed via `routes.yaml` (configured in Ghost Admin).

Post "sections" are driven by internal tags (`#course`, `#lesson`, `#blog`,
`#training`, `documentation`, …) which switch the navbar context and post layout.

&nbsp;

## Contributing

Contributions are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for setup,
coding conventions, and how to propose changes.

## License

Released under the [MIT license](LICENSE).
This theme began as a fork of Ghost's [Casper](https://github.com/TryGhost/Casper) theme.
