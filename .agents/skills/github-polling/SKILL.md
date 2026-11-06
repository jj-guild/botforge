---
name: github-polling
description: Never wait a fixed worst-case duration after a GitHub action (deploy, workflow dispatch, CI check, log fetch). Poll the actual status every 10-30s until a terminal state, then act on the real result. Apply to every GitHub call that has to wait on an asynchronous outcome.
---

# GitHub polling — never a fixed sleep

**The rule:** after triggering anything on GitHub (a `/deploy` comment, a
workflow dispatch, a push that starts CI checks, a run whose logs are
needed), the session **never** parks for a hard-coded "safe" duration
(480s, 8 minutes, "long enough to be sure"). A fixed wait sized to the
worst case wastes the difference on every fast run — and still races the
slow ones. The wait is a **poll loop on the real status**, not a timer.

## Procedure

1. **Identify what to poll** — the run id(s) or check state that
   represents the outcome:
   ```bash
   gh run list --repo merlin-pinpin-org/<repo> --branch <branch> \
     --json databaseId,workflowName,status,conclusion
   ```
2. **Poll every 10–30s until terminal.** Short waits (gate verdicts,
   seconds-scale) lean toward 10s; long pipelines (deploys, full CI)
   15–30s is fine:
   ```bash
   while :; do
     status=$(gh run view <id> --repo <repo> --json status,conclusion \
       --jq '.status + "/" + (.conclusion // "")')
     case "$status" in
       completed/*) break ;;
     esac
     sleep 15
   done
   ```
   `gh run watch <id>` is an acceptable alternative (it polls and
   exits at the terminal state); a bare `sleep 480` is not.
3. **Act on the terminal state**, never on the elapsed time: read the
   conclusion, then the logs (`gh run view <id> --log-failed`) or the
   tracking comment, and report the actual outcome.
4. **Cap the loop, don't remove it**: if a run stays non-terminal far
   beyond its normal duration, that is a diagnosis (see
   [diagnose-deploy](../diagnose-deploy/SKILL.md) — queued forever,
   waiting for a runner), not a reason to switch back to a fixed sleep.

## Scope — every GitHub wait

The rule applies to any call that waits on an asynchronous GitHub
outcome, including:

- deploy pipelines (`Deploy PR (comment)` → `Pin state` →
  `Deploy environment` — poll each run, don't sleep between them);
- CI checks after a push (see
  [ci-monitoring](../ci-monitoring/SKILL.md));
- workflow dispatches (roadmap sync, dependency regeneration, tag
  releases);
- fetching logs of a run that is still writing them;
- automerge: poll the PR state (`gh pr view <n> --json state,
  mergeStateStatus`) instead of assuming the merge landed.

**Never** answer the human with a result inferred from elapsed time
("8 minutes passed, it must be done") — only a terminal status read
from GitHub counts.
