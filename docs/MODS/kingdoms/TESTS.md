# Kingdoms mod — test scenarios

The scenarios that validate/secure the kingdoms implementation. Each has
one test in `modules/mods/kingdom/tests/test_scenarios.py`
(botforge-services), run by CI; the botforge docs check fails if a
scenario here has no test.

## SC-KING-001 — the admin salon is `console`, no `settings` salon remains

- **Given** the mod declaration `conf/mod.yaml`
- **When** the channels are listed
- **Then** `console` is declared and `settings` is gone (the old slug is
  swept as undeclared at the next provisioning)

## SC-KING-002 — every declared view id follows the R9 contract

- **Given** `conf/views.yaml`
- **When** its view ids are read
- **Then** all start with `panel:mod:kingdom:` or `menu:mod:kingdom:`

## SC-KING-003 — the console ops are scoped to the mod console

- **Given** the kingdom console actions
- **When** they are built
- **Then** all 7 (relaunch/reset/clock/debug-status/bypass-on/bypass-off/
  skip-event) carry `mod="kingdom"` — they never render in the global
  `panel:admin:console`

## SC-KING-004 — the wired console surface is the SDK one

- **Given** the settings/console panel
- **When** its view key is read
- **Then** it is `panel:mod:kingdom:admin:console`
  (`mod_console_view_id("kingdom")`)

## SC-KING-005 — service errors always answer the user, translated

- **Given** a `KingdomError` with a stable code (e.g. `NoSeasonError`,
  `KingdomLimitError`)
- **When** the console/panel catches it
- **Then** `service_failure_note` maps the code to `settings_err_<code>`
  in both fr and en — the user gets an answer, the log is never the only
  report

## SC-KING-006 — modals build without deprecation warnings (discord.py 2.7)

- **Given** the four settings modals
- **When** they are built under `simplefilter("error", DeprecationWarning)`
- **Then** no warning: every TextInput rides a `discord.ui.Label` ≤ 45 chars

## SC-KING-007 — the admin-debug toolkit builds from the mod stack

- **Given** a mod stack (`mod_service("kingdom").stack()`)
- **When** `build_debug_service(stack)` runs
- **Then** the DebugService exposes the ported ops (list_attacks,
  view_cooldowns, skip_to_next_event, grant_bird, …)

## SC-KING-008 — the attack phases loop imports cleanly

- **Given** the phases cog
- **When** it is imported
- **Then** no ImportError (sibling imports resolve)

## SC-KING-009 — locale parity fr/en

- **Given** `conf/locales/fr.yaml` and `en.yaml`
- **When** their key sets are compared
- **Then** they are identical

## SC-KING-010 — the mod's pins are declared

- **Given** the cogs package
- **When** its static pins are registered
- **Then** attack, candidates, apply, register, console, time-machine,
  distributor, validation and market pins are all declared
## SC-KING-011 — season durations derive from the active preset

- **Given** the time-machine cockpit (preset official or beta)
- **When** the panel labels are built
- **Then** the season length reads the active preset: official = 3 weeks
  (config `weeks` matches D55), beta shows the real compressed plan in
  hours (e.g. `52h (compressed beta)`), never a hardcoded text
- **And** the setup phase line carries the rhythm phrase (cycles from the
  crons, or the beta plan `T0+4h… T0+52h`)

## SC-KING-012 — the time-machine pin auto-refreshes

- **Given** the pinned time-machine panel
- **When** the refresher pass runs every 5 minutes
- **Then** the machine pin is re-ensured, and a pass with an unchanged
  fingerprint makes no Discord API call (since pins-heal-v1 the pass
  actually walks every kingdom pin — see SC-KING-015)
## SC-KING-013 — the admin salon wears the ⚙️ paramètres name

- **Given** the admin category's console salon (key `console`, SC-KING-001)
- **Then** its declared display name is **⚙️ paramètres** (the 08/11
  reference capture) and the pinned panel titles
  « ⚙️ Kingdoms — paramètres » with an « Administration » section header
- **And** the strings exist in full fr/en parity (`settings_section`)
## SC-KING-014 — the boot pass provisions the declared salons before pinning

- **Given** a served guild that never received the mod's provisioning
  (legacy salons, no ⚙️ paramètres)
- **When** the once-per-boot self-heal pass runs
- **Then** it provisions the declared roles then channels (the Repair-click
  seams) BEFORE ensuring the pins — the pins land in salons that exist
- **And** `BOTFORGE_KINGDOM_BOOT_PROVISION=off/0/false` skips the
  provisioning (pins/commands passes stay) — the report says « off »

## SC-KING-015 — a lost pin heals within one refresher cycle

- **Given** a guild where a boot pin was lost (best-effort pass dropped
  in provisioning's API storm — an empty admin salon)
- **When** the 5-minute refresher pass runs (`run_mod_pin_refresh_pass`)
- **Then** EVERY pin of scope `mod/kingdom` is re-ensured per guild
  (console, machine à temps, distributeur), best-effort per spec
- **And** foreign-scope pins are never touched; steady state costs zero
  Discord API call (fingerprint guard)
- **And** `BOTFORGE_KINGDOM_PIN_REFRESHER=off/0/false` disables the pass
  (legacy `BOTFORGE_KINGDOM_MACHINE_REFRESHER` still honored)

## SC-KING-016 — founding a realm provisions it dormant (never engages)

- **Given** a player who founds a realm (the camp's founding modal,
  royaume-persistant-v1)
- **When** the founding completes
- **Then** the realm shell PERSISTS (name, Roi, members, presentation,
  salons — the season wipe NEVER drops it) and the 🏰 category is
  provisioned in DORMANT mode: only 🏰 Le royaume shows (Discussions /
  Territoire / Alliances are masked, never destroyed)
- **And** the 🏰 Entrée button opens the chez-soi window: Ma
  seigneurie + 📝 Présentation + 📺 Voir la saison + 🏆 Palmarès +
  🚪 Quitter
- **And** the Roi's « Voir la saison » records a join request — an
  admin accepts the season entry (the draft starter, tranche 2)
