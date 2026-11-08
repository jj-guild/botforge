# ADR-0003: Channel categories

**Status:** Accepted
**Date:** 2026-09-18
**Reference:** botforge#2, botforge#6

## Context

Different types of messages need to go to different channels:

- Registration notifications → the register mod's admin channel
- Reports → `REPORTS` channel (platform-level)
- Ladder standings → the ladder mod's rankings channel
- General messages → default channel

Without a system, we'd have:

- Hardcoded channel IDs
- No flexibility for different guilds
- Difficulties adding new channel types

## Decision

Implement a **`ChannelService`** keyed by **mod-scoped channel
categories**:

- The core enum keeps only platform-level categories (`ADMIN`, `REPORTS`,
  `LOGS`); **mods declare their own categories** (e.g. ladder: admin,
  rankings, info) via their mod config and `ModRegistry`
  (botforge-services#26) — mods never extend core enums
- Categories are addressed as `mod:key` (e.g. `ladder:ladder_rankings`)
- Maps `guild_id + category → channel_id`
- Creates channels automatically if missing (via `IPlatform`)
- Caches mappings in Redis for performance
- Falls back to MongoDB (`ChannelModel`) for persistence
- Same mechanism for roles: each mod declares its roles; the core provides
  `RoleService` with logical role keys, never hardcoded Discord role IDs

## Alternatives Considered

1. **Hardcoded channel IDs:** simple but inflexible
2. **Config file only:** no automatic channel creation
3. **User-configured per guild:** too complex for the initial version
4. **A single core enum extended per mod (`LADDER`, `REGISTRATION`, ...):**
   rejected — it makes mods pollute the core; each new mod would require a
   core code change

## Consequences

### Positive

- Flexible channel routing
- Automatic channel creation
- Works across multiple guilds
- Easy to add new categories
- Good performance (cached)

### Negative

- Slight complexity in `ChannelService`
- Need to handle channel creation errors (permissions)

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) — channel management diagram
- [WORKFLOWS.md](../WORKFLOWS.md) — channel category management and message
  routing
- botforge-services#5 (ChannelService), botforge-services#7 (enums), botforge-services#26 (per-mod channel/role management)
