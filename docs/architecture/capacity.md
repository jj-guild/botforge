# Capacity & peak planning

This page is the architecture committee's **capacity and peak planning**
doc (botforge-infra#132): the load curves the platform must absorb, the
sizing rules per component, and the headroom policy. The surfaces are
in [vision.md](vision.md), the topology in [topology.md](topology.md).

It is a **planning frame**, not a measurement report: numbers marked
*TBD* are filled by the sizing inputs
(botforge-services#315, botforge-services#281) or by the first real
peak observed.

## Load model — the peaks

The platform's load is event-driven. Three peak families, in rising
order of severity:

| Peak | Trigger | Shape | Notes |
| --- | --- | --- | --- |
| **Stream** | a streamer goes live with the bot connected | burst of interaction events over hours | Twitch/Fluxer surfaces deferred; sized when built |
| **Tournament** | a tournament opens/joins/rounds | sharp burst (joins + queries) over minutes | first family to size — the most likely early peak |
| **Season launch** | a new season goes live for all players | sustained high load over days | the sizing reference: the platform must absorb it without degradation |

The baseline between peaks is low (a Discord bot platform at rest);
**the topology is sized for the season launch**, not the baseline.

## Sizing rules per component

### MongoDB (durable data)

- Rule: size for **write throughput at peak**, not storage — bot data
  is small; the season-launch join/queue writes are the constraint.
- Per-provider data isolation and per-service DB isolation
  (botforge-services#315, botforge-services#281) are the sizing
  inputs: isolation multiplies databases, which multiplies connection
  pools and working set.
- Baseline numbers: *TBD* (filled from #315).

### Redis (hot state)

- Rule: the workflow hot state is proportional to **concurrent
  in-flight interactions**, not total users (ADR-0005). Size for the
  tournament burst.
- Single-instance today; the headroom policy below decides when a
  second instance (or managed offer) enters the topology.

### ELK (or equivalent)

- Rule: log volume scales with **event count**, so the season-launch
  week is the retention/sizing reference. A lighter equivalent
  (Loki, or a managed offer) is allowed if self-hosting the full
  stack loses the build-vs-buy comparison in [vision.md](vision.md).
- Baseline numbers: *TBD* (deferred component — sized before build).

### Bot processes

- Rule: the 4-process split per env (ADR-0020) is the unit; the
  question is **processes per env at peak**, not hosts. The hosting
  decision (ADR-022) determines whether peak capacity means a bigger
  VPS tier, Kapsule nodes, or a hypervisor host.

## Headroom policy

1. **Measure, then act**: each component gets a warning threshold
   (70 % of its limit) and a critical threshold (90 %) — crossing
   warning opens a committee capacity review; crossing critical is an
   incident.
2. **Default headroom**: every sizing keeps **2× the last observed
   peak** available before the warning threshold.
3. **Peaks are load tests**: the first tournament and the first season
   launch are instrumented (metrics/logs captured) and their numbers
   are written back into this page — the frame becomes a report.

## Review

This page is reviewed at every architecture committee session
([committee.md](committee.md)) — the capacity review is agenda item 2.
