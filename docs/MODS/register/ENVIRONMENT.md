# Register mod — Environment

## Discord requirements

- Bot permissions: send messages, send DMs, manage roles (to assign game
  roles), view channels
- Channels declared by the mod (provisioned automatically by the core via
  `ModRegistry`, botforge-services#26):
  - `register:register_admin` — registration notifications and approvals
  - `register:register_info` — welcome panel and instructions
- Roles declared by the mod (logical keys, resolved by `RoleService`):
  - `player` — base registered player
  - `registered_aoe2` (example game role, one per allowed game)
- Role requirements: the bot's role must be above the game roles it assigns

## Database requirements

- Collections:
  - `users` (UserModel: one document per registered player)
  - `workflow_states` (registration workflow state)
- Indexes:
  - `users.name` — unique, case-insensitive (name uniqueness rule)
  - `users.platform_id` — unique
  - `workflow_states.status` — for resuming in-flight registrations

## Redis keys

- `workflow:{user_id}:registration` — hot registration state (current step,
  payload), TTL = workflow timeout

## Configuration options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| enabled | bool | true | Enable/disable the mod |
| default_role | str | "Player" | Default role when a game has no specific role |
| admin_notifications | bool | true | Post registrations to the ADMIN category |
| allowed_games | list[str] | all declared games | Games offered in the selector |
| welcome_message_key | str | "register.welcome" | i18n key of the welcome message |

## Environment variables

```ini
# Required (shared with the platform)
DISCORD_TOKEN=your_token
MONGO_URI=mongodb://localhost:27017
REDIS_URI=redis://localhost:6379

# Optional (register mod)
REGISTRATION_TIMEOUT=600
```
