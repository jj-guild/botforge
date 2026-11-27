---
name: issue-craft
description: How to create and maintain GitHub issues that pass validation — the mandatory templates, the exact required sections per repo, the labels, the Dependencies section, and the Lot-equals-milestone rule. Use BEFORE creating any issue, and whenever an issue is edited, linked, or flagged invalid.
---

# Issue craft — the issues that pass validation and stay readable

Issues are the roadmap's single source of truth: the generator
(`sync_roadmap.py` / `sync_dependencies.py`) reads them, the sessions
pick them up from the generated work order, and a **Validate issue**
workflow enforces the templates at creation and at every edit — a
non-compliant issue gets labeled `invalid` with a comment naming the
missing sections, and the label is removed automatically once fixed.
An `invalid` issue is invisible to the work order: **it never gets
picked up until compliant.**

## The templates are mandatory — create FROM them

Blank issues are disabled in every repo. Always:

```bash
gh issue create -R <repo> --template <Feature|Bug|Sub-task|Task>   # botforge-services, botforge-infra
gh issue create -R jj-guild/botforge --template <documentation|decision-adr|maintenance>
```

## The exact required sections (the validator matches them literally)

| Repo | Required `##` sections |
|------|----------------------|
| `botforge-services`, `botforge-infra` | `## Objective`, `## Context`, `## Specifications`, `## Acceptance criteria`, `## Dependencies` |
| `botforge` | `## Summary`, `## Details` |

- The headings must appear **exactly** (case-insensitive, but no
  suffixes): `## Context — the incident` FAILS validation — the
  validator matches the whole heading. Write `## Context` and put the
  nuance in the body.
- A near-miss section (`## Inventory`, `## Goal`, `## AC`) does not
  count. Retrofit or rename it.

## What goes in each section

- **Objective** — what done looks like, one paragraph, no history.
- **Context** — why now, what exists, what triggered it. Facts.
- **Specifications** — the how, normative and testable. The session
  reads this as the contract; anything vague here becomes a drift.
- **Acceptance criteria** — the checklist a reviewer runs; unit tests
  named where they apply.
- **Dependencies** — task-list checkboxes pointing at the blocking
  issues, fully qualified across repos (`jj-guild/botforge#123`);
  "Depends on" = cannot start before. Soft relations go in
  `## Related`. A repo-requiring issue without blockers says
  "None — <why it can start now>".

## Labels

- **One `scope/*`** — the delegation contract (`scope/core` maintainer,
  `scope/mod` / `scope/game` owner). Mandatory on every open issue.
- **One `size/*`** (XS/S/M/L/XL) — services and infra mandatory.
- **One `priority/P0-P3`** — maintained by the dependency analysis
  script; do not hand-set unless the analysis is wrong (then say so in
  the issue).
- The auto-triage labels `bug`/`enhancement`/`documentation` etc. from
  the title's conventional prefix (`fix(...)`, `feat(...)`,
  `docs(...)`). Write the prefix, the label follows.

## "Lot N" IS the milestone

When the human says "lot 4", "lot suivant", "this is lot 3", they mean
the **GitHub milestone** `Lot N — …`. Assign it:

```bash
gh issue edit <n> -R <repo> --milestone "Lot 4 — Mod SDK & pro docs"
```

Never encode the lot in the title (`[lot 4] …` is wrong and confusing),
never as a label, never in the body's prose as the tracking of record.
In a repo where the lot's milestone does not exist yet (e.g. `botforge`
skills docs for a services lot), create the sibling milestone first:
`Lot N — Title (<repo>)` — the generator displays it in the same lot
row.

## Maintenance

- Keep an issue in sync with reality: when the scope shifts, edit the
  Specifications; when a dependency closes, tick the checkbox.
- If you find a flagged `invalid` issue, fix the sections (the sections
  above) — the workflow re-validates on edit and removes the label.
- Never delete and recreate an issue to fix it: the number is
  referenced everywhere; edit in place.
