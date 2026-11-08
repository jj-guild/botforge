# Ladder mod — Environment

> Adapted from the JeanJack V2.0 reference (§2, §7.1) to the BotForge
> stack. Exhaustive field-level definitions live in the
> [reference](../../PLANS/reference/ladder-1v1-jeanjack-v2.md).

## Discord requirements

- Bot permissions: send messages, send DMs, view channels, manage
  messages, manage roles (for ladder roles), use components v2.
- Mod-declared surfaces (provisioned by the core via ChannelService,
  keys resolved per reference §7.1):
  - `ladder:play` — persistent menu message (PlayView)
  - `ladder:leaderboard` — persistent standings message
  - `ladder:matches` — match feed / match surfaces timeline
  - `ladder:players` — player sheets
  - `ladder:admins` — admin notifications (disputes, alerts)
- Roles declared by the mod (RoleService): `ladder_player`,
  `ladder_admin`.
- Persistent message IDs are stored in the **platform message registry**
  by `(platform, message_key, entity_id)` — never in the mod's
  collections.

## Process placement (ADR-0020)

- Domain core: `mods/ladder` in **svc-core** (owns the collections
  below).
- Discord surface: in **bot-discord** (talks to svc-core over gRPC).
- Game data/results: **ext-librematch** / **ext-aoe2lobby** provider
  processes (gRPC streams + calls), behind the `games/aoe2` module.

## Database requirements (MongoDB, mod-owned)

| Collection | Content |
|---|---|
| `ladders` | Ladder config: owner_ref, game_key, settings, active_map_pool_id, season fields |
| `players` | Per-ladder players: rating (+ system block: RD/volatility for glicko2), W/L/streak, fav/ban map refs, queue state |
| `matches` | Match records, state machine fields, game block (opaque match_ref, participants, factions), rating_applied |
| `rating_history` | Source of truth for every rating change (MATCH_RESULT / MANUAL_ADJUSTMENT / RESET) |
| `maps` / `map_pools` / `map_pool_history` | Game-data catalog entities scoped by game_key |
| `admin_audit` | Every admin mutation with payload diff |

Indexes: unique `(ladder_id, user_id)` on players; unique
`(game_key, name)` on maps (excluding archived); unique sparse
`game.match_ref` on matches; `(ladder_id, status)` and
`(ladder_id, rating)` on matches/players query paths.

## Redis keys

| Key | Type | Role |
|---|---|---|
| `ladder:{id}:queue` | ZSET (score = queued_at) | Queue mirror of `players.queued_at` |
| `ladder:{id}:mm_lock` | SET NX EX | Matchmaking pass lock |
| `ladder:{id}:settings` | HASH | Settings cache (invalidated on update) |
| `ladder:{id}:rank` | ZSET (score = rating) | Fast leaderboard |

## Background tasks (svc-core)

| Task | Cadence | Role |
|---|---|---|
| Matchmaking tick | `matchmaking_tick_interval` (default 5 s) | Pairing + deadline expiry, under lock |
| Surface cleanup | 300 s | Ask platform to delete old finished match surfaces |
| Auto-report | on-demand post RESULT_PENDING (5 s × 30 s) | Poll provider for result |
| Rank recompute | after confirmation + 60 s | Leaderboard ZSET |

## Configuration

Mod YAML (`config/mods/ladder.yaml`): `enabled`, declared channels/roles,
default settings template. Per-ladder settings (matchmaking thresholds,
rating system + constants, fav/ban counts, cleanup delay,
auto-confirm) are admin-editable from Discord (reference §2 defaults).
