# 19 · The teaching method

`12` decides *what* gets made and in what order. This decides **what a lesson
is made of**, and it is the more valuable of the two — format is what makes
teaching repeatable by someone who is not you.

Every rule here has a reason attached. A rule without a reason gets followed
until it is inconvenient.

---

## The stance

> **Teach the failure first, then the fix. Never the API first.**

Salesforce documentation already explains what every feature does, it is free,
and it outranks you. Competing with it is unwinnable and pointless.

What the docs cannot do is tell someone **why their thing broke at 2am**.
That is the entire gap this site exists to fill, and it dictates the shape of a
lesson: start from a symptom the reader recognises, not from a feature.

| Docs do this | You do this |
| --- | --- |
| "`Database.Stateful` retains instance state" | "Your batch resets its counter every 200 records. Here is why." |
| lists the governor limits | "Here is the exception. Here is the line that caused it." |
| "Permission sets grant access" | "Why your user still can't see the record after you gave them the profile." |

The second column is also what people type into Google, which is not a
coincidence — it is the same gap.

## The three questions every lesson answers

In this order. A lesson missing any one of them does not work.

1. **What breaks?** — the symptom, concretely, with the real error text.
2. **Why?** — the smallest mental model that explains it. *One* model.
3. **What do I do?** — steps, with a way to tell they worked.

Most technical writing answers 3 and gestures at 2. **Skipping 1 is why people
bounce**: they cannot tell whether the page is about their problem until they
have read it, so they don't.

---

## The lesson skeleton

Eight blocks. Same order every time. The consistency is the feature — a
returning reader learns where things live and starts skimming to the block they
need, which is what a reference-quality lesson must allow.

```
1  OUTCOME        one sentence: what you can do after this
2  THE FAILURE    the symptom, verbatim — error text, wrong number, silence
3  THE MODEL      the smallest correct explanation. One diagram maximum.
4  WORKED EXAMPLE complete, runnable, annotated. Nothing left as an exercise.
5  FADED REPEAT   the same shape again, with the middle removed
6  YOUR TURN      one task + how to know you got it right
7  WHEN IT BREAKS limits, edge cases, the version this changed in
8  NEXT           the single next lesson, named
```

### 1 · Outcome
From `12`: *"After this, you can take a governor-limit exception and find the
line that caused it, first time."* If you cannot write this sentence, you have
a topic, not a lesson. Stop and go find the concept.

### 2 · The failure
**Paste the actual error.** `System.LimitException: Too many SOQL queries: 101`
is a search term; "you may encounter limit errors" is not. This block is what
makes the page findable and what tells a reader in three seconds that they are
in the right place.

### 3 · The model
The **smallest** explanation that makes the fix predictable rather than
memorised. Ruthlessly one model — the instinct to also mention the related
thing is where lessons go to die.

Test: *could the reader now predict the outcome of a case I did not show them?*
If no, the model is decoration. If they need the second model, that is the next
lesson, and it is block 8.

### 4 · Worked example
**Complete and annotated.** Do not leave steps to the reader here.

This is not laziness on the reader's part — studying a fully worked example is
measurably more effective for a novice than attempting the problem, because
attempting it spends all their working memory on search instead of on the
pattern. Give them the pattern first.

Every example must **run**. Code that has never been executed is the fastest
way to lose a technical audience permanently, and it will be found.

### 5 · The faded repeat
The same problem shape, with the middle removed:

```apex
// You do this bit:
for (Account a : scope) {
    // ← the query that must not be here. Move it where?
}
```

This is the step almost everybody skips, and it is where the learning actually
happens. Going straight from "watch me" to "now do it alone" is the cliff
people fall off. Fading is the ramp.

### 6 · Your turn
**One** task, and — non-negotiable — **how they know they succeeded**. "Try
experimenting with bulkification" is not a task. "Make this trigger handle 200
records. You'll know it works when the debug log shows 1 SOQL query, not 200."

Retrieval beats re-reading by a wide margin. This block is the retrieval.

### 7 · When it breaks
Limits, the edge case, the version where it changed, the thing that looks like
it should work. This is the block that makes a lesson *trusted* rather than
merely correct — it is the difference between a tutorial and something someone
sends to a colleague.

### 8 · Next
Name **one** next lesson and link it. A menu of six is a decision, and a
decision at the end of a lesson is where sessions end.

---

## The steps format

For any procedure — a click-path, a setup, a deployment.

**One action per step.** If a step has an "and" in it, it is two steps. The
reader is alternating between screen and page; every step is a context switch,
and a compound step is where they lose their place.

**A consistent path notation**, always the same, always in `code`:
`Setup → Object Manager → Account → Fields & Relationships → New`

**Say what success looks like** at the end, and at any step where it is not
obvious:
> You should now see **Status: Active** and a green tick.

**Name the trap in the step it happens in**, not in a note at the bottom.
Nobody reads the bottom note before they need it.

**Number what is ordered; bullet what is not.** Numbered steps promise
sequence. Using them for an unordered list of options teaches the reader that
your numbers are decorative, and then they stop following them where it matters.

**Screenshots are a maintenance liability.** Salesforce ships three releases a
year and the UI moves. Screenshot only what cannot be written: a chart to
interpret, a layout to match. Never screenshot a click path or code — text
survives the release, is searchable, and can be copied.

---

## Style

**Second person, present tense, active.** "You add the field." Not "the field
should then be added by the administrator."

**Ban `simply`, `just`, `obviously`, `of course`, `merely`.** Every one of them
tells a stuck reader that their difficulty is a personal failing. They add
nothing when things go right and do real damage when they don't.

**Show the real thing.** Real org, real data volumes, real error text. Sanitise
names, never sanitise the shape.

**Say the cost.** "This works but it is O(n) queries and will die at 10k rows."
Trust comes from stated limits, not from confidence.

**Define an acronym once, on first use, per lesson** — not per site. Someone
landed here from Google and has not read your other pages.

**Short paragraphs.** Most of this audience is reading on a phone between
meetings, or on a second monitor while the thing is still broken.

---

## Difficulty and prerequisites

Difficulty is **not** a property of the lesson — it is the gap between the
lesson and the reader. So state the gap, not a vibe.

Not: *"Intermediate."*
But: **"Assumes you have written a trigger and seen a governor limit error."**

That is checkable by the reader in two seconds, and it is why `#prereq-*` in
`18` is a tag and not a badge. `#level-*` still earns its place for browsing —
"everything for a beginner, in order" is a real request — but it is a filter,
never an excuse to skip stating the actual assumption.

---

## Sequencing a course

**Order by dependency, not by the reference manual.** The docs are organised by
feature area because they are a reference. A course organised that way teaches
in the order things are *documented*, which is almost never the order they are
*needed*.

**Every lesson ends with something that works.** Not "we'll wire this up in
lesson 7." A learner who stops after lesson 3 must still have gained a working
thing, because most learners stop.

**Spiral, don't exhaust.** Cover a topic at the depth needed now; return later
at greater depth. Exhausting `SOQL` in lesson 2 means lesson 2 is 6,000 words
and nobody reaches lesson 3.

**Interleave.** A module that is nine trigger lessons in a row produces people
who can write triggers only when told the answer is a trigger. Mix in the
neighbouring choice — Flow, an async pattern — so they practise *choosing*,
which is the actual job.

---

## Failure modes to watch for

| Symptom | What it actually means |
| --- | --- |
| The lesson is a feature tour | You started from the API, not the failure |
| Nobody finishes it | Two concepts wearing one title — split it |
| It needs three prerequisites | It is lesson 4 pretending to be lesson 1 |
| The example is `Account`/`Contact` with 3 rows | It will not survive contact with a real org, and readers know it |
| You cannot write the outcome sentence | It is a topic |
| The comments all ask the same question | That question is block 3, and it is missing |

**Read the comments as a defect log.** A repeated question is not readers being
slow, it is a hole in the lesson at a known location. Fixing the lesson beats
answering the question, and it is the cheapest content improvement available.

---

## How this binds to the theme

The skeleton is not just an authoring convention — it is a **rendering
contract**. Blocks 1, 2, 6 and 7 are the ones a template can lift out of the
body and present as their own component: an outcome banner, the error block, a
task card, a limits callout.

That only works if every lesson really has them in the same order, which is the
practical argument for the format. It is also why `09-content-prompts.md`
exists: the prompts encode this skeleton so generated drafts arrive already
shaped.

> ⚠️ **Do not build components for these blocks until several real lessons
> exist.** Designing a "worked example" component from one imagined lesson is
> exactly the mistake `10` documents. Write five, see what actually repeats,
> then check whether NSDS already has it before writing a class (`00`).
