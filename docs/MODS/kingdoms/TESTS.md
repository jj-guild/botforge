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
