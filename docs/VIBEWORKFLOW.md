# Vibe-coding workflow

This document describes the operating model used to build Kingdoms: the full
interaction loop between the AI agent, GitHub, the VPS, Discord, and the humans
(game designer, developer).

Kingdoms is built by AI agent sessions that have **no access to previous
conversations**. This repo is the source of truth, so the operating model
itself is written down here. Any future session — and any human contributor —
must be able to understand the model from this page alone.

## Modes

Every contributor works in one of three modes — sandbox (vibe coder),
pro (dev/ops) or cowboy (maintainer, explicit single-shot activation
per command — an activation covers only the next operation and
expires immediately, never the whole session). The mode
decides the branch strategy, the review gate and the GitHub powers; it
is documented on its own page: [MODES.md](MODES.md).

## Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| Game designer | Non-developer, idea-rich | Defines features, game rules, environments; validates behavior in Discord |
| Developer | Experienced, maintains the platform | Challenges the design, **reviews and approves the PRs that touch core/platform code** (per CODEOWNERS); never codes |
| Ops | Infrastructure owner | Everything the developer does, plus environment and secret administration in the GitHub web UI and production deployment approvals |
| AI agent (Vibe Code) | Mistral-powered coding agent | Does 100% of the technical work: issues, code, branches, PRs, CI, test deployments, tags/releases on request — core and mod alike, flagging core changes for review. Merges are automated (automerge once reviews land); the session drives draft → ready |

**Humans never check out, write code, or run scripts** — this platform is a
pure vibe-coding test. Every human technical action is a **click in the
GitHub web UI**: approving PRs, approving production deployments, and the
one-time administration (org teams, rulesets, environments, secrets).
There is deliberately no human CLI step anywhere in the model; agents must
never propose one (see `AGENTS.md`).**Human GitHub scope (developer-mandated, exhaustive):** humans accept to
do exactly two recurring things on GitHub — **merge PRs** and **approve
production deployments** — plus the one-time bootstrapping (org teams,
rulesets, environments, secrets, runner install). Everything else is the
agent's job, done through automation. When a session hits a step that
seems to require another manual action, fix the automation instead (see
CONVENTIONS.md, *Human GitHub scope*).

The three roles map to GitHub org teams (created once in the web UI by the
org owner):

| Team | Members | Repo permissions |
|------|---------|-----------------|
| `@merlin-pinpin-org/maintainers` | developer + ops | Write on the 3 repos; code owners (required reviewers on `main` PRs) |
| `@merlin-pinpin-org/ops` | ops | Maintain on `kingdoms-infra` (environments + secrets), Read elsewhere; owns the `/deploy/prod/` CODEOWNERS paths |
| `@merlin-pinpin-org/game-designers` | game designers | Write on `kingdoms` and `kingdoms-services`; each designer **owns and reviews their mod's code** (CODEOWNERS names them per mod), validates on the test Discord; core-touching PRs need a maintainer review per CODEOWNERS. Read on `kingdoms-infra` |

## Artifact map

| Artifact | Location | Owner |
|----------|----------|-------|
| Ideas, rules, environments | `kingdoms` docs (`docs/MODS/`) | Game designer (via agent) |
| Work items | GitHub issues (3 repos) | Agent creates |
| Implementation | Feature branches `vibe/<slug>` → PRs | Agent |
| Approvals & merges | PR review, GitHub rulesets | CODEOWNERS review; GitHub automerges the ready PR (rebase-only — see [GUIDES/rulesets.md](GUIDES/rulesets.md)) |
| Versions | Git tags + GitHub releases | Agent executes on request; permissions enforced by GitHub |
| Deployment | `kingdoms-infra` GitOps (test / prod, self-hosted runner on the VPS) | Agent via CI/CD; ops approves prod |

## End-to-end flow

```mermaid
flowchart TD
    GD["Game Designer"] -->|"Feature idea"| A["AI Agent - Vibe Code"]
    DEV["Developer"] -->|"Approves / challenges"| A
    A -->|"Creates issue"| GH["GitHub Issues - 3 repos"]
    A -->|"Implements"| BR["Feature branch vibe/slug"]
    BR -->|"PR"| PR["Pull Request draft"]
    PR -->|"CI checks"| CI["GitHub Actions"]
    CI -->|"Pass"| READY["Agent marks PR ready"]
    READY -->|"Review"| REV["Developer review"]
    REV -->|"Approve + merge"| MAIN["main branch"]
    A -->|"On request"| TAG["Tag vX.Y.Z"]
    TAG -->|"Release"| REL["GitHub Release"]
    REL -->|"GitOps trigger"| VPS["VPS - Docker Compose"]
    VPS -->|"Bot running"| DISC["Discord"]
    DISC -->|"Game Designer validates"| GD
```

Step by step:

1. The game designer brings a feature idea (or a change to rules or
   environment) to the agent.
2. The agent challenges and shapes the idea toward automatable, simply
   explainable behavior, then creates a self-contained GitHub issue in the
   relevant repo, using that repo's issue templates — blank issues are
   disabled and a "Validate issue" workflow flags non-compliant issues
   `invalid`.
3. The agent implements the issue. For a **personal mod** (sandbox
   mode), the commits stack directly on the user's integration branch
   `vibe/<alias>/main` (CONVENTIONS.md — *Integration branches*) — no
   additional PRs are opened on top of the mod PR. The **mod PR**
   (`vibe/<alias>/main` → `main`) is opened as a draft when the mod
   work starts and stays open for the mod's whole life: every push
   re-runs the required checks on it, which is its purpose — continuous
   validation of the stack. It goes ready only when the owner judges
   the mod complete; the standard path then applies (review by another
   user, test deploy, release). The agent monitors and fixes check
   failures on the mod PR, deploys the integration branch to the
   personal environment, **validates the deployment itself**
   (healthchecks green, stack healthy, no crash loop), and reports;
   while the mod is in progress, the PR stays in draft.
4. **The session never merges; GitHub automerges.** The session flips
   the PR to *ready for review* **only when it has nothing left to do**:
   checks green and completed on the head commit, deployed (the
   requestor's personal env by default, `test` explicitly) and
   verified (when there is something to deploy), self-review done, docs
   updated. Flipping to ready comes with enabling GitHub automerge.
   What requires a review is decided by **CODEOWNERS** — every path has
   a named owner: the mod's designer reviews their mod's PRs (no
   platform review), the maintainer/dev/ops teams review the core,
   platform and infra. Once the owners have approved and the checks are
   green, GitHub merges the ready PR automatically. The session
   commits as the **vibe coder** (the human who ran it, per the
   CONTRIBUTORS.md roster — alias used verbatim; personal emails are
   forbidden in the roster)
   and adds the agent as co-author via
   `Co-authored-by: Mistral AI <noreply@mistral.ai>` (see the *Git
   identity of agent sessions* rule in CONVENTIONS.md).
5. When explicitly requested, the agent tags a version and creates the GitHub
   release — tag and release permissions are enforced by GitHub.
6. PR deployments are **on demand** (`/deploy` PR comment posted by
   the session); the PR image (commit-SHA tagged) is pinned in the
   environment **state branch** `deploy/test` by the kingdoms-deployer
   GitHub App (ephemeral Actions: write token), and the push to
   `deploy/test` triggers the deployment — the deploy reads the pinned
   image from Git, never from a workflow input (ADR-0018). Production
   deployments happen only from a released tag (`vX.Y.Z`), written to
   `deploy/prod` by the release pipeline; its branch ruleset requires a
   pull request, so approving a prod deployment is merging that PR. The bot runs and the game
   designer validates the behavior in Discord.

## Automation mandate (developer-mandated)

**Everything is automation, on both sides of the table.** Humans never
run commands (above), and sessions never leave recurring operations as
one-off shell commands: every operation that will be needed again exists
as a committed Makefile target, script, or GitHub Actions workflow, so
future sessions (which have no conversation memory) rediscover it from
the repos. **Learn it or drop it:** whenever a session improvises a command
or helper script that could be useful again, it commits it — wrapped in a
Makefile target or script, with the session's learnings baked in. The
procedure and placement rules live in the
[Automate or learn](../.agents/skills/automate-or-learn/SKILL.md) skill.

## PR conventions (agent rules, developer-mandated)

The binding rules live once in [CONVENTIONS.md](CONVENTIONS.md) — *PR
lifecycle (merge-readiness)*; this page keeps only the operating-model
view:

- **Ready = nothing left to do** — checks green and completed on the
  head commit, deployed and verified, self-review done, docs updated;
  flipping to ready enables automerge, and the transition never waits
  for a reminder (CONVENTIONS.md, *PR lifecycle* 1).
- **Deploy to test, validate, then ready — in that order** (CONVENTIONS.md,
  *PR lifecycle* 2; the procedure is the
  [deploy-and-validate](../.agents/skills/deploy-and-validate/SKILL.md)
  skill).
- **Never overwrite another PR's test deployment** (CONVENTIONS.md,
  *PR lifecycle* 3).
- **Normal-size PRs on platform work** — one PR = one coherent scope;
  the sandbox-mode mod PR is the one exception (CONVENTIONS.md,
  *PR lifecycle* 4 and *Integration branches*).

## Generated artifacts sync

`generated/ROADMAP.md` and `generated/DEPENDENCIES.md` are generated
artifacts owned by the **`sync-generated` workflow — the single writer**:
it regenerates both and publishes them on the `sync/generated-artifacts`
branch on every push to `main`, daily at 06:00 UTC, and on demand. The
sync skill ([Generated
artifacts](../.agents/skills/generated-artifacts/SKILL.md)) is
**preview-only**: the agent runs the sync script locally
(`.github/workflows/scripts/sync_roadmap.py`,
`.github/workflows/scripts/sync_dependencies.py`) to detect drift and fix
what the script reports (labels, references) — it **never commits the
regenerated artifact**: no PR carries it, no rolling `automation/*` PR,
no direct push to `main`. Generated
technical docs (pydoc) live in `kingdoms-services` and are
freshness-checked there.

- **Fail-closed:** both scripts read the issues of `kingdoms-services` and
  `kingdoms-infra` through `gh api` (all three repositories are public, no
  custom secret); they fail with an explicit error when a repo is
  unreadable, never regenerating from partial data. Every sync script fails
  when its validation fails (unreadable repo, partial data, missing
  labels, stale generated docs) — no best-effort or partial writes.
- **Status mapping:** closed-as-completed → `done`, closed-as-not-planned →
  `dropped` (moved to "Out of Scope"), open with a closing-keyword PR →
  `in-review`, otherwise `todo`. `in-progress` and `blocked` require human
  judgment and are preserved as-is.
- **Linking PRs to issues:** use a closing keyword in the PR description
  (`Closes #N` same-repo, `Closes owner/repo#N` cross-repo) — this populates
  the GitHub "Development" section, drives `in-review` detection, and closes
  the issue on merge.
- **Issue references everywhere** (bodies, comments, `## Dependencies`
  checkboxes): same-repo as `#N`, cross-repo as `owner/repo#N` (e.g.
  `merlin-pinpin-org/kingdoms-infra#78`) — GitHub renders both as clickable
  links with backlinks. A bare `repo#N` (no owner) is plain text on GitHub:
  never write it, and never use the pre-rename owner `merlin-pinpin/...`.

The `Check Docs` required check runs `.github/workflows/scripts/validate_docs.py` on every PR
— documentation validation never depends on a manual command.

## Session loop

An agent session (which starts with no memory of previous conversations):

1. Read `AGENTS.md` in the target repo, then the assigned issue in full —
   issues are self-contained, with skills tables and dependencies.
2. Ask the human what the session is for — a personal mod or platform
   work — and pick the mode accordingly
   ([MODES.md](MODES.md)). For a personal mod (sandbox mode): commit
   and push directly on the user's integration branch
   `vibe/<alias>/main`, and keep its draft **mod PR** to `main` up to
   date — open it on the first push if it does not exist yet, never
   stack extra PRs on top of it (CONVENTIONS.md — *Integration
   branches*). For platform work (pro mode): collaborative feature
   branch `vibe/<short-slug>` → PR to `main`.
3. Implement, run `make lint` + `make test`.
4. Push; the mod PR's checks re-run — monitor CI, fix failures.
5. Keep the mod PR in draft while the mod is in progress. The owner
   decides when the mod is complete; then the mod PR goes ready and
   follows the standard path (review by another user → test/validation
   deploy → RC → validate → release → prod with ops check).
6. Report the PR URL; the required reviewers approve (or ask for changes) and the PR automerges
   — the agent never merges). On request, tag and release — only from
   actors authorized by the GitHub policies.
7. **Enrich the docs and skills on your own** (developer-mandated, see
   *Documentation is part of the change* in
   [CONVENTIONS.md](CONVENTIONS.md)): when the session's work taught a
   rule, pitfall or pattern, update the matching skill page, convention
   or repo `AGENTS.md` entry as part of the change — never wait to
   be asked.
8. Verify the roadmap: run `.github/workflows/scripts/sync_roadmap.py
   --check` (the
   [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md)
   skill); if drift is reported, the single writer catches it on the
   next merge or its daily run — **never commit the generated
   artifact to a PR branch**.

## Rules

- **Who may do what is enforced by GitHub, not by this document**: merge
  approvals are enforced by the `main` ruleset of each repository, PR
  validation by its required checks, and deployments by environment
  protection rules. No agent-facing instruction grants or restricts access
  to a person.
- **Required status checks**: the merge-blocking checks are enforced by the
  `main` ruleset of each repository. For `kingdoms`: `check` (Check Docs —
  docstring completeness **and** generated-docs freshness) and `cla` (CLA
  Check). For `kingdoms-services`: the full CI matrix (lint, typecheck, unit
  tests, compose, smoke, Discord smoke, image build). All three repositories
  are public with an active `main` ruleset enforcing their required checks
  (`kingdoms`: `check`, `cla`; `kingdoms-services`: the full CI matrix +
  `cla`; `kingdoms-infra`: its CI matrix + `cla`). A PR cannot be merged
  with a red check.
- **Anyone can run the tests locally**, with no special access: `make lint`,
  `make typecheck` and `make test` in `kingdoms-services`, the doc validation
  in `kingdoms`, the shell checks in `kingdoms-infra`. The local toolchain
  only requires public clones — no credentials. (In practice no human ever
  runs them: the agent runs them, and CI re-runs them on every PR.)
- **Humans never check out, write code, or run scripts.** The only manual
  technical actions are clicks in the GitHub web UI, listed in
  [PROCESS.md](PROCESS.md). An agent session must never propose a
  human CLI step.
- **Always include GitHub links in user-facing reports.** Every PR,
  issue, workflow run or branch mentioned in a report to a human carries
  its full GitHub URL: humans never open a terminal, links are their
  only access to the artifacts.
- All issues are written in English and are self-contained (future sessions
  have no conversation memory).
- **PR draft status is the agent's merge-readiness signal.** The agent always
  opens PRs as drafts. It marks a PR *ready for review* —
  `gh pr ready` — **only** when, from its point of view, the PR can be merged:
  all checks green, implementation complete, self-review done, docs updated.
  If work remains (red or pending checks, missing doc updates, open review
  comments), the PR stays in (or returns to) draft — `gh pr ready --undo`.
  The reviewer remains free to merge or ask for changes at any time.
- Every feature is validated by the game designer in Discord before a release
  is tagged.
- Environments (all on the Kingdoms VPS, deployed by the CD pipeline
  running on its self-hosted runner — installation guide:
  [VPS-SETUP.md](https://github.com/merlin-pinpin-org/kingdoms-infra/blob/main/docs/VPS-SETUP.md)):
  - **personal (`<alias>`)**: deployed **on demand** — the `/deploy` PR
    comment default (the requestor's env, from the roster alias; the PR
    image, commit-SHA tagged, is pinned in the `deploy/<alias>` state
    branch by the kingdoms-deployer GitHub App).
  - **test**: deployed **on demand** — by the explicit `/deploy test` PR
    comment (the shared validation env; the PR image, commit-SHA
    tagged, is pinned in the `deploy/test`
    state branch by the kingdoms-deployer GitHub App — setup guide:
    kingdoms-infra docs/DEPLOY-TEST-APP.md); the push to `deploy/test`
    deploys the pinned image (ADR-0018). Test-config changes on `main`
    also redeploy (the pipeline pins the latest `sha-<sha>` image).
    It is the validation environment where the game designer checks the
    bot in Discord
  - **prod**: released only — image tagged `vX.Y.Z`, triggered by the
    released tag or an ops member, paused until an ops member approves
    the `prod` environment protection (required reviewers), and gated to
    ops actors by the Actions policy on the Deploy prod workflow. Only
    ops deploys to production.

## Cross-references

- [AGENTS.md](../AGENTS.md) — agent entry points (all 3 repos link back
  to this document)
- [CONVENTIONS.md](CONVENTIONS.md) — conventions shared by the three
  repositories (language, secrets, PR lifecycle, issues, checks)
- [DEVELOPER.md](DEVELOPER.md) — developer guide for this repo
- [WORKFLOWS.md](WORKFLOWS.md) — user-facing game workflows
- [PROCESS.md](PROCESS.md) — the four processes (development, test
  deployment, release, production) per role: game designer, developer, ops
- [ARCHITECTURE.md](ARCHITECTURE.md) — technical architecture, including the
  deployment flow
- `kingdoms-infra` — GitOps implementation of the deployment flow
  (kingdoms-infra#2)
