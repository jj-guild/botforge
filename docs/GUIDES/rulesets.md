# GitHub rulesets — reference and policy

This guide documents **every ruleset of the three BotForge repositories**,
the platform's policy on them, and the workflow that keeps them honest.
Rulesets are the enforcement layer of the conventions: what the session
discipline handles softly (draft status, self-review), GitHub enforces
hard (required checks, required reviews, merge methods).

> **Humans never code — and barely click.** Rulesets are one-time
> bootstrapping: an org admin creates them once in the GitHub web UI
> (Settings → Rules → Rulesets), and the agent maintains the
> documentation you are reading. The agent never edits rulesets through
> the API (org permissions live with the maintainers); it documents the
> expected state and flags drift.

## Policy — merge method: rebase, never squash

**Every `main` ruleset allows only the `rebase` merge method** — this is
a parameter of the `pull_request` **rule inside the ruleset** (Require a
pull request before merging → Allowed merge methods: **Rebase and
merge** only). There is no repository-level merge-method setting to
touch: squash, merge commits and the method choices all live in the
ruleset's `pull_request` rule.

Why rebase-only:

1. **Stacked PRs are the norm** (CONVENTIONS.md, *PR lifecycle*): sessions
   grow one PR per repo with clean, sequential, logical commits. A squash
   would collapse that story into one opaque commit and rewrite the SHA,
   breaking every PR stacked on top of it (forcing `--force-with-lease`
   cascades and stale reviews).
2. **Linear history is already a rule**: every `main` ruleset enforces
   `required_linear_history` + `non_fast_forward` + `deletion`. Rebase is
   the only merge method consistent with that shape.
3. **The session commits like it merges** (5-bis): each commit is a
   self-contained logical unit that passes the checks on its own —
   rebasing preserves exactly those units, squash destroys them.
4. **Automerge needs no question asked**: with a single allowed method,
   GitHub's automerge picks rebase mechanically; there is no squash-or-
   rebase decision left to anyone, and the auto-commit never guesses.

Consequence for sessions: never merge locally, never create merge commits,
keep the branch rebased, and expect the
PR to land as its exact commit list, one commit per logical unit.

## Rulesets per repository

The authoritative live state is the GitHub API
(`gh api repos/jj-guild/<repo>/rulesets`); this section is the
**documented expectation** the check workflow compares against.

### `botforge-services` — `main`

- Target: `~DEFAULT_BRANCH`, enforcement **active**
- Rules:
  - `deletion`, `non_fast_forward`, `required_linear_history`
  - `pull_request`: 0 blanket approving reviews, **code-owner review required**,
    review threads must be resolved, **allowed merge methods: `rebase`
    only**
  - `required_status_checks`: Lint (ruff), Typecheck (mypy strict), Unit
    tests (pytest), Validate and boot docker-compose.yml, Smoke test
    (bot image + MongoDB + Redis), Discord smoke (real gateway via the
    CI/CD bot), Build and test the image, Generate and check pydoc
    freshness, Check Docs

### `botforge` — `main`

- Target: `~DEFAULT_BRANCH`, enforcement **active**
- Rules: `deletion`, `non_fast_forward`, `required_linear_history`,
  `pull_request` (0 blanket approvals, code-owner review required, **rebase-only**),
  `required_status_checks` (docs validation)

### `botforge-infra` — `main`

- Same shape as `botforge` `main` (rebase-only, code-owner review).

### `botforge-infra` — `Deploy TEST` / `Deploy PROD` (state branches)

- Targets: `refs/heads/deploy/test`, `refs/heads/deploy/prod`
- Rules: `deletion`, `non_fast_forward`, `required_linear_history`,
  `required_status_checks`; `Deploy PROD` additionally requires a pull
  request and `required_deployments` (the `prod` environment approval) —
  **approving a prod deployment is merging that PR** (ADR-0018).
- Bypass actors: `maintainers`, `ops` teams and the `jj-guild-deployer`
  App (the state-branch writer). The **production gate is the GitHub
  environment** (`environment: prod` in deploy-env.yml — required
  reviewers, secrets, `env-prod` runner), not the workflow and not the
  ruleset.
- **Rollback** (`rollback.yml`): a broken deployment reverts the *pinned
  state* (never the code on main). On `test` the revert pushes directly
  (no PR required by the ruleset); on `prod` it opens a revert PR to
  `deploy/prod`. The push re-triggers the Deploy environment workflow,
  which re-applies the previous known-good image — **except when the
  re-pinned image is already the one running**, in which case the revert
  is pushed without re-deploying (botforge-infra#96: silent re-pin).
- **Day-to-day control** (`env-control.yml` + `scripts/envctl.sh`):
  start / stop / restart / status per environment, run on the env's
  runner from a workflow_dispatch with two choice lists (command +
  environment); it dumps the stack state and never deploys, pulls or
  touches the pinned state. Prod control operations pass the
  environment gate (required reviewers); `status` is read-only.

### `botforge-services` — `release-tags` (target: tag)

- Guards tag creation (`vX.Y.Z`) — only the release pipeline may tag;
  see [../PROCESS.md](../PROCESS.md) *Releases*.

### Rulesets for many environments — wildcard or per-env, documented

The two live rulesets target explicit refs (`refs/heads/deploy/test`,
`refs/heads/deploy/prod`). A ruleset condition **can match a wildcard** —
`refs/heads/deploy/*` — which covers every current and future
environment state branch in one ruleset, with a single set of rules
and bypass actors.

Trade-off, documented choice:

- **Wildcard (`deploy/*`)**: one ruleset for the whole environment
  fleet; a new environment inherits its protection the moment its state
  branch exists — no maintainer action per env. Limitation: the rules are
  shared, so a prod-only rule (PR requirement, `required_deployments`)
  would apply to test too, or the prod PR rule needs to stay a separate
  ruleset targeting `deploy/prod` explicitly.
- **Per-env rulesets**: rules can differ per env (the current state —
  `deploy/test` accepts a direct push from the jj-guild-deployer App,
  `deploy/prod` requires an approved PR + `required_deployments`);
  at N environments that is N rulesets to create and keep aligned.

Current choice: **two explicit rulesets** (test and prod differ — direct
push vs PR + deployments gate), a split that a wildcard cannot express.
If the fleet grows with uniform per-env rules (e.g. per-contributor
environments, all test-like), the wildcard `Deploy *` ruleset is the
scalable option, provisioned once; environments that need different
rules get their own explicit ruleset (GitHub supports several rulesets
matching the same ref — the strictest wins).

Documented expectations for every future deploy ruleset: same rules as
`Deploy TEST` for test-like envs; PR rule + `required_deployments` for
prod-like ones; bypass actors `maintainers`, `ops`, `jj-guild-deployer`;
the gate always lives in the GitHub environment (required reviewers),
never in the workflow.

## Ruleset parameters — exact expected state

For each repository's `main` ruleset (all three are **exactly
identical**), the `pull_request` rule declares: required approving
reviews **0** (the code-owner requirement is what forces the review —
CODEOWNERS names the owner of every touched path, and GitHub requires
that owner's approval; a blanket count would double-review mod PRs),
**require review from code owners**, require conversation resolution,
allowed merge methods **["rebase"]**. **Bypass actors**: the
`maintainers` team (org-wide maintainer on all three repos) — the trust
anchor for bootstrapping and emergencies; nobody else bypasses, the agent
included. The only remaining repository-level settings (Settings →
General → Pull Requests) are the **user preferences**: auto-merge enabled
and automatic head-branch deletion — everything else about merging lives
in the ruleset.

**CODEOWNERS is the review router** — the ruleset only enforces "the
owner(s) of every touched path approved". The default rule
(`* @jj-guild/maintainers`) makes everything non-mod
maintainer-reviewed; each mod's paths are delegated to its designer
(one line per mod, added in the mod's own PR — GitHub CODEOWNERS has no
negative/regex patterns, so per-mod lines are the mechanism; a new mod
means adding its line, which is part of the mod's bootstrap).

**CODEOWNERS also protects the authority surfaces** — the files the
permission model itself relies on are maintainer-reviewed in the three
repositories: `.github/workflows/` (the CI/CD and deploy gates — a
workflow change is a security-sensitive change), `AGENTS.md`,
`CONTRIBUTORS.md` (the roster: the source of truth the `authorize.yml`
gates read), `docs/DECISIONS/` (ADRs), and `scripts/` (sync and
validation machinery). Combined with the required code-owner review on
`main`, no session or contributor changes the permission model without
a maintainer approving it.

## Shared checks — factorized once, referenced thrice

Several checks are logically identical across the three repos but exist
as three copies (CLA Check, Auto-triage, Validate issue): GitHub runs
workflows per repository, so the *contexts* cannot be shared, but the
*code* can: a single reusable implementation (a script in `botforge` or
a `workflow_call` workflow) with three thin per-repo wrappers keeps the
behavior identical everywhere while the maintenance happens in one
place. Required-check contexts stay per-repo (they match by exact
workflow/job name) — factorization reduces drift, not check count.

## Drift detection — the ruleset check workflow

Documentation is the expectation; GitHub is the reality. A scheduled
workflow (botforge-services #183, *Ruleset conformance*:
`.github/workflows/ruleset-conformance.yml`, daily at 06:00 UTC +
`workflow_dispatch`) compares the live rulesets of the three repos
against this guide's expected state:

- **fail**: a `main` ruleset whose `allowed_merge_methods` is not
  `["rebase"]`, a missing code-owner review requirement, a missing or
  renamed required status check, a ruleset flipped to `evaluate` or
  disabled;
- the failure opens an issue flagged for maintainers with the exact
  drift — humans resolve it in the web UI (the doc drives GitHub, never
  the other way around, same as [CONTRIBUTORS.md](../../CONTRIBUTORS.md)).

## Bootstrapping checklist (one-time, org admin)

1. On each repo: `main` ruleset — linear history + PR rule (1 approval,
   code-owner review, conversation resolution, **rebase only**) +
   required checks (names must match the CI job names exactly).
2. `release-tags` (botforge-services) and the deploy state-branch
   rulesets (botforge-infra).
3. Repository-level user preferences: **Allow auto-merge** on,
   automatic head-branch deletion on (Settings → General → Pull
   Requests — the only settings outside the rulesets).
4. No bypass actors on any ruleset — the agent included.
