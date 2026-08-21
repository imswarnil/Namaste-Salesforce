# 11 · What actually makes this a better Ghost theme

Ranked by **return per hour**, not by how interesting it is to build. The old
theme had most of the bottom half and none of the top three.

---

## Tier 1 — build these first

### 1. Search that works on a learning site
Ghost's built-in search (`data-ghost-search`) indexes titles and excerpts only.
On a site whose value is 300 lessons, a reader searching "governor limit" needs
to land *inside* a lesson. Options, cheapest first:

- Ghost search + good excerpts on every post (free, weak)
- **Pagefind** — static index built at deploy, no service, searches full text
- Algolia/Typesense (fast, costs money and a sync job)

**Pagefind is the right first move.** It indexes the built HTML, so it needs no
Ghost integration at all.

### 2. Progress, and therefore a reason to return
Right now nothing remembers a reader. The honest static version:
`localStorage` per lesson slug → a tick in the rail, a "continue where you left
off" card on `/training/`. No account needed, works immediately.

The real version is a member record via Ghost's Members API, which unlocks
certificates. **Do the localStorage one first** — it takes a day and tells you
whether anyone actually uses the sequencing.

### 3. A real 404 and a real empty state
Every dead end should offer the three places someone actually wanted. This is
cheap and it is the page people hit when your URL model changes — see
`abstract/01` for how easily that happens.

## Tier 2 — worth it once Tier 1 exists

- **Reading position sync across devices** — needs members; big retention win
  for long-form training.
- **`/tag/` archive pages that earn their place.** Today they redirect (right
  call for course/section tags). For topic tags they should be real landing
  pages: intro copy from the tag description, then the posts.
- **RSS per collection.** `/blog/rss/`, `/training/rss/` — Ghost gives you the
  first free; the others need routes.
- **An `og:image` that is generated, not uploaded.** Every post needs one and
  nobody makes them. A build-time SVG→PNG per post using the title and NSDS
  tokens costs one script and makes every share look deliberate.
- **Comments** — Ghost has them native; the theme just has to place them well.

## Tier 3 — polish that compounds

- Keyboard shortcuts on the lesson player (`j`/`k` prev-next, `/` search)
- Print stylesheet for docs and cheatsheets (people do print reference pages)
- Web Share API on mobile instead of four network buttons
- View Transitions between lessons — one line now that navigation is real links

## The performance budget, so it stays fast

Write it down and hold it. Suggested, and achievable with NSDS as-is:

| Metric | Budget |
| --- | --- |
| LCP | < 1.8s on 4G |
| CLS | < 0.05 |
| JS shipped per page | < 40 KB gzipped |
| Fonts | 2, both preloaded, ~67 KB total |
| Blocking requests in `<head>` | 1 stylesheet + 1 inline script |

The current architecture already gets you most of this: self-hosted fonts,
inline SVG icons, no icon font in the render path, per-page deferred scripts.
**The thing that breaks it is adding a third-party embed** — analytics, chat,
an ad network. Each one is a budget decision, not a feature decision.

## Accessibility, treated as correctness

NSDS does most of it if you use its contracts rather than inventing them:

- state is an ATTRIBUTE (`aria-current`, `data-state`, `[open]`) so the CSS and
  the screen reader read one source
- native `<details>`, `<dialog>`, `popover` instead of Alpine — focus trapping,
  Esc and light dismiss come from the platform
- a skip link, and a visible focus ring everywhere

Test with the keyboard only, once per feature. It takes two minutes and catches
almost everything.

## What NOT to build

- **A second design system.** This is the mistake that cost the last rebuild.
  See `abstract/10`.
- **A comment system, a forum, a course player with video hosting.** Ghost is a
  publishing platform. The moment you need real application state (quizzes,
  grading, certificates at scale) that belongs in the Next.js app at
  app.namastesalesforce.com, sharing NSDS. The theme's job is the public,
  readable, indexable half.
