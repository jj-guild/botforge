---
name: roadmap-unroll
description: What to do when the human says "roadmap", "unroll the roadmap", "what's next?", "continue", "go". Determines the current lot (first unfinished Lot milestone), prints the ordered work table for that lot, and on "continue" starts the top issue in pro mode. Use whenever the human asks where the project stands or what to do next.
---

# Roadmap unrolling — the agent-side procedure

The published artifacts (`generated/ROADMAP.md`, `generated/DEPENDENCIES.md`
on the `sync/generated-artifacts` branch) are written **only** by the
`sync-generated` workflow — the single writer. Agents never edit or
regenerate them; the generation scripts
(`.github/workflows/scripts/sync_roadmap.py`, `sync_dependencies.py`) belong
to that workflow. This skill is the agent side: read-only, via
[scripts/roadmap_next.py](../../../scripts/roadmap_next.py), which reuses
those scripts' parsers and CPM so the GitHub issues stay the single source
of truth.

## When the human says "roadmap" / "unroll the roadmap" / "what's next?"

1. From the kingdoms repo root, run:
   ```bash
   python3 scripts/roadmap_next.py
   ```
   It determines the **current lot** — the first unfinished `Lot N`
   milestone, i.e. the lowest N with open issues — and prints that lot's
   issues in work order.
2. Report the table to the human. The first cell carries the links on two
   lines (`issue: #322` / `PR: #306`, `PR: —` when none); then the priority
   label with its plain-language gloss, a short summary, the details
   (critical-path flag, dependency wave, number of dependent issues,
   size/complexity in points, slack), and the lot.
3. Work order rule: **dependency wave first** (an issue whose dependencies
   are still open cannot start), then **priority label** (P0 first), then
   **slack** (critical path first), then issue number.
4. Add a one-line status: current lot, done / in-review / todo counts, and
   the open PRs on the lot.

## When the human says "continue" / "go"

Take the **top todo issue of the current lot's table** (skip the ones
already in-review) and work it in pro mode: one branch `vibe/<slug>` from
`main` per subject, implement with tests landing in the same change,
`make lint` / `make typecheck` / `make test` green before pushing, push,
open the PR (draft), report the PR URL, then watch CI. If the work changes
what an issue depends on, update its `## Dependencies` checkboxes — the
graph regenerates from the issues, never by hand.

## Rules

- Never edit `generated/ROADMAP.md` / `generated/DEPENDENCIES.md` by hand.
  Drift is detected with
  `python3 .github/workflows/scripts/sync_roadmap.py --check` and resolved
  by the `sync-generated` workflow (post-merge push on `main`, daily
  06:00 UTC run, or an on-demand run by a maintainer) — not by the agent.
- Changing **what the generated files contain** is a PR on
  `.github/workflows/scripts/sync_*.py` (workflow-owned), never on the
  artifacts themselves.
- A new feature idea from the human routes through
  [shape-game-designer-idea](../shape-game-designer-idea/SKILL.md) first;
  unrolling only reads the plan.

## See also

- [workflow-router](../workflow-router/SKILL.md) — the route table entry
  for roadmap requests
- [generated-artifacts](../generated-artifacts/SKILL.md) — the artifacts,
  the single writer, drift detection
- [scripts/roadmap_next.py](../../../scripts/roadmap_next.py) — the helper
  this skill runs (`--lots` for the per-lot summary, `--lot N` for another
  lot)
