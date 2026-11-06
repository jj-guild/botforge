[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)

# Kingdoms

Kingdoms is a modular Discord bot platform, built and maintained through a
vibe-coding workflow. It is the successor of JeanJack.

This repository is the **source of truth** for the project: it hosts all
architecture documentation, game workflows, mods documentation (rules and
environment), Architecture Decision Records (ADRs), and auto-generated
development docs. No application code lives here.

## Repositories

| Repository | Purpose |
| ---------- | ------- |
| [kingdoms](https://github.com/merlin-pinpin-org/kingdoms) (this repo) | Documentation: architecture, workflows, ADRs, mods docs, generated dev docs |
| [kingdoms-services](https://github.com/merlin-pinpin-org/kingdoms-services) | All Python code: generic core, Discord platform, mods, YAML configs |
| [kingdoms-infra](https://github.com/merlin-pinpin-org/kingdoms-infra) | Docker, CI/CD, GitOps manifests, deployment scripts |

## Key principles

1. **Platform-agnostic core** — game logic lives in
   `kingdoms-services/src/kingdoms/core/`, behind the `IPlatform`
   interface. Discord is one implementation
   ([ADR-0001](docs/DECISIONS/001-multi-platform-architecture.md))
2. **Modular mods** — each game mode is a self-contained mod declaring its
   channels, roles, and workflows via `ModRegistry`
   ([docs/MODS/](docs/MODS/),
   [docs/architecture/mods.md](docs/architecture/mods.md))
3. **MongoDB only** (no relational database) for durable data, plus
   **Redis** for cache, hot state, and distributed locks
   ([ADR-0004](docs/DECISIONS/004-mongodb-schema-design.md),
   [ADR-0005](docs/DECISIONS/005-redis-state-management.md))
4. **Full-stack testing** — `MockDiscord` provides an in-memory
   `IPlatform` simulation; no test ever touches the real Discord API
   ([docs/architecture/testing.md](docs/architecture/testing.md))
5. **i18n by default** — English is the default locale, French is
   available; every user-facing string comes from YAML locale files
   ([ADR-0008](docs/DECISIONS/008-i18n-system.md))

## Documentation structure

```
kingdoms/
├── README.md                      # This overview (the human entry point)
├── AGENTS.md                      # Rules for AI coding agents (the agent entry point)
├── docs/
│   ├── INDEX.md                   # The router: question → page
│   ├── ARCHITECTURE.md            # Technical architecture (Mermaid diagrams)
│   ├── GAME-DESIGN.md             # The game designer's guide (English)
│   ├── GAME-DESIGN.fr.md          # The game designer's guide (français)
│   ├── WORKFLOWS.md               # Game workflows (registration, ladder, ...)
│   ├── SKILLS/README.md           # The agent skills index
│   ├── MODS/                      # Mods documentation
│   │   ├── register/              # Registration mod (rules, environment)
│   │   ├── ladder/                # Ladder mod (rules, environment)
│   │   └── TEMPLATE/              # Template referenced by new mod docs
│   └── DECISIONS/                 # Architecture Decision Records (ADR)
├── .agents/skills/                # Agent skills (one directory per skill, SKILL.md)
├── .github/workflows/             # Docs generation and validation workflows
├── scripts/                       # Doc generation and validation scripts
└── templates/                     # Reusable templates (mods, ADRs)
```

## Documentation map — where to look

**For humans:** start at [docs/INDEX.md](docs/INDEX.md) — the
question → page router ("I am… / I want to… — where do I look?").
The main entries:

- [docs/GAME-DESIGN.md](docs/GAME-DESIGN.md) — **the game designer's guide**
  ([français](docs/GAME-DESIGN.fr.md)): how to describe an idea, follow its
  delivery, test it in Discord, read the bot's `/status` — no tooling
  involved
- [docs/CONVENTIONS.md](docs/CONVENTIONS.md) — the binding rules every
  contributor (human or agent) follows
- [docs/VIBEWORKFLOW.md](docs/VIBEWORKFLOW.md) — the operating model
  (roles, session loop, approvals, deployment flow)
- [docs/MODES.md](docs/MODES.md) — the working modes (sandbox, pro, cowboy)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) +
  [docs/DECISIONS/](docs/DECISIONS/) — the architecture and its decisions
- [docs/MODS/](docs/MODS/) — mods documentation
- [docs/SKILLS/README.md](docs/SKILLS/README.md) — the agent skills index
  (what each skill is for; agents load a skill's full instructions only
  when a task matches)

**For AI agents:** start at [AGENTS.md](AGENTS.md) — the PRIORITY 0 rules
and the instruction loading map.

## Automation

Generated artifacts (`generated/ROADMAP.md`,
`generated/DEPENDENCIES.md`) are owned by the `sync-generated` workflow:
the **single writer**, which publishes them on the
`sync/generated-artifacts` branch (never on `main`, never in a PR).
Sessions only *preview* drift with the
[Update roadmap](.agents/skills/update-roadmap/SKILL.md) and
[Update dependencies](.agents/skills/update-dependencies/SKILL.md)
skills — the output is never committed by hand.

Generated technical documentation (pydoc) lives in `kingdoms-services`
([`docs/DEVELOPMENT/pydoc`](https://github.com/merlin-pinpin-org/kingdoms-services/tree/main/docs/DEVELOPMENT/pydoc)),
next to the sources it documents; a dedicated workflow checks its freshness
on every PR of that repo.

The sync scripts read the issues of `kingdoms-services` and
`kingdoms-infra` through `gh api`; all three repositories are public, so no
credentials are needed. They fail closed when a repository is unreadable.
The `Check Docs` workflow (`scripts/validate_docs.py`) runs on every PR.

## Contributing

You do not need an AI agent to contribute to Kingdoms. The human path:

1. Pick or create an issue (templates are mandatory; blank issues are
   disabled).
2. Clone this repo and [`kingdoms-services`](https://github.com/merlin-pinpin-org/kingdoms-services)
   side by side, create a branch from `main`.
3. Edit the documentation, then run `make session-check
   KINGDOMS_SERVICES=../kingdoms-services` — the same validation CI runs
   on every PR.
4. If you created or closed issues, regenerate the synced artifacts with
   `make sync-artifacts` (`ROADMAP.md` and `docs/DEPENDENCIES.md` are
   generated — never edit them by hand).
5. Open a pull request; the maintainer merges.

Documentation must be in **English**; game-related examples may be in
French for i18n purposes.

The project is primarily built through the vibe-coding workflow (an AI
agent implements issues on `vibe/<short-slug>` branches — see
[AGENTS.md](AGENTS.md)), but human contributions follow exactly the same
checks. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide and the
CLA process.

## License

Kingdoms is licensed under the [GNU Affero General Public License v3.0](LICENSE).
AGPL-3.0 was chosen so that any fork operated as a service must publish its
modified source to its users (§13) — a direct deterrent for competitive
privatization, since a bot is inherently a network service. External
contributors sign the [CLA](CLA.md), which preserves a relicensing option for
the project owner.
