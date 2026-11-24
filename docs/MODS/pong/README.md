# Pong mod (montante/descendante ladder, "ping-pong style")

> Scaffolded from `docs/MODS/TEMPLATE/README.md`. This README is the
> mod's lore doc: the agent reads it in full at every session on the
> mod (mod-lore skill). The functional source is the AOE Pong
> tournament rulebook, archived in [REFERENCE.md](REFERENCE.md); zones
> marked **TO BE DEFINED** must never be invented by an implementation.

## Purpose and concepts

AOE Pong is a **regular competitive tournament**: it gives players a
weekly tournament frame to improve, against the opponent closest to
their own level. The central concept comes from the tournament's
origin (\[TabA\] Zyxuwyz): **climbs and drops like in ping pong**;
the winner of a round **moves up** one table, the loser **moves
down**.

Concepts (the game's own names):

- **Table**: the weekly 1v1 duel; on Discord, a table channel opened
  when the round opens and closed when it closes;
- **Round**: one week of play (default Wednesday to Tuesday), match
  played as a BO (`bo_format`, default BO5);
- **Season**: `rounds_per_season` rounds (name of the form
  "AOE Pong S<N>"), with its own map pool and presets;
- **Civ draft**: automated random ban per table down to
  `civs_remaining` (default 15) civilizations left, one draft-civ
  preset per table;
- **Map draft**: run "as in every other tournament"; each player's
  three first bans = one common category;
- **Neutral map**: the last map picked in the draft is the first map
  played; the loser picks every following map;
- **Casting / records**: open stream, results posted in a
  standardised format with the drafts and recording zips.

One-line lore: a den where you climb or drop a table every
tournament week, the way ping-pong steps go up and down, so you
always play the opponent closest to your level.

## Channel tree: channels, categories, roles

Discord layout of the mod (declared in `conf/mod.yaml`):

Categories / groups:

- `pong:admin` ("AOE Pong — Staff", admin_only): mod console, admin
  fact threads;
- `pong:ladder` ("AOE Pong"): channels visible to enrolled players;
- `pong:tables` ("AOE Pong — Tables"): the per-round generated
  table channels.

Channels:

- `pong:announcements` ("annonces-pong", text, player access) in
  `pong:ladder`: round open/close announcements, Wednesday table
  list and presets;
- `pong:bot-commands` ("bot-commands", text): mod slash commands
  (`/register_to_tournament`, ...);
- `pong:planning` ("planification", text, one thread per match):
  scheduling, date/time fixes and admin heads-up;
- `pong:records` ("records", text): standardised result posts +
  draft/recording zips, feeds casters and admins;
- `pong:casting` ("casting", text): cast announcements;
- `pong:table_<slug>` (**generated** table channels, one per active
  table, opened at round start, archived/closed at round close) in
  `pong:tables`.

Roles (standard trio + mod-specific extras):

- `candidate` (display: Pong Candidat): registration done
  (RG-REG-1), not yet enrolled in the current season;
- `member` (display: Pong Joueur): enrolled player of the season;
  granted by season enrollment (RG-REG-2), removed at season close;
- `admin` (display: Pong Admin): access to `pong:admin`, console,
  admin validations;
- `pong_waitlist` (display: Pong Waitlist): candidate enrolled after
  the registration window closed (D-PONG-015), waiting for a pair
  (RG-TAB-3/4);
- `pong_caster` (display: Pong Caster): cast announcement access
  (open stream, descriptive role).

Machine-room rule: `pong:admin` is staff-only while the mod is
installed (admin fact-thread dossiers); installing the mod asks for
admin confirmation (gate), and uninstalling closes the active table
channels and removes `member`.

## External system integration

- **Game-bound**: yes, the mod is tied to AoE2 (`game_key: aoe2`,
  like the kingdoms mod): the season's civ/map draft presets and BO
  formats; the old den (S5) was exclusively AoE2.
- **What the mod reads from the core** (never owned/duplicated): the
  civilization, map and season map-pool catalog via
  `GameDataService`; profiles (elo, country, steam_id, discord_id)
  via the core profile route. The mod stores no game-data civs or
  maps.
- **External providers**: aoe2cm (map/civ draft presets,
  `draft_map_preset` config; the mod **generates the preset link**,
  it does not manage the external platform); aoe2lobby/LibreMatch
  later for automatic results (out of v1 scope).
- **Core seams**: season registry with the visible game-scoped id
  `pong-aoe2-<guild id>-<index>`; entity forums (one planning
  thread per match); the core `[game key]-maps` forum sync for map
  topics (read-only for the mod).

## Views, buttons and actions of the mod

Views (R9 naming contract, `conf/views.yaml`):

- `menu:mod:pong:home` (menu): the mod home; active season, role,
  own table; pinned via `pong:announcements`;
- `panel:mod:pong:table` (panel, dynamic by table): the table
  panel; players A/B (A hosts both drafts), the table's civ preset,
  neutral map, remaining maps if tracked, A/host rules reminders,
  result state (`PENDING`/`VALIDATED`/`CONTESTED`), table action
  buttons;
- `panel:mod:pong:round` (panel): the running round; every table,
  pending scores, round deadline;
- `panel:mod:pong:standings` (panel): the global results view;
  per-table record, previous round moves;
- `panel:mod:pong:table:draft` (panel, **TO BE DEFINED**): the
  internal draft surface (if kept in DECISIONS); bans/picks with the
  "3 bans = 1 category" rule applied by the mod;
- `panel:mod:pong:admin:console` (SDK-owned console): the mod ops
  (see below).

Buttons/actions (custom id `<mod>:<component>:<payload>`, template
`.+`):

- `pong:register:<discord_id>`: start the registration (privacy
  gate before persistence, RG-REG-1);
- `pong:register_season:<season_id>`: season enrollment with
  `rules: True` and the availability statement (RG-REG-2);
- `pong:add_result:<table_id>`: result declaration (player A /
  score / player B modal, RG-RES-1);
- `pong:validate:<result_id>` / `pong:contest:<result_id>`:
  validation/contest by the second player (RG-RES-2; a contest tags
  the admins);
- `pong:report_preset:<table_id>`: "preset with > 2 unowned civs"
  report, tags an admin (RG-CDRAFT-2);
- `pong:report_draft:<table_id>`: "non-conforming draft" report,
  tags an admin (RG-MDRAFT-2, if the draft is external);
- `pong:record_template:<table_id>`: generates the records-message
  template + zip handling (RG-REC-1);
- `pong:announce_cast:<table_id>`: cast announcement in
  `pong:casting` (RG-REC-2);
- `pong:update_entry:<discord_id>`: registration update, tags an
  admin (RG-REG-2);
- `pong:resend_recap:<discord_id>`: re-send the closing recap when
  the player's DMs are closed; ephemeral notice fallback in
  `pong:bot-commands` (D-PONG-021).

Guards: admin check at click time (never at render) for every console
op; confirm cards for admin mutations (block a table, apply an admin
win/loose, invalidate a result); modals for `/add_result` and
enrollment.

Admin console (`mod="pong"`): `open_season`, `open_round`
(creates tables/channels + civ bans + presets), `close_round`
(closes the table channels), `block_table` (move up/down,
RG-TAB-2), `admin_result` (admin win/loose, RG-ADM),
`arbitrate_result` (validate/invalidate/redeclare, RG-RES-2),
`redraft_preset` (RG-CDRAFT-2), `patch_policy` (RG-ADM),
`reset_table`, `reload_season_config` (per-season map pool
preset), `remove_player` (withdraw a player from the season,
D-PONG-023); every op is logged (confirm card + mutation log).

## Pinned channels

- `menu:mod:pong:home` pinned in `pong:announcements`;
- `panel:mod:pong:round` pinned in `pong:ladder` (season home
  channel);
- lifecycle: pin created when missing, refreshed in place on every
  change, restored if the channel is deleted (boot self-heal),
  swept on mod uninstall.

## Player / admin / bot interactions

- **player**: links their identity through the core
  (`/home` > Profil), registers via the `register-as-a-player`
  front door (consent gate, RG-REG-1), then `/register_to_tournament`
  (RG-REG-2, availability modal); checks their table
  panel (A/B, host, preset, neutral map); declares the result on
  their table (`/add_result`, guard: author = player A or B of the
  table, round open, X-X score format); validates or contests their
  table mate's result; reports a preset (> 2 unowned civs) or a
  non-conforming draft; generates their records template; announces
  their cast; updates their registration (tags an admin);
  self-withdraws from the season (`/unregister_from_tournament`,
  admins notified, D-PONG-023).
- **admin**: console: season open, round open (tables + civ bans +
  presets), round close, table blocking, admin win/loose on the
  mod's time-stamped facts (30-min lateness, rescheduling under 24h,
  no scheduling), contest arbitration, preset regen, patch policy,
  player removal (D-PONG-023); every mutation has a confirm card and
  a log; NO dispute automation (facts stated, human decides);
- **bot**: boot passes: self-heal of missing channels/pins, table
  reconcile (a channel exists for every open round), role heal;
  scheduled loops: round open/close (Wednesday to Tuesday), Wednesday
  announcement (tables + presets), deadline reminders; no unrendered
  exception ever: every pass posts its report (in
  `pong:announcements` or a fact thread, never log-only); archival
  pass of closed table channels; guild-leave watcher: a member
  leaving the server is auto-withdrawn from the active seasons with
  an immediate forfeit and a replacement attempt at the exact slot,
  player profile kept (D-PONG-024); caster-event loop: a
  caster-planned Discord event starting triggers an automatic
  announcement in the events channel chosen at season creation
  (D-PONG-025).

## Usage

> Slice v1 (D-PONG-037): only `/home` and `/admin` are live — the mod
> registers no command. The flows below land step by step, as declared
> action buttons on the auto-generated menus first.

```text
/home > Profil                # core identity link (steam <-> discord, AoE2 profile)
pong:register (front door)    # player registration (consent required)
/register_to_tournament       # enroll in the active season (rules: True)
/unregister_from_tournament   # self-withdraw from the season (admins notified)
/add_result                   # declare a result on the table (X-X)
/validate_score               # validate the declared result
/contest_score                # contest it; tags an admin
```

## See also

- [REFERENCE.md](REFERENCE.md): the official AOE Pong rulebook (source)
- [RULES.md](RULES.md): the game rules (automatable/testable)
- [ENVIRONMENT.md](ENVIRONMENT.md): the configuration + season config
- [DECISIONS.md](DECISIONS.md): the validated decisions (they win)
- [TESTS.md](TESTS.md): the validation scenarios
- [../CATALOGUE.md](../CATALOGUE.md): the mod's catalogue entry
- [../../WORKFLOWS.md](../../WORKFLOWS.md): the related platform workflows
