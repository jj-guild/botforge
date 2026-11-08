# Game workflows — user-facing flows (registration, ladder, …)

This document is the definitive reference for BotForge user interactions and
system behavior. All workflows are described **platform-agnostically**: they
are expressed against the generic core (see
[ARCHITECTURE.md](ARCHITECTURE.md)), so they apply to Discord today and to
future platforms (Twitch) without changes.

Components referenced here (`WorkflowEngine`, `ChannelService`,
`ChannelCategory`, `WorkflowState`) are documented in
[ARCHITECTURE.md](ARCHITECTURE.md#2-generic-core-botforge-servicessrcbotforgecore).
UI component conventions (buttons, select menus, modals, `custom_id`) are
documented in [architecture/discord.md](architecture/discord.md).

> The `/report` command is **out of scope** (dropped, see
> botforge-services#18). Moderation is admin-driven.

## 1. Registration workflow

**Description:** new user onboarding process.

**Steps:**

1. User sends `/register` command
2. Bot sends DM: "What is your name?"
3. User replies with name
4. Bot validates name uniqueness
5. Bot sends DM: "Which game? [AoE2, Chess, Other]"
6. User selects game
7. Bot assigns default role for that game
8. Bot sends confirmation DM with welcome message
9. Bot posts notification in admin channel

**Channels used:**

- DM for user interaction
- `register:register_admin` channel for notifications (mod-declared)

```mermaid
sequenceDiagram
    participant U as User
    participant B as Bot
    participant C as Core
    participant DB as MongoDB
    participant A as Admin Channel

    U->>B: /register
    B->>C: start_workflow("registration")
    C->>DB: create WorkflowState(PENDING)
    C->>B: send_dm("What is your name?")
    B-->>U: DM with question
    U->>B: Replies: "JohnDoe"
    B->>C: handle_interaction({name: "JohnDoe"})
    C->>DB: validate name uniqueness
    C->>DB: update WorkflowState(name="JohnDoe")
    C->>B: send_dm("Which game?") + SelectMenu
    B-->>U: DM with game selector
    U->>B: Selects "AoE2"
    B->>C: handle_interaction({game: "aoe2"})
    C->>DB: create UserModel(name, game)
    C->>DB: update WorkflowState(COMPLETED)
    C->>B: send_dm("Welcome! You're registered for AoE2")
    C->>B: send_admin_notification({user: "JohnDoe", game: "aoe2"})
    B->>A: Post in admin channel
```

## 2. Ladder workflow

**Description:** competitive ranking system.

**Steps:**

1. User sends `/ladder join`
2. Bot verifies user is registered
3. Bot adds user to ladder queue
4. When 2+ users in queue, bot creates match
5. Bot sends DM to both players: "Match ready vs [opponent]"
6. Players confirm availability
7. Bot records match result
8. Bot updates ELO ratings
9. Bot updates ladder rankings
10. Bot posts results in the `ladder:ladder_rankings` channel

**Channels used:**

- DM for match coordination
- `ladder:ladder_rankings` channel for rankings, `ladder:ladder_info` for announcements

```mermaid
sequenceDiagram
    participant U1 as User1
    participant U2 as User2
    participant B as Bot
    participant C as Core
    participant DB as MongoDB
    participant L as Ladder Channel

    U1->>B: /ladder join
    B->>C: handle_ladder_join(user1)
    C->>DB: add_to_queue(user1)
    C->>B: send_dm("Added to queue. Position: 1")
    B-->>U1: Confirmation DM

    U2->>B: /ladder join
    B->>C: handle_ladder_join(user2)
    C->>DB: add_to_queue(user2)
    C->>DB: check_queue_size()
    C->>C: queue >= 2
    C->>DB: create_match(user1, user2)
    C->>B: send_dm(user1, "Match ready vs User2")
    C->>B: send_dm(user2, "Match ready vs User1")
    B-->>U1: Match notification
    B-->>U2: Match notification

    U1->>B: /ladder confirm
    U2->>B: /ladder confirm
    B->>C: handle_confirmation(user1, user2)
    C->>DB: update_match_status(IN_PROGRESS)
    C->>B: send_dm("Match confirmed. Good luck!")

    U1->>B: /ladder report win
    B->>C: handle_result(user1, user2, winner=user1)
    C->>DB: update_match_result(winner, loser)
    C->>DB: update_elo(user1, +25, user2, -25)
    C->>DB: update_ladder_rankings()
    C->>B: send_dm(user1, "You won! New ELO: 1250")
    C->>B: send_dm(user2, "You lost. New ELO: 1175")
    C->>B: send_ladder_update()
    B->>L: Post match results
```

## 3. Moderation workflow

**Description:** admin actions and warnings. There is **no user-facing report
command**; moderation is admin-driven.

**Steps:**

1. Admin sends `/warn @user "reason"` or `/ban @user`
2. Bot validates admin permission
3. Bot records moderation action (`ModerationSystem`)
4. Bot posts the action in the `LOGS` channel
5. Bot notifies the user by DM

**Channels used:**

- Mod-declared admin channels (e.g. `register:register_admin`, `ladder:ladder_admin`) for admin actions
- `LOGS` channel for moderation history
- DM for user notification

```mermaid
sequenceDiagram
    participant A as Admin
    participant U as User
    participant B as Bot
    participant C as Core
    participant DB as MongoDB
    participant L as Logs Channel

    A->>B: /warn @User "Spamming in chat"
    B->>C: handle_warn(admin, user, reason)
    C->>DB: create ModerationAction
    C->>B: send_logs_channel(action)
    B->>L: Post moderation embed
    C->>B: send_dm(user, "You received a warning")
    B-->>U: Warning notification
```

## 4. Channel category management

**Description:** how the system routes messages to the correct channels.
Mods request channels by `ChannelCategory`, never by name or ID; the
`ChannelService` resolves the category (cache → database → creation).
See [ADR-0003](DECISIONS/003-channel-categories.md).

```mermaid
flowchart TD
    A["User Action"] --> B{"Action Type?"}
    B -->|"/register"| C["Start Registration Workflow"]
    B -->|"/ladder"| E["Handle Ladder"]
    B -->|"/clan"| D2["Handle Clan Action"]
    B -->|"Other"| F["Default Channel"]

    C --> G["register:register_admin"]
    E --> I["ladder:ladder_rankings"]
    D2 --> I2["clans:clan_chat"]

    G --> J["get_channel_for_category"]
    H --> J
    I --> J

    J --> K["Cache: guild_id -> channel_id"]
    K -->|"Hit"| L["Return Channel"]
    K -->|"Miss"| M["MongoDB ChannelModel"]
    M -->|"Miss"| N["DiscordPlatform create_channel"]
    N --> M
    M --> K
```

## 5. Message routing workflow

**Description:** how incoming messages are dispatched based on their type and
the channel category. Component interactions are dispatched through the
`custom_id` convention (`<mod>:<component>:<payload>`, see
[architecture/discord.md](architecture/discord.md#6-custom_id-conventions-project-wide)).

```mermaid
flowchart TD
    A["Message Received"] --> B["Determine Message Type"]
    B --> C["Command?"]
    B --> D["Component Interaction?"]
    B --> E["Regular Message?"]

    C --> F["Parse Command"]
    F --> G["Get Command Handler"]
    G --> H["Execute Command"]
    H --> I["Get Response Channel"]
    I --> J["Send Response"]

    D --> K["Get Custom ID"]
    K --> L["Parse Interaction Data"]
    L --> M["Get Workflow State"]
    M --> N["Handle Interaction"]
    N --> I

    E --> O["Check Channel Category"]
    O --> P{"Category Type?"}
    P -->|"ADMIN"| Q["Forward to Admin Channel"]
    P -->|"REPORTS"| R2["Forward to Reports Channel"]
    P -->|"LOGS"| R["Forward to Logs Channel"]
    P -->|"LEADERBOARD"| S["Forward to Leaderboard Channel"]
    P -->|"DEFAULT"| T["No Action"]
```

## Workflow state lifecycle

Every multi-step workflow is executed by the `WorkflowEngine` and persisted as
a `WorkflowState` (MongoDB, hot state in Redis), so flows survive restarts and
can be resumed. Status transitions:

```mermaid
stateDiagram-v2
    [*] --> PENDING: start_workflow()
    PENDING --> IN_PROGRESS: first interaction
    IN_PROGRESS --> IN_PROGRESS: step transitions
    IN_PROGRESS --> COMPLETED: all steps done
    IN_PROGRESS --> CANCELLED: user cancels
    IN_PROGRESS --> TIMED_OUT: inactivity timeout
    PENDING --> CANCELLED: user cancels
    COMPLETED --> [*]
    CANCELLED --> [*]
    TIMED_OUT --> [*]
```

## Ops commands workflows (PR/issue comments)

The `ops-commands` workflow (botforge-services) intercepts four keywords
on any PR or issue comment, acknowledges immediately (what will happen,
why the requestor may ask), gates through the reusable `authorize.yml`
against the roster authority matrix, then dispatches to botforge-infra
which runs on the environment's own runner:

| Keyword | Capability | Who | What it does |
| --- | --- | --- | --- |
| `/logs [env] [--service S] [--since 30m] [--from iso] [--to iso] [--tail N]` | `env-logs` | ops, dev on test | `env-logs` workflow: filtered `docker compose logs` dump, posted back in the thread + private artifact. Read-only. |
| `/restart [env]` | `env-control` | ops, dev on test | `env-control` workflow (restart): in-place restart, no pull, no recreate. |
| `/rollback [env]` | `rollback` | ops | `rollback-state` dispatch: reverts the last pin on the state branch, the push re-triggers the deployment of the previous known-good image. |
| `/dump-db [env]` | `db-dump` | ops | `db-daily-dump` workflow on demand: mongodump + Redis snapshot, hosting archive + private artifact. |

The daily cron (04:30 UTC) runs the same `db-daily-dump` on every
environment — no gate needed: the dump is read-only for the data.

## See also

- [ARCHITECTURE.md](ARCHITECTURE.md) — core components and data flow
- [architecture/discord.md](architecture/discord.md) — UI component patterns
  and `custom_id` routing
- [MODS/](MODS/) — per-mod rules and environments
- [DECISIONS/](DECISIONS/) — ADRs backing these workflows
- [VIBEWORKFLOW.md](VIBEWORKFLOW.md) — the human + agent operating model
