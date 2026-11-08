# Guide — Game provider developer (new game integration)

Add a new game (AoE2 today, any game later) with its external data
providers. Audience: AI session or human developer; the platform
developer reviews.

## The model (ADR-0020)

```
bot-discord ──gRPC──> svc-core ──gRPC──> ext-<provider> process(es) ──HTTPS──> external APIs
```

- The **game module** (`src/botforge/games/<game_key>/` in svc-core)
  holds the game's domain identity and the provider seam.
- The **provider process** (`ext-<name>`) talks to the external API:
  its own rate limiting, caching, secrets and downtime. It never shares
  a process with the bot (ADR-0020 rationale).
- Mods consume the game exclusively through the provider seam —
  profiles, events, results, metadata. The mod core never interprets
  game-specific data formats.

## Capability declaration — the contract that matters

A provider declares what it can do; the platform **degrades cleanly**
around what is missing:

| Capability | Effect when missing |
|---|---|
| `realtime` (lobby/game lifecycle events) | state machine skips LOBBY/GAME states |
| `reliable_results` (trusted match results) | manual result confirmation everywhere |
| `check_map` | map anomalies are not detected |
| `player_stats` | player sheets show mod stats only |

Rules: capabilities are declared, never guessed; a mod must pass its
acceptance tests against a provider with **zero** capabilities; a
capability added later lights up features without mod changes.

## Step-by-step

1. **Spike first**: discover the real API surface (endpoints, auth,
   rate limits, realtime options, result reliability). Write the
   findings in the issue; declare capabilities from evidence.
2. **Contract**: extend `contracts/` with the provider seam
   (`make contracts`); payloads JSON-serializable, errors mapped onto
   the taxonomy, streams for lifecycle events, per-call deadlines.
3. **Game module**: `src/botforge/games/<game_key>/` — identity
   resolution, capability flags, game data (maps/civs catalog hook).
4. **Provider process**: own secrets (never in bot/core), own
   rate-limit Redis keys, own retry policy; health endpoint for the
   deployment battery.
5. **Deployment**: compose/GitOps service (see
   [botforge-infra#89](https://github.com/jj-guild/botforge-infra/issues/89));
   OCI image labels in the same PR ([#144](https://github.com/jj-guild/botforge-services/issues/144)).
6. **Tests**: provider against recorded fixtures/mocks; degradation
   paths (zero-capability) in CI; rate-limit behaviour simulated.
7. **Docs**: `docs/games/<game>/` in the botforge repo — capabilities,
   data sources, known limitations.

## Checklist (from the ladder migration decisions)

- [ ] Capabilities declared from the spike evidence
- [ ] Zero-capability degradation tested
- [ ] Secrets isolated in the provider process
- [ ] Rate limiting + caching owned by the provider
- [ ] Streams (not polling) for lifecycle events when available
- [ ] Grace-period quirks handled adapter-side (e.g. AoE2 lobby-closed
      trap)
- [ ] OCI labels on the image; health endpoint wired

## Review gate

Platform developer review, plus a live check on the test environment:
bot boots with the provider down (degradation), provider recovers
(reattachment), results flow end-to-end.
