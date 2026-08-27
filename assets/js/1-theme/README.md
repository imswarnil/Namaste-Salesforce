# 1-theme/ — the theme's own scripts

Empty, and worth keeping that way.

Everything the chrome does — the menus, the mobile sheet, the theme switch,
the outline, the reading progress, the code copy button — is NSDS's, vendored
into `0-vendor/`. Anything written here is behaviour the design system does
not have, which means the LMS will not have it either, which usually means it
belongs upstream.

Files here are concatenated into `main.min.js` **after** the vendored layer,
so they can assume NSDS's behaviour is already wired. They are picked up by a
glob in `gulpfile.mjs`, so no registration step is needed — unlike
`0-vendor/`, which is listed file by file on purpose.

Before adding one, check the three questions in `abstract/04-css.md`: does
Ghost do it, does NSDS do it, and only then write it. The pace picker on the
homepage is the worked example of the alternative — it needed a script and got
CSS `:has()` instead, so it keeps working with JavaScript blocked.
