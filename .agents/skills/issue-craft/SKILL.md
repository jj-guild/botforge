---
name: issue-craft
description: How to write issues that pass validation and stay readable — the writing procedure, what goes in each section, the validator's behavior, and the maintenance discipline. Use BEFORE creating any issue, and whenever an issue is edited or flagged invalid. The normative rules (templates mandatory, required sections, labels, Lot = milestone) live in CONVENTIONS.md §Issues — this skill is the agent-side craft.
---

# Issue craft — the writing procedure

The norms live in [CONVENTIONS.md §Issues](../../../docs/CONVENTIONS.md):
templates are mandatory, the required sections per repo, the label
rules, "Lot N" IS the milestone. Read that section once; this skill
is how you apply it.

## Creating — always from the template

```bash
gh issue create -R <repo> --template <Feature|Bug|Sub-task|Task>   # services, infra
gh issue create -R jj-guild/botforge --template <documentation|decision-adr|maintenance>
```

Blank issues are disabled. The **Validate issue** workflow checks the
required `##` headings **literally** (the whole heading, lowercased —
`## Context — the incident` does NOT count as `## Context`), labels a
non-compliant issue `invalid` with a comment naming the missing
sections, and **removes the label automatically once the sections are
fixed** — it re-validates on every edit. Consequences:

- An `invalid` issue never enters the work order — fix it, don't leave it.
- Fix in place, never delete and recreate: the number is referenced
  everywhere.
- Near-miss headings are the common failure — write the exact
  section, put the nuance in the body.

## Writing each section (the craft)

- **Objective** — what done looks like. One paragraph, present tense,
  no history, no justification: the justification is Context.
- **Context** — why now: what exists, what triggered it, what the
  surrounding decisions are. Facts and links, no design.
- **Specifications** — the how, normative and testable. A session
  reads this as the contract: anything vague here becomes a drift.
  One bullet per rule; say the rule, not the aspiration.
- **Acceptance criteria** — the checklist a reviewer runs. Concrete
  and verifiable; name the unit tests where they apply.
- **Dependencies** — task-list checkboxes pointing at the blocking
  issues, fully qualified across repos (`jj-guild/botforge#123`).
  "Depends on" = cannot start before; soft relations go in
  `## Related`. No blockers? Say "None — <why it can start now>",
  not an empty section.

## Titles

The conventional prefix (`feat(...)`, `fix(...)`, `docs(...)`,
`refactor(...)`) drives the auto-triage labels — write it. The title
carries the outcome ("the X does Y"), not the task ("add a field to
X"). **Never encode the lot in the title** — "lot X" is the milestone
(see CONVENTIONS.md *"Lot N" IS the milestone*).

## Maintenance

- An issue is a living artifact: when the scope shifts, edit the
  Specifications; when a dependency closes, tick the checkbox; when
  the work lands, close with the PR that resolved it.
- Link, don't repeat: a cross-cutting rule belongs in its own issue;
  others reference it in `## Dependencies` or `## Related`.
