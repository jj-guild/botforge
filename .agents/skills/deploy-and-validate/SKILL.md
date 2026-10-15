---
name: deploy-and-validate
description: Deploy a pull request to the test environment and validate it yourself (healthchecks, stack healthy, no crash loop) before marking the PR ready. Use for any PR with something to deploy on kingdoms-services (the /deploy flow), and to decide whether the test environment may be re-aligned to main after a merge.
---

# Deploy to test and validate before ready

The developer-mandated PR lifecycle (see *PR lifecycle* in
[docs/CONVENTIONS.md](../../../docs/CONVENTIONS.md)): a PR is flipped
to **ready** only after it has been **deployed to test and validated by
the agent itself** — then GitHub automerges it once the CODEOWNERS
reviews land (rebase-only, see
[docs/GUIDES/rulesets.md](../../../docs/GUIDES/rulesets.md)). The
human's Discord check is the final acceptance, not a precondition for
ready.

## Preconditions (all required before deploying)

- All CI checks green **on the head commit, completed** (never deploy on a
  pending check).
- The branch is up to date with its base (`gh pr view` shows
  `mergeable: MERGEABLE`; rebase on the base if not).
- Nothing to redeploy (doc-only, workflow-only PRs) → skip the deployment,
  keep the rest of the lifecycle.

## Procedure (kingdoms-services PRs)

1. **Know your target**: your personal env (the default — no
   overwrite risk, it is yours) or the shared `test` env (explicit
   `/deploy test`). For `test`, first read the pinned image on the
   `deploy/test` state branch —
   `git show origin/deploy/test:envs/test/state/kingdoms-bot.yml`;
   if a **different** PR is pinned there and still under validation, do
   not deploy on top of it: wait for its cycle to finish (never
   overwrite another PR's shared-env deployment).
2. **Deploy**: the session comments `/deploy` on the PR **itself**
   (this comment is the agent's action, never the human's — the gate
   checks the human's roster rights, the session acts on their behalf;
   never ask the human to post it)
   (`gh pr comment <n> --repo merlin-pinpin-org/kingdoms-services --body "/deploy"` —
   no argument: the workflow targets your **personal env** from your
   roster alias — **never** the shared `test` env; a bare `/deploy` on a
   personal alias therefore deploys to the personal env (e.g. `merlin`),
   not `test`. When the designer says "déploie", they mean **`/deploy
   test`** unless they name their personal env — always add the explicit
   environment argument).
   Only collaborators with write+ may trigger it; forks are rejected.
3. **Wait and read the gate's answer before doing anything else**:
   poll the PR conversation / runs (`gh run list --workflow deploy.yml`,
   the tracking comment) — polling every 10-30s until a terminal state
   ([github-polling](../github-polling/SKILL.md)), never a fixed
   sleep — for the roster-gate verdict (seconds) and then
   the pipeline result; report the actual outcome to the human only
   once a final status has landed — never answer with "posted, should
   work" while a run is still in progress, and never move on before
   the gate verdict (a deny means the deploy never started).
4. **Follow the pipeline**: the `Deploy PR (comment)` workflow builds the
   image (`pr-<id>-<timestamp>-<sha>`), pushes it to GHCR, then dispatches
   the `Pin state` workflow on kingdoms-infra which pins it on the target's
   `deploy/<env>` state branch; the pin push triggers `Deploy environment`,
   which runs on the env's self-hosted runner.
5. **Validate the deployment yourself** — all of:
   - `Deploy PR (comment)` run: conclusion `success`;
   - `Pin state` + `Deploy environment` runs: `success`;
   - Deploy environment logs end with `deployment to '<env>' applied and
     healthy` — kingdoms-bot, kingdoms-mongo and kingdoms-redis all
     report healthy (the bot healthcheck probes `/healthz`);
   - the pinned image on `deploy/<env>` matches the PR head sha.
   A crash loop, an exited container or a failed healthcheck → the PR
   stays in draft, diagnose (see the
   [diagnose-deploy](../diagnose-deploy/SKILL.md) skill), fix, redeploy.
6. **Mark ready and hand over**: `gh pr ready <n>` + `gh pr merge <n>
   --auto --rebase` (automerge; the rebase method is the only one the
   rulesets allow), then report the PR URL and the deployed image and
   ask the human to test in Discord. This transition is mandatory and
   never waits for a reminder (developer-mandated): a green, deployed,
   self-validated PR left in draft is an agent bug.

## After a merge: re-align the shared test env to main?

Only if the merged PR is the one deployed on `test`. Merging to `main`
never re-pins an environment automatically (state branches are pinned by
`/deploy` comments and by tag releases); re-aligning is a deliberate
action, done by deploying the `main` state or the next release — never on
top of another PR's validation run. A personal env is re-aligned by its
owner whenever they choose (it is their sandbox).

## Infra PRs (kingdoms-infra)

Infra PRs have no `/deploy`: their CI **boots the real stack** from the
branch (compose validation, smoke test, backup/restore round-trip). The
agent validates the CI evidence the same way (all green on head) before
marking ready; the infra changes reach the test environment at the next
re-pin after merge.
