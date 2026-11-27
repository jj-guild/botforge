---
name: pull-request-ops
description: The PR lifecycle and the PR-comment ops commands — branch, draft, merge-readiness, CODEOWNERS review, cowboy mode (one explicit operation, never assumed), and the /deploy /logs /console family run from PR comments. Use when creating a PR, when a PR needs an environment action, or whenever cowboy mode is mentioned.
---

# Pull-request ops — the PR lifecycle and the ops you run from a comment

## The PR lifecycle (the default path)

1. **Branch**: `vibe/<short-slug>` from the target base (a mod rides
   its integration branch, e.g. `vibe/mod-kingdom`; the platform rides
   `main`).
2. **Draft PR early** — the PR is the workspace: the checks run from
   the first push, the ops commands below only work from a PR or an
   issue comment, and the review starts before the code is "done".
3. **Merge-readiness** (per CONVENTIONS.md §PR lifecycle): CI green
   everywhere, the issue's acceptance criteria met, the docs updated
   in the same change, the pydoc fresh (`make docs` — the check fails
   on stale committed copy).
4. **Ready for review** → CODEOWNERS decides who reviews: `scope/core`
   is maintainer-validated, `scope/mod` / `scope/game` owner-validated.
   A PR crossing scopes splits when the mix is not clean.
5. **The merge is automated** — agents never merge a PR themselves
   (see MODES.md). A maintainer merges, or the automation does.

Title and body discipline: write the body to a file
(`--body-file`, quoted heredoc, unique delimiter) — never inline
double quotes in `--title` (backticks and `$(...)` run as commands).
End the description with `Closes <issue>` only when the PR truly
resolves it.

## The ops commands — run from PR/issue comments

The `Ops commands` workflow watches the comments; every command
resolves the requestor's roster alias (never a @login mention — no
pings), acks with a comment carrying the run links, and executes on
the target environment's own runner (botforge-infra owns the envs;
each command dispatches there — single-writer like everything).

| Command | What it does |
|---------|-------------|
| `/deploy <env>` | Deploy the PR's branch (or the pinned state) to an env |
| `/logs <env> [--service <svc>]` | Read the env's logs (the service filter takes the listed names) |
| `/status <env>` | The env's stack status |
| `/start`, `/stop`, `/restart <env>` | Stack lifecycle |
| `/seed <env>` | Run the env's seed |
| `/console <env> <action> <guild\|all> [--confirm NUKE]` | The console ops — `clean-managed`, `nuke` (needs `--confirm NUKE`), `reset-data`, `install --games=… --mods=…` — **never on prod** |
| `/rollback <env>` | Re-pin and redeploy the previous state |
| `/dump-db`, `/reset-env`, `/clean-env`, `/clear-db <env>` | The destructive family — capability-checked, confirmed |

Conventions: one command per comment, the ack comment carries the
links to the dispatched run, and the result lands as a follow-up
comment on the same thread. If a command fails, read the ack's run
link — the diagnose-deploy skill takes over.

## Cowboy mode — the explicit exception, never the default

From MODES.md, binding for every agent session:

- The agent **never assumes** cowboy mode, never "inherits" it from
  the previous operation, and never proposes it as a shortcut for
  convenience.
- An explicit "cowboy" activation covers **exactly one operation** —
  the next one — and ends there. It is never a session-long state.
- Direct-push to `main` (the cowboy shortcut) happens only when the
  human said "cowboy" for this operation after the situation was
  stated. **Never force-push `main`.**
- When cowboy was used, the trail stays honest: the push message and
  the issue/PR record say what was cowboy'd and why.

## Branch hygiene

- Never delete a PR's branch while the PR is open; delete after merge
  (the automation offers it).
- A branch whose PR was closed unmerged is dead only if its content is
  merged or abandoned by an explicit decision — when in doubt, ask.
- The reference branches (`vibe/<user>/main` integrations) are never
  merged, never restacked, never closed without the owner's word.
