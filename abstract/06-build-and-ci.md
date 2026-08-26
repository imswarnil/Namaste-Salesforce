# 06 · The build, the checks, and CI/CD

**There is a build.** `assets/css/screen.css` and `assets/js/*.js` are the
source; `assets/built/` is what Ghost serves, and it is **committed** — Ghost
serves the theme exactly as uploaded and there is no build step on the server.

The risk that creates is a **stale build**: output that no longer describes the
source, which is a whole class of "but I fixed that already" bug. Rebuilding
and diffing in CI is what removes it, and it is the entire reason committing
generated files is safe here.

---

## Commands

```bash
npm install
npm run dev      # gulp: build once, then watch and rebuild
npm run build    # NODE_ENV=production — one production build
npm test         # build, then gscan
npm run test:ci  # build, then gscan --fatal (warnings fail too)
npm run zip      # test:ci, then package dist/namaste-salesforce.zip

./scripts/sync-nsds.sh   # re-vendor the design system, then npm run build
```

Every check is a plain node script, so any of them runs on its own with no
gulp:

```bash
node scripts/build-icon-bridge.mjs --check
node scripts/check-layers.mjs
node scripts/check-classes.mjs
node scripts/check-icons.mjs
```

## What `gulp build` does, in order

| step | what | why it is where it is |
|---|---|---|
| `clean` | delete `assets/built/` | a rename leaves the old file behind otherwise, and it keeps being served |
| `iconBridge` | regenerate `theme/icon-bridge.css` | **before** css, because css imports it |
| `css` | `screen.css` → `built/screen.css` | Tailwind v4 through `@tailwindcss/postcss`; cssnano in production only |
| `js` | `assets/js/*.js` → `built/main.js` | concatenated in a fixed order, not bundled |
| `checkLayers` | the cascade contract, **on the output** | the source cannot prove it — see [`04`](04-css-architecture.md) §2 |
| `checkMarkup` | `check-classes` + `check-icons` | both catch failures that *render* |

### Three details in that pipeline that are load-bearing

**`cssnano`'s `mergeLonghand` is off.** Its default merges longhands into
shorthands and silently drops a custom property a longhand was holding — and
this sheet is almost entirely custom properties.

**The JS list is explicit, not globbed**, so a new file in `assets/js/` does
not silently join the bundle — and so `theme-init.js` stays *out* of it. That
one must be inlined in `<head>`; in the deferred bundle it paints too late,
which is the white-flash-on-every-navigation bug ([`09`](09-performance.md)).

**The `js` task is not `allowEmpty`.** It was once, and silently produced a
bundle of one file because the other six had never been copied in. A missing
script does not fail — it just does not run. Let it throw.

### `dev` watches templates as well as CSS

Tailwind emits utilities from the class names it finds in the templates, so
**editing a `.hbs` changes the CSS.** Miss that in the watch glob and a new
utility does nothing until the next full build, which is a genuinely confusing
ten minutes.

## The checks, and the silent failure each one catches

Every check here exists because something shipped broken while the build was
green. None of them duplicates gscan.

| check | catches | how it fails without the check |
|---|---|---|
| `assets/built` diff | a stale committed build | you fix a bug, forget to rebuild, and ship the CSS from before the fix |
| `build-icon-bridge --check` | a bridge that no longer matches the bundle | 85 icon rules quietly stop applying after a sync |
| `check-layers` | the cascade order inverting | overrides stop working. **No error, no warning.** |
| `check-classes` | a `.ns-*` name that is not defined | renders as unstyled markup, and gscan passes — it is valid HTML |
| `check-icons` | a `{{> "icons/…"}}` with no partial | throws at *render* time, on one page, in production |
| no inline styles | `style="…"` in a template | cannot be overridden by a stylesheet, so it breaks dark mode and the publisher's accent silently |
| Handlebars comments | a comment-close sequence inside a comment | the comment ends there and every remaining line is emitted into the page as visible text |
| `gscan --fatal` | Ghost API misuse | the theme fails to upload, or a helper renders nothing |

> **Check by exit code, not by grepping output.** These print human-readable
> findings with no `FAIL` prefix, so `npm run build | grep -i error` reports
> success on a failing build.

### `check-layers` runs on the output, and knows about two builds

The bare `@layer` statement fixes precedence outright — where the blocks appear
is then irrelevant. In a **development** build the statement survives, and the
blocks legitimately come out in a different order (Tailwind emits its utilities
early). In **production**, cssnano drops the statement once the blocks have
been reordered to match it — and that is the build where block order becomes
the only surviving evidence.

So the check looks for the statement first and only falls through to block
order when it is gone. Checking block order unconditionally fails every dev
build, and a check that cries wolf in the edit loop is a check somebody
deletes.

## CI — `.github/workflows/ci.yml`

Runs on every push to `main` and every pull request:

1. `npm ci`
2. `NODE_ENV=production npx gulp build`
3. **`assets/built` is not stale** — `git diff --exit-code`
4. icon bridge is current
5. cascade contract
6. every `.ns-*` class is defined
7. every icon partial exists
8. `gscan --fatal --verbose`
9. no inline styles in templates
10. Handlebars comments close cleanly

Steps 3–7 and 9–10 are all things gscan cannot see. Step 8 is everything Ghost
itself will refuse.

## Deploy — `.github/workflows/deploy-theme.yml`

Push to `main` → build → prune → `TryGhost/action-deploy-theme`.

**It builds before deploying**, even though CI has just proved the committed
output is current, so the deployed bytes do not depend on that proof holding.

**The prune list is the theme's boundary.** Everything removed is something a
running Ghost site has no use for:

```
.claude  abstract  scripts  dummy-content  node_modules
gulpfile.mjs  package-lock.json  routes.yaml  *.md
assets/css        ← the SOURCE. Only the compiled output is served.
```

`routes.yaml` goes because Ghost stores routes separately — it is uploaded in
Admin → Settings → Labs → Routes, not read from the theme. See
[`01`](01-content-model.md).

Secrets: `GHOST_ADMIN_API_URL` and `GHOST_ADMIN_API_KEY`.

## Release — `.github/workflows/release.yml`

```bash
git tag -a v0.2.0 -m "…" && git push origin v0.2.0
```

Builds, checks the tag matches `package.json`'s version, runs `test:ci`,
packages the zip and publishes a GitHub release with it attached. The zip is
what a site owner uploads in **Admin → Design → Change theme**, so it must
contain the theme and nothing else.

> The `zip` script's exclude list and the deploy workflow's prune list are two
> statements of the same boundary. **They must agree.** When you add a
> directory that should not ship, change both.

## When something is wrong

| symptom | first thing to check |
|---|---|
| a style has no effect | `node scripts/check-layers.mjs`, then whether the class is defined |
| a component renders unstyled | `node scripts/check-classes.mjs` — a name was invented or mistyped |
| an icon is missing entirely | `node scripts/check-icons.mjs` |
| icons are the wrong size or colour | the bridge is stale — `node scripts/build-icon-bridge.mjs` |
| CI says `assets/built` is stale | `npm run build`, commit the result |
| a new utility does nothing | gulp was not watching `.hbs`, or the build was not re-run |
| the theme will not upload | `npx gscan --fatal --verbose .` |
