# Pong — REFERENCE (AOE Pong rulebook, the functional source)

> **Source document, translated from the original French**: the official
> AOE Pong tournament rulebook (season 5, "Antre de l'Ours"), provided by
> Aramatu (mod owner). The original rulebook was written in French; this
> is its English translation, kept as the **functional source of truth**
> for the "better, on BotForge" migration. Adapting to BotForge's real
> contracts (ADR-0011 seams, ADR-0020 split, core GameDataService,
> DraftProvider) happens in [RULES.md](RULES.md) and
> [DECISIONS.md](DECISIONS.md), never by editing this reference.
> Gaps/conflicts and non-automatable zones are traced there instead of
> being resolved here.

## AOE Pong (original rulebook, S5)

**Tournament presentation:**

AOE Pong is a tournament meant to give you a competitive frame in which
you can improve on different aspects of the game, and more generally
on tournament preparation.
The goal is to let you play matches regularly, in tournament
conditions, against the opponent closest to your own level.

The idea and the origin of the tournament come from \[TabA\] Zyxuwyz,
who proposed climbs and drops like in ping pong. The winner of a round
moves up, and the loser moves down.
We may decide to block tables against moving up or down to avoid
(re)matches.

**Tournament flow:**

The tournament runs over six rounds spread over six weeks.
You will therefore have one week to play your BO5 match.

> ⚠️ Internal conflict in the source: the presentation announces six
> rounds over six weeks, while the "Dates and duration" section (S5)
> announces four (Wednesday-to-Tuesday rounds). Used as a **config
> parameter** (`rounds_per_season`), the value settled by the mod
> owner; see [DECISIONS.md](DECISIONS.md).

At the start of each round, for every table, we will ban in an
automated and random way the number of civilizations required so that
only 15 remain at your disposal. We will communicate the draft-civ
preset linked to your table at that time. Afterwards we stay more
classic: the map draft and the civ draft run as in every other
tournament.

Player A is the first player announced on the table, player B the
other one. Player A hosts the map draft. Player A hosts the civ
draft.

The last map picked in the draft is the neutral map, meaning the
first map played.

Map draft link: https://aoe2cm.net/preset/pGWoJ

**Map draft specifics:**

Each player's **three first bans** amount to one category ban. They
must therefore hit maps from the **same** category. Any draft not
respecting this rule is considered invalid and must be redone from
the start.

**Map-picking specifics:**

The loser picks the next map among all available ones (i.e. not
already played), even among the ones their opponent drafted.

**Enrollment (automatable excerpt):**

- `/register` on the #bot-commands channel: registers the player,
  links steamID ↔ discordID + AoE2 data (country, elo). Explicit
  consent required (database storage).
- Discord nickname = in-game nickname required (renaming requested
  otherwise).
- Two consecutive 3-hour availability windows per week within
  17:00-23:00 (FR timezone) asked from participants.
- `/register_to_tournament` with the name "AOE Pong S5" +
  `rules: True` validation (the rules read are accepted). Any
  enrollment change notified to an admin. Admins can refuse an
  enrollment.
- Discord presence required at the start (exclusion otherwise).

**Dates and duration (S5):** Wednesday-to-Tuesday rounds; Round 1:
Wed 3 June → Tue 9 June 2026, then one round per week (Wednesday to
Tuesday), four rounds in S5.

**Round flow:**

- **Scheduling**: on Wednesday, the admin publishes the table list
  and the civ draft preset. If the preset contains more than two
  civilizations the player does not own, tag an admin for a new
  draft. Players set date/time themselves and inform the admins in
  the tournament section provided for that. Announced absence:
  propose a new date; a request less than 24h before the initial
  match → the opponent can claim the Admin Win. Match not schedulable
  in time: extra delay or Admin Win at the admins' discretion.
- **Lateness**: > 30 minutes late → possible Admin Loose. Announced
  lateness: the opponent may accept it or not, and may claim the
  Admin Win at any time; the admins remain the referees beyond 30
  minutes.
- **Results**: `/add_result` on the table (player A, "X-X" score,
  player B). The second player validates via `/validate_score` or
  contests via `/contest_score` (tags an admin).
- **Records** (casting/admins): post the result in the format
  `AOE Pong Ronde X Table X : Pseudo1 || Score || Pseudo 2` with a
  zip containing a "Drafts" text file (map and civ drafts) + the
  games renamed `AOEPong_Pseudo1_vs_Pseudo2_Game_X.aoe2rec`.

**General rules (mod-related excerpts):**

- No voluntary bug use; patch: old/new choice at the admins'
  discretion during the event.
- Cheating: immediate disqualification + ban from future events; no
  third-party communication allowed during a game; written agreement
  required to stream one's POV (streaming "on mute"); account sharing
  forbidden.
- Behaviour: respect required from everyone (players, admins,
  casters); arbitration and sanctions (warning → exclusion) reserved
  to the admins.
- Rulebook modifiable by the admins mid-tournament.

**In-game rules (mod-related excerpts):**

- No restart except an **Admin Restart**: requestable within the
  first 6 in-game minutes for a bugged map generation (missing
  villagers/animals, > 50% of inaccessible ore/forage sides,
  missing relics, trapped unit, non-conforming generation). After a
  restart: same civilizations and colours.
- **Laming** (forum-less maps, 3 villagers, up to 3 min in-game or
  end of the treaty): forbidden to attack villagers/buildings/
  animals, wall enemies/resources/relics/animals in, drop Town
  Centers within range of each other (admin-re if a blind TC), kill
  an animal without taking 35 food from it; stealing sheep/cows/
  chickens allowed. Elsewhere: every form of laming allowed.
- **Pause**: pausing allowed only for an issue affecting the ability
  to play; interruption mandatory on admin request; the player who
  paused resumes (after the opponent's agreement); reasonable pauses.
- **Settings**: normal ladder settings (reference: the original
  rulebook screenshot). **S5 map pool**: mod
  https://www.ageofempires.com/mods/details/503568/ (22 maps listed
  in the source: African Reed Beds, African River, Arena, Bypass,
  Cliffbound, CoastToMountain, Dzimbabwe, Dzong, Fernando de Noronha,
  Fortified Clearing, Frigid Lake, Ishtmus, Land Madness, Morass,
  Nomad, Northern Crossrings, Quebrada de Cafayate, Ring of Reeds,
  Slopes, Stranded, Te Fiti...). **TO BE DEFINED**: the per-season
  map pool is read from the core (`GameDataService`), never
  hard-coded in the mod.
- **Streaming**: open stream; any streamer may cast; "AOE Pong" in
  the stream title required.

**Contacts (S5)**: Aramatu, Elhyar, Phare_Macie, Scramble (Discord
admins).
