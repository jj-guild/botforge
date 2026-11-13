---
name: generated-artifacts
description: The generated artifacts (ROADMAP.md, DEPENDENCIES.md, pydoc) — the sync-generated workflow is the single writer; sessions only detect drift and preview. Use when the roadmap or dependency graph looks stale, when sync_roadmap.py --check reports drift, or to preview what the workflow will change.
---

# Generated artifacts — single writer, drift detection, preview

`generated/ROADMAP.md`, `generated/DEPENDENCIES.md` and
`generated/pydoc/` are **generated artifacts**: the `sync-generated`
workflow (botforge repo) is their **single writer**. It regenerates and
publishes them on the `sync/generated-artifacts` branch on every merge
to `main`, daily at 06:00 UTC, or on demand. **Agents and humans never
edit, regenerate or commit them by hand** — they are not on `main`
anymore; the sync branch is workflow-owned.

## What a session does

1. **Detect drift** — from the botforge repo root:
   ```bash
   python3 .github/workflows/scripts/sync_roadmap.py --check
   ```

   `--check` reports what would change without writing anything. The
   session-check target runs it too.

2. **Preview the dependency graph** (optional, informational only):
   ```bash
   python3 .github/workflows/scripts/sync_dependencies.py --dry-run
   ```
   It fails loudly on missing `size/*`/`priority/*` labels, unknown or
   still-open checked dependencies, cycles, and unreadable repositories
   — then reports what it would write. The output is **never committed**.

3. **If drift is reported**, trigger the single writer:
   ```bash
   gh workflow run sync-generated.yml --repo jj-guild/botforge
   ```
   **A session token gets 403 on `workflow_dispatch`** (the trust
   design — see the
   [release-flow](../release-flow/SKILL.md) skill): when the dispatch
   is refused, do not report a bug — the drift is caught by the next
   push on `main` (every merge triggers the sync) or the daily 06:00
   UTC schedule; a maintainer may trigger the on-demand run from the
   GitHub web UI if the refresh cannot wait.
   The workflow restores the previous state from the sync branch,
   regenerates the three artifacts, and pushes the result to
   `sync/generated-artifacts` — no PR, no review, no human click.

4. **If a script fails on content** (unreadable repository, unknown
   reference, an open issue missing from the roadmap, Out-of-Scope
   drift), that is a real content problem: fix the underlying cause
   (usually the roadmap source data or an issue label) — the workflow
   alone cannot fix a broken reference. Report the failure to the
   human if it is not something the session can fix.

## Reference — how the statuses and labels are derived

**Off-roadmap labels** (`OFF_ROADMAP_LABELS` in `sync_dependencies.py`:
`arch-discussion`, `poc`): an issue carrying one of them is a parallel
track — committee discussion, proof of concept, experimental chantier —
and is **excluded entirely** from both generated files: it never appears
in a lot, in the "Out of scope / no lot" section, or in the dependency
graph. Dependencies pointing at it still resolve (it stays in the id
space), it is simply never planned. Tag any POC you create with `poc` at
creation; committee-scope issues get `arch-discussion`. Removing the
label re-adds the issue at the next sync.

Roadmap status inference (each issue referenced in the roadmap maps to):

| GitHub state | Roadmap status |
| ------------ | --------------- |
| open + linked PR | `in-review` |
| open + assignee actively working | `in-progress` |
| open + no PR | `todo` |
| open + blocked dependency | `blocked` |
| closed as completed | `done` |
| closed as not planned | `dropped` (row moves to "Out of Scope") |

Statuses that require human judgment (`in-progress`, `blocked`) cannot
be inferred from GitHub state alone — the script preserves them. Never
invent statuses: every row must reflect an actual GitHub issue state.

The generated pages show the current state and the next steps, not the
history (the git log of the `sync/generated-artifacts` branch carries it).
ROADMAP.md is regenerated from scratch on every run: the current lot, its
open issues in work order as a vertical list of `[#id — title](url)`
links (with status, priority, size, PR link), the upcoming lots with
their live description, and the out-of-scope / no-lot issues. Milestone
titles and descriptions are read live from GitHub — a rename or edit is
reflected at the next sync. DEPENDENCIES.md leads with "Next up — wave 0
(no open dependency: actionable now)" before the graph and the later
waves; an open issue depending on an issue closed as not planned is
listed as out of scope instead of entering the waves.

Priority labels (slack = points by which an issue can slip without
delaying the project; set manually, the script only reports drift):

| Label | Slack |
| ----- | ----- |
| `priority/P0` | 0 (critical path) |
| `priority/P1` | ≤ 4 |
| `priority/P2` | ≤ 12 |
| `priority/P3` | > 12 |

Every open issue must have exactly one `size/*` and one `priority/*`
label, and a `## Dependencies` section (even if "Depends on: none").
Cross-repo dependencies use fully qualified references
(`jj-guild/botforge-infra#2`), same-repo ones the short form
(`#4`).

## Rules

- **Never edit, regenerate or commit the generated artifacts.**
- Both scripts read the issues of all three repos through `gh api`
  (public repos, no custom secret) and **fail closed** on an
  unreadable repository — never a partial regeneration.
- The canonical reading links are on the `sync/generated-artifacts`
  branch:
  [generated/ROADMAP.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md)
  and
  [generated/DEPENDENCIES.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/DEPENDENCIES.md).

## See also

- `.github/workflows/sync-generated.yml` — the single writer
- [sync_roadmap.py](../../../.github/workflows/scripts/sync_roadmap.py) —
  the drift detector (`--check`), also the generator the workflow runs
- [sync_dependencies.py](../../../.github/workflows/scripts/sync_dependencies.py) —
  the dependency-graph preview (`--dry-run`)
- [AGENTS.md](../../../AGENTS.md) — the end-of-session check that
  calls this skill
