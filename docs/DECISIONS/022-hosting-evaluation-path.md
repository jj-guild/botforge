# ADR-022: Hosting evaluation path — VPS (incl. Kapsule trial) vs bare metal + hypervisor

**Status:** Proposed

**Date:** 2026-11-09

**Origin:** architecture committee kickoff
(botforge-infra#132); criteria adopted at the first session
(see `docs/architecture/committee.md`).

## Context

The platform runs today on a **single VPS** (Ubuntu) shared by four
compose environments (`prod`, `test`, `merlin`, `drasah`), deployed by
GitOps state branches through a self-hosted runner, data on bind
mounts under `/opt/botforge/data/<env>/`. No Kubernetes manifest
exists; **Scaleway Kapsule (managed Kubernetes) is a free-trial option
to test K8s**, not the current topology.

The surface keeps expanding (webapp, website front, PyQt app,
Twitch/Matrix bots, self-hosted dev/ops stack — Forgejo, Nextcloud,
OpenBao, ELK) and the owner raised the hosting question: stay on VPS
vs move to **bare metal + hypervisor**. The committee owns the
decision; this ADR records the **evaluation path**, not the final
choice.

## Decision

The hosting decision follows this path:

1. **Criteria** (adopted at kickoff, in order of weight):
   1. total monthly cost (VPS tiers vs hardware CAPEX + power);
   2. ops burden (patching, backups, monitoring, upgrades);
   3. isolation & failure domains (compose projects vs VMs vs K8s
      namespaces);
   4. backup & restore path — bind mounts and hoster-level restore
      are a direct input (botforge-services#338);
   5. capacity headroom against the season-launch sizing
      (botforge-services#315, botforge-services#281;
      `docs/architecture/capacity.md`);
   6. artifact topology — the registry choice
      (botforge-services#329);
   7. Kubernetes appetite — a Kapsule POC informs, never replaces, the
      criteria above.
2. **Inputs land as their issues close** (#338, #329, #315, #281) —
   the evaluation advances with them.
3. **No fixed deadline**: the path is reviewed at every committee
   session; the decision is taken when the inputs allow it, not on a
   calendar.
4. The decision itself will be a **superseding ADR** (Accepted) that
   cites the evidence gathered.

## Alternatives Considered

- **Decide now on cost alone** — rejected: the sizing inputs (#315,
  #281) and the restore-path evidence (#338) are not yet in; a
  calendar-imposed choice would be a guess.
- **Fixed evaluation deadline** — rejected at kickoff ("on verra"):
  a deadline without inputs manufactures urgency; the committee
  reviews the path each session instead.
- **Trial K8s first, decide hosting after** — partially adopted: the
  Kapsule free trial is the cheapest way to test Kubernetes appetite,
  but it is one input among seven, not a prerequisite.

## Consequences

### Positive

- Every future infra issue can cite this ADR instead of re-arguing the
  hosting question.
- The evaluation is evidence-driven and its inputs are named, tracked
  issues.
- The Kapsule trial gives real K8s ops-burden data for free.

### Negative

- The hosting question stays open until the inputs land — the VPS
  topology must absorb growth in the meantime (mitigated by the
  headroom policy in `docs/architecture/capacity.md`).
- "No deadline" can drift; the committee's capacity review (agenda
  item 2) is the standing check against that drift.
