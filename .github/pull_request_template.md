## What and why

<!-- What changes, and the problem it solves. Link an issue if there is one. -->

## Checklist

- [ ] `yarn build` run, and **`assets/built/` committed** (Ghost serves it directly; CI fails if it is stale)
- [ ] `yarn test` passes (gscan)
- [ ] No `style="…"` and no `<style>` in any `.hbs` — see `abstract/05`
- [ ] Checked NSDS first: this does not reimplement a component the design system already ships (`abstract/03`)
- [ ] If markup moved onto a new class, I grepped the JS for the old one **in this same change** (`abstract/10`)
- [ ] Looked at it in a browser, in **both** light and dark

## Does this break an existing site?

- [ ] No — styling, a fix, or a new addition → **MINOR** or **PATCH**
- [ ] Yes — it changes a URL, a required tag convention, `routes.yaml`, or removes a custom setting → **MAJOR**

<!-- If yes, say what a site owner has to do when they upgrade. -->

## Screenshots

<!-- For anything visual. Light and dark, please. -->
