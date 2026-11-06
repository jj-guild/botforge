---
name: update-roadmap
description: Check generated/ROADMAP.md for drift against the actual GitHub issue states across the three Kingdoms repos, and trigger the sync workflow when needed. The roadmap is generated — agents never write it.
---

# Update roadmap

`generated/ROADMAP.md` is a **generated artifact**: the
`sync-generated` workflow (kingdoms repo) is its single writer. It
regenerates and publishes it on the `sync/generated-artifacts` branch
on every merge to main, daily at 06:00 UTC, or on demand. **Agents and
humans never edit or regenerate it by hand.**

## What a session does

1. **Detect drift** — from the kingdoms repo root:
   ```bash
   python3 .github/workflows/scripts/sync_roadmap.py --check
   ```
   `--check` reports what would change without writing anything. The
   session-check target runs it too.

2. **If drift is reported**, trigger the single writer:
   ```bash
   gh workflow run sync-generated.yml --repo merlin-pinpin-org/kingdoms
   ```
   **A session token gets 403 on `workflow_dispatch`** (the trust
   design — see the
   [release-flow](../release-flow/SKILL.md) skill): when the dispatch
   is refused, do not report a bug — the drift is caught by the next
   push on `main` (every merge triggers the sync) or the daily 06:00
   UTC schedule; a maintainer may trigger the on-demand run from the
   GitHub web UI if the refresh cannot wait.
   The workflow restores the previous state from the sync branch,
   regenerates `generated/ROADMAP.md` + `generated/DEPENDENCIES.md` +
   `generated/pydoc/`, and pushes the result to
   `sync/generated-artifacts` — no PR, no review, no human click.

3. **If the script fails on content** (unreadable repository, unknown
   reference, an open issue missing from the roadmap, Out-of-Scope
   drift), that is a real content problem: fix the underlying cause
   (usually the roadmap source data or an issue label) — the workflow
   alone cannot fix a broken reference. Report the failure to the
   human if it is not something the session can fix.

## Status inference

The script maps each issue referenced in the roadmap to a status:

| GitHub state | Roadmap status |
| ------------ | --------------- |
| open + linked PR | `in-review` |
| open + assignee actively working | `in-progress` |
| open + no PR | `todo` |
| open + blocked dependency | `blocked` |
| closed as completed | `done` |
| closed as not planned | `dropped` (row moves to "Out of Scope") |

Statuses that require human judgment (`in-progress`, `blocked`) cannot
be inferred from GitHub state alone — the script preserves them.

## Rules

- **Never edit, regenerate or commit `generated/ROADMAP.md`,
  `generated/DEPENDENCIES.md` or `generated/pydoc/`** — they are not
  on main anymore; the sync branch is workflow-owned.
- Never invent statuses: every row must reflect an actual GitHub issue
  state.
- The canonical reading links are on the `sync/generated-artifacts`
  branch:
  [generated/ROADMAP.md](https://github.com/merlin-pinpin-org/kingdoms/blob/sync/generated-artifacts/generated/ROADMAP.md)
  and
  [generated/DEPENDENCIES.md](https://github.com/merlin-pinpin-org/kingdoms/blob/sync/generated-artifacts/generated/DEPENDENCIES.md).

## See also

- `.github/workflows/sync-generated.yml` — the single writer
- [sync_roadmap.py](../../../.github/workflows/scripts/sync_roadmap.py) — the drift
  detector (`--check`), also the generator the workflow runs
- [AGENTS.md](../../../AGENTS.md) — the end-of-session check that
  calls this skill
