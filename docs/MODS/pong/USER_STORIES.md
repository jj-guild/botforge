# Pong — User stories

Every user story the bot must cover. Each story:
**As a <role>, I want <capability> so that <benefit>**, traced to the
rules (RULES.md), decisions (DECISIONS.md) and test scenarios
(TESTS.md) that realise it. Any story with no rule trace = a design
point to settle; any rule with no story = dead doc, flagged in
review.

Roles: **C**andidate, **W**aitlist, **P**layer, **K** (caster),
**A**dmin, **S**pectator.

## Player journey

| ID | As | I want | so that | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-001 | C | register myself (steam ↔ discord) with my explicit consent | link my AoE2 profile with no privacy surprise | RG-REG-1, SC-001/002 |
| US-PONG-002 | C | enroll in the season by validating the rulebook (a traced version) and declare my availabilities | play the season having accepted known rules | RG-REG-2 |
| US-PONG-003 | C | self-declare my level ("I play above/below my Elo") | be placed at my real height from round 1 | D-PONG-013, RG-REG-2 |
| US-PONG-004 | P | receive my weekly match ("this week, vs Y") with no position and no move up/down displayed | play without ranking pressure | RG-TAB-5, D-PONG-014, SC-004 |
| | US-PONG-005 | P | have a dedicated table channel whose pinned welcome panel holds everything: both players tagged by Discord id, handbook and preset links, round end date, the command list with an example each, the admin role tag, and a kindness reminder | know everything needed to play without rereading the rulebook | RG-CDRAFT-1, RG-MDRAFT-1/2, D-PONG-035, SC-004 |
| | US-PONG-006 | P | agree on a slot in my table channel and publish it with `/update_date` (Discord timestamp): the round's schedule board updates our line, read-only for everyone | agree on a slot without DM ping-pong | D-PONG-032, SC-032 |
| US-PONG-007 | P | declare my result (`3-2`) on my table and have my opponent validate it | close the match with no admin intervention | RG-RES-1/2, SC-007/009 |
| US-PONG-008 | P | contest a wrong result (`/contest_score`, tags an admin) | be protected against false declarations | RG-RES-2 |
| US-PONG-009 | P | declare a forfeit (a "lost" result, no score manipulation) | cleanly give up an impossible week | D-PONG-011-1, SC-016 |
| US-PONG-010 | P | resign mid-set with the score completed (remaining wins to the opponent) | stop a lost set without a dispute | D-PONG-011-3, SC-017 |
| US-PONG-011 | P | report "no date found" and let the admin settle on the facts dossier | not carry the arbitration burden | D-PONG-011-2, SC-018 |
| US-PONG-012 | P | play inside the ±3-day grace and know my movement will defer by one round | absorb the unexpected without blocking the chain | D-PONG-012, SC-023 |
| US-PONG-013 | P | read my recap on demand (`/recap`, ephemeral reply visible only to me) | track MY progress without being judged (or judging myself) | D-PONG-014, SC-024 |
| US-PONG-014 | P | receive my final recap as a DM at season close, with a resend button in `pong:bot-commands` if my DMs are closed | keep a trace of my season | D-PONG-014/021, SC-024 |
| US-PONG-015 | P | report an unplayable civ preset (≥ 3 unowned civs) or a non-conforming map draft (3 bans ≠ 1 category) | play under valid conditions | RG-CDRAFT-2, RG-MDRAFT-2, SC-013 |
| US-PONG-016 | P | leave the tournament between rounds, self-service (`/unregister_from_tournament`), and receive my closed recap | leave without penalising my opponents or the structure | D-PONG-017/023, SC-021 |
| US-PONG-017 | P | volunteer for a make-up match against an orphan (no table movement, recap only) | help the community never leave a player alone | D-PONG-018/019, SC-022 |
| US-PONG-037 | P | self-withdraw from the season in one of two modes: scheduled (effective next round, my running match plays out and its result counts, no forfeit) or immediate (forfeit on my running match, replacement through the parity chain) | leave mid-season without penalising my opponent | D-PONG-023, SC-025 |
| US-PONG-018 | W | be drafted as a replacement at a leaver's exact slot | play the season without disrupting the tables | D-PONG-017, SC-021 |
| US-PONG-019 | W | be inserted as a duo ("half table") at our level and play our match from the running round | enter mid-season like a normal table | D-PONG-016, SC-020 |
| US-PONG-020 | W | join the waitlist once enrollment is closed and be visible for the admin pairing | not miss the season over a few late days | D-PONG-015, SC-019 |
| US-PONG-021 | K | announce my cast (open stream, "AOE Pong" title) | cast freely | RG-REC-2 |
| US-PONG-041 | K | plan a Discord event for the games I cast and get it announced automatically when it starts | get extra visibility without spamming by hand | D-PONG-025, SC-028/029 |
| US-PONG-043 | K/P | register as a caster for a tournament, cumulable with my player role, and get the caster surface (records, casting, table channels) | cast the games I want without being a player | D-PONG-027, SC-030 |
| | US-PONG-022 | S/P | read the standardised records packs (`Round X Table X: P1 ‖ S ‖ P2` + zip) | review/arbitrate matches spoiler-free | RG-REC-1, D-PONG-010 |
| US-PONG-044 | P | see the round's schedule board, updated by the bot from both players' `/update_date`, and get a T-48h reminder in my table channel when no date is set | never ghost a match by accident | D-PONG-032, SC-032 |
| US-PONG-045 | S | read every validated match's bot-authored result card in the results channel (map draft, civ draft, score in a spoiler, records link) | follow the tournament spoiler-free | D-PONG-033, SC-033 |

## Admin journey (facts stated, decision by a human)

| ID | As | I want | so that | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-023 | A | open a season: seed draw (ladder + human), round 1 pairing (seed-adjacent), channel provisioning | launch the competition with confidence | RG-STRUC-1, D-PONG-020, SC-004 |
| US-PONG-024 | A | correct a player's seed (before the draw, between rounds) in the console | fold in field feedback without publishing seeds | D-PONG-013, RG-ADM |
| US-PONG-025 | A | pair the waitlist candidates into insertion duos, with human-seed side-by-sides | decide entries with informed feel | D-PONG-015, RG-ADM |
| US-PONG-026 | A | validate the bot's proposed insertion point for a duo | insert without roughing up the chain | D-PONG-016, SC-020 |
| US-PONG-027 | A | validate a departure on the facts dossier (played matches, pending) and trigger the parity chain (waitlist → voluntary match → fuse) | handle departures humanely in 2 clicks | D-PONG-017/019, SC-021/022 |
| US-PONG-028 | A | apply an admin win/loose on time-stamped facts (30-min lateness, rescheduling <24h, no date) | arbitrate fast and traceably | D-PONG-011-2, SC-018 |
| US-PONG-029 | A | block tables against moves up/down (anti-rematch), the block locking the `semi_blocked` group | avoid unwanted re-series | RG-TAB-2 |
| US-PONG-030 | A | regen a non-conforming civ draft from the report button | keep the tables playable | RG-CDRAFT-2 |
| US-PONG-031 | A | decide the patch policy mid-tournament | not freeze the competition on a game update | RG-ADM |
| US-PONG-032 | A | pull a table's fact thread from the console on demand (timestamps, states) | arbitrate disputes with evidence | RG-ADM, D-PONG-004 |
| US-PONG-033 | A | see the seeds/positions in the console (the only place where the order exists) | administer without exposing it to players | RG-TAB-5 |
| US-PONG-038 | A | withdraw a player from the season (console op `remove_player`) | handle contentious cases | D-PONG-023, SC-026 |
| US-PONG-039 | A | be notified when a member leaves the server: automatic withdrawal from the active seasons, immediate forfeit, replacement attempt at the exact slot, profile kept | not manage silent walk-outs by hand | D-PONG-024, SC-027 |
| US-PONG-040 | A | choose the caster-events announcement channel in the season-creation view: an existing channel, one to create, or off (feature disabled) | decide where event announcements land, per season | D-PONG-025, SC-029 |
| | US-PONG-042 | A | export the enrolled roster (Discord nickname, in-game nickname, 1v1/max Elo, tournament seed) into a staff-restricted channel | work from a full roster without exposing seeds to players | D-PONG-027, SC-031 |
| US-PONG-046 | A | provision the whole tournament surface from the creation view (news, events, infos, media-kit, register, schedule board, results, roster, staff space, optional cast studio) and edit it after creation | open a tournament in one flow | D-PONG-028/030/034, SC-034 |

## Platform journey (the mod itself)

| ID | As | I want | so that | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-034 | system | open/close rounds automatically (timer + grace), self-heal the channels/pins at boot | run without manual supervision (no more S5 manual management) | RG-STRUC-1, SC-004/014/015 |
| US-PONG-035 | system | compute movements per the season's `move_policy` (alternating S1 classic, S2 semi_blocked, ...) | run the pong without human error | D-PONG-006/012, SC-005/006 |
| | US-PONG-036 | system | keep the whole journey auditable: admin logs, seeds persisted per round/table (replayable drafts), nothing silent | earn the community's trust | D-001..004, SC-014 |
| US-PONG-047 | system | archive round-closed table channels read-only and purge them after `archive_retention_days` | keep the guild under the platform channel caps without losing history | D-PONG-031, SC-035 |

> The "system" stories 34-36 trace the automation; the rests of the
> manual S5 flow (fuse, half tables, voluntary matches) live in
> US-017/019/025/027; producing the complete de-sacralisation of
> the admin workload is what motivated this mod.
