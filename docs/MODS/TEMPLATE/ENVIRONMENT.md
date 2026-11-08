# Template — Mod Environment

Describe the mod environment and configuration here.

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Whether the mod is enabled |

## Channels and roles

List the channels and roles the mod **declares** in its YAML config
(`config/mods/<mod>.yaml`). Channels are addressed by mod-scoped category
keys (`mod:key`, e.g. `ladder:ladder_rankings`); roles by logical role keys
(e.g. `ladder_participant`). The core provisions them automatically via
`ModRegistry` + `ChannelService`/`RoleService` (botforge-services#26) —
never list platform-level categories here unless the mod also uses one
(e.g. `REPORTS`).
