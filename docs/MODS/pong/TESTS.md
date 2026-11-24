# Pong — Mod test scenarios

The scenarios that validate and safeguard the implementation. **Every
scenario has exactly one automated test**, written by the agent in
`modules/mods/pong/tests/test_scenarios.py` (botforge-services), run
by CI (`pytest tests modules/mods/pong/tests/test_scenarios.py`),
and cross-checked by the docs validation (`validate_docs.py` fails
when a documented scenario has no test).

## Scenario format

- one id per scenario, `SC-PONG-NNN`;
- the scenario ships in the same PR as the rule and the test that
  implement it;
- the test's docstring carries the id, keeping doc and code paired.

## Scenarios

### SC-PONG-001 — player registration with consent

- **Given** an unregistered Discord user, an AoE2 profile resolved by
  the core (steam_id, country, elo)
- **When** they run `/register` and accept the privacy gate
- **Then** the player is registered (discord_id ↔ steam_id linked,
  AoE2 data read through the core, not duplicated) and the
  `candidate` role is granted

Implemented by `test_SC_PONG_001_register_with_consent` in
`test_scenarios.py`.

### SC-PONG-002 — registration without consent refused

- **Given** an unregistered user
- **When** they run `/register` and refuse the privacy gate
- **Then** nothing is persisted (no Mongo/Redis collection touched)

Implemented by `test_SC_PONG_002_register_no_consent`.

### SC-PONG-003 — season enrollment: ladder seed + human seed

- **Given** a registered player (`candidate`), the active season
- **When** they run `/register_to_tournament` ("AOE Pong S<N>")
  with `rules: True`, the availability statement **and their level
  self-declaration** (human seed)
- **Then** they are enrolled (trace of the accepted rulebook version),
  granted `member`, their **elo seed** is computed:
  `(2 × current Elo + max Elo) / 3` (D-PONG-007) and their human
  seed stored (D-PONG-013); neither is ever displayed to the player

Implemented by `test_SC_PONG_003_register_to_tournament`.

### SC-PONG-004 — round open: neutral channels + civ ban

- **Given** an active season with N tables and players distributed
- **When** an admin runs the round-open console op
- **Then** every table has its provisioned channel (panel: player A
  in the first slot, B in the other, reminder that A hosts both
  drafts), the automated civ ban leaves exactly `civs_remaining`
  (15) civs available **per table** (seed persisted round+table for
  audit), the per-table draft-civ preset is displayed, and the
  Wednesday announcement is posted; **neutral table names, no
  position and no move up/down in player messages, unordered
  list** (D-PONG-014, RG-TAB-5); round 1 pairs seed-adjacent
  (1v2, 3v4, ..., D-PONG-020)

Implemented by `test_SC_PONG_004_open_round`.

### SC-PONG-005 — classic movement after a validated result

- **Given** tables 1..N, `move_policy: classic`, a validated result
  on table T (2 < T < N-1)
- **When** the next round is computed
- **Then** the winner moves up one table, the loser moves down one;
  next round the climber holds slot B and the dropper slot A
  (D-PONG-007)

Implemented by `test_SC_PONG_005_climb_fall_classic`.

### SC-PONG-006 — semi_blocked movement: groups of 2 tables

- **Given** `move_policy: semi_blocked`, 5 tables → groups {T1,T2},
  {T3,T4}, {T5} (the last group takes the odd one), a validated
  result on T3 and one on T4
- **When** the next round is computed
- **Then** movements happen within each group only: T3's winner
  stays in T3 (slot B), T3's loser goes to T4 (slot A), T4's winner
  goes to T3, T4's loser stays in T4; no inter-group movement
  (D-PONG-006)

Implemented by `test_SC_PONG_006_move_semi_blocked_groups`.

### SC-PONG-007 — valid result declaration

- **Given** an open round, table T with players A and B
- **When** player A runs `/add_result` with "3-2"
- **Then** the result is created `PENDING`; player B is prompted to
  validate or contest

Implemented by `test_SC_PONG_007_add_result`.

### SC-PONG-008 — off-format score refused

- **Given** `bo_format` = 5 (BO5)
- **When** a player declares "4-2" (X+Y > 5)
- **Then** the declaration is refused with the reason (off BO5
  format), nothing is persisted

Implemented by `test_SC_PONG_008_bad_score`.

### SC-PONG-009 — validation and contest

- **Given** a `PENDING` result
- **When** the second player runs `/validate_score`
- **Then** the result becomes `VALIDATED`, the round views update,
  the player's personal recap is fed (D-PONG-014), and
  re-validation is idempotent (logged, no effect)
- **When** the second player runs `/contest_score`
- **Then** the result becomes `CONTESTED` and the admins are tagged

Implemented by `test_SC_PONG_009_validate_contest`.

### SC-PONG-010 — table outsider refused

- **Given** table T and player X, an outsider (neither A nor B)
- **When** player X tries `/add_result` on T
- **Then** refused (guard: author ∈ {A, B} of the table, round open)

Implemented by `test_SC_PONG_010_outsider`.

### SC-PONG-011 — civ preset derived from the base_preset

- **Given** the season's `civ_draft_base_preset` and an open table
- **When** the mod generates the table's draft-civ preset
  (D-PONG-009: derivation from the base preset)
- **Then** the displayed preset contains only `civs_remaining`
  (15) civs, consistent with the automated ban at the persisted
  seed (generation is re-traceable: same round+table ⇒ same preset)

Implemented by `test_SC_PONG_011_civ_preset_derivation`.

### SC-PONG-012 — neutral map played first

- **Given** a finished map draft on table T (aeo2cm, external)
- **When** the series starts
- **Then** the last map picked in the draft is displayed as the
  neutral map, played first (RG-MDRAFT-1)

Implemented by `test_SC_PONG_012_neutral_map`.

### SC-PONG-013 — reporting a civ preset

- **Given** the table panel with a report button
- **When** a player reports "preset with > 2 unowned civs"
- **Then** the admins are tagged with the table and the preset (the
  mod states the facts, the regen is an admin decision)

Implemented by `test_SC_PONG_013_report_preset`.

### SC-PONG-014 — round close and channel archival

- **Given** the round window elapsed (Wednesday to Tuesday)
- **When** the closing pass runs
- **Then** the table channels are closed/archived
  (`close_tables`), the remaining `PENDING` results are listed in
  a fact thread for admin arbitration, and the pass report is
  posted (never log-only)

Implemented by `test_SC_PONG_014_close_round`.

### SC-PONG-015 — boot self-heal of channels and pins

- **Given** a table channel deleted during an open round
- **When** the boot pass runs
- **Then** the channel is recreated, the `menu:mod:pong:home` pin
  restored, with no unrendered exception (report posted in
  `pong:announcements`)

Implemented by `test_SC_PONG_015_selfheal`.

### SC-PONG-016 — forfeit declared and validated

- **Given** an open round, table T; player A warns they forfeit in
  their table discussion
- **When** they enter the forfeit result ("lost") and player B
  validates (`/validate_score`)
- **Then** the result is **validated with no score manipulation**
  (D-PONG-011 case 1), the RG-TAB movement applies

Implemented by `test_SC_PONG_016_forfeit`.

### SC-PONG-017 — in-set abandon

- **Given** a partially played BO5 (e.g. 1-1), player A abandons the
  set
- **When** the result is entered with the remaining wins granted to
  the opponent (e.g. 1-3) and validated
- **Then** the result is accepted (D-PONG-011 case 3: in-set
  abandons are allowed, the remaining wins go to the opponent)

Implemented by `test_SC_PONG_017_mid_set_abandon`.

### SC-PONG-018 — no date found: admin arbitration

- **Given** a table with no possible scheduling at round close (no
  result, empty planning thread)
- **When** the closing pass lists the facts and the admin applies an
  admin win via the console
- **Then** the admin result is persisted with the decision's author
  (D-PONG-011 case 2: settling is reserved to the admin, never the
  bot)

Implemented by `test_SC_PONG_018_admin_no_schedule`.

### SC-PONG-019 — enrollment after close: waitlist

- **Given** round 1 open (enrollment window closed), a `candidate`
  player running `/register_to_tournament`
- **When** the command is processed
- **Then** season enrollment is refused with an explicit message,
  the player goes to **`waitlist`** (role `pong_waitlist`,
  D-PONG-015); no active player is modified

Implemented by `test_SC_PONG_019_waitlist`.

### SC-PONG-020 — duo insertion ("half table", D-PONG-016)

- **Given** two `waitlist` candidates paired by the admin, a
  running round, a table chain with `chain_position`
- **When** the bot proposes the insertion point and the admin
  validates it (console, confirm card)
- **Then** the duo plays **itself** from the running round (no other
  table modified), the table takes its place in the chain next round
  with **automatic renumbering**; only the direct neighbours change
  their movement counterpart; the operation is logged

Implemented by `test_SC_PONG_020_duo_insertion`.

### SC-PONG-021 — departure filled at the exact slot (D-PONG-017)

- **Given** a player leaving between rounds, a `waitlist`
  volunteer, validated results already involving the leaver
- **When** the admin validates the withdrawal in the console (facts
  dossier)
- **Then** the leaver becomes `departed` (recap closed), **their
  validated results stay acquired** for the opponents, and the
  volunteer takes **the exact slot** in the chain (`replacing`):
  no other table is re-shuffled

Implemented by `test_SC_PONG_021_departure_slot_swap`.

### SC-PONG-022 — orphan with no replacement: recap-only voluntary match (D-PONG-018/019)

- **Given** a validated departure with no `waitlist` volunteer,
  the players of the neighbouring tables
- **When** the bot offers a make-up match and a neighbour accepts
- **Then** the match is played and validated **recap-only**: it
  counts in both players' recaps, **no table movement** applies
  (RG-TAB-1); the orphan keeps their slot; last-resort fuse: a
  waitlist volunteer, then the admin

Implemented by `test_SC_PONG_022_orphan_volunteer_match`.

### SC-PONG-023 — ±3-day grace: deferred movement (D-PONG-012)

- **Given** a round at its deadline with a `PENDING` result, and
  the next round paired on the validated results
- **When** the match is played during the grace and validated
- **Then** the players' recap updates immediately, and the table
  movement applies **from the next round** (deferred by one round:
  the climber/dropper moves one cycle later)

Implemented by `test_SC_PONG_023_grace_deferred_move`.

### SC-PONG-024 — personal recap: ephemeral on demand, DM at close (D-PONG-014)

- **Given** a season with validated results, a player
- **When** the player runs `/recap` (anytime in the season)
- **Then** the reply is **`ephemeral`**: visible only to them (sets
  played, W/L, opponents, table history)
- **When** the season closes (or the player leaves, D-PONG-017)
- **Then** the full final recap is sent **as a private DM**, with an
  ephemeral notice + resend button in `pong:bot-commands` when the
  DM cannot be delivered (D-PONG-021); **no global standings,
  comparative table or podium is ever published** on the server;
  tables are listed with no level order (RG-TAB-5)

Implemented by `test_SC_PONG_024_personal_recap`.

### SC-PONG-025 — withdrawal in two modes: scheduled or immediate (D-PONG-023)

- **Given** an open round, a player with a pending match on their
  table
- **When** the player runs `/unregister_from_tournament` in
  **scheduled** mode
- **Then** the withdrawal is recorded for the next round and the
  admins are notified; the running match **plays out to the end and
  its validated result counts normally, no forfeit applies**
- **When** the withdrawal is requested in **immediate** mode
- **Then** the running match is forfeit for the withdrawing player
  and a replacement is attempted through the parity chain (waitlist
  at the exact slot first)

Implemented by `test_SC_PONG_025_self_withdrawal`.

### SC-PONG-026 — admin removal of a player (D-PONG-023)

- **Given** an enrolled player, an admin
- **When** the admin runs the console op `remove_player` (confirm
  card)
- **Then** the player is withdrawn with the same semantics as
  SC-PONG-025 (mid-round match plays out, forfeit at round close),
  the operation is logged with its author, and the player is
  notified

Implemented by `test_SC_PONG_026_admin_removal`.

### SC-PONG-027 — guild leave: automatic withdrawal and immediate forfeit (D-PONG-024)

- **Given** a member enrolled in an active season with a pending
  match, a waitlist with a volunteer
- **When** the member leaves the Discord server
- **Then** they are automatically withdrawn from every active season
  with an **immediate forfeit** on the pending match (unlike
  D-PONG-023, the match does not play out), the freed slot is
  offered first to the waitlist **at the exact slot**, their
  player profile is **kept** (re-enrollment free on return), and
  the admins are notified

Implemented by `test_SC_PONG_027_guild_leave_forfeit`.

### SC-PONG-028 — caster event announced at start (D-PONG-025)

- **Given** a season with a caster-events announcement channel set,
  a Discord event planned by a `pong_caster`
- **When** the event starts
- **Then** the bot posts an automatic announcement in the configured
  channel; manual cast announcements in `pong:casting` are
  unaffected

Implemented by `test_SC_PONG_028_caster_event_announcement`.

### SC-PONG-029 — events channel optional, feature can be off (D-PONG-025)

- **Given** the season-creation view
- **When** the admin sets the caster-events channel to an existing
  channel, a channel to create, or **off**
- **Then** respectively: announcements land in that channel; the
  channel is provisioned by the view and announcements land in it;
  the feature is **disabled** and no automatic announcement is ever
  posted for that season

Implemented by `test_SC_PONG_029_events_channel_options`.

### SC-PONG-030 — caster read+write on table channels (D-PONG-027)

- **Given** an open round with a provisioned table channel, a
  `pong_caster` member
- **When** the channel permissions are provisioned
- **Then** the caster may read **and post** in the table channel;
  players outside the table and non-casters still cannot

Implemented by `test_SC_PONG_030_caster_table_access`.

### SC-PONG-031 — roster export restricted to staff channels (D-PONG-027)

- **Given** an enrolled roster, an admin running the export action
- **When** the target channel is staff-restricted, then
  player-visible
- **Then** the export (Discord nickname, in-game nickname, 1v1/max
  Elo, tournament seed) lands in the staff channel; targeting a
  player-visible channel is **refused** (seeds are never
  player-facing, D-PONG-013/014)

Implemented by `test_SC_PONG_031_roster_export_staff_only`.

> Auto records (D-PONG-010, phase 2, spoiler-free zip provider)
> arrive with their scenario in the PR that implements them. Every
> new automatable rule added to RULES.md arrives with its scenario
> in the same PR.
