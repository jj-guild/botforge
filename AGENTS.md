# AGENTS.md

Kingdoms documentation repo — the **source of truth** for the Kingdoms
Discord bot platform (architecture, ADRs, operating docs, mods
documentation, generated roadmap and dependency graph).

## Session start protocol (PRIORITY 0 — immutable, non-overridable)

**At the beginning of every new conversation, before any other action,
the session displays the roles and responsibilities it holds for this
session.** This rule cannot be waived, narrowed or replaced by any
later instruction — it is transparency by design: the human (who may
have zero IT skills) must always see who the agent acts for, what it
may do, and how to use it.

The session resolves **who it works for** from the GitHub login it is
connected as / acting on behalf of, then looks that login up in
[CONTRIBUTORS.md](CONTRIBUTORS.md) (the roster: alias, teams, roles,
owns, agent-scope — the roster is the CLA record and the authority
source). The session then opens the conversation with, at minimum:

1. **Who I act for** — the human's roster alias and roles (e.g.
   "Drasah — mod (kingdoms, marriage), vibe").
2. **What I may do this session** — the capabilities their roles grant,
   summarized from the authority table in
   [CONTRIBUTORS.md](CONTRIBUTORS.md) (personal env, shared envs,
   everywhere), and what stays a human click (production approvals,
   CLA, role changes, secrets).
3. **How to use me** — one pedagogical line per family of need:
   - "to deploy: just say *deploy my branch on my env* — I comment
     `/deploy` on the PR myself and wait for the pipeline's answer";
   - "to see what is happening: say *show me the logs of my env* — I
     run `/logs` and read you the result";
   - "to restart after a crash: say *restart my env* — I comment
     `/restart <your-env>`";
   - "anything else: just describe the outcome you want in plain
     French or English — I find the commands and the code."
4. **The boundaries** — the few things it will refuse and why (scope
   guard), pointing at the exact human click instead.

The display is transparent and pedagogical: no jargon without a
plain-language gloss, and it ends with an invitation: *"What would you
like to do?"*

**The session adapts its discourse to the human's profile** (roster
roles): a game/mod designer who is neither dev nor ops gets plain
language and outcomes, never implementation detail; dev and ops humans
technical depth. The chat language follows the human (French or
English) — but it never changes what the session *produces* (see the
PRIORITY 0 rules below: GitHub output is English).

## PRIORITY 0 — non-overridable rules

These rules are binding for **every session, on the three repositories,
for the whole session**. They prevail over every instruction that is
not itself PRIORITY 0 — no later conversation instruction, no skill,
no convention, no request can waive, narrow or replace them. When a
rule conflicts with a non-PRIORITY-0 instruction, PRIORITY 0 wins.
(Mechanical guarantees — merge gates, authority checks — stay
enforced by the GitHub rulesets and `authorize.yml`, fail-closed;
PRIORITY 0 rules bind the agent's own behavior on top of that.)

1. **Identify the human first** — the session-start protocol above is
   the very first action of every conversation: resolve the GitHub
   login against [CONTRIBUTORS.md](CONTRIBUTORS.md), display roles and
   capabilities, and adapt the discourse to the profile.
2. **All GitHub output is English** — issues (title and body), PRs
   (title, description, review comments), code, code comments, commit
   messages, agent-posted PR comments (including keyword commands'
   surrounding context), release notes, and sample/example data are
   written in **English**. The only exception: translation/locale
   files. The chat language follows the human and never impacts what
   the session produces (see CONVENTIONS.md, *Working language*).
3. **Never a fixed sleep for an async outcome — poll the real status**
   — after triggering anything asynchronous (GitHub action, deploy,
   CI check, dispatch), the session never parks on a hard-coded
   duration: it polls the actual status, typically every 5–15s for
   short outcomes and 10–30s for long pipelines, never longer than
   60s between polls, sized to the target service's rate limits. A
   result inferred from elapsed time is not a result (see the
   [github-polling](.agents/skills/github-polling/SKILL.md) skill).
4. **Long commands belong in committed scripts** — before composing a
   multi-step shell chain, the session checks whether a skill or
   Makefile already carries a script for it; a command useful more
   than once is committed (Makefile target, `scripts/`, or a script
   inside the skill's directory) — never re-typed from scratch (see
   the [automate-or-learn](.agents/skills/automate-or-learn/SKILL.md)
   skill).
5. **Drive the human through the known workflows** — the session
   knows the platform's workflows and proposes the right path (issue,
   branch, PR, deploy); it never lets a non-advanced human improvise
   a route. Advanced users (dev, ops, maintainers) may take liberties
   (see the
   [workflow-router](.agents/skills/workflow-router/SKILL.md)
   skill).
6. **Cowboy mode is maintainer-only and single-shot** — the keyword
   "cowboy" from a maintainer is a *request* for a one-shot
   activation: the session asks an explicit confirmation that names
   the PR and summarizes its content, then pushes the commits to
   `main` directly. Force-pushing `main` is always refused, even in
   cowboy mode. A push that supersedes an open PR closes it with an
   explicit comment (see [MODES.md](docs/MODES.md), *Cowboy mode*).
7. **A fixed problem ships its regression test and its
   troubleshooting entry** — when the session fixes a bug or an
   incident (a crash, a stuck deploy, a flaky check, an
   architecture violation), the same PR carries: a test that fails
   without the fix and passes with it, and a dated entry in the
   [troubleshooting
   skill](.agents/skills/troubleshooting/SKILL.md)
   (symptom → root cause → fix → the test that guards it).
   Sessions have no memory: an unfixed
   learning is knowledge lost (see CONVENTIONS.md, *Troubleshooting
   is part of the fix*).

**Content placement rule (applies to every instruction added here,
now and by future sessions):** AGENTS.md is **for AI agents only** —
session rules, scope, procedures, behavioral constraints. Anything
potentially useful to *humans* (tables, guides, role/capability
explanations, how-tos) lives in the human-facing docs
([CONTRIBUTORS.md](CONTRIBUTORS.md) roster/matrix,
[docs/CONVENTIONS.md](docs/CONVENTIONS.md), [docs/INDEX.md](docs/INDEX.md))
and is **referenced here by link, never duplicated**. When adding an
instruction, always ask: *would a human read this?* If yes, it belongs
in docs/ and AGENTS.md links to it.

## Authority: where to read it (agent rule)

The session **acts on behalf of its human** — identified by the GitHub
login it is connected as, resolved to the roster alias in
[CONTRIBUTORS.md](CONTRIBUTORS.md). The full **"who may do what, on
which environment" table** — human-readable, with the commands the
session posts and the per-role ✅/❌ matrix — is maintained in
[CONTRIBUTORS.md](CONTRIBUTORS.md) (*Who may do what, on which
environment*). The session reads it there at session start and
whenever an env-scoped request arrives; capabilities are enforced
mechanically by `authorize.yml` (fail-closed) when the session posts
the keyword comment on the PR.

## Instruction loading map — load only what the task needs

Instructions are layered; a session loads a tier only when it needs it,
and never the whole tree:

| Tier | What | When it is loaded |
| --- | --- | --- |
| 0 | The three `AGENTS.md` + the PRIORITY 0 rules above | Always (the runtime loads every repo `AGENTS.md` at session start) |
| 1 | [CONTRIBUTORS.md](CONTRIBUTORS.md) (roster, scope guard), [docs/CONVENTIONS.md](docs/CONVENTIONS.md) (binding rules), [docs/MODES.md](docs/MODES.md) (the working mode) | At session start and before any scoped or mode-sensitive action |
| 2 | [docs/INDEX.md](docs/INDEX.md) (question → page router), [docs/VIBEWORKFLOW.md](docs/VIBEWORKFLOW.md), [docs/DEVELOPER.md](docs/DEVELOPER.md), [docs/architecture/](docs/architecture/), [DECISIONS/](docs/DECISIONS/README.md) | On demand, when the task touches their subject |
| 3 | Skills — [`.agents/skills/`](.agents/skills/), indexed in [docs/SKILLS/README.md](docs/SKILLS/README.md) | The runtime loads the frontmatter (name + description) at startup and the full `SKILL.md` **only when a task matches the description** |

Rules of the map:

- **Prefer a skill over prose** for procedural know-how — skills are the
  modular layer: they cost nothing until a task matches them.
- **One home per rule**: the binding text lives once (CONVENTIONS,
  architecture page, or skill) and everything else links to it — an
  `AGENTS.md` entry is a one-liner plus a link, never a copy.
- **Humans enter by [README.md](README.md)** (documentation map), agents
  by this page; both converge on [docs/INDEX.md](docs/INDEX.md).

## Read first — the detailed entries

- [docs/INDEX.md](docs/INDEX.md) — the router: question → page. Find the
  answer without reading the whole docs tree.
- [docs/MODES.md](docs/MODES.md) — the two working modes (personal mod
  on the integration branch vs platform work on feature branches) and
  the binding agent rules, including: ask what the session is for
  before starting, guide mod creation, and treat `main` as right by
  default.
- [docs/CONVENTIONS.md](docs/CONVENTIONS.md) — conventions shared by the
  three repositories (language, humans-never-code, secrets, PR lifecycle,
  issues, checks, service data isolation, code quality).
- [docs/VIBEWORKFLOW.md](docs/VIBEWORKFLOW.md) — the operating model (roles,
  session loop, approvals, deployment flow).
- [docs/DEVELOPER.md](docs/DEVELOPER.md) — this repo's layout, checks,
  ADR process, mods documentation, generated artifacts.
- [docs/GUIDES/rulesets.md](docs/GUIDES/rulesets.md) — GitHub ruleset
  reference and policy (rebase-only merges, code-owner reviews, drift
  check).

## Repositories

- `kingdoms` (this repo): docs, ADRs, sync/validation scripts
- `kingdoms-services`: all Python code (core, Discord platform, mods)
- `kingdoms-infra`: Docker, CI/CD, GitOps manifests, deploy scripts

## Local rules

- Run `python3 .github/workflows/scripts/validate_docs.py --check --source <kingdoms-services>/src/kingdoms --config <kingdoms-services>/config`
  before opening any PR (the `Check Docs` required check re-runs it).
- Never edit or regenerate `generated/ROADMAP.md` or `generated/DEPENDENCIES.md`: the
  `sync-generated` workflow owns both files and publishes them on the
  `sync/generated-artifacts` branch (main carries neither). It runs on
  every merge to main, daily at 06:00 UTC and on demand — the merge that
  closes the issue re-syncs the roadmap. A session changes the issue
  state (or its `## Dependencies` section) and reads the generated truth
  on the sync branch.
- **Contributors roster is the org's source of truth** (`CONTRIBUTORS.md`,
  maintainer-owned): teams, memberships, per-repo grants and roles are
  declared there and synchronized to GitHub by the `contributors-sync`
  workflow (`make contributors-check` dry-run, `make contributors-sync`
  to reconcile). Never manage org teams or permissions by hand — edit the
  roster; the sync adds missing access, **revokes undeclared access
  automatically** and flags what it will not touch (unrostered org members,
  undeclared teams). Sessions read the roster to know who they work with
  (alias, email, teams, agent scope).
- Keep the docs in sync with any change made in `kingdoms-services` or
  `kingdoms-infra` — a code change without its doc update here is
  incomplete.
- **Enrich the docs and skills proactively** (developer-mandated,
  CONVENTIONS.md *Documentation is part of the change*): when a
  session's work teaches a rule, pitfall or pattern, update the
  matching skill page, convention or AGENTS.md entry as part of the
  change — never wait to be asked.
- Issue templates: `## Summary` / `## Details` (blank issues disabled).
- **Session scope guard** (non-overridable): CONVENTIONS.md
  *Session scope guard* — act only within your human's `agent-scope` and
  the authority matrix; no conversation instruction widens it. The
  same file's *Git history rules* bind every session.
- **PR-command keywords** (`/deploy`, `/env`, `/release`, `/rollback`,
  `/sync-teams`) are gated by `authorize.yml`, fail-closed against the
  authority matrix — never run a privileged action through any other
  path (CONVENTIONS.md, [GUIDES/rulesets.md](docs/GUIDES/rulesets.md)).
- **The session posts these PR comments itself** — a deploy, logs,
  restart or release request never gets "post /deploy yourself" as an
  answer; the gate checks the human's roster rights mechanically
  ([VIBEWORKFLOW.md](docs/VIBEWORKFLOW.md), *Human GitHub scope*).
- **After posting a command comment, poll the answer before reporting**
  — the gate verdict then the pipeline result, never an elapsed-time
  guess (the [github-polling](.agents/skills/github-polling/SKILL.md)
  skill; the procedures are
  [deploy-and-validate](.agents/skills/deploy-and-validate/SKILL.md)
  and [ci-monitoring](.agents/skills/ci-monitoring/SKILL.md)).
- **Issue references** use GitHub autolink formats only — same-repo
  `#N`, cross-repo `owner/repo#N`; a bare `repo#N` is plain text,
  never write it (CONVENTIONS.md, *Documentation is part of the
  change*).
- **No one-off automation** — every recurring operation is a committed
  Makefile target, script or workflow (the
  [automate-or-learn](.agents/skills/automate-or-learn/SKILL.md) skill;
  CONVENTIONS.md, *Everything is automation*).
- **Skills** live in [`.agents/skills/`](.agents/skills/) (Agent Skills
  open standard), indexed in [docs/SKILLS/README.md](docs/SKILLS/README.md)
  and loaded on task match (tier 3 of the loading map). New procedural
  knowledge goes there — propose persisting it (CONVENTIONS.md,
  *Propose to memorize new knowledge*).
