# Contributing to Namaste Salesforce

Thanks for your interest in improving the theme! 🎉 This project is open source and
contributions of every size — typo fixes, new components, docs, accessibility
improvements, whole new sections — are welcome.

## Getting set up

1. **Fork** the repository and clone your fork.
2. Install dependencies and start the dev server:
   ```bash
   yarn install
   yarn dev
   ```
   This builds the assets and watches `assets/scss`, `assets/js` and `*.hbs` with
   livereload. You'll need a local [Ghost](https://ghost.org/docs/install/local/)
   install to preview the theme against real content.
3. Make your changes (see conventions below).
4. **Rebuild and commit the build output:**
   ```bash
   yarn build
   ```
   `assets/built/` is committed because Ghost serves it directly. PRs that change
   SCSS/JS but not the built files will look "broken" to reviewers.
5. **Validate** the theme:
   ```bash
   yarn test        # runs gscan, Ghost's theme validator
   ```
6. Open a pull request with a clear description of *what* and *why*.

## Coding conventions

### SCSS

- **Use the design tokens.** Pull colours, spacing, radii, shadows and breakpoints from
  `assets/scss/variables.scss` (`@use "variables" as sf;`) rather than hard-coding values.
- **Theme both modes.** Anything with a colour needs a dark-mode counterpart via
  `[data-theme="dark"] & { … }` using the `$sf-dark-*` tokens.
- **Two layers of CSS:**
  - `framework/` — generic, reusable classes (grid, buttons, utilities). Keep these
    framework-like and unopinionated.
  - `components.scss` — bespoke, branded components. Prefix them with `ns-`.
- **Comment new components** with a short usage example, matching the existing style.
- Respect `prefers-reduced-motion` for any animation.

### Handlebars templates

- Start page templates with `{{!< default}}` to inherit the shared shell.
- Reuse partials (`{{> name}}`) instead of duplicating markup.
- Keep markup accessible: real headings, `alt` text, `aria-label`s on icon-only buttons,
  and `aria-hidden="true"` on decorative icons.
- Add a brief comment block at the top of new templates/partials explaining their purpose.

### General

- Match the surrounding code's style, naming, and comment density.
- Prefer small, focused PRs.
- If you change behaviour, update the README/docs where relevant.

## Reporting bugs & ideas

Open an [issue](https://github.com/imswarnil/Namaste-Salesforce/issues) describing the
problem (with steps to reproduce / screenshots) or your feature idea. For visual bugs,
note your browser and whether it happens in light or dark mode.

## Code of conduct

Be kind and constructive. We want this to be a welcoming place for learners and
contributors of all experience levels.
