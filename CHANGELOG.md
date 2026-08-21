# Changelog

All notable changes to this theme are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## What a version number means for a Ghost THEME

Semver is written for libraries with an API. A theme's "public API" is the
things a site owner depends on and cannot change themselves:

| Change | Bump |
| --- | --- |
| a URL shape, a required tag convention, or `routes.yaml` | **MAJOR** |
| a Ghost custom setting removed or renamed | **MAJOR** |
| a template or partial removed that a fork may have overridden | **MAJOR** |
| a new template, section, component, or custom setting | **MINOR** |
| a styling, accessibility, or performance fix | **PATCH** |

The rule of thumb: **if upgrading could change a live site's URLs or lose an
editor's Admin settings, it is a MAJOR.** Everything else is not.

---

## [Unreleased]

### Changed
- **Reset to a stack-free starter.** The NSDS-based implementation was removed
  wholesale so the stack decisions could be made explicitly rather than one
  commit at a time — see `abstract/15`. Everything is recoverable from git.
- **Rebuilt from scratch on NSDS.** The theme no longer carries its own
  component library; every visual decision comes from the vendored
  [NS-Design-System](https://github.com/imswarnil/NS-Design-System), which the
  Next.js LMS also renders. See `abstract/03`.
- Type is Switzer (interface and reading) + Roboto Mono (labels, code). No
  shipped serif — the editorial register uses the platform's own.

### Removed
- The theme's own CSS layers, all theme-authored components, and the generated
  styleguide. Recoverable from the git history if any of it is wanted back.
- All Ghost custom settings. They return with the features that read them; a
  setting that toggles nothing is worse than no setting.

### Added
- `abstract/` — the knowledge base needed to rebuild the theme from nothing,
  ordered by what breaks the site if you get it wrong.

---

## [0.1.0] — unreleased

The first tagged release of the rebuild. Pre-1.0 on purpose: the structure is
still moving, and semver says that is what `0.x` is for.

`1.0.0` is when the templates in `abstract/01` all exist and the theme has been
run against real content on a live site.

[Unreleased]: https://github.com/imswarnil/Namaste-Salesforce/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/imswarnil/Namaste-Salesforce/releases/tag/v0.1.0
