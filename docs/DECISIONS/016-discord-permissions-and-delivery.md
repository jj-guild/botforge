# ADR-0016: Discord permissions & message delivery — DM vs channel, runtime role checks, channel access policies

- **Status**: Accepted

- **Accepted with**: co-built with the developer across agent sessions (challenged and revised together)
- **Date**: 2026-09-21
- **Deciders**: developer (pending), game designer (requested)
- **Reference**: botforge-services#55, botforge-services#56, botforge-services#57, botforge-services#58

## Context

The game designer defined Discord-facing permission rules the bot must
follow:

1. **DM and channel messages are different** and must be treated as distinct
   delivery contexts: a DM targets one known user; a channel message is
   visible to everyone who can read the channel.
2. Button (component) actions must be **authorized at runtime** based on the
   roles the interacting user actually holds — not on what was rendered.
3. In a **DM**, buttons the user has no access to are sent **disabled**
   (not hidden).
4. In a **channel**, only components and content **visible to everyone** may
   be sent — never role-gated buttons or personal data.
5. Channels are **categorized with per-role access policies**, and a drift
   **alerting** mechanism must report when reality diverges from the
   declaration.
6. Roles and channels can be **synchronized on an admin's demand**.

The existing pieces this builds on: logical role keys and `role_mappings`
(ADR-0003, botforge-services#26), the dual UI system (ADR-0009), the i18n
system (ADR-0008) and the admin levels (botforge-services#35). Rendering
hints cannot be a security boundary: roles change, persistent views survive
restarts, and any user can attempt an interaction on a stale message.

## Decision

BotForge separates **rendering** (UX, per-destination) from **authorization**
(runtime, per-interaction):

- **Every send path carries an explicit destination** — `DM`, `CHANNEL` or
  `EPHEMERAL`. Channel messages must contain only public components and no
  personal data. DMs may be personalized; components the user lacks the role
  for are rendered **disabled**, impossible ones are omitted. Components
  declare delivery intent (`required_roles`, `dm_allowed`, `public`); a
  shared render helper applies the policy for both UI systems of ADR-0009.
- **Every component action is authorized at interaction time** by a core
  `PermissionService` (platform-agnostic): logical role keys resolve through
  `role_mappings`; bot admins bypass mod-level checks; DM interactions are
  denied unless the component is `dm_allowed` or requires no roles. Denials
  answer ephemerally via i18n and produce a log/audit record. No view
  implements its own ad-hoc check.
- **Every channel category declares a `ChannelAccessPolicy`** (view/post role
  keys, everyone flags, bot overwrite). The declaration is the source of
  truth, applied as permission overwrites when the bot creates the channel
  and persisted in `ChannelModel`.
- **Drift is reported, never silently repaired**: a `ChannelAuditService`
  compares declaration and reality (startup, post-sync, schedule, on
  demand) and routes findings to `ADMIN` (summary) and `LOGS` (detail).
- **Sync is admin-triggered, idempotent, non-destructive**: `/setup sync`
  reconciles channels/roles with declarations, repairs bot-managed bindings,
  flags everything else as `manual_action_needed`, and never deletes or
  touches channels the bot did not create or claim.

Full operating rules: [architecture/discord-permissions.md](../architecture/discord-permissions.md).

## Alternatives Considered

1. **Trust the rendering (hide/disable buttons only)** — rejected: roles
   change after a message is sent, persistent views survive restarts, and
   rendering is client-side advice, not enforcement. Any stale message would
   become a privilege-escalation vector.
2. **Discord-level enforcement only (channel permission overwrites)** —
   rejected as sole mechanism: DMs have no permission overwrites at all, and
   component actions inside a channel the user can read still need
   role-based gating. Overwrites complement, not replace, runtime checks.
3. **Hide unauthorized buttons in DMs instead of disabling them** — rejected
   by the game designer: a disabled button teaches the player what exists
   and what to unlock; hiding makes the game opaque.
4. **Automatic continuous sync of roles/channels** — rejected: rewriting
   guild structure without an explicit admin action is surprising and
   racy with human moderation. The sync is explicit; the audit provides the
   safety net between syncs.
5. **Hardcoded Discord role/channel IDs in mods** — already rejected by
   ADR-0003/botforge-services#26 (logical keys only); this ADR extends the
   same principle to component actions and channel access.

## Consequences

**Positive:**

- A single authorization path (`PermissionService`) for every component
  action, identical across mods; behavior is testable with MockDiscord and
  SimCord without a live guild.
- Channel messages are safe by construction: no leaks of role-gated actions
  or personal data to a public audience.
- Disabled-but-visible DM buttons make progression legible for players.
- The declaration-vs-drift model keeps Discord as runtime state: the bot
  survives human edits, deleted roles and renamed channels, and reports
  instead of fighting them.

**Negative:**

- Two layers to implement and test (rendering intent + runtime checks); the
  UI layer gains a mandatory render helper and components carry permission
  metadata.
- Runtime checks add a role-resolution hop on hot interaction paths; caching
  (Redis, ADR-0005) will be needed for large guilds.
- Disabled buttons in DMs reveal the existence of gated features; acceptable
  by design decision, but mods must not put secrets behind them.
- The audit/sync pair adds operational surface (two services, one admin
  command, report channels) that must stay documented.
