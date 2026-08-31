# 06 · Structured data, feeds, and being readable by machines

Two audiences read this site without eyes: search crawlers and language
models. They want nearly the same things, and a theme that serves one well
serves the other almost for free — **so this is one job, not two.**

The short version: say what a page IS in JSON-LD, keep the prose in the HTML,
and make every surface reachable without JavaScript.

---

## 1 · What Ghost already emits, and what it does not

`{{ghost_head}}` is not a formality. It writes, per page:

| | |
|---|---|
| `Article` / `WebSite` / `Person` JSON-LD | title, excerpt, images, `datePublished`, `dateModified`, author, publisher |
| Open Graph + Twitter cards | including the per-post overrides from the editor |
| `<link rel=canonical>` | with the post's own canonical override honoured |
| `<meta name=description>` | from the excerpt |

**Never hand-write any of that.** A theme that emits its own `og:title` ends
up with two, and Ghost's is the one that follows the editor.

What Ghost does **not** know is anything about the *shape* of this site: that a
lesson belongs to a course, that a page is one of four stages, that a nav menu
exists. That gap is the theme's job, and it is the whole of §2 and §3.

## 2 · The types this site needs, and which page carries each

Ghost calls every post an `Article`. For a learning site that is true and
useless — `Article` says "someone wrote words", not "this is a course with
eight modules that takes 42 hours".

| Surface | Type to add | Why it earns its place |
|---|---|---|
| main menu | `SiteNavigationElement` | **built** — `partials/navbar/jsonld.hbs` |
| a course | `Course` + `hasCourseInstance` | carries `courseMode`, `timeRequired`, `educationalLevel` |
| a lesson | `LearningResource` + `isPartOf` the course | the parent link is the thing `Article` cannot express |
| any nested page | `BreadcrumbList` | tells a crawler the hierarchy the URL already implies |
| a listing | `ItemList` | turns a page of cards into an ordered set |
| the FAQ band | `FAQPage` | the only one here that can win a rich result outright |
| a how-to lesson | `HowTo` with `step` | matches the teaching format — concept, example, bridge |
| the site itself | `Organization` / `Person` | Ghost emits `Person` for authors; the publisher may want `Organization` |

**One `@graph`, not eight scripts.** Ghost writes its own block; add exactly
one more, and put everything the theme contributes inside a single
`"@graph": [ … ]`. Two blocks are valid and are how a theme adds to rather
than replaces what the platform describes; nine blocks is a page nobody can
debug.

### The rules that make it not break

Learned the hard way — see `09-lessons.md`:

- **`{{json}}` for every value.** Handlebars' `{{ }}` escapes for HTML, so an
  apostrophe becomes `&#x27;` — which lands in the JSON string literally,
  because JSON-LD is parsed as JSON, not HTML. `{{json}}` also escapes `<`,
  `>` and `&` to `<`-style sequences, which is what stops a title
  containing `</script>` from ending the block early.
- **Except URLs**, which need the `{{url absolute="true"}}` helper — and that
  returns a SafeString, which `{{json}}` would serialise as
  `{"string":"…"}`. Quote those by hand in a **triple** stash so an `&` in a
  query string does not become `&amp;`.
- **Never let a `}` sit directly after a `}}`.** `}}}` is a triple-stash to
  Handlebars, the template fails to *compile*, and the whole site 500s. Put
  the closing brace on its own line.
- **`{{@number}}`, not `{{number}}`**, for a position inside `{{#foreach}}`.

### Validate it, do not eyeball it

```bash
curl -s https://SITE/some-post/ | python3 -c "
import sys,re,json
for b in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', sys.stdin.read(), re.S):
    print(json.loads(b).get('@type') or [x.get('@type') for x in json.loads(b)['@graph']])
"
```

If that raises, the page is shipping broken structured data. It is worth a
check script the day a second type is added.

## 3 · Readable by a language model

A model fetches the page and reads the HTML. Everything below is about the
text still being there when it does.

- **The prose must be in the HTML.** It is — Ghost renders `{{content}}`
  server-side. Any future component that fetches its own content on the client
  is invisible to every crawler and model, and that is the one architectural
  line here.
- **One `<h1>`, real `<h2>`/`<h3>` under it.** Headings are the outline a model
  uses to chunk a page. `partials/post/article.hbs` already relies on this for
  its table of contents, so the two requirements reinforce each other.
- **`<time datetime="…">`, not a printed date.** "4 Aug" is ambiguous; the
  attribute is not.
- **Link text that names its destination.** "Start Apex basics", never "here".
  Same rule the accessibility floor already imposes.
- **`alt` that describes, or `alt=""` that admits it is decorative.** A model
  reads alt text as content.
- **Semantic landmarks** — `<article>`, `<nav>`, `<footer>`, `<main id="main">`.
  They mark where the content stops and the chrome starts.
- **Do not lock content behind Members you want indexed.** A gated lesson is
  correctly invisible; a gated *overview* is a page that cannot be found.

### `llms.txt` — **Ghost already does this. Do not build it.**

The convention is a plain-text map of the site at `/llms.txt`, listing the
pages worth reading with a line each. It is `robots.txt` for models, except it
*invites* rather than restricts.

**Ghost 6.57 ships it natively**, behind a setting. It also serves
`/llms-full.txt` and a markdown rendering of every post — append `.md` to any
post URL — which no theme template can match, because a template cannot
re-render a post as markdown.

On this install the setting is **off**, and the endpoints 302 to the homepage:

```
/llms.txt       302 → /          llms_enabled = false
/llms-full.txt  302 → /
```

The 6.46 migration switched it off for upgrading sites, which is why it looks
missing. **The fix is the Admin setting, not a template.**

A theme template was written for this and then deleted, because it would have
been a worse copy of a platform feature — the first question in
`abstract/README.md` is "does Ghost already do it", and here it does. If a
*curated* map is ever wanted alongside the generated one, mount it somewhere
Ghost does not own (`/llms/`) and rewrite at the proxy; `/llms.txt` itself is
claimed by the platform and a routes.yaml entry for it is dead code.

### `robots.txt` — **also Ghost's, and a route cannot override it**

Ghost serves its own, and serves it *before* the routes.yaml router runs. A
`/robots.txt/` route is dead code. Verified against the running site:

```
User-agent: *
Sitemap: http://localhost:2369/sitemap.xml
Disallow: /ghost/      /email/      /r/
Disallow: /webmentions/receive/     /members/api/comments/counts/
Disallow: /.ghost/analytics/api/
```

That is already correct: the sitemap is absolute, the private paths are
covered, and `User-agent: *` means **every AI crawler is already allowed** —
GPTBot, ClaudeBot, PerplexityBot and the rest. For a site that wants to be
found and cited, the default *is* the policy, so overriding it buys nothing
today.

Two things it deliberately does not block, and both are right:

- **`/p/` previews** — `ghost_head` emits `noindex,nofollow` on preview
  context, and a robots block would *hide* that noindex from the crawler that
  needs to read it. Blocking a page is not the same as de-indexing it.
- **`?ref=` params** — canonical tags consolidate them, which is the correct
  mechanism.

**If it ever does need changing**, the only override Ghost honours is a static
`robots.txt` file in the theme root, checked at theme *activation* — so it
needs a re-upload to be noticed, and it is served verbatim, meaning the
sitemap URL has to be hardcoded absolute rather than templated. Serving it at
the CDN in front of Ghost is usually the better answer.

### `ads.txt`

The one of the three that a theme genuinely owns, because Ghost has no opinion
on it. `ads.hbs` renders the `ads_txt` theme setting, and nothing when it is
empty — which is the correct state for a site with no ad inventory.

⚠ **It is reachable only at `/ads.txt/`, with the trailing slash.** A bare
`/ads.txt` has a file extension, so Ghost's static-theme middleware hands it
to `express.static` with `fallthrough: false` and 404s it before the router
runs. IAB crawlers request the bare path, so production needs a proxy
**rewrite** — not a redirect, since whether verifiers follow one is
unverified.

## 4 · Feeds are not legacy

RSS is how the newsletter, aggregators and a good number of model pipelines
actually ingest a site — and Ghost generates it per collection, for free, at
`<mount>rss/`.

Consequences worth knowing:

- **The feed lives where the collection is mounted.** This site's catch-all is
  at `/blog/`, so the feed is `/blog/rss/` and the templates link to it
  there. Move the mount and the feed moves with it — grep `blog/rss`.
- **Every collection gets its own feed**, which is a feature: a reader who
  wants only the courses can have exactly that.
- Ghost also writes `sitemap.xml` and `robots.txt` with no help from the
  theme. Do not add either.

## 5 · The checklist, when adding a surface

1. Does Ghost already describe it? (`Article` covers a plain post.)
2. If not, which type from §2 — and does it need `isPartOf` a parent?
3. Add it to the theme's single `@graph`, via `{{json}}`.
4. Curl the page and parse the JSON. Do not eyeball it.
5. Check the prose is in the HTML with JavaScript off.
6. If the surface has its own feed, link it where a reader would look.
