# Pong — Discord architecture (channels, categories, usage)

Target architecture of the mod's Discord space: categories, channels,
permissions, the per-round lifecycle, and usage rules. Complements
[ENVIRONMENT.md](ENVIRONMENT.md) (config keys) and
[RULES.md](RULES.md) (business rules). Decisions D-PONG-006..035
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
  operation), moved **read-only** to the archive category at round
  close and purged after `archive_retention_days` (D-PONG-031);
  never statically declared.

## 2. Map

```
🏓 AOE PONG (ladder group — visible to players)       [pong:ladder]
├─ 📖 tutoriel              pong:tutorial          (text, pinned how-to)
├─ 🏓 register-as-a-player  pong:register_player  (text, registration front door)
├─ 🎙️ register-as-a-caster  pong:register_caster  (text, caster signup)
├─ 📣 annonces-pong         pong:announcements    (text, news)
├─ 🔊 cast-studio           pong:cast_studio      (voice, optional, D-PONG-034)
├─ ℹ️ infos                  pong:infos            (text, wizard-edited)
├─ 🖼️ media-kit             pong:media_kit        (text)
├─ ✍️ register              pong:enroll           (text, enrollment, players write)
├─ 🤖 bot-commands          pong:bot-commands     (text, all commands)
├─ 📅 match-scheduled        pong:schedule         (text, bot-managed board)
├─ 🎞️ records               pong:records         (text, bot-authored result cards)
└─ 🎙️ casting               pong:casting          (text, public read)

🏓 TABLES (tables groups — generated per round)     [pong:tables]
└─ table-<slug>            pong:table_<slug>    (text, 1 per table)
                                                     neutral slugs, unique
                                                     per round; a 51st table
                                                     channel opens a new group
                                                     (tables-2, tables-3, ...;
                                                     50 channels per category
                                                     cap, D-PONG-030)

🗄️ ARCHIVE (read-only, purge after retention)       [pong:archive]
└─ round-closed table channels                       (D-PONG-031)

⚙️ PONG-STAFF (admin group — admin_only)             [pong:admin]
├─ 💬 admins               pong:admins           (text, staff discussion)
├─ 📋 roster                pong:roster           (text, roster-export destination)
├─ ⚙️ paramètres            pong:settings        (lifecycle panel)
└─ 📜 journal-admin         pong:admin_log       (time-stamped ops)
```

## 3. Permission matrix

| Channel | Candidate | Waitlist | Player | Caster | Admin | off-server |
| --- | --- | --- | --- | --- | --- | --- |
| `tutoriel` | read | read | read | read | write | no |
| `register-as-a-player` | cmd + post | read | read | read | write | no |
| `register-as-a-caster` | cmd + post | read | read | read | write | no |
| `annonces-pong` | read | read | read | read | write | no |
| `bot-commands` | enroll cmd | waitlist-enroll cmd | all cmds | — | all cmds | no |
| `infos` | read | read | read | read | write | no |
| `media-kit` | read | read | read | read | write | no |
| `register` | write | write | write | read | write | no |
| `match-scheduled` | read | read | read | read | write (bot writes) | no |
| `records` | read | read | read | read | read (bot writes) | no |
| `casting` | read | read | read | write | write | read (everyone) |
| `cast-studio` | no | no | connect | connect | connect | no |
| `table_<slug>` | no | no unless in the table | the table's players | read/write | write | no |
| `admins` | no | no | no | no | write | no |
| `roster` | no | no | no | no | read | no |
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
   from the `neutral_random` pool, unordered, D-PONG-014) with the
   pinned **welcome panel** (D-PONG-035): both players tagged by
   Discord id, the handbook link, the season map preset link, the
   table's generated civ preset link (D-PONG-009), the round end
   date (window + grace), the command list with an example each
   (`/update_date`, `/add_result`, `/validate_score`,
   `/contest_score`), the admin role tag to call for help, a
   kindness reminder (D-PONG-014), and the panel facts (player A =
   first slot, host of both drafts; 3 bans = 1 category; neutral
   map = last picked, loser picks the next one).
3. Permissions sync: only the table's two players + admins.
4. A line created for the table on the round's pinned schedule
   board in `pong:schedule` (one board message per round, one
   line per table; the date is filled in by `/update_date`,
   D-PONG-032).
5. Announcement in `annonces-pong`: the table list **without any
   level order**, deadlines, usage reminder. No mention of moves up
   or down (RG-TAB-5).

### During the round

- Players agree on a slot in their table channel and publish it
  with `/update_date` (their line on the round's schedule board
  updates, D-PONG-032), then play, declare
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
2. `table_<slug>` channels moved **read-only** to the archive
   category (`pong:archive`, D-PONG-031): history stays
   consultable, grace-window validations keep working there; the
   purge job deletes them after `archive_retention_days`
   (default 14), and the pass report lists the purged channels
   (never log-only).
3. Matches played inside the grace window (±3 days) keep being
   validated in the archived read-only channels; the recap updates at once,
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
- **`schedule` (match-scheduled)**: the bot-managed per-round
  schedule board (D-PONG-032). One pinned message per round, one
  line per table (players + date, written by `/update_date`);
  read-only for members, write bot + admins; the negotiation
  happens in the table channel; T-48h before the deadline the bot
  posts a reminder in the table channel when no date is set.
  (Supersedes the per-match planning thread.)
- **`table_<slug>`**: the match workspace; automated table
  messages (pinned welcome panel per D-PONG-035, broadcasts). The
  channel name discloses no level.
- **`casting`**: free stream announcements (open stream, D-PONG-002
  REFERENCE), at the caster-player's hand; the bot does not inspect
  titles.
- **`records` (results)**: **bot-written** (D-PONG-033). On every
  validation the bot posts the match's result card: map draft preset
  link, the table's civ draft preset link, the score **inside a
  spoiler**, and the records zip (phase 2, D-PONG-010; the
  players' set link until then), keeping the standardised
  `AOE Pong Round X Table X: P1 || S || P2` header. Members
  read, never post; a pinned manual template stays as the
  documented last-resort fallback.
- **Tournament surface (D-PONG-030)**: `tutoriel` (pinned
  registration how-to), the front doors `register-as-a-player` /
  `register-as-a-caster`, `infos` (wizard-edited: audience, base
  preset links, map pack, handbook), `media-kit` (logo,
  graphics), `register` (players write: enrollment
  confirmations), and the staff space `admins` (discussion) +
  `roster` (roster-export destination, D-PONG-027).
- **Roster export**: admin-initiated export of the enrolled roster
  (Discord nickname, in-game nickname, 1v1/max Elo, tournament
  seed) into a staff-restricted channel (the provisioned default:
  `pong:roster`) (seeds
  are never player-facing, D-PONG-027). Casters get read+write on
  the table channels (D-PONG-027) to organise casts.
- **Player DMs**: only the closing recap (season close or departure,
  D-PONG-017). If the player's DMs are closed: ephemeral notice in
  `bot-commands` with a "resend it to me" button (D-PONG-021). No
  other DM use (no private nudges).
- **`waitlist`**: candidates enrolled after the window close keep
  access to `bot-commands` (waitlist enrollment) and read
  `annonces`; they only enter `tables` once inserted
  as a duo (RG-TAB-3) or as a replacement (RG-TAB-4).

## 6. Insertions, replacements, withdrawals, archives (player flows, D-PONG-015..024)

- Validated duo (half-table): the `table_<slug>` channel is created
  **in the running round** (the two play each other), the chain
  position takes effect next round, automatic renumbering.
- Replacement: the exact slot is taken over; the table channel
  permissions are updated, the schedule-board line reused or reopened.
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
