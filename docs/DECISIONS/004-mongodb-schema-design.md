# ADR-0004: MongoDB schema design

**Status:** Accepted
**Date:** 2026-09-18
**Reference:** kingdoms#6

## Context

We need to store:

- Users (profile, preferences, stats)
- Guilds (configuration, channels)
- Workflow states
- Ladder data (matches, rankings)

Game rules evolve with the game designer's iterations, so stored payloads
(mostly workflow data) change shape frequently.

## Decision

Use **MongoDB** with **Pydantic models** for:

- Flexible, schema-less storage
- Easy schema evolution
- Good Python integration (PyMongo, Pydantic)
- Horizontal scalability
- JSON-like query language

### Schema design principles

- Embed related data (user preferences in the user document)
- Reference large/volatile data (messages, logs)
- Use indexes for query performance
- Version schemas for backward compatibility

## Alternatives Considered

1. **PostgreSQL:** more structured, but less flexible for evolving schemas
2. **SQLite:** simple but not scalable, no horizontal scaling
3. **Firebase:** good for realtime, but vendor lock-in

## Consequences

### Positive

- Schema flexibility
- Easy to add new fields
- Good for hierarchical data (users, guilds)
- Horizontal scaling possible

### Negative

- No joins (need to denormalize)
- Less ACID compliance

## Revision (2026-11-06)

The original decision listed "no multi-document transactions" among
the accepted negatives. **Revised:** cross-document invariants under
concurrent writers **are** allowed to use multi-document transactions
(MongoDB supports them on replica sets) or the existing Redis locks
(ADR-0005). The default remains atomic single-document updates;
transactions are the exception for multi-document invariants, not the
rule. The full concurrency hierarchy lives in
[architecture/core.md](../architecture/core.md), *MongoDB write
atomicity*.

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) — models
- kingdoms-services#4 (DB models)
