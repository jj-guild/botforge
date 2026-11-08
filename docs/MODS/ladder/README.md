# Ladder mod

> Rewritten from the JeanJack V2.0 reference
> ([../PLANS/reference/ladder-1v1-jeanjack-v2.md](../../PLANS/reference/ladder-1v1-jeanjack-v2.md))
> for BotForge v0.4.0. The reference is the **functional source of truth**
> (rules, state machine, data model, intents, acceptance criteria — its
> §1–§9). This directory adapts it to the BotForge stack: process split
> (ADR-0020), seams (ADR-0011), i18n, seasons, pluggable rating.

## Purpose

A per-ladder competitive 1v1 system: registration, matchmaking queue +
direct invites, map pick from a season pool, match lifecycle via DM and
match surfaces, result reporting/confirmation, rating, leaderboard. AoE2
is the first game; the core is game- and platform-agnostic (reference §6).

## Architecture placement (ADR-0020)

| Concern | Location |
|---|---|
| Ladder domain core (rules, rating, matchmaking, state machine, persistence) | `mods/ladder` module in **svc-core** |
| Discord surface (views, modals, buttons, intents rendering, DM delivery) | ladder surface in **bot-discord** |
| Game data / results / realtime events | `games/aoe2` module in svc-core + **ext-librematch** / **ext-aoe2lobby** provider processes |
| Communication | gRPC seams (ADR-0020 annex) |

Non-negotiables (unchanged from the reference §0/§6): no Discord or game
IDs in the mod's MongoDB collections; persistent message IDs live in the
platform message registry by `(platform, key, entity_id)`; idempotent
state transitions; declared provider capabilities with clean degradation.

## Concepts

- **Ladder**: one config per community (name, `game_key`, settings —
  reference §2 `ladders`).
- **Season**: config entity (start, end, `reset_ratings` bool). Activating
  a season = transactional map-pool switch (`active_map_pool_id` +
  `map_pool_history`), per reference §4. The AoE2 ladder is seasonal
  *without* rating reset.
- **Queue + invites**: matchmaking with reciprocal Elo-window
  compatibility widening over wait time (base 60, +20 / 15 s, cap 400 —
  admin-tunable), **maximum matching via Edmonds' blossom** (no pairable
  player left alone when a complete matching exists), plus direct
  invites (validity 3/5/15/30 min, optional map).
- **Match lifecycle**: `CREATED → READY → STARTED → (LOBBY → GAME) →
  RESULT_PENDING → REPORTED → COMPLETED` (+ `CANCELED`), full rules and
  AoE2 lobby-closed grace period in reference §5.2.
- **Rating**: pluggable `RatingSystem` seam, admin-selectable per ladder —
  **elo** (reference §3 verbatim) and **glicko2** (Glickman 2013: RD,
  volatility, inactivity decay, provisional-by-RD). Invariants
  rating-system-agnostic: single application at REPORTED→COMPLETED,
  `rating_history` as source of truth, admin corrections with
  compensation.
- **Maps & pools**: game-data catalog (maps, civs, rules) + map pools,
  optionally bundled into map packs; map pick = weighted random
  (fav-boosted) minus admin+player bans, snapshot frozen per match.
- **Intents**: the core emits notification intents (reference §7.2
  catalogue); the Discord surface renders them (embed/DM/ephemeral),
  i18n-owned.

## Discord surface (adaptation of reference §7)

- Category "Ladder 1v1" + surfaces: `#play`, `#leaderboard`, `#matches`,
  `#players`, `#admins` — provisioned via ChannelService (mod-declared
  keys, botforge-services#26/#57).
- Roles: "Ladder 1v1 admin", "Ladder 1v1 player" (RoleService).
- Views: PlayView, QueueView, LeaderboardView, MatchView, PlayerView,
  AdminView; modals per reference §7.4. Persistent views survive restarts
  (botforge-services#122); every interaction respects the 3-second rule
  (defer, then followup).
- Admin surface: full game-data CRUD (maps/civs/rules), map pools &
  packs, settings, rating adjustments, audit — **Discord-first**, no dev
  action required.

## Configuration options

Settings live on the `ladders` document (reference §2 defaults),
including: matchmaking thresholds/ticks, rating system choice & Elo
constants, map fav/ban counts, surface cleanup delay, auto-confirm of
reliable provider reports. All admin-editable from Discord. Mod-level
YAML (`config/mods/ladder.yaml`) declares: `enabled`, declared channels,
declared roles, default settings template.

## Environment

See [ENVIRONMENT.md](ENVIRONMENT.md) for channels/roles/database/redis
requirements and [RULES.md](RULES.md) for the authoritative rules
summary (both defer to the reference for the exhaustive statements).

## Acceptance

Reference §9 criteria apply verbatim (game-independence with a mocked
provider, platform-independence via the message registry, matchmaking
timing thresholds, single rating application, Discord-only admin
management, idempotent transitions, non-admin invisibility).
