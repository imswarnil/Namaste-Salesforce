# 5-utilities/ — theme utilities

Empty, and it should stay empty for as long as possible.

Tailwind is already loaded and its utilities sit in `@layer utilities`, which
beats everything. A hand-written utility here would be a second utility system
competing with a complete one — write `mt-6`, not `.u-mt-6`.

This folder exists for the rare case Tailwind cannot express: a utility that
needs an NSDS token with no Tailwind bridge, or a container-query helper. Both
should be checked against `assets/css/nsds/tailwind.css` first — the bridge
generates a utility for every token, so `p-card` and `bg-brand-500` already
exist.
