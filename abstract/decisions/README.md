# abstract/decisions/ — the decision record

One file per decision that is expensive to reverse. Numbered in the order they
were **made**, not by importance.

## Why this folder exists

`abstract/10-how-this-went-wrong.md` is a postmortem of a theme whose stack was
never actually chosen. Tailwind, Alpine, a component library and a build
pipeline all arrived one commit at a time, each defensible on its own, and the
result was a system nobody had decided on and nobody could argue with — because
there was no argument on record to reopen.

A bullet in a doc is not a decision record. It says what, never why, and the
*why* is the only part that cannot be reconstructed from the code later.

> **The test for whether something belongs here:** if reversing it would take
> more than a day, or if someone six months from now would reasonably ask "why
> is it like this?", write the file.

## The format

Five headings, deliberately few. Copy an existing file.

```markdown
# NNNN · Title

**Status:** Proposed | Accepted | Superseded by NNNN | Open
**Date:** YYYY-MM-DD

## Context      — what is true that forces a choice. Facts, not preferences.
## Options      — what was genuinely considered, each with its real cost.
## Decision     — what was chosen.
## Consequences — what this now commits us to, INCLUDING the bad parts.
## Revisit if   — the observation that should reopen this.
```

**"Consequences" is the heading people skip and the one that pays.** A decision
recorded without its downside reads as an endorsement, and the next person
inherits it without knowing what was traded away.

**"Revisit if" is what stops a record becoming dogma.** A decision with a stated
trigger can be reopened by evidence instead of by argument.

## Rules

- **Append, never rewrite.** A decision that turns out wrong gets a *new* file
  and the old one's status becomes `Superseded by NNNN`. Editing history to
  look correct destroys the only thing this folder is for.
- **Status `Open` is legitimate.** An identified decision that has not been made
  is worth recording — it stops it being made by accident, which is precisely
  how the last stack happened.
- **Link from the code.** A comment saying `see abstract/decisions/0002` at the
  top of a stylesheet is worth more than the record itself.

## Index

| # | Decision | Status |
| --- | --- | --- |
| [0001](0001-reset-to-a-starter.md) | Reset the theme to a stack-free starter | Accepted |
| [0002](0002-css-strategy.md) | How the theme gets its CSS | **Open** |
| [0003](0003-routes-yaml-minimal.md) | `routes.yaml` names only servable templates | Accepted |
