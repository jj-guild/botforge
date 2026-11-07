---
name: provider-aoe2lobby
description: Working with the aoe2lobby realtime provider (ext-aoe2lobby, wss://data.aoe2lobby.com/ws/) — the WS endpoint and the relic id it expects. Load when touching lobby events, match summaries or the live dashboard.
---

# aoe2lobby provider (ext-aoe2lobby)

## Endpoint

The WS endpoint is `wss://data.aoe2lobby.com/ws/` — the code default
(`DEFAULT_WS_URL` in `ext_aoe2lobby/adapter.py`, mirrored in
`ext_aoe2lobby/server.py` and `core_process/realtime_checks.py`); the
compose files fall back to it when `AOE2LOBBY_WS_URL` is empty. The old
`wss://aoe2lobby.com/ws` default never delivered a single frame.

## Profile id

aoe2lobby wants the **relic id**, not the aoe2insights URL id — see
[provider-aoe2insights](../provider-aoe2insights/SKILL.md) for the
resolution.
