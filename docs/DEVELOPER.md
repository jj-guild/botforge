# kingdoms — developer guide

`kingdoms` is the **source of truth** of the Kingdoms Discord bot platform:
architecture, operating workflow, ADRs, mods documentation, roadmap and
dependency graph. It contains no runtime code — only docs and the sync /
validation scripts that maintain them.

Read [docs/VIBEWORKFLOW.md](VIBEWORKFLOW.md) for the operating model and
[docs/CONVENTIONS.md](CONVENTIONS.md) for the shared conventions. This page
covers what is specific to working *in this repo*.

## Layout

| Path | Content |
| ---- | ------- |
| `AGENTS.md` | Short agent entry point (points here) |
| `docs/ARCHITECTURE.md`, `docs/architecture/` | System overview, per-area deep dives |
| `docs/VIBEWORKFLOW.md` | Operating model (roles, session loop, approvals) |
| `docs/PROCESS.md`, `docs/WORKFLOWS.md` | Delivery process, CI/CD workflows |
| `docs/DECISIONS/` | Architecture decision records |
| `docs/MODS/<mod-name>/` | Mods documentation (`README.md`, `RULES.md`, `ENVIRONMENT.md`) |
| `docs/GUIDES/` | Audience entry points: mod developer, game provider developer, vibe coder (AI session), game designer |
| `.agents/skills/` | Agent Skills (open standard, `SKILL.md` per skill): automate-or-learn, diagnose-deploy, generated-artifacts, deploy-and-validate, release-flow, shape-game-designer-idea, ci-monitoring |
| `docs/CONVENTIONS.md` | Conventions shared by the three repos |
| `generated/ROADMAP.md`, `generated/DEPENDENCIES.md` | Generated artifacts — never edit manually |
| `scripts/` | `validate_docs.py`, `sync_roadmap.py`, `sync_dependencies.py`, `session_check.py` |
| `templates/mod-template/` | Template for a new mod's documentation |

## Checks

Anyone can run the local checks with public clones only (this repo and
`kingdoms-services` side by side, no credentials):

```bash
python3 .github/workflows/scripts/validate_docs.py --check \
  --source <kingdoms-services>/src/kingdoms \
  --config <kingdoms-services>/config
```

The full session checklist (docs validation + roadmap drift +
dependency-graph drift) runs with `make session-check`; the synced
artefacts regenerate with `make sync-artifacts` (commit the result to the
open PR branch).

It validates: mod docs completeness, Python docstrings in the
kingdoms-services source, Mermaid block syntax. Fail-closed: it refuses to
run without the kingdoms-services source/config. The `Check Docs` required
check re-runs it on every PR — it must pass before opening a PR.

## Writing rules

- Mermaid diagrams must use **GitHub-compatible syntax**: quote node
  labels containing special characters like `->` or `{}`; never put colons
  inside unquoted labels.
- Keep `docs/` in sync with any change made in `kingdoms-services` or
  `kingdoms-infra`; the docs describing a change are updated in the same
  session, not later.

## ADR process

Any major architecture change gets an ADR in `docs/DECISIONS/`:

1. Create the ADR's tracking issue first, and check the numbers already
   reserved by other open issues and in-flight PRs (parallel sessions are
   common); never pick a number already in use.
2. **Status**: a decision shaped and challenged collaboratively with the
   developer during a session is **Accepted** on creation (the ADR body
   records the co-construction); an ADR drafted unilaterally by the agent
   starts as **Proposed** until the developer reviews it.

## Mods documentation

A new mod's documentation lives in `docs/MODS/<mod-name>/` and follows the
template in `templates/mod-template/` (`README.md`, `RULES.md`,
`ENVIRONMENT.md`). `validate_docs.py` fails when a mod declared in
`kingdoms-services/config/mods/` is missing its doc directory or required
files.

## Generated artifacts

`generated/ROADMAP.md` and `generated/DEPENDENCIES.md` are regenerated, never hand-edited:

- Change the **issue state** or its `## Dependencies` section instead, then
  preview drift with the sync scripts ([Generated
  artifacts](../.agents/skills/generated-artifacts/SKILL.md)) — the
  single-writer workflow publishes them; a session never commits the
  regenerated files to your open PR branch.
- Statuses needing human judgment (`in-progress`, `blocked`) are set
  manually and preserved by the script.
- Priorities (`priority/P0-P3` labels) come from critical-path analysis
  maintained by `.github/workflows/scripts/sync_dependencies.py` — do not set them by hand
  unless the analysis is wrong.

## Testing strategy (summary)

Full strategy: [docs/architecture/testing.md](architecture/testing.md).
Two complementary Discord test doubles live in `kingdoms-services` — pick
the right depth:

- **MockDiscord** (mock objects, `kingdoms-services` `tests/mocks/`) for
  adapter and UI-builder unit tests; permissive by design, never validates
  the discord.py glue.
- **SimCord** (behavioral simulator, dev-dependency `simcord[pytest]` in
  `kingdoms-services`) for journeys through the real discord.py dispatch:
  slash commands, buttons, selects, modals, permissions, timeouts,
  Components V2. Drive the bot as a user; never call a command callback
  directly; no token, no network, no sleeps.

A doc change describing testing must keep this page and
`docs/architecture/testing.md` consistent.
