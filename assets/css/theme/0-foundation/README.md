# 0-foundation/ — empty on purpose

Theme-local custom properties go here. **Design tokens do not.**

NSDS owns colour, spacing, radius, type and timing, and both this theme and
the Next.js LMS consume the same vendored copy. Declaring one of those here
creates a second source of truth for a value the two products must agree on,
and nothing will tell you they have drifted.

What legitimately belongs here: a knob that is meaningless outside this theme.
A component-scoped variable, a Ghost-specific measurement, a switch NSDS has
no view on. There is nothing like that yet, which is why this folder holds
only this file.

If you are about to add a colour, a spacing step or a font size — that change
belongs in NS-Design-System, and it will benefit the LMS too.

See `../README.md`.
