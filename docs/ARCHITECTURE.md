# Architecture

This document describes the technical architecture of BotForge: a modular,
multi-platform Discord bot platform. It is the reference for how the three
repositories fit together, how the generic core is organized, and how data
flows through the system.

The **long-term infrastructure vision** (target topology, surfaces,
capacity peaks, hosting options) is held by the architecture committee in
[architecture/vision.md](architecture/vision.md),
[architecture/topology.md](architecture/topology.md) and
[architecture/capacity.md](architecture/capacity.md).

The five architectural pillars:

1. **Multi-platform**: abstraction via `IPlatform` (Discord now, Twitch later)
2. **Modular**: generic core + specific implementations
3. **Workflow-based**: a workflow engine drives interaction sequences
4. **Channel categories**: intelligent message routing; core keeps only platform-level categories (`ADMIN`, `REPORTS`, `LOGS`), mods declare their own (`ladder:ladder_rankings`, ...)
5. **GitOps**: deployment via Docker Compose manifests

## 1. Overview

BotForge is split across three repositories:

| Repository | Role |
| ---------- | ---- |
| `botforge` (this repo) | Source of truth: architecture, workflows, ADRs, mods docs, generated dev docs |
| `botforge-services` | All Python code: generic core, Discord platform implementation, mods, YAML configs |
| `botforge-infra` | Docker, CI/CD, GitOps manifests, deployment scripts |

### Global architecture

```mermaid
flowchart TD
    subgraph Infra["botforge-infra"]
        DOCKER["Docker Compose"]
        CI["GitHub Actions"]
    end

    subgraph Services["botforge-services"]
        subgraph Core["Generic core"]
            IPLAT["IPlatform"]
            CHANSVC["ChannelService"]
            WFENGINE["WorkflowEngine"]
            STATESVC["StateService"]
        end
        subgraph Discord["Discord platform"]
            DPLAT["DiscordPlatform"]
            BOT["Bot entrypoint + cogs"]
            UI["UI components"]
        end
        CFG["YAML config"]
    end

    CI -->|"build and deploy"| DOCKER
    DOCKER -->|"runs"| BOT
    BOT -->|"uses"| DPLAT
    DPLAT -->|"implements"| IPLAT
    UI -->|"feeds events"| BOT
    CFG -->|"loads"| CHANSVC
    CFG -->|"loads"| WFENGINE
    CHANSVC --> IPLAT
    WFENGINE --> STATESVC
    WFENGINE --> CHANSVC
```

### Data flow between repositories

- `botforge` (docs) describes rules and decisions; `botforge-services`
  implements them; `botforge-infra` deploys the implementation.
- Any code change in `botforge-services` or `botforge-infra` must come with — or
  be followed by — a doc update in this repo (see [docs/CONVENTIONS.md](CONVENTIONS.md)).
- Technical docs are generated **in the repository hosting the sources**:
  the pydoc of `botforge-services` is produced by that repo itself
  (`scripts/generate_pydoc.py`, `make docs`) and freshness-checked on every
  one of its PRs.

## 2. Generic core (`botforge-services/src/botforge/core/`)

The generic core contains everything platform-agnostic. Mods and workflows are
written against the core only; they never import Discord-specific code.

### `interfaces/`

All contracts are `typing.Protocol` classes (`@runtime_checkable`):
implementations satisfy them **structurally**, without inheritance —
conformance is verified by mypy strict, not at instantiation time
([ADR-0011](DECISIONS/011-protocol-interfaces.md)).

- **`IPlatform`**: the platform abstraction. Methods cover messaging
  (send/edit/delete), channel management (create/get by category), role
  assignment, and DMs. First implementation: `DiscordPlatform`.
- **`IMessage`, `IChannel`, `IUser`**: platform-agnostic models exchanged
  between the core and platforms. Adapters convert platform objects to these
  models and back.
- **`IWorkflow`**: contract for an interaction sequence (steps, transitions,
  timeouts). Implemented by concrete workflows and executed by the
  `WorkflowEngine`.

```mermaid
classDiagram
    class IPlatform {
        <<interface>>
        send_message(channel, content)
        send_dm(user, content)
        create_channel(guild, category)
        assign_role(user, role)
    }
    class DiscordPlatform {
        +send_message(channel, content)
        +create_channel(guild, category)
    }
    class IWorkflow {
        <<interface>>
        start(context)
        handle_interaction(event)
        steps()
    }
    class WorkflowEngine {
        start_workflow(name, context)
        resume(state)
        handle_interaction(event)
    }
    IPlatform <|.. DiscordPlatform
    IWorkflow <|.. RegistrationWorkflow
    IWorkflow <|.. LadderWorkflow
    WorkflowEngine --> IWorkflow : executes
    WorkflowEngine --> IPlatform : uses
```

### `models/`

MongoDB-backed persistence models (MongoDB is used for schema flexibility —
workflow payloads evolve with the game rules):

- **`UserModel`**: platform user identity, registration data, per-game profiles
- **`GuildModel`**: per-server configuration (locale, channel category mapping)
- **`ChannelModel`**: channel registry keyed by `ChannelCategory`
- **`WorkflowState`**: persisted workflow instances (current step, payload,
  status) so flows survive restarts
- **`db.py`**: MongoDB client setup — singleton sync (`MongoClient`) and async
  (`AsyncMongoClient`, the native pymongo async API — no Motor dependency)
  clients configured from `MONGO_URI`/`MONGO_DB`; models expose
  `to_mongo()`/`from_mongo()` for lossless document round trips

### `services/`

- **`ChannelService`**: channel category management. Mods ask for a channel by
  category, never by name or ID. Resolution order: cache → database → platform
  creation.
- **`IdentityService`** (botforge-services#130): internal `user_id` ↔
  platform account resolution. Identities are multi-platform by design — one
  BotForge user may be bound to accounts on several platforms; the binding
  lives in its own `platform_identities` collection, never in mod data. Mods
  reference users by `user_id` only. Cache-aside (Redis → MongoDB), idempotent
  `get_or_create_user` per `(platform, platform_user_id)`.
- **`MessageRegistryService`** (botforge-services#130): the **only** place
  platform message IDs ever live — `(platform, message_key, entity_id)` →
  `(channel_id, message_id)`. Mods register persistent messages by logical key
  and resolve them back to re-render in place; re-registration replaces
  (messages are recreated, not patched). Mod collections never store message or
  channel IDs. Complements the `custom_id` state reconstruction
  (§ *Persistent components*): reconstruction survives component clicks, the
  registry lets a mod find its own message back.
- **`SurfaceService`** (botforge-services#130): named surfaces — a mod's
  declared channel categories resolved through the ChannelService seam
  (`surface_channel`), and surface permission queries (« is ladder
  admin/player ») delegated to the runtime PermissionService
  (`has_surface_role` — failure denies, never opens).
- **`StatusService`**: operational report (version label, uptime, configured
  games, enabled mods with their declared channels/roles, bot admins,
  deploy label + URL) — powers the generic `/status` command.
- **`AdminService`** (botforge-services#35): distinguishes **bot admins**
  (operators, defined by the `BOT_ADMINS` environment variable — provisioned
  as a GitHub environment *variable*, not a secret, since user IDs are not
  sensitive) from **guild admins**
  (guild-scoped: platform permissions or mod-declared admin roles). Bot
  admins operate the bot; guild admins administer their guild only.
- **`WorkflowEngine`**: workflow execution. Declares nothing itself; loads
  workflow definitions, drives step transitions, persists state through
  `StateService`, and dispatches UI events to the right running workflow.
- **`StateService`**: state management in Redis for hot data (current step,
  short-lived payloads), with MongoDB as durable backing store.

### `enums/`

- **`ChannelCategory`**: platform-level routing keys (`ADMIN`, `REPORTS`, `LOGS`); mod-scoped categories are declared per mod (`mod:key`)
  used by `ChannelService`
- **`PlatformType`**: `DISCORD`, `TWITCH`, ...
- **`WorkflowStatus`**: `PENDING`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`,
  `TIMED_OUT`

## 3. Discord implementation (`botforge-services/src/botforge/discord/`)

### `platform/`

- **`DiscordPlatform`**: implements `IPlatform` on top of discord.py
- **`adapters.py`**: converts discord.py objects (`Message`, `TextChannel`,
  `User`/`Member`) to core models (`IMessage`, `IChannel`, `IUser`) and back

### `bot/`

- **`main.py`**: entry point — loads config, wires the core services, starts
  the Discord client, syncs slash commands on ready (guild-scoped when
  `CICD_GUILD_ID` is set, global otherwise)
- **`cogs/`**: Discord mods (`register.py`, `ladder.py`, ...). Each cog maps
  commands and interactions to core services; no game logic lives in cogs.
- **`status.py`**: the generic `/status` command — bot and per-guild
  operational report (uptime, version, Discord gateway latency, deploy
  link, games, enabled mods with their declared channels/roles, and one
  merged Admins bullet list of bot admins (`BOT_ADMINS`) and the invoking
  guild's admins as Discord mentions). Not a mod: it is a platform
  capability, gated by admin levels (botforge-services#35). Every link is
  rendered with a short label, never a bare URL. The Version field is a
  labeled GitHub link built from `BOTFORGE_DEPLOY_LABEL` +
  `BOTFORGE_DEPLOY_URL`: the services source tree at the deployed commit
  for PR and main deploys (`pr-<id>-<timestamp>-<sha7>`, `main@<sha>`), the
  GitHub release for `vX.Y.Z` (botforge-infra#39). The Deploy field links
  the botforge-infra deploy job itself (`BOTFORGE_DEPLOY_RUN_URL`, label
  `deploy run`), falling back to the artifact link.
- **`admin.py`**: the generic `/admin` command — an operator panel built
  as a Components V2 `LayoutView` (ADR-0009): a container with a text
  header and a section whose button reacts live. The first concrete use
  of the layout system in a shipped command (botforge-services#102):
  further admin features reuse the section + accessory button pattern
  and the `<mod>:<component>:<payload>` custom-id convention.

### `ui/`

- **`views.py`**: buttons and select menus
- **`modals.py`**: forms (modal dialogs)
- **`embeds.py`**: rich message builders

UI conventions (persistent views, dynamic items, `custom_id` scheme) are
documented in [architecture/discord.md](architecture/discord.md).

## 4. Configuration (`botforge-services/config/`)

All configuration is versioned YAML, loaded at startup:

- **`locales/`**: i18n message catalogs (`en.yaml`, `fr.yaml`) — common keys;
  mod strings arrive with their mods
- **`games/`**: game declarations (name, aliases, team size) — added per game,
  none shipped yet
- **`mods/`**: mod declarations (`_example.yaml` is the documented template) —
  enabled flags, channels, roles, workflows, commands, dependencies

```mermaid
flowchart LR
    LOCALE["locales/*.yaml"] --> BOT
    GAMES["games/*.yaml"] --> MODS["Mods (cogs)"]
    MODCFG["mods/*.yaml"] --> MODS
    MODS --> CORE["Core services"]
    BOT --> CORE
```

## 5. Infra (`botforge-infra/`)

- **`deploy/`**: Docker Compose manifests per environment (test,
  production). One command launches the bot and its dependencies (MongoDB,
  Redis).
- **Images**: the bot image is a **multi-stage build** (deps → build →
  runtime) published by the `botforge-services` `Docker` workflow to
  `ghcr.io/jj-guild/botforge-services` (tags: `main`, `vX.Y.Z`, `sha-*`).
  Environments pull it from GHCR; production pins the exact tag via
  `BOTFORGE_IMAGE`.
- **Backups**: every deployment runs a **mandatory pre-deploy backup of both
  stores** (`scripts/backup_db.sh`): MongoDB via `mongodump --archive --gzip`,
  Redis via a `BGSAVE` RDB snapshot. Both artifacts share a timestamp prefix,
  are verified (non-empty, gzip integrity for Mongo) and abort the deployment
  on failure.
- **Rollback**: `scripts/rollback.sh` restores the latest backup (or a given
  archive) and reverts the manifests; `deploy.sh` triggers it automatically
  when the post-deploy health gate fails.
- **Smoke/preflight**: the bot image ships a `--preflight` mode that runs the
  real startup path (environment, MongoDB, Redis, locale catalogs) without
  connecting to the Discord gateway; CI runs it through the real container
  entrypoint on every PR.
- **`.github/workflows/`**: CI/CD — shellcheck, compose validation, smoke
  test (dev stack boot), **backup/restore round-trip test** (seed → dump →
  wipe → restore → byte-for-byte diff, on MongoDB **and** Redis), then
  deploy. Deployment is GitOps-style: environments are defined by versioned
  manifests, and deploys are reproducible from the repo state.

## 6. Key diagrams

### Communication flow: registration example

```mermaid
sequenceDiagram
    participant U as User
    participant B as Bot (Discord)
    participant C as Core (Generic)
    participant DB as MongoDB

    U->>B: /register
    B->>C: start_workflow("registration")
    C->>DB: Save WorkflowState
    C->>B: send_dm("What is your name?")
    B-->>U: DM with question
    U->>B: Replies with name
    B->>C: handle_interaction({name: "Player1"})
    C->>DB: Update WorkflowState
    C->>B: send_dm("Which game? [AoE2, Chess]")
    B-->>U: DM with select menu
    U->>B: Selects game
    B->>C: handle_interaction({game: "aoe2"})
    C->>DB: Save UserModel, complete WorkflowState
    C->>B: assign_role + confirm message
    B-->>U: Registration confirmed
```

### Channel management

```mermaid
flowchart TD
    MOD["Mod code"] -->|"get_channel_for_category(guild, category)"| CHANSVC["ChannelService"]
    CHANSVC --> CACHE{"Cache hit?"}
    CACHE -->|"Yes"| RET["Return channel id"]
    CACHE -->|"Miss"| DBQ{"MongoDB ChannelModel?"}
    DBQ -->|"Found"| CACHEPUT["Save to cache"] --> RET
    DBQ -->|"Not found"| CREATE["DiscordPlatform create_channel"]
    CREATE --> SAVE["Save to DB and cache"]
    SAVE --> RET
```

### Deployment flow

```mermaid
flowchart LR
    PUSH["Push to main"] --> CI["CI: lint, test, build"]
    CI -->|"tag / manual"| DEPLOY["Deploy job"]
    DEPLOY --> ENV["Docker Compose environment"]
    ENV --> BOT["botforge bot container"]
    ENV --> MONGO["MongoDB"]
    ENV --> REDIS["Redis"]
```

## 7. Key decisions

| Decision | Rationale | ADR |
| -------- | ---------- | --- |
| `IPlatform` abstraction | **Extensibility** — Twitch later without touching game logic | [ADR-0001](DECISIONS/001-multi-platform-architecture.md) |
| `typing.Protocol` contracts | **Decoupling** — adapters satisfy interfaces structurally, no inheritance | [ADR-0011](DECISIONS/011-protocol-interfaces.md) |
| Building-block taxonomy | **Clarity** — platform / game / data provider / mod; CI-enforced dependency matrix; cross-game mods; per-environment activation | [ADR-0012](DECISIONS/012-taxonomy-repo-strategy.md) |
| Cross-platform identity | **Continuity** — one account, N platform identities; OAuth (Discord, Twitch) + Steam game-account link; explicit reversible merge | [ADR-0013](DECISIONS/013-cross-platform-identity.md) |
| RBAC grants | **Uniform rights** — one permission model enforced in the application layer for every frontend | [ADR-0014](DECISIONS/014-rbac-permissions.md) |
| Webapp API boundary | **Single business path** — webapp is a request/response frontend over the application layer, not an `IPlatform` | [ADR-0015](DECISIONS/015-webapp-api-boundary.md) |
| Packaging trajectory | **Boundaries as packages** — uv workspace now, private index on first external consumer, public PyPI only by explicit decision | [ADR-0017](DECISIONS/017-packaging-distribution.md) |
| Modular monolith + extraction contracts | **No premature microservices** — one runtime until an ADR-0012 trigger fires; seams stay network-ready (serializable, own state, typed errors, idempotent) | [ADR-0019](DECISIONS/019-modular-monolith-extraction-contracts.md) |
| MongoDB | **Flexibility** — dynamic schemas for evolving workflow payloads | — |
| Redis + MongoDB state split | **Responsiveness** — hot state in Redis, durability in MongoDB | [ADR-0002](DECISIONS/002-workflow-engine.md) |
| Channel categories | **Portability** — same mod on any server without code changes | [ADR-0003](DECISIONS/003-channel-categories.md) |
| Discord permissions & delivery | **Least surprise** — runtime role checks, DM/channel content policies, drift alerting, admin-triggered sync | [ADR-0016](DECISIONS/016-discord-permissions-and-delivery.md) |
| Docker Compose | **Simplicity** — one command to launch everything | — |
| GitOps | **Reproducibility** — versioned, reviewable environments | — |

New major decisions follow the ADR process in [DECISIONS/](DECISIONS/)
(template: [templates/decision-template.md](../templates/decision-template.md)).

## 8. Frontends and application layer

Beyond Discord, BotForge is planned to grow a Twitch bot and a webapp.
All three are **frontends** over one application layer
([ADR-0012](DECISIONS/012-taxonomy-repo-strategy.md),
[ADR-0015](DECISIONS/015-webapp-api-boundary.md)):

- **Every building block has one of four natures**: platform frontend,
  game, data provider, mod. Dependencies follow a CI-enforced matrix;
  mods may be game-agnostic or bound to N games; what runs per
  environment is an infra-owned activation manifest.
- **Identity is cross-platform**: one account, N platform identities
  (Discord now; OAuth for the webapp, Twitch later; Steam links game
  accounts via `mod-profile`). Duplicates merge explicitly and
  reversibly ([ADR-0013](DECISIONS/013-cross-platform-identity.md)).
- **Permissions are application-level**: mod-declared permission keys,
  app roles, scoped grants; platform roles are synced grant sources, and
  enforcement happens in application services for every frontend
  ([ADR-0014](DECISIONS/014-rbac-permissions.md)).
- **The webapp is request/response**, not an `IPlatform`: it consumes a
  versioned API (`/api/v1/`) that calls the same services and workflows
  as the bot; stats come from read models, never from direct database
  access ([ADR-0015](DECISIONS/015-webapp-api-boundary.md)).

## See also

- [architecture/core.md](architecture/core.md) — core services design deep-dive
- [architecture/mods.md](architecture/mods.md) — mod system design
- [architecture/channels.md](architecture/channels.md) — channels,
  pinned views and admin surfaces runtime conventions
- [architecture/testing.md](architecture/testing.md) — hybrid testing strategy  (`MockDiscord` mock objects + SimCord behavioral simulator)
- [architecture/discord.md](architecture/discord.md) — Discord.py components guide
- [architecture/discord-permissions.md](architecture/discord-permissions.md) — Discord permissions & message delivery guide (DM vs channel, runtime role checks, channel access, sync)
- [WORKFLOWS.md](WORKFLOWS.md) — game workflow documentation
- [MODS/](MODS/) — per-mod documentation
- [DECISIONS/](DECISIONS/) — architecture decision records
- [AGENTS.md](../AGENTS.md) — agent entry points (all 3 repos)
- [docs/CONVENTIONS.md](CONVENTIONS.md) — conventions shared by the three repositories
