# ADR-0018: Per-environment state branches (GitOps deploy state)

**Status:** Accepted
**Date:** 2026-09-23
**Reference:** botforge#80, botforge-infra#40

## Context

ADR-0007 established GitOps deployment: manifests live in Git on `main`,
deploys run on the self-hosted hosting runners, and audit comes from Git history.
Two gaps surfaced while validating the `/status` deploy-link feature:

1. **Floating image tag.** `deploy/test/docker-compose.yml` referenced
   `ghcr.io/.../botforge-services:main` with `pull_policy: missing`: a
   config-change deploy can restart the bot on a stale local image while the
   freshly merged image is still building. The deploy "succeeds" against
   outdated code (evidence: botforge-infra run 35804044373).
2. **No deployment state in Git.** Nothing in the repository records which
   image runs on which environment, since when, deployed by whom. The only
   trace is the transient Actions run log.

The earlier candidate — one commit per deployment on `main` — is incompatible
with the `main` ruleset (code-owner review + required checks, no bypass for
the deploy pipeline): one PR per deploy is review noise, and a bypassing bot
breaks the one-human-click governance.

## Decision

**Each environment owns a state branch, `deploy/<env>`, carrying the desired
state of that environment as a single state file per deployed service.**

- The state file (`deploy/state/<env>/<service>.yml`) pins the exact image
  reference (never a floating tag), the version label and artifact URL
  shown by `/status` (`BOTFORGE_DEPLOY_LABEL` + `BOTFORGE_DEPLOY_URL`), who
  requested the deploy, and when. PR deploys are tagged
  `pr-<id>-<timestamp>-<sha7>`; main config-change deploys pin the latest
  `sha-<sha>` image; prod deploys pin the released `vX.Y.Z` image.
- **Deployment trigger:** a push to `deploy/<env>` deploys that environment.
  The deploy workflow reads the state file at the pushed commit; the image
  never comes from a workflow input, so it cannot be spoofed or drifted.
- **Writers:** only the pipelines commit to state branches — never a human
  and never the deploy workflow itself (which would re-trigger itself):
  - `deploy/test`: the `jj-guild-deployer` GitHub App, from the
    `/deploy [env]` PR comment (PR image + PR URL + commenter) or from a
    merged main-branch config change (pinned latest `sha-<sha>` image).
  - `deploy/prod`: the `Promote release` workflow of `botforge-services`
    (human-triggered `workflow_dispatch` with the released tag, after the
    release was validated on the test environment — the tag push pins the
    released image on `deploy/test` first); the pin push is allowed by the
    jj-guild-deployer App bypass on the state-branch ruleset, and the human
    gates are the **workflow trigger** and the **`prod` environment
    approval** in the deploy run — human clicks, consistent with the
    governance model.
- **Protection:** per-branch rulesets (no force-push, no deletion; PR
  required on `deploy/prod`). The `main` ruleset is untouched: state branches
  carry state only, manifests stay on `main` as the source of truth.
- **Rollback:** committing the previous state (the parent state file) and
  pushing it redeploys the previous artifact — Git history is the rollback
  ledger.
- **Extensibility:** a new environment `<name>` needs exactly three
  artifacts, no workflow fork: a `deploy/<name>/docker-compose.yml` on
  `main`, a `deploy/state/<name>/` directory (first state commit), and a
  branch `deploy/<name>` with its ruleset. The deploy workflow is generated
  per environment from one template (matrix/templating, one job per env).

## Consequences

- Every deployment is a Git commit on the environment branch: image, author,
  timestamp, artifact URL — answering "what runs where, since when, by whom"
  from Git alone.
- State branches are cut from `main` once and evolve independently: pipeline
  changes merged on `main` (deploy workflows, manifests, scripts) must be
  fast-forward propagated to every state branch, or the environment keeps
  deploying with the stale pipeline code (see botforge-infra
  docs/ENVIRONMENTS.md § "Keeping the state branches current").
- No floating image tags remain in any manifest.
- `/deploy [env]` keeps its user experience (PR comment) but now writes state
  instead of passing a `bot_image` input; the workflow's `workflow_dispatch`
  image input disappears.
- The runner-side deploy script reads the pinned image from the state file;
  `pull_policy: always` remains as a safety net (a state commit must deploy
  the exact pushed image, even if a same-named tag moved).
- Failed deploys leave the tip pointing at something not running: the state
  commit links its run, and the next state commit supersedes it; the health
  gate keeps the hosting on the last healthy state.
- One commit per deployment on the environment branch — the accepted price
  of a Git-native audit trail.

## Alternatives Considered

1. **Post-deploy journal branch only (model 1).** Accurate but weak: the
   branch is an effect, not a cause; per-env permissions and PR-approval for
   prod deployments are impossible to express.
2. **One PR per deployment on `main`.** Breaks the review budget and either
   adds review noise or requires a bypassing bot — rejected.
3. **Status quo (floating `:main` + run logs).** Already produced a stale-
   image deployment; no audit trail. Rejected.
