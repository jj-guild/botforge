---
name: workflow-router
description: Route the human's intention to the right workflow before any work starts — bug report, feature idea, mod creation, mod work, platform code, documentation, or QoL. Use at session start and whenever a human brings a new request, especially a non-technical one who does not know what they may do.
---

# Workflow router — drive the human, don't follow them

The human often does not know what they are allowed to do, or which
path their wish takes. The session knows the platform's workflows:
**it proposes the path, it does not let the human improvise one.**
Advanced users (dev, ops, maintainers per the roster) may take
liberties — a maintainer asking for a direct push is not routed
through the bug workflow; apply judgment, not bureaucracy.

## The route table

| The human says | The workflow | Entry point |
| -------------- | ------------ | ----------- |
| "I want to report a bug" | Bug intake | Issue with the bug template (auto-triage labels it), then a fix branch/PR once confirmed |
| "I have an idea / I want a feature" | Feature shaping | [shape-game-designer-idea](../shape-game-designer-idea/SKILL.md) — challenge, scope, acceptance criteria, then the issue |
| "I want to create a mod" | Mod bootstrap | Sandbox mode ([MODES.md](../../../docs/MODES.md)): `vibe/<alias>/main` branch, draft mod PR, personal env |
| "I want to work on my mod" | Sandbox mode | Stack commits on `vibe/<alias>/main`, the mod PR's checks re-run, deploy on the personal env |
| "I want to fix a bug in the platform" / "I want to add a platform feature" | Pro mode | Feature branch per subject → PR → CODEOWNERS review → [deploy-and-validate](../deploy-and-validate/SKILL.md) |
| "I want to document the project" | Docs change | `kingdoms` repo, PR (docs are code: same lifecycle, same checks) |
| "I want to improve QoL (skills, scripts, tokens, CLI)" | Automation work | [automate-or-learn](../automate-or-learn/SKILL.md) — where the automation belongs, then the same PR lifecycle |
| "Unroll the roadmap" / "what's next?" | Roadmap unrolling | The [roadmap-unroll](../roadmap-unroll/SKILL.md) skill — it runs `scripts/roadmap_next.py` (current lot, ordered work table) and reports status + next steps |

## Unrolling the roadmap

When the human says "unroll the roadmap" / "what's next?", route to the
[roadmap-unroll](../roadmap-unroll/SKILL.md) skill. It runs
`python3 scripts/roadmap_next.py` from the kingdoms repo root — which
determines the current lot (first unfinished `Lot N` milestone) and
prints that lot's issues in work order (dependency wave, then priority
label, then slack/criticality) with issue URL, PR URL if open, priority,
summary, and details (dependents, size, slack) — and the session reports
that table plus a one-line status. The session works **from the generated
truth** (the issues and the artifacts on the sync branch), never from
memory. On "continue" / "go", the skill starts the top todo issue of the
lot in pro mode.

## Rules

- **Ask which workflow applies only when the intention is genuinely
  ambiguous** — then ask with a UI select of concrete options
  ([human-interaction](../human-interaction/SKILL.md)), never a bare
  question.
- **State the route before starting**: one line ("this is a bug
  report on the platform — I'll open an issue, then a fix branch").
- **Never silently upgrade powers**: the mode (sandbox/pro/cowboy) is
  a property of the person + the task ([MODES.md](../../../docs/MODES.md));
  a session never picks a stronger mode on its own.
- **A request outside the human's scope is refused with the pointer**
  to the roster entry and the human click that covers it
  (CONTRIBUTORS.md authority matrix).
- **Deploy, logs, restart, release requests route through the PR
  comments** (`/deploy`, `/env`, `/release`) — the session posts
  them itself and polls the answer
  ([deploy-and-validate](../deploy-and-validate/SKILL.md),
  [github-polling](../github-polling/SKILL.md)). **kingdoms-services
  PRs only**: infra PRs have no `/deploy` — their CI boots the real
  stack from the branch, and the agent validates that evidence instead.
