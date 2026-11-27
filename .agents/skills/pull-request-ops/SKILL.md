---
name: pull-request-ops
description: The PR procedure and the PR-comment ops commands — the consolidated /deploy /logs /console family table with its conventions, run from PR comments. Use when creating a PR, when a PR needs an environment action, or when running ops from a comment. The norms (PR lifecycle, branch lifecycle, modes, cowboy) live in CONVENTIONS.md and MODES.md — this skill is the agent-side procedure.
---

# Pull-request ops — the procedure and the ops commands

The norms live in the docs: the PR lifecycle and merge-readiness in
[CONVENTIONS.md](../../../docs/CONVENTIONS.md) (*PR lifecycle*), the
branch model (*Branch lifecycle* — feature branches `vibe/<slug>`,
no per-user integration branches) and the working modes including
**cowboy** in [MODES.md](../../../docs/MODES.md) — read those once;
this skill is how the agent drives them.

## Creating a PR (the procedure)

1. **Branch**: `vibe/<short-slug>` from the target base (CONVENTIONS
   *Branch lifecycle*). One branch per coherent subject.
2. **Draft early**: the PR is the workspace — the checks run from
   the first push, the ops commands below only answer from PR/issue
   comments, and the review starts before the code is "done".
3. **Merge-readiness** (the checklist, per CONVENTIONS *PR lifecycle*):
   CI green everywhere, the issue's acceptance criteria met, the docs
   updated in the same change, the pydoc fresh (`make docs`).
4. **Ready → CODEOWNERS review**: `scope/core` maintainer-validated,
   `scope/mod` / `scope/game` owner-validated; split when the mix is
   not clean. **The merge is automated** — an agent never merges.
5. Branch cleanup after merge: never delete a branch whose code is
   not fully on `main` (`git cherry origin/main <branch>` — every
   line `-`, or keep it).

Title and body discipline: write the body to a file
(`--body-file`, quoted heredoc, unique delimiter) — never inline
double quotes in `--title` (backticks and `$(...)` run as commands).
End the description with `Closes <issue>` only when the PR truly
resolves it.

## Cowboy — read MODES.md, keep one line in mind

The full rules are MODES.md (*cowboy*): the agent never assumes
cowboy, never inherits it, and an explicit activation covers exactly
**one operation** — the next one — then ends. Never force-push
`main`. If in doubt: it is not cowboy.

## The ops commands — the consolidated table

The `Ops commands` workflow (botforge-services) watches PR/issue
comments; each command resolves the requestor's roster alias (never
a @login mention — no pings), acks with a comment carrying the run
links, and executes on the target environment's own runner
(botforge-infra owns the envs; each command dispatches there —
single-writer like everything). The per-workflow details are in
[WORKFLOWS.md](../../../docs/WORKFLOWS.md).

| Command | What it does |
|---------|-------------|
| `/deploy <env>` | Deploy the PR's branch to an env (a personal env is the default target for its owner) |
| `/logs <env> [--service <svc>]` | Read the env's logs (the service filter takes the listed names) |
| `/status <env>` | The env's stack status |
| `/start`, `/stop`, `/restart <env>` | Stack lifecycle |
| `/seed <env>` | Run the env's seed job |
| `/console <env> <action> <guild\|all> [--confirm NUKE]` | The console ops — `clean-managed`, `nuke` (needs `--confirm NUKE`), `reset-data`, `install --games=… --mods=…` — **never on prod** |
| `/rollback <env>` | Re-pin and redeploy the previous state |
| `/dump-db`, `/reset-env`, `/clean-env`, `/clear-db <env>` | The destructive family — capability-checked, confirmed |

Conventions: one command per comment; the ack carries the dispatched
run's links; the result lands as a follow-up on the same thread. A
failed command: read the ack's run link, then the `diagnose-deploy`
skill takes over.
