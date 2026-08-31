# 10 · User tracking — measure like a site with zero readers

The theme now has the wiring for GA4, PostHog and OneSignal
(`partials/services/`), each dormant until its custom setting is filled in.
This file is the argument for **leaving almost all of them empty**, and the
plan for when to stop.

The short version: Ghost 6 already ships the analytics this site needs for
its first year, at zero page weight. Every script you add is a tax on every
reader to answer a question you could not act on yet.

---

## 1 · The measurement question first

This site has **zero published posts and zero subscribers**. That is not a
gap in the analytics; it *is* the analytics. Every dashboard you could
install today would render the same chart — a flat line — with different
fonts.

Tooling is premature when the decisions it could change do not exist yet.
There is no headline to A/B test against no traffic, no funnel to optimise
before there is a course to fall out of, no cohort to retain before anyone
has arrived twice. At this stage exactly three questions matter, and none
needs a new script:

1. **Is anything being found?** — Google Search Console: impressions and
   queries, zero bytes on the page.
2. **Where do the visitors that exist come from?** — Ghost's native
   analytics: sources, top content, locations.
3. **Does anyone care enough to subscribe, and which post did it?** —
   Ghost's member attribution, recorded on the member record itself.

The honest failure mode this section exists to prevent: a solo founder
spending a content-writing evening wiring Segment into Mixpanel into a
dashboard that will report `0` either way. **Instrumentation is not
progress.** Publishing is.

## 2 · The layers — what each is actually for

Tracking tools get bought as one category and are five. Adopt them in this
order, because each layer is useless without the one before it producing
signal:

| Layer | Question it answers | Examples | Useless until |
|---|---|---|---|
| **Web analytics** | which pages, from where, how many | Ghost native, GA4, Plausible, Fathom, Umami | you publish |
| **Product analytics** | what does one person DO across a session/funnel | PostHog, Mixpanel, Amplitude | a funnel exists (courses, paid tiers) |
| **CRM** | who is this person and what did we say to them | HubSpot free, (Ghost members admin, at small scale) | you have conversations, not just readers |
| **Enrichment** | what company/role is behind this email | Clearbit, Apollo, Koala, Common Room | you sell to teams |
| **Messaging** | say the right thing at the right moment | Ghost email, Customer.io, Intercom, Crisp, OneSignal | there is a lifecycle to message about |

Two structural notes. **Segment/RudderStack are plumbing between layers**,
not a layer — a pipeline is worth owning when three or more tools consume
the same events, and a pipeline installed first is an empty pipe with a
monthly bill. And **Ghost itself already occupies three of the five** at
small scale: web analytics natively, CRM-of-record via members, messaging
via newsletters. The build-vs-buy question for each layer is really "what
does Ghost stop being enough for, and when" — §4 and §8.

## 3 · The tools, with the trade-offs written down

Weights are what §6 measures — wire size gzipped; parse cost is roughly 3×
that. "Verdict" is for **this** site: a solo-founder Salesforce learning
site with EU readers, courses coming, paid tiers eventually.

| Tool | Cost | Weight (wire) | Privacy posture | Verdict |
|---|---|---|---|---|
| **Ghost native analytics** | included | ~0 (first-party, cookie-free) | best available: no cookies, 24-hour windows, your domain | **use now — it is already on** |
| **GA4** | free | ~149 KB | consent required in the EU; data goes to Google; Schrems-era rulings against it in several EU DPAs | **skip.** Ghost + Search Console answer everything GA4 would here. The partial exists for a future ads/demographics need, not for now |
| **Plausible / Fathom** | ~$9–14/mo | ~1.3 / ~2.1 KB | cookie-free, EU-hosted, no consent banner needed | skip — lovely tools, but they duplicate Ghost native for money |
| **Umami** | free self-hosted / cloud tier | ~2.3 KB | cookie-free, self-hostable | skip, same reason; the self-hosting is a hobby wearing an analytics costume |
| **PostHog** | free ≤1M events/mo | ~85 KB | EU cloud available (`eu.i.posthog.com`) — the theme defaults to it; consent required, it builds person profiles | **the one product-analytics tool to adopt — when the LMS funnel exists, not before.** One tool, both products (site + app), includes replay and flags, kills three other line items |
| **Mixpanel / Amplitude** | free tiers, then steep | ~30–40 KB (unmeasured) | consent required; US-default hosting | skip — never run a second product-analytics tool; PostHog's free tier is the most generous of the three |
| **Segment / RudderStack** | $120+/mo / self-host | ~30 KB + destinations (unmeasured) | amplifies whatever you pipe through it | skip until ≥3 tools consume the same events, which is years away if ever |
| **HubSpot free CRM** | free (that is the hook) | none if kept off the site; ~20 KB+ with forms/chat embeds (unmeasured) | consent required for its tracking script | skip until actual sales conversations exist (team-training deals). Keep its script off the site even then |
| **Customer.io** | ~$100/mo | none (server-side email) | fine — it messages people you already know | the first paid messaging upgrade — at "paid tier live and onboarding emails demonstrably needed", not at a subscriber count |
| **Intercom** | $39+/seat, rises fast | ~200 KB+ (unmeasured) | consent required | skip. The heaviest common widget on the web, priced for funded startups |
| **Crisp** | free tier | ~30–100 KB (unmeasured) | consent required | skip; a `mailto:` and the Ghost portal cover support at this scale |
| **Hotjar** | free tier | ~40–80 KB (unmeasured) | consent required; session recording is the most invasive category | skip — and when replay is wanted, PostHog already includes it |
| **MS Clarity** | free | ~10–25 KB (unmeasured) | "free" is paid for with data sharing to Microsoft; consent required | skip, same replacement argument |
| **Clearbit / Apollo enrichment** | $$$ | none (server-side) | processes personal data you did not collect from the person — GDPR-hard | skip until selling to companies; then enrich in the CRM, never on the page |
| **Koala / Common Room** | free-ish tiers | ~10 KB (unmeasured) | intent tracking; consent required | B2B pipeline tools for sites with a sales motion. Not this site, possibly ever |
| **Dub** | free tier | none (redirect-side) | fine | skip — Ghost attributes inbound links natively (§4); `?ref=` costs nothing and needs no account. Revisit only for public link-in-bio aesthetics |
| **OneSignal** | free tier | ~43 KB | its consent is the browser's own permission prompt | wired but empty. Web push earns its place when there is a stream worth interrupting people for — not before content ships |

The pattern in the verdicts: **at this scale, every category is either
covered by Ghost, covered by PostHog-later, or not applicable until there
is a sales motion.** The whole stack for year one is Ghost + Search Console,
and the whole stack for year two is probably Ghost + Search Console +
PostHog EU.

## 4 · What Ghost already gives you — free, and already on

Verified against Ghost 6's own documentation; do not re-buy any of this.

- **Native web analytics** (Ghost 6, Tinybird-backed): unique visitors
  counted in 24-hour windows — **cookie-free, no persistent browser
  storage, fully first-party through your own domain** — plus total views,
  top content, top sources (direct/search/social/referral), and visitor
  locations. On Ghost(Pro) it is simply on. Self-hosted Ghost 6 needs the
  Tinybird-backed analytics service configured (TryGhost/TrafficAnalytics)
  — verify against the deployment before assuming the Traffic tab fills.
- **Member source attribution**: when someone subscribes, Ghost records
  which post converted them and the source that brought them. The Growth
  view aggregates it — members and MRR by source and by post. This is the
  question "which content works" answered natively, and it is why Dub-style
  link attribution is not needed inbound.
- **Newsletter analytics**: delivered/opened/clicked per email, subscriber
  growth, top campaigns. Per-member engagement shows on the member record.
  Outbound link tagging appends `?ref=yoursite` to links in emails, so the
  site's own newsletter shows up attributed in other people's analytics —
  and in Ghost's, on the return trip.
- **Member events**: the admin activity feed — signups, sign-ins, email
  opens/clicks, comment activity, paid subscription started/cancelled.
  A solo founder scrolling this feed weekly *is* the CRM at <1000 members.
- **Members as a database**: every member carries tiers, **labels**
  (free-form, filterable), created-at, engagement, attribution. The Admin
  API reads and writes all of it, and **webhooks** fire on member events —
  which is the integration surface everything in §5 hangs off.

What Ghost does **not** give: behavior inside a page or across a funnel
(product analytics), automated multi-step email sequences triggered by
behavior (messaging), or any scoring. Those are the real gaps the external
tools exist for — none of which matters before there is behavior to score.

## 5 · Lead scoring and segmentation — what Ghost can and cannot do

**Natively:** segmentation, coarse but real. Email sends target *all /
tier / label* combinations; content gates by tier (`public`, `members`,
`paid`, or specific tiers); labels are applied by hand in admin, at import,
or via the Admin API. That is enough to run "founding member" cohorts,
"asked about the Data Cloud course" lists, and tier-based drips-by-hand.

**Not natively:** scoring of any kind. Ghost will not rank members by
engagement or fire an email when someone hits a threshold.

**The pattern when scoring becomes real** (it is a paid-tier-era problem):

1. Ghost **webhooks** (`member.added`, `member.updated`, email events) post
   to a small worker — the Cloudflare account this site already has is the
   natural home.
2. The worker keeps a score per member — signup source, email clicks,
   which gated pages they hit — trivial arithmetic, not ML.
3. It writes the score **back as a Ghost label** (`score-hot`,
   `score-warm`) via the Admin API (`PUT /members/:id`, labels array).
4. Labels being email-targetable closes the loop: "send the annual-plan
   pitch to `score-hot` free members" is now a native Ghost send.

That keeps Ghost as the single member record — the moment two systems both
claim to know who a member is, they disagree. An external tool
(Customer.io, HubSpot) earns its place only when the *messaging* outgrows
Ghost's editor, and it should still treat Ghost as the source of truth,
synced by the same webhooks.

## 6 · The performance budget

Measured 2026-08 (curl, gzip transfer size; decompressed size is what the
main thread parses). The theme's whole compiled stylesheet is ~467 KB raw
for comparison — a single analytics tag can out-weigh the design system.

| Script | Wire (gz) | Decompressed | LCP effect | INP effect |
|---|---|---|---|---|
| Ghost native analytics | ~0 (first-party, no tag to add) | — | none | none |
| Plausible | 1.3 KB | ~5 KB | none | none |
| Fathom | 2.1 KB | ~8 KB | none | none |
| Umami | 2.3 KB | ~9 KB | none | none |
| OneSignal v16 | 0.6 KB loader + 42.5 KB deferred | ~140 KB | none (defer) | small; SW registration off main path |
| PostHog `array.js` | 85 KB | 267 KB | none *as wired* (async, end of body) | real: ~250 ms+ of parse/exec on a mid-range phone; replay adds more |
| GA4 `gtag.js` | 149 KB | 417 KB | none *as wired* | the worst here: long parse tasks land exactly when the reader first scrolls or taps |
| Hotjar / Clarity / Intercom / Crisp | ~40 / ~15 / ~200+ / ~50 KB (unmeasured) | 3–4× wire | Intercom's iframe can also fight for bandwidth pre-LCP | recording tools listen to every input — a standing INP tax |

Two rules fall out. **"Async at the end of body" protects LCP, not INP** —
the parse happens regardless, on the same thread that must respond to the
reader's first tap, which is why the partials load *nothing at all* until
consent rather than loading politely. And **the budget is a count, not
just kilobytes**: every third-party adds a DNS+TLS round trip, a consent
question, and a failure mode. This site's budget is: Ghost native always;
at most **one** script from §3's table live at a time; anything session-
recording only while actively investigating something specific, then off.

## 7 · Privacy, GDPR, consent — honestly

This site will have EU readers from day one — Salesforce's market
guarantees it — so build to GDPR and everything else is covered.

- **Cookie-free, aggregate-only tools need no consent banner.** Ghost
  native analytics, Plausible, Fathom, Umami store nothing on the device
  and identify nobody. This is the strongest practical argument for the
  §8 plan: the year-one stack requires no banner at all, and the site
  simply does not have one until a setting turns one on.
- **GA4 and PostHog are consent-required.** They set identifiers and build
  profiles. The theme's gate (`partials/services/consent.hbs`) blocks them
  entirely — no script, no request — until the reader says yes, honours
  Global Privacy Control and DNT outright, and remembers "no". PostHog is
  pinned to the **EU cloud by default** (`posthog_host`), which keeps the
  data in the EEA; GA4 has no EU-residency answer, which is half the
  reason its verdict in §3 is "skip".
- **What the gate is not:** a compliance product. It covers exactly the
  scripts this theme adds. It has no per-vendor granularity, no consent
  records, no withdrawal UI (a /privacy page should say "clear site data
  to reset your choice"). The day the stack has three consent-requiring
  vendors is the day to buy a real CMP — §8 is designed so that day never
  comes.
- **Email is also GDPR.** Ghost's double-opt-in-able signup, unsubscribe
  handling and export cover the newsletter; the rule to keep manually is
  never to export members into a tool that was not named when they signed
  up. Enrichment (§3) is the sharp edge here — appending Clearbit data to
  a subscriber is processing they never saw coming; done at all, it
  belongs in a CRM with a lawful-basis argument, not in this repo.
- Ghost(Pro)'s analytics data is stored in EU regions per Ghost's own
  documentation — one more thing not to have to paper over.

## 8 · The plan

**Now — 0 posts, 0 subscribers.** Ghost native analytics (already on) +
Google Search Console (zero weight). Every theme setting in
`partials/services/` stays **empty**; the site ships no third-party
script, no cookie, no banner. Put `?ref=` on every link you share by hand
— Ghost attributes it, and the habit is the whole of "attribution
infrastructure" at this scale. Then close this file and write posts;
nothing in it beats publishing.

**At ~100 subscribers** (really: when a weekly newsletter is actually
going out). Still no new scripts. Start reading two Ghost views weekly —
Growth-by-source and newsletter clicks — and let them pick next month's
topics. Begin labelling members by interest as replies come in
(`interest-admin`, `interest-dev`); it is minutes of work that makes the
1000-tier segmentation real instead of retroactive. If push notifications
have a genuine stream to carry by now, `onesignal_app_id` is the one
setting worth considering — it is the only wired service whose value does
not depend on traffic volume.

**When the LMS funnel exists** (courses live, sign-up → lesson → paid path
— this threshold is an event, not a subscriber count). Set `posthog_key`
with the default EU host, same project as the Next.js app, so one funnel
spans both products. Accept the consent banner that comes with it — that
is the honest price of person-level analytics, and the gate is already
built. This is also the moment lead scoring (§5) starts meaning something.

**At ~1000 subscribers / paid tiers live.** Add the §5 scoring worker
(webhooks → score → labels). Adopt **Customer.io** only if onboarding and
win-back sequences are demonstrably being done by hand in Ghost's editor —
it replaces labor, not curiosity. Revisit HubSpot/enrichment only if
team-training sales conversations have appeared. Everything else in §3
keeps its "skip" until one of its named thresholds — a second funnel tool,
a third consent vendor, a sales motion — is actually crossed, and the
correct number of analytics scripts on the page is still **one**.
