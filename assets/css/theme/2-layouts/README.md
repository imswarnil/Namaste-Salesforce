# 2-layouts/ — page-level structure the theme owns

Empty for now, and it may stay that way.

NSDS ships the layouts: `.ns-post` is the three-column reading surface,
`.ns-band` is a page section, `.ns-page` is the width-capped shell. A layout
file here is only justified when a page shape exists that NSDS has no
component for AND that the collection specs actually call for — the docs tree
is the likely first one.

Before adding a file, check `NS-Design-System/templates/` for an archetype
that already does it. `abstract/03-design-system.md` has the porting
procedure.
