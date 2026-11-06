---
name: shape-game-designer-idea
description: Turn a game designer's feature idea into an automatable, simply explainable GitHub issue (challenge, scope, acceptance criteria, dependencies) before implementing. Use whenever the game designer brings a new idea, rule change, or environment request.
---

# Shape a game designer's idea

The game designer is full of ideas and motivated, but does not develop:
the agent challenges and shapes every idea toward behavior that is
**automatable** and **explainable simply**, then commits it as a
self-contained GitHub issue. The repo is the platform's memory — the idea
lives in an issue, never only in a conversation.

## Procedure

1. **Challenge the idea** — ask (in plain language, in the working
   language of the session):
   - What does the player see/experience? (the observable behavior)
   - Who can do it, where, how often? (gating, scope, cooldowns)
   - What happens in edge cases — offline player, missing role, tie,
     cancellation? (fail-closed behavior)
   - Is it a rule (kingdoms docs), a bot feature (kingdoms-services),
     an environment change (kingdoms-infra), or a mix?
2. **Simplify toward automation** — prefer:
   - deterministic rules over judgment calls (no "the bot decides");
   - explicit states over free text (a workflow enum, not a chat);
   - data over code when possible (config YAML, mods as declared
     registries — a new channel/role category is a config change, not a
     code change);
   - explaining the rule in one sentence a player would understand.
3. **Write the issue** in the relevant repo, following its template
   (`## Objective` / `## Context` / `## Specifications` /
   `## Acceptance criteria` / `## Dependencies` in kingdoms-services and
   kingdoms-infra; `## Summary` / `## Details` in kingdoms). The issue must
   be self-contained: future sessions have no conversation memory.
   - Acceptance criteria are **checkable** (a human can tick each box
     after testing in Discord).
   - `## Dependencies` uses task-list checkboxes with repo-qualified
     references; set `size/*` and `priority/*` labels (the dependency sync
     fails without them).
4. **Wire it**: the roadmap/dependency artifacts pick the issue up at the
   next sync (see the
   [generated-artifacts](../generated-artifacts/SKILL.md) skill).
5. **Explain back**: restate the shaped rule to the game designer in one
   short paragraph before implementing — the game designer validates the
   *rule*, then the developer validates the *implementation*.

## Anti-patterns to push back on

- "The bot should be smart about it" → ask for the exact rule instead.
- Scope that requires reading Discord message content without a clear
  rule → challenge (privacy, complexity, failure modes).
- One giant feature → decompose into issues with explicit dependencies
  (the dependency graph computes the waves and the critical path).
- A rule that cannot be summarized simply → usually two rules, or the
  wrong rule.
