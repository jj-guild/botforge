---
name: release-flow
description: Cut a release of the Kingdoms bot (tag vX.Y.Z, GitHub release, deploy to prod) when the game designer has validated the features in Discord and asks for it. Use when the human says to tag, release, or ship to production.
---

# Release flow

Releasing is a human-requested, agent-executed pipeline: the agent tags
`vX.Y.Z` on `main` (annotated, notes from `scripts/release_notes.sh`), and
the Docker workflow publishes the image, creates the GitHub release and
pins it on `deploy/test`; the promotion to prod pins it on `deploy/prod`.
Prod-like environments deploy released images only — never a PR image.

## The session cannot trigger workflows (developer-mandated)

**An agent session can never launch a GitHub Actions workflow**
(`workflow_dispatch` and `repository_dispatch` return 403 for the session
token — this is the trust design, not a permission bug). The **Git push
is the official path** for everything a session must trigger:

- **tag release** → push the tag: the Docker workflow runs on the tag
  push and pins the image on `deploy/test`;
- **promote to prod** → push the pin commit directly on the
  `deploy/prod` state branch (see *Promotion* below) — the push triggers
  the `Deploy environment` workflow, which waits for the required
  reviewers' approval (human click);
- **deploy a PR to an env** → the `/deploy` PR comment (personal env by default, `test` explicitly; the comment event,
  not a dispatch, triggers it).

Never report "I cannot deploy because I cannot trigger the workflow":
use the Git path.

## Preconditions

- The game designer has **validated the features in Discord** (every
  feature is validated before a release is tagged — CONVENTIONS).
- All checks are green on `main`; the roadmap is synced.
- The release notes are drafted (the workflow creates the GitHub release
  page from them).

## Procedure

1. **Draft the release notes** (`scripts/release_notes.sh` on
   kingdoms-services assembles the change log since the last tag).
2. **Tag and push** from the kingdoms-services clone:
   ```bash
   make release VERSION=vX.Y.Z
   ```
   The Makefile target runs the pre-flight checks (clean tree, on main,
   up to date, notes present) before anything is pushed.
3. **The workflows do the rest**: build and push
   `ghcr.io/merlin-pinpin-org/kingdoms-services:vX.Y.Z` (plus `sha-<sha>`
   and `main` tags), create the GitHub release, pin the released image on
   `deploy/test` — the pin push triggers the test deploy.
4. **Promote to prod (Git path — the official way for sessions)**: the
   human validates the release in Discord on test, then the session
   updates `envs/prod/state/kingdoms-bot.yml` on the `deploy/prod` state
   branch (merge `origin/main` in first, mirroring the Pin state
   workflow: image, version_label, deploy_url, deploy_ref,
   deploy_tree_url, deploy_ts, deployed_by, deployed_at), commits with
   `deploy(prod): pin vX.Y.Z`, and pushes the branch. The push triggers
   the prod `Deploy environment` run, which **waits for the required
   reviewers' approval** — link the run to the human, who clicks
   *Approve and deploy*.
5. **Watch the prod deploy** with `make watch-deploy` (kingdoms-services)
   — polling the status, never a fixed sleep
   ([github-polling](../github-polling/SKILL.md)) — or the
   kingdoms-infra `make doctor` if anything stays pending (see
   the [diagnose-deploy](../diagnose-deploy/SKILL.md) skill).
5. **Post-release**: the game designer validates the release in Discord;
   `/status` shows the release link. Keep the roadmap and dependency
   artifacts in sync (the closed issues change the graph).

## Rules

- The agent never tags on its own initiative — a release is explicitly
  requested by the human.
- Versioning: semver-ish `vX.Y.Z`; breaking rule changes bump the major,
  new features the minor, fixes the patch.
- Never release with a red check or an unsynced roadmap; the Makefile
  pre-flight fails closed.
