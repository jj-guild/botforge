# Pong — Decisions

Validated decisions win over the rest of the doc set (platform rule:
see docs/MODS/README.md — if it was discussed, it is written here,
dated). Decisions marked **open** are design questions awaiting the
mod owner.

## 2026-11-23 — Mod bootstrap

- **D-PONG-001** — `pong` is a **distinct mod** from `ladder`: the
  ladder (Elo queue, blossom matchmaking, botforge-services#15) and
  pong (a montante/descendante table tournament, a season of weekly
  rounds) coexist; neither derives from the other. Validated by
  Aramatu (mod owner), session of 2026-11-23.
- **D-PONG-002** — The mod's **functional source** is the official
  AOE Pong tournament rulebook (S5, "Antre de l'Ours"), provided by
  Aramatu and archived as-is in [REFERENCE.md](REFERENCE.md) — same
  pattern as the ladder mod's JeanJack V2.0 reference.
- **D-PONG-003** — The mod is **game-bound AoE2** (`game_key: aoe2`,
  like kingdoms): draft presets and BO formats are tied to AoE2; the
  civ/map/pool catalog is read through `GameDataService` (never
  duplicated).
- **D-PONG-004** — The rulebook's human-discretion decisions (admin
  win/loose, dispute arbitration, enrollment refusal, patch policy,
  sanctions) stay **facts stated by the bot, decision by a human**:
  the mod provides the documents and time-stamped fact threads, the
  admins arbitrate through the console.

## 2026-11-23 — Mod owner answers (design questions)

- **D-PONG-005 (ex Q-PONG-001)** — `rounds_per_season` = **4** (the
  S5 source contradiction is settled: 4 rounds).
- **D-PONG-006 (ex Q-PONG-002)** — **Two movement policies**
  (`move_policy`, a season parameter):
  1. **`classic`** — the winner moves up, the loser moves down (one
     table);
  2. **`semi_blocked`** — tables are grouped 2 by 2 (3 for the last
     group if the table count is odd); moves are handled **within
     each group only** (e.g. group {T1, T2}: T1's winner stays in T1,
     T1's loser goes to T2, T2's winner goes to T1, T2's loser stays
     in T2). No inter-group movement.
- **D-PONG-007 (ex Q-PONG-003)** — **A/B assignment**: player A is
  the player seated in the table's **first slot**. Every player is
  ranked by their **elo seed** = `(2 × current Elo + max Elo) / 3`,
  computed **at enrollment**. Round 1: A = the higher-ranked of the
  two. Following rounds: **the player moving up takes slot B, the
  player moving down takes slot A** (the winner climbs into B, the
  loser drops into A).
- **D-PONG-008 (ex Q-PONG-004)** — **Table count = player count /
  2**, provisioned at season open (or round open, to be settled in
  implementation). **Odd** case: solved by the parity chain
  (D-PONG-019).
- **D-PONG-009 (ex Q-PONG-005)** — **External drafts via aoe2cm**:
  the map draft uses a plain preset (the map pool); the civ draft is
  **derived from a `base_preset`** (automated generation — the mod
  owner provides his current Python generator; aoe2cm source:
  https://github.com/SiegeEngineers/aoe2cm2). The "3 bans = 1
  category" rule stays **declarative** (a report button tags an
  admin), the external platform not being pilotable by the bot.
- **D-PONG-010 (ex Q-PONG-006)** — **Automatic records**: the mod
  builds the records zip by fetching the players' games (lead:
  https://replaypacker.zeta-two.com) so casters always get the 5
  records of a BO5 **spoiler-free**, with a message showing the map
  draft and the civ draft. Targeted at phase 2 (depends on the
  records provider).
- **D-PONG-011 (ex Q-PONG-007)** — **Off-format scores**, three
  distinct cases:
  1. **Forfeit** — a player declares a forfeit on their table: they
     enter a "lost" result, the other player validates, done (a
     dedicated format `/add_result --forfeit` or equivalent, no
     score manipulation);
  2. **No date found** — two players who fail to schedule:
     **settling is reserved to the competition's admin** (admin
     win/arbitration via console);
  3. **Partially played match / in-set forfeit** — allowed: the
     forfeit grants the remaining wins to the opponent (score
     completed, normal declaration + validation).

## 2026-11-23 — Session 2: flexibility, human seed, player flows

- **D-PONG-012 — v1 format kept + alternation + ±3-day grace.**
  The v1 stays weekly (1 match per week, a Wednesday to Tuesday
  window), with two relaxations:
  1. **`move_policy` alternates per season**: S1 `classic`, S2
     `semi_blocked`, S3 `classic`, ... (an automatic season
     parameter; D-PONG-006 keeps its definition);
  2. **±3-day grace per round**: the next pairing is computed from
     the results **validated at the round deadline**; a match played
     during the grace counts at once (recap), and its movement
     applies from the next round (**movement deferred by one
     round**).
- **D-PONG-013 — Human seed at enrollment.** On top of the ladder
  seed (D-PONG-007 formula), the player **self-declares their
  level** ("I play above/below my ladder Elo"); the admin can
  **correct a player's seed** before the draw and between rounds
  (console, facts stated, decision by a human). Seeds are never
  displayed to players.
- **D-PONG-014 — No global standings; personal recap.** Tournament
  goal: a competitive frame **without pressure** (no cash prize,
  focus on improvement and kindness). No standings, leaderboard,
  podium or comparative score is published. Every player can access
  their **personal per-season recap** (sets played, W/L, opponents,
  table history): **on demand, via an `ephemeral` reply to
  `/recap`** (visible only to the requester), and **as a private DM
  at season close** (final recap). A player leaving mid-season: the
  recap closes on their played sets, no reordering. The table order
  exists only as **internal data** (`chain_position`): neutral
  table names, player messages with no mention of moves or
  position.
- **D-PONG-015 — Late enrollment = waitlist.** The enrollment window
  closes at round 1's opening. After that: the candidate goes to
  **`waitlist`** (a mod state). The **pairing** of candidates into
  insertion duos is decided **by the admin** (no automatic level
  tolerance).
- **D-PONG-016 — "Half" tables theorised (local insertion).** A
  validated duo enters as a **full table inserted in the chain
  between the two tables bracketing its level**: the bot proposes
  the insertion point, the admin validates. The insertion can happen
  **mid-round** (the duo plays itself from the running round, zero
  impact on other tables) and takes effect in the movement chain
  from the next round, with **automatic renumbering**. Strictly
  local effect: the neighbours only change their movement
  neighbour, no global re-shuffle.
- **D-PONG-017 — Departures.** Notification → the bot builds the
  dossier (dates, played matches, pending match — facts) → admin
  validation in the console. **Already validated results stay
  acquired** for the opponents. The leaver's slot is offered
  **first to the waitlist**, at the **exact slot** in the chain (no
  re-shuffle). Leaving during a round with a pending match =
  **forfeit (loss)** for the leaver, the opponent validates and
  advances (D-PONG-011 case 1).
- **D-PONG-018 — Voluntary match (orphan absorption).** Without a
  replacement, the bot offers the **neighbouring players (by
  proximity)** a **voluntary** make-up match against the orphan.
  This match is **recap-only: no movement** in either direction
  (movements are computed only on table matches, RG-TAB-1).
- **D-PONG-019 — Parity chain (resolves Q-PONG-002).** The playable
  count is **never odd**; each level absorbs the next one:
  1. arrivals are **paired** (an isolated player waits for a
     partner);
  2. a departure is **filled at the exact slot** by the waitlist;
  3. without a replacement: a **recap-only voluntary match**
     (D-PONG-018);
  4. last resort: the **fuse** — a waitlist volunteer first, the
     admin next.
  Three-player tables are excluded. Q-PONG-002 is closed.

## 2026-11-24 — Session 3: pairing, recap delivery, withdrawals, caster events

- **D-PONG-020 — Round 1 pairing is seed-adjacent.** The first round
  pairs the sorted seed order adjacently: 1v2, 3v4, 5v6, and so on.
  No global shuffle and no random draw: the two seeds bracketing a
  level meet from round 1.
- **D-PONG-021 — Recap delivery when DMs are closed (settles the
  ARCHITECTURE.md fallback).** The closing recap stays a private DM;
  when the player's DMs are closed or the DM fails, the bot posts an
  **ephemeral notice in `pong:bot-commands`** with a **"resend it
  to me" button** (`pong:resend_recap`) so the player can retrieve
  the final recap at any time. No other DM use changes.
- **D-PONG-022 — The future "ladder" tournament type is a distinct
  concept.** A future ladder-style tournament type (if ever added) is
  **not** the JeanJack ladder mod and will be **renamed** when its
  spec lands (spec to come from the mod owner); the ladder mod keeps
  its own perimeter (D-PONG-001).
- **D-PONG-023 — Withdrawals: self-service and admin-initiated.** A
  player can self-withdraw from the season
  (`/unregister_from_tournament`, the admins are notified);
  an admin can remove a player (console op `remove_player`). A
  mid-round match **plays out**: the withdrawing player's pending
  match becomes a **forfeit at round close**, the opponent follows
  the normal end-of-round placement (waitlist fuse first, admin
  last). Outside a round, the withdrawal is immediate.
- **D-PONG-024 — Guild leave: automatic withdrawal and immediate
  forfeit.** A member leaving the Discord server is automatically
  withdrawn from every active season, with an **immediate forfeit**
  on the pending match (unlike D-PONG-023, the leaver will not play
  it) and a **replacement attempt at the exact slot** (waitlist
  first). The player **profile is kept**; re-enrollment is free if
  the player returns. The admins are notified (leave + applied
  withdrawals/forfeits).
- **D-PONG-025 — Caster events announced automatically.** When a
  Discord event planned by a caster starts, the bot posts an
  announcement automatically. The target channel is chosen **in the
  season-creation view**: an existing channel, a channel to create
  from the view, or **off** (the feature is then disabled for that
  season). Caster streams remain freely announced by hand in
  `pong:casting` regardless.

## Open

- (none — Q-PONG-001..007 are resolved by D-PONG-005..011,
  Q-PONG-002 by D-PONG-019.)
