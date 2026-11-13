# Mods

BotForge uses a **modular architecture**: each game feature (register, ladder,
clans, ...) is a separate mod built on the generic core. This directory is
where the game designer defines and evolves mod rules and environments —
without coding.

## Mod system overview

A mod is a self-contained feature that:

- declares its configuration in YAML — modular layout
  `botforge-services/modules/mods/<mod>/mod.yaml` (one self-contained
  directory per mod, botforge#179) or legacy
  `botforge-services/config/mods/<mod>.yaml` (supported, priority on
  collision during the migration)
- implements its logic against the generic core (`IPlatform`,
  `WorkflowEngine`, `ChannelService`) — never against a specific platform
- documents its rules and environment here, in `docs/MODS/<mod-name>/`
  (following [TEMPLATE/](TEMPLATE/))

#### Game-bound mods

A mod is normally game-agnostic (it may declare `allowed_games`, but its
logic never depends on one game's data). Some mods are **game-bound by
design**: their whole concept targets a single game (e.g. `kingdoms` is
AoE2-only, because its map/civilization meta-game only makes sense there).

A game-bound mod MAY hard-code its game key and game-specific options,
but it MUST NOT own its game data:

- the game catalog (maps, map pools, civilizations) is owned by the core
  `GameDataService` — the mod reads it and never duplicates it
- seasons are registered in the core season registry with a visible,
  game-scoped id (`<mod>-<game key>-<guild id>-<index>`) — the mod never
  runs its own season numbering
- Discord surfaces (forum topics such as `<game key>-maps` and
  `<game key>-map-pools` in the `games` category) are provisioned by the
  core forum syncs — the mod grafts onto them and never creates them

### How mods integrate with the workflow engine

Multi-step interactions (registration, match reporting) are declared as
workflows and executed by the core `WorkflowEngine`, which persists their
state so flows survive restarts (see
[ADR-0002](../DECISIONS/002-workflow-engine.md)). UI components feed events
back into the running workflow via the `custom_id` convention (see
[architecture/discord.md](../architecture/discord.md)).

### Mod lifecycle

1. **Load**: the bot reads mod declarations (`config/mods/*.yaml`) at startup
2. **Initialize**: enabled mods register their commands and workflows
3. **Execute**: user interactions drive mod workflows
4. **Cleanup**: on shutdown, in-flight workflows are persisted and can resume

### Mod configuration format (YAML)

```yaml
mod:
  name: register
  enabled: true
  settings:
    default_role: "Player"
    admin_notifications: true
    allowed_games:
      - aoe2
      - chess
```

### Extending core functionality

Mods extend the platform by combining core services:

- new workflows → `WorkflowEngine`
- new destinations → `ChannelCategory` via `ChannelService`
- new persistent data → MongoDB models
- new hot state → Redis keys through `StateService`

```mermaid
flowchart TD
    A["Core System"] --> B["ModRegistry loads config/mods/*.yaml"]
    B --> C{"Mod enabled?"}
    C -->|No| X["Skip (startup warning if depended on)"]
    C -->|Yes| D["Provision declared channels and roles"]
    D --> E["Register declared commands and workflows"]
    E --> F["Mod workflows run on the WorkflowEngine"]
    F --> G["Core models and services"]
    G --> H["MongoDB / Redis"]
```

## Available mods

The repo provides the generic mod tooling: the `config/mods/_example.yaml`
declaration template and the `ModRegistry` (botforge-services#26). Each mod
lands with its own issue, implementation and documentation set.

## Starting a new mod

Never improvise a mod's bootstrap: run `botforge mod init <name>` — see
the reference guide [GUIDES/mod-init.md](../GUIDES/mod-init.md)
(layout, command, ladder & kingdoms as real examples).

## Mod catalogue

Every mod — developed, scoped, specified, shaped or a vague idea — is listed
with its maturity level, categories and links in the
[**mod catalogue**](CATALOGUE.md). The catalogue is the game designers'
entry point for browsing and **prioritizing** ideas; the linked issue or doc
holds the decisions. The register, ladder and kingdoms design docs live
under [register/](register/), [ladder/](ladder/) and [botforge/](botforge/) —
they describe the target behavior, not shipped code.

## Mod version history

Mod rule and environment changes are tracked per mod (`register/CHANGELOG.md`)
and in the [roadmap](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md).

## See also

- [TEMPLATE/](TEMPLATE/) — template for new mod documentation
- [../WORKFLOWS.md](../WORKFLOWS.md) — user-facing workflow reference
- [../ARCHITECTURE.md](../ARCHITECTURE.md) — core components
