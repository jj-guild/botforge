# INDEX — find the answer without reading everything

You are an agent session or a human contributor with a question. This
page routes you to the answer. Read this page, not the whole docs tree.

## "I am… / I want to… — where do I look?"

| Question | Answer lives in |
| --- | --- |
| Who am I working with? Who may do what? | [CONTRIBUTORS.md](../CONTRIBUTORS.md) — the roster (login, alias, email, teams, roles, agent scope) + the authority matrix |
| What are the universal rules every session follows? | [CONVENTIONS.md](CONVENTIONS.md) — working language, git identity, scope guard, automation, PR lifecycle, docs quality |
| What are the code architecture rules (data isolation, write atomicity, DRY/KISS)? | [CONVENTIONS.md](CONVENTIONS.md) *Service data isolation*, *Code quality* + [architecture/core.md](architecture/core.md) *MongoDB write atomicity* + [ADR-0021](DECISIONS/021-architecture-five-rules.md) |
| Something declarative (channels, labels, emojis, flags, views, tunables) — code or config? | Config — [CONVENTIONS.md](CONVENTIONS.md) *Configuration over code* + `botforge-services/config/` (`views.yaml`, `mods/<mod>.yaml`, locales) |
| How does the platform work end to end (roles, sessions, deploys)? | [VIBEWORKFLOW.md](VIBEWORKFLOW.md) — the operating model |
| Which working mode applies to me (sandbox, pro, cowboy)? | [MODES.md](MODES.md) — branch strategy, review gate and powers per mode |
| What does each person click (and nothing else)? | [VIBEWORKFLOW.md](VIBEWORKFLOW.md) *Human GitHub scope* + [GUIDES/rulesets.md](GUIDES/rulesets.md) |
| What is the process for dev / test deploy / release / prod? | [PROCESS.md](PROCESS.md) |
| Which CI/CD workflows exist and what do they do? | [WORKFLOWS.md](WORKFLOWS.md) |
| Which PR-comment commands exist (`/deploy`, `/logs`, `/restart`, `/rollback`, `/dump-db`, `/release`…)? | [CONTRIBUTORS.md](../CONTRIBUTORS.md) authority matrix (who) + [WORKFLOWS.md](WORKFLOWS.md) (how) |
| How do I deploy something to test? | [PROCESS.md](PROCESS.md) §Test deployment + the `deploy-and-validate` [skill](../.agents/skills/deploy-and-validate/SKILL.md) |
| How do I debug a failed deployment / read the test logs? | `/logs [env] [--service S] [--since 30m]` PR comment (see [WORKFLOWS.md](WORKFLOWS.md)) + the `diagnose-deploy` [skill](../.agents/skills/diagnose-deploy/SKILL.md) |
| How do I release / cut a version? | [PROCESS.md](PROCESS.md) §Release + the `release-flow` [skill](../.agents/skills/release-flow/SKILL.md) |
| I want to flag an arch discussion / POC (pre-roadmap, committee territory) | Label it `arch-discussion` (or `poc`) — excluded from the lots, listed in the roadmap's "Pre-roadmap" section; see [CONVENTIONS.md](CONVENTIONS.md) *Off-roadmap labels* |
| How do I shape a game-designer idea into an issue? | the `shape-game-designer-idea` [skill](../.agents/skills/shape-game-designer-idea/SKILL.md) |
| What is the architecture? Why was X decided? | [ARCHITECTURE.md](ARCHITECTURE.md) + [DECISIONS/](DECISIONS/README.md) (ADRs) |
| What is the long-term infra vision / hosting plan? When does the architecture committee meet? | [architecture/committee.md](architecture/committee.md) — the committee home, its kickoff inventory & surface map, plus [vision.md](architecture/vision.md), [topology.md](architecture/topology.md), [capacity.md](architecture/capacity.md) |
| How are salons/pinned menus/admin panels managed at runtime? | [architecture/channels.md](architecture/channels.md) — id-based resolution, pinned-view contract, mod types & admin surfaces, core/mods split |
| How do I write/update a mod's docs? | [DEVELOPER.md](DEVELOPER.md) + [MODS/](MODS/README.md) |
| Who reviews my PR? | [GUIDES/rulesets.md](GUIDES/rulesets.md) (rulesets) + CODEOWNERS in the target repo |
| I am a game designer / mod dev / provider dev / vibe coder | [GUIDES/](GUIDES/README.md) — the per-role guides |
| I want to join the platform — what do I need? | [GUIDES/join-the-platform.md](GUIDES/join-the-platform.md) — GitHub + Mistral accounts, connector, runner, CLA |
| What is the roadmap? What depends on what? | [generated/ROADMAP.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md) + [DEPENDENCIES.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/DEPENDENCIES.md) — both **generated**, never edited |

## The three laws (if you read nothing else)

1. **The docs are the single source of truth** — keep them simple,
   non-redundant, up to date; one home per rule, links elsewhere.
2. **Humans never code** — everything technical is done by agents or
   CI; human actions are GitHub web UI clicks only.
3. **Everything is automation** — the second repetition of any
   operation becomes a committed script, target or workflow.

## Reading order for a fresh agent session

1. [CONTRIBUTORS.md](../CONTRIBUTORS.md) — who you work for (scope guard)
2. [CONVENTIONS.md](CONVENTIONS.md) — the rules
3. [VIBEWORKFLOW.md](VIBEWORKFLOW.md) — the model
4. The repo's `AGENTS.md` — the local mandates
5. This index when a question comes up — never the whole tree
