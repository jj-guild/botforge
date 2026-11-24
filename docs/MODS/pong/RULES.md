# Pong — Mod Rules

The game rules applied by the mod, extracted from
[REFERENCE.md](REFERENCE.md) (the AOE Pong rulebook). Every rule is
written to be automatable: testable or checkable by the bot. Zones of
admin discretion are classified **facts stated, decision by a
human**: the bot reports the facts (tags, timestamps, states), the
admin settles. Decisions win ([DECISIONS.md](DECISIONS.md),
D-PONG-001..025).

## RG-REG — Registration and enrollment

### RG-REG-1 — Player registration

`/register` (channel `pong:bot-commands`) registers the player:
linking `steam_id` ↔ `discord_id` plus the core's AoE2 data
(country, elo) **read through the game profile, never copied into
the mod's collections**. The command requires explicit consent
(privacy gate) before persistence; without consent, refused.

- **Edge cases**: discord_id already registered → offer to link to
  the existing profile; steam_id already taken by another player →
  refuse + admin notification.
- Otherwise manual: nothing is inferred, the admin arbitrates.

### RG-REG-2 — Season enrollment

`/register_to_tournament` with the active season's name +
`rules: True` validation (rulebook acceptance traced with the
accepted rulebook version). The mod requires: RG-REG-1 succeeded,
Discord presence, and the statement "2 consecutive 3-hour windows
within 17:00-23:00" captured at enrollment. Any enrollment change
must be reported to an admin: the mod provides `/update_entry`,
which tags the admins.

- **Ladder seed**: at enrollment the player receives their **elo
  seed** = `(2 × current Elo + max Elo) / 3` (D-PONG-007).
- **Human seed (D-PONG-013)**: the player **self-declares their
  level** ("above / below my ladder Elo", a short free-text field);
  the admin can **correct a player's seed** before the draw and
  between rounds (console, confirm card, log). The seed serves the
  initial placement only, **never displayed** to players.
- **Enrollment refusal**: a human decision (the mod neither accepts
  nor refuses alone), it exposes the matching admin button.

### RG-REG-3 — Late enrollment: waitlist

The enrollment window **closes at round 1's opening** (D-PONG-015).
A `/register_to_tournament` after the close is refused and offers
joining the **waitlist** (player state `waitlist`, role
`pong_waitlist`). The **pairing** of two waitlist candidates into
an insertion duo is an admin decision (no automatic level
tolerance); the duo enters through RG-TAB-3.

### RG-REG-4 — Withdrawals (D-PONG-023/024)

- **Self-service withdrawal**: `/unregister_from_tournament`
  removes the player from the active season; the admins are
  notified. Outside a round, the withdrawal is immediate. During a
  round with a pending match, the match **stays playable** and the
  withdrawing player's result becomes a **forfeit at round close**
  (the opponent validates and follows the normal end-of-round
  placement, RG-TAB-4).
- **Admin removal**: the console op `remove_player` applies the
  same semantics, with a confirm card, a log and a notice to the
  player.
- **Guild leave**: a member leaving the Discord server is
  **automatically withdrawn** from every active season with an
  **immediate forfeit** on the pending match (the match does not
  play out); the freed slot follows RG-TAB-4 (waitlist first, at
  the exact slot); the player **profile is kept** and re-enrollment
  is free on return; the admins are notified.

## RG-STRUC — Season structure

### RG-STRUC-1 — Rounds and tables

A season counts `rounds_per_season` rounds (**4**, D-PONG-005),
each one a `round_window` (default 7 days, Wednesday to Tuesday)
**plus a grace of `round_grace_days` (3) days** (D-PONG-012). The
BO is `bo_format` (default BO5). **The table count = player count
/ 2**; the playable count is never odd (parity chain, RG-TAB-4). At
round open, the mod creates each table's channel, announcing
players A/B, preset and round there; at close it closes the
channels (config `close_tables`).

- **±3-day grace (D-PONG-012)**: the next round's pairing is
  computed from the results **validated at the deadline**. A match
  played during the grace counts immediately in the player's recap
  (RG-RES-3); its **movement is deferred by one round** and applies
  at the next computation.

### RG-STRUC-2 — A/B assignment and draft hosting

On every table, **player A is the player seated in the table's first
slot**, player B the other one (D-PONG-007):

- **round 1**: the pairing is **seed-adjacent** (1v2, 3v4, 5v6,
  ..., sorted by seed; D-PONG-020) and A = the higher-ranked of the
  two by seed (ladder + human, D-PONG-007/013);
- **following rounds**: **the player moving up takes slot B, the
  player moving down takes slot A** (from the RG-TAB movement
  computation);
- player A hosts the map draft **and** the civ draft; the
  convention is restated in the table panel.

## RG-TAB — Tables and moves up/down

### RG-TAB-1 — Movements

Central rule ("like in ping pong"): **the winner moves up, the
loser moves down**. Two movement policies (D-PONG-006), which
**alternate per season** (D-PONG-012: S1 `classic`, S2
`semi_blocked`, S3 `classic`, ...):

1. **`classic`** — the winner moves up one table, the loser moves
   down one table;
2. **`semi_blocked`** — tables are grouped 2 by 2 (3 for the last
   group if the table count is odd); moves happen **within each
   group only** (e.g. group {T1, T2}: T1's winner stays in T1,
   T1's loser goes to T2, T2's winner goes to T1, T2's loser stays
   in T2). No inter-group movement.

Movements are computed **on table matches only** (a voluntary
make-up match moves nobody, RG-TAB-4), at the next round's opening,
on the results validated at the deadline (grace: movement deferred
by one round, D-PONG-012). They set the next round's A/B slots (the
climber takes B, the dropper takes A).

### RG-TAB-2 — Table blocking

The admin can **block tables against moves up or down** to avoid
(re)matches: in `classic`, a player stays at their table when the
target table is blocked against their movement direction; in
`semi_blocked`, blocking one table locks its whole group. Admin
console operation (`mod="pong"`), confirm card, mutation log,
applied at the next round's computation.

### RG-TAB-3 — "Half" tables: duo insertion (D-PONG-016)

The table chain is an **ordered internal list** (`chain_position`,
a numeric index accepting in-between values like 7.5). A validated
duo's entry (RG-REG-3) goes like this:

1. the bot **proposes the insertion point**: between the two tables
   bracketing the duo's level (each entrant's human seed);
2. the **admin validates** the insertion in the console (confirm
   card, log);
3. **mid-round**: the duo plays its match against itself from the
   running round, **zero impact on other tables**;
4. next round, the table takes its place in the movement chain and
   **renumbering is automatic**. Only the direct neighbours change
   their movement counterpart; no global re-shuffle.

### RG-TAB-4 — Parity chain and make-up matches (D-PONG-019)

The playable count is **never odd**; each level absorbs the next
one:

1. **Pair-gated arrivals**: a lone waitlist candidate waits for a
   partner (RG-REG-3);
2. **Departures filled at the exact slot**: the first waitlist
   volunteer takes the leaver's place in the chain (no re-shuffle,
   acquired results kept, D-PONG-017);
3. **No replacement — voluntary match**: the bot offers the
   **neighbouring tables' players (by proximity)** a make-up match
   against the orphan, voluntary, **recap-only**: the result counts
   in both players' recaps but **no movement** applies (RG-TAB-1);
4. **Last resort — the fuse**: a waitlist volunteer, then the
   admin.

A departure during a round with a pending match = **forfeit
(loss)** for the leaver (D-PONG-011 case 1 / D-PONG-017); on a
guild leave the forfeit is **immediate** (D-PONG-024).

### RG-TAB-5 — The invisible table order (D-PONG-014)

The table order exists **in the data, not in the display**:

- `chain_position` is internal (consumed by the RG-TAB-1 movement
  computation and the RG-TAB-3 insertion, visible in the admin
  console only);
- table channels carry **neutral names** (no order number, no
  level); the announcements channel lists tables in a
  non-significant order (alphabetical);
- player messages **never** mention position or moves up/down:
  "this week, your match: vs Y".

## RG-CDRAFT — Civilizations

### RG-CDRAFT-1 — Automated per-table civ ban

At each round's start, **for every table**, the mod bans, in an
automated random way, the number required so that exactly
`civs_remaining` (default 15) civilizations remain available, and
publishes the table's linked draft-civ preset.

- **Re-traceable** randomness (seed persisted per round+table for
  audit and replayability).
- Civilization source: `GameDataService` (core); the mod never
  duplicates the civ catalog.

### RG-CDRAFT-2 — Unplayable preset

If a table's draft-civ preset contains more than two civilizations a
player does not own, that player can request a new draft (a report
button on the table tags an admin). The regen decision is human
(admin); the new draft goes through RG-CDRAFT-1.

## RG-MDRAFT — Map draft and map picks

### RG-MDRAFT-1 — External drafts (aeo2cm)

The map draft and the civ draft stay **external, on aoe2cm**
(D-PONG-009):

- **map draft**: a plain preset to handle, the season's map pool
  (e.g. S5: `https://aoe2cm.net/preset/pGWoJ`);
- **civ draft**: **derived from a `base_preset`** — the mod
  generates the table's preset from the `base_preset` (port of the
  mod owner's Python generator; aoe2cm source:
  https://github.com/SiegeEngineers/aoe2cm2), applying
  RG-CDRAFT-1 first.

The **last map picked** in the draft is the **neutral map**, played
first: the mod displays it as-is in the table panel.

### RG-MDRAFT-2 — The three first bans = one category

In the map draft, each player's **three first bans** must hit maps
from the **same category** (a category ban). Any draft not
respecting this rule is **invalid and must be redone from the
start**.

- The draft being external (aeo2cm), the check is **declarative**:
  the draft post on the table carries a visible "non-conforming
  draft" button that tags an admin (facts stated, human decides).

### RG-MDRAFT-3 — Picking the next map

The **loser** of the previous game picks the next map among **all
available maps** (not already played), including the ones their
opponent drafted.

- Declarative reminder in the table panel (series tracking by the
  mod is not required in phase 1: the result declaration stays the
  entry point).

## RG-RES — Results

### RG-RES-1 — Declaration

`/add_result` **on the table channel**: player A, score `X-X`
(**score A on the left, score B on the right**), player B.
Validations:

- author ∈ {player A, player B} of the table, round open;
- score format `^[0-9]+-[0-9]+`, compatible with `bo_format`
  (BO5: X+Y ≤ 5, max(X,Y) = 3).

**Off-format scores, three distinct cases (D-PONG-011)**:

1. **Forfeit** — a player declares a forfeit on their table: they
   enter a "lost" result (dedicated forfeit format, no score
   manipulation), the other player validates, done;
2. **No date found** — two players with no possible scheduling:
   **the competition's admin settles** (admin win via console,
   facts stated, human decides);
3. **Partially played match / in-set abandon** — allowed: the
   forfeit grants the remaining wins to the opponent (score
   completed, normal declaration + validation).

### RG-RES-2 — Validation or contest

The **second player** (the one who did not declare) is prompted to
validate via `/validate_score` or contest via `/contest_score`,
**which tags an admin**. Without validation, the result stays
`PENDING` until admin handling (facts stated, human decides).
After a contest: the admin settles via the console
(validate/invalidate/redeclare).

### RG-RES-3 — Persistence, personal recap, movement

A **validated** (or admin-arbitrated) result is persisted, triggers
RG-TAB-1 (table movement, deferred by one round when played during
the grace, D-PONG-012) and feeds the player's **personal recap**
(D-PONG-014):

- **no global standings**: no comparative table published;
- **`/recap` (an `ephemeral` reply** — visible only to the
  requester): sets played, W/L, opponents, table history;
- **at season close**, the full final recap is sent **as a private
  DM**; if the DM cannot be delivered, an ephemeral notice and a
  resend button are posted in `pong:bot-commands` (D-PONG-021); a
  leaving player receives the closed recap of their played sets
  (D-PONG-017);
- idempotent: re-validating an already validated result has no
  effect (log only).

## RG-REC — Records and casting

### RG-REC-1 — Records

To ease casting and arbitration, every match comes with a result
message in the exact format
`AOE Pong Ronde X Table X : Pseudo1 || Score || Pseudo2` showing
the map draft and the civ draft, plus a zip containing the
"Drafts" file and the games
`AOEPong_Pseudo1_vs_Pseudo2_Game_X.aoe2rec` (the wording is
locale-driven: the format's structure is binding, the words come
from the season's locale files).

- **Targeted automation (D-PONG-010, phase 2)**: the mod builds
  the zip by fetching the players' games (lead:
  https://replaypacker.zeta-two.com) so casters always get the 5
  records of a BO5 **spoiler-free**. In phase 1 the mod generates
  the message template (button); the physical file collection
  stays human.

### RG-REC-2 — Open stream

Open stream by default (config `open_stream`, default true): any
caster may cast; the title must contain "AOE Pong". The mod offers
the cast announcement on the table (channel `pong:casting`, role
`pong_caster`) but does not check stream titles (out of bot
scope).

### RG-REC-3 — Caster events announced automatically (D-PONG-025)

A caster (`pong_caster` role) can plan a Discord event for the
games they cast. When a planned event starts, the mod posts an
automatic announcement in the season's configured events channel.
The channel is chosen in the season-creation view: an existing
channel, a channel to create from the view, or **off** (the
feature is then disabled for that season; no announcement is ever
posted). Manual cast announcements (RG-REC-2) are unaffected.

## RG-ADM — Admin operations (facts stated, human decides)

The mod provides the documents and buttons, the decision stays
human:

- **Admin Win / Admin Loose**: lateness > 30 min (table opening
  timestamp + reminder), rescheduling < 24h before the planned slot,
  or **no date found** (D-PONG-011 case 2) → the mod lists the
  time-stamped facts on the table and in the console; the admin
  applies the admin result via the console (confirm card + log).
- **Admin Restart**: criteria reminder (first 6 in-game minutes,
  generation-bug list from the reference), table announcement; same
  civs/colours after the restart (to be refreshed in the panel).
- **Seed correction (D-PONG-013)**: the admin adjusts a player's
  seed (before the draw, between rounds); confirm card + log; the
  corrected seed serves the next placement, never displayed.
- **Insertion validation (D-PONG-016)**: the bot proposes a duo's
  insertion point, the admin validates in the console (confirm
  card); **waitlist pairing (D-PONG-015)**: an admin decision, duo
  by duo.
- **Player departure (D-PONG-017)**: the bot builds the dossier
  (played/pending matches, dates); the admin validates the
  withdrawal in the console; the slot is offered to the waitlist,
  otherwise a voluntary match (RG-TAB-4).
- **Player removal (D-PONG-023)**: the console op `remove_player`
  withdraws a player with the RG-REG-4 semantics (confirm card,
  log, notice to the player).
- **Mid-tournament patch**: old/new patch choice → a season
  parameter editable from the console (config `patch_policy`,
  default "admin decides").
- **Disputes / sanctions / exclusions / enrollment refusals**:
  outside automation; the mod provides the fact thread (logs,
  timestamps, states) on console request.
