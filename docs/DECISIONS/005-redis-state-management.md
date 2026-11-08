# ADR-0005: Redis state management

**Status:** Accepted
**Date:** 2026-09-18
**Reference:** botforge#6

## Context

We need to store:

- Workflow states (temporary, fast access)
- Channel mappings (`guild_id → channel_id`)
- Rate limiting data
- Session data
- Locks (for distributed coordination)

## Decision

Use **Redis** for:

- Ephemeral state (workflow steps, sessions) with TTLs
- Caching (channel category mappings)
- Rate limiting
- Distributed locks
- Pub/Sub for cross-service communication

## Alternatives Considered

1. **In-memory cache:** not distributed, lost on restart
2. **MongoDB for everything:** slower for caching, more expensive
3. **Memcached:** simpler but fewer features (no persistence, no data
   structures)

## Consequences

### Positive

- Very fast (in-memory)
- Rich data structures (hashes, sets, lists)
- Atomic operations
- Pub/Sub capabilities
- Persistence options

### Negative

- Additional infrastructure to maintain
- Memory usage can grow
- Need to handle Redis failures

## References

- [ADR-0002](002-workflow-engine.md) — the durable/hot state split
- [ARCHITECTURE.md](../ARCHITECTURE.md) — `StateService`
- botforge-services#9 (StateService)
