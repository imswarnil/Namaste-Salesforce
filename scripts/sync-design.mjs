/**
 * Vendors the NS Design System into this theme.
 *
 * The system lives OUTSIDE the theme, beside the Ghost install, at
 * ../../../../NS-Design-System. It is the source of truth and is READ-ONLY
 * from here: never edit it to make the theme happy — change the theme, or
 * change the system in its own repo and re-sync.
 *
 *   yarn design:sync     refresh the vendored copy
 *   yarn design:check    fail if the copy has drifted (runs in pretest/CI)
 *
 * Why vendor instead of @import across the filesystem: a Ghost theme ships as
 * a self-contained zip. Anything reaching outside the theme root resolves on
 * this machine and 404s on the server. We copy, and we commit the copy.
 *
 * What lands where:
 *
 *   assets/css/ds/styles.css        entry — imports everything below
 *   assets/css/ds/tokens/*.css      colors, spacing, layout, fonts, type, effects
 *   assets/css/ds/icons/*.css       phosphor.css + icons-gap.css
 *   assets/css/ds/patterns/*.css    patterns.css
 *   assets/css/ds/components/css/   the .ns-* class layer shared with the app
 *   assets/fonts/nm*.woff2          N&M Display / Text / Mono
 *   assets/fonts/phosphor*.woff2    the subsetted icon font
 *   assets/icons/namaste-icons.svg  the <use href> sprite
 *
 * ⚠️ FONT PATHS. The gulp pipeline (postcss + cssnano) rebases relative url()s
 * against assets/built/screen.css and consumes exactly one `../` on the way —
 * the gotcha documented in CLAUDE.md. Upstream writes `url("../fonts/x.woff2")`
 * from tokens/, which is correct in the design system's own tree and wrong
 * here at a different nesting depth. So the copied stylesheets get their font
 * and icon url()s REWRITTEN to this theme's layout. That rewrite is the one
 * edit this script makes to upstream bytes, it is confined to url() values,
 * and FONT_URL_DEPTH below is the single number that controls it.
 *
 * ⚠️ Everything under assets/css/ds/ is GENERATED. Never hand-edit it — the
 * next sync silently reverts the change. Theme-local styling belongs in
 * assets/css/0-foundation .. 3-modules, which is where the layering contract
 * in CLAUDE.md still applies.
 */
import { cp, mkdir, rm, readdir, readFile, writeFile, stat } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { join, resolve, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { tmpdir } from 'node:os'

const themeRoot = resolve(fileURLToPath(import.meta.url), '../..')
const source = resolve(themeRoot, '../../../../NS-Design-System')

const checkOnly = process.argv.includes('--check')

/**
 * Copied stylesheets sit at assets/css/ds/<dir>/file.css. To reach
 * assets/fonts/ from there on disk is `../../../fonts/`, and the pipeline eats
 * one `../` when it rebases into assets/built/ — which leaves `../../fonts/`,
 * resolving to assets/fonts/. That is the path we want, so we write the
 * on-disk-correct one and let the rebase land it.
 *
 * If a stylesheet ever lands at a different depth, this is the number to
 * change — and `yarn build && grep -o 'url([^)]*)' assets/built/screen.css`
 * is how you check it, per CLAUDE.md.
 */
const FONT_URL_DEPTH = '../../../'

/** Rewrite upstream's font/icon url()s onto this theme's asset layout. */
function rewriteAssetUrls(css) {
  return css.replace(
    /url\((['"]?)([^'")]+?)\1\)/g,
    (whole, quote, url) => {
      // Absolute, data: and protocol urls are already final.
      if (/^(?:[a-z]+:|\/|#)/i.test(url)) return whole
      const file = url.split('/').pop()
      if (/\.(woff2?|ttf|otf|eot)$/i.test(file)) {
        return `url(${quote}${FONT_URL_DEPTH}fonts/${file}${quote})`
      }
      if (/\.(svg|png|jpe?g|webp|avif)$/i.test(file)) {
        return `url(${quote}${FONT_URL_DEPTH}icons/${file}${quote})`
      }
      return whole
    },
  )
}

async function hashTree(dir) {
  if (!existsSync(dir)) return null
  const hash = createHash('sha256')
  const walk = async (d) => {
    for (const entry of (await readdir(d, { withFileTypes: true })).sort((a, b) =>
      a.name.localeCompare(b.name),
    )) {
      const full = join(d, entry.name)
      if (entry.isDirectory()) await walk(full)
      else {
        hash.update(relative(dir, full))
        hash.update(await readFile(full))
      }
    }
  }
  await walk(dir)
  return hash.digest('hex')
}

/** Rewrite every .css under a directory in place. */
async function rewriteTree(dir) {
  if (!existsSync(dir)) return
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name)
    if (entry.isDirectory()) await rewriteTree(full)
    else if (entry.name.endsWith('.css')) {
      const css = await readFile(full, 'utf8')
      const next = rewriteAssetUrls(css)
      if (next !== css) await writeFile(full, next)
    }
  }
}

async function build(cssTarget, fontTarget, iconTarget) {
  await rm(cssTarget, { recursive: true, force: true })
  await mkdir(cssTarget, { recursive: true })

  await cp(join(source, 'styles.css'), join(cssTarget, 'styles.css'))

  // WHOLE directories, not a named file list — styles.css decides what it
  // imports, and that list grows upstream. Copying a hardcoded subset means
  // the next stylesheet added there breaks the build with an unresolved
  // @import. Discovered, not hardcoded, so an upstream rename degrades to a
  // missing style rather than a failed sync that already deleted the copy.
  for (const dir of ['tokens', 'icons', 'patterns']) {
    if (!existsSync(join(source, dir))) continue
    await cp(join(source, dir), join(cssTarget, dir), { recursive: true })
  }

  // The .ns-* component layer — the shared class contract with the Next.js
  // app. It lands under components/css/ because styles.css imports
  // "./components/css/index.css" relative to itself.
  await cp(join(source, 'components/css'), join(cssTarget, 'components/css'), {
    recursive: true,
  })

  // Fonts and the icon font are served by Ghost from the theme's own origin,
  // so they live in assets/fonts/ next to the compiled CSS, not in the
  // vendored css tree. Binaries are moved out; the .css files stay behind.
  await mkdir(fontTarget, { recursive: true })
  for (const dir of ['fonts', 'icons']) {
    const from = join(source, dir)
    if (!existsSync(from)) continue
    for (const entry of await readdir(from, { withFileTypes: true })) {
      if (!entry.isFile() || !/\.(woff2?|ttf|otf)$/i.test(entry.name)) continue
      await cp(join(from, entry.name), join(fontTarget, entry.name))
    }
  }

  // The sprite is fetched at runtime by <use href="…#ns-i-course">, so it
  // needs a stable public URL rather than a bundler-hashed one.
  await mkdir(iconTarget, { recursive: true })
  const sprite = join(source, 'icons/namaste-icons.svg')
  if (existsSync(sprite)) await cp(sprite, join(iconTarget, 'namaste-icons.svg'))

  // Binaries were copied out of the css tree above; drop the duplicates so the
  // theme zip does not ship every woff2 twice.
  for (const dir of ['tokens', 'icons', 'patterns']) {
    const here = join(cssTarget, dir)
    if (!existsSync(here)) continue
    for (const entry of await readdir(here, { withFileTypes: true })) {
      if (entry.isFile() && /\.(woff2?|ttf|otf|svg)$/i.test(entry.name)) {
        await rm(join(here, entry.name))
      }
    }
  }

  await rewriteTree(cssTarget)

  const files = []
  const count = async (d) => {
    for (const e of await readdir(d, { withFileTypes: true })) {
      if (e.isDirectory()) await count(join(d, e.name))
      else files.push(e.name)
    }
  }
  await count(cssTarget)
  return { cssFiles: files.length }
}

if (!existsSync(source)) {
  // Expected wherever only the theme was checked out. The vendored copy is
  // committed precisely so the build does not need the source — succeed.
  if (existsSync(join(themeRoot, 'assets/css/ds/styles.css'))) {
    console.log('· NS-Design-System not present — using the committed copy')
    process.exit(0)
  }
  console.error(`✗ NS-Design-System not found at ${source}, and no committed copy`)
  process.exit(1)
}

const cssTarget = join(themeRoot, 'assets/css/ds')
const fontTarget = join(themeRoot, 'assets/fonts')
const iconTarget = join(themeRoot, 'assets/icons')

if (checkOnly) {
  // ⚠️ Build into a temp directory, never in place. A check that rebuilds over
  // the working tree silently FIXES the drift it is meant to report and then
  // passes on the next run.
  //
  // Only the vendored css tree is fingerprinted. assets/fonts/ and
  // assets/icons/ are shared with theme-owned files, so a hash of those
  // directories would report drift every time the theme adds an asset of its
  // own — the copy is verified through the css tree that references it.
  const scratch = join(tmpdir(), `ns-theme-design-check-${process.pid}`)
  try {
    await build(join(scratch, 'css'), join(scratch, 'fonts'), join(scratch, 'icons'))
    const committed = await hashTree(cssTarget)
    const fresh = await hashTree(join(scratch, 'css'))
    if (committed === fresh) {
      console.log('✓ vendored design system is in sync with NS-Design-System')
      process.exit(0)
    }
    console.error('✗ vendored design system has drifted from NS-Design-System')
    console.error('  Run: yarn design:sync   (and commit the result)')
    process.exit(1)
  } finally {
    await rm(scratch, { recursive: true, force: true })
  }
}

const { cssFiles } = await build(cssTarget, fontTarget, iconTarget)
console.log('✓ synced NS-Design-System → assets/css/ds')
console.log(`  ${cssFiles} stylesheets, fonts → assets/fonts, sprite → assets/icons`)
console.log('  Verify font urls: yarn build && grep -o \'url([^)]*)\' assets/built/screen.css')
