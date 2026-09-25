# NEXT — what to do after the 7–8 Sep 2026 session

Everything below is either a value only you can set, a decision only
you can make, or a follow-up that was deliberately left out. The build
is green (`pnpm build`, `pnpm test` / gscan, all templates parse).

## 1. Set these in Ghost Admin (nothing to code)

| Where | Setting | Why |
|---|---|---|
| Design → Site-wide | **Hero video** | YouTube URL the hero square plays. Empty = still cover, no play button. |
| Design → Site-wide | **Hero chips** | Comma list of badges around the hero card. Empty = `Agentforce, AI, Apex, Flow, LWC`. |
| Design → Site-wide | **Contact email** | Where the contact page + its composer write to. Empty = `hello@namastesalesforce.com`. |
| Design → Brand | **Publication cover** | The hero card shows it. Currently an Unsplash placeholder. |
| Staff → your profile | **Profile photo** | The About page hero shows it; today it renders the fallback avatar. |

## 2. Content only you can write

- **Journey years** — `partials/journey.hbs` carries PLACEHOLDER years
  (2018 … 2026), spaced to fit "7+ years in IT". Replace with real dates.
  The ⚠ comment in the file marks them.
- **Products I use** — the page is grouped by category now (every `h2` is a
  shelf). Shelves are empty until you add bullets under each heading, in
  the shape `**Name** — one honest line`. Each bullet becomes a tile.
- **About page copy** — `page-about.hbs` renders the page body between
  the hero and the journey. The body in Ghost is two short paragraphs.
- **Sponsor email** — `page-sponsor.hbs` still hardcodes
  `sponsor@namastesalesforce.com`. Wire it to a setting if it changes.

## 3. Decisions parked

- **Sticky-stack every section.** Not done on purpose: it conflicts with
  the training-path rail (a sticky ancestor becomes its containing block)
  and hurts reading on a long page. If wanted, pick 3–4 sections.
- **Homepage video teaser** (`videos/namaste-teaser/`, HyperFrames,
  1080×1080, 5 s). Built and checked, never rendered — parked on request.
  `npx hyperframes render . -q high -o ./renders/video.mp4` when needed.
  The kicker still repeats the title; swap it before rendering.

## 4. Check on a real phone

Verified in a browser harness at 360–1400 px, not on a device:
- drawer: rows are full-width taps, closes on link tap / Escape / resize
- hero card: chips + social rail in the gutters, toggle plays and closes
- courses / shop: sidebar sticks, filters build, ad slot below

## 5. Design system — one repo now

| Site | Where | What |
|---|---|---|
| **salesforce.imswarnil.com** | this repo, `design-system/` (`main`) | v3 — the NS Design System + styleguide site, **published by `.github/workflows/design-system.yml`** |
| nsds.imswarnil.com | `imswarnil/NSDS-Design-System` | the v2 build this folder replaced — still live; archive the repo or point its README here when convenient |
| sfdc.imswarnil.com | `imswarnil/sfdc` | the original token/gate system — DNS record exists now |

**To do — DNS.** `salesforce.imswarnil.com` is currently a Cloudflare
Workers custom domain for the `salesforce-passport` Worker (a Nuxt app,
"Salesforce Passport"). GitHub Pages has the custom domain set and will
serve the moment the hostname points at it. To switch: remove the Worker
custom domain, then add `CNAME salesforce → imswarnil.github.io` (proxied,
like `nsds`), then tick "Enforce HTTPS" in the repo's Pages settings once
the certificate is issued.

## 6. Running Ghost locally

`better-sqlite3` in `ghost/versions/6.57.1` is built for Node 22:
```
cd ghost && lsof -ti :2369 | xargs -r kill -9
NODE_ENV=development ~/.nvm/versions/node/v22.21.1/bin/node current/index.js
```
A new `page-<slug>.hbs` or a new `config.custom` setting needs this
restart to register — Ghost only reads them at boot.
