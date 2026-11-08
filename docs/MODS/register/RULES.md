# Register mod — Rules

Rules enforced by the register mod. Each rule is written so it can be
automated and verified by the bot.

## Name uniqueness

1. Player names are unique across the platform.
2. A name that already exists (case-insensitive) is rejected during
   registration, with an ephemeral DM inviting the player to pick another.
3. Names are validated before any data is written (no partial registrations).

## Game selection

1. The player must select at least one game from the allowed list
   (`allowed_games` in the mod configuration).
2. Only games declared in `botforge-services/config/games/` are offered in
   the selector.
3. The selection is a required step: the workflow cannot complete without it.

## Role assignment

1. Registering for a game grants that game's default role automatically.
2. Roles are granted once per game; re-registration for the same game is a
   no-op (idempotent).
3. Role names come from configuration, never from code.

## Admin notification

1. Every successful registration posts a notification to the `ADMIN`
   channel category.
2. The notification contains: player name, selected game(s), platform user
   reference, and timestamp.
3. Failed or timed-out registrations are logged for the admin team but do
   not post notifications.

## Workflow timeouts

1. A registration workflow that receives no interaction within the
   configured timeout is marked `TIMED_OUT` (see
   [../../WORKFLOWS.md](../../WORKFLOWS.md#workflow-state-lifecycle)).
2. The player can restart registration with `/register` at any time.

## Moderation and penalties

Registration itself has no penalties; moderation is handled by the admin mod
(see botforge-services#21). See the template rules format in
[../TEMPLATE/RULES.md](../TEMPLATE/RULES.md) for the standard penalty grid.
