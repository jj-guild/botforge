---
name: provider-aoe2insights
description: aoe2insights.com profile ids — the insights user id vs the relic id, how to resolve a pasted id/URL, and which path builds a valid profile link. Load before storing or linking a player profile.
---

# aoe2insights — two ids, one profile

The aoe2insights URL id (e.g. `12488557`) and the **relic id** (e.g.
`17190369`) are different numbers. librematch and aoe2lobby want the
**relic id** — see [provider-librematch](../provider-librematch/SKILL.md)
and [provider-aoe2lobby](../provider-aoe2lobby/SKILL.md).

- Resolve any pasted id/URL through
  `aoe2insights.com/user/<id>/relic-id/` (plain text); store the relic
  id.
- Build insights links with the **relic** path:
  `aoe2insights.com/user/relic/<relic_id>/` — the plain `/user/<id>/`
  path expects the insights user id, NOT the relic id.
