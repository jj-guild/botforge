# ADR-0021: The five architecture rules — enforced, not remembered

**Status:** Accepted (owner direction, 2026-11-05 remise en conformité)

**Date:** 2026-11-05

**Extends:** ADR-0020 (process split) — this ADR tightens the seams ADR-0020
opened and makes them testable.

## Context

The 2026-11-05 audit found the process split (ADR-0020) eroded on five axes:
the bot spoke directly to ext-librematch, the AoE2 game code lived in `core`,
the ext providers imported game code, collections were read across ownership
lines, and nothing prevented any of it from coming back. A provider ban
(Liquipedia 429s) had condemned every environment on the VPS — the blast
radius of one leaky seam.

## Decision

Five rules, each enforced by an AST-based guard
(`botforge-services: tests/architecture/test_layering.py`) that runs on every
commit. A violation fails the suite; a fixed violation demands its allowlist
entry's removal (the allowlists must shrink, never rot).

### R1 — The ext providers are isolated, code and run

`ext-liquipedia`, `ext-aoe2lobby`, `ext-librematch`, `ext-aoe2techtree` import
only shared utils (`core.ids`, `core.debug`, `core.rate_limit`,
`core.upstream_identity`, `core.rpc`, `core.models`, `core.wiki_names`,
`core_process.*`, `botforge.aoe2` — the game's shared raw formats) — never
game code, never discord, never another provider's internals. The Liquipedia
HTTP client (pacing, backoff, circuit breaker, batch queries) lives INSIDE
ext-liquipedia; the game's raw formats (slotinfo/options blobs, the lobby
grace, MapSeed) live in `botforge.aoe2`.

### R2 — A game service knows its providers by name, never by URL

The wiring URL ↔ provider is configuration (the process environment), never
code: no hardcoded upstream URL inside a game package. The game service owns
its providers' doors (`EXT_*_URI` in ITS environment) and proxies them over
its contract.

### R3 — Core never mentions a provider

Core knows the games by their gRPC services, not their code and not their
providers' names. The provider config plumbing lives in `core_process`.

### R4 — Discord (the bot, the mods) talks to game services and core, never an ext

No ext import, no `EXT_*_URI` read, no provider client. Every provider
surface the bot needs is a GameData proxy: `GetProfileStats`,
`GetMatchResult`, `GetProviderCapabilities`, `GetMapSeed`,
`GetLastCompletedTimes`, `SyncContent`. A provider failure comes back as a
**functional error** the UI shows as-is (the provider is down, rate-limited,
or not configured) — never a crash, never a silent fallback.

### R5 — Every Mongo collection has ONE owner

A service only touches its own collections and exposes the data through its
service (gRPC for cross-process). Landed on the hot paths: the game
collections' indexes are ensured by the game service at its boot; the
matches aggregation answers over `GetLastCompletedTimes`; the bindings read
rides the registration service's batched API.

**The catalog gateway (landed 2026-11-05):** the game's collections (maps,
map pools, map packs, factions, the localized content docs) answer through
`GameData.Call` — an allowlisted op dispatch over the game service's own
`GameDataService` + content store. The bot's `RemoteGameDataService` exposes
the same method surface and rebuilds the same pydantic models, so the views
keep their objects; a functional error crosses the wire with its kind and
re-raises as the same exception type. The R5 allowlist carries exactly one
dated entry: the operational purge tool.

## The sync rule

Content syncs (civs, maps) run IN the game service against ITS providers
(`GameData.SyncContent`); the DM panel's buttons and the boot refresh ask the
service. **No vendored data**: a missing provider is a functional error,
never a local dataset fallback.

## Consequences

- A provider's failure (rate limit, downtime, ban) is contained to that
  provider's process; the game degrades, the platform lives.
- Replacing a provider (challonge → aoe2cm, a mod reusing liquipedia) touches
  the provider's process and the game's wiring, nothing else.
- The five rules hold by test: the guard's allowlists are the audit trail of
  what remains (today: the game-catalog CRUD gap under R5).
