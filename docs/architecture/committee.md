# Architecture committee

This page is the home of the **architecture committee** — the recurring
designer + developer session that holds the platform's **long-term
infrastructure vision**: the growing surface (local PyQt app, webapp,
website front, Twitch & Matrix bots, streamer bot flows, self-hosted
dev/ops stack), the **capacity/peak planning**, and the **architecture
diagrams** — so each new component lands in a decided topology instead
of improvising it. It was created by
[botforge-infra#132](https://github.com/jj-guild/botforge-infra/issues/132).

## Role and rules

- **Who**: the game designer and the developer (the two maintainer roles)
  — any other contributor joins when their domain is on the agenda.
- **What it owns**: the target topology
  ([topology.md](topology.md)), the long-term vision and the
  keep/defer/drop surface map ([vision.md](vision.md)), the capacity
  and peak planning ([capacity.md](capacity.md)), and the hosting
  question (VPS — incl. a managed-Kubernetes trial — vs bare metal +
  hypervisor).
- **How it decides**: one decision = one ADR in
  [DECISIONS/](../DECISIONS/README.md), written `Proposed` by the
  session that drafts it and flipped to `Accepted` at review — the
  same lifecycle as every other ADR.
- **How it is tracked**: each session ends with a decision log update
  (ADR) or an explicit "no decision" note in the next agenda.

## Cadence

There is **no fixed calendar cadence**. A session is called when a
trigger fires, typically:

- a new surface or component asks where it lands (the list in
  [vision.md](vision.md) grows);
- a capacity event is coming (tournament, season launch, stream — see
  [capacity.md](capacity.md));
- a hosting input lands (backup/restore evidence, registry choice,
  per-provider sizing data);
- enough drift has accumulated that the vision doc no longer matches
  reality.

The agenda is always the same skeleton, so a session can be called
without preparation:

1. **Vision drift check** — does the inventory below still match
   reality? What changed since last session?
2. **Capacity review** — any peak coming? Any component over its
   headroom?
3. **One deep-dive** — the component or question that triggered the
   session.
4. **Decisions log** — write the ADR(s), or record explicitly that
   none was needed.

## First session (kickoff) — minutes

Held at committee creation (botforge-infra#132). Deliverables of the
issue were split into three doc PRs: this page (committee + minutes),
[topology.md](topology.md) + [vision.md](vision.md), and
[capacity.md](capacity.md) + ADR-022.

### Inventory (what exists, as observed in the repos)

- **Hosting**: a single VPS (Ubuntu), shared by all environments —
  **no Kubernetes manifest exists anywhere**; a managed-Kubernetes
  offer (e.g. Scaleway Kapsule) is a **free-trial option to evaluate**,
  not the current topology.
- **Environments**: `prod`, `test`, `merlin`, `drasah` — one
  docker-compose manifest per env in `botforge-infra/envs/<env>/`
  (bot processes + MongoDB + Redis), data on bind mounts under
  `/opt/botforge/data/<env>/`.
- **Deployment**: GitOps via per-environment state branches — the
  deploy chain applies the pinned state on the hosting through a
  self-hosted runner, with post-deploy verification and automatic
  rollback (see `botforge-infra/docs/GITOPS.md`).
- **Packaging**: private PyPI index per
  [ADR-0017](../DECISIONS/017-packaging-distribution.md); the public
  vs private registry question is open
  (botforge-services#329).

### Surface mapping — keep / defer / drop

The owner's full list (botforge-infra#132), mapped by the committee:

| Component | Call | Notes |
| --- | --- | --- |
| Webapp | **keep** (ADR-0015 boundary) | active surface |
| Website front | **keep** | part of the webapp surface |
| MongoDB / Redis | **keep** | already sized per ADR-0004/0005 |
| Forgejo | **keep** | self-hosted dev stack anchor |
| VPN | **keep** | access layer for the self-hosted stack |
| Ansible / IaC everywhere | **keep** | standing rule, not a new component |
| PyQt app | **defer** | needs its own deep-dive (packaging, data access) |
| Twitch bot | **defer** | core is platform-agnostic (ADR-0001), placement TBD |
| Matrix bot | **defer** | same |
| Streamer bot (streamer & bot flows) | **defer** | sizing unknown |
| Woodpecker (agents/runners) | **defer** | depends on Forgejo placement |
| Nextcloud | **defer** | ops burden to size first |
| ArgoCD | **defer** | only if Kubernetes is chosen |
| OpenBao | **defer** | secrets story TBD |
| ELK (or equivalent) | **defer** | sizing input of capacity.md |
| Fluxer (Discord alternative) | **defer** | POC tracked by botforge-infra#133 |
| Managed Kubernetes (Kapsule) | **option** | free trial — a way to test K8s, not the existing topology |
| Bare metal + hypervisor | **option** | the hosting alternative — see ADR-022 |

No component is dropped at this stage; "defer" items enter the agenda
when their trigger fires.

### Hosting evaluation criteria (adopted)

The VPS vs bare-metal decision path (ADR-022) is evaluated on:

1. **Total monthly cost** — VPS tier(s) vs hardware + power + hosting.
2. **Ops burden** — patching, backups, monitoring, upgrades; what the
   managed offer removes.
3. **Isolation & failure domains** — env separation today (compose
   projects) vs hypervisor VMs or K8s namespaces.
4. **Backup & restore path** — bind mounts and hoster-level restore
   are a direct input (botforge-services#338).
5. **Capacity headroom** — sizing data from per-provider data and
   per-service DB isolation (botforge-services#315,
   botforge-services#281).
6. **Artifact topology** — the registry choice
   (botforge-services#329).
7. **Kubernetes appetite** — Kapsule is free to trial; a POC informs,
   never replaces, the criteria above.

The evaluation has **no fixed deadline**; it advances as its inputs
land and is reviewed at each committee session.
