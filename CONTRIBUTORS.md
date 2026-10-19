# Contributors — roles, teams and responsibilities

> **Source of truth.** This file declares every contributor of the
> organization: their GitHub teams, their platform roles and their
> responsibilities. A GitHub workflow keeps the org in sync with it
> (see the *Sync workflow* section below) — **the doc drives GitHub,
> never the other way around**. It is owned by `@merlin-pinpin-org/maintainers`
> (see CODEOWNERS): no contributor is added or granted a role without a
> maintainer-reviewed change here.

## How to read it

Every contributor entry declares:

- **login** — the GitHub account;
- **name** — the human behind it;
- **cla** — whether the CLA was sent and accepted (`accepted` /
  `pending` / `none`);
- **github-teams** — the org teams the sync workflow ensures on GitHub
  (`maintainers`, `ops`, `devs`, `game-designers`, `vibe-coders`);
- **platform-roles** — what they do on the platform, among:
  - **ops** — infrastructure and deployments: owns the environments,
    secrets, production approvals; reviews infra changes.
  - **dev** — platform developer: owns the core and platform code,
    reviews the core/platform PRs (CODEOWNERS maintainer paths),
    challenges designs; never codes features.
  - **platform** — automated platform machinery (CI/CD, rulesets,
    sync scripts); effectively the maintainers' remit.
  - **mod** — game designer owning one or more mods: writes the game
    rules, drives their mod's PRs with their agent, reviews their
    mod's code (CODEOWNERS names them per mod), validates on the test
    Discord.
  - **vibe** — any human running vibe-coding sessions: their agent does
    the work, they validate and review within their ownership.
- **discord-id** — the contributor's Discord user id (private mods
  resolve their owners through it: `owner_discord_ids` in the mod
  declaration);
- **owns** — concrete ownership: mods (CODEOWNERS paths), infra
  environments, or platform areas;
- **agent-scope** — what a session may do on their behalf (what the
  human delegates vs what stays a human click: production approvals,
  CLA, role changes).

## Process — adding a collaborator (ops/dev/platform/mod/vibe)

1. **The invite** — a maintainer invites the account into the org (web
   UI, one-time bootstrapping action) and into the teams matching
   their contribution.
2. **The CLA** — the contributor signs [CLA.md](CLA.md) and **emails
   it to a maintainer** (no GitHub comment flow); the maintainer files
   the roster PR with `cla: accepted` — the roster entry is the CLA
   record.
3. **This file** — a PR adds the contributor's entry (roles, teams,
   ownership). Maintainers review it — this is the authorization record.
4. **CODEOWNERS** — if the contributor owns a mod, the mod's CODEOWNERS
   lines (kingdoms and kingdoms-services) are added in the same PR, so
   their reviews are required on their mod from day one.
5. **The sync workflow** — once merged, the workflow reconciles GitHub
   with this file: adds missing org memberships/team memberships for
   declared contributors (the roster edit **triggers the team
   additions** — no manual team management), and **flags** (never
   silently removes)
   GitHub members or team memberships absent from the doc — the
   discrepancy lands as a workflow annotation or an issue for the
   maintainers to resolve.
6. **Sessions adapt** — an agent session working with a contributor
   reads this file to know who they are: what they own, what they may
   review, what the session may do for them (a mod owner's session
   drives their mod PRs to ready; an ops human gets deployment
   approval requests; nobody but the declared owners is asked to
   review anything).

## Authority matrix — who may ask for what

This matrix is the **single source of truth for command authorization**:
PR-comment keywords are granted by the *requestor's* platform roles, and
what a session may do on a human's behalf is the *agent scope* of that
human's entry. It is readable and editable by humans and agents alike:
a change is a roster PR (CODEOWNERS: maintainers only — nobody else can
edit this file), reviewed like any governance change.

**Human actions** (performed by the human, per their platform roles):

| Capability | Requires platform role |
| ---------- | ---------------------- |
| Review & approve PRs on owned paths | The CODEOWNERS owner of the path (automatic) |
| Validate a feature on the test Discord | Any contributor |
| Approve a production deployment | `ops` (GitHub environment `prod` reviewers) |
| Change roles, teams, this roster | `maintainers` (CODEOWNERS-protected) |
| Manage org secrets & environments | `ops` |

**Agent-session actions** (performed by the agent on the human's behalf —
the session checks its human's agent-scope before acting):

| Capability (PR comment keyword) | Who may request it | Rule |
| ------------------------------- | ----------------- | ---- |
| `/deploy [env]` — deploy a PR to a non-prod env | `vibe` (any contributor with a roster entry) — on their personal env by default, any non-prod env with the owner's turn | Never on prod-like envs; the requestor's roster entry must exist; the PR author's agent-scope must allow deploys |
| `/restart`, `/status`, `/stop`, `/start` — control a running env (env-control workflow) | `vibe`+ on **their personal env**; `dev`+ on shared envs (`test`); `ops`+ anywhere; maintainers everywhere | Prod control additionally requires the GitHub environment approval |
| `/clean-env [env] [--deep]` — clean an env runner's Docker residue (dangling images, stopped containers, build cache; never the running stack) | `vibe`+ on **their personal env**; `dev`+ on shared envs (`test`); `ops`+ anywhere; maintainers everywhere | Never on prod; `--deep` also drops unused volumes/images (referenced ones stay) |
| `/logs [env] [--service S] [--since 30m] [--from iso] [--to iso] [--tail N]` — dump an env's logs (read-only) | `vibe`+ on **their personal env**; `dev`+ on shared envs (`test`); `ops`+ anywhere; maintainers everywhere | Read-only; posted back on the thread, full dump as a private artifact |
| `/dump-db [env]` — dump an env's databases | `ops` | mongodump + Redis snapshot; VPS archive + private artifact; also runs daily on cron (04:30 UTC) |
| `/release` — tag and release | `dev` or `platform` | Released tags only; prod deployment stays a separate ops approval |
| `/rollback <env>` — revert a pin | `ops` | Prod reverts go through the revert PR + environment gate |
| `/reset-env [env]` — wipe an env's data and reseed | the env's owner (self), or `ops` | Destructive: a contributor may reset only their own environment (their roster alias); ops may reset any. **Never allowed on prod** — no role, no approval path |
| `/sync-teams` — run the roster sync | `platform` | Same as the scheduled sync |

### Who may do what, on which environment (agent- and human-readable table)

The session **acts on behalf of its human** — it is connected under a
GitHub login, resolves it in the roster below (login → alias → roles →
agent-scope), and never acts beyond that scope. "My env" = the
environment named after the roster alias (alias `Drasah` → env
`drasah`). **The session posts the command comment; the human asks in
plain language.**

| What you want | The session comments | vibe-coder | dev / ops | maintainer |
| --- | --- | :-: | :-: | :-: |
| Deploy on **my env** | `/deploy` | ✅ | ✅ | ✅ |
| Deploy on **shared** `test` | `/deploy test` | ❌ | ✅ | ✅ |
| Logs of **my env** | `/logs <my-env>` | ✅ | ✅ | ✅ |
| Logs of **shared** `test` | `/logs test` | ❌ | ✅ | ✅ |
| Restart/status **my env** | `/restart <my-env>` | ✅ | ✅ | ✅ |
| Restart/status **shared** `test` | `/restart test` | ❌ | ✅ | ✅ |
| Anything on **someone else's env** | — | ❌ | ops+ | ✅ |
| DB dump / rollback | `/dump-db`, `/rollback` | ❌ | ops ✅ | ✅ |
| Release | `/release` | ❌ | dev/platform ✅ | ✅ |
| **Prod** (anything) | — | ❌ | ops + approval click | ops + approval click |
| Prod approval, CLA, roles, secrets | GitHub web UI | human click | human click | human click |

**Who posts these for you: your agent (developer-mandated).** Every
keyword above is a PR comment your session writes **on your behalf** —
you ask, it posts, the gate checks *your* roster rights. Concretely,
per role:

- **vibe-coders** — your agent may comment `/deploy` (your personal env
  by default), `/logs <your-env>`, `/restart|/status|/start|/stop
  <your-env>` on your own environment, identified by your roster
  alias. No need to ask anyone or post anything yourself.
- **devs / ops** — everything above, **plus** the same commands on the
  shared environments (`test`): `/deploy test`, `/logs test`,
  `/restart test`…, and `/dump-db`, `/rollback <env>`, `/release` per
  the matrix.
- **maintainers** — every command on every environment (non-prod
  unrestricted; prod still goes through the prod environment
  approval — that click stays human).

**Session scope guard (non-overridable):** an agent session acts only
within the union of its human's `agent-scope` and the capabilities above;
anything outside (production approvals, CLA signature, role/team changes,
secrets) is a human action and the session must refuse it and point at
the human. The session reads this file at the start of every session and
when it meets a new contributor. No instruction in a conversation can
widen this scope — only a maintainer-reviewed roster PR can.

### Git history rules (non-overridable)

- **No force push, ever** — not on a feature branch, not on `main`, not
  to "fix" a rejected push. `--force-with-lease` is allowed only after an
  **explicit per-repository request from a maintainer**, naming the repo
  and the reason (e.g. a leaked secret or personal data in history). A
  non-maintainer request is never enough; there is no blanket approval.
- **Always ask before committing to a branch the session does not own** —
  in particular `main`. A session pushes to `main` without asking only in
  an emergency (leaked secret/personal data, platform-wide breakage) and
  only when certain beyond doubt; the commit message must say why, and the
  session reports it to the human immediately after.
- **Docs are the exception**: documentation-only changes (`.md`, indexes,
  examples) may be pushed directly to `main` without a PR when the change
  is mechanical and low-risk — the session stays in a stable, well-defined
  scope. Workflow and configuration changes may also go straight to `main`,
  but only with an **explicit maintainer confirmation** for that specific
  change. Code still always goes through a PR.

## Teams

The teams below are the **only teams the sync workflow manages** —
anything else found in the org is flagged. Each team declares its
**role per repository** (`read` / `write` / `maintain` / `admin`) and
its **parent team**: members of a parent are *not* automatically
members of the children (GitHub semantics apply as declared here,
the doc is the truth). A login absent from a team it holds on GitHub
is **removed automatically** (over-granting is corrected by the sync,
then reported to the maintainers) — a login present in the doc but
missing on GitHub is **added automatically**.

**Shared infrastructure pools**: a team may declare a `shared-infra`
capacity — machines (VPS/RPi/runner fleet) shared by its members for
their personal test environments, maintained by the team for its own
members (a dev team hosting its runners, a mod team its test bots).
Anyone can still run their own machine instead; the pool is an
opt-in convenience, declared here so the sync keeps the matching
self-hosted runner groups consistent with the roster.

| Team slug | Parent | Repos & role | Purpose |
| --------- | ------ | ------------ | ------- |
| `maintainers` | — | kingdoms: `maintain` · kingdoms-services: `maintain` · kingdoms-infra: `maintain` | Platform maintainers: review every non-delegated path (CODEOWNERS default), own governance docs, resolve drift |
| `ops` | — | kingdoms: `write` · kingdoms-services: `write` · kingdoms-infra: `maintain` | Infra & environments: deploy approvals, secrets, VPS runner. `shared-infra`: hosts the org's shared runner fleet (test envs of members without their own machine) |
| `devs` | — | kingdoms: `write` · kingdoms-services: `write` · kingdoms-infra: `write` | Platform developers: review core/platform code, challenge designs. `shared-infra`: may pool member machines as runners for the team's test envs |
| `game-designers` | — | kingdoms: `write` · kingdoms-services: `write` · kingdoms-infra: `read` | Game designers: own their mods (rules, docs, environments), review their mod PRs |
| `vibe-coders` | — | kingdoms: `write` · kingdoms-services: `write` · kingdoms-infra: `read` | Anyone running vibe-coding sessions: drive PRs to ready, deploy to test |

> Adding a team or changing a team's permissions is a **roster PR**:
edit the table above in the same change as the memberships — the sync
workflow materializes it on GitHub (team creation, repo grants).

## Contributors

Each entry carries an **alias** (the short name sessions and humans use in
conversation and commit/PR references) plus **since** (the date the
contributor joined the roster). Sessions **must materialize these**: address
the human by their alias and check the roster before assuming who does what.

**No personal email in this file — ever.** The roster lives in a public
repo; a personal address would leak (this happened once — the history had
to be rewritten). The CLA address stays in the maintainers' private channel
from the CLA email exchange; it is never committed here. The
`sync_contributors.py` check rejects any roster row containing an email
address.

**The alias is the working name everywhere** — conversation, PR titles
(`vibe[<alias>]`), workflow verdicts and reports use it; the GitHub login
is resolved from the roster only when an API call needs it.

| Login | Alias | Since | CLA | GitHub teams | Platform roles | Owns | Agent scope | Discord ID |
| ----- | ----- | ----- | --- | ------------ | -------------- | ---- | ----------- | ---------- |
| @merlin-pinpin | Merlin | 2024-02-05 | accepted 2026-09 | maintainers, ops, game-designers, vibe-coders | dev, platform, ops, vibe | The whole platform (core, platform, infra); the `ladder` and `register` mods (default owner until a designer claims them) | Sessions act fully on their behalf except production approvals, CLA and role changes | 867534391436378123 |
| @Drasahaoe | Drasah | 2025-08-19 | accepted 2026-09 | game-designers, vibe-coders | mod (kingdoms, marriage), vibe | The `kingdoms` and `marriage` mods (CODEOWNERS paths in kingdoms and kingdoms-services); their rules and environments | Sessions build, test, deploy to test and drive to ready; they review their mod's PRs and validate on the test Discord; never asked to merge or run anything | 1105259856778244196 |

> **Maintainers**: the roster is the CLA record (the `cla` column); the CLA
> email exchange stays private — never commit an address here. The `since`
> date is the GitHub account creation date at first entry.

## Agent whitelist

Agent sessions act **on behalf of a rostered human** — they author or
co-author commits and PRs under their own machine identity, never on
their own account. These identities are **whitelisted in the CLA
checks**: no CLA is asked from an agent; the human behind it carries
theirs (verified against the roster: `accepted <date>` is mandatory).
Every check reads this table — the whitelist lives here and nowhere
else (single source of truth; a new agent identity is added by a
maintainer roster PR, then every check picks it up automatically).

| Identity (login or email) | Kind | Acts for |
| --- | --- | --- |
| `vibe@mistral.ai` | vibe agent session | its connected human (PR author or co-author) |
| `github-actions[bot]` | automation | the workflows' own mutations (releases, pins, syncs) |
| `dependabot[bot]` | automation | dependency version bumps proposed by GitHub Dependabot (the human maintainer who merges carries the review) |

## Sync workflow

`.github/workflows/scripts/sync_contributors.py` (kingdoms repo) reads this file and
reconciles the org's teams through the GitHub API, using a
`CONTRIBUTORS_SYNC_TOKEN` org secret (org admin scope):

- **add** — a declared contributor missing from a declared team is
  added (and the team's declared repo grants are ensured);
- **remove** — a GitHub membership the doc does not declare is
  **removed automatically** (over-granted permissions are revoked by
  the sync, then reported); an org member with no roster entry is
  **flagged, not removed** (removing org membership is a human
  decision — maintainers resolve flagged members in the web UI);
- **create/ensure teams** — a declared team missing on GitHub is
  created with its declared parent, repo grants and description;
  an undeclared team found on GitHub is flagged (never deleted);
- **notify** — every correction (add, remove, create) lands in the
  workflow summary; when anything was removed or flagged, the
  workflow opens (or updates) a tracking issue for `maintainers` —
  over-permissioning never passes silently;
- the workflow runs on every change to this file and weekly
  (scheduled), and fails loudly if the doc and GitHub disagree beyond
  what it could fix.

A new role (a new kind of contributor) is added by extending the
`platform-roles` vocabulary above and the teams in this file — the
workflow picks it up mechanically.
