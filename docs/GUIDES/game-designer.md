# Guide — Game designer

You design the features and rules; the AI agent builds them; the
developer reviews. You never code, never run scripts, never touch files
— you design, challenge, and validate in Discord.

## How your ideas become features

1. **Describe the feature** to the AI agent (rules, flows, channels,
   roles, edge cases). The agent challenges what is hard to automate
   and proposes simpler alternatives — expect back-and-forth; that is
   the platform working as intended.
2. **Agree on the rules**: they get written into `docs/MODS/<mod>/`
   (the source of truth you can read and re-read later).
3. **The agent builds** the issue → PR → test environment pipeline.
4. **You validate in Discord** on the test environment: click through
   the real flows (commands, buttons, DMs) and report what feels wrong.

## What you manage yourself (Discord-first)

Once a mod is live, its day-to-day management is **yours, from Discord**:
settings, map pools and game data, seasons, disputes — admin commands
and surfaces. If an admin task needs a developer, that is a bug:
report it, do not work around it.

## Design rules of thumb

- **Prefer automatable rules**: "match when ratings are close" beats
  "an admin pairs players by feel". The agent will push back on
  anything manual.
- **Explicit numbers**: thresholds, durations, bonuses — give concrete
  values (defaults exist; everything is tunable later from Discord).
- **Think in seasons/rotations**: content changes, player identity and
  ratings persist (or reset — say which, per season).
- **Degradation**: what should happen when the game data source is
  down? Design the fallback, or accept the default (manual
  confirmation everywhere).
- Look at [MODS/ladder](../MODS/ladder/README.md) for a fully worked
  example (rules, environment, admin surface).

## Where things are documented (for your reference)

- Your features' rules: [docs/MODS/](../MODS/README.md) — per-mod
  README/RULES/ENVIRONMENT, written for a non-developer.
- The big picture: [GAME-DESIGN.md](../GAME-DESIGN.md) (vision,
  phases, modules) — you own this document.
- Progress: [ROADMAP.md](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md).

## Limits on purpose

The developer approves architecture and reviews PRs; some decisions
(rating algorithms, process split, contracts) are the developer's
call. When your request touches those, the agent will say so and bring
the question to the developer — it is not a refusal of your feature,
only of a specific implementation.
