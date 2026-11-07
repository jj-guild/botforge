---
name: provider-librematch
description: Working with the Libre:Match provider (ext-librematch, aoe-api.worldsedgelink.com) — its API key gating, its real wire shape, and the relic id it expects. Load when touching the librematch integration or profile stats.
---

# Libre:Match provider (ext-librematch)

## The gate must match the wire

A key/config gate invented on our side silently rejected every valid
input while the real service answered anyone. Before gating on a config
value (`LIBREMATCH_API_KEY`, `EXT_LIBREMATCH_URI`, `LIBREMATCH_API_URL`),
verify the value can actually be absent AND that the service genuinely
requires it. An env var that exists-but-empty defeats ``${VAR:-default}``
compose defaults — code must fall back itself (``value or DEFAULT``),
always.

Without `LIBREMATCH_API_KEY`, `player_stats()` degrades to `None` — the
declared capabilities stay static (`player_stats=True` in
`DECLARED_CAPABILITIES`, the provider's single source of truth), so
GetCapabilities never reports `player_stats=false`.

## Test the real wire shape

A test suite that mocks the seam passes while prod fails. The
integration test must run the real gRPC server, the real adapter, the
real reply payloads (`statGroups`/`leaderboardStats`, `GetPersonalStat` —
never `/api/leaderboard`) and assert on the endpoint actually called.

## Profile id

librematch wants the **relic id**, not the aoe2insights URL id — see
[provider-aoe2insights](../provider-aoe2insights/SKILL.md) for the
resolution.
