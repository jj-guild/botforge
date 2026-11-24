# Pong — Discord architecture (channels, categories, usage)

Target architecture of the mod's Discord space: categories, channels,
permissions, the per-round lifecycle, and usage rules. Complements
[ENVIRONMENT.md](ENVIRONMENT.md) (config keys) and
[RULES.md](RULES.md) (business rules). Decisions D-PONG-006..025
([DECISIONS.md](DECISIONS.md)) apply.

## 1. Principle: mod-scoped categories, provisioned by the core

- No category or channel is created directly by the mod: everything
  goes through the core's `ModRegistry` +
  `ChannelService`/`RoleService` (botforge-services#26), from the
  YAML **declaration** (`modules/mods/pong/conf/mod.yaml`).
- Channels are addressed by logical keys `pong:<key>`, never by
  name. The mod never depends on physical naming: renaming a channel
  breaks nothing.
- Table channels are **generated per round** (the `open_round`
  operation) and **archived** at round close; never statically
  declared.

## 2. Map

```
🏓 AOE PONG (ladder group — visible to players)       [pong:ladder]
├─ 📣 annonces-pong        pong:announcements   (text)
├─ 🤖 bot-commands         pong:bot-commands    (text)
├─ 📅 planification        pong:planning        (text, 1 thread/match)
├─ 🎞️ records              pong:records         (text)
└─ 🎙️ casting              pong:casting         (text, public read)

🏓 TABLES (tables group — generated per round)       [pong:tables]
└─ table-<slug>            pong:table_<slug>    (text, 1 per table)
                                                     neutral slugs, unique
                                                     per round, recycled

⚙️ PONG-STAFF (admin group — admin_only)             [pong:admin]
├─ ⚙️ paramètres           pong:settings        (lifecycle panel)
└─ 📜 journal-admin        pong:admin_log       (time-stamped ops)
```

## 3. Permission matrix

| Channel | Candidate | Waitlist | Player | Caster | Admin | off-server |
| --- | --- | --- | --- | --- | --- | --- |
| `annonces-pong` | read | read | read | read | write | no |
| `bot-commands` | `/register` cmd | waitlist-enroll cmd | all cmds | — | all cmds | no |
| `planning` | no | no | read + start thread | read | write | no |
| `records` | no | no | read + post | read/post | write | no |
| `casting` | read | read | read | write | write | read (everyone) |
| `table_<slug>` | no | no unless in the table | the table's players | read/write | write | no |
| `paramètres` | no | no | no | no | write | no |
| `journal-admin` | no | no | no | no | read | no |

Roles gate: `candidate`, `pong_waitlist`, `member`,
`pong_caster`, `admin` (see ENVIRONMENT.md, "Roles"). The core
resynchronises permissions at every round (open/close).

## 4. Round lifecycle (operational usage)

### Opening (console op `open_round`)

1. Pairing computed from the results **validated at the deadline**
   (±3-day grace: D-PONG-012, deferred movement for late finishers).
   Round 1 pairs seed-adjacent: 1v2, 3v4, and so on (D-PONG-020).
2. `table-<slug>` channels created in the tables group (slug drawn
   from the `neutral_random` pool, unordered, D-PONG-014) + pinned
   panel: players A/B (A = first slot, host of both drafts), the
   draft-civ preset, reminders (3 bans = 1 category, neutral map =
   last picked, loser picks the next one), deadline = window end +
   grace.
3. Permissions sync: only the table's two players + admins.
4. Planning thread created in `pong:planning`:
   `Round <n> — <slug>: <NickA> vs <NickB>`.
5. Announcement in `annonces-pong`: the table list **without any
   level order**, deadlines, usage reminder. No mention of moves up
   or down (RG-TAB-5).

### During the round

- Players schedule in their thread, play, declare
  (`/add_result` on the table channel) and validate
  (`/validate_score`) or contest (`/contest_score`, tags an
  admin).
- Fact buttons on the table: "non-conforming draft", "forfeit",
  "report". Every report tags an admin + a time-stamped fact thread
  (facts stated, human decides, RG-ADM).
- `/recap`: **ephemeral** reply (visible only to the requester).

### Closing (`round_window` timer + closing pass)

1. `PENDING` results listed in an arbitration thread (never
   log-only); admin win/loose if needed (D-PONG-011).
2. `table_<slug>` channels **archived** (closed + moved to a
   core-provisioned archive category, not deleted: history is part
   of the fact thread).
3. Matches played inside the grace window (±3 days) keep being
   validated in the archived threads; the recap updates at once,
   the movement applies at the next pairing computation.

### Self-heal (boot + periodic)

- Missing channel: rebuilt from state (panel reconstructed), pins
  restored, permissions resynchronised, report in
  `annonces-pong` (no silent exception, SC-PONG-015).

## 5. Usage rules (the "hows")

- **`annonces-pong`**: only the automated announcements + admins
  post there. Contractual content: round opened/closed, tables
  (unordered list), per-table civs, generic reminders. No results,
  no scores, no recap.
- **`bot-commands`**: every slash command is expected to work there
  (declare/validate/contest also work on the table channel).
  Sensitive command replies are **ephemeral**: notices, recap,
  registration status.
- **`planning`**: one thread per match and per round; scheduling
  exchanges stay inside it (no mandatory DM); the thread is locked
  at round close.
- **`table_<slug>`**: the match workspace; automated table
  messages (panel, broadcasts). The channel name discloses no level.
- **`casting`**: free stream announcements (open stream, D-PONG-002
  REFERENCE), at the caster-player's hand; the bot does not inspect
  titles.
- **`records`**: the packs (phase 1: template + button; phase 2:
  spoiler-free auto zip, D-PONG-010) per match, standardised
  message format `AOE Pong Round X Table X: P1 || S || P2`.
- **Roster export**: admin-initiated export of the enrolled roster
  (Discord nickname, in-game nickname, 1v1/max Elo, tournament
  seed) into a chosen channel that MUST be staff-restricted (seeds
  are never player-facing, D-PONG-027). Casters get read+write on
  the table channels (D-PONG-027) to organise casts.
- **Player DMs**: only the closing recap (season close or departure,
  D-PONG-017). If the player's DMs are closed: ephemeral notice in
  `bot-commands` with a "resend it to me" button (D-PONG-021). No
  other DM use (no private nudges).
- **`waitlist`**: candidates enrolled after the window close keep
  access to `bot-commands` (waitlist enrollment) and read
  `annonces`; they only enter `tables`/`planning` once inserted
  as a duo (RG-TAB-3) or as a replacement (RG-TAB-4).

## 6. Insertions, replacements, withdrawals, archives (player flows, D-PONG-015..024)

- Validated duo (half-table): the `table_<slug>` channel is created
  **in the running round** (the two play each other), the chain
  position takes effect next round, automatic renumbering.
- Replacement: the exact slot is taken over; the table channel
  permissions are updated, the planning thread reused or reopened.
- Self-service withdrawal (`/unregister_from_tournament`, admins
  notified) or admin removal (`remove_player`, D-PONG-023), in the
  two modes: **scheduled** (effective next round; the running match
  plays out and its validated result counts, no forfeit) or
  **immediate** (forfeit on the running match, replacement through
  the parity chain).
- Guild leave (D-PONG-024): automatic withdrawal from every active
  season and **immediate forfeit**; the freed slot is offered first
  to the waitlist at the exact chain slot; the player profile is
  kept, re-enrollment is free. The admins are notified.
- Departure: the table channel switches to orphan mode (panel
  updated: "voluntary make-up match offered to the neighbours")
  until absorbed (replacement, voluntary match, fuse); otherwise the
  channel is archived early at round close.

## 7. Multi-tournament (scope note)

Every tournament type lives in **its own mod-scoped perimeter**
(`pong:*`, future `swiss:*`, `bracket:*`, ...) with its
categories provisioned the same way: no channel collisions, the
core handles coexistence (botforge-services#26). The pong pairing
engine sits behind a `PairingPolicy` seam (a pure domain
interface): future formats (swiss rounds, brackets) will reuse the
shared base (enrollment, seasons, results, drafts, recaps, console)
by swapping the pairing policy. Extracting a shared
`tournament-core` will be decided **at the second
implementation**, not before (rule: abstract after two). The future
"ladder"-type tournament is a **distinct concept** from the
JeanJack ladder mod and will be renamed when its spec lands
(D-PONG-022).
