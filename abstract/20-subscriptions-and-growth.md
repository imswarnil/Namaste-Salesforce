# 20 · Subscriptions, pricing, and the path to them

Three things: what the tiers are called, what they cost, and how content
becomes subscribers. The third is the one that decides whether the first two
matter.

> **On the numbers below.** They are a defensible *starting hypothesis* built
> from the shape of this market, not from researched competitor data or your
> own traffic. Treat them as something to test and move, and expect the first
> set to be wrong. What is worth keeping regardless is the **structure** — the
> number of tiers, where the line between free and paid sits, and why.

---

## The tiers

| | **Free** | **Practitioner** | **Architect** | **Team** |
| --- | --- | --- | --- | --- |
| Who | anyone reading | someone doing the job | someone levelling up | a company |
| Monthly | ₹0 | ₹499 | ₹999 | — |
| Yearly | ₹0 | **₹4,499** | **₹8,999** | ₹35,000 / 5 seats |
| ≈ USD/yr | — | ~$54 | ~$108 | ~$420 |

### Why these names

They are **the career ladder this audience is already climbing** — Admin →
Developer → Architect is how Salesforce itself frames progression, and
"Architect" is a title people genuinely want on LinkedIn. A tier name that
names an outcome sells better than one that names a quantity, because the
customer is buying the outcome.

Avoid: Bronze/Silver/Gold (says nothing), Basic/Pro/Premium (says nothing, and
"Basic" insults the person who picked it), and anything borrowed from
Trailhead's rank names — that is Salesforce's trademark territory and it would
confuse the two.

Keep **three paid tiers maximum**, and really you want two. Every extra tier is
a decision you are asking a stranger to make, and a fourth column measurably
reduces the number of people who pick any.

### Why annual is the headline

The yearly prices are ~25% off monthly, and they should be the *default
selection* in Portal, for two reasons — one universal, one specific to you:

1. Learning is a months-long commitment. A monthly plan invites a cancel
   decision every 30 days, right when someone is between courses.
2. **Recurring card payments in India carry real friction.** RBI's e-mandate
   rules require additional setup for recurring card charges, and Indian Stripe
   accounts have their own constraints on international recurring payments.
   One annual charge sidesteps a large amount of this.

> ### ⚠️ Verify before you price anything
>
> This is the biggest operational unknown here, and it is worth an afternoon
> before it is worth a design:
>
> - **Currency.** Ghost tier prices are tied to your Stripe account. You will
>   likely be charging one currency to everyone — INR to a US reader, or USD to
>   an Indian one. Neither is free of consequence.
> - **Indian recurring mandates.** Confirm with Stripe what actually works for
>   an Indian account taking both domestic and international subscriptions.
> - **One-time payments.** Ghost is subscriptions-only; there is no native
>   one-off checkout (see `18` on `/toolkit/`).
>
> Check Stripe's and Ghost's current documentation. Do not take these lines as
> settled — they are exactly the kind of platform detail that moves.

---

## The line between free and paid

**This is the single most consequential decision on this page.** Get it wrong in
either direction and nothing else compensates.

```
FREE, public, indexed          →  BLOG · DOCS · TRAINING
FREE, but costs an email       →  downloads · progress tracking · newsletter
PAID                           →  COURSES · TOOLKIT · CERT PREP
```

### The rule

> **Information is free. Structure is paid.**

Every fact you would teach is already somewhere on the internet at no cost.
Nobody will pay you for a fact. What is genuinely scarce, and what people pay
for without resentment, is:

- **Order** — the right things in the right sequence, so no time is spent deciding what to learn next
- **Compression** — the 8 hours of docs that mattered, out of 80
- **Trust** — someone who has hit this in production says do it this way
- **Completion** — a path with an end, and a way to know you reached it

That is why **courses are paid and training is free**, even though both teach.
Training is a set of lessons; a course is a *path* with a sequence, a
prerequisite chain and an ending. The path is the product.

### Why the free half must stay genuinely free

Gating documentation or the training track would be the intuitive move and it
would be a serious mistake. The free content is not a loss leader you tolerate
— **it is the entire acquisition channel.** Search cannot index what it cannot
read, and a `#cert-pd1` landing page assembled from free lessons (`18`) is the
top-of-funnel that costs nothing to run.

A site that gates early has no traffic to convert.

### Public preview — use it on every paid post

Ghost lets a paid post publish a **public preview**: the first section renders
publicly and is indexed, then the rest is gated. Use it everywhere, and put the
split after the *problem statement*, never before.

That way the page ranks for the symptom someone searched, proves it is about
their exact problem, and asks for the subscription at the moment of highest
intent — rather than showing a paywall to someone who cannot yet tell whether
you have their answer.

---

## The path from reader to subscriber

Four stages. **Nobody skips one**, and most attempts to grow fail by trying to
run stage 1 straight into stage 4.

```
1 · FOUND       search / LinkedIn / YouTube  →  a free page that solves one thing
2 · KNOWN       that page offers ONE relevant thing for an email
3 · TRUSTED     newsletter, weekly, useful, for several weeks
4 · PAID        a specific offer, at a moment that makes sense
```

### 1 · Found

**SEO is the main channel and the compounding one.** This audience searches
error messages, so `19`'s rule — paste the real error text in block 2 — is not
a style preference, it is the acquisition strategy. `System.LimitException: Too
many SOQL queries: 101` is a query with intent behind it.

**LinkedIn is where this audience actually lives**, more than any other
platform. It is a distribution channel, not a content channel: the post makes
one sharp claim from a lesson and links to it (`12`, step 5).

**Community answers compound quietly.** A genuinely good answer in the
Trailblazer Community or r/salesforce, linking to the lesson that goes deeper,
is durable, targeted traffic. Answer the question fully in the reply — a
link-only answer is spam and gets treated as spam.

### 2 · Known — the email is the asset

Search rankings and social reach are rented. The list is owned. Ghost's free
member signup is the most important conversion on the site, and it is *not* the
paid one.

**One offer per page, and specific to that page.** A governor-limits lesson
offers a governor-limit cheatsheet — not "subscribe to our newsletter." The
generic ask converts at a fraction of the specific one, because the specific
one is obviously about the thing the reader is currently doing.

This is what the free-member tier is *for*. It costs you nothing and it is the
entire middle of the funnel.

### 3 · Trusted

**Weekly, same day, actually useful.** The newsletter's job is to be worth
opening on a week when you are selling nothing — that is what makes it work on
the week you are.

Ghost sends posts as email natively. **Do not send everything.** A newsletter
that is an RSS dump teaches people to stop opening it. Curate: one main thing,
one short note, one link.

Email-only posts (never published to the site) are worth using occasionally —
they make the list feel like a place rather than a broadcast.

### 4 · Paid — ask at the right moment

The moments that convert, in rough order:

1. **Finishing something free.** Someone who just completed the training track
   has proved intent and has momentum. This is the single best moment and most
   sites waste it on a "thanks for reading."
2. **Hitting a paid lesson mid-path** — the public preview moment above.
3. **A launch.** A new course, announced to the list, with a genuine reason to
   act now.
4. **Renewal season.** Cert deadlines and appraisal cycles are real dates
   people plan around.

Use Ghost **Offers** for launches and win-backs rather than editing tier prices
— an offer is a tracked, expiring, shareable link, so you can tell what worked.

**Never discount below your annual price for new customers only.** Existing
subscribers see it, and it is the fastest way to teach everyone to wait.

---

## Making the free tier worth signing up for

A free tier that only means "you get emails" converts poorly. Give it something
the reader can *feel*:

- **Progress tracking** on the free training track — a completion state is a
  reason to come back and a reason to log in
- **The download library** — cheatsheets, checklists, ERD templates
- **Comments** — Ghost has native member comments; a lesson with a real
  discussion under it is a page people return to
- **Early access** to a lesson a week before it is public

Each of these costs you approximately nothing and each is a reason to create an
account rather than bookmark.

---

## What to measure

Four numbers. Ignore the rest until these are moving.

| Number | Why it and not something else |
| --- | --- |
| **Free signups / week** | the top of the funnel; everything downstream is a ratio of it |
| **Free → paid conversion %** | the health of the free/paid line. Below ~1%, the line is wrong, not the price |
| **Annual share of new paid** | your cash-flow and churn exposure in one number |
| **Churn, monthly** | above ~5–6% you have a retention problem, and no amount of acquisition fixes it |

**Not:** pageviews, follower count, or total posts published. All three move
without the business moving, which makes them comfortable and useless.

Ghost's own dashboard covers signups, conversion and churn. Do not build
analytics before you have numbers worth analysing.

---

## Sequencing — do not build this in the order it is written

Roughly six months, and each stage exists because the next one fails without it:

1. **Free content only.** No tiers, no Stripe, no Portal configuration. Get to
   ~30 genuinely good lessons and let search find them. **You cannot convert
   traffic you do not have**, and this stage is the one people skip.
2. **Turn on free membership.** Add the per-page offers and the newsletter.
   Build the list while it is still cheap to change your mind about everything.
3. **One paid tier — Practitioner — and one finished course.** One. A pricing
   page with three tiers and no product is a landing page for a business that
   does not exist.
4. **Then Architect, the toolkit, and Team**, in that order, and only where the
   list has told you there is demand.

> The most common failure is building the pricing page first, because it is the
> most fun part and it feels like progress. It converts nobody, because at that
> stage there is nobody to convert.

---

## Status

**Everything on this page is a proposal.** Tier names and the free/paid line are
the parts I would defend hardest; the numbers are the parts most likely to be
wrong. Neither is recorded as decided — when you settle them, they become an
ADR in [`decisions/`](decisions/) with the reasoning, so the next revision is
an argument with evidence rather than a fresh guess.

Related: `12` (what to make), `19` (how to teach it), `18` (`/toolkit/` and the
one-time-payment constraint).
