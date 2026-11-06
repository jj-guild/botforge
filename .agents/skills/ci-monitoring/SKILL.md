---
name: ci-monitoring
description: Monitor GitHub Actions checks of a PR after a push, read the failing logs, find the root cause, reproduce locally when feasible, and push focused fixes until green. Use after pushing any change, when a check turns red, or when the human asks to monitor CI.
---

# CI monitoring

After pushing a change, the agent monitors the CI of the branch/PR and
fixes failures until green — a PR left red is an incomplete session.
**Checks are verified on the head commit, completed** (the 2026-09-24
SC2046 incident: a merge landed between the push of a doc commit and its
lint conclusion).

## Procedure

1. **List the runs** of the branch:
   ```bash
   gh run list --repo merlin-pinpin-org/<repo> --branch <branch> \
     --json databaseId,workflowName,status,conclusion
   ```
2. **Wait for completion by polling the status every 10-30s until the
   terminal state** — never a fixed sleep sized to the worst case (see
   [github-polling](../github-polling/SKILL.md)) — then check every
   job of every run — including the `skipping` ones (a job skipping where
   it should have run is a workflow bug: check its `if:` condition).
3. **On failure — read the evidence before guessing**:
   ```bash
   gh run view <id> --repo <repo> --log-failed   # the failing steps only
   gh run view <id> --repo <repo> --json jobs    # which job failed
   ```
   Find the **root cause in the logs** (the exact error line, the exact
   command), never a guessed symptom. Diagnose before blaming the
   infrastructure (CONVENTIONS).
4. **Reproduce locally when feasible**: workflow lint (actionlint —
   install in /tmp, the same binary the CI installs), shellcheck, ruff,
   mypy, pytest, docs validation — all run in the sandbox. Compose boots
   and deploy runs do not: they are reproduced by the CI jobs themselves.
5. **Push a focused fix** to the same branch (never a workaround), then
   re-monitor. One root cause = one commit when possible.
6. **Report** the failure and the fix with run URLs (reports carry
   GitHub links).

## Known failure classes and their reflexes

- **actionlint/shellcheck findings** (SC20xx): quote expansions, replace
  `for x in $(ls ...)` with globs, `find` instead of `ls -t`. Reproduce
  locally: `actionlint -color` in the repo root.
- **Startup failure** (`queued` forever, `waiting for a runner`): a
  `runs-on` label no runner carries — see the
  [diagnose-deploy](../diagnose-deploy/SKILL.md) skill.
- **Secret-less local repro of `gh` commands**: the repos are public;
  `gh api`/`gh run`/`gh pr` work from the sandbox with the session token.
- **Required checks**: a required status check never uses a `paths:`
  filter — if a required check is missing on a PR, verify the workflow's
  `on:` triggers, not the ruleset first.

## Conventions kept

- Never ask for a merge while a check is pending or only the previous
  commit is green.
- Never cancel a run from a session (run mutation is a human click);
  report the URL instead.
- Link every run mentioned in a report.
