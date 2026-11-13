# Mod catalogue

One page listing **every mod idea** on the platform, at its current maturity
level — the entry point for the game designers to **browse, compare and
prioritize** ideas. Each entry is one row: maturity, one-line description,
categories, and links to the detailed docs/issues.

The repo is the memory: the catalogue row only summarizes; the linked issue or
doc holds the decisions.

## Maturity levels

A mod moves up one level at a time; each level has an entry requirement.

| Level | Meaning | Entry requirement |
|-------|---------|-------------------|
| **1 — Vague idea** | A raw game-designer idea, no shaping yet | None — write the row |
| **2 — Shaped** | Challenged into an automatable, explainable issue (self-contained, checkable acceptance criteria) | A tracking issue in `botforge-services` |
| **3 — Specified** | Rules, environment and workflows written under `docs/MODS/<mod>/` (TEMPLATE-based) | Mod docs directory |
| **4 — Scoped** | Picked by a milestone: implementation sliced into sub-tasks with dependencies | Sub-task issues + a milestone |
| **5 — Developed** | Implemented, tested, shipped in a release | Released version |

Categories: `game` (gameplay), `social` (community), `organizer` (event/orga
tooling), `platform` (bot/infra capability), `money` (touches payments —
requires the [monetization plan](../PLANS/monetization.md) gate).

## Catalogue

| Mod | Maturity | Description | Categories | Details |
|-----|----------|-------------|------------|---------|
| register | 5 — Developed | Player onboarding: DM name+game workflow, auto game-role assignment, admin notification | platform, social | [register/](register/), botforge-services#14 |
| ladder | 4 — Scoped | Competitive 1v1 ladders: queue + blossom matchmaking, map pick, match lifecycle, pluggable rating, leaderboard (AoE2 first) | game | [ladder/](ladder/), botforge-services#15 (core #134, surface #135) |
| kingdoms | 3 — Specified | Territory-conquest meta-game around AoE2 (Season II reference): seasons, weekly events, attacks/defenses, tech economy, diplomacy | game | [kingdoms/](kingdoms/), botforge#129, reference doc |
| coaching | 2 — Shaped | Pro feedback marketplace: coach pool (level/reputation/free price), booking via dynamic views, per-coach request pool, session workspace (thread + temp voice), cross ratings & reputation, indicative commission ledger (no payment handling in v1) | social, money | botforge-services#151 (monetization: [PLANS/monetization.md](../PLANS/monetization.md) Axis C/D; readiness #154) |
| tournament (80%) | 2 — Shaped | Operator-assisted tournaments: sign-ups, seeding, brackets, disputes | organizer | botforge-services#120 |
| tournament (full-auto) | 2 — Shaped | Fully automated tournaments: auto rounds, auto seeding, scheduled seasons | organizer | botforge-services#121 |
| clans | 5 — Developed | Clan management: free creation, mutual-agreement admissions (criteria + admin approval), leader/officer/member roles, dashboard with member counts, per-clan forum — reference example (mod-intake skill) | social | [clans/](clans/), botforge-services#19, botforge-services#267 |
| admin | 2 — Shaped | Discord-first admin surface: game data, map pools, seasons, rating admin | platform | botforge-services#21, botforge-services#136 |
| /drasah | 4 — Scoped | Medieval greeting command | social | botforge-services#148 |
| friends & feedback (Epic J) | 2 — Shaped | Friends graph, private teammate micro-feedback (matching-only), avoid-lists, graduated sanctions with appeals | social | botforge#118 |
| presence (Epic E) | 2 — Shaped | Real-time player availability | platform | botforge#114 |
| team maker (Epic F) | 2 — Shaped | LFG tickets, balanced teams, captain drafts | game | botforge#115 |
| ratings & stars (Epic D) | 2 — Shaped | Glicko-2, rating history, badges | platform | botforge#113 |
| game data & drafts (Epic C) | 2 — Shaped | Maps, map pools, civs, DraftProvider | platform | botforge#112 |
| tournament machine (Epic B) | 2 — Shaped | Sign-ups, seeding, brackets, disputes (post-pivot epic) | organizer | botforge#111 |
| core domain (Epic A) | 2 — Shaped | Players, seasons, matches, scoring, entitlements | platform | botforge#110 |
| vibe-coding mod platform (Epic K) | 2 — Shaped | Assisted, UI-based mod co-construction for designers and community | platform | botforge#136, [PLANS/vibe-mod-platform.md](../PLANS/vibe-mod-platform.md) |
| report (/report) | — Dropped | Match reporting command — dropped, rationale in the issue | game | botforge-services#18 |

Levels legend: 1 vague · 2 shaped · 3 specified · 4 scoped · 5 developed.

## Prioritization notes

- **ladder** and **kingdoms** carry the v0.4.0 milestone — highest priority.
- **coaching** is shaped and ready to be picked up by a milestone; its
  monetization axes are parked ([PLANS/monetization.md](../PLANS/monetization.md)),
  so v1 needs no payment work.
- Mods with a `money` category require the monetization gate (community
  consultation + ADR) **before** any implementation.

## See also

- [README.md](README.md) — how mods work (config, registry, lifecycle)
- [../ROADMAP.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md) — global roadmap (issues, milestones, waves)
- [TEMPLATE/](TEMPLATE/) — template for new mod documentation
