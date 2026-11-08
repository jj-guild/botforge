# ADR-0010: Redis hosting — Redis Cloud free tier for prod, containerized Redis for local/test

**Status:** Accepted

**Date:** 2026-09-21

**Reference:** ADR-0005 (Redis state management), ADR-0006 (Docker Compose infra)

## Context

[ADR-0005](005-redis-state-management.md) decided **what** Redis is used for
(hot workflow state with TTLs, locks, rate limiting, channel-mapping
cache). [ADR-0006](006-docker-compose-infra.md) decided that local and test
run on Docker Compose. Neither decides **where Redis runs in production**.

Constraints:

- Zero budget for production infrastructure.
- Redis holds only **ephemeral** state: every key has a TTL, and the
  durable copy of workflows lives in MongoDB (Atlas free tier, same
  reasoning as the MongoDB hosting choice). Losing Redis contents degrades
  responsiveness for a few seconds but never loses game data.
- The bot is a single process for the foreseeable future, so connection
  counts are low.

Redis Cloud Essentials (official Redis Inc. hosted offering) has a permanent
free plan: 30 MB database, 30 concurrent connections, 100 ops/sec
throughput, 5 GB monthly bandwidth, TLS + IP allowlist, persistence on.

## Decision

- **Production**: managed **Redis Cloud** (Essentials free tier). It is the
  official Redis offering, mirroring the "official vendor free tier" choice
  already made for MongoDB Atlas.
- **Local and test**: Redis as a service in the local `docker-compose.yml`
  (per ADR-0006). No cloud dependency for local runs.
- The connection string comes from environment config only
  (`REDIS_URL` + `REDIS_TLS`); no code difference between environments.
- **Budget for the limits**: `StateService` keeps a small connection pool
  (≤ 10 connections), keys always carry TTLs (30 MB ceiling), and the
  100 ops/sec ceiling is a per-guild concern to revisit only if a mod
  starts polling in hot loops.
- If a free-tier limit is hit (throughput or size), the upgrade path is a
  paid Redis Cloud Essentials plan (~$5/month) — same provider, same
  connection string, no migration.

## Alternatives Considered

1. **Upstash free tier**: 256 MB and 500K commands/month are more generous,
   and it is serverless, but it is a third-party HTTP-based Redis dialect
   and meters per command. Rejected in favor of the official Redis
   offering, consistent with Atlas-for-Mongo.
2. **Self-hosted Redis on the same hosting as the bot**: no external dependency
   but adds ops burden (persistence, restarts, monitoring) for a hobby
   project. Rejected.
3. **MongoDB for hot state too** (drop Redis from prod): fewer services but
   contradicts ADR-0005 (TTL-based ephemeral state, locks, pub/sub). Rejected.

## Consequences

### Positive

- Zero cost, officially supported product, TLS and IP allowlist included.
- Same Redis server (not a dialect) across test and prod.
- Durable state is unaffected by Redis outages (ADR-0002 split).

### Negative

- Hard ceilings: 30 MB / 30 connections / 100 ops/sec / 5 GB per month.
  Adequate for one guild and a single bot process; not for a multi-guild
  future at scale.
- No SLA on the free tier; a Redis Cloud incident pauses hot-state
  features (workflow steps, locks) until it recovers.
- One more external account to manage alongside Atlas and the Discord
  developer portal.

## References

- [ADR-0005](005-redis-state-management.md) — what Redis stores
- [ADR-0006](006-docker-compose-infra.md) — Docker Compose environments
- [Redis Cloud Essentials plan details](https://redis.io/docs/latest/operate/rc/subscriptions/view-essentials-subscription/essentials-plan-details/)
- botforge-services#9 (StateService), botforge-services#23 (caching integration)
