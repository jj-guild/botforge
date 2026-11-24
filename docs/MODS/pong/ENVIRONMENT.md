# Pong — Mod Environment

The mod's environment and configuration. Defaults come from the S5
rulebook ([REFERENCE.md](REFERENCE.md)) and the decisions
([DECISIONS.md](DECISIONS.md), D-PONG-001..025).

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Whether the mod is enabled |
| `game_key` | str | Bound game key; default `aoe2` (game-bound mod; the mod reads the catalog through the core, never owns it) |
| `season_name` | str | Active season name (form "AOE Pong S<N>") |
| `rounds_per_season` | int | Rounds per season; default **4** (D-PONG-005) |
| `round_window` | dict | Round window; default Wednesday to Tuesday (7 days), automatic closing timer |
| `round_grace_days` | int | **Grace in days beyond the window; default 3** (D-PONG-012): the next pairing uses the results **validated at the deadline**; a match played during the grace counts for the recap, with **movement deferred by one round** |
| `bo_format` | int | Best-of for matches; default 5 (BO5) |
| `civs_remaining` | int | Civilizations left after the automated per-table ban; default 15 |
| `tables_count` | derived | **Enrolled players / 2** (D-PONG-008); the playable count is never odd (parity chain, D-PONG-019, RG-TAB-4) |
| `elo_seed_formula` | expr | Ladder seed = `(2 × current Elo + max Elo) / 3`, computed at enrollment (D-PONG-007) |
| `human_seed` | dict | **Human seed (D-PONG-013)**: level self-declaration at enrollment + `admin_override: true` (admin correction before the draw and between rounds, console). Used for placement only, **never displayed** |
| `move_policy` | enum | **`classic`** (winner up, loser down) or **`semi_blocked`** (groups of 2 tables, 3 if odd; intra-group moves only); definitions D-PONG-006 |
| `move_policy_schedule` | str | **Per-season alternation (D-PONG-012)**: `alternate` = S1 `classic`, S2 `semi_blocked`, S3 `classic`, ... (default value) |
| `table_naming` | enum | **Neutral names (D-PONG-014)**: table channels carry no order number and no level; default `neutral_random`; internal `chain_position`, never displayed |
| `waitlist_admin_pairing` | bool | Waitlist pairing into insertion duos is decided by the admin, duo by duo (D-PONG-015); default true (no automatic tolerance) |
| `orphan_match` | enum | Voluntary make-up match against an orphan with no replacement: `recap_only` (default, D-PONG-018), no table movement, offered to the neighbours by proximity; last-resort fuse: a waitlist volunteer, then the admin (D-PONG-019) |
| `recap_delivery` | dict | Personal per-season recap (sets, W/L, opponents, table history): **`on_request: ephemeral`** (the `/recap` reply is visible only to the requester, D-PONG-014) and **`season_close: dm`** (closing recap as a private DM). If the player's DMs are closed: ephemeral notice in `pong:bot-commands` + resend button (D-PONG-021). No comparative view published |
| `draft_map_preset` | url | aoe2cm preset of the season's map pool (S5: https://aoe2cm.net/preset/pGWoJ) |
| `civ_draft_base_preset` | url | aoe2cm `base_preset` the mod **derives** each table's draft-civ preset from (D-PONG-009; endpoints `GET /api/preset/<id>` and `POST /api/preset/new`, payload field `encodedCivilisations` as a hex bitmask over the 60 civs; excluded indexes {0, 12, 46, 47, 48, 54, 55, 56}, max 3 DLC civs (> 42) with reroll; 7/11/15 civs for BO1/BO3/BO5) |
| `map_pool` | ref | Reference to the core's season map pool (`GameDataService`); never a hard-coded list in the mod |
| `open_stream` | bool | Open stream allowed; default true ("AOE Pong" title required, not checked by the bot) |
| `patch_policy` | enum | In-tournament patch policy; default "admin decides" (console) |
| `close_tables` | bool | Close the table channels at round close; default true |
| `planning_requirement` | str | Declarative enrollment requirement: "two 3-hour consecutive windows within 17:00-23:00" (FR timezone), captured at enrollment |
| `records_provider` | ref | **Phase 2 (D-PONG-010)**: provider generating the records zip from the players' games (lead: https://replaypacker.zeta-two.com) |
| `withdrawal` | dict | Self-service withdrawal (`/unregister_from_tournament`) and admin removal (console op `remove_player`), both notifying the admins, in two modes (D-PONG-023): **scheduled** (effective next round, the running match plays out and its result counts) or **immediate** (forfeit + replacement attempt at the exact slot); leaving the Discord server = automatic withdrawal + **immediate forfeit**, profile kept, re-enrollment free (D-PONG-024) |
| `caster_events` | dict | Automatic announcement of caster-planned Discord events when they start (D-PONG-025); target channel chosen in the season-creation view: an existing channel, a channel to create, or **off** (feature disabled) |
| `roster_export` | dict | Admin-initiated export of the enrolled roster (Discord nickname, in-game nickname, 1v1/max Elo, tournament seed); the target channel MUST be staff-restricted (seeds are never player-facing, D-PONG-027) |
| `logo_url` | url | Tournament logo URL, cosmetic, editable after creation (D-PONG-028) |
| `caster_table_access` | str | Caster access to table channels; default `read_write` (D-PONG-027) |

## Player state (lifecycle)

`candidate` → `registered` → (`waitlist` — after the enrollment
window closes, D-PONG-015) → `player` (active season) →
`replacing` (entered at a departing player's exact slot,
D-PONG-017) → `departed` (withdrawal validated by the admin, recap
closed; on a guild leave the withdrawal is automatic and the forfeit
immediate, D-PONG-024). Every withdrawal transition is **facts
stated by the bot, decision by the admin in the console** (RG-ADM),
except the guild-leave auto-withdrawal which applies as stated
above.

## Channels and roles

Channels and roles **declared** by the mod in its declaration YAML
(`modules/mods/pong/conf/mod.yaml`, botforge-services). Channels
are addressed by mod-scoped category keys (`pong:<key>`); roles by
logical keys. The core provisions them through `ModRegistry` +
`ChannelService`/`RoleService` (botforge-services#26); never any
platform category here.

### Categories (mod-scoped)

| Key | Display name | Admin only | Access roles |
| --- | --------------- | ----------- | ------------- |
| `pong:ladder` | AOE Pong | no | `member`, `admin` |
| `pong:tables` | AOE Pong — Tables | no | `member`, `admin` |
| `pong:admin` | AOE Pong — Staff | yes | `admin` |

### Channels

| Key | Name | Group | Kind | Access |
| --- | --------------- | ------ | ---- | ----- |
| `pong:announcements` | annonces-pong | ladder | text | players (read), admins (post); table list **without any level order** (D-PONG-014) |
| `pong:bot-commands` | bot-commands | ladder | text | players (commands, including `/recap` as an ephemeral reply) |
| `pong:planning` | planification | ladder | text (one thread per match) | players |
| `pong:records` | records | ladder | text | players, casters |
| `pong:casting` | casting | ladder | text | public read |
| `pong:table_<slug>` | table-<neutral name> | tables | text | the table's `member`s + admins (channels **generated** per round, neutral names with no level number; D-PONG-014/RG-TAB-5, created at open, closed/archived at close) |

### Roles

The role trio uses the platform's standard keys (`candidate`,
`member`, `admin`, like the kingdoms mod), with mod-specific
extras for the waitlist and casters. The trio stays
mod-level in v1; per-tournament roles are the v2 multi-tournament
pattern (D-PONG-026).

| Key | Display name | What it gates |
| --- | --------------- | --------------- |
| `candidate` | Pong Candidat | `/register` done, not yet enrolled in the season |
| `member` | Pong Joueur | enrolled player of the season (ladder + tables channels) |
| `pong_waitlist` | Pong Waitlist | candidate enrolled after the enrollment window closed (D-PONG-015); waiting for a pair (RG-TAB-3/4) |
| `admin` | Pong Admin | staff category, mod console, admin ops |
| `pong_caster` | Pong Caster | cast announcements (descriptive role, open stream) |

## Season configuration

Seasons are registered in the core's season registry with the
visible game-scoped id `pong-aoe2-<guild id>-<index>` (the mod never
runs its own counter). At season activation: map pool (core
reference), presets (map + civ `base_preset`), `bo_format`,
`rounds_per_season` (4), `round_grace_days` (3), `move_policy`
resolved by `move_policy_schedule: alternate` (S1 classic, S2
semi_blocked, S3 classic, ..., D-PONG-012), parity policy
(`waitlist_admin_pairing`, `orphan_match`), `recap_delivery`
(`on_request: ephemeral`, `season_close: dm`), withdrawal policy
(`withdrawal`, D-PONG-023/024), caster events
(`caster_events`, D-PONG-025), policies (`open_stream`,
`patch_policy`).
