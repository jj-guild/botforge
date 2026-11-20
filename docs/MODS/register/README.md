# Register mod

> **⚠️ OUTDATED (2026-11-20)** — this doc set is stale: kept for history, never the source for new work. See the mod-status table in [../README.md](../README.md).

The register mod handles player onboarding: it collects the player's chosen
name and game in a DM workflow, assigns the game's default role, and notifies
the admin team.

## Purpose and goals

- Give every player a unique, human-readable identity on the platform
- Attach players to the games they play (AoE2, Chess, ...)
- Grant the right roles automatically, without admin intervention
- Give admins visibility on new registrations

## User onboarding flow

See the registration workflow in
[../../WORKFLOWS.md](../../WORKFLOWS.md#1-registration-workflow) for the
authoritative step-by-step sequence and diagram.

In short: `/register` → DM name question → name uniqueness validation → DM
game selector → role assignment → confirmation DM → admin notification.

## Role assignment system

- Each game has a default role (e.g., `Player AoE2`), configured in the mod
  YAML (`default_role`, per-game overrides)
- Roles are assigned through the platform abstraction (`IPlatform`
  `assign_role`), never by hard-coded Discord role IDs
- A player can be registered for several games; each grants its role

## Admin notification system

On successful registration, the mod posts a notification to the `ADMIN`
channel category (via `ChannelService`), containing the player name, the
game, and the platform user reference.

## Data stored (UserModel fields)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `platform_id` | str | Platform user identity (e.g., Discord ID) |
| `name` | str | Unique player name (validated for uniqueness) |
| `games` | list[str] | Registered games (`aoe2`, `chess`, ...) |
| `roles` | list[str] | Roles granted at registration |
| `locale` | str | Preferred language (default: guild locale) |
| `created_at` | datetime | Registration timestamp |

## Rules

See [RULES.md](RULES.md) for the enforced rules (name uniqueness, game
selection, role assignment, admin notification format).

## Environment

See [ENVIRONMENT.md](ENVIRONMENT.md) for permissions, channel categories,
and database requirements.
