---
name: troubleshooting
description: The platform's failure memory — every incident already met and fixed (crashes, stuck deploys, flaky checks, architecture violations), per scope. Use when a session hits a problem: check here before diagnosing from scratch, and add the entry when the fix lands.
---

# Troubleshooting — the failure memory

Sessions have no memory; this skill is the platform's. Every incident
already met and fixed lives here, **per scope**, one dated entry per
incident, newest first. Before diagnosing a problem from scratch, check
whether the wall has already been met — and when a session fixes a
problem, the same PR adds the entry (PRIORITY 0 rule 7, botforge
CONVENTIONS.md *Troubleshooting is part of the fix*).

**Entry shape (all four, always):**

```
### <date> — <one-line symptom>
- Symptom: what it looked like (logs, behavior, error)
- Root cause: the real mechanism, found in the evidence
- Fix: what changed (commit/PR reference)
- Guard: the regression test that fails without the fix, by name
```

A fix without its test and its entry is incomplete; an entry without a
guard test is a story, not a memory.

## Scope: platform code (botforge-services)

### 2026-11-23 — The match cards' elo lines vanished silently
- Symptom: the profile panels rendered NO 1v1/TG elo lines under the
  seats, with no error on the bot side; the game-aoe2 log carried
  `GetAccountStats` … `AioRpcError: DEADLINE_EXCEEDED` (merlin 14:27).
- Root cause: `MatchHistorySyncer.account_stats` served missing-board
  PROBES on the gRPC serve path \u2014 one popup means the seat batch
  (8 profiles \u00d7 missing 1v1/TG boards) walked the World's Edge
  API inside the RPC window; the discord side catches the failed
  stats fetch and renders an EMPTY ladder dict, so the degradation is
  silent for the user and noisier only far away in another service's
  logs. An upstream call on a serve path is a design smell: serves
  answer the store, syncs walk the upstream.
- Fix: the serve is store-only; the probes ride the sync flow
  (`sync_account` probes the met players, capped) \u2014
  botforge-services `4577d9f` on #405.
- Guard: `test_account_stats_serves_known_and_unknown` (an unknown
  account reads `known=False` and never triggers an upstream call).

### 2026-11-23 — The abandoned "test" lobbies served forever
- Symptom: `SERVE history` kept listing lobbies the owner quit long
  ago (`lobby test`, one seat); the first seal pass answered
  `nModified: 0` \u2014 nothing matched, the ghosts stayed.
- Root cause: the narrow stale filter ("no completion AND no winner")
  read the world wrong \u2014 the abandoned captures DO carry a
  completion timestamp or a self-reported solo outcome, so the $or
  matched none of them. Read the actual documents' shape (the live
  slow-query log printed the docs scanned) before widening a
  filter.
- Fix: a VALID decision reads "finished + at least one winner + at
  least two profiles", and any capture older than a day without one
  seals `invalid` (the serving skips it, the raw stays) \u2014
  botforge-services `e63d7c2` + `b2abb69` on #405.
- Guard: `test_stale_never_played_match_seals_and_never_serves`,
  `test_stale_solo_capture_with_completion_still_seals` and
  `test_recent_ongoing_match_still_serves` (the young capture stays).

### 2026-11-17 — CI red at random: the Liquipedia battery 429s
- Symptom: the `External services (real provider batteries)` CI job
  fails intermittently on `liquipedia :: maps-query-shape` with
  `429 Too Many Requests` — any PR's CI goes red for an external
  reason (botforge-services#397).
- Root cause: the throttle is IP-level (GitHub hosted runners share
  IPs), not title-count-level — the one-page battery still got 429'd
  (~11% of the post-fix runs), and the observed 429s carry **no
  `Retry-After` header**, so the retry path slept a blind 30 s floor
  and retried into the same wall. Read the failed run logs before
  designing the fix: the absent header was the deciding fact.
- Fix: no retry when `Retry-After` is absent/unparseable — the circuit
  opens on the first 429, zero further traffic, fail fast; the
  battery's verdict stays an honest FAIL with a message naming the
  external rate limit (botforge-services#406).
- Guard: `test_429_without_retry_after_opens_the_circuit_without_retrying`
  (one call only), `test_battery_fails_with_clear_rate_limit_detail_on_429`
  and `..._on_open_circuit` (honest FAIL + rate-limit detail).

## Scope: deploy & infra (botforge-infra, hosting, runners)

### 2026-11-23 — Redis MISCONF: one failed bgsave, the whole env stops writing
- Symptom: `stats cache write failed` warnings storm; Redis answers
  `MISCONF … unable to persist to disk … stop-writes-on-bgsave-error`
  \u2014 EVERY write on the environment is refused (rate limits,
  caches, coordination).
- Root cause: the env Redis is a PURE cache (every key TTL'd, nothing
  source-of-truth) but the image's default RDB snapshotting served
  nothing \u2014 and its `bgsave` fork is the first casualty of any
  disk or overcommit hiccup, turning an irrelevant persistence into
  an env-wide write blackout via `stop-writes-on-bgsave-error`.
- Fix: the env Redises run with persistence OFF entirely
  (`--save "" --appendonly no`) \u2014 botforge-infra `008c38e`
  (merlin) and #152 (test); prod deliberately untouched (not in sync
  with the other envs, needs its own review \u2014 infra#151).
- Guard: none testable (a compose flag); the mode of failure is
  structurally removed \u2014 no `bgsave` can exist to fail, whatever
  the disk says.

### 2026-10-16 — Hours of hypotheses on a silent failure
- Symptom: a flow silently does nothing; no error, no logs.
- Root cause: the answer was in `/logs <env>` all along — one grep beats an afternoon of hypotheses.
- Fix: check `/logs <env>` before forming any hypothesis (habit, not code).
- Guard: none (process lesson, not a regression test).

(The concurrency-zombie trap — a run waiting for an environment approval
holding the deploy group forever — is documented with its diagnosis
procedure in the
[diagnose-deploy](../diagnose-deploy/SKILL.md) skill.)

## Scope: docs & CI (botforge, workflows, checks)

No entry yet — the first fixed incident lands here.

## Rules

- **One home**: the entry lives in this skill; other docs link to it,
  never copy it (CONVENTIONS.md, *one home per rule*).
- **Root cause from evidence**: an entry states the mechanism found in
  the logs, not a guess (CONVENTIONS.md, *Diagnose before blaming the
  infrastructure*).
- **Scope first**: pick the section matching where the failure
  manifested; cross-scope incidents get one entry in the primary scope
  and links from the others.
- **Pruning is healthy**: an entry whose guard test was removed, or
  describing a mechanism that no longer exists, is deleted in the same
  PR that obsolete it — this is a memory, not a graveyard.
