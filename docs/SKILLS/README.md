# Skills

The Kingdoms agent skills moved to the **Agent Skills open standard**
([agentskills.io](https://agentskills.io/specification)): one directory per
skill with a `SKILL.md` file (YAML frontmatter + Markdown instructions),
discovered by agent runtimes (Mistral Vibe Code among others) via
progressive disclosure — the session loads only the skill names and
descriptions at startup, and the full instructions when a task matches.

**Location:** [`.agents/skills/`](../../.agents/skills/) at the repo root
(the `kingdoms` repo carries the shared skills; a repo may also carry its
own repo-local skills — `kingdoms-services` ships `discord-bot-docs` in
its `.agents/skills/` — every future session discovers both).

**Loading model:** the agent runtime discovers the skills through this
index and the frontmatter (name + description) at startup, and loads a
skill's full `SKILL.md` **only when a task matches its description** —
the modular layer of the instruction loading map (AGENTS.md). Humans
browse the table below to see what the agents know how to do.

| Skill | Purpose |
| ----- | ------- |
| [automate-or-learn](../../.agents/skills/automate-or-learn/SKILL.md) | Where each automation belongs; the propose-to-memorize rule |
| [human-interaction](../../.agents/skills/human-interaction/SKILL.md) | How the session talks to its human — UI-select asks, live plan, context links, aliases |
| [diagnose-deploy](../../.agents/skills/diagnose-deploy/SKILL.md) | Diagnose a stuck/pending deploy before blaming the runner |
| [generated-artifacts](../../.agents/skills/generated-artifacts/SKILL.md) | The generated artifacts (ROADMAP, DEPENDENCIES, pydoc): single writer, drift detection, preview |
| [troubleshooting](../../.agents/skills/troubleshooting/SKILL.md) | The platform's failure memory — check it before diagnosing, add an entry when a fix lands |
| [deploy-and-validate](../../.agents/skills/deploy-and-validate/SKILL.md) | Deploy a PR to test and validate it before ready |
| [release-flow](../../.agents/skills/release-flow/SKILL.md) | Cut a release (tag, GitHub release, prod pin) on request |
| [shape-game-designer-idea](../../.agents/skills/shape-game-designer-idea/SKILL.md) | Turn a game designer idea into an automatable issue |
| [ci-monitoring](../../.agents/skills/ci-monitoring/SKILL.md) | Monitor CI, find root causes, push focused fixes |
| [github-polling](../../.agents/skills/github-polling/SKILL.md) | Poll GitHub statuses every 10-30s instead of a fixed worst-case sleep |
| [discord-ui](../../.agents/skills/discord-ui/SKILL.md) | Build any Discord message through the kingdoms-services UI SDK — bricks, archetypes, guards, i18n |

This directory is kept as the documentation entry point; do not add new
skill pages here — create `.agents/skills/<name>/SKILL.md` instead.
