---
name: diagnose-deploy
description: Diagnose a stuck or pending deployment on botforge-infra (test or prod) before suspecting the hosting or runner. Use when a Deploy environment run stays pending/queued for a long time, when a deployment never finishes, or when the developer reports a stuck deploy.
---

# Diagnose a stuck deploy

**The committed status check** — `.agents/skills/diagnose-deploy/scripts/deploy_status.sh
<env>` prints the latest pin on `deploy/<env>`, the latest deploy run
(id/status/conclusion) and its per-job verdicts in one call; exit 0 when the
run succeeded. A session never re-types the `gh api`/`gh run list`/
`gh run view` sequence — it runs the script.

A deployment that never finishes is almost never the runner's fault. Run
the diagnosis tooling **before** suspecting the hosting: in the 2026-09-24 prod
incident, the runner was healthy and idle the whole time while every deploy
stayed pending for hours with no notification.

**Mechanism:** `botforge-infra` ships `scripts/diagnose_deploy.sh <env>`
(+ `--json` for agent sessions) wrapped in Makefile targets
(`make doctor`, `make diagnose-deploy-<env>`). It walks the blocking causes
in order and prints the exact fix with links.

## The trap (memorize this)

A run left `waiting` for an environment approval **acquires the
`deploy-<env>` concurrency group immediately**. With
`cancel-in-progress: false`, it holds the group forever — every newer run
stays `pending` with **no deployment status, no notification, and the
runner is never asked**. The zombie may even run an older or deleted
workflow version (its labels and file were baked at creation), so fixing
the workflow does not unblock it. Only cancelling the zombie does.

## First reflex on a failed deployment: read the logs

Comment `/logs [env] [--service S] [--since 30m] [--from <iso>] [--to
<iso>] [--tail N]` on the PR (or the bug issue): the `ops-commands`
workflow (botforge-services) gates it against the roster authority
matrix (capability `env-logs` — ops, or dev on test), dispatches the
`env-logs` workflow on botforge-infra, and the environment's own runner
dumps the filtered `docker compose logs` back into the thread (full dump
as a private artifact). Use it **before** any hypothesis: the bot's
own traceback names the failing service more often than any inference.
Filters are docker-native: `--since 30m`, `--from`/`--to` ISO8601
windows, `--service botforge-bot` to isolate one process.

## Procedure

```bash
# from the botforge-infra clone
make diagnose-deploy-test
make diagnose-deploy-prod
make doctor          # both envs + script checks
```

Read the output top-down:

1. **Stale in-flight runs** (waiting/pending/queued) on the same state
   branch → they hold the concurrency group: cancel them from the run
   page (human click; agent sessions cannot mutate runs).
2. **Pending environment approval** on the newest run → the required
   reviewers must click *Approve and deploy*; GitHub only notifies
   through the review banner, not the usual run events.
3. **Broken `runs-on`** (one comma-joined label instead of a 3-element
   array — the pre-`fromJSON` bug) → no runner will ever match: cancel.
4. **Everything green on GitHub** → then, and only then, check the
   runner on the hosting (HOSTING-SETUP troubleshooting).

Agent sessions exit early: `--json` returns
`{environment, newest_run, stale_runs, approval_pending_run, deploy_jobs,
blocking}` — `blocking: true` means a cause above applies; link every
stale run URL to the human, who cancels/approves by click.

## Conventions kept

- Diagnose before blaming the runner; link every run mentioned in a
  report (CONVENTIONS: reports carry GitHub links).
- The script is read-only: it never cancels or approves anything —
  cancelling and approving are human clicks.
- Queued runs of **deleted workflows** never start and hold no group;
  report them as advisory cleanup only.
