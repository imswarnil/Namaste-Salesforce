# 16 · Working effectively with Claude Code

Written from what actually happened on this project — the things that worked,
and the things that cost days. Most of it generalises to any AI coding tool,
and all of it is defensible in an interview because it is grounded in a real
failure, not a feature list.

---

## Part 1 · The mental model

**Claude Code is an agent with tools, not an autocomplete.** It reads files,
runs commands, and acts on what it finds. That changes what a good prompt is:
you are not describing code to write, you are describing a **goal and the
constraints on reaching it**.

The three things that determine output quality, in order:

1. **What it can verify.** An agent that can run your tests writes better code
   than one that cannot, because it finds its own mistakes.
2. **What context it has.** It cannot infer a convention that exists only in
   your head or in a Slack thread.
3. **How the task is framed.** "Fix the navbar" and "the navbar overflows at
   1280px, find out why" produce very different work.

### The failure mode to internalise

On this project, every static check passed — build, validator, no undefined
classes, all JS parsing — **and the pages were still wrong.** The agent had no
way to see the result, so it optimised for the signals it had.

> **Give the agent the same feedback loop you have, or it will confidently
> optimise the wrong thing.**

That is the single most useful sentence in this file.

---

## Part 2 · CLAUDE.md — the highest-leverage file in a repo

Claude reads `CLAUDE.md` automatically at the start of a session. It is where
conventions live so they do not have to be re-explained.

**What belongs in it:**
- how to build, test and run the thing
- architecture that is not obvious from the file tree
- conventions with the REASON attached
- traps — the things that look fine and are not

**What does not:**
- anything derivable from the code
- long prose (it is loaded every session; keep it dense)

**The pattern that works best is a trap with its reason:**

```md
⚠️ Never call a Ghost helper across `../` ({{../url}}) — Ghost throws and 500s
the page. Dotted property access ({{primary_tag.slug}}) is fine.
```

A rule without a reason gets followed until it is inconvenient. A rule with a
reason gets followed.

Nested `CLAUDE.md` files apply to their subtree, which is useful in a monorepo.
`#` at the start of a message asks Claude to add a memory for you.

---

## Part 3 · Tools worth knowing by name

### Skills
Packaged instructions for a recurring task — a deploy runbook, a review
checklist, a project-specific workflow. Live in `.claude/skills/`, invoked as
`/name`. **Use one when you have written the same three-paragraph explanation
more than twice.** The value is that the instructions load only when relevant,
rather than bloating every session.

### MCP (Model Context Protocol)
An open standard for connecting a model to external systems — a database, a
ticket tracker, a browser, an internal API. A server exposes tools; the client
(Claude Code, or another app) can call them.

Configured per project or globally; servers can be local processes or remote
endpoints. The point is that **it is a standard**: one integration works across
any MCP-speaking client, instead of a bespoke plugin per tool.

Worth being able to say in an interview: *"MCP is how you give a model
first-class access to your systems without hard-coding an integration per
model or per vendor."*

### Subagents
A separate context for a scoped task, returning only its conclusion. Right for
broad searches across many files where you want the answer and not the file
dumps. Wrong for a single lookup you could do directly.

### Hooks
Shell commands the harness runs on events — before a tool call, after an edit,
on stop. **This is how you enforce a rule rather than request one.** "Always
run the formatter after editing" is a hook, not a prompt: the harness executes
it deterministically.

### Plan mode
Think and research without editing. Use it when the approach is unclear, not
when the task is obvious.

### Headless / CI
`claude -p "…"` runs non-interactively for scripted use — triage, batch edits,
a review step in a pipeline.

---

## Part 4 · How to actually prompt

### Give the goal and the constraint, not the steps
> ✅ "The navbar overflows at 1280px. Find out why and fix it, without adding
> theme CSS — the design system should already have a variant for this."

> ❌ "Add overflow-x hidden to the navbar."

The first got a correct answer (a `flex: none` on the links row, fixed with an
existing variant). The second would have hidden the bug.

### Ask for the diagnosis before the fix
"Find out why X happens and tell me before changing anything." Cheap, and it
catches the case where the fix would have been wrong.

### Insist on evidence over assertion
The most valuable correction on this project was: *"I still think components
are not in sync."* That pushed a shift from **reasoning about** class names to
**measuring** them — a script comparing the design system's reference templates
against the theme's markup. It produced a number that moved from 51% to 77%.

> **If the agent asserts something is fine, ask how it knows. If the answer is
> not a command it ran, it is a guess.**

### Correct the process, not just the output
"Don't just fix it, tell me why it happened" produces a fix AND a rule that
prevents recurrence — which is what `abstract/10` is.

### Work in verifiable increments
Small changes, each ending in a green check and a commit. Long unverified
stretches are where errors compound silently.

---

## Part 5 · The specific lessons from this project

**1. Static checks are necessary and not sufficient.**
Build, validator, linters — all green while the site was visually broken. Add
a check that observes the *result*: a screenshot, a rendered page, a real
browser.

**2. Comparing names is not comparing things.**
A module was declared "disjoint from the design system, nothing to migrate."
It was disjoint by NAME — every class was a design-system component under a
different one. ~100 classes of duplication. **Compare what things ARE.**

**3. When markup moves, grep the scripts in the same change.**
Selectors that no longer match fail silently. Build green, validator green,
feature dead.

**4. Ask the agent to quantify, then watch the number.**
Two metrics beat one: "does the right class appear" said 77%; "is the markup
around it still hand-rolled" said 59%. Both were true, and only having both
told the real story.

**5. Say when something is not broken.**
A long stretch here was spent hunting a breakage that did not exist. Precise
feedback — *"nothing was broken, I want a rebuild"* — would have saved it.

**6. Destructive requests deserve a confirmation.**
"Delete everything" can mean five different scopes. The good pattern is: the
agent proposes the exact list and waits. Insist on that.

---

## Part 6 · What to say in an interview

Framed as judgement rather than tool-trivia:

- **On context:** *"I keep conventions in a file the agent loads automatically,
  and I write the reason next to each rule — a rule without a reason gets
  followed until it is inconvenient."*
- **On verification:** *"The agent optimises for the signals it has. If it can
  only see the build, it will make the build pass. I make sure it can see what
  I care about — tests, a rendered page, a real metric."*
- **On scope:** *"I have it diagnose before it fixes, and work in increments
  that each end green. Long unverified stretches are where errors compound."*
- **On MCP:** *"A standard protocol for connecting a model to real systems, so
  one integration works across clients rather than a bespoke plugin per tool."*
- **On limits:** *"It is very good at consistent, wide, mechanical change and
  at explaining a codebase. It is weak at anything it cannot observe — which is
  a tooling problem, not a model problem, and mostly fixable."*

## Part 7 · The one-line version

> **Give it the goal, the constraints, and your feedback loop — then check the
> thing it could not see.**
