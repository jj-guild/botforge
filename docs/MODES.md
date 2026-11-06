# Modes — how every contributor works

> **Source of truth for the three working modes.** Every human or AI
> agent picks a mode from this page before touching a repo. The mode
> decides the branch strategy, the review gate and the GitHub powers
> used. When a session is unsure which mode applies, it asks the human
> — it never silently upgrades its own powers.

The mode is a property of **the person + the task**, declared by the
roster ([CONTRIBUTORS.md](../CONTRIBUTORS.md)): maintainers may use all
three, dev/ops use pro mode by default, vibe coders live in sandbox mode.
Nobody downgrades their gate without an explicit human decision.

## The three modes

| | Sandbox (vibe coder) | Pro (dev/ops) | Cowboy (maintainer only) |
|---|---|---|---|
| Who | Any rostered user, default for `vibe` role | `dev` and `ops` roles | `maintainers` only |
| Branch | `vibe/<alias>/main` — everything stacks there | Feature branch per subject → PR to `main` | `main` directly |
| Review gate | Another user validates the PR to `main` (standard path) | CODEOWNERS review, PR per feature | **Explicit human validation per operation** |
| Environment | Personal env only (their bot, their Discord, their runner) | Personal env → shared validation env (`test`) → `prod` | Any |
| Deploy | Own env; `test` via the standard path | Own env, `test`, `prod` (ops check) | Any, including prod |
| Force push / bypass | Never | Never | Yes, after explicit human OK — and you own the fallout |

## Sandbox mode (vibe coder) — the default for vibe roles

One branch, one PR, one environment, zero friction with the rest of
the org:

- **Branch**: everything lands on `vibe/<alias>/main`. No per-feature
  branches, no PRs between own branches — commits stack directly on
  the integration branch for the whole life of a personal mod. The
  sync workflow keeps `main` merged in; the owner resolves conflicts.
- **Mod PR**: while a personal mod is being built, exactly **one PR
  from `vibe/<alias>/main` to `main`** stays open — the *mod PR*. It
  is opened as a draft as soon as work starts, it runs the required
  checks on every push (that is its purpose: continuous validation of
  the stack), and it is never merged until the mod is complete. Do
  not stack additional PRs on top of it — that adds workflow friction
  for no benefit; push to the integration branch instead.
- **Environment**: the personal environment (bot + Discord server +
  runner labeled `env-<alias>`) deploys from the user branch; anything
  can be tested there, it is a sandbox.
- **Promotion**: when the owner judges the mod complete, they mark the
  mod PR ready — validated by another user (the standard path,
  [CONVENTIONS.md](CONVENTIONS.md) — *Integration branches*). Until
  then, nothing leaves the sandbox.
- **Agents do the work**: the human describes, the agent stacks commits
  on the user branch, pushes so the mod PR's checks re-run, deploys on
  the personal env and reports. The human validates in **their**
  Discord.

## Pro mode (dev/ops) — PR per feature

- **Feature branch per subject** (`vibe/<slug>`): one branch per
  coherent scope, collaborative PRs to `main`, normal size, CODEOWNERS
  review. Platform work is collaborative: several PRs may be open in
  parallel — the sequential-chain constraint applies nowhere.
- **Personal environment** still exists for work in progress (dev in
  progress, risky experiments) — same mapping `vibe/<alias>/main` ↔
  `env-<alias>`.
- **The ladder**: personal env → shared validation env (`test`) →
  `prod` (ops/owner check). A change is never promoted skipping a rung.
- Long evolutions follow this mode even for maintainers; only
  justified urgent/quick fixes may take the cowboy shortcut.

## Cowboy mode (maintainer only) — explicit, single-shot per command

- Direct push to `main`, ruleset bypass, force push, no PR: everything
  GitHub lets a maintainer do.
- **The human validates explicitly for every single operation of this
  kind** — the agent never assumes cowboy mode, never "inherits" it
  from the previous operation, and states what it is about to do
  before doing it.
- **Activation is single-shot and expires with the next command:** an
  explicit "cowboy" activation covers exactly one operation — the next
  command the session runs — and expires the moment that operation
  ends. It is never a session-long state: any later cowboy operation
  needs a fresh, explicit activation and confirmation, even mid-
  session, even for the same kind of operation.
- **You own the fallout**: no review caught it, so whatever breaks is
  the author's. Use it for justified speed (broken CI fix, hotfix,
  state-branch surgery), not for convenience.
- Default is pro mode: a maintainer works like dev/ops unless the
  situation justifies cowboy and the human has said yes.
- **Agents cannot merge PRs** (the rulesets block every session — API
  and CLI alike). When a maintainer asks to "merge" a PR in cowboy
  mode, the agent pushes the PR's commits directly to `main`
  (ruleset bypass) instead — after one explicit confirmation **per
  push**. **Force-pushing `main` is always refused**: technically
  possible, never done — history is never rewritten.
- **The word "cowboy" from a maintainer is an activation request, not
  an order**: the session answers with an explicit confirmation ask
  that names the PR and summarizes its content ("Push the commits of
  PR #N — <one-line summary> — directly to main?") and only pushes
  on the human's yes. The activation is single-shot (one operation,
  expires immediately) and is refused from any non-maintainer.
- **A cowboy push that supersedes an open PR closes it explicitly**:
  pushing the PR's commits to `main` makes the PR mergeable-state
  moot — GitHub closes it as merged-equivalent only via the UI; the
  session closes the PR with a comment stating what happened
  ("superseded by direct push of these commits to main, cowboy mode,
  <alias>") so the review thread stays readable.

## Environment map (all modes)

| Environment | Branch | Runner label | Discord | Who deploys |
|---|---|---|---|---|
| `env-<alias>` (personal) | `vibe/<alias>/main` | `<alias>` (shared VPS ok) | Personal server, personal bot | The owner (any mode) |
| `test` (shared validation) | `deploy/test` | `test` | Shared validation server | Any user, via `/deploy test` |
| `prod` | `deploy/prod` | `prod` (own VPS) | Production server | Release pipeline + ops approval |

Co-located personal environments on one VPS use **per-env debug host
ports** (`kingdoms-infra` docs/ENVIRONMENTS.md); each environment
remains an isolated sandbox (own compose project, own data volumes).

## Agent rules (binding)

1. **The session asks what the session is for** before starting work —
   personal mod (sandbox) or platform work (pro) — and guides the
   human accordingly (mod creation: help and point to the mod
   bootstrap path, never a blank slate).
2. **`main` is right by default.** When the session's opinion conflicts
   with what is on `main` (architecture, conventions, patterns), it
   follows `main` and steers the human toward best practices;
   disagreement is raised to the human (and the maintainer for
   core/platform), never worked around.
3. Sandbox mode never touches `main`, never opens PRs to `main`
   uninvited, never deploys outside the personal env.
4. Pro mode never force-pushes, never bypasses a ruleset. No mode
   ever force-pushes `main` — history is never rewritten.
5. Cowboy mode requires a fresh, explicit human validation **per
   operation**; an activation is valid only for the **next command**
   and expires as soon as it completes — it never lasts the session;
   the session reports each cowboy operation in its
   summary so the audit trail exists.
5b. No session merges PRs (API-blocked); the cowboy "merge" is a
   direct push of the PR's commits to `main`, confirmed once per
   push.
6. The mode applies to the session's GitHub actions only — the human
   can always do more in the web UI than the session may automate.
